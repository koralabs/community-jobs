# Community Jobs - Workflow

This repository is intentionally simple, but the workflow around it matters.
The goal is not just to create files; the goal is to create artifacts that another engineer, reviewer, or executor can trust later.

This document describes the recommended lifecycle from intake to artifact to review.

## 1) Intake and triage

Work usually begins with one of the following:

- a GitHub issue in `koralabs/community-jobs`
- a community request that needs a reproducible export
- a ticket, alert, or thread that needs durable public tracking context
- a linked issue in another repo that owns the real implementation

At intake time, answer five questions before you write anything:

1. What is the job type?
2. What is the source of truth?
3. Is the output safe to commit?
4. Which repo owns the real implementation, if any?
5. What is the smallest durable artifact that would fully answer the request?

That short triage step prevents most repository drift.

## 2) Choose inputs and lock provenance

Artifacts are only useful if they can be reproduced or at least defended.
Before you generate output or write tracking notes, record the inputs that matter.

Common provenance fields include:

- snapshot file paths
- commit hashes or branch names
- endpoint URLs and query parameters
- generation date or capture timestamp
- environment or service version when relevant

For snapshot-based jobs, the key is usually "which file did this come from?"
For live API jobs, the key is usually "which endpoint did we call, with which parameters, and at what time?"
For tracking artifacts, the key is usually "which repo, issue, PR, or alert are we summarizing?"

If provenance is fuzzy, the artifact will not age well.

## 3) Choose the right execution pattern

Not every request should be fulfilled the same way.
Pick the simplest pattern that preserves correctness:

- one-liner + output file when the transformation is trivial and obvious
- committed helper script when the logic is non-trivial or needs tests
- narrative README-only tracking artifact when the primary output is context rather than transformed data

Prefer readability over cleverness.
The next person should be able to understand how the artifact was produced without reverse-engineering shell syntax.

## 4) Create the job folder

Create one folder per job and keep everything needed for review inside it.
That usually includes:

- `README.md`
- one or more output files
- helper script(s) if needed
- tests if the helper script contains logic that could silently regress

Do not scatter a single job across multiple unrelated folders.
If a later rerun materially changes the input or semantics, create a new job folder instead of mutating history in place.

## 5) Write the README before the details get fuzzy

Every job README should answer the same basic questions:

- What was requested?
- What inputs were used?
- What command or steps produced the artifact?
- What files were produced?
- How should a reviewer verify correctness?

The README does not need to be long, but it does need to remove guesswork.

For cross-repo tracking artifacts, the README must also make it hard to confuse:

- which repo owns implementation
- which repo stores the public tracking note
- what the current linked issue or PR is

## 6) Generate outputs carefully

When producing outputs:

- prefer deterministic ordering
- avoid hidden local state
- keep dependencies lightweight
- store outputs as files rather than pasting them into the README

If a job hits a `*.handle.me` endpoint directly, the surrounding ecosystem rules matter:

- use an explicit `User-Agent` loaded from `KORA_USER_AGENT`
- use clear request headers such as `Accept: application/json`
- respect rate limits and bounded request pacing
- document whether the endpoint returns a point-in-time snapshot or can report a catch-up state

The current live API example in this repo already documents `Accept: application/json`, rate limiting, and `200` versus `202` semantics in code.
Future updates should continue moving these networked jobs toward explicit, policy-compliant request metadata.

## 7) Verify before treating the artifact as done

Verification requirements vary by job type.

For query artifacts:

- confirm output files exist
- validate counts, ordering, or required keys
- sanity-check representative values

For tracking artifacts:

- confirm links point to the intended repo and issue or PR
- confirm status is accurate
- confirm the text does not imply the fix landed here when it belongs elsewhere

For runbooks or investigations:

- confirm reproduction steps work as written
- confirm evidence references are stable
- confirm the conclusion matches the observations

The key is that verification must catch a real failure mode.
"File exists" alone is not enough unless the request truly only asked for a placeholder.

## 8) Review like code, not like scratch notes

Even though this repo often stores outputs rather than product code, review should still be disciplined.

Reviewers should check:

- safety of committed data
- clarity of the README
- relevance of verification steps
- reasonableness of file size
- cross-repo ownership boundaries

A poor artifact wastes future time in exactly the same way that poor code does.

## 9) Maintain artifacts deliberately

Artifacts sometimes need follow-up:

- the same query may need to be rerun against a new snapshot
- a tracking artifact may need the final PR link
- a runbook may need a corrected step

Use additive history when the meaning changes materially.
Use in-place edits only for small clarifications or metadata additions that do not alter the substance of the artifact.

## 10) Know when not to use this repo

Do not force a job into `community-jobs` just because it is convenient.
If the real deliverable is:

- a code fix
- a production configuration change
- canonical product documentation
- a private operational record

then the primary work belongs somewhere else.

This repo succeeds by being selective.
It should store durable outputs and tracking context, not absorb every adjacent task.
