# PS Group Website Archive Transfer Log

**Date:** 2026-07-25  
**Status:** Drive transfer in progress; local deletion is not yet authorized.

## Source and destination

- Active source of truth: `pssarmiento-site/`
- GitHub: `https://github.com/oscarjr-oes/pssarmiento-site`
- Legacy working folder: `Projects/PS Group Webpage/`
- Manual-upload package: `PS-Group-Website-Working-Folder-2026-07-25.zip`
- Package SHA-256: `fb40cdb07386c3681a52e2c49866b561920707df4316c11f602221b6319b36db`
- Package size at creation: approximately 262 MB
- Drive destination: `Apps in Development Archive/PS Group Website/Completed Website Build - Archived/`
- Drive verification: uploaded as `PS-Group-Website-Working-Folder-2026-07-25.zip`, Drive-reported size `275051932` bytes, file ID `1bCDNXi7plPh3ZlhRbYed_L0V7KjvSo_4`

## Pending Wix work

The remaining Wix scope is the blog/news work. Keep these references available in:

`Apps in Development Archive/PS Group Website/Wix Blog - Pending/`

The active local reference is `pssarmiento-site/docs/WIX-NEWS-PROMPT.md`.

## Deletion hold

Do not delete the local legacy folder until the uploaded ZIP is verified in Drive by filename, size, and SHA-256 where practical. The ZIP is a recoverable archive; the local source folder is not to be treated as disposable until verification is complete.

## Graphify impact

- `pssarmiento-site/graphify-out/` is the active repo's generated graph and is unaffected by archiving the legacy folder.
- `Operations/graphify-out/` is unrelated and must not be deleted or rebuilt as part of this website cleanup.
- `Projects/PS Group Webpage/graphify-out/` belongs to the legacy workspace. Deleting that workspace removes the local graphify index, report, and cache for the historical website materials. It can be rebuilt from the uploaded ZIP or the Drive archive if needed.
- Any graphify result pointing at `Projects/PS Group Webpage/` becomes stale after deletion because its source paths will no longer exist. Re-run graphify only if historical-search capability is needed; do not merge its historical graph into the active repo graph without an explicit decision.

## Benchmark history

The benchmark CSVs from `Projects/PS Group Webpage/Benchmark stats/` were separately copied to:

`Apps in Development Archive/PS Group Website/Benchmark History/`

They should be treated as comparison snapshots, not active site source. The filenames with `(1)` and `(2)` are not exact byte-for-byte duplicates of the unsuffixed export; retain all six until their differing date ranges/columns are reviewed.

## Historical graphify storage

The legacy graphify report, manifest, graph JSON, and cost JSON were separately copied to:

`Apps in Development Archive/PS Group Website/Historical Graphify Snapshot/`

Do not place this historical graphify output into the active GitHub source. The repo's `graphify-out/` remains the current-site analysis location and is intentionally ignored by Git. Historical graphify should remain a Drive/archive snapshot and be rebuilt only from the legacy package when needed.

## After verification

1. Keep `pssarmiento-site/` as the only active local website source.
2. Preserve this log in the GitHub repo.
3. If the legacy folder is removed, add the deletion date and Drive verification details below.

### Drive verification / deletion record

Verified on 2026-07-25. Local legacy website workspace may now be removed after the graphify/readme records in `pssarmiento-site/docs/` are retained.
