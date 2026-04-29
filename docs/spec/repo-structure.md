# `community-jobs` - Repository Structure (Spec)

This document specifies how `community-jobs` is laid out and how new artifacts should be added.

The repository is an artifact store, not an application.
Most meaningful top-level folders are job folders containing a README plus outputs, scripts, tests, or tracking notes for one bounded task.

## Top-level layout

At repo root you will commonly find:

- `docs/`
  - canonical documentation for this repo
  - `docs/index.md` is the table of contents
  - `docs/product/` explains purpose, safety, workflow, and quality expectations
  - `docs/spec/` defines formats, templates, and checklists
- `<job-folder>/`
  - one directory per job
- `.kora/`
  - local K.O.R.A. runtime artifacts such as executor logs or scratch output
- root metadata such as `README.md`, `.gitignore`, and `AGENTS.md`

## What is a job folder

A job folder is the atomic storage unit in this repo.
It should be reviewable as a standalone package.

### Required contents

- `README.md`
  - required
  - documents context, inputs, run steps, outputs, and verification

### Common optional contents

- `output.txt`, `output.json`, `output.csv`, or `report.md`
- a small helper script such as `.py` or `.js`
- tests for the helper script when logic is non-trivial
- secondary notes or checklists when they materially improve reviewability

### What does not belong in a job folder

- secrets or credentials
- entire clones of sibling repos
- large binary blobs or database dumps
- unexplained files with no provenance
- new cross-repo code patch handoff artifacts as the default pattern

## Naming conventions

Preferred patterns:

1. Issue-driven community requests: `<request-slug>-issue-<number>/`
2. Executor or tracking artifacts: `<slug>-<short-job-id>/`

Examples already present:

- `can-you-give-me-a-issue-1/`
- `list-the-first-page-of-issue-27/`
- `api-timeout-remediation-149a610d/`

If a longer folder name prevents ambiguity, prefer clarity over brevity.

## `.kora/` executor artifacts

The executor may produce logs under `.kora/executor-logs/`.

Rules:

- do not intentionally commit new executor logs
- keep durable outputs in job folders, not in `.kora/`
- if executor logs matter, summarize the important points in a job README instead of committing raw logs

The current `.gitignore` already ignores new executor logs.
Historical committed logs may exist on older branches or commits, but they are not the model to follow.

## Linking and discoverability

To keep navigation consistent:

- update `docs/index.md` when adding canonical docs under `docs/product/` or `docs/spec/`
- keep each job self-contained enough that someone can understand it by opening only that folder
- include issue references, owning repo references, and executor identifiers in the job README when relevant

Job folders do not need to be listed individually in the docs TOC.
Their README is the navigation entry point.

## Legacy patch folders

Older folders in this repo may include patch artifacts or cross-repo remediation handoffs.
They remain part of the historical record, but they should be treated as legacy examples.

For new work, prefer:

- code changes in the owning repo
- a tracking artifact here only when the public trail is useful
