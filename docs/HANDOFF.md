# pssarmiento.com Hybrid Publishing Handoff

**Status:** GitHub Pages deployment complete; Wix News subdomain remains open.

**Execution stamp**

- Executed by: OpenAI Codex, GPT-5-based agent
- Date: 2026-07-24 (Asia/Manila)
- Deployment effort: Low–medium; mechanical configuration and verification
- Design/content edits: Not performed during deployment

## Architecture

- GitHub Pages serves the non-changing site at `https://pssarmiento.com`.
- Wix remains the intended host for News/Blog at `https://news.pssarmiento.com`.
- Repository: `oscarjr-oes/pssarmiento-site`
- Branch: `main`
- Repository visibility: Public
- Custom-domain file: `CNAME` containing `pssarmiento.com`

## Completed

| Item | Status | Evidence | Effort |
|---|---|---|---|
| Create repository and publish site contents at repository root | **DONE** | Public repo; `main` deployed | Low |
| Configure GitHub Pages from `main` / root | **DONE** | GitHub Pages deployment serving content | Low |
| Configure apex DNS | **DONE** | `pssarmiento.com` resolves to all four GitHub Pages A records | Low |
| Configure `www` DNS | **DONE** | `www.pssarmiento.com` CNAME → `oscarjr-oes.github.io` | Low |
| HTTPS certificate and serving | **DONE** | `https://pssarmiento.com` returns HTTP 200 with valid HTTPS | Low |
| Replace GA4 placeholder | **DONE** | `G-ECYJ5Z8FSW` deployed in all 12 instrumented HTML pages; zero placeholders remain | Low |
| Replace Formspree placeholder | **DONE** | `https://formspree.io/f/mdaqwdre` deployed in `contact.html` | Low |
| Contact-form delivery | **DONE** | Synthetic submission accepted; notification received at `admin@pssarmiento.com` | Low |
| Page smoke test | **DONE** | All 13 HTML pages return HTTP 200 | Low |
| Banwag 3D asset availability | **DONE** | `banwag-web.ply` returns HTTP 200 | Low |
| Preserve News links | **SUPERSEDED** | Nav/footer `News` link on all 13 pages now points to `/news/` (was `https://news.pssarmiento.com`) — see News/Blog migration below | Low |
| News/Blog migration off Wix (Phases 1, 2, 4, 5) | **DONE** — see `docs/NEWS-MIGRATION-PLAN.md` (2026-08-04) | `/news/` Jekyll listing + `_posts` collection live on branch `news-migration`; all 13 Wix posts migrated to Markdown; `/admin/` Decap CMS installed (Editorial Workflow); 8 of 13 old Wix `/post/...` slugs redirect to their `/news/...` equivalents (see gaps below) | Medium |

## News migration — open items (branch `news-migration`, not yet merged)

| Item | Owner/action | Effort |
|---|---|---|
| GitHub OAuth provider for Decap CMS | `/admin/config.yml` uses the Netlify OAuth-proxy pattern (`base_url: https://api.netlify.com`) for the `github` backend. Jun needs to register a GitHub OAuth App and enable it on a (can be auth-only) Netlify site under Site settings → Access control → OAuth, then confirm the client ID/secret are wired up. Without this the `/admin/` login flow will not work. | Medium |
| Phase 3 — restricted access | Branch protection on `main` is now ON (PR required + 1 approval, no force-pushes/deletions; `enforce_admins: false` so the repo owner can still bypass in an emergency). Still needed: Jun to confirm the news editor's GitHub username before inviting as a collaborator. | Low |
| 5 posts missing old Wix slugs for redirects | Resolved. Pulled the real published URLs from the live Wix dashboard's "View post" action for Grand Opening (FSPHI office), Introducing Primosa Foundation, One Pablo - Option 2, Letter from the Chairman, and University Square Project Lifts Off. All 13 posts now have a working `/post/<old-slug>/` → `/news/<new-slug>/` redirect, verified locally. | — |
| 3 of 13 posts have no cover/gallery images | All 13 Wix posts were re-audited directly in each post's editor (not just list-view thumbnails), including expanding a collapsed "Gallery" accordion block in the MOU Signing post that had been hiding 16 images. 10 posts now have a `cover` and/or `gallery` field pulling real re-hosted images from Wix under `/assets/news/`. Confirmed via direct inspection that Other Projects, Letter from the Chairman, and University Square Project Lifts Off genuinely have zero images in Wix — nothing missing, nothing to add. | Low |
| 5 article-specific deep-links still point to Wix | `index.html` (3 story cards) and `projects.html` (2 CTA links) link directly to `https://news.pssarmiento.com` for specific articles, not through the generic nav/footer "News" link — left untouched as it was outside the approved edit scope for this pass (only the nav/footer `News` link was authorized to change). Worth a follow-up pass once Jun confirms. | Low |
| Local Jekyll build verified | System Ruby (2.6.10) was too old for a modern Jekyll toolchain (needs Ruby ≥ 3.0); installed Ruby 4.0.6 via Homebrew plus Jekyll 4.4.1 and ran `jekyll serve` locally against the branch. Confirmed the `/news/` listing and individual post pages (incl. galleries) render without errors. Still worth checking GitHub Pages' own build log after merging, since Pages uses its own Jekyll/Ruby version. | Low |

## Remaining TODOs (pre-existing, unrelated to News)

| Item | Owner/action | Effort |
|---|---|---|
| Hide non-News Wix pages | Wix administrator keeps the existing Blog/CMS and hides/removes duplicate non-News pages | Medium |
| Confirm GA4 Realtime | Open GA4 Realtime after visiting the live site; tag deployment is complete, but Realtime access was not available to Codex | Low |
| Homepage Banwag image crop | Adjust framing so the face is not cropped | Low–medium |
| Banwag award badge formatting | Improve `GOOD DESIGN AWARD PH 2026` line breaks/typography | Low |
| Banwag CTA placement | Move `Visit Banwag` below the paragraph so it does not overlap text | Low |
| Portal authentication | **PARTIAL** — `portal.html` now links Team and Executive users to the Cloudflare Access-protected Pages deployments. Custom `os.` / `exec.` hostnames still require DNS-owner changes; the `pages.dev` links are the working interim route. | Low |

`graphify-out/` is local generated analysis output and was not included in the website deployment.
