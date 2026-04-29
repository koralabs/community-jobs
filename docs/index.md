# `community-jobs` documentation

This `docs/` folder explains how `koralabs/community-jobs` should be used and what should, and should not, be stored here.

The short version:

- store durable community query artifacts here
- store lightweight public tracking context here when it helps people follow work happening in another repo
- keep implementation changes in the owning repo instead of using this repo as a general patch drop

If you are looking for a specific output, start at the repository root and open the relevant job folder.
Each job folder should stand on its own and include its own `README.md`.

## Table of contents

### Product

- [Overview](product/overview.md)
- [Job Types](product/job-types.md)
- [Workflow](product/workflow.md)
- [Data Handling](product/data-handling.md)
- [Quality Bar](product/quality-bar.md)
- [Glossary](product/glossary.md)

### Spec

- [Repo Structure](spec/repo-structure.md)
- [Job README Format](spec/job-readme-format.md)
- [Community API Query](spec/community-api-query.md)
- [Artifact Lifecycle](spec/artifact-lifecycle.md)
- [Templates](spec/templates.md)
- [Checklists](spec/checklists.md)

## Quick start: adding a new artifact

1. Create a new job folder at repo root using [Repo Structure](spec/repo-structure.md).
2. Add a `README.md` following [Job README Format](spec/job-readme-format.md).
3. Add committed outputs that belong in this repo, usually exports, reports, or lightweight tracking notes.
4. Add meaningful verification steps to the README.
5. Review the diff for secrets, private data, or oversized artifacts before opening a PR.

If the request belongs to another repo:

- name the owning repo clearly
- link the owning issue or PR when available
- keep implementation work in the owning repo
- use this repo only for tracking context that is safe and useful to keep here

## Current examples in this repo

- `can-you-give-me-a-issue-1/` is a snapshot-based export job that writes a plain-text list of handles.
- `list-the-first-page-of-issue-27/` is a live API query job that captures a structured JSON artifact plus tests for the helper script.
- `api-timeout-remediation-*` folders are legacy tracking or patch handoff artifacts that remain useful as audit history, but they should not define the preferred pattern for new work.
