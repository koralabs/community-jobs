# Community Jobs - Glossary

This glossary defines the terms used throughout `docs/product/*`, `docs/spec/*`, and job folder READMEs.
The point is not to be academic; it is to keep contributors, reviewers, and AI executors using the same words for the same concepts.

## Artifact

A file or set of files committed in this repo that represents the durable output of a job.

Examples:

- `output.txt` from a community data export
- `output.json` from a live API capture
- `report.md` containing investigation notes
- `README.md` that preserves tracking context for work happening in another repo

An artifact is not just any file that happens to exist.
It is a file worth keeping because it answers a request, preserves context, or makes later review possible.

## Job

A bounded unit of work that produces one or more artifacts.

A job should always have:

- a request or reference
- inputs
- steps
- outputs
- verification

In this repo, a job usually maps to one folder at repository root.

## Job folder

A directory at repo root that contains the files for exactly one job.

Typical contents:

- `README.md` describing context and reproducibility
- one or more outputs
- helper scripts or tests when needed

Examples in this repo:

- `can-you-give-me-a-issue-1/`
- `list-the-first-page-of-issue-27/`
- `api-timeout-remediation-149a610d/`

## Output

The concrete result of a job.
Outputs are often committed files such as:

- text exports
- JSON payload captures
- markdown summaries
- checklists

The output should answer the request directly, while the README explains how that output was produced and how to trust it.

## Provenance

The chain of custody for an artifact.

Provenance answers questions such as:

- where did the input come from?
- which snapshot, commit, branch, or endpoint was used?
- when was the artifact generated?
- what transformation was applied?

Good provenance is what turns a file from "something someone made once" into "an artifact we can rely on."

## Snapshot

A point-in-time capture of data used as an input to a query job.

Examples:

- a JSON export produced by a sibling service repo
- a saved dataset keyed to a specific commit or branch
- a local file created during a documented extraction workflow

Snapshots often live outside this repo.
The job README should state where they came from and how to obtain them.

## Live capture

A job that queries a live endpoint or environment directly and commits a structured result.

Unlike snapshot-based jobs, live captures need stronger documentation for:

- endpoint URL
- query parameters
- headers
- rate limiting
- freshness or catch-up semantics

The `list-the-first-page-of-issue-27/` folder is the clearest current example in this repo.

## Verification

Checks that provide confidence an artifact is correct.

Examples:

- file exists and is non-empty
- line count matches an expected invariant
- JSON parses and includes required keys
- links point to the intended issue or PR
- tests exercise the transformation logic

Verification should be able to catch a real mistake, not just prove that a file was written.

## Owning repo

The repository where the canonical implementation or behavior change belongs.

For query artifacts, the owning repo is often the repo that produced the input snapshot or exposed the endpoint being queried.
For bug fixes or features, the owning repo is where the actual code should change.

This distinction matters because `community-jobs` stores artifacts and tracking context, not the primary implementation of sibling applications.

## Tracking artifact

A job whose main value is preserving safe public context about work happening elsewhere.

A tracking artifact should identify:

- the owning repo
- the linked issue or PR when available
- the current status
- any stable evidence identifiers that help explain the request

It should not pretend implementation happened here if it did not.

## Helper script

A small script committed in a job folder to make artifact generation reproducible.

Helper scripts are appropriate when:

- the transformation logic is non-trivial
- the same command is likely to be rerun later
- inline shell would be hard to review

They should remain lightweight and job-scoped rather than turning into a generalized application.

## K.O.R.A. executor

K.O.R.A. is the internal execution system used to fulfill community requests and operational jobs across the Kora/Handles ecosystem.

In this repo, the executor may:

- create job folders
- write READMEs
- generate outputs
- include identifiers such as `action_id` and `job_id` for traceability

Executor runtime artifacts may exist locally under `.kora/`, but those logs are not the preferred durable artifact model for this repo.

## `action_id` / `job_id`

Identifiers produced by the executor runtime that help correlate:

- the high-level action
- the specific job run
- related local logs or upstream automation context

Including them in a README is useful whenever the job was created by automation or when future troubleshooting may need to correlate the artifact with a specific execution.

## Legacy artifact

A folder that remains useful as history but does not represent the preferred current pattern.

In this repo, some patch-style remediation folders are legacy artifacts.
They may still be valuable for auditability, but new work should generally prefer:

- direct implementation in the owning repo
- a lightweight tracking artifact here, when needed

## Docs readiness

The state in which `docs/product/` and `docs/spec/` give future contributors enough context to add or review artifacts without reverse-engineering the repo from examples alone.

Good docs readiness means:

- purpose is explicit
- scope boundaries are explicit
- templates and checklists exist
- current artifact patterns are documented
