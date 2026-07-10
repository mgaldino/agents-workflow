#!/usr/bin/env python3
"""Unit tests for adaptive Codex routing."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from route_task import MODEL_LUNA, MODEL_SOL, MODEL_TERRA, POLICY, route_task
from run_routed_task import classify_runtime_status, parse_reported_total_tokens


class RouterTests(unittest.TestCase):
    def test_mechanical_routes_to_luna_fast(self):
        route = route_task("Extrair campos do JSON para CSV", task_type="mechanical", stage="internal", ambiguity="low", stakes="low")
        self.assertEqual(route["model"], MODEL_LUNA)
        self.assertEqual(route["effort"], "low")
        self.assertEqual(route["speed_requested"], "fast")

    def test_scoped_coding_routes_to_terra_fast(self):
        route = route_task("Corrigir bug no parser e rodar testes", task_type="coding", stage="internal", ambiguity="low", stakes="medium", scope="small")
        self.assertEqual(route["model"], MODEL_TERRA)
        self.assertEqual(route["effort"], "medium")
        self.assertEqual(route["speed_requested"], "fast")

    def test_formal_routes_to_sol_xhigh(self):
        route = route_task("Verificar prova formal", task_type="formal", stage="final", ambiguity="high", stakes="high")
        self.assertEqual(route["model"], MODEL_SOL)
        self.assertEqual(route["effort"], "xhigh")
        self.assertEqual(route["speed_requested"], "standard")
        self.assertTrue(route["quality_floor"]["adversarial_review"])
        self.assertEqual(route["orchestration"], "single-agent-plus-adversarial-review")
        self.assertEqual(route["orchestration_plan"]["review"]["review_mode"], "adversarial")

    def test_final_analysis_requires_review(self):
        route = route_task("Finalizar análise causal para submissão", task_type="analysis", stage="final", ambiguity="medium", stakes="high")
        self.assertEqual(route["model"], MODEL_SOL)
        self.assertTrue(route["quality_floor"]["independent_review"])
        self.assertEqual(route["quality_floor"]["critical_errors_allowed"], 0)

    def test_ultra_requires_large_decomposable_task(self):
        small = route_task("Revisar paper", task_type="review", stage="final", scope="small", decomposable=True)
        large = route_task("Revisar paper", task_type="review", stage="final", scope="large", decomposable=True)
        self.assertEqual(small["orchestration"], "single-agent-plus-independent-review")
        self.assertEqual(large["orchestration"], "ultra")

    def test_large_batch_uses_staged_orchestration(self):
        route = route_task("Extrair campos de 500 PDFs", task_type="mechanical", stage="internal", scope="large")
        self.assertEqual(route["orchestration"], "staged-pilot-batch-audit")
        self.assertEqual(route["orchestration_plan"]["pilot"]["model"], MODEL_TERRA)
        self.assertEqual(route["orchestration_plan"]["batch"]["model"], MODEL_LUNA)
        self.assertTrue(route["orchestration_plan"]["audit"]["independent_sample"])

    def test_fast_command_is_explicit(self):
        route = route_task("Classificar registros", task_type="classification", stage="internal", ambiguity="low")
        command = route["codex_command"]
        self.assertIn('service_tier="fast"', command)
        self.assertIn("fast_mode", command)

    def test_skip_git_repo_check_is_opt_in(self):
        normal = route_task("Extrair registros", task_type="mechanical")
        skipped = route_task("Extrair registros", task_type="mechanical", skip_git_repo_check=True)
        self.assertNotIn("--skip-git-repo-check", normal["codex_command"])
        self.assertIn("--skip-git-repo-check", skipped["codex_command"])

    def test_route_does_not_invent_pass_probability(self):
        route = route_task("Fazer uma tarefa ambígua")
        self.assertEqual(route["benchmark_status"], "uncalibrated")
        self.assertNotIn("pass_probability", route)
        self.assertEqual(route["optimization_status"], "conservative-heuristic-not-empirical-optimum")

    def test_task_is_delivered_by_stdin_not_cli_option(self):
        route = route_task("--help", task_type="mechanical", stage="internal", ambiguity="low", stakes="low")
        self.assertEqual(route["codex_command"][-1], "-")
        self.assertNotIn("--help", route["codex_command"])
        self.assertEqual(route["prompt_delivery"], "stdin")

    def test_high_risk_dominates_mechanical_efficiency(self):
        route = route_task("Classificar documentos legais", task_type="classification", stage="high-risk", ambiguity="low", stakes="low")
        self.assertEqual(route["model"], MODEL_SOL)
        self.assertEqual(route["effort"], "xhigh")
        self.assertTrue(route["quality_floor"]["adversarial_review"])

    def test_lexical_normalization_and_boundaries(self):
        inference = route_task("Fazer inferência sobre parâmetros")
        proofread = route_task("Proofread this short paragraph")
        self.assertEqual(inference["inputs"]["task_type"], "analysis")
        self.assertEqual(proofread["inputs"]["task_type"], "writing")

    def test_invalid_api_input_is_rejected(self):
        with self.assertRaises(ValueError):
            route_task("Tarefa", task_type="nonsense")

    def test_speed_status_follows_requested_speed(self):
        route = route_task("Revisar prova urgente", task_type="formal", stage="internal", urgent=True)
        self.assertEqual(route["speed_requested"], "fast")
        self.assertEqual(route["speed_support_status"], "catalog-dependent-or-unverified")

    def test_policy_file_is_canonical(self):
        route = route_task("Extrair registros", task_type="mechanical")
        self.assertEqual(route["policy_version"], POLICY["policy_version"])
        self.assertEqual(route["objective_order"], POLICY["objective_order"])
        self.assertEqual(route["escalation_order"], POLICY["escalation_order"])

    def test_portuguese_risk_flexions_are_inferred(self):
        for text in ("Classificar documentos legais", "Revisar pareceres jurídicos", "Analisar laudos médicos"):
            route = route_task(text, ambiguity="low", stakes="low")
            self.assertEqual(route["inputs"]["stage"], "high-risk", text)
            self.assertEqual(route["model"], MODEL_SOL, text)
            self.assertEqual(route["orchestration_plan"]["review"]["review_mode"], "adversarial", text)

    def test_high_risk_large_batch_has_adversarial_audit(self):
        route = route_task(
            "Classificar documentos legais", task_type="classification", stage="high-risk",
            ambiguity="low", stakes="low", scope="large",
        )
        self.assertEqual(route["orchestration"], "staged-pilot-batch-audit")
        self.assertEqual(route["orchestration_plan"]["audit"]["review_mode"], "adversarial")
        self.assertEqual(route["orchestration_plan"]["audit"]["model"], MODEL_SOL)

    def test_dry_run_log_is_private_redacted_and_exclusive(self):
        runner = Path(__file__).with_name("run_routed_task.py")
        secret = "SEGREDO-NAO-REGISTRAR"
        with tempfile.TemporaryDirectory() as temp_dir:
            log = Path(temp_dir) / "route.json"
            command = [
                sys.executable, str(runner), secret, "--task-type", "mechanical",
                "--stage", "internal", "--ambiguity", "low", "--stakes", "low",
                "--log", str(log),
            ]
            first = subprocess.run(command, text=True, capture_output=True, check=False)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(os.stat(log).st_mode & 0o777, 0o600)
            payload = log.read_text(encoding="utf-8")
            self.assertNotIn(secret, payload)
            self.assertEqual(json.loads(payload)["status"], "dry-run")
            second = subprocess.run(command, text=True, capture_output=True, check=False)
            self.assertNotEqual(second.returncode, 0)

    def test_runtime_upgrade_error_is_distinguished(self):
        status, speed = classify_runtime_status(
            1,
            "The gpt-5.6-terra model requires a newer version of Codex.",
            True,
        )
        self.assertEqual(status, "runtime-upgrade-required")
        self.assertEqual(speed, "not-observed")

    def test_cli_token_usage_is_parsed(self):
        self.assertEqual(parse_reported_total_tokens("tokens used\n14.867\n"), 14867)
        self.assertIsNone(parse_reported_total_tokens("no usage here"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
