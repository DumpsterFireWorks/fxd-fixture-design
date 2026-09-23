# Claude Code Instructions for FXD

GitHub is authoritative.

Before modifying FXD, read current main:
1. `AGENTS.md`
2. `docs/CONTROL_STATE.json`
3. `CURRENT.md`
4. the active issue
5. the active PR/exact head
6. required recovery/product docs and tests

Claude Code may implement an FXD gate **only when current CONTROL_STATE explicitly selects `claude_code` as the active builder**.

If another builder is selected, do not modify the active branch. Report that the current gate belongs to the selected builder.

When selected:
- implement exactly one bounded active gate;
- use one implementation PR;
- preserve source CAD immutability and deterministic validation;
- never use a product-runtime provider key unless the gate separately authorizes a live request;
- do not create paid API development orchestration;
- do not choose new scope, merge, advance, or review/approve your own work;
- stop `AWAITING_REVIEW` with exact SHA and actual evidence.

Claude Code implementation authority does not make Anthropic/Claude an FXD product-runtime provider, independent reviewer, audit fallback, or tie-break route.
