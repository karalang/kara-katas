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
// `?seq` tells the coi-serviceworker shim in index.html NOT to register, so
// this leg exercises the true single-threaded fallback on a headerless server.
const PAGE_URL = `http://127.0.0.1:${PORT}/index.html?seq`;
const PAGE_URL_COI = `http://127.0.0.1:${PORT}/index.html`;

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
  const iso1 = await evalJs("self.crossOriginIsolated === true");
  if (iso1) throw new Error("?seq leg is cross-origin isolated — coi shim registered anyway?");
  const thr1 = await evalJs("__prism.threaded()");
  if (thr1 !== false) throw new Error("?seq leg picked threaded (escape hatch broken)");
  console.error("[ok] wasm instantiated (sequential fallback, ?seq honored)");

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

  // ── Phase 2: THREADED leg — serve cross-origin isolated (serve.py sets
  // COOP/COEP), fresh page, assert the threaded module is picked, then prove
  // an op produces oracle-exact pixels with the pool active.
  stage("threaded-serve");
  const PORT2 = PORT + 1;
  const server2 = spawn("python3", [join(HERE, "serve.py"), String(PORT2)], { cwd: HERE, stdio: "ignore" });
  const cleanup2 = () => { try { server2.kill("SIGKILL"); } catch {} };
  process.on("exit", cleanup2);
  const PAGE2 = `http://127.0.0.1:${PORT2}/index.html`;
  if (!(await waitForHttp(PAGE2))) throw new Error("COOP/COEP server never came up");
  const { targetId: t2 } = await cdp.send("Target.createTarget", { url: PAGE2 });
  const { sessionId: s2 } = await cdp.send("Target.attachToTarget", { targetId: t2, flatten: true });
  await cdp.send("Page.enable", {}, s2);
  await cdp.send("Runtime.enable", {}, s2);
  const evalJs2 = async (expr) => {
    const r = await cdp.send("Runtime.evaluate",
      { expression: expr, returnByValue: true, awaitPromise: true }, s2, 20000);
    if (r.exceptionDetails) throw new Error("page JS threw: " + JSON.stringify(r.exceptionDetails));
    return r.result.value;
  };
  stage("threaded-ready");
  let ok2 = false;
  for (let i = 0; i < 150; i++) {
    try { ok2 = await evalJs2("window.__prism ? __prism.ready() : false"); } catch {}
    if (ok2) break;
    await sleep(200);
  }
  if (!ok2) throw new Error("threaded page: wasm never became ready");
  const iso = await evalJs2("self.crossOriginIsolated === true");
  if (!iso) throw new Error("threaded page is NOT cross-origin isolated");
  const thr = await evalJs2("__prism.threaded()");
  if (thr !== true) throw new Error("threaded page picked sequential (threaded=" + thr + ")");
  console.error("[ok] threaded module active (crossOriginIsolated + threaded=true)");
  stage("threaded-op");
  await evalJs2(`(() => {
    const w = 4, h = 2, a = new Uint8ClampedArray(w * h * 4);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const o = (y * w + x) * 4;
      if (x < 2) { a[o] = 255; } else { a[o + 1] = 255; }
      a[o + 3] = 255;
    }
    __prism.loadPixels(a, w, h);
    return true;
  })()`);
  await evalJs2(`document.getElementById('grayscale').click()`);
  let gp = null;
  for (let i = 0; i < 50; i++) {
    await sleep(200);
    gp = await evalJs2("__prism.pixel(0, 0)");
    if (String(gp) === "76,76,76,255") break;
  }
  if (String(gp) !== "76,76,76,255") throw new Error(`threaded grayscale: pixel ${gp} != 76-gray`);
  // Lanczos resize through the pool (the banded kernel): 4x2 -> 8x4.
  await evalJs2(`(() => {
    document.getElementById('method').value = '2';
    const rw = document.getElementById('rw'), rh = document.getElementById('rh');
    rw.value = 8; rh.value = 4;
    document.getElementById('resize').click();
    return true;
  })()`);
  let d2 = null;
  for (let i = 0; i < 50; i++) {
    await sleep(200);
    d2 = await evalJs2("__prism.dims()");
    if (d2 && d2.w === 8 && d2.h === 4) break;
  }
  if (!d2 || d2.w !== 8 || d2.h !== 4) throw new Error(`threaded resize: dims ${d2 && d2.w}x${d2 && d2.h} != 8x4`);
  console.error("[ok] threaded ops: grayscale oracle + banded lanczos resize on the pool");
  cleanup2();

  // ── Phase 3: COI-SHIM leg — the GitHub Pages simulation. Same headerless
  // server as phase 1, but WITHOUT ?seq: coi-serviceworker registers, reloads
  // the page once, and the reloaded document is cross-origin isolated, so the
  // threaded module gets picked with no server-side headers at all.
  stage("coi-shim");
  const { targetId: t3 } = await cdp.send("Target.createTarget", { url: PAGE_URL_COI });
  const { sessionId: s3 } = await cdp.send("Target.attachToTarget", { targetId: t3, flatten: true });
  await cdp.send("Page.enable", {}, s3);
  await cdp.send("Runtime.enable", {}, s3);
  const evalJs3 = async (expr) => {
    const r = await cdp.send("Runtime.evaluate",
      { expression: expr, returnByValue: true, awaitPromise: true }, s3, 20000);
    if (r.exceptionDetails) throw new Error("page JS threw: " + JSON.stringify(r.exceptionDetails));
    return r.result.value;
  };
  // Poll across the shim's mid-flight reload: evaluate can fail during the
  // navigation, and the pre-reload document reports isolated=false — keep
  // polling until the post-reload document is isolated AND the wasm is live.
  stage("coi-shim-ready");
  let ok3 = false;
  for (let i = 0; i < 150; i++) {
    try {
      ok3 = await evalJs3(
        "self.crossOriginIsolated === true && window.__prism ? __prism.ready() : false");
    } catch {}
    if (ok3) break;
    await sleep(200);
  }
  if (!ok3) throw new Error("coi-shim page never became isolated+ready (SW failed to register?)");
  const thr3 = await evalJs3("__prism.threaded()");
  if (thr3 !== true) throw new Error("coi-shim page picked sequential (threaded=" + thr3 + ")");
  stage("coi-shim-op");
  await evalJs3(`(() => {
    const w = 4, h = 2, a = new Uint8ClampedArray(w * h * 4);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const o = (y * w + x) * 4;
      if (x < 2) { a[o] = 255; } else { a[o + 1] = 255; }
      a[o + 3] = 255;
    }
    __prism.loadPixels(a, w, h);
    return true;
  })()`);
  await evalJs3(`document.getElementById('grayscale').click()`);
  let gp3 = null;
  for (let i = 0; i < 50; i++) {
    await sleep(200);
    gp3 = await evalJs3("__prism.pixel(0, 0)");
    if (String(gp3) === "76,76,76,255") break;
  }
  if (String(gp3) !== "76,76,76,255") throw new Error(`coi-shim grayscale: pixel ${gp3} != 76-gray`);
  console.error("[ok] coi-shim leg: headerless server -> SW-injected COOP/COEP -> threaded + oracle");

  console.log("PASS — page + wasm verified in real Chrome: sequential leg (?seq: fallback pinned + load, grayscale oracle, undo, rotate, resize, crop, chained), threaded leg (real COOP/COEP headers + banded lanczos on the pool), AND coi-shim leg (headerless server, SW-injected isolation -> threaded).");
  ws.close();
  process.exit(0);
}

main().catch((e) => {
  console.error("FAIL:", e.message || e);
  process.exit(1);
});
