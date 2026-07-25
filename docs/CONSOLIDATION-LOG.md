# Website Folder Consolidation — 2026-07-25

**Executed by:** Claude (Cowork mode), at Jun's request.
**Reason:** Website working files were scattered across multiple folders on
disk with no clear "source of truth." pssarmiento.com is now live on GitHub
Pages; this pass consolidates around that fact and archives what's superseded.

## Starting state (as found)

Three unrelated locations held website-related material:

1. `PS Group/pssarmiento-site/` — **the live repo.** Git-tracked, remote
   `github.com/oscarjr-oes/pssarmiento-site`, branch `main`, deployed via
   GitHub Pages to `pssarmiento.com` (CNAME present, GA4 + Formspree wired).
2. `Projects/PS Group Webpage/Final/psgroup-site/` — an **un-versioned**
   `.dc.html` packaging pass, built as source/spec material for a native Wix
   Studio rebuild (see its own `README.md`, `WIX-BUILD-GUIDE.md`,
   `pssarmiento-execution-plan.md`). Never deployed directly. No `.git`.
3. `PS Group/handoff/` — three markdown handoff docs (`HANDOFF.md`,
   `WIX-NEWS-PROMPT.md`, `GITHUB-PAGES-PROMPT.md`) describing the GitHub
   Pages deployment and the still-open Wix News subdomain work, living as a
   sibling to the repo rather than inside it.

There were also two independent `graphify-out/` directories:
   `PS Group/pssarmiento-site/graphify-out/` (inside the repo, untracked)
   and `PS Group/Operations/graphify-out/` (unrelated to the site, left
   untouched by this pass).

## What changed

1. **Archived** `Projects/PS Group Webpage/Final/psgroup-site/` in full to
   `PS Group/_archive/psgroup-site-2026-07-25/` (verbatim copy). The
   original folder was left in place (not deleted — outside this assistant's
   permissions/scope to remove), with an `ARCHIVED_NOTICE.md` added at its
   root pointing here and explaining status.
2. **Moved** (copied; originals left with a pointer note) the three
   `PS Group/handoff/` docs into this repo at `docs/HANDOFF.md`,
   `docs/WIX-NEWS-PROMPT.md`, `docs/GITHUB-PAGES-PROMPT.md` — so they now
   live with the code GitHub Desktop manages, and travel with future commits
   instead of drifting out of sync in a sibling folder.
3. **Added `.gitignore`** entries for `graphify-out/` and `.DS_Store` in this
   repo, since `graphify-out/` was showing as untracked noise in
   `git status` / GitHub Desktop.
4. **This file** — filed as the trace record.

## Decision going forward

- **GitHub is the manager of record for the main site** (`pssarmiento.com`),
  via this repo + GitHub Desktop + GitHub Pages. This was already true and
  is unchanged; this pass just cleans up the scattered supporting files
  around that fact.
- **Wix's only remaining scope is the News/Blog subdomain**
  (`news.pssarmiento.com`) — see `docs/WIX-NEWS-PROMPT.md`. The Wix "full
  site rebuild" plan captured in the archived `psgroup-site/` package is
  superseded; do not resume it as a full-site plan. If the News subdomain
  work resumes, the design-token spec in the archived
  `WIX-BUILD-GUIDE.md` / `pssarmiento-execution-plan.md` is still the right
  reference for styling that shell to match the main site.

## Effect on graphify scans

- Any graphify scan run against the **old** `PS Group/handoff/` location
  (e.g. one that indexed `HANDOFF.md`, `WIX-NEWS-PROMPT.md`,
  `GITHUB-PAGES-PROMPT.md` at that path) is now stale for those three files
  — they live at `pssarmiento-site/docs/` instead. Re-run/re-index if a scan
  depends on those paths resolving.
- A graphify scan run against the **archived** `psgroup-site/` Wix package
  (original location `Projects/PS Group Webpage/Final/psgroup-site/`) is
  still valid at that original path (nothing was deleted there — only the
  copy at `PS Group/_archive/psgroup-site-2026-07-25/` is new and
  unscanned). Treat that content as historical/reference-only per
  `ARCHIVED_NOTICE.md`, not as an active build target.
- The repo's own `graphify-out/` (inside `pssarmiento-site/`) is unaffected
  in content, but is now `.gitignore`'d — it will no longer show as an
  untracked-file prompt in `git status`/GitHub Desktop. It was already
  noted in `docs/HANDOFF.md` as "local generated analysis output, not
  included in the website deployment."
- `PS Group/Operations/graphify-out/` is unrelated to the website and was
  not touched.

## Not done (out of scope / needs a human)

- Nothing was deleted anywhere — only copied/archived and annotated. If Jun
  wants the original `Projects/PS Group Webpage/Final/psgroup-site/` folder
  actually removed from disk (now that it's archived), that needs to be
  done manually or with explicit delete confirmation.
- Git changes below are **committed locally** in this repo. They still need
  to be pushed via GitHub Desktop (or `git push`) for `origin/main` to pick
  them up.
