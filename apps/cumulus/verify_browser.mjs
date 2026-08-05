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

import { chromium } from "playwright";
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
  const status = await page.textContent("#log");

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
} finally {
  await browser.close();
  server.close();
}

console.log(failures === 0 ? "PASS" : "FAIL");
process.exit(failures === 0 ? 0 : 1);
