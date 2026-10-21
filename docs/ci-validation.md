# CI validation scope

## What this repository owns

This repository collects community request/job outputs and remediation artifacts. The tracked content before this CI naming correction comprises Markdown tracking/apply instructions, executor logs, a generated handle-name text output, and one `.patch` artifact. It has no application source tree, package/build manifest or owned executable test suite. There are currently no tracked `.json` files.

The patch embeds TypeScript/application changes and tests intended for **api.handle.me**, not executable source owned here. The accompanying tracking documents explicitly name that owning repository and explain applying/verifying the patch there. Commands quoted in Markdown are artifact reproduction instructions, not a local application entrypoint. Do not apply patches, execute copied financial/runtime code, run provider queries or reach into sibling application builds just to make this collection report unit coverage.

## What CI proves

`Artifact conflict markers and optional JSON` checks tracked non-Markdown content for unresolved conflict markers and syntax-checks any tracked JSON files if present. The JSON command is conditional; with the current inventory it processes **zero files**. The meaningful current scope is conflict-marker hygiene for the artifact collection. The workflow runs for every pull request and default-branch push.

This is **artifact hygiene only**, not application lint/build/unit tests, patch applicability, handle-output chain accuracy, executor correctness or end-to-end acceptance. A green check must not be cited as coverage of the application code quoted in logs or patches.

During the required-context migration, `Lint, build and unit tests` is retained solely as a temporary compatibility gate requiring the honestly named validation job to succeed. Once the new successful default context is required, the compatibility gate is removed in a follow-up PR without disabling protection.

## Applicability boundary

Application changes and their native tests belong to their named owning repositories. This repository is not excluded because it is old; its checked-in artifacts were inspected. If executable source/build targets become owned here, re-evaluate CI and add real tests rather than continuing to claim artifact validation as application acceptance.
