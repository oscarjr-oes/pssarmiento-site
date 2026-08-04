# Wix News Subdomain — Remaining Execution Prompt

**Status:** SUPERSEDED — see `docs/NEWS-MIGRATION-PLAN.md` (2026-08-04). News/Blog is moving to GitHub Pages + Decap CMS instead of Wix, since neither Wix nor DNS are managed by Jun. This file kept for history.

**AI handoff stamp:** OpenAI Codex, GPT-5-based agent · 2026-07-24 · Medium effort expected.

The root site is now live on GitHub Pages. Continue only on the Wix News side; do not rebuild the GitHub Pages site.

1. In Wix, retain the existing Blog/CMS and its real posts.
2. Hide or remove duplicate non-News pages from the Wix site menu/pages panel.
3. Keep the News/Blog page as the only public Wix content destination.
4. Connect `news.pssarmiento.com` in Wix → Settings → Domains.
5. Add the exact CNAME target Wix supplies for the `news` host in the active DNS editor. Do not alter the working apex A records or `www` CNAME used by GitHub Pages.
6. Add a simple `← PS Group of Companies` link to `https://pssarmiento.com`.
7. Restyle only the News shell as practical: green `#0B6B28`, dark green `#1A4D20`, deep green `#0B3D18`, gold `#C8A878`, parchment/cream background, Figtree body text, and Newsreader display text.
8. Verify Wix's native Blog category filtering and confirm that the subdomain resolves to the Blog.
9. Do not publish email addresses in Wix content, alt text, or metadata.

## Completion report required

- Pages hidden vs. deleted
- `news.pssarmiento.com` DNS and serving status
- Blog/category filtering status
- Any styling mismatch or unresolved Wix limitation

