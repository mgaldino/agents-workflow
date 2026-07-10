# Quality gates

Define the acceptance contract before execution. Treat hard gates as non-compensatory: a strong average score cannot offset a critical error.

## Universal hard gates

- Allow zero critical errors.
- Complete every material part of the request or mark an explicit blocker.
- Preserve canonical and raw artifacts.
- Do not fabricate evidence, testing, sources, or execution status.
- Verify that the final artifact exists, opens, compiles, or parses as appropriate.
- Report what was and was not tested.

## Gates by task class

### Mechanical transformation and extraction

- Validate schema, row or item counts, required fields, encoding, and deterministic reruns.
- Compare a sample against the source.
- Detect silent truncation, duplicates, and dropped records.

### Classification

- Validate allowed labels and completeness.
- Audit a stratified sample, including ambiguous cases.
- Compare decision-critical fields rather than relying only on aggregate agreement.

### Code and data pipelines

- Run targeted tests and relevant integration tests.
- Run formatting or lint checks when configured.
- Run `git diff --check` in Git repositories.
- Check dates, impossible values, duplicates, keys, denominators, and missingness when applicable.
- Keep computation in reproducible scripts and log inputs and outputs.

### Analysis and causal inference

- Verify the estimand-estimator match, sample definition, treatment timing, controls, uncertainty, and numerical claims.
- Reproduce tables and figures from scripts.
- Distinguish exploratory patterns from causal claims.

### Papers, reports, and reviews

- Preserve argument fidelity.
- Support every material factual or numerical claim.
- Check structure, completeness, citations, tables, figures, captions, and language.
- Require independent review for final or high-risk deliverables.

### Formal models and proofs

- State assumptions, timing, strategies, solution concept, and boundary cases.
- Verify algebra or formal proof artifacts where possible.
- Require adversarial review for publication-facing results.

## Escalation

Repair only the failed component when safe. Increase reasoning effort before upgrading the model. Upgrade Luna to Terra and Terra to Sol when the failure is substantive rather than mechanical. Add independent or adversarial review when a final or high-risk artifact remains judgment-dependent. Use Ultra only when separate workstreams can be integrated and checked.
