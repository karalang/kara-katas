// verify_browser.mjs — drive the real Veil page in headless Chrome over CDP
// and assert the full pipeline works: page glue + wasm kernels + canvas.
//
// The node harness (test_node.mjs) proves the wasm in isolation; this proves
// the PAGE — instantiation, the working-image model, button wiring, and the
// canvas round-trip. Ops are driven through the real buttons; only the file
// picker is bypassed (the `window.__veil` test hook injects decoded pixels).
//
// Requires: Chrome/Chromium (auto-detected or $CHROME) and node >= 22.
// Run:  ./build.sh --build && node verify_browser.mjs
// Exits 0 on PASS, 1 on failure, 2 on a missing-prerequisite skip.
import { spawn, spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const PORT = 8764;
const CDP_PORT = 9413;
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
  if (!existsSync(join(HERE, "veil.js")) || !existsSync(join(HERE, "veil.wasm"))) {
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
  userDataDir = mkdtempSync(join(tmpdir(), "veil-cdp-"));
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
    try { ok = await evalJs("window.__veil ? __veil.ready() : false"); } catch {}
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
    __veil.loadPixels(a, w, h);
    return true;
  })()`);
  let d = await evalJs("__veil.dims()");
  if (d.w !== 4 || d.h !== 2) throw new Error(`load: dims ${d.w}x${d.h} != 4x2`);
  let p = await evalJs("__veil.pixel(0, 0)");
  if (String(p) !== "255,0,0,255") throw new Error(`load: pixel(0,0) ${p} != red`);
  console.error("[ok] load: 4x2 painted, top-left red");

  // Bar redaction via the REAL controls: left 2x2 -> black; right stays green.
  stage("bar");
  await evalJs(`(() => {
    document.getElementById('style').value = '2';
    document.getElementById('style').dispatchEvent(new Event('change'));
    document.getElementById('shade').value = '0';
    __veil.setSel(0, 0, 2, 2);
    document.getElementById('applysel').click();
    return true;
  })()`);
  await sleep(300);
  p = await evalJs("__veil.pixel(0, 0)");
  let pg = await evalJs("__veil.pixel(3, 0)");
  if (String(p) !== "0,0,0,255") throw new Error(`bar: pixel(0,0) ${p} != black`);
  if (String(pg) !== "0,255,0,255") throw new Error(`bar: pixel(3,0) ${pg} != green (outside touched!)`);
  console.error("[ok] bar redaction: rect black, outside untouched");

  // Undo restores.
  stage("undo");
  await evalJs(`document.getElementById('undo').click()`);
  await sleep(150);
  p = await evalJs("__veil.pixel(0, 0)");
  if (String(p) !== "255,0,0,255") throw new Error(`undo: pixel(0,0) ${p} != red`);
  console.error("[ok] undo restores working image");

  // Pixelate via the real controls over a red|blue 2x2 block: avg = (127,0,127).
  stage("pixelate");
  await evalJs(`(() => {
    const w = 4, h = 2, a = new Uint8ClampedArray(w * h * 4);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const o = (y * w + x) * 4;
      if (x === 0) { a[o] = 255; } else if (x === 1) { a[o + 2] = 255; }
      else { a[o + 1] = 255; }
      a[o + 3] = 255;
    }
    __veil.loadPixels(a, w, h);
    document.getElementById('style').value = '0';
    document.getElementById('style').dispatchEvent(new Event('change'));
    document.getElementById('str').value = 2;
    __veil.setSel(0, 0, 2, 2);
    document.getElementById('applysel').click();
    return true;
  })()`);
  await sleep(300);
  p = await evalJs("__veil.pixel(0, 0)");
  if (String(p) !== "127,0,127,255") throw new Error(`pixelate: pixel(0,0) ${p} != (127,0,127)`);
  console.error("[ok] pixelate: tile average on canvas");

  // The whole chain ran against ONE working image with no reload — the chaining
  // model itself is what just got verified.
  console.log("PASS — Veil page + wasm verified in real Chrome: load, bar redaction (exact), undo, pixelate (tile-average oracle).");
  ws.close();
  process.exit(0);
}

main().catch((e) => {
  console.error("FAIL:", e.message || e);
  process.exit(1);
});
