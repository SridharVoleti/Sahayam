import unittest
from sahayam.requirements import load_requirements
from sahayam.evidence import summarize

class RequirementRegistryTests(unittest.TestCase):
    def test_all_baseline_ids_unique(self):
        records = load_requirements()
        self.assertEqual(len(records), 271)
        self.assertEqual(len({r["id"] for r in records}), 271)

    def test_known_requirement_present(self):
        ids = {r["id"] for r in load_requirements()}
        self.assertIn("MOB-011", ids)
        self.assertIn("KIT-024", ids)
        self.assertIn("CLN-043", ids)

    def test_no_unverified_requirement_is_marked_passed(self):
        records = load_requirements()
        counts = summarize(records, {})
        self.assertEqual(counts["not_started"], 271)
        self.assertEqual(counts["sim_pass"], 0)
        self.assertEqual(counts["physical_pass"], 0)

if __name__ == "__main__":
    unittest.main()
