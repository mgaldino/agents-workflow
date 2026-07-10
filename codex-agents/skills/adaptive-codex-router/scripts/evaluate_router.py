#!/usr/bin/env python3
"""Evaluate deterministic routes on representative task scenarios."""

from __future__ import annotations

import json
from pathlib import Path

from route_task import route_task


SCENARIOS = [
    {
        "name": "luna-extraction",
        "task": "Extrair três campos de cada registro JSON e salvar CSV validando o schema.",
        "kwargs": {"stage": "internal", "task_type": "mechanical", "ambiguity": "low", "stakes": "low", "scope": "large"},
        "expected": {"model": "gpt-5.6-luna", "effort": "low", "speed_requested": "fast", "orchestration": "staged-pilot-batch-audit"},
    },
    {
        "name": "luna-classification",
        "task": "Classificar 500 resumos em cinco categorias com labels fechados.",
        "kwargs": {"stage": "internal", "task_type": "classification", "ambiguity": "low", "stakes": "medium", "scope": "large"},
        "expected": {"model": "gpt-5.6-luna", "effort": "medium", "speed_requested": "fast", "orchestration": "staged-pilot-batch-audit"},
    },
    {
        "name": "terra-python-fix",
        "task": "Corrigir um bug delimitado no parser Python e rodar os testes existentes.",
        "kwargs": {"stage": "internal", "task_type": "coding", "ambiguity": "low", "stakes": "medium", "scope": "small"},
        "expected": {"model": "gpt-5.6-terra", "effort": "medium", "speed_requested": "fast"},
    },
    {
        "name": "terra-analysis",
        "task": "Estimar modelos descritivos em R e produzir tabela reproduzível para uso interno.",
        "kwargs": {"stage": "internal", "task_type": "analysis", "ambiguity": "medium", "stakes": "medium", "scope": "medium"},
        "expected": {"model": "gpt-5.6-terra", "effort": "high", "speed_requested": "fast"},
    },
    {
        "name": "sol-formal",
        "task": "Verificar uma prova de unicidade de equilíbrio e checar casos-limite.",
        "kwargs": {"stage": "final", "task_type": "formal", "ambiguity": "high", "stakes": "high", "scope": "medium"},
        "expected": {"model": "gpt-5.6-sol", "effort": "xhigh", "speed_requested": "standard", "orchestration": "single-agent-plus-adversarial-review"},
    },
    {
        "name": "sol-ultra-review",
        "task": "Produzir parecer completo de um paper com revisão de identificação, estimação e exposição.",
        "kwargs": {"stage": "final", "task_type": "review", "ambiguity": "high", "stakes": "high", "scope": "large", "decomposable": True},
        "expected": {"model": "gpt-5.6-sol", "effort": "xhigh", "speed_requested": "standard", "orchestration": "ultra"},
    },
]


def main() -> int:
    results = []
    for scenario in SCENARIOS:
        route = route_task(scenario["task"], **scenario["kwargs"])
        mismatches = {
            key: {"expected": value, "actual": route.get(key)}
            for key, value in scenario["expected"].items()
            if route.get(key) != value
        }
        results.append({"name": scenario["name"], "pass": not mismatches, "mismatches": mismatches, "route": route})
    summary = {"passed": sum(item["pass"] for item in results), "total": len(results), "results": results}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["passed"] == summary["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
