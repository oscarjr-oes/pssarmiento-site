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
| Preserve News links | **DONE** | Site links target `https://news.pssarmiento.com` | Low |

## Remaining TODOs

| Item | Owner/action | Effort |
|---|---|---|
| Configure `news.pssarmiento.com` in Wix and DNS | Wix administrator connects the subdomain and adds Wix's supplied `news` CNAME target | Medium |
| Hide non-News Wix pages | Wix administrator keeps the existing Blog/CMS and hides/removes duplicate non-News pages | Medium |
| Confirm GA4 Realtime | Open GA4 Realtime after visiting the live site; tag deployment is complete, but Realtime access was not available to Codex | Low |
| Homepage Banwag image crop | Adjust framing so the face is not cropped | Low–medium |
| Banwag award badge formatting | Improve `GOOD DESIGN AWARD PH 2026` line breaks/typography | Low |
| Banwag CTA placement | Move `Visit Banwag` below the paragraph so it does not overlap text | Low |
| Portal authentication | Add an identity provider; recommended next investigation is Firebase Auth or Cloudflare Access | Medium |

`graphify-out/` is local generated analysis output and was not included in the website deployment.

