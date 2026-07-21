# Deploying Prism & Veil (karac.dev)

**Single source of truth, one-directional flow:**

| What | Where | Repo |
|---|---|---|
| App **source + tests** (`.kara`, `index.html`, node oracles, CDP harnesses, `build.sh`) | `apps/prism/`, `apps/veil/` | **kara-katas** (this repo — build artifacts are gitignored) |
| **Deployed artifacts** (html + js glue + wasm) | `public/prism/`, `public/veil/` | **karalang/website** — served verbatim at `karac.dev/prism` and `karac.dev/veil` by GitHub Pages on every push to `main` |

Nothing is committed twice: this repo holds no built bundles, the website repo
holds no app source.

## Redeploy flow

```bash
# 1. build + verify here (node oracles + three-leg headless-Chrome CDP)
( cd prism && ./build.sh --verify )
( cd veil  && ./build.sh --verify )

# 2. copy artifacts into a website checkout (the only direction they flow)
./sync-website.sh /path/to/website

# 3. push the website repo — GitHub Pages redeploys karac.dev automatically
cd /path/to/website && git add public && git commit -m "Update Prism/Veil artifacts" && git push
```

Building needs the kara-tree `karac` (`--features llvm`) and `wasm-tools` on
PATH (the ~10× debug-info strip); see each app's README.

## Threads without response headers (how karac.dev/prism gets multicore)

Prism's multicore build needs **cross-origin isolation** (SharedArrayBuffer),
which normally requires two response headers:

```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

GitHub Pages **cannot set response headers**, so Prism ships the vendored
**coi-serviceworker** shim (MIT, gzuidhof/coi-serviceworker v0.1.7 —
`prism/coi-serviceworker.min.js`): on a headers-blind host it registers a
service worker that injects COOP/COEP client-side and reloads once; after
that first-visit reload, `crossOriginIsolated` is true and the threaded
module (`prism.threads.wasm`) loads. On a host that already sends the
headers, the shim is a no-op. Appending `?seq` to the URL skips it and pins
the single-threaded fallback. Veil is single-threaded by design and needs
none of this.

If you ever host on a headers-capable platform (Cloudflare Pages / Netlify),
you can serve the headers directly with a `_headers` file:

```
/prism/*
  Cross-Origin-Opener-Policy: same-origin
  Cross-Origin-Embedder-Policy: require-corp
```

## Post-deploy verification (2 minutes)

On the live `karac.dev/prism`:

1. First visit may reload once (the shim installing); DevTools console then
   shows `COOP/COEP Service Worker registered`.
2. Console: `crossOriginIsolated` → must print `true`.
3. Drop a photo, click a resize — the meta line should read
   `… ms (Kāra/WASM, threads)`.
4. The privacy claim, live: keep the **Network tab** open while editing —
   after the initial page load, zero requests.

The same checks minus the isolation bits apply to `karac.dev/veil`.

## Provenance

Artifacts are built by each app's `./build.sh` and verified before shipping
by `test_node.mjs` (exact-oracle kernel tests) plus `verify_browser.mjs`
(real-Chrome CDP drive of the actual page — for Prism: the `?seq`
sequential-fallback leg, the real-COOP/COEP threaded leg, AND the coi-shim
leg that simulates GitHub Pages: headerless server → SW-injected isolation →
threaded module + pixel oracle).
