// bench_browser.mjs — measure Prism's resize kernels in a real browser.
//
// The README quotes browser timings for a 3 MP and a 12 MP Lanczos resize.
// Those are the numbers a user actually experiences, and they are not
// derivable from the native bench: wasm codegen, the single-threaded fallback,
// and the put_pixels canvas write all differ. So they get measured here, the
// same way the page measures them — `__prism.bench` spans exactly what the
// `apply()` readout in index.html reports.
//
// Both legs are measured against the SAME artifacts the page ships:
//   sequential  — `?seq` pins the single-threaded fallback (headerless server)
//   threaded    — real COOP/COEP headers via serve.py, so prism.threads.wasm
//                 loads and the compiler's auto-par fan-out has a pool
//
// Requires: Chrome/Chromium (auto-detected or $CHROME) and node >= 22.
// Run:  ./build.sh && node bench_browser.mjs
// Exits 0 on success, 1 on failure, 2 on a missing-prerequisite skip.
import { spawn, spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const PORT_PLAIN = 8765;   // python http.server — no COOP/COEP, `?seq` leg
const PORT_COI = 8766;     // serve.py — real isolation headers, threaded leg
const CDP_PORT = 9414;
const HERE = new URL(".", import.meta.url).pathname;
const REPS = Number(process.env.PRISM_BENCH_REPS || 7);
const OP_LANCZOS = 2;

// (label, source dims, target dims). 12 MP -> 3 MP is the README's headline
// case; 3 MP -> 0.75 MP is the smaller one it also quotes.
const CASES = [
  { label: "12 MP → 3 MP", sw: 4000, sh: 3000, dw: 2000, dh: 1500 },
  { label: "3 MP → 0.75 MP", sw: 2000, sh: 1500, dw: 1000, dh: 750 },
];

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

async function waitForHttp(url, tries = 80) {
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
  send(method, params = {}, sessionId, timeoutMs = 120000) {
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

let plainServer, coiServer, chrome, userDataDir;
function cleanup() {
  try { chrome?.kill("SIGKILL"); } catch {}
  try { plainServer?.kill("SIGKILL"); } catch {}
  try { coiServer?.kill("SIGKILL"); } catch {}
  try { if (userDataDir) rmSync(userDataDir, { recursive: true, force: true }); } catch {}
}
process.on("exit", cleanup);

let lastStage = "start";
const stage = (s) => { lastStage = s; console.error(`[stage] ${s}`); };
setTimeout(() => {
  console.error(`FAIL: watchdog — bench exceeded 600s (last stage: ${lastStage})`);
  process.exit(3);
}, 600000);

/** Open a page, wait for wasm, and run every case through `__prism.bench`. */
async function benchLeg(cdp, url, expectThreaded) {
  const { targetId } = await cdp.send("Target.createTarget", { url });
  const { sessionId } = await cdp.send("Target.attachToTarget", { targetId, flatten: true });
  await cdp.send("Page.enable", {}, sessionId);
  await cdp.send("Runtime.enable", {}, sessionId);
  const evalJs = async (expr, timeoutMs = 120000) => {
    const r = await cdp.send("Runtime.evaluate",
      { expression: expr, returnByValue: true, awaitPromise: true }, sessionId, timeoutMs);
    if (r.exceptionDetails) throw new Error("page JS threw: " + JSON.stringify(r.exceptionDetails));
    return r.result.value;
  };

  let ready = false;
  for (let i = 0; i < 200; i++) {
    try { ready = await evalJs("window.__prism ? __prism.ready() : false"); } catch {}
    if (ready) break;
    await sleep(150);
  }
  if (!ready) throw new Error(`wasm never became ready at ${url}`);

  const threaded = await evalJs("__prism.threaded()");
  if (threaded !== expectThreaded) {
    throw new Error(
      `${url}: threaded=${threaded}, expected ${expectThreaded} — the leg under ` +
      `test is not the leg that loaded, so the number would be mislabelled`);
  }

  const out = [];
  for (const c of CASES) {
    // A deterministic non-flat source: a flat image would let neither the
    // kernel nor the browser shortcut anything, but it also would not exercise
    // the tap arithmetic on varying data.
    await evalJs(`(() => {
      const w = ${c.sw}, h = ${c.sh}, a = new Uint8ClampedArray(w * h * 4);
      for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
        const o = (y * w + x) * 4;
        a[o] = (x * 7 + y * 3) & 255;
        a[o + 1] = (x ^ y) & 255;
        a[o + 2] = (x + y * 5) & 255;
        a[o + 3] = 255;
      }
      __prism.loadPixels(a, w, h);
      return true;
    })()`);
    const r = await evalJs(
      `__prism.bench(${OP_LANCZOS}, ${c.dw}, ${c.dh}, ${REPS})`, 300000);
    out.push({ label: c.label, median: r.median });
    console.error(`  ${c.label.padEnd(16)} ${r.median.toFixed(0).padStart(6)} ms`);
  }
  await cdp.send("Target.closeTarget", { targetId });
  return out;
}

async function main() {
  for (const f of ["prism.js", "prism.wasm", "prism.threads.wasm"]) {
    if (!existsSync(join(HERE, f))) {
      console.error(`SKIP: ${f} missing — run \`./build.sh\` first.`);
      process.exit(2);
    }
  }
  const chromePath = findChrome();
  if (!chromePath) { console.error("SKIP: no Chrome/Chromium found (set $CHROME)."); process.exit(2); }

  stage("serve");
  plainServer = spawn("python3", ["-m", "http.server", String(PORT_PLAIN), "--bind", "127.0.0.1"],
    { cwd: HERE, stdio: "ignore" });
  coiServer = spawn("python3", ["serve.py", String(PORT_COI)], { cwd: HERE, stdio: "ignore" });
  if (!(await waitForHttp(`http://127.0.0.1:${PORT_PLAIN}/index.html`)))
    throw new Error("plain static server never came up");
  if (!(await waitForHttp(`http://127.0.0.1:${PORT_COI}/index.html`)))
    throw new Error("COOP/COEP server never came up");

  stage("chrome");
  userDataDir = mkdtempSync(join(tmpdir(), "prism-bench-"));
  chrome = spawn(chromePath, [
    "--headless=new", "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage",
    "--no-first-run", "--no-default-browser-check",
    `--user-data-dir=${userDataDir}`, `--remote-debugging-port=${CDP_PORT}`, "about:blank",
  ], { stdio: "ignore" });

  let version;
  for (let i = 0; i < 80; i++) {
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

  console.error(`\nmedian of ${REPS} reps, lanczos-3, headless Chrome`);
  stage("sequential");
  console.error("\nsequential (?seq, single-threaded fallback):");
  const seq = await benchLeg(cdp, `http://127.0.0.1:${PORT_PLAIN}/index.html?seq`, false);
  stage("threaded");
  console.error("\nthreaded (real COOP/COEP headers, worker pool):");
  const thr = await benchLeg(cdp, `http://127.0.0.1:${PORT_COI}/index.html`, true);

  console.error("\n" + "─".repeat(52));
  console.error("case              sequential    threaded   speedup");
  for (let i = 0; i < CASES.length; i++) {
    const s = seq[i].median, t = thr[i].median;
    console.error(
      `${CASES[i].label.padEnd(16)} ${s.toFixed(0).padStart(8)} ms ${t.toFixed(0).padStart(9)} ms` +
      `   ${(s / t).toFixed(2)}x`);
  }
  console.error("─".repeat(52));
  console.log(JSON.stringify({ reps: REPS, sequential: seq, threaded: thr }));
}

main().then(() => process.exit(0)).catch((e) => {
  console.error(`FAIL (stage: ${lastStage}): ${e.message}`);
  process.exit(1);
});
