#!/usr/bin/env python3
"""Safely dry-run or execute one routed Codex worker with a private audit log."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

from route_task import LEVELS, SCOPES, STAGES, TASK_TYPES, route_task


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task")
    parser.add_argument("--stage", choices=STAGES)
    parser.add_argument("--task-type", choices=TASK_TYPES, default="auto")
    parser.add_argument("--ambiguity", choices=LEVELS, default="medium")
    parser.add_argument("--stakes", choices=LEVELS, default="medium")
    parser.add_argument("--scope", choices=SCOPES, default="medium")
    parser.add_argument("--decomposable", action="store_true")
    parser.add_argument("--urgent", action="store_true")
    parser.add_argument("--workdir")
    parser.add_argument("--skip-git-repo-check", action="store_true")
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--execute", action="store_true", help="Execute one worker; otherwise only write a dry-run log")
    parser.add_argument("--capture-content", action="store_true", help="Opt in to storing full prompt and output in the private log")
    return parser.parse_args()


def fingerprint(text: str) -> dict:
    return {"sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(), "characters": len(text)}


def safe_route(route: dict, task: str, capture_content: bool) -> dict:
    copy = json.loads(json.dumps(route))
    copy.pop("task", None)
    copy["task_fingerprint"] = fingerprint(task)
    if capture_content:
        copy["task"] = task
    return copy


def create_private_log(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(fd, payload)
    finally:
        os.close(fd)


def replace_private_log(path: Path, record: dict) -> None:
    payload = json.dumps(record, ensure_ascii=False, indent=2) + "\n"
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(payload)
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def parse_reported_total_tokens(stderr: str) -> int | None:
    match = re.search(r"tokens used\s+([0-9][0-9.,]*)", stderr.lower())
    if not match:
        return None
    digits = re.sub(r"[^0-9]", "", match.group(1))
    return int(digits) if digits else None


def classify_runtime_status(returncode: int, stderr: str, fast_requested: bool) -> tuple[str, str]:
    stderr_lower = stderr.lower()
    if "requires a newer version of codex" in stderr_lower:
        return "runtime-upgrade-required", "not-observed"
    fast_rejected = fast_requested and any(
        marker in stderr_lower
        for marker in ("unsupported service tier", "invalid service tier", "fast mode is not available", "unknown service tier")
    )
    if fast_rejected:
        return "speed-request-rejected", "rejected"
    if returncode == 0:
        speed = "request-accepted-unconfirmed" if fast_requested else "standard-requested"
        return "worker-output-ready-gates-pending", speed
    return "worker-execution-failed", "not-observed"


def main() -> int:
    args = parse_args()
    created_at = datetime.now(timezone.utc).isoformat()
    try:
        route = route_task(
            args.task,
            task_type=args.task_type,
            stage=args.stage,
            ambiguity=args.ambiguity,
            stakes=args.stakes,
            scope=args.scope,
            decomposable=args.decomposable,
            urgent=args.urgent,
            workdir=args.workdir,
            skip_git_repo_check=args.skip_git_repo_check,
        )
    except Exception as exc:
        record = {
            "created_at": created_at,
            "status": "routing-failed",
            "task_fingerprint": fingerprint(args.task),
            "error": {"type": type(exc).__name__, "message": str(exc)},
        }
        try:
            create_private_log(args.log, record)
        except FileExistsError:
            print(f"Refusing to overwrite existing log: {args.log}", file=sys.stderr)
            return 2
        print(json.dumps(record, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2

    record = {
        "created_at": created_at,
        "status": "dry-run" if not args.execute else "started",
        "executed": False,
        "route": safe_route(route, args.task, args.capture_content),
        "shell_command": shlex.join(route["codex_command"]),
        "content_capture_enabled": args.capture_content,
    }
    try:
        create_private_log(args.log, record)
    except FileExistsError:
        print(f"Refusing to overwrite existing log: {args.log}", file=sys.stderr)
        return 2

    if not args.execute:
        print(json.dumps(record, ensure_ascii=False, indent=2))
        return 0

    if route["orchestration"] != "single-agent":
        record["status"] = "external-orchestration-required"
        record["reason"] = (
            "This safe worker runner does not degrade staged, reviewed, or Ultra routes to one call. "
            "Use the skill workflow to run the recorded orchestration plan and gates."
        )
        replace_private_log(args.log, record)
        print(json.dumps(record, ensure_ascii=False, indent=2), file=sys.stderr)
        return 4

    started = time.monotonic()
    completed = subprocess.run(
        route["codex_command"],
        input=args.task,
        text=True,
        capture_output=True,
        check=False,
    )
    status, speed_effective = classify_runtime_status(
        completed.returncode, completed.stderr, route["speed_requested"] == "fast"
    )
    record["executed"] = True
    record["status"] = status
    record["runtime"] = {
        "exit_code": completed.returncode,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "reported_total_tokens": parse_reported_total_tokens(completed.stderr),
        "stdout": completed.stdout if args.capture_content else fingerprint(completed.stdout),
        "stderr": completed.stderr if args.capture_content else fingerprint(completed.stderr),
        "speed_effective": speed_effective,
        "automatic_retry": False,
        "quality_gates_complete": False,
    }
    replace_private_log(args.log, record)
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)
    print(json.dumps({"status": record["status"], "log": str(args.log)}, ensure_ascii=False), file=sys.stderr)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
