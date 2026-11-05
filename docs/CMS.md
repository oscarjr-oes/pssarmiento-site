# Decap CMS (`/admin`) — can login work on GitHub Pages?

_Audit of `admin/config.yml` and `admin/index.html`. No auth settings were changed, and no secrets belong in this repo._

## Short answer

**Not by itself.** GitHub Pages only serves static files, and Decap's `github` backend needs a server-side
component to exchange GitHub's OAuth `code` for an access token (this step needs the OAuth app's *client secret*,
which can't live in browser code). The static `/admin/` page can load, but **login will fail unless a working OAuth
proxy is reachable at the URL the config points to.**

## What the config says today

```yaml
backend:
  name: github
  repo: oscarjr-oes/pssarmiento-site
  branch: main
  base_url: https://astounding-torrone-689f38.netlify.app
  auth_endpoint: auth
```

When an editor clicks "Login with GitHub", Decap opens a popup to
`https://astounding-torrone-689f38.netlify.app/auth?provider=github&site_id=…&scope=…`. That Netlify site must answer
there with a GitHub OAuth redirect, and later handle `/callback`, then post the token back to the CMS window.

Findings:

1. **Unverified / likely incomplete.** A plain Netlify site (even with Site settings → Access control → OAuth enabled)
   does *not* serve `/auth` or `/callback`. Netlify's built-in OAuth handler lives on `api.netlify.com`, and Decap only uses
   it when `base_url` is `https://api.netlify.com` (the earlier config; see `docs/HANDOFF.md`). The current
   `base_url` + `auth_endpoint: auth` combination is the **self-hosted OAuth proxy** pattern, so
   that Netlify site must actually be running an OAuth proxy (function/app) exposing `/auth` and `/callback`.
   This audit environment has no outbound access to that site, so whether it does could not be tested. Check it
   (see "How to test").
2. **Netlify's built-in OAuth also has a limit:** it requires `site_id` to be a domain registered as a custom domain on
   that Netlify site, which is not the case for a site hosted on GitHub Pages at `pssarmiento.com`.
3. **GitHub OAuth App** (not a GitHub App) must exist, with its **Authorization callback URL** set to the proxy's
   `/callback` (e.g. `https://<proxy-host>/callback`). Its client ID/secret live **only** in the proxy's environment
   variables.
4. **Scope:** for a public repo the proxy should request `public_repo` (or `repo` for a private one). Commits
   are made as the logged-in GitHub user, so each editor needs a GitHub account with **write access** to the repo.
5. **Editorial workflow + branch protection.** `publish_mode: editorial_workflow` opens a pull request per draft.
   `main` is protected (PR + 1 approval per `docs/HANDOFF.md`), so "Publish" in the CMS merges only if the
   editor can satisfy that rule; otherwise the PR waits for a reviewer. This is expected, but editors should know.
6. **`admin/index.html` loads `decap-cms@^3.0.0` from unpkg.** A floating range means an upstream release can change
   behaviour without a commit here. Pin an exact version (e.g. `decap-cms@3.x.y`) after testing.
7. **Config files are fine otherwise:** `media_folder: assets/news` / `public_folder: /assets/news` match the existing images,
   and the collection `folder: _posts` with the `{{year}}-{{month}}-{{day}}-{{slug}}` filename pattern matches
   Jekyll's post naming. `/admin/` is `noindex`, disallowed in `robots.txt` and excluded from the sitemap.

## What is needed to make login work

Pick one:

**A. Self-host a small OAuth proxy (matches the current config).**
Deploy an open-source Decap/Netlify-CMS OAuth provider (e.g. `netlify-cms-oauth-provider-node`, or a Cloudflare Worker /
Netlify Function equivalent) to the Netlify site named in `base_url`, then:

1. Create a GitHub OAuth App (GitHub → Settings → Developer settings → OAuth Apps). Homepage URL
   `https://pssarmiento.com`; callback URL `https://<proxy-host>/callback`.
2. Put the client ID and client secret in the proxy host's **environment variables** (never in this repo).
3. Set the proxy's allowed origin to `https://pssarmiento.com` and its scope to `public_repo`.
4. Keep `base_url` / `auth_endpoint` in `admin/config.yml` pointing at that proxy (`auth_endpoint` is the path of its
   auth route).

**B. Host the site (or only `/admin`) on Netlify** and use Netlify's built-in GitHub OAuth (`base_url: https://api.netlify.com`).
This is only practical if the site moves off GitHub Pages.

**C. No CMS login at all.** Editors can create posts by adding a Markdown file to `_posts/` through the GitHub web UI
(see `docs/NEWS-POSTING.md`); no proxy is needed.

## How to test

1. Open `https://pssarmiento.com/admin/` → "Login with GitHub".
2. In the browser dev tools Network tab, the popup should land on GitHub's authorize page, not a 404 from the
   proxy host. A 404 at `<base_url>/auth` confirms the proxy is missing.
3. After approving, the popup closes and the CMS shows the "News Posts" collection.
4. Create a draft; confirm a pull request opens against `main`.

## Do not

- Commit OAuth client secrets, tokens, or `.env` files — this repository is public.
- Weaken branch protection to make the CMS publish work.
