# MAC_DEVICE_WORK.md: Mac device and local-runner handoff (Grok Build)

**Written:** 2026-10-07 PT by Grok Bot, at Danny's direction (5:15 PM PT).  
**For:** Grok Build, a coding agent on Danny's Mac with Xcode and Android Studio.  
**Board:** [SUAS Product Board](https://github.com/users/scrimshawlife-ctrl/projects/6), card "Mac device work (Grok Build): see docs/handoffs/MAC_DEVICE_WORK.md".  
**Read first:** [CONTEXT.md](../../CONTEXT.md) and [AGENTS.md](../../AGENTS.md) in this repo, then each app repo's `CONTEXT.md` and `AGENTS.md`.

Every command and path below was checked against the four repositories on 2026-10-07. If a repo has moved on, trust the repo and say what changed in your report.

## 1. Goal and scope

Finish the work that needs a Mac and that Grok Bot's Linux box cannot do:

- Run the iOS `Demo` and `Local` schemes in the Simulator and check the look and the DEBUG-only demo behavior.
- Archive a Release iOS build and run `scripts/check_release_bundle.py` on it.
- Create an Android emulator, run the debug launchers and the instrumented tests, and take screenshots.
- Re-run each repo's CI jobs locally for every merge made while GitHub Actions could not start.
- Report pass or fail per item and tick the board cards (section 8).

Out of scope. Do not do these, and stop and ask Danny if a task seems to need one:

- Blocked decisions: D-034 (on-device protection of retained Veteran data), D-006, SPEC-018 store launch (`KEEP_BLOCKED`), production VA, and live operations.
- Deploys of any kind. Do not run `worker-deploy`, `pages`, or any `staging-*` workflow. Do not touch `https://suasqrf.com` or any production host.
- Real email or SMS. The LOCAL Worker uses fake email and SMS.
- Merges. Every merge needs Danny's yes. Open fix PRs as drafts only.
- Real Veteran data. All data is synthetic: `@example.invalid` emails and 555-0100 to 555-0199 phone numbers.
- Em dashes in anything you write (docs, PR titles and bodies, commits, changelog lines).
- Editing `HANDOFF.md`, changing repo settings or rulesets, or enabling issues on `suas-ios` or `suas-android`.

## 2. Repositories

Clone all four side by side:

```bash
mkdir -p ~/suas-work && cd ~/suas-work
git clone https://github.com/scrimshawlife-ctrl/suas.git
git clone https://github.com/scrimshawlife-ctrl/suas-ios.git
git clone https://github.com/scrimshawlife-ctrl/suas-android.git
git clone https://github.com/scrimshawlife-ctrl/suas-specs.git
```

| Repo | Role | `main` when this was written | Tags |
|---|---|---|---|
| `suas` | Cloudflare Worker, `/api/v0`, web `/app` | `7783284f896935f9ae5274171fec3798a442a230` (#194) | `v0.1.0`, `v0.2.0` |
| `suas-ios` | Native iOS client (SwiftUI) | `bb5e75e0f7ffbcd6a1d5f5c94c4b5ba5ab75a9f5` (#14) | `v0.1.0` |
| `suas-android` | Native Android client (Kotlin, Compose) | `9fae29948af69e572d53c0dc1a021973e2284f4c` (#17) | `v0.1.0` |
| `suas-specs` | Canonical specification | the merge commit of the PR that added this file (after `cf0b883`, #47) | `v0.1.0` to `v0.1.6`, `v0.2.0` to `v0.6.0` |

Run `git log -1 --format='%H %s'` in each clone and record the SHAs you actually tested.

## 3. Prerequisites (from the repos)

| Tool | What the repos say |
|---|---|
| Xcode | Project `objectVersion = 77` and `LastUpgradeCheck = 2650` in `suas-ios/suas/suas.xcodeproj/project.pbxproj`, so use Xcode 26.5 or later. CI uses the default Xcode on `macos-latest`. |
| iOS Simulator runtime | `IPHONEOS_DEPLOYMENT_TARGET = 17.0`; any iPhone Simulator runtime iOS 17.0 or later. `SWIFT_VERSION = 5.0`. |
| JDK | Android CI sets up Temurin 17 (`.github/workflows/ci.yml`). The Gradle daemon toolchain is JDK 25 (`gradle/gradle-daemon-jvm.properties`, `toolchainVersion=25`); if Gradle cannot find it, pass `-Porg.gradle.java.installations.paths=$JAVA_HOME` (README "Checks"). Sources compile for Java 11. |
| Android SDK | AGP 9.3.2, Gradle 9.5.0, `compileSdk` 37, `targetSdk` 37, `minSdk` 24. Set `ANDROID_HOME`. |
| Emulator image | Not pinned by the repo. Use a Google APIs `arm64-v8a` system image with API level between 24 and 37. |
| Node | Node 22 (`engines.node` is `>=22.0.0`; every workflow uses `node-version: '22'`). |
| PostgreSQL | PostgreSQL 17 on localhost with a `suas` / `suas` role that can create databases. If Postgres is not reachable and Docker is running, `npm run dev:demo` starts the `suas-postgres17-local` container. |
| wrangler | `4.148.0`. `npm run dev:demo` runs `wrangler@4.148.0` through `npx`, and `worker-deploy` and `recovery-runtime-acceptance` pin the same version. No global install is needed. |
| Python | `python3` for the repo scripts; `PyYAML` for the skill validators. |
| `act` (optional) | To run the Linux CI jobs in containers (section 7). |

## 4. Start the LOCAL Worker

```bash
cd ~/suas-work/suas
npm ci
npm run dev:demo            # wrangler dev on http://127.0.0.1:3000, SUAS_ENV=LOCAL, migrations and seed
# second terminal:
npm run smoke:demo          # end-to-end smoke over /api/v0 (LOCAL only)
```

- `npm run dev:demo -- --reset` drops and recreates the `suas_demo` database first.
- Base URL `http://127.0.0.1:3000`. The iOS Simulator uses `http://localhost:3000`. The Android emulator uses `http://10.0.2.2:3000`.
- Demo sign-in: `demo@example.invalid`, code `123456`. `newvet@example.invalid` is enrolled with no case; its code comes from `curl "http://127.0.0.1:3000/api/v0/dev/last-challenge?destination=newvet@example.invalid"`.
- The fixed code `123456` for `demo@example.invalid` needs `SUAS_DEMO_FIXED_CODE=enabled`. LOCAL also needs `SUAS_ENV=LOCAL` and a local database (`npm run dev:demo` sets the flag). The synthetic STAGING Worker at `https://suasqrf.com` may use the same account when its deploy sets the flag. TEST and PRODUCTION reject the flag. A Node process pointed at the staging database cannot mint the code. `/api/v0/dev/*` exists only on LOCAL and returns 404 on staging.
- Pass: `smoke:demo` exits 0.

## 5. iOS tasks (`suas-ios`)

Evidence folder: `~/SUAS-device-evidence/2026-10-DD/ios/` (use the day you run it). Take Simulator screenshots with `xcrun simctl io booted screenshot <file>.png`.

### 5.1 Demo and Local schemes in the Simulator

Steps:

1. Open `suas/suas.xcodeproj` in Xcode. Shared schemes are `suas`, `Demo` (`-SUASDemoMode`) and `Local` (`-SUASLocal`); all three run the Debug configuration and set `suas/DemoLocation.gpx` as the default location.
2. Select the `Demo` scheme, pick an iPhone Simulator, and Run (Cmd-R). No server is needed.
3. Keep `npm run dev:demo` running (section 4), select the `Local` scheme, and Run. It talks to `http://localhost:3000`.
4. Select the `suas` scheme and Run once to see the shipped STAGING mode sign-in screen. Do not sign in to staging with real data.

Acceptance (screenshot each):

- Home: navigation title "What do you need?", grouped light background (`Color(.systemGroupedBackground)`), service blue accent `#1C529E` (`SUAS.accent = Color(red: 0.11, green: 0.32, blue: 0.62)`).
- Four need cards in this order: Transportation, Food, Temporary Shelter, Peer Support (`ServiceCategory.allCases`). Four is correct (Danny, 2026-10-07).
- Demo scheme: the home header shows "Demo mode: synthetic data, no server." The first tap on each card opens its seeded synthetic request (`demo-fixtures.json`: Transportation MATCHING, Food FULFILLED, Temporary Shelter CANCELLED, Peer Support CREATED).
- Sign-in prefill `demo@example.invalid` and the "One-tap demo sign-in" button appear only in the `Demo` and `Local` schemes. The `suas` scheme shows an empty email and no one-tap button.
- `Local` scheme: typed sign-in with `demo@example.invalid` and `123456` works against the LOCAL Worker.
- Location in Debug, when the app is started with Xcode Run: "Use my current location" resolves to the `DemoLocation.gpx` point (37.3349, -122.0090). `xcodebuild test` does not apply that scheme location. For an `xcodebuild` check, set it with `xcrun simctl location booted 37.3349,-122.0090`.

### 5.2 Release archive and bundle check

```bash
cd ~/suas-work/suas-ios
xcodebuild archive \
  -project suas/suas.xcodeproj \
  -scheme suas \
  -configuration Release \
  -destination "generic/platform=iOS" \
  -archivePath /tmp/suas.xcarchive \
  CODE_SIGNING_ALLOWED=NO
python3 scripts/check_release_bundle.py /tmp/suas.xcarchive
```

Pass: `** ARCHIVE SUCCEEDED **`, then `release bundle checks: OK (...)` with no `FAIL:` lines. There must be no `demo-fixtures.json`, no `.gpx` file (Release excludes `DemoLocation.gpx` since suas-ios #13), and no `DemoService` or `demo-fixtures` bytes in the bundle. Save the output to the evidence folder.

### 5.3 Unit tests

```bash
cd ~/suas-work/suas-ios
xcrun simctl list devices available        # pick an iPhone; copy its UDID
xcodebuild test \
  -project suas/suas.xcodeproj \
  -scheme suas \
  -destination "platform=iOS Simulator,id=<UDID>" \
  -skip-testing:suasUITests \
  CODE_SIGNING_ALLOWED=NO
```

Pass: `** TEST SUCCEEDED **`, and the log lists the Swift Testing tests (26 on 2026-10-08). `-only-testing:suasTests` matches no Swift Testing tests and can report success after zero tests. Do not use it. Save the summary and the Simulator screenshots from 5.1 to the evidence folder.

## 6. Android tasks (`suas-android`)

Evidence folder: `~/SUAS-device-evidence/2026-10-DD/android/`. Take screenshots with `adb exec-out screencap -p > <file>.png`.

### 6.1 Create and start an emulator

```bash
export ANDROID_HOME=~/Library/Android/sdk          # or your SDK path
sdkmanager --list | grep "system-images;android-"  # pick google_apis;arm64-v8a, API 24 to 37
sdkmanager "<chosen system-images package>"
avdmanager create avd -n suas-test -k "<chosen system-images package>"
emulator -avd suas-test
```

Android Studio's Device Manager works too. Record the image you used.

### 6.2 Launchers and screens

```bash
cd ~/suas-work/suas-android
./gradlew :app:installDebug
adb shell am start -n com.example.suas/.DemoRootActivity     # "SUAS Demo (no server)"
adb shell am start -n com.example.suas/.LocalRootActivity    # "SUAS Local Worker", needs npm run dev:demo
adb shell am start -n com.example.suas/.RootActivity         # product launcher, STAGING
```

Acceptance (screenshot each):

- The launcher shows three icons in a debug build: "Veteran's Passport" (`RootActivity`, since suas-android #17), "SUAS Demo (no server)" and "SUAS Local Worker".
- Home: light off-white background, a "Sign in" button, the "S.U.A.S." heading, four service cards (Transportation, Food, Temporary Shelter, Peer Support), then the "Need help right now?" notice with "Call 911" and "Call or text 988" that dial only when tapped. README calls this the SOS-first home cards; compare with the v0.1.0 look and report any difference.
- Demo launcher: banner "Demo mode: synthetic data, no server. ...", the email is prefilled and the sign-in hint shows the demo email and code; after sign-in each card opens its seeded request, and the "Demo only: advance status" button moves it forward.
- Local launcher: banner "LOCAL Worker at http://10.0.2.2:3000. Synthetic demo data."; sign in with `demo@example.invalid` (prefilled) and `123456`.

### 6.3 Instrumented tests

```bash
./gradlew :app:connectedDebugAndroidTest
```

Pass: all tests in `app/src/androidTest` pass, including `ExampleInstrumentedTest.harnessBannerIsShown` (suas-android #16), which checks the "TEST HARNESS ONLY: not the product launcher. ..." banner on the debug `MainActivity`.

### 6.4 Release build manifest check

```bash
./gradlew :app:assembleRelease
"$ANDROID_HOME"/build-tools/<version>/aapt2 dump badging app/build/outputs/apk/release/app-release.apk | grep -E "launchable-activity|^application:"
```

Pass: one `launchable-activity`, `com.example.suas.RootActivity` with `label='Veteran's Passport'`; no `MainActivity`, `DemoRootActivity` or `LocalRootActivity`. `application: label='Suas'` is expected (`app_name` is the application label, not the launcher label).

## 7. Local-runner verification of merges made while CI was blocked

On the afternoon of 2026-10-07 PT, GitHub Actions jobs stopped starting ("The job was not started because recent account payments have failed or your spending limit needs to be increased."). These merges were checked only locally on Grok Bot's box:

| Repo | PR | Merge SHA |
|---|---|---|
| suas-ios | [#13](https://github.com/scrimshawlife-ctrl/suas-ios/pull/13) release-bundle check, gpx excluded | `6b6ad4ed81a47ee415144912cd5954d9dff86c4c` |
| suas-android | [#16](https://github.com/scrimshawlife-ctrl/suas-android/pull/16) MainActivity harness test | `d26a6a6f50a159868be286795e44d7a66448bc57` |
| suas | [#193](https://github.com/scrimshawlife-ctrl/suas/pull/193) SPEC017_NEXT alignment | `06c2b7588af22560f4696cece78d9714ff315039` |
| suas-specs | [#46](https://github.com/scrimshawlife-ctrl/suas-specs/pull/46) living-docs alignment | `ee9a9b0432e1b9d37eeecfb6dfed9a252102dbfe` |
| suas-android | [#17](https://github.com/scrimshawlife-ctrl/suas-android/pull/17) launcher label Veteran's Passport | `9fae29948af69e572d53c0dc1a021973e2284f4c` |
| suas-specs | [#47](https://github.com/scrimshawlife-ctrl/suas-specs/pull/47) draft RELEASE_DECISIONS-0.7.0.md | `cf0b883ed52344ca42958f9bebf7c84e570e3394` |
| suas-ios | [#14](https://github.com/scrimshawlife-ctrl/suas-ios/pull/14) CONTEXT.md handoff link | `bb5e75e0f7ffbcd6a1d5f5c94c4b5ba5ab75a9f5` |
| suas | [#194](https://github.com/scrimshawlife-ctrl/suas/pull/194) CONTEXT.md handoff link | `7783284f896935f9ae5274171fec3798a442a230` |
| suas-specs | the PR that added this file | its merge commit on `main` |

Each repo's `main` contains all of its rows, so one run per repo at the current `main` covers them. Also check out each listed SHA (`git checkout <sha>`) if a run at `main` fails, to find the first bad merge.

The commands below are the `run:` steps of each repo's PR and `main` workflows. Workflows that deploy or touch staging (`suas` `pages`, `worker-deploy`, `staging-*`, `synthetic-staging-soak`, `recovery-runtime-acceptance`, `cloudflare-token-preflight`, and the tag-only `release` workflows) are not part of this check.

### suas: `verify.yml` (job `verify`, ubuntu-24.04, Postgres 17 service)

```bash
cd ~/suas-work/suas
# Postgres 17 on localhost:5432 with user/password suas/suas and database suas_test
export SUAS_ENV=TEST SUAS_SPEC_VERSION=0.6.0 SUAS_RELEASE_MANIFEST=RELEASE_MANIFEST-0.6.0.md \
  SUAS_ALLOW_REAL_EXTERNAL_EFFECTS=false SUAS_MIGRATIONS_MODE=apply SUAS_BROWSER_AUTH_MODE=disabled \
  SUAS_EMAIL_MODE=fake SUAS_SMS_MODE=fake SUAS_TRANSPORTATION_ADAPTER_MODE=fake \
  SUAS_SHELTER_ADAPTER_MODE=fake SUAS_FOOD_ADAPTER_MODE=fake SUAS_PEER_SUPPORT_ADAPTER_MODE=manual \
  SUAS_SUPPORT_SIGNAL_MODE=fixture SUAS_SAFETY_COPY_MODE=placeholder_test_only \
  SUAS_SENSITIVE_AGGREGATE_REPORTING=disabled \
  DATABASE_URL=postgresql://suas:suas@localhost:5432/suas_test \
  TEST_DATABASE_URL=postgresql://suas:suas@localhost:5432/suas_test \
  TEST_MIGRATIONS_DATABASE_URL=postgresql://suas:suas@localhost:5432/suas_migrations_test
PGPASSWORD=suas psql -h localhost -U suas -d suas_test -c 'CREATE DATABASE suas_migrations_test'
npm ci
export SUAS_SESSION_SECRET=$(openssl rand -hex 32)
cp .env.example .env
export SUAS_BUILD_COMMIT=$(git rev-parse HEAD) SUAS_BUILD_TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
npm run format:check && npm run lint && npm run typecheck && npm run staging:contract \
  && npm run build && npm test && npm run openapi:check && npm run migrate -- apply && npm run provenance
```

Note: `.env` is gitignored; remove the copied `.env` afterwards if you need a clean tree for `dev:demo`.

### suas: `skills-validate.yml`

```bash
python3 -m pip install PyYAML
python3 -m unittest discover -s tests -p 'test_skill_metadata.py' -v
python3 scripts/validate-skills.py
```

### suas-ios: `ci.yml` (jobs `contract`, `unit`, `release-bundle`)

```bash
cd ~/suas-work/suas-ios
# contract (ubuntu-24.04 in CI; runs fine on macOS)
bash scripts/forbidden-capabilities.sh
python3 scripts/check_xcode_project.py
python3 scripts/test_check_release_bundle.py
curl -fsSL -o /tmp/v0.json https://raw.githubusercontent.com/scrimshawlife-ctrl/suas/main/docs/openapi/v0.json
python3 scripts/openapi-client-pin.py /tmp/v0.json
# unit (macos-latest): the xcodebuild test command in section 5.3
# release-bundle (macos-latest): the archive and check commands in section 5.2
```

### suas-android: `ci.yml` (job `contract`, ubuntu-24.04, Temurin 17)

```bash
cd ~/suas-work/suas-android
bash scripts/forbidden-capabilities.sh
curl -fsSL -o /tmp/v0.json https://raw.githubusercontent.com/scrimshawlife-ctrl/suas/main/docs/openapi/v0.json
python3 scripts/openapi-client-pin.py /tmp/v0.json
chmod +x ./gradlew
./gradlew :app:testDebugUnitTest :app:lintDebug :app:assembleDebug :app:assembleRelease --stacktrace
```

### suas-specs: `skills-validate.yml`

```bash
cd ~/suas-work/suas-specs
python3 -m pip install PyYAML
python3 -m unittest discover -s tests -p 'test_skill_metadata.py' -v
python3 scripts/validate_skills.py
```

This workflow only triggers on skill paths, so docs-only merges never ran it; run it anyway.

### Using `act` for the Linux jobs

`act` can run the Linux jobs from the workflow files in Docker, for example `act pull_request -W .github/workflows/verify.yml -j verify` in `suas` (it starts the Postgres service container) or `act pull_request -W .github/workflows/ci.yml -j contract` in `suas-android`. List jobs with `act -l`. If `act` asks which image to use for `ubuntu-24.04`, map it with `-P ubuntu-24.04=<image>`. The macOS jobs (`suas-ios` `unit` and `release-bundle`) cannot run in `act`; run them natively as in sections 5.2 and 5.3.

## 8. Where results go

- Board ([project 6](https://github.com/users/scrimshawlife-ctrl/projects/6)): move each card to Done when it passes, or leave it and comment on the linked PR when it fails:
  - "iOS Simulator visual check of Demo and Local schemes"
  - "Android emulator screenshots of demo mode"
  - "Confirm release-bundle CI on suas-ios main after billing fix"
  - "Verify batch merges with local runners (billing blocked CI)"
  - "Mac device work (Grok Build): see docs/handoffs/MAC_DEVICE_WORK.md"
- Screenshots and logs: attach them to one issue on `suas-specs` (for example "Mac device evidence 2026-10-DD") or to a draft PR there. The 2026-10-08 report is [MAC_DEVICE_RESULTS-2026-10-08.md](MAC_DEVICE_RESULTS-2026-10-08.md). Issues are disabled on `suas-ios` and `suas-android` and must stay disabled.
- Report pass or fail per item in sections 4 to 7, with the SHAs tested, the Xcode, Simulator runtime, emulator image, JDK and Node versions used, and where the evidence is.
- Fixes: open draft PRs only, one per problem, with a CHANGELOG `[Unreleased]` line. Do not merge.

## 9. Known gotchas

- No KVM on Grok Bot's box, so no Android emulator there. That is why this work moved to the Mac.
- `check_release_bundle.py` scans bytes. Swift keeps strings of 15 bytes or fewer inline in code, so `-SUASDemoMode` and `-SUASLocal` are best-effort markers; `DemoService` and `demo-fixtures` are the reliable ones.
- `suasTests` uses Swift Testing (`import Testing`, `@Test`). `-only-testing:suasTests` selects no XCTest cases, runs nothing, and can still print `** TEST SUCCEEDED **`. Section 5.3 uses `-skip-testing:suasUITests`.
- Run the release checker on an archive. A plain unstripped `xcodebuild build` keeps object names such as `DemoService.o` in the symbol table and gives a false `DemoService` failure.
- GitHub Actions is blocked by billing until Danny fixes it under "Billing & plans". Jobs show "The job was not started ...". Do not re-run them in a loop.
- Branch protection blocks the normal merge on several repos. When Danny approves a merge, the fallback is `gh api -X PUT repos/scrimshawlife-ctrl/<repo>/pulls/<n>/merge -f merge_method=squash -f sha=<head sha>`. Never change protection or rulesets.
- The demo fixed code `123456` is opt-in. LOCAL needs `SUAS_ENV=LOCAL`, `SUAS_DEMO_FIXED_CODE=enabled`, and a local database. The synthetic STAGING Worker may set the flag. TEST and PRODUCTION reject it. Do not mint the code from a Node process pointed at the staging database.
