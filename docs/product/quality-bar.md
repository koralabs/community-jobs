# Community Jobs - Quality Bar (Definition of Done)

This repo is useful only if its artifacts are trustworthy.
"Done" does not mean a file exists.
It means a reviewer can understand what happened, validate the output, and trust that the artifact will still make sense later.

Use this document as the Definition of Done for `community-jobs`.

## Required for all job types

- Context is captured:
  - original request or link
  - relevant issue, ticket, or alert references
  - executor identifiers when available
- Inputs are documented:
  - source repo, file path, endpoint, or environment reference
  - time boundary or snapshot reference when relevant
  - assumptions and known limitations
- Steps are reproducible:
  - commands are copy-pastable
  - prerequisites are explicit
  - steps do not rely on hidden local state
- Verification exists:
  - at least one check would fail if something important were wrong
- Artifact is safe to store:
  - no secrets
  - no private or unsafe data
  - output size is reasonable for Git

## Query artifacts: additional requirements

- Output ordering is deterministic or explicitly described.
- Output format is documented.
- Failure modes are addressed in either tests, verification commands, or README notes.
- For live API captures, request scope and freshness semantics are documented.

## Tracking artifacts: additional requirements

- Owning repo is explicit.
- Linked issue or PR is explicit when available.
- Current status is understandable without external tribal knowledge.
- The artifact does not imply implementation landed in this repo when it did not.

## Investigation notes: additional requirements

- Evidence is linked or summarized with stable identifiers.
- Conclusions are actionable.
- Recommended next steps are concrete.

## Review checklist

When reviewing a PR in this repo, confirm:

- the diff contains no secrets or unsafe raw data
- the README is understandable on its own
- verification steps are relevant and non-trivial
- outputs are reasonable in size and safe to store
- cross-repo ownership is explicit where relevant
- the artifact adds durable value rather than duplicating another system of record
