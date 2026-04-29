# Artifact Lifecycle and Versioning (Spec)

Artifacts in this repo are durable records, not disposable scratch files.
That means changes to them should preserve traceability rather than erasing history silently.

This document defines how artifacts should evolve over time.

## General principle: prefer additive history

When the substance of an artifact changes, prefer creating a new job folder rather than silently replacing the old output in place.

The goal is to preserve:

- what was produced at the time of the original request
- what later changed
- why the later version exists

Silent replacement makes old discussions and linked issues harder to interpret.

## Create a new job folder when

Create a new folder if any of the following are true:

- the input snapshot changed
- the endpoint or environment changed materially
- the semantics of the request changed
- the output format changed
- the linked issue or executor run needs separate traceability
- the job entered a new phase that deserves its own artifact

Examples:

- same query, new snapshot: new folder
- same live capture, but now against a materially different endpoint contract: new folder
- same tracking topic, but a later executor run needs its own audit trail: usually new folder

## Update in place when

It is reasonable to update an existing folder in place when:

- fixing typos in the README
- clarifying provenance without changing outputs
- adding verification steps
- adding links to the final owning PR or issue
- correcting a broken local path reference

If you regenerate the output, default back to "create a new folder" unless you can prove the resulting artifact is substantively identical and the in-place update improves clarity without obscuring history.

## Query artifact versioning patterns

### New snapshot, same transform

Create a new folder.
The snapshot boundary is part of the artifact identity.

### Same snapshot, stronger tests or better README

Update in place.
The artifact meaning did not change; only its documentation improved.

### Same request, different output format

Usually create a new folder, or at minimum make the change extremely explicit in the README.
Format changes can affect downstream users as much as content changes do.

### Live endpoint capture repeated later

Create a new folder when the later capture is meant to preserve a different moment in time.
Live captures are intrinsically time-bound, so the date or run identity matters.

## Tracking artifact versioning patterns

Create a new folder when:

- the owning issue or PR changed materially
- a new executor run should be traceable separately
- the artifact moved from investigation to remediation to closure and each phase needs a distinct record

Update in place when:

- you are adding the final PR link
- you are clarifying context
- you are adding a safe status update that does not change the artifact's identity

## Deprecation and supersession

Sometimes an older artifact is still valid as history but no longer the best current reference.
In that case:

- add a short note in the old README
- link to the superseding folder
- explain briefly why it was superseded

Examples:

- later snapshot with corrected assumptions
- later tracking artifact with the canonical PR link
- later runbook that replaces a rough early investigation note

Deletion should be rare and reserved for unsafe or accidental content.

## Cleanup policy

Do not delete history just because it is old.
This repo exists partly to preserve a public trail.

Cleanup should focus on:

- improving README clarity
- marking legacy patterns as legacy
- preventing new unsafe artifacts
- reducing confusion about which folder is canonical for a given question

## Linking to canonical outcomes

When a tracking artifact points to work in another repo:

- add the canonical issue or PR link once it exists
- keep the summary concise
- avoid copying large amounts of owning-repo implementation detail

When a query artifact was used to answer a support request:

- preserve the artifact
- optionally note where it was shared, but avoid copying private thread contents into the repo

## Review implications

Reviewers should ask:

- does this change preserve interpretability of existing history?
- should this have been a new folder instead of an edit?
- does the README explain the relationship between the old and new artifacts?

That discipline keeps the repo useful months later, not just at PR time.
