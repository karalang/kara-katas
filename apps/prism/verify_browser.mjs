// verify_browser.mjs — drive the real Prism page in headless Chrome over CDP
// and assert the full pipeline works: page glue + wasm kernels + canvas.
//
// The node harness (test_node.mjs) proves the wasm in isolation; this proves
// the PAGE — instantiation, the working-image model, button wiring, and the
// canvas round-trip. Ops are driven through the real buttons; only the file
// picker is bypassed (the `window.__prism` test hook injects decoded pixels).
//
// Requires: Chrome/Chromium (auto-detected or $CHROME) and node >= 22.
// Run:  ./build.sh --build && node verify_browser.mjs
// Exits 0 on PASS, 1 on failure, 2 on a missing-prerequisite skip.
import { spawn, spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const PORT = 8763;
const CDP_PORT = 9412;
const HERE = new URL(".", import.meta.url).pathname;
const PAGE_URL = `http://127.0.0.1:${PORT}/index.html`;

function findChrome() {
  const candidates = [
    process.env.CHROME,
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome", "chromium", "chromium-browser",
  ].filter(Boolean);
  for (const c of candidates) {
    if (c.includes("/")) {
      try { if (spawnSync(c, ["--version"]).status === 0) return c; } catch {}
    } else {
      const r = spawnSync("which", [c]);
      if (r.status === 0) return r.stdout.toString().trim();
    }
  }
  return null;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function waitForHttp(url, tries = 50) {
  for (let i = 0; i < tries; i++) {
    try { const r = await fetch(url); if (r.ok || r.status === 404) return true; } catch {}
    await sleep(100);
  }
  return false;
}

class CDP {
  constructor(ws) {
    this.ws = ws; this.id = 0; this.pending = new Map();
    ws.addEventListener("message", (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        msg.error ? reject(new Error(JSON.stringify(msg.error))) : resolve(msg.result);
      }
    });
  }
  send(method, params = {}, sessionId, timeoutMs = 8000) {
    const id = ++this.id;
    const payload = { id, method, params };
    if (sessionId) payload.sessionId = sessionId;
    this.ws.send(JSON.stringify(payload));
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error(`CDP ${method} timed out after ${timeoutMs}ms`));
      }, timeoutMs);
      this.pending.set(id, {
        resolve: (v) => { clearTimeout(timer); resolve(v); },
        reject: (e) => { clearTimeout(timer); reject(e); },
      });
    });
  }
}

let server, chrome, userDataDir;
function cleanup() {
  try { chrome?.kill("SIGKILL"); } catch {}
  try { server?.kill("SIGKILL"); } catch {}
  try { if (userDataDir) rmSync(userDataDir, { recursive: true, force: true }); } catch {}
}
process.on("exit", cleanup);

let lastStage = "start";
const stage = (s) => { lastStage = s; console.error(`[stage] ${s}`); };
setTimeout(() => {
  console.error(`FAIL: watchdog — verify exceeded 120s (last stage: ${lastStage})`);
  process.exit(3);
}, 120000);

async function main() {
  if (!existsSync(join(HERE, "prism.js")) || !existsSync(join(HERE, "prism.wasm"))) {
    console.error("SKIP: artifacts missing — run `./build.sh --build` first.");
    process.exit(2);
  }
  const chromePath = findChrome();
  if (!chromePath) { console.error("SKIP: no Chrome/Chromium found (set $CHROME)."); process.exit(2); }

  stage("serve");
  server = spawn("python3", ["-m", "http.server", String(PORT), "--bind", "127.0.0.1"],
    { cwd: HERE, stdio: "ignore" });
  if (!(await waitForHttp(PAGE_URL))) throw new Error("static server never came up");

  stage("chrome");
  userDataDir = mkdtempSync(join(tmpdir(), "prism-cdp-"));
  chrome = spawn(chromePath, [
    "--headless=new", "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage",
    "--no-first-run", "--no-default-browser-check",
    `--user-data-dir=${userDataDir}`, `--remote-debugging-port=${CDP_PORT}`, "about:blank",
  ], { stdio: "ignore" });

  let version;
  for (let i = 0; i < 60; i++) {
    try { version = await (await fetch(`http://127.0.0.1:${CDP_PORT}/json/version`)).json(); break; } catch {}
    await sleep(100);
  }
  if (!version) throw new Error("Chrome CDP endpoint never came up");

  const ws = new WebSocket(version.webSocketDebuggerUrl);
  await new Promise((res, rej) => {
    ws.addEventListener("open", res, { once: true });
    ws.addEventListener("error", rej, { once: true });
  });
  const cdp = new CDP(ws);

  stage("attach");
  const { targetId } = await cdp.send("Target.createTarget", { url: PAGE_URL });
  const { sessionId } = await cdp.send("Target.attachToTarget", { targetId, flatten: true });
  await cdp.send("Page.enable", {}, sessionId);
  await cdp.send("Runtime.enable", {}, sessionId);

  const evalJs = async (expr) => {
    const r = await cdp.send("Runtime.evaluate",
      { expression: expr, returnByValue: true, awaitPromise: true }, sessionId, 15000);
    if (r.exceptionDetails) throw new Error("page JS threw: " + JSON.stringify(r.exceptionDetails));
    return r.result.value;
  };

  // Wait for the module + wasm to be live.
  stage("wasm-ready");
  let ok = false;
  for (let i = 0; i < 100; i++) {
    try { ok = await evalJs("window.__prism ? __prism.ready() : false"); } catch {}
    if (ok) break;
    await sleep(150);
  }
  if (!ok) throw new Error("wasm never became ready (instantiate failed?)");
  console.error("[ok] wasm instantiated");

  // Inject a known 4x2 image through the test hook: left half red, right green.
  stage("load");
  await evalJs(`(() => {
    const w = 4, h = 2, a = new Uint8ClampedArray(w * h * 4);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const o = (y * w + x) * 4;
      if (x < 2) { a[o] = 255; } else { a[o + 1] = 255; }
      a[o + 3] = 255;
    }
    __prism.loadPixels(a, w, h);
    return true;
  })()`);
  let d = await evalJs("__prism.dims()");
  if (d.w !== 4 || d.h !== 2) throw new Error(`load: dims ${d.w}x${d.h} != 4x2`);
  let p = await evalJs("__prism.pixel(0, 0)");
  if (String(p) !== "255,0,0,255") throw new Error(`load: pixel(0,0) ${p} != red`);
  console.error("[ok] load: 4x2 painted, top-left red");

  // Grayscale via the REAL button: red -> 76, green -> 150 (the kernel oracle).
  stage("grayscale");
  await evalJs(`document.getElementById('grayscale').click()`);
  await sleep(300);
  p = await evalJs("__prism.pixel(0, 0)");
  const p2 = await evalJs("__prism.pixel(3, 0)");
  if (String(p) !== "76,76,76,255") throw new Error(`grayscale: pixel(0,0) ${p} != 76-gray`);
  if (String(p2) !== "150,150,150,255") throw new Error(`grayscale: pixel(3,0) ${p2} != 150-gray`);
  console.error("[ok] grayscale via button: Rec.601 oracle matches on canvas");

  // Undo restores the color image.
  stage("undo");
  await evalJs(`document.getElementById('undo').click()`);
  await sleep(150);
  p = await evalJs("__prism.pixel(0, 0)");
  if (String(p) !== "255,0,0,255") throw new Error(`undo: pixel(0,0) ${p} != red`);
  console.error("[ok] undo restores working image");

  // Rotate 90° CW via button: dims swap to 2x4; old top-RIGHT (green) is now
  // top-left... check: dst(0,0) = src(0, h-1-0=1) = (x=0,y=1) = red actually.
  // src (x=0,y=1) is left half -> red. Assert dims + that corner.
  stage("rotate");
  await evalJs(`document.getElementById('rotr').click()`);
  await sleep(300);
  d = await evalJs("__prism.dims()");
  if (d.w !== 2 || d.h !== 4) throw new Error(`rotate: dims ${d.w}x${d.h} != 2x4`);
  p = await evalJs("__prism.pixel(0, 0)");
  if (String(p) !== "255,0,0,255") throw new Error(`rotate: pixel(0,0) ${p} != red`);
  console.error("[ok] rotate 90cw via button: dims swapped, corner correct");

  // Resize to 4x8 via the real inputs + button (bilinear for exactness of dims).
  stage("resize");
  await evalJs(`(() => {
    document.getElementById('method').value = '1';
    const rw = document.getElementById('rw'), rh = document.getElementById('rh');
    rw.value = 4; rh.value = 8;
    document.getElementById('resize').click();
    return true;
  })()`);
  await sleep(400);
  d = await evalJs("__prism.dims()");
  if (d.w !== 4 || d.h !== 8) throw new Error(`resize: dims ${d.w}x${d.h} != 4x8`);
  console.error("[ok] resize via panel: canvas is 4x8");

  // Crop back down via the selection path (hook sets the rect; real button applies).
  stage("crop");
  await evalJs(`__prism.setSel(0, 0, 2, 2)`);
  await evalJs(`document.getElementById('docrop').click()`);
  await sleep(300);
  d = await evalJs("__prism.dims()");
  if (d.w !== 2 || d.h !== 2) throw new Error(`crop: dims ${d.w}x${d.h} != 2x2`);
  console.error("[ok] crop selection applies");

  // The whole chain ran against ONE working image with no reload — the chaining
  // model itself is what just got verified.
  console.log("PASS — page + wasm pipeline verified in real Chrome: load, grayscale (oracle pixels), undo, rotate, resize, crop, chained.");
  ws.close();
  process.exit(0);
}

main().catch((e) => {
  console.error("FAIL:", e.message || e);
  process.exit(1);
});
