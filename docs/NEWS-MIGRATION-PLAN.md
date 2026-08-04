# News/Blog Migration Plan — Wix → GitHub Pages + Decap CMS

**Status:** DRAFT — supersedes `docs/WIX-NEWS-PROMPT.md`
**Prepared by:** Claude (Cowork mode), at Jun's request · 2026-08-04
**Supersedes open item:** "Configure `news.pssarmiento.com` in Wix and DNS" (`docs/HANDOFF.md` Remaining TODOs)

## 0. Why this replaces the Wix News plan

The original plan (`docs/WIX-NEWS-PROMPT.md`) kept Wix as the News/Blog host on a `news.pssarmiento.com` subdomain, which requires an admin action in Wix plus a CNAME record from whoever controls DNS. Neither is owned by Jun today:

- **DNS** for `pssarmiento.com` is managed by someone else (nameservers are `ns14/ns15.wixdns.net`).
- **The Wix Blog/CMS** is managed by someone else.

This plan instead folds News into the existing GitHub Pages site (`oscarjr-oes/pssarmiento-site`, already live at `pssarmiento.com`) as a `/news/` path, edited via **Decap CMS**. That removes the DNS dependency entirely — no new subdomain, no new DNS records, ever. It also gives Jun full ownership of the news content going forward instead of split ownership across two platforms.

## 1. Current state (audited 2026-08-04)

| Item | Status |
|---|---|
| Main site | Live, static HTML, GitHub Pages, repo `oscarjr-oes/pssarmiento-site`, public, branch `main` |
| DNS | Apex + `www` → GitHub Pages (working). `news` → `pointing.wixdns.net` (connected but not resolving/serving). Nameservers on Wix, **not Jun's account**. |
| Wix Blog | Exists, has real posts, **owned/managed by someone else**, not currently reachable at `news.pssarmiento.com` |
| `news.html` in repo | Client-side redirect stub pointing to `https://news.pssarmiento.com` — will need to change |
| Known Wix post inventory | 8 real blog posts recovered from an old design-reference file (`_archive/psgroup-site-2026-07-25/News.dc.html`) — titles, dates, categories, one-line summaries, and Wix-hosted cover images are known. **Full post body text is not captured anywhere in local files** — only card/teaser copy. |

### Known posts (teaser-level only, from archived reference file)

| Date | Category | Title | Old Wix slug |
|---|---|---|---|
| May 19 | Foundation | Garage Sale for a Cause: turning preloved items into brighter futures | `/post/garage-sale-for-a-cause-turning-preloved-items-into-brighter-futures` |
| Feb 12 | Foundation | PS Group meeting with Cotabato State University heads | `/post/ps-group-meeting-with-cotabato-state-university-heads` |
| Feb 9 | Projects | MOU Signing: FLP and MHSD | `/post/mou-signing-flp-and-mhsd` |
| Jul 11, 2023 | Projects | New bamboo treatment facility in Maguindanao to support Mindanao sustainable housing effort | `/post/new-bamboo-treatment-facility-in-maguindanao-to-support-mindanao-sustainable-housing-effort` |
| Apr 28, 2023 | Newsletter | New HQ: soon to rise | `/post/new-hq-soon-to-rise` |
| Apr 28, 2023 | Projects | Other Mindanao updates | `/post/other-mindanao-updates` |
| Apr 28, 2023 | Projects | University Square | `/post/university-square` |
| Apr 28, 2023 | Newsletter | Other projects | `/post/other-projects` |

*("Introducing, Primosa Foundation" was a card linking to the internal Primosa page, not a real Wix blog post — excluded.)*

## 2. Blocking dependency — this cannot be scraped blind

Full post bodies (not just the teaser text above) live only inside the Wix editor/CMS. `news.pssarmiento.com` currently returns an empty page (DNS points at Wix but nothing serves), and no working public Wix preview URL (e.g. `xxxxx.wixsite.com/...`) is recorded anywhere in local files. **Before any content migration can start, Jun needs one of the following from whoever manages the Wix site:**

1. **Preferred:** Temporary read-only ("Viewer" or "Contributor") access to the Wix dashboard, so posts can be copied out directly (full text, all images at full resolution, correct dates/categories) — cleanest and fastest.
2. **Fallback:** The live/preview Wix URL (even the default `*.wixsite.com` one, if `news.pssarmiento.com` never finished connecting) so pages can be fetched and the rendered text extracted. This recovers visible content but not things like alt text, SEO metadata, or unpublished drafts.
3. **Fallback:** Ask them to manually export/copy each post's text into a shared doc. Lowest tech lift for them, highest manual effort on both sides.

Without one of these, migration can only carry forward the 8 teaser summaries above — not full articles. **This is the one step in this plan that only a human can unblock.**

## 3. Target architecture

- News lives at `pssarmiento.com/news/` — a Jekyll `_posts` collection inside the existing repo, built automatically by GitHub Pages on every push. No new subdomain, no new DNS.
- **Decap CMS** provides the non-technical editing UI at `pssarmiento.com/admin/` — a form (title, date, category, cover image, body) instead of git/code. Publishing a post = filling the form and clicking "Publish"; Decap commits a new Markdown file to the repo.
- Editing access is scoped to a **single restricted GitHub collaborator** (see Section 5) so the news editor can't touch the rest of the site.
- Existing `news.html` redirect stub is replaced with the real `/news/index.html` listing page (styled per the existing brand tokens: green `#0B6B28`/`#1A4D20`/`#0B3D18`, gold `#C8A878`, parchment `#F5ECD8`/cream `#FBF4EB`, Figtree + Newsreader — same tokens already used sitewide, documented in the archived `WIX-BUILD-GUIDE.md`).
- Old Wix post URLs get simple redirect pages (or a redirects table) pointing to their new `/news/...` equivalents, to preserve any existing inbound/shared links and SEO value.

## 4. Phased plan

**Phase 1 — Repo scaffolding (no blockers, can start immediately)**
Add Jekyll config (`_config.yml`), a `_posts` collection, and a `/news/` listing template matching the current site's nav/footer/design tokens. Replace `news.html`'s redirect with the new listing page. Keep all 13 existing pages untouched.

**Phase 2 — Decap CMS install (no blockers)**
Add `/admin/index.html` + `/admin/config.yml` pointing Decap at the `_posts` collection (fields: title, date, category, cover image, summary, body). Configure GitHub backend with **Editorial Workflow** enabled (see Section 5) so every post goes through a draft to review to publish flow instead of publishing straight to the live site.

**Phase 3 — Access setup (needs Jun's decision, no external dependency)**
Create/invite the news editor's GitHub account as a repo collaborator, add branch protection on `main` requiring review before merge. Editor gets a login at `/admin/`, never touches git or code directly.

**Phase 4 — Content migration (BLOCKED on Section 2 — needs Wix access or URL)**
Recreate all real Wix posts as Markdown files with correct dates/categories, download and re-host images locally in `/assets/news/` (stop depending on `static.wixstatic.com` long-term). Rebuild the 8 known posts at minimum; add any older/additional posts once full access is available.

**Phase 5 — Redirects & cleanup**
Add redirect stubs for old `/post/...` slugs to new `/news/...` slugs. Retire the Wix News plan once this is live. Removing the `news.pssarmiento.com` DNS record is optional and **not required** — it can simply be left pointing nowhere, or Jun can ask the DNS admin to delete it as housekeeping once convenient (not a blocker to launch).

**Phase 6 — QA & docs update**
Mobile pass, broken-link check, verify `/admin/` login works end-to-end for the restricted editor account, confirm old links redirect. Update `docs/HANDOFF.md` and mark `docs/WIX-NEWS-PROMPT.md` as superseded (done as part of this pass — see Section 8).

## 5. Restricted access for the news/blog editor

Recommended approach — lowest effort, fully supported by GitHub's free tier, no second repo needed:

1. Add the editor as a **Collaborator** on `oscarjr-oes/pssarmiento-site` (GitHub -> repo Settings -> Collaborators).
2. Turn on **branch protection** on `main`: require a pull request before merging, no direct pushes even for collaborators.
3. Configure Decap CMS's **Editorial Workflow** (`publish_mode: editorial_workflow` in `config.yml`). Every post the editor writes becomes a Draft -> moves to Review -> Jun clicks "Publish," which is really just merging the pull request Decap opened.

Net effect: the editor can only ever propose changes (technically they could edit any file through the PR, but nothing reaches the live site without Jun's approval, and the diff view makes any out-of-scope edit obvious before merging). This is trust-plus-review, not a hard technical wall — but it's the standard, low-maintenance way small teams do this.

**If true isolation is required** (editor should be structurally unable to touch anything but news content, even in a PR), the stronger option is to split news into its **own small repo** (e.g. `pssarmiento-news`) that the editor has full write access to, with a GitHub Actions workflow that syncs its content into the main site repo on every publish. This fully firewalls the main site from the editor's account, at the cost of one extra repo and a small sync workflow to build and maintain. Recommend only if the editor is not fully trusted, or if the review-based approach above proves insufficient in practice — for a family business this is likely overkill to start.

## 6. Effort & model recommendation for building this

| Phase | Nature of work | Suggested model | Effort |
|---|---|---|---|
| 1-2 (scaffolding + Decap install) | Mechanical config/templating, matches existing patterns in repo | Claude Sonnet 5 | Low-medium |
| 3 (access/branch protection) | GitHub settings, no code | Claude Sonnet 5 | Low |
| 4 (content migration) | Content transcription/formatting once source text is available; judgment on formatting fidelity | Claude Sonnet 5 (Opus only if post bodies are long/complex and need heavier editorial judgment) | Medium (mostly gated by how the Wix content is obtained, not by model capability) |
| 5-6 (redirects, QA, docs) | Mechanical, verification-heavy | Claude Sonnet 5 | Low |

Nothing in this project needs Opus-level reasoning — it's config, templating, and content transcription against an already-documented design system. Sonnet 5 is the right default throughout; only reach for Opus if post content turns out to need substantial rewriting/judgment calls.

## 7. Claude Code vs. Cowork for execution

**Recommendation: Claude Code**, for this specific build phase.

- This work is almost entirely repo/file/git operations (config files, Jekyll templates, Decap config, GitHub settings) — exactly Claude Code's home turf, with direct file/git access and no chat-turn overhead per edit.
- **Token economics right now favor Code over Cowork specifically:** as of this writing, Claude Code has a 50% higher weekly usage limit running through **August 19, 2026**, automatically applied, across CLI/IDE/desktop/web — no setup needed. Cowork's own promo (a doubled 5-hour session limit) only runs through **August 5, 2026** — i.e., it's expiring essentially immediately — and only affects the short session window, not the weekly budget that a multi-day migration like this will actually consume. For a project spanning several sessions (scaffolding, access setup, content migration, QA), Code's longer-running, broader promo is the better fit.
- Cowork (this environment) remains the better choice for anything involving talking through content/design decisions, reading local business files (like this session did to reconstruct the post inventory), or coordinating with non-technical people — but the actual implementation is better run in Code.

## 8. Plan-document updates made in this pass

- This file (`NEWS-MIGRATION-PLAN.md`) is the new source of truth for the News/Blog work.
- `docs/WIX-NEWS-PROMPT.md` status changed from `OPEN` to `SUPERSEDED`, pointing here.
- `docs/HANDOFF.md` "Remaining TODOs" row for the Wix News subdomain updated to point here instead.
- No files were deleted; Wix plan docs are kept for history.

## 9. Immediate next step

**Jun:** request temporary Wix viewer/contributor access (or just the live Wix preview URL) from whoever manages the Wix Blog — that's the only step blocking Phase 4, and the sooner it's requested, the less this migration is gated on someone else's schedule. Everything else (Phases 1-3, 5-6) can start in parallel without waiting on that.
