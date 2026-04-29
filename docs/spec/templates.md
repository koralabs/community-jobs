# Templates (Spec)

Use these templates when adding new job folders.
They are intentionally a little verbose so authors have room to delete irrelevant sections rather than forgetting important ones.

## Template A: Snapshot-based community query artifact

```md
# <short title> (issue #<n>)

## original_request
<paste request text or summarize it>

## references
- issue: `koralabs/community-jobs#<n>`
- executor:
  - action_id: `<uuid>`
  - job_id: `<uuid>`

## inputs
- source repo: `<repo>`
- snapshot path: `<path>`
- snapshot notes: <how it was produced and when>

## setup/install steps
1. <runtime requirement>
2. <required local files present>

## run steps
1. <command(s) used to generate the output>

## outputs
- `output.txt`: <what it contains>

## test/verification steps
1. <non-empty check>
2. <count or invariant check>
3. <spot check or ordering check>

## assumptions / limitations
- <list>
```

## Template B: Live API query artifact

```md
# <short title> (issue #<n>)

## original_request
<paste request text or summarize it>

## references
- issue: `koralabs/community-jobs#<n>`
- executor:
  - action_id: `<uuid>`
  - job_id: `<uuid>`

## request details
- endpoint: `<url>`
- query parameters: `<params>`
- headers:
  - `Accept`: `application/json`
  - `User-Agent`: `<from KORA_USER_AGENT when required>`
- timeout: `<seconds>`
- rate limiting: `<policy>`

## setup/install steps
1. <runtime requirement>
2. <env var requirements, if any>

## run steps
1. <command to capture the output>

## outputs
- `output.json`: <top-level shape and meaning>

## test/verification steps
1. <run script tests>
2. <validate JSON>
3. <check summary fields or status semantics>

## assumptions / limitations
- <point-in-time capture notes>
```

## Template C: Cross-repo tracking artifact

```md
# <owning repo> <request or incident> tracking

## references
- community tracking issue: `<org/repo#issue>`
- owning repo: `<repo>`
- owning issue or PR: `<org/repo#issue-or-pr>`
- executor:
  - action_id: `<uuid>`
  - job_id: `<uuid>`

## context
- request, alert, or ticket summary: <summary>
- safe evidence identifiers: <ids>
- current status: <status>

## what belongs elsewhere
- implementation repo: `<repo>`
- reason: <why code changes belong there>

## verification
1. <confirm issue or PR links are correct>
2. <confirm status summary matches current state>

## notes
- <risks, follow-ups, anything special>
```

## Template D: Investigation notes or runbook

```md
# <title>

## context
- request / ticket / alert: <id>
- date: <YYYY-MM-DD>

## environment
- service or repo: <name>
- branch, tag, or snapshot: <reference>

## reproduction steps
1. ...

## observations
- ...

## conclusion
- ...

## next steps
- ...
```

## Template usage notes

- Delete sections that truly do not apply, but do not remove provenance or verification just because they take a few extra lines.
- Keep the job README focused on the artifact in that folder rather than turning it into general ecosystem documentation.
- If the artifact depends on a sibling repo, prefer a precise path or link over vague prose.
