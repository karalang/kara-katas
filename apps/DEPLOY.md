# Deploying Prism & Veil to karac.dev

Both apps are **fully static** — no backend, no build step on the host. Each
`deploy/` directory is the complete site:

| App | Bundle | Size | Suggested home |
|---|---|---|---|
| Prism | `apps/prism/deploy/` (`index.html`, `prism.js`, `prism.wasm`, `prism.threads.wasm`, `_headers`) | ~360 KB | `prism.karac.dev` |
| Veil  | `apps/veil/deploy/` (`index.html`, `veil.js`, `veil.wasm`) | ~148 KB | `veil.karac.dev` |

Subdomains keep the root `karac.dev` free for the language homepage, and let
Prism's cross-origin-isolation headers apply only where they're wanted.

## The one header rule (Prism only)

Prism's multicore build needs **cross-origin isolation** (SharedArrayBuffer):

```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

`prism/deploy/_headers` already declares this in the format Cloudflare Pages
and Netlify both read natively. **Without the headers the app still works** —
the glue detects the missing isolation and falls back to the single-threaded
module automatically (the meta line shows "1 thread" instead of "threads").
Veil is single-threaded by design and needs no headers.

## Cloudflare Pages (recommended)

Per app (5 minutes each):

1. Cloudflare dashboard → **Workers & Pages → Create → Pages →
   Upload assets** ("direct upload"). Name the project (`prism` / `veil`).
2. Drag the contents of the app's `deploy/` directory in and deploy.
   (`_headers` is picked up automatically.)
3. Project → **Custom domains → Set up a custom domain** →
   `prism.karac.dev` (resp. `veil.karac.dev`). If karac.dev's DNS is on
   Cloudflare this is one click; otherwise add the CNAME it shows you
   (`prism.karac.dev → <project>.pages.dev`). TLS is automatic.

Redeploys: re-run the app's `./build.sh`, re-copy into `deploy/`
(or just upload the app dir's fresh artifacts), drag-and-drop again — or wire
`wrangler pages deploy deploy/` into CI later.

## Alternatives

- **Netlify**: drag `deploy/` onto app.netlify.com/drop; `_headers` works
  as-is; add the custom domain in Site settings.
- **Vercel**: works, but move the header rule into `vercel.json`
  (`headers` key) — Vercel ignores `_headers`.
- **GitHub Pages**: hosts the files fine but **cannot set response headers**,
  so Prism runs in single-threaded fallback there. Fine for Veil.

## Post-deploy verification (2 minutes)

On the live `prism.karac.dev`:

1. DevTools console: `crossOriginIsolated` → must print `true`
   (if `false`, the headers aren't being served).
2. Drop a photo, click a resize — the meta line should read
   `… ms (Kāra/WASM, threads)`.
3. The privacy claim, live: keep the **Network tab** open while editing —
   after the initial page load, zero requests.

The same checks minus the isolation bits apply to Veil.

## Provenance

Bundles are built by each app's `./build.sh` (requires the kara-tree `karac`
with `--features llvm` and `wasm-tools` on PATH for the ~10× debug-info
strip) and verified before shipping by `test_node.mjs` (exact-oracle kernel
tests) plus `verify_browser.mjs` (real-Chrome CDP drive of the actual page —
for Prism: both the sequential-fallback and threaded legs).
