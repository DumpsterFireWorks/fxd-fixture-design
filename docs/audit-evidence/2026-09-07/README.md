# Audit and repair-setup evidence

## Product baselines

- Main: `801aad49f4c5e5fac4626fe18576717d71d19580`.
- PR #79: `686486b0cfd6e1f062a3074b8d1319a0e84549b4`.
- Original full offline audit: main 480 tests run, 6 skipped, pass; PR 487 run, 1 failure, 6 skipped. The PR failure is an obsolete governance literal assertion, not an OCP failure.
- Fourteen independent diagnostic records reproduced on unchanged heads during September 7 repair setup. See `probe-results.json` and the full audit for limitations.
- `scripts/audit/fxd_reassessment_probe.py` is a portable diagnostic adaptation using an explicit main/held phase and temporary artifact directory. It is not acceptance CI and does not assert that existing defects are acceptable.

## Governance setup validation

- `bash scripts/ci.sh`: PASS, 481 tests run, 6 skipped (475 pass); pinned real-OCP proof, frozen-history validation, workflow cost checks and API-spend firewall pass.
- Focused governance: 19 tests pass, including twelve unauthorized state/scope/spend mutations and a contradictory current-state projection.
- Focused standing-prompt API firewall: 3 tests pass.
- `git diff --check`: pass.
- Product modules, UI implementation, runtime dependency pins, workflow executables and frozen milestone bytes unchanged.
- Environment: Python 3.12, pinned OCP/PySide6/VTK, Linux offscreen Qt with local EGL runtime. No Windows acceptance claimed.
- Development/provider API requests made by this audit/setup: 0. No credentials, live opt-ins or paid dispatch used.

The governance PR and its hosted checks identify the exact pushed setup head. These setup checks do not repair or accept PR #79, prove live model competence, or approve a fixture. Profile E and current-head Windows acceptance remain outstanding.
