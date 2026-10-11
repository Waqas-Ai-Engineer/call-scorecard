import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from callscore.scorer import parse, score, score_file
from callscore.cli import main

EX = os.path.join(os.path.dirname(__file__), "..", "examples", "calls")


class T(unittest.TestCase):
    def test_parse_lines_and_json(self):
        self.assertEqual(len(parse("Agent: hi\nCaller: yo")), 2)
        self.assertEqual(parse('[{"role":"ai","text":"x"}]')[0].role, "agent")

    def test_good_call_high(self):
        r = score_file(os.path.join(EX, "hvac_good.txt"))
        self.assertGreaterEqual(r.score, 90)
        self.assertEqual(r.outcome, "booked")
        self.assertTrue(r.urgent)

    def test_poor_call_low_with_coaching(self):
        r = score_file(os.path.join(EX, "roofing_poor.txt"))
        self.assertLess(r.score, 40)
        self.assertTrue(r.coaching)

    def test_risky_promise_flagged(self):
        r = score(parse("Agent: We guarantee the best result.\nCaller: ok"))
        self.assertTrue(any(n == "No risky promises" and p == 0 for n, p, _, _ in r.checks))

    def test_cli_min_score_exit_code(self):
        self.assertEqual(main([EX, "--min-score", "50", "--out", os.devnull]), 1)
        self.assertEqual(main([os.path.join(EX, "hvac_good.txt"), "--min-score", "50", "--out", os.devnull]), 0)

    def test_empty_transcript(self):
        self.assertLessEqual(score(parse("")).score, 25)


if __name__ == "__main__":
    unittest.main()
