#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = [
    "evidence-gate",
    "synthetic-data",
    "recovery-test",
    "contract-validation",
    "adversarial-testing",
    "accessibility-audit",
]
REQUIRED_META = {
    "version": "1.0.0",
    "kind": "specification",
    "status": "active",
    "authority": "canonical-spec",
    "fail_closed": "true",
}
SHARED = [
    ROOT / "skills" / "FRAMEWORK.md",
    ROOT / "skills" / "schemas" / "skill-result.schema.json",
    ROOT / "skills" / "templates" / "skill-result.yaml",
    ROOT / "skills" / "README.md",
]

errors = []

def fail(msg: str) -> None:
    errors.append(msg)

def parse_frontmatter(text: str, path: Path) -> dict[str, str]:
    if not text.startswith("---\n"):
        fail(f"{path}: missing YAML frontmatter opener")
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        fail(f"{path}: missing YAML frontmatter closer")
        return {}
    meta = {}
    for raw in text[4:end].splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if ":" not in raw:
            fail(f"{path}: malformed frontmatter line: {raw}")
            continue
        key, value = raw.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta

for path in SHARED:
    if not path.is_file():
        fail(f"missing shared skill artifact: {path.relative_to(ROOT)}")

router = (ROOT / "skills" / "README.md")
router_text = router.read_text(encoding="utf-8") if router.is_file() else ""

for skill in SKILLS:
    path = ROOT / "skills" / skill / "SKILL.md"
    if not path.is_file():
        fail(f"missing skill package: {path.relative_to(ROOT)}")
        continue
    text = path.read_text(encoding="utf-8")
    meta = parse_frontmatter(text, path.relative_to(ROOT))
    if meta.get("name") != skill:
        fail(f"{path.relative_to(ROOT)}: name must be {skill!r}")
    for key, expected in REQUIRED_META.items():
        if meta.get(key) != expected:
            fail(f"{path.relative_to(ROOT)}: {key} must be {expected!r}, got {meta.get(key)!r}")
    for key in ("inputs", "outputs", "self_test"):
        if not meta.get(key):
            fail(f"{path.relative_to(ROOT)}: missing required metadata {key}")
    self_test = meta.get("self_test")
    if self_test:
        fixture = ROOT / self_test
        if not fixture.is_file():
            fail(f"{path.relative_to(ROOT)}: self_test does not exist: {self_test}")
        else:
            fixture_text = fixture.read_text(encoding="utf-8")
            if not re.search(rf"(?m)^skill:\s*{re.escape(skill)}\s*$", fixture_text):
                fail(f"{fixture.relative_to(ROOT)}: fixture skill does not match {skill}")
            if not re.search(r"(?m)^expected(_verdict|_status|_result)?:", fixture_text):
                fail(f"{fixture.relative_to(ROOT)}: fixture must declare an expected result/status/verdict")
    for section in ("## Purpose", "## Trigger", "## Procedure", "## Output schema", "## Completion criteria", "## Invocation example", "## Self-test"):
        if section not in text:
            fail(f"{path.relative_to(ROOT)}: missing required section {section}")
    if skill not in router_text:
        fail(f"skills/README.md: router does not reference {skill}")

if errors:
    print("SUAS skill framework validation: FAIL")
    for err in errors:
        print(f"- {err}")
    sys.exit(1)

print(f"SUAS skill framework validation: PASS ({len(SKILLS)} skills)")
