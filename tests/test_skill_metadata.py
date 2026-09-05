from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]

class SkillMetadataTests(unittest.TestCase):
    def test_workflow_runs_metadata_with_dependency_and_path_filters(self):
        workflow = yaml.safe_load((ROOT / ".github/workflows/skills-validate.yml").read_text())
        # PyYAML uses YAML 1.1, where the GitHub Actions key `on` is boolean True.
        triggers = workflow[True]
        required_paths = ["tests/test_skill_metadata.py", "skills/FRAMEWORK.md",
                          ".github/workflows/skills-validate.yml"]
        required_paths.append("templates/agent-skill-subsystem/README.md")
        from fnmatch import fnmatchcase
        for event in ("push", "pull_request"):
            for path in required_paths:
                with self.subTest(event=event, path=path):
                    self.assertTrue(any(fnmatchcase(path, pattern)
                                        for pattern in triggers[event]["paths"]))
        commands = [step["run"] for step in workflow["jobs"]["validate-skills"]["steps"]
                    if "run" in step]
        install = "python -m pip install PyYAML"
        regression = "python -m unittest discover -s tests -p 'test_skill_metadata.py' -v"
        self.assertIn(install, commands)
        self.assertIn(regression, commands)
        self.assertLess(commands.index(install), commands.index(regression))

    def test_frontmatter_templates_include_required_description(self):
        import re
        paths = [ROOT / "skills/FRAMEWORK.md"]
        paths.append(ROOT / "templates/agent-skill-subsystem/README.md")
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT)):
                headers = re.findall(r"```yaml\n---\n(.*?)\n---\n```", path.read_text(), re.S)
                self.assertTrue(headers, "Required frontmatter example missing")
                for header in headers:
                    metadata = yaml.safe_load(header)
                    self.assertIsInstance(metadata.get("description"), str)
                    self.assertTrue(metadata["description"].strip())
                    self.assertLessEqual(len(metadata["description"]), 1024)

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
