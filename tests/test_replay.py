import unittest

from cyber_agent.replay import run_replay


class ReplayTests(unittest.TestCase):
    def test_all_six_checks_pass_without_real_actions(self):
        rows = run_replay()
        self.assertEqual(len(rows), 6)
        self.assertTrue(all(row["passed"] for row in rows))
        self.assertEqual(len({row["case"] for row in rows}), 6)
        self.assertIn("Instruction in alert text", {row["case"] for row in rows})
        self.assertIn("Model-style suggestion overstates evidence", {row["case"] for row in rows})


if __name__ == "__main__":
    unittest.main()
