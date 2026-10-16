# Summarize workflow receipts

Implement `summarize_receipts(receipts)` in `receipt_stats.py`. It takes any iterable of dictionaries already parsed from our receipt JSONL file. Return a dictionary with exactly these fields:

- `total`: number of receipts.
- `outcomes`: counts for all four outcomes, including zeros: `accepted`, `needs-correction`, `blocked`, `incomplete`.
- `acceptance_rate`: accepted / total, or `None` for no receipts.
- `corrections`: sum of correction counts, defaulting absent counts to zero.
- `known_cost_usd`: sum of costs that are provided and not None, or None when none are known.
- `cost_coverage`: number of receipts with known costs / total, or None for no receipts.

Unknown cost must remain unknown, not become a free run. Inputs must not be modified. An invalid outcome, a negative/noninteger/bool correction count, or a negative/nonfinite/nonnumeric/bool cost raises ValueError. Use no third-party dependencies. Add a small test file and execute it. This is a programming capability check, not a claim that the workflow is already reliable across projects.
