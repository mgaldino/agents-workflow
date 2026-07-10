---
name: adaptive-codex-router
description: Route Codex tasks to an appropriate model, reasoning effort, speed preference, and orchestration pattern using a quality-first lexicographic policy. Use when choosing among GPT-5.6 Sol, Terra, or Luna; deciding low, medium, high, xhigh, max, or Ultra; reducing latency and token or credit use without lowering an explicit quality floor; preparing safe codex exec commands; or calibrating model choices on representative tasks.
---

# Adaptive Codex Router

Apply a conservative routing heuristic until benchmark evidence exists. After calibration, choose among configurations that preserve the task-specific quality floor, prioritizing quality first, speed second, and token or credit use third.

## Route a task

1. Identify the deliverable stage: `exploratory`, `internal`, `final`, or `high-risk`.
2. Identify the task type, stakes, ambiguity, scope, urgency, and whether meaningful parallel decomposition exists.
3. Run `scripts/route_task.py` with the task text and any known overrides.
4. Inspect the generated quality contract, assumptions, route confidence, and speed-support warning.
5. Apply the recommendation before starting a new root task. For an already-running root task, use the route for a new `codex exec`, a configured worker, or the next task; do not claim to have changed the current model retroactively.
6. Execute the relevant gates in `references/quality-gates.md`.
7. Deliver only after all hard gates pass. On failure, repair the failed part and escalate one step: effort first, model second, independent review or Ultra third.

Example:

```bash
python3 scripts/route_task.py \
  "Implementar uma correção Python pequena e rodar os testes" \
  --stage internal --shell-command
```

Use `scripts/run_routed_task.py` only when the user has authorized execution. It defaults to dry-run, sends prompts through stdin, records a private `0600` JSON log with content redacted by default, and never retries a failed mutating task automatically. It executes only `single-agent` worker routes; orchestrate staged, reviewed, or Ultra plans with separate workers and gates rather than degrading them silently.
Add `--skip-git-repo-check` only for a directory deliberately chosen for non-repository work or when trust has been checked separately; never apply it silently.

## Apply the policy

- Treat zero critical errors and all mandatory gates as non-compensatory constraints.
- Prefer Luna for clear, repeatable, mechanically verifiable work.
- Prefer Terra for ordinary implementation, analysis, synthesis, and tool use.
- Prefer Sol for ambiguous, high-value, open-ended, formal, causal, or publication-facing work.
- Prefer Fast for Luna and Terra by default. Record `requested` and `effective` speed separately. If the active catalog rejects Fast, stop, disclose the rejection, and relaunch at an accepted speed only when doing so cannot duplicate side effects or after explicit confirmation.
- For large mechanical or classification batches, use a staged pilot → batch → independent sample audit. Do not send an untested heterogeneous corpus directly to Luna.
- Use Max only for an exceptionally hard single-agent problem.
- Use Ultra only when the work has independent subproblems and a final integrator or reviewer.
- Represent mandatory independent review in the orchestration plan even when the implementation itself is single-agent.
- Require an explicit adversarial review step for high-risk work and publication-facing formal results.
- Escalate uncertainty upward. Never downgrade merely because the prompt is short.
- Do not invent pass probabilities. Mark routes `uncalibrated` until representative benchmark evidence exists.
- Call uncalibrated output a conservative heuristic, never an empirical optimum.
- Compare expected end-to-end latency, including likely repair and rerun time, rather than first-response latency alone.

## Maintain and calibrate

- Read `references/routing-policy.json` when changing thresholds or mappings.
- Read `references/model-capabilities.json` when model availability, effort levels, or speed tiers may have changed. Refresh current official documentation when its `checked_at` date is stale or a command is rejected.
- Read `references/quality-gates.md` when defining the acceptance contract for a new task class.
- Read `references/benchmark-baseline.json` only as smoke-test evidence. Do not infer comparative superiority from one non-comparable run per model.
- Run `python3 scripts/test_router.py` after any policy or code change.
- Run `python3 scripts/evaluate_router.py` to check the representative scenario manifest.
- Preserve benchmark prompts, expected routes, outputs, latency, tokens, gate results, and review decisions in an isolated evaluation directory. Do not overwrite canonical project artifacts.

## Report the decision

Return the chosen model, effort, requested speed, orchestration pattern, quality floor, route confidence, assumptions, and escalation path. Distinguish routing confidence from empirically measured task success.
