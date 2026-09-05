from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]

class SkillMetadataTests(unittest.TestCase):
    def test_all_six_have_manager_metadata(self):
        paths = sorted((ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(paths), 6)
        for path in paths:
            with self.subTest(skill=path.parent.name):
                text = path.read_text()
                self.assertTrue(text.startswith("---\n"))
                _, header, body = text.split("---", 2)
                meta = yaml.safe_load(header)
                self.assertIsInstance(meta, dict)
                self.assertEqual(meta["name"], path.parent.name)
                self.assertIsInstance(meta.get("description"), str)
                self.assertTrue(meta["description"].strip())
                self.assertLessEqual(len(meta["description"]), 1024)
                self.assertTrue(body.strip())
                for field in ("kind", "authority", "fail_closed", "self_test"):
                    self.assertIn(field, meta)

if __name__ == "__main__":
    unittest.main()
