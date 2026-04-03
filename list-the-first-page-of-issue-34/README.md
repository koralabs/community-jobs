# community API query artifact (issue #34)

## original_request
List the first page of handles and summarize the total count returned.

## setup/install steps
1. Ensure Python 3 is available:
   ```bash
   python3 --version
   ```
2. No package installation is required. The script uses only the Python standard library.

## environment variable requirements
- `KORA_USER_AGENT`
  - Required for live `*.handle.me` requests.
  - The script reads it from the current environment first, then from `--env-file` if it is not already exported.
  - In the Kora ecosystem checkout, the default `--env-file` location is `~/src/koralabs/.env`.

## run steps
1. From the repository root, run:
   ```bash
   python3 list-the-first-page-of-issue-34/list_first_page_handles.py --page 1 --records-per-page 100 --env-file ~/src/koralabs/.env --output list-the-first-page-of-issue-34/output.json
   ```
2. The script queries `https://api.handle.me/handles?page=1&records_per_page=100` with `Accept: application/json`.
3. It also sends the required `KORA_USER_AGENT` value as the `User-Agent` header.
4. The captured artifact is written to `list-the-first-page-of-issue-34/output.json`.

## test/verification steps
1. Run the local tests:
   ```bash
   python3 -m unittest discover -s list-the-first-page-of-issue-34 -p 'test_*.py'
   ```
2. Refresh the live API artifact:
   ```bash
   python3 list-the-first-page-of-issue-34/list_first_page_handles.py --page 1 --records-per-page 100 --env-file ~/src/koralabs/.env --output list-the-first-page-of-issue-34/output.json
   ```
3. Inspect the captured summary:
   ```bash
   python3 - <<'PY'
   import json
   from pathlib import Path
   data = json.loads(Path("list-the-first-page-of-issue-34/output.json").read_text())
   print(data["summary"])
   print(data["handle_names"][:5])
   PY
   ```
