# Skill source provenance and verification

Before installation record `git remote get-url origin`, `git rev-parse HEAD`,
skill path/name/version, and resolved host/profile target. Repository names or
identical triggers do not prove two packs are interchangeable. The operator must
choose the source/version; this document makes no new canonical ownership choice.
Preserve existing domain authority distinctions (especially SUAS specification
versus runtime conformance). Do not install both same-named variants into one
profile without a deliberate selection. Avoid globally installing whole project
packs when repository-local discovery is enough.

Before migration compare source contents and dependencies, preserve the old
package/link and mutable state outside discovery, and record old/new commit and
target. Verify the selected new package before retiring the old discovery entry.
Deprecation requires owner approval and an explicit replacement source/commit;
do not silently delete another profile's copy or infer retirement from age.

## Safe local checks

Run from this checkout; Python 3.11+, pytest for pytest commands, and
PyYAML for SUAS metadata tests (`python3 -m pip install pytest PyYAML` in a
disposable venv). No live enrollment, deploy, or publication is needed.

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -p test_skill_metadata.py
```
