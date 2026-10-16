import math


def summarize_receipts(receipts):
    outcomes = {
        "accepted": 0,
        "needs-correction": 0,
        "blocked": 0,
        "incomplete": 0,
    }
    total = 0
    corrections = 0
    known_cost_usd = None
    known_costs = 0

    for receipt in receipts:
        outcome = receipt.get("outcome")
        if outcome not in outcomes:
            raise ValueError("invalid outcome")

        correction_count = receipt.get("corrections", 0)
        if (
            isinstance(correction_count, bool)
            or not isinstance(correction_count, int)
            or correction_count < 0
        ):
            raise ValueError("invalid correction count")

        cost = receipt.get("cost_usd")
        if cost is not None:
            if (
                isinstance(cost, bool)
                or not isinstance(cost, (int, float))
                or not math.isfinite(cost)
                or cost < 0
            ):
                raise ValueError("invalid cost")
            known_cost_usd = (known_cost_usd or 0) + cost
            known_costs += 1

        outcomes[outcome] += 1
        total += 1
        corrections += correction_count

    return {
        "total": total,
        "outcomes": outcomes,
        "acceptance_rate": outcomes["accepted"] / total if total else None,
        "corrections": corrections,
        "known_cost_usd": known_cost_usd,
        "cost_coverage": known_costs / total if total else None,
    }
