# Checklists (Spec)

These checklists are intended for both authors and reviewers.
They overlap with `docs/product/quality-bar.md`, but this file focuses on concrete mechanical checks.

## Checklist: adding a new query artifact

- [ ] Created a new job folder with a descriptive name
- [ ] Added `README.md` with context and issue references
- [ ] Documented the input snapshot or endpoint details
- [ ] Documented any required headers, env vars, or rate limits for live requests
- [ ] Output is deterministic or the time boundary is explicit
- [ ] Committed outputs as files, not pasted into the README
- [ ] Added meaningful verification commands
- [ ] Added tests if the helper script has parsing or transformation logic
- [ ] Reviewed outputs for secrets or private data

## Checklist: adding a new tracking artifact

- [ ] README includes the owning repo when relevant
- [ ] README links the owning issue or PR when available
- [ ] README makes it clear that implementation belongs in the owning repo
- [ ] Context and status are understandable without external tribal knowledge
- [ ] Verification includes link or reference checks
- [ ] No private or unsafe data appears in the artifact

## Checklist: adding or updating repo docs

- [ ] Added new docs under `docs/product/` or `docs/spec/` only when they express reusable repo guidance
- [ ] Updated `docs/index.md`
- [ ] Confirmed the docs reflect current repo behavior and examples
- [ ] Avoided copying large chunks of sibling-repo documentation unnecessarily

## Checklist: reviewing a PR in this repo

- [ ] Searched the diff for tokens, secrets, or unsafe raw logs
- [ ] Confirmed the README is understandable without external context
- [ ] Confirmed verification steps are meaningful and copy-pastable
- [ ] Confirmed outputs are reasonable in size and safe to store
- [ ] Confirmed the artifact type is appropriate for this repo
- [ ] For cross-repo tracking, confirmed the owning repo is explicit and implementation is not being redirected here
