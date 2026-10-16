import math
import unittest

from receipt_stats import summarize_receipts


class SummarizeReceiptsTests(unittest.TestCase):
    def test_summarizes_generator_and_preserves_unknown_costs(self):
        receipts = (
            receipt
            for receipt in [
                {"outcome": "accepted", "corrections": 2, "cost_usd": 1.5},
                {"outcome": "blocked", "cost_usd": None},
                {"outcome": "accepted"},
            ]
        )

        self.assertEqual(
            summarize_receipts(receipts),
            {
                "total": 3,
                "outcomes": {
                    "accepted": 2,
                    "needs-correction": 0,
                    "blocked": 1,
                    "incomplete": 0,
                },
                "acceptance_rate": 2 / 3,
                "corrections": 2,
                "known_cost_usd": 1.5,
                "cost_coverage": 1 / 3,
            },
        )

    def test_empty_receipts(self):
        self.assertEqual(
            summarize_receipts([]),
            {
                "total": 0,
                "outcomes": {
                    "accepted": 0,
                    "needs-correction": 0,
                    "blocked": 0,
                    "incomplete": 0,
                },
                "acceptance_rate": None,
                "corrections": 0,
                "known_cost_usd": None,
                "cost_coverage": None,
            },
        )

    def test_rejects_invalid_values(self):
        for receipt in [
            {"outcome": "other"},
            {"outcome": "accepted", "corrections": -1},
            {"outcome": "accepted", "corrections": True},
            {"outcome": "accepted", "cost_usd": -0.1},
            {"outcome": "accepted", "cost_usd": math.inf},
            {"outcome": "accepted", "cost_usd": True},
        ]:
            with self.subTest(receipt=receipt):
                with self.assertRaises(ValueError):
                    summarize_receipts([receipt])


if __name__ == "__main__":
    unittest.main()
