# Mac device results, 2026-10-08 PT

**Documentation only. Not a version bump. No manifest, no tag. Moves no readiness gate and closes no D-id. SPEC-018 stays `KEEP_BLOCKED`. Nothing recorded here was merged by this check.**

Source of the tasks: [MAC_DEVICE_WORK.md](MAC_DEVICE_WORK.md). Logs and screenshots stay on the Mac at `~/SUAS-device-evidence/2026-10-08/`. This note is the report named in section 8 of that handoff.

## SHAs on `main` for the device checks

| Repo | SHA |
|---|---|
| suas | `7783284f896935f9ae5274171fec3798a442a230` (#194) |
| suas-ios | `bb5e75e0f7ffbcd6a1d5f5c94c4b5ba5ab75a9f5` (#14) |
| suas-android | `9fae29948af69e572d53c0dc1a021973e2284f4c` (#17) |
| suas-specs | `9ed2c9a2aefa0d29b37b587d55cd59b9036cf01f` (#48) |

Toolchain: Xcode 26.5 (17F42), iOS Simulator 26.5 (23F77), iPhone 17 `018AF642-2C1A-4922-850B-085705399934`, Node v22.23.1, Temurin 25.0.4.1 at `~/jdks/jdk-25.0.4.1+1`, Android SDK `~/Library/Android/sdk` (platform `android-37.0`, build-tools `37.0.0`). AVD `suas-test`: Pixel 6, `system-images;android-36;google_apis;arm64-v8a`.

## Pass

- Section 4. `npm run dev:demo` reached `http://127.0.0.1:3000/api/v0/health`. `npm run smoke:demo`: 21 passed, 0 failed.
- Section 5.1. Demo, Local, and shipped `suas` schemes. Demo and Local prefill `demo@example.invalid`. The shipped scheme has an empty email and no one-tap button. No staging sign-in. "Use my current location" resolved to `37.3349, -122.0090` after `xcrun simctl location`, because `xcodebuild test` does not apply the scheme GPX.
- Section 5.2. `** ARCHIVE SUCCEEDED **`, then `release bundle checks: OK (5 checks, 9 files scanned)`.
- Section 5.3. Swift Testing: 26 tests in 6 suites passed with `-skip-testing:suasUITests`. An earlier `-only-testing:suasTests` run executed 0 tests and is not the result. The handoff command is corrected in this change.
- Section 6. Android contract, 47 unit tests, lint, debug and release assemble, one release launchable activity `com.example.suas.RootActivity` labeled Veteran's Passport (application label Suas). Debug drawer shows the product launcher plus "SUAS Demo (no server)" and "SUAS Local Worker". Demo sign-in and the advance control, and Local sign-in against `http://10.0.2.2:3000`, were screenshotted. `connectedDebugAndroidTest`: 6 tests, 0 failures, including `harnessBannerIsShown`.
- Section 7. Local re-run of the blocked-CI batch passed for `suas` verify steps (1204 tests), both skill validators (6 skills each), iOS contract scripts, and the Android Gradle contract job. The Android Gradle job is what closed the batch-merge gap.

## Still open

- Private `suas-ios` hosted jobs still fail before any step (account billing). Do not re-run them in a loop. The board card "Confirm release-bundle CI on suas-ios main after billing fix" stays Ready. A green self-hosted run, including the one on `main` below, is not that card. Hosted billing is still blocked.
- The parent card "Mac device work (Grok Build)" stays Ready for the same reason.
- [suas-ios #16](https://github.com/scrimshawlife-ctrl/suas-ios/pull/16) was squash-merged to `main` as `f8ead04`. It labels auto-advance "Auto-advance (demo)" or "Auto-advance (LOCAL demo)", hides the toggle on the shipped scheme, and points `contract`, `unit`, and `release-bundle` at `mac-suas`. Pull-request run [37727319059](https://github.com/scrimshawlife-ctrl/suas-ios/actions/runs/37727319059) passed. The `main` push run [37728469476](https://github.com/scrimshawlife-ctrl/suas-ios/actions/runs/37728469476) passed: 26 Swift tests, forbidden-capability scan passed, `** ARCHIVE SUCCEEDED **`, `release bundle checks: OK (5 checks, 9 files scanned)`. The earlier hosted run [37717488925](https://github.com/scrimshawlife-ctrl/suas-ios/actions/runs/37717488925) failed with zero steps. That was the billing block.
- Draft [suas-ios #15](https://github.com/scrimshawlife-ctrl/suas-ios/pull/15) (`e96cf1f`, run [37715808214](https://github.com/scrimshawlife-ctrl/suas-ios/actions/runs/37715808214)) repeats the runner change that #16 already put on `main`. It does not contain the auto-advance fix. Merging it conflicts with `main`. Left open.
- [suas-ios #17](https://github.com/scrimshawlife-ctrl/suas-ios/pull/17) was squash-merged to `main` as `d8af3e6`. It adds simulator XCUITests for Demo and LOCAL, signed in as `demo@example.invalid` / `123456`. Pull-request CI run [37737280366](https://github.com/scrimshawlife-ctrl/suas-ios/actions/runs/37737280366) passed. Simulator run [37737285289](https://github.com/scrimshawlife-ctrl/suas-ios/actions/runs/37737285289) passed on `mac-suas`: `LocalModeUITests` 2 tests and `DemoModeUITests` 3 tests, each `** TEST SUCCEEDED **`. The main push run [37739776479](https://github.com/scrimshawlife-ctrl/suas-ios/actions/runs/37739776479) passed. It does not upload xcresult bundles, because Actions artifact storage for this account is over quota.
- [suas-android #18](https://github.com/scrimshawlife-ctrl/suas-android/pull/18) was squash-merged to `main` as `18ac773`. Pull-request run [37718820020](https://github.com/scrimshawlife-ctrl/suas-android/actions/runs/37718820020) passed: `contract`, and `demo launchers (emulator)` finished 8 tests. The main push run [37739784265](https://github.com/scrimshawlife-ctrl/suas-android/actions/runs/37739784265) passed the contract job. It replaced the compile failure on suas-android #14. #14 was closed on 2026-10-08 without merge.
- suas-ios #11 was closed on 2026-10-08 without merge. It described `veteran@example.invalid` / `246810`. Current demo sign-in is `demo@example.invalid` / `123456`.
- Later commits are not part of the device check in the table above. `suas` `main` is `b819d28`. Synthetic STAGING at `https://suasqrf.com` runs `80c27e7` (worker-deploy run `37746194370`).

## Not claimed

Production readiness and pilot readiness stay `NOT_READY`. No deploy, no store binary, no production host, no real Veteran data, and no HIPAA conclusion.
