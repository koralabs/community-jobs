# community API query artifact (issue #1)

## original_request
can you give me a list of all handle names as plain text?

## setup/install steps
1. Ensure Node.js is installed (`node -v`).
2. Ensure this sibling snapshot source file exists: `../api.handle.me/tmp/handles_utxos.json`.

## run steps
1. From repo root, run:
   ```bash
   node -e "const fs=require('fs'); const src='../api.handle.me/tmp/handles_utxos.json'; const out='can-you-give-me-a-issue-1/output.txt'; const data=JSON.parse(fs.readFileSync(src,'utf8')); const names=Object.keys(data.mintingData||{}).sort(); fs.writeFileSync(out,names.join('\\n')+'\\n'); console.log('count',names.length);"
   ```
2. The plain-text handle list is written to `can-you-give-me-a-issue-1/output.txt`.

## test/verification steps
1. Verify the file exists and is non-empty:
   ```bash
   test -s can-you-give-me-a-issue-1/output.txt
   ```
2. Verify line count from this run:
   ```bash
   wc -l can-you-give-me-a-issue-1/output.txt
   ```
3. Verify the count matches keys in snapshot:
   ```bash
   node -e "const fs=require('fs'); const data=JSON.parse(fs.readFileSync('../api.handle.me/tmp/handles_utxos.json','utf8')); console.log(Object.keys(data.mintingData||{}).length);"
   ```
