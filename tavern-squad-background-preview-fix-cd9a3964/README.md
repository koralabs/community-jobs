# handle.me Tavern Squad background preview fix (tracking)

Owning repo: `handle.me`  
Tracking issue (artifact repo): `koralabs/community-jobs#11`  
Tracking issue (owning repo): `koralabs/handle.me#1137`

Ticket context
- Discord ticket thread/channel: `1484131323886178436` (guild `882401389328875620`)
- executor job_id: `cd9a3964-07fd-4d86-ad1b-172d5ec747c9`

## Summary
The `Tavern Squad - Backgrounds` collection preview image was configured to use a `pbs.twimg.com` URL that now returns `404`, causing the collection tile image to render as broken.

This patch swaps the collection preview image to a durable IPFS URL and adds a small regression test to ensure we don’t reintroduce `pbs.twimg.com` as a source for that collection image.

## Patch
- `handle.me-tavern-squad-background-preview.patch`

Base branch (target): `mainnet`

## Apply (manual)
1. In a clone of `handle.me`, checkout and update the base branch:
   ```bash
   git checkout mainnet
   git pull --ff-only
   ```
2. Create a working branch:
   ```bash
   git checkout -b kora/bugfix-tavern-squad-preview
   ```
3. Apply the patch:
   ```bash
   git apply /path/to/community-jobs/tavern-squad-background-preview-fix-cd9a3964/handle.me-tavern-squad-background-preview.patch
   ```

## Verify
1. Confirm the new preview image URL is reachable:
   ```bash
   curl -sS -o /dev/null -w "status=%{http_code}\n" "https://public-handles.myfilebase.com/ipfs/bafybeicesd5prafy55k2nsmqwxwde7sooindt7pmevcbswkm4dve4jg2km?img-width=512"
   ```
2. Run Handle.me tests (from the owning repo):
   ```bash
   cd static
   yarn
   yarn lint
   yarn test

   cd ../bff
   yarn
   yarn build:tsc:noEmit
   yarn test
   ```
3. Manual UI verification (mainnet):
   - Navigate to personalization → Backgrounds marketplace.
   - Confirm `Tavern Squad - Backgrounds` collection tile renders an image (not broken).

## Notes / Follow-ups
- The `ts.backgrounds` handle datum’s `collectionImage` currently decodes to the same broken `pbs.twimg.com` URL. If any surfaces read the collection image from datum (instead of config), an operator-led on-chain update may still be required.
