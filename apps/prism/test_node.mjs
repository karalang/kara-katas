import { instantiate } from "./prism.js";
import { readFileSync } from "node:fs";

const bytes = readFileSync(new URL("./prism.wasm", import.meta.url));

// A known 2×1 RGBA image: pixel0 = red, pixel1 = green.
const W = 2, H = 1;
const src = new Uint8Array([255, 0, 0, 255,  0, 255, 0, 255]);
let out = null;

const host = {
  read_src(dst, len, ctx) {
    new Uint8Array(ctx.memory.buffer, Number(dst), Number(len)).set(src.subarray(0, Number(len)));
  },
  put_pixels(ptr, len, w, h, ctx) {
    out = new Uint8Array(ctx.memory.buffer, Number(ptr), Number(len)).slice();
  },
};

const handle = await instantiate(host, { bytes });
handle.exports.process(BigInt(W), BigInt(H));

// Rec.601 integer luma: red = 255*30/100 = 76; green = 255*59/100 = 150. Alpha kept.
const expected = [76, 76, 76, 255,  150, 150, 150, 255];
const got = out ? [...out] : null;
console.log("got     :", JSON.stringify(got));
console.log("expected:", JSON.stringify(expected));
const ok = got && expected.every((v, i) => v === got[i]);
console.log(ok ? "PASS ✅  (host-FFI in + kernel + out all correct)" : "FAIL ❌");
process.exit(ok ? 0 : 1);
