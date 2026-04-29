# Job Folder README Format (Spec)

Every job folder must include a `README.md` with a predictable structure.
This is the main mechanism that makes artifacts reproducible, reviewable, and durable.

Exact headings can vary by job type, but every README must answer the same core questions.

## Required sections for all job types

### 1) Title

Use a title that matches the job folder intent and makes the job discoverable.

Examples:

- `# community API query artifact (issue #1)`
- `# api.handle.me timeout remediation tracking`
- `# first page handles capture (issue #27)`

### 2) Original request or context

Include one of:

- the original request text
- a concise summary of the request
- a stable link to the issue, ticket, or alert

A reviewer should not need to guess why the folder exists.

### 3) References

When available, include:

- GitHub issue reference
- owning repo reference for cross-repo work
- linked PR or issue in the owning repo
- executor identifiers:
  - `action_id`
  - `job_id`

Prefer stable identifiers over local-only references.

### 4) Inputs or data sources

Document the source-of-truth inputs.

Examples:

- snapshot file paths
- endpoint URLs and query parameters
- environment or branch references
- evidence identifiers for tracking artifacts

If the job depends on a sibling checkout, be explicit about the relative path and why that dependency exists.

### 5) Setup or prerequisites

List what a reviewer needs to run the job:

- runtime requirements
- dependency installation, if any
- required local files
- environment variables or headers when applicable

If setup would duplicate canonical documentation in another repo, link to that repo instead of rewriting everything here.

### 6) Run steps

Include exact commands when commands were used.

Rules:

- prefer copy-pastable blocks
- avoid hidden state
- call out any destructive or privileged steps clearly
- if the artifact is mainly tracking context, document the exact verification or collection steps that were taken

### 7) Outputs

List the files produced and what they contain.
If an output is large, document size expectations, ordering rules, or notable fields.

### 8) Verification

Provide meaningful checks.
Examples:

- `test -s output.txt`
- `jq . output.json >/dev/null`
- `wc -l output.txt`
- run unit tests for a helper script
- confirm links resolve to the intended repo and issue or PR

The verification section should catch a real failure mode, not just prove the command ran.

## Recommended sections

These are optional but often helpful:

- `assumptions / limitations`
- `safety notes`
- `supersedes` or `superseded by`
- `next steps`

## README expectations by job type

### Query artifact READMEs

Must be precise about:

- source data
- deterministic behavior
- output schema or formatting
- verification invariants

### Tracking artifact READMEs

Must be precise about:

- owning repo
- current status
- what belongs elsewhere

### Investigation or runbook READMEs

Must be precise about:

- environment assumptions
- observations
- conclusion
- next action

## Minimal templates

Full starter templates live in `docs/spec/templates.md`.
Use them as scaffolding, then tailor them to the job rather than leaving irrelevant headings behind.
