// verify_browser.mjs — drive the real page in a real browser.
//
// test_node.mjs proves the wasm kernels match native. This proves the PAGE
// does: it loads index.html in headless Chromium, feeds it the demo FITS subs
// through the same code path the file picker uses, runs the stack, and compares
// the pixels the page holds against what the native binary produced from the
// same files.
//
// The gap this closes is the JS FITS decoder. The page parses FITS headers in
// JavaScript while the CLI parses them in Kāra — two implementations of the
// same spec, and the BZERO transform is exactly the kind of thing that drifts
// between them (unsigned data in signed 16-bit space; drop it and stars become
// holes). Requiring the page's stack to equal the CLI's stack pins both
// decoders to each other.
//
// Usage: node verify_browser.mjs <native_stack.cstack> [--keep]

import { chromium, devices } from "playwright";
import { existsSync, readFileSync, readdirSync } from "node:fs";
import { createServer } from "node:http";
import { extname, join } from "node:path";

const nativePath = process.argv[2];
if (!nativePath) {
  console.error("usage: node verify_browser.mjs <native_stack.cstack>");
  process.exit(2);
}

const TYPES = {
  ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript",
  ".wasm": "application/wasm", ".fits": "application/octet-stream",
};

const root = process.cwd();
const server = createServer((req, res) => {
  // Chromium always asks for /favicon.ico. Answer it rather than muting 4xx in
  // the error check — a genuine missing asset (a stale .wasm path, a renamed
  // module) must still fail the run.
  if (req.url === "/favicon.ico") { res.writeHead(204).end(); return; }
  const path = join(root, decodeURIComponent(req.url.split("?")[0]).replace(/^\/+/, "") || "index.html");
  try {
    const body = readFileSync(path);
    res.writeHead(200, {
      "content-type": TYPES[extname(path)] ?? "application/octet-stream",
      // Harmless here, and required if this ever moves to the threaded build.
      "cross-origin-opener-policy": "same-origin",
      "cross-origin-embedder-policy": "require-corp",
    });
    res.end(body);
  } catch {
    if (process.env.LOG_404) console.log(`  [404] ${req.url}`);
    res.writeHead(404).end("not found");
  }
});
await new Promise((r) => server.listen(0, r));
const base = `http://127.0.0.1:${server.address().port}`;

function readCstack(path) {
  const buf = readFileSync(path);
  const dv = new DataView(buf.buffer, buf.byteOffset);
  const w = dv.getUint32(4, true), h = dv.getUint32(8, true);
  const px = new Uint16Array(w * h);
  for (let i = 0; i < w * h; i++) px[i] = dv.getUint16(16 + i * 2, true);
  return { w, h, px };
}

const want = readCstack(nativePath);
// The npm playwright package pins a browser build that a preinstalled image may
// not carry (image ships 1194, package wants 1234). Prefer an explicit binary —
// CHROME_PATH, then whatever chromium-* build is actually on disk — and only
// fall back to playwright's own resolution.
function findChrome() {
  if (process.env.CHROME_PATH) return process.env.CHROME_PATH;
  const root = process.env.PLAYWRIGHT_BROWSERS_PATH || "/opt/pw-browsers";
  try {
    for (const d of readdirSync(root).filter((x) => x.startsWith("chromium-")).sort().reverse()) {
      const p = join(root, d, "chrome-linux", "chrome");
      if (existsSync(p)) return p;
    }
  } catch { /* fall through to playwright's own resolution */ }
  return undefined;
}
const exe = findChrome();
if (exe) console.log(`  browser: ${exe}`);
const browser = await chromium.launch({ args: ["--no-sandbox"], executablePath: exe });
let failures = 0;

try {
  const page = await browser.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
  page.on("response", (r) => { if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`); });

  await page.goto(`${base}/index.html`, { waitUntil: "load" });

  const subs = readdirSync("demo").filter((f) => f.endsWith(".fits")).sort();
  if (subs.length < 2) throw new Error("demo/ has fewer than 2 .fits files");

  // Feed the page the same bytes the file picker would hand it.
  await page.evaluate(async (names) => {
    const bufs = await Promise.all(names.map((n) => fetch(`demo/${n}`).then((r) => r.arrayBuffer())));
    await window.__cumulus.loadBuffers(bufs);
  }, subs);

  await page.selectOption("#mode", "2"); // register + sigma clip
  await page.evaluate(() => window.__cumulus.stack());
  await page.waitForFunction(() => window.__cumulus.getResult() !== null, { timeout: 60000 });

  const got = await page.evaluate(() => window.__cumulus.getResult());
  const runPath = await page.evaluate(() => window.__cumulus.getRunPath());
  const status = await page.textContent("#log");

  // The inline fallback produces IDENTICAL pixels, so every other assertion in
  // this file passes whether or not the worker ran. Without this check, a
  // regression that permanently broke the worker — the whole reason the page
  // stays responsive, and the difference between usable and killed on a phone
  // — would ship green.
  // Threads need cross-origin isolation. The glue falls back to the sequential
  // module without error when it is missing — same pixels, 8.3x slower — so
  // nothing downstream would notice. Assert it explicitly.
  const threaded = await page.evaluate(() => window.__cumulus.getThreaded());
  const isolated = await page.evaluate(() => window.__cumulus.isIsolated());
  if (threaded !== true) {
    console.log(`  FAIL: stack ran on the SEQUENTIAL module (crossOriginIsolated=${isolated}) ` +
                `— threads give 8.3x here, and losing them is silent`);
    failures++;
  } else {
    console.log(`  stack ran on the threaded module (crossOriginIsolated=${isolated})`);
  }

  if (runPath !== "worker") {
    console.log(`  FAIL: stack ran via "${runPath}", expected the worker`);
    failures++;
  } else {
    console.log("  stack ran off the main thread (worker)");
  }

  // The page must hold HANDLES, not pixels. Nothing else in this file can see
  // that: a page that decoded every sub up front would produce identical
  // pixels, paint an identical canvas, and pass every other assertion here —
  // while being the exact thing streaming exists to stop, and the thing that
  // gets a tab killed on a phone. So the shape of what is retained is checked
  // directly.
  const held = await page.evaluate(() => window.__cumulus.getHeld());
  const pixelly = held.flatMap((s, i) =>
    Object.entries(s).filter(([, v]) => String(v).startsWith("bytes:")).map(([k, v]) => `sub ${i}.${k}=${v}`));
  if (!held.length) {
    console.log("  FAIL: page reports nothing loaded");
    failures++;
  } else if (pixelly.length) {
    console.log(`  FAIL: page is holding decoded pixels, not handles: ${pixelly.slice(0, 3).join(", ")}`);
    failures++;
  } else {
    const blobs = held.filter((s) => Object.values(s).some((v) => String(v).startsWith("blob:"))).length;
    console.log(`  page holds ${blobs}/${held.length} subs as blob handles, no decoded pixels`);
  }

  if (errors.length) {
    console.log(`  page errors: ${errors.slice(0, 3).join(" | ")}`);
    failures++;
  }
  if (got.w !== want.w || got.h !== want.h) {
    console.log(`  FAIL: page produced ${got.w}x${got.h}, native ${want.w}x${want.h}`);
    failures++;
  } else {
    let diff = 0, firstAt = -1;
    for (let i = 0; i < want.px.length; i++) {
      if (got.px[i] !== want.px[i]) { if (firstAt < 0) firstAt = i; diff++; }
    }
    if (diff === 0) {
      console.log(`  page stack byte-identical to native over ${want.px.length} pixels`);
    } else {
      console.log(`  FAIL: ${diff}/${want.px.length} pixels differ; first at ${firstAt} ` +
                  `page ${got.px[firstAt]} vs native ${want.px[firstAt]}`);
      failures++;
    }
  }

  // The canvas must actually have been painted — an all-black canvas means the
  // stretch or the blit silently failed, and the pixel comparison above would
  // still pass because it reads the data, not the display.
  const painted = await page.evaluate(() => {
    const cv = document.getElementById("view");
    const d = cv.getContext("2d").getImageData(0, 0, cv.width, cv.height).data;
    let min = 255, max = 0;
    for (let i = 0; i < d.length; i += 4) { if (d[i] < min) min = d[i]; if (d[i] > max) max = d[i]; }
    return { min, max };
  });
  if (painted.max - painted.min < 32) {
    console.log(`  FAIL: canvas is flat (min ${painted.min}, max ${painted.max}) — nothing rendered`);
    failures++;
  } else {
    console.log(`  canvas painted, luminance range ${painted.min}..${painted.max}`);
  }

  console.log(`  status line: ${status.trim().replace(/\s+/g, " ")}`);
  if (process.argv.includes("--shot")) {
    await page.screenshot({ path: "browser-shot.png", fullPage: true });
    console.log("  wrote browser-shot.png");
  }

  // A colour mosaic stacked as if it were grey does not fail — it produces a
  // plausible picture with checkerboard texture and colour-biased star
  // positions. The CLI refuses that combination (verify.sh checks it); until
  // this slice the page silently accepted it, because its JS reader never
  // looked at BAYERPAT. Synthesise the smallest file that reproduces it rather
  // than shipping a mosaic into demo/.
  const refusal = await page.evaluate(async () => {
    const CARD = 80, BLOCK = 2880;
    const card = (k, v) => (`${k.padEnd(8)}= ${String(v).padStart(20)}`).padEnd(CARD);
    const hdr = [card("SIMPLE", "T"), card("BITPIX", 16), card("NAXIS", 2),
                 card("NAXIS1", 4), card("NAXIS2", 4), card("BAYERPAT", "'RGGB    '"),
                 "END".padEnd(CARD)].join("");
    const bytes = new Uint8Array(BLOCK * 2);
    for (let i = 0; i < hdr.length; i++) bytes[i] = hdr.charCodeAt(i);
    for (let i = hdr.length; i < BLOCK; i++) bytes[i] = 32;
    await window.__cumulus.loadBuffers([bytes.buffer, bytes.buffer.slice(0)]);
    return { held: window.__cumulus.getHeld().length, log: window.__cumulus.loadProblems() };
  });
  if (refusal.held !== 0 || !/Bayer mosaic/.test(refusal.log)) {
    console.log(`  FAIL: page accepted a Bayer mosaic (${refusal.held} loaded): ` +
                `${refusal.log.replace(/\s+/g, " ").slice(0, 120)}`);
    failures++;
  } else {
    console.log("  Bayer mosaic refused by the page, as the CLI refuses it");
  }

  // ── the inline fallback ───────────────────────────────────────────────────
  // The fallback exists for a page opened over file://, where a module worker
  // cannot load. That case never occurs in this harness, so the fallback is
  // code no test reaches — exactly the shape of a path that quietly rots and
  // then fails the one time it is needed. Denying the page a Worker
  // constructor reproduces the failure the fallback is FOR, and the same
  // byte-identity bar applies: degraded should mean slower, not different.
  const ctx2 = await browser.newContext();
  await ctx2.addInitScript(() => {
    window.Worker = function () { throw new Error("Worker disabled for the fallback check"); };
  });
  const page2 = await ctx2.newPage();
  const errors2 = [];
  page2.on("pageerror", (e) => errors2.push(String(e)));
  await page2.goto(`${base}/index.html`, { waitUntil: "load" });
  await page2.evaluate(async (names) => {
    const bufs = await Promise.all(names.map((n) => fetch(`demo/${n}`).then((r) => r.arrayBuffer())));
    await window.__cumulus.loadBuffers(bufs);
  }, subs);
  await page2.selectOption("#mode", "2");
  await page2.evaluate(() => window.__cumulus.stack());
  await page2.waitForFunction(() => window.__cumulus.getResult() !== null, { timeout: 60000 });

  const path2 = await page2.evaluate(() => window.__cumulus.getRunPath());
  const got2 = await page2.evaluate(() => window.__cumulus.getResult());
  let diff2 = 0;
  for (let i = 0; i < want.px.length; i++) if (got2.px[i] !== want.px[i]) diff2++;

  if (path2 !== "inline") {
    console.log(`  FAIL: with Worker denied the run took the "${path2}" path, expected "inline"`);
    failures++;
  } else if (diff2 !== 0) {
    console.log(`  FAIL: inline fallback differs from native in ${diff2}/${want.px.length} pixels`);
    failures++;
  } else if (errors2.length) {
    console.log(`  FAIL: inline fallback raised: ${errors2.slice(0, 2).join(" | ")}`);
    failures++;
  } else {
    console.log("  Worker denied -> inline fallback ran, still byte-identical to native");
  }
  await ctx2.close();

  // ── mobile viewports ──────────────────────────────────────────────────────
  // Emulation gives real layout, touch and DOM at a phone's viewport — it does
  // NOT give WebKit's engine or a device's memory ceiling, so this can show the
  // page is broken on a phone and never that it is good. What it does cover is
  // the class of failure that is invisible at desktop width: a page that
  // scrolls sideways, a canvas wider than the screen, a tap target too small to
  // hit. The README makes claims about these; this is what backs them.
  for (const name of ["iPhone 13", "Pixel 5"]) {
    const mctx = await browser.newContext({ ...devices[name] });
    const mpage = await mctx.newPage();
    const merrors = [];
    mpage.on("pageerror", (e) => merrors.push(String(e)));
    await mpage.goto(`${base}/index.html`, { waitUntil: "load" });
    await mpage.evaluate(async (names) => {
      const bufs = await Promise.all(names.map((n) => fetch(`demo/${n}`).then((r) => r.arrayBuffer())));
      await window.__cumulus.loadBuffers(bufs);
    }, subs);
    await mpage.evaluate(() => window.__cumulus.stack());
    await mpage.waitForFunction(() => window.__cumulus.getResult() !== null, { timeout: 60000 });

    const vp = mpage.viewportSize();
    const overflow = await mpage.evaluate(() =>
      document.documentElement.scrollWidth - document.documentElement.clientWidth);
    const drop = await mpage.locator("#drop").boundingBox();
    const canvas = await mpage.locator("#view").boundingBox();
    const lum = await mpage.evaluate(() => {
      const cv = document.getElementById("view");
      const d = cv.getContext("2d").getImageData(0, 0, cv.width, cv.height).data;
      let min = 255, max = 0;
      for (let i = 0; i < d.length; i += 4) { if (d[i] < min) min = d[i]; if (d[i] > max) max = d[i]; }
      return max - min;
    });

    const bad = [];
    if (overflow > 1) bad.push(`page scrolls sideways by ${overflow}px`);
    // 44px is the smallest reliably tappable target on a touch screen.
    if (!drop || drop.width < 44 || drop.height < 44) bad.push("file picker target under 44px");
    if (canvas && canvas.width > vp.width + 1) bad.push(`canvas ${Math.round(canvas.width)}px wider than viewport`);
    if (lum < 32) bad.push("canvas flat — nothing rendered");
    if (merrors.length) bad.push(`errors: ${merrors.slice(0, 2).join(" | ")}`);

    if (bad.length) {
      console.log(`  FAIL ${name} (${vp.width}x${vp.height}): ${bad.join("; ")}`);
      failures++;
    } else {
      console.log(`  ${name} ${vp.width}x${vp.height}: no overflow, canvas ` +
                  `${Math.round(canvas.width)}px, stacked and painted`);
    }
    await mctx.close();
  }
} finally {
  await browser.close();
  server.close();
}

console.log(failures === 0 ? "PASS" : "FAIL");
process.exit(failures === 0 ? 0 : 1);
