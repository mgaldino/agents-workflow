#!/usr/bin/env python3
"""Deterministic, conservative routing for Codex tasks."""

from __future__ import annotations

import argparse
import json
import re
import shlex
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SKILL_DIR = Path(__file__).resolve().parents[1]
POLICY = json.loads((SKILL_DIR / "references" / "routing-policy.json").read_text(encoding="utf-8"))
CAPABILITIES = json.loads((SKILL_DIR / "references" / "model-capabilities.json").read_text(encoding="utf-8"))
MODEL_LUNA = "gpt-5.6-luna"
MODEL_TERRA = "gpt-5.6-terra"
MODEL_SOL = "gpt-5.6-sol"
for required_model in (MODEL_LUNA, MODEL_TERRA, MODEL_SOL):
    if required_model not in CAPABILITIES["models"]:
        raise RuntimeError(f"Missing model capability: {required_model}")

TASK_TYPES = (
    "auto",
    "mechanical",
    "classification",
    "coding",
    "analysis",
    "research",
    "writing",
    "review",
    "formal",
)
LEVELS = ("low", "medium", "high")
SCOPES = ("small", "medium", "large")
STAGES = ("exploratory", "internal", "final", "high-risk")


def normalized(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return " ".join(text.lower().split())


def contains_any(text: str, terms: Iterable[str]) -> bool:
    for term in terms:
        normalized_term = normalized(term)
        if re.search(rf"(?<!\w){re.escape(normalized_term)}(?!\w)", text):
            return True
    return False


TYPE_TERMS = {
    "formal": (
        "prova", "proof", "teorema", "theorem", "lemma", "lean", "equilibrio",
        "game theory", "modelo formal", "derivacao formal",
    ),
    "review": (
        "parecer", "peer review", "referee", "auditar", "audit", "critique",
        "revisao metodologica", "review the paper",
    ),
    "research": (
        "literatura", "literature review", "pesquisa profunda", "deep research",
        "fontes", "evidencias", "research question",
    ),
    "analysis": (
        "analise de dados", "regressao", "estimador", "causal", "did", "sdid",
        "inferencia", "inference", "estatistica", "dataset", "dados",
    ),
    "coding": (
        "implementar", "implementation", "bug", "codigo", "code", "python", "rscript",
        "script r", "funcao r", "tidyverse", "ggplot", "script", "cli", "app", "teste", "test", "refactor",
    ),
    "classification": (
        "classificar", "classification", "rotular", "label", "categorizar", "triagem",
    ),
    "mechanical": (
        "extrair", "extract", "converter", "formatar", "renomear", "copiar",
        "transformar", "schema", "csv", "json", "contar", "ordenar",
    ),
    "writing": (
        "escrever", "reescrever", "write", "rewrite", "editar texto", "paper",
        "relatorio", "manuscrito", "introducao", "proofread", "paragraph", "paragrafo",
    ),
}


@dataclass(frozen=True)
class RouteInputs:
    task_type: str
    stage: str
    ambiguity: str
    stakes: str
    scope: str
    decomposable: bool
    urgent: bool


def infer_task_type(text: str) -> tuple[str, float, list[str]]:
    matches = [name for name, terms in TYPE_TERMS.items() if contains_any(text, terms)]
    if not matches:
        return "coding", 0.45, ["No task-class keyword matched; conservative general-work default."]
    priority = ("formal", "review", "research", "analysis", "coding", "classification", "mechanical", "writing")
    chosen = next(name for name in priority if name in matches)
    confidence = 0.9 if len(matches) == 1 else 0.72
    return chosen, confidence, [f"Matched task classes: {', '.join(matches)}."]


def infer_stage(text: str) -> str:
    high_risk_terms = (
        "alto risco", "high-risk", "producao", "production", "deploy",
        "legal", "legais", "juridico", "juridica", "juridicos", "juridicas",
        "medico", "medica", "medicos", "medicas", "medical", "financial decision",
    )
    if contains_any(text, high_risk_terms):
        return "high-risk"
    if contains_any(text, ("submeter", "submission", "entrega final", "final deliverable", "cliente", "publicar", "publication")):
        return "final"
    if contains_any(text, ("explorar", "brainstorm", "rascunho inicial", "diagnostico inicial", "sketch")):
        return "exploratory"
    return "internal"


def build_quality_floor(stage: str, task_type: str, stakes: str) -> dict:
    stage_policy = POLICY["stages"][stage]
    mean_min = stage_policy["rubric_mean_min"]
    dimension_min = stage_policy["essential_dimension_min"]
    independent = stage_policy["independent_review"] or (
        POLICY["independent_review_when_stakes_high"] and stakes == "high"
    )
    adversarial = stage_policy.get("adversarial_review", False) or (
        task_type == "formal" and stage in {"final", "high-risk"}
    )
    gate_profile = {
        "mechanical": "mechanical-transformation",
        "classification": "classification",
        "coding": "code-and-pipeline",
        "analysis": "analysis-and-causal-inference",
        "research": "papers-reports-and-reviews",
        "writing": "papers-reports-and-reviews",
        "review": "papers-reports-and-reviews",
        "formal": "formal-models-and-proofs",
    }[task_type]
    return {
        "critical_errors_allowed": stage_policy["critical_errors_allowed"],
        "all_mandatory_gates_must_pass": True,
        "rubric_mean_min_5": mean_min,
        "essential_dimension_min_5": dimension_min,
        "independent_review": independent,
        "adversarial_review": adversarial,
        "gate_profile": gate_profile,
    }


def choose_route(inputs: RouteInputs, inference_confidence: float) -> tuple[str, str, str, str, list[str]]:
    reasons: list[str] = []

    if inputs.stage == "high-risk" or inputs.stakes == "high":
        model = MODEL_SOL
        effort = "xhigh"
        reasons.append("High-risk stage or high stakes dominates efficiency routing and requires Sol.")
    elif inputs.task_type in {"mechanical", "classification"} and inputs.ambiguity != "high":
        model = MODEL_LUNA
        effort = "low" if inputs.task_type == "mechanical" else "medium"
        reasons.append("Clear or repeatable work is eligible for Luna.")
    elif (
        inputs.task_type in {"formal", "review", "research"}
        or inputs.ambiguity == "high"
        or (inputs.stage == "final" and inputs.task_type in {"analysis", "writing"})
    ):
        model = MODEL_SOL
        effort = "high"
        if inputs.stage == "high-risk" or (inputs.ambiguity == "high" and inputs.scope == "large") or inputs.task_type == "formal":
            effort = "xhigh"
        reasons.append("Ambiguity, stakes, or substantive judgment requires Sol.")
    else:
        model = MODEL_TERRA
        effort = "medium"
        if inputs.scope == "large" or inputs.ambiguity == "medium" or inputs.task_type == "analysis":
            effort = "high"
        reasons.append("Everyday implementation or analysis fits Terra.")

    if POLICY["conservative_when_uncertain"] and inference_confidence < 0.6:
        if model == MODEL_LUNA:
            model, effort = MODEL_TERRA, "medium"
        elif model == MODEL_TERRA:
            model, effort = MODEL_SOL, "high"
        reasons.append("Low routing confidence triggered a conservative upward shift.")

    fast_preferred_models = set(POLICY["fast_preferred_models"])
    speed = "fast" if model in fast_preferred_models else ("fast" if inputs.urgent else "standard")
    if model in fast_preferred_models:
        reasons.append("User policy requests Fast by default for Luna and Terra.")

    orchestration = "single-agent"
    if inputs.scope == "large" and inputs.task_type in {"mechanical", "classification"}:
        orchestration = "staged-pilot-batch-audit"
        reasons.append("Large repeatable workload requires a pilot, batch execution, and audited sample.")
    elif inputs.decomposable and inputs.scope == "large" and inputs.task_type in {"coding", "analysis", "research", "review", "formal"}:
        orchestration = "ultra"
        reasons.append("Large task has meaningful independent workstreams.")
    elif inputs.stage == "high-risk" or (inputs.task_type == "formal" and inputs.stage == "final"):
        orchestration = "single-agent-plus-adversarial-review"
        reasons.append("High-risk or final formal work requires a separate adversarial reviewer.")
    elif inputs.stage == "final":
        orchestration = "single-agent-plus-independent-review"
        reasons.append("Final work requires a separate reviewer even without parallel decomposition.")

    escalation_target = {
        MODEL_LUNA: "increase effort, then upgrade to gpt-5.6-terra",
        MODEL_TERRA: "increase effort, then upgrade to gpt-5.6-sol",
        MODEL_SOL: "increase effort up to max, then add independent review or Ultra if decomposable",
    }[model]
    return model, effort, speed, orchestration, reasons + [f"Model-specific escalation target: {escalation_target}."]


def build_codex_command(
    route: dict,
    workdir: str | None = None,
    skip_git_repo_check: bool = False,
) -> list[str]:
    command = [
        "codex", "exec", "--ephemeral", "--model", route["model"],
        "-c", f'model_reasoning_effort="{route["effort"]}"',
    ]
    if route["speed_requested"] == "fast":
        command.extend(["-c", 'service_tier="fast"', "--enable", "fast_mode"])
    if workdir:
        command.extend(["--cd", workdir])
    if skip_git_repo_check:
        command.append("--skip-git-repo-check")
    command.append("-")
    return command


def route_task(
    task: str,
    *,
    task_type: str = "auto",
    stage: str | None = None,
    ambiguity: str = "medium",
    stakes: str = "medium",
    scope: str = "medium",
    decomposable: bool = False,
    urgent: bool = False,
    workdir: str | None = None,
    skip_git_repo_check: bool = False,
) -> dict:
    if task_type not in TASK_TYPES:
        raise ValueError(f"Invalid task_type: {task_type}")
    if stage is not None and stage not in STAGES:
        raise ValueError(f"Invalid stage: {stage}")
    if ambiguity not in LEVELS:
        raise ValueError(f"Invalid ambiguity: {ambiguity}")
    if stakes not in LEVELS:
        raise ValueError(f"Invalid stakes: {stakes}")
    if scope not in SCOPES:
        raise ValueError(f"Invalid scope: {scope}")
    text = f" {normalized(task)} "
    notes: list[str] = []
    if task_type == "auto":
        task_type, confidence, inferred_notes = infer_task_type(text)
        notes.extend(inferred_notes)
    else:
        confidence = 0.95
        notes.append("Task class supplied explicitly.")
    actual_stage = stage or infer_stage(text)
    if stage is None:
        notes.append(f"Stage inferred as {actual_stage}.")

    inputs = RouteInputs(task_type, actual_stage, ambiguity, stakes, scope, decomposable, urgent)
    model, effort, speed, orchestration, reasons = choose_route(inputs, confidence)
    quality_floor = build_quality_floor(actual_stage, task_type, stakes)
    route = {
        "policy_version": POLICY["policy_version"],
        "objective_order": POLICY["objective_order"],
        "escalation_order": POLICY["escalation_order"],
        "task": task,
        "inputs": asdict(inputs),
        "model": model,
        "effort": effort,
        "speed_requested": speed,
        "speed_effective": "not-observed",
        "speed_support_status": "catalog-dependent-or-unverified" if speed == "fast" else "not-requested",
        "orchestration": orchestration,
        "quality_floor": quality_floor,
        "routing_confidence": round(confidence, 2),
        "benchmark_status": "uncalibrated",
        "optimization_status": "conservative-heuristic-not-empirical-optimum",
        "prompt_delivery": "stdin",
        "assumptions": notes,
        "reasons": reasons,
    }
    if orchestration == "staged-pilot-batch-audit":
        route["orchestration_plan"] = {
            "pilot": {"model": MODEL_TERRA if ambiguity != "high" else MODEL_SOL, "effort": "high"},
            "batch": {"model": model, "effort": effort, "speed_requested": speed},
            "audit": {
                "model": MODEL_SOL if quality_floor["adversarial_review"] else MODEL_TERRA,
                "effort": "xhigh" if quality_floor["adversarial_review"] else "high",
                "independent_sample": True,
                "review_mode": "adversarial" if quality_floor["adversarial_review"] else "independent",
            },
        }
    elif orchestration in {"single-agent-plus-independent-review", "single-agent-plus-adversarial-review"}:
        route["orchestration_plan"] = {
            "implementation": {"model": model, "effort": effort},
            "review": {
                "model": MODEL_SOL,
                "effort": "xhigh" if quality_floor["adversarial_review"] else "high",
                "must_be_independent": True,
                "review_mode": "adversarial" if quality_floor["adversarial_review"] else "independent",
            },
        }
    elif orchestration == "ultra":
        route["orchestration_plan"] = {
            "workers": "Split only into independent task-specific workstreams.",
            "integrator": {"model": MODEL_SOL, "effort": effort},
            "review": {
                "model": MODEL_SOL,
                "effort": "xhigh" if quality_floor["adversarial_review"] else "high",
                "must_be_independent": True,
                "review_mode": "adversarial" if quality_floor["adversarial_review"] else "independent",
            },
        }
    route["codex_command"] = build_codex_command(route, workdir, skip_git_repo_check)
    return route


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", nargs="?", help="Task text to route")
    parser.add_argument("--task-file", type=Path)
    parser.add_argument("--task-type", choices=TASK_TYPES, default="auto")
    parser.add_argument("--stage", choices=STAGES)
    parser.add_argument("--ambiguity", choices=LEVELS, default="medium")
    parser.add_argument("--stakes", choices=LEVELS, default="medium")
    parser.add_argument("--scope", choices=SCOPES, default="medium")
    parser.add_argument("--decomposable", action="store_true")
    parser.add_argument("--urgent", action="store_true")
    parser.add_argument("--workdir")
    parser.add_argument("--skip-git-repo-check", action="store_true")
    parser.add_argument("--shell-command", action="store_true")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    task = args.task_file.read_text(encoding="utf-8") if args.task_file else args.task
    if not task:
        raise SystemExit("Provide task text or --task-file")
    route = route_task(
        task,
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
    rendered = shlex.join(route["codex_command"]) if args.shell_command else json.dumps(route, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
