# Community API Query Artifacts (Spec)

This document defines how to produce and store community API query artifacts in `community-jobs`.

These jobs answer "export", "list", "count", or "summarize" requests using either:

- a known snapshot, often produced by a sibling repo such as `api.handle.me`, or
- a tightly bounded live request to a public API endpoint

Both modes are supported here, but they need different guardrails.

## Design goals

- Deterministic outputs whenever possible
- Lightweight tooling
- Strong provenance
- Safe committed artifacts
- Reviewable output formats

## Query mode A: snapshot-based jobs

Snapshot-based jobs should be the default when:

- the question can be answered from a known local dataset
- the source repo already produces a suitable snapshot
- repeated live requests would be noisy or unnecessary

Example already in this repo:

- `can-you-give-me-a-issue-1/`

That pattern reads a point-in-time JSON file from a sibling repo, transforms it, and commits only the derived output.

### Snapshot rules

- The README must identify the snapshot path.
- The README must identify the owning repo.
- The README must describe how the snapshot was produced or where that process is documented.
- Do not commit the full snapshot into this repo unless the snapshot itself is the intended artifact and is safe to store.

## Query mode B: live API capture jobs

Live captures are appropriate when:

- the request is explicitly about current or first-page API behavior
- there is no suitable snapshot
- the response shape itself is part of the artifact

Example already in this repo:

- `list-the-first-page-of-issue-27/`

That folder uses a committed Python script and tests to capture `GET /handles` output, preserve summary metadata, and validate the parsing logic.

### Live query rules

When a job hits a `*.handle.me` endpoint directly:

- document the endpoint and query parameters
- document the relevant request headers
- respect bounded timeouts
- respect rate limiting
- capture enough metadata that freshness or catch-up status is understandable

The broader Kora ecosystem guidance requires a `User-Agent` loaded from `KORA_USER_AGENT` for `*.handle.me` requests.
Contributors should follow that requirement for new or updated networked scripts, even when older examples in repo history predate the convention.

### Rate limiting guidance

If the script can make repeated requests, include a limiter.
The current first-page example uses a per-host limiter capped at five requests per second.

Even if a specific job only makes one request today, it is still useful to document the intended pace if the script might be extended later.

### Freshness semantics

Some public endpoints may return more than simple success or failure.
For example, the current first-page helper interprets:

- `200` as successful and up to date
- `202` as successful but the scanner is still catching up

If an endpoint has those semantics:

- preserve them in the output
- explain them in the README
- avoid flattening them into a single "success" boolean with no nuance

## Output format rules

Choose the simplest format that fits the request.

### `output.txt`

Use for plain lists.
Document:

- encoding
- newline rules
- sort order
- whether duplicates are allowed

### `output.json`

Use for structured captures.
Document:

- top-level shape
- important summary fields
- whether ordering matters
- whether the JSON is pretty-printed

The current first-page example uses JSON with:

- `captured_at_utc`
- `request`
- `summary`
- `handle_names`

That is a good pattern because it preserves both the answer and the minimal provenance needed to understand it later.

### `output.csv`

Use when spreadsheet consumers are the primary audience.
Document:

- delimiter
- header row
- quoting behavior

### `report.md`

Use when a narrative explanation matters more than a raw export.
Prefer concise summaries plus committed machine-readable files when both are helpful.

## Determinism rules

To keep outputs stable:

- sort lists explicitly
- avoid unnecessary timestamps inside plain export files
- make filters explicit
- document any non-deterministic external dependency

If the artifact necessarily depends on live data, make the time boundary explicit rather than pretending the output is timeless.

## Tooling guidance

Prefer:

- standard-library Python or Node.js
- a small committed script when the query logic is non-trivial
- tests when parsing or summary logic could silently regress

Avoid:

- hidden local aliases
- complex shell pipelines that are hard to review
- heavyweight dependencies for simple transforms

## Verification guidance

For text outputs:

- `test -s <file>`
- `wc -l <file>`
- spot-check deterministic ordering or representative items

For JSON outputs:

- validate JSON syntax
- verify required keys
- verify counts or summary fields
- run helper-script tests when present

For live captures specifically:

- confirm the saved request metadata matches the intended parameters
- confirm the status interpretation is correct
- confirm the output time boundary is understandable

## Avoiding footguns

- Do not paste large outputs into the README.
- Do not rely on personal shell history as the only recipe.
- Do not hide endpoint semantics that matter to interpretation.
- Do not store raw sensitive headers, tokens, or cookies in captured artifacts.

## Recommended example pattern

For a non-trivial query job, the preferred pattern is:

1. Create a job folder.
2. Add a small script.
3. Add tests if the script parses or transforms data.
4. Add `README.md` with request, inputs, run steps, outputs, and verification.
5. Commit the resulting output artifact.

That pattern scales better than unstructured one-liners and keeps future reruns tractable.
