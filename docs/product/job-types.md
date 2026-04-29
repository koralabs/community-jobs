# Community Jobs - Job Types

This repo holds artifacts from several related but distinct categories of work.
Keeping those categories explicit makes the repository easier to search, easier to review, and less likely to become a dumping ground for unrelated files.

This document defines the canonical job types for `community-jobs`, what belongs in each, and what "done" should mean for each one.

## 1) Community API query artifacts

### What they are

Jobs that answer a question primarily by querying, filtering, transforming, or summarizing data.
They usually produce a concrete output file such as:

- `output.txt`
- `output.json`
- `output.csv`
- `report.md`

Typical prompts include:

- "Give me a list of all handle names as plain text."
- "List the first page of handles and summarize the total count returned."
- "Export all items matching a known rule from a safe snapshot."
- "Count or aggregate public handle data and preserve the result."

### Why they belong here

These outputs are frequently requested by support or community-facing workflows.
They benefit from:

- repeatability
- explicit provenance
- a durable, reviewable location
- separation from production application repos

### Common subtypes

There are two common patterns already represented in this repository:

1. Snapshot-based queries
   - Example: `can-you-give-me-a-issue-1/`
   - The artifact reads a point-in-time file produced elsewhere, transforms it, and writes an output file.
2. Live API query captures
   - Example: `list-the-first-page-of-issue-27/`
   - The artifact makes a bounded request to a public endpoint, captures the response summary, and stores a structured export plus validation logic.

Both are valid, but they need slightly different documentation.
Snapshot-based jobs must document the snapshot path and provenance.
Live API jobs must document request parameters, headers, rate limiting, and time sensitivity.

### Expected contents

Each query artifact folder should include:

- `README.md` describing:
  - the original request
  - the source of truth inputs
  - the exact run steps
  - the output format
  - the verification steps
- one or more output files
- helper scripts when the query is complex enough that a script is clearer than a shell one-liner
- tests when a script contains logic that could regress silently

### Quality bar

A query artifact is complete when:

- the output format is explicit
- the data source or endpoint is explicit
- the commands are reproducible
- a reviewer can run at least one meaningful verification step
- the outputs are safe to commit

For live API jobs, "complete" also means the README explains the time boundary and the request contract well enough that someone understands whether the output is a fresh measurement or a point-in-time capture.

## 2) Tracking artifacts for work owned elsewhere

### What they are

Artifacts that capture safe public context about work that is actually implemented in another repository.

Typical examples:

- a short README linking a community-facing issue to an owning repo issue or PR
- an alert summary that points to the real service repo
- a narrow investigation note that helps someone understand what happened before they switch repos

### Why they belong here

Sometimes it is useful to preserve a public-facing trail in the same place where community jobs are tracked, even when the code change must happen elsewhere.
In those cases, this repo can store the tracking layer without pretending to own the implementation.

### Expected contents

Each tracking artifact folder should include:

- `README.md` describing:
  - the original request, alert, or incident
  - the owning repo
  - the owning issue or PR when available
  - safe evidence identifiers or public notes
  - current status and next step
- optional small supporting files such as a checklist or report

### Quality bar

A tracking artifact is complete when:

- the owning repo is explicit
- the current status is understandable
- a reviewer can see where implementation is happening
- the artifact adds context rather than duplicating the owning repo
- no private or unsafe data leaked into the repo

### Important non-goal

Tracking artifacts are not a reason to move code patches into `community-jobs`.
Historical patch folders exist here, but they are legacy patterns rather than the target state.

## 3) Investigation notes and runbooks

### What they are

Jobs where the primary output is narrative understanding rather than a raw export.
Examples include:

- a reproduction guide
- a root cause analysis summary
- a runbook for future responders
- a decision log that explains why a query or workflow exists

These artifacts may include a small helper script, but the written explanation is the main product.

### Why they belong here

Not every useful artifact is code or a data dump.
Some of the highest-leverage outputs are the concise notes that let the next responder skip hours of rediscovery.

### Expected contents

- `README.md` or `report.md` with:
  - context
  - environment assumptions
  - reproduction steps
  - observations
  - conclusion
  - next steps when relevant

### Quality bar

Investigation artifacts should be actionable:

- commands should be concrete
- evidence references should be stable
- conclusions should be testable or at least falsifiable
- next steps should say what to do next, not just "investigate further"

## 4) Documentation and repo-governance artifacts

### What they are

Files under `docs/product/` and `docs/spec/` that define the expected shape of the repo itself.

### Why they belong here

This repository is executor-heavy and intentionally lightweight.
That combination makes written conventions unusually important.
Without them, each new artifact risks inventing a slightly different format, naming scheme, or quality bar.

### Expected contents

- product docs describing purpose, workflow, safety, and quality expectations
- spec docs describing folder shape, README format, templates, and checklists

### Quality bar

Repo docs are complete when they are:

- aligned with current repository behavior
- specific enough to guide future additions
- updated when new artifact patterns appear

## Naming conventions

Preferred folder naming patterns:

1. Issue-driven community requests: `<request-slug>-issue-<number>/`
2. Executor or tracking artifacts: `<slug>-<short-job-id>/`

Examples in this repo:

- `can-you-give-me-a-issue-1/`
- `list-the-first-page-of-issue-27/`
- `api-timeout-remediation-149a610d/`

Clarity matters more than brevity.
If a long folder name prevents ambiguity, keep the long name.

## Choosing the right job type

Use these rules of thumb:

- If the main value is a committed output file produced from known data, it is a query artifact.
- If the main value is a durable public pointer to work happening elsewhere, it is a tracking artifact.
- If the main value is written understanding or a repeatable procedure, it is an investigation artifact.
- If the main value is repo-wide guidance, it belongs under `docs/`.

When a job spans categories, choose the dominant one and make the README explicit about the secondary role.
For example, a live query artifact can include a brief narrative summary, but it is still primarily a query artifact if the durable output is the captured JSON.
