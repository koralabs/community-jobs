# community-jobs canonical contract

## Purpose and authority

I am a scratch collection: outputs of community requests and K.O.R.A. executor jobs (a handle-name list, remediation notes, one patch destined for `api.handle.me`, executor logs). I own no application code and I am not a source of truth for anything. The owning repository (for the patch, `api.handle.me`) is. I must never become a back channel for secrets or an unreviewed way into another repo. Ecosystem rules: `../AGENTS.md`. The enclave is only the two policy files, because nothing else here carries behaviour.

## Invariants (must never be violated)

1. No secrets in the repo: no keys, tokens, mnemonics, `.env` values or credentialed URLs, including inside executor logs, patches and job outputs. (The only check today is a manual scan I ran while writing this: the tracked files contain hex and base64-looking data but no key-shaped secret. No automated test enforces it.)
2. A patch or snippet kept here is never executed or applied from here. It is applied in its owning repository through that repository's own PR and tests. (`docs/ci-validation.md` states this; no test can enforce it.)
3. A file here never claims chain accuracy. The handle-name list in `can-you-give-me-a-issue-1/output.txt` is a snapshot derived from an API snapshot file outside the repo; the owning API is authoritative. (Convention only.)
4. No unresolved merge-conflict markers in tracked non-Markdown files. (`.github/workflows/pr-tests.yml` "Artifact validation" checks this on every PR.)

## Boundaries and known limits

- CI proves conflict-marker hygiene only. It does not prove the patch applies, the list is accurate, or logs are clean (`docs/ci-validation.md`).
- `.kora/executor-logs/` is listed in `.gitignore` but six pairs of logs are already tracked, so the ignore rule does not protect them. They could contain anything an executor printed.
- The job output can go stale the moment it is written.

## Refactors needed to enforce this

- Add a secret-pattern scan (tokens, key-shaped strings, credentialed URLs) to the existing artifact validation workflow, so invariant 1 has a test.
- Remove the tracked `.kora/executor-logs/` files from git so the ignore rule works, or move executor output to the box log store.
- Move finished remediation patches into their owning repositories and delete them here.
