# 91. Decode Ways

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String, Dynamic Programming &nbsp;·&nbsp; **Source:** [leetcode.com/problems/decode-ways](https://leetcode.com/problems/decode-ways/)

A message containing letters from A–Z is encoded by the mapping `'A' → "1"`, `'B' → "2"`, …, `'Z' → "26"`. To *decode* a digit string you partition it into a sequence of pieces, each of which is a key in that mapping; the answer for a string `s` is the number of distinct partitions. Strings containing partitions that map to a key with a leading zero (`"06"`, `"00"`, etc.) are **not** valid encodings — `'0'` is not in the alphabet on its own, and `"06"` is not the same key as `"6"`.

Return the number of ways to decode `s`. The answer is guaranteed to fit in a 32-bit integer.

```
"12"      →  2     "AB" (1,2) | "L" (12)
"226"     →  3     "BBF" (2,2,6) | "BZ" (2,26) | "VF" (22,6)
"06"      →  0     leading zero — no valid partition starts with '0'
"10"      →  1     "J" (10)         — the '0' attaches to the preceding '1'
"100"     →  0     '00' is not a key; '0' alone is not a key
"27"      →  1     "BG" (2,7)       — 27 is out of range, so two-digit split is illegal
```

**Constraints:** `1 ≤ s.length ≤ 100`, `s` consists of digits `'0'–'9'` only.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Bottom-up DP with a 2-cell rolling window | O(n) time, O(1) extra space | [`src/main.kara`](src/main.kara) ✓ | [`decode_ways.py`](decode_ways.py) ✓ |

`karac test` runs the 22-case block-form suite in [`src/main_test.kara`](src/main_test.kara) as the primary correctness loop; case titles name input + expected count, so a failure surfaces both without consulting the test source.

## Why a rolling window

The recurrence touches at most two prior cells:

```
dp[i] = (1 ≤ s[i-1] ≤ 9 ? dp[i-1] : 0)              // peel one digit off the end
      + (10 ≤ 10·s[i-2] + s[i-1] ≤ 26 ? dp[i-2] : 0) // peel two digits off the end
```

with `dp[0] = 1` (empty suffix has one decoding) and `dp[1] = 1` once a leading `'0'` has been rejected. Two `i64` cells (`prev2`, `prev1`) carry the entire state. The header comment in [`src/main.kara`](src/main.kara) covers the leading-zero bail and mid-stream-zero propagation.

## Kāra features exercised

- **`ref String` + `s.bytes()`** — read-only string borrow plus a zero-copy `Slice[u8]` view; LeetCode alphabet is digits only, so byte == codepoint and indexing is O(1) with no `Vec[char]` snapshot.
- **`u8` → `i32` digit math** — `(bytes[i] as i32) - (zero as i32)` widens before subtracting; `zero` is `b'0'` per design.md § Byte and Byte-String Literals.
- **`and` short-circuit range guards** — `d1 >= 1 and d1 <= 9` skips the second compare when the first fails.

No `Vec`, no `Map`, no shared structs — `Slice[u8]` view + two scalar `i64` cells.

## Running

```bash
# Primary correctness loop — 22-case block-form suite, JSONL on stdout.
karac test

# Cross-language reference — preserved as a paper-trail.
karac run src/main.kara
python3 decode_ways.py
diff <(karac run src/main.kara) <(python3 decode_ways.py) && echo OK
```

`karac test --filter <substring>` runs only cases whose name contains the substring (e.g. `karac test "leading"` runs just `"leading zero is invalid"`).

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, and Go. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`decode_ways.{kara,rs,c}`, `go-seq/main.go`). The Python mirror [`bench/decode_ways.py`](bench/decode_ways.py) is gated behind `KARA_BENCH_INCLUDE_PY=1` — at 10M calls it lands in the tens of seconds and would block the bench by default.

Per [`../../../BENCH.md`](../../../BENCH.md), the DP's `prev1`/`prev2` carry a strict cross-iteration dependency, so kata #91 is **seq-only** — no par lane.

**Workload.** An 80-byte mutable digit buffer; the hot loop calls `decode_ways` 10,000,000 times, mutating one byte per iteration (cycling digits 1–9 at position `k % 80`) so the input genuinely varies per call and the optimizer cannot hoist. The accumulator is reduced mod `1e9+7` each step; the sink line is the final reduced sum. All four mirrors agree on `507945311` before any timing runs — `bench.sh` fails loudly on mismatch.

### Runtime — seq lane

Snapshot — M5 Pro, 2026-06-05, hyperfine `--warmup 2 --runs 10 --shell=none`:

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| **kāra decode_ways**         | **379.8 ms ± 0.9 ms** | 377.0 ms | 99% |
| rust decode_ways (rustc -O)  | **354.5 ms ± 8.1 ms** | 352.0 ms | 99% |
| c    decode_ways (clang -O3) | **400.5 ms ± 3.0 ms** | 398.0 ms | 99% |
| go   decode_ways             | **455.3 ms ± 14.9 ms** | 453.0 ms | 99% |

Kāra matches rustc-O within combined σ and runs ~1.05× faster than `clang -O3`. (The 2026-05-22 snapshot read kāra 381.1 / rust 381.7 / c 427.5 / go 490.3 — all four moved down 4–6% together in the 06-05 batch on **byte-identical binaries**, including the kāra one, which the May-30 karac rebuilt to the same sha256; the kāra/rust order flip within the parity band is noise.) Two consecutive karac codegen fixes closed the gap from the initial 501 ms (1.35× rust) snapshot:

1. Cast lowering (commit `5eac110`) — `(bytes[i] as i32)` for `bytes: Vec[u8]` was emitting `ldrsb`+`sxtb`+`and #0xff` where rust emitted a single `ldrb`. Inner-loop went 16 → 14 instructions, dropping the wall to 415 ms (1.13× rust).
2. Auto-par cost-model (commit `1f3f498`) — `stmt_is_constant_init` was missing `ExprKind::ByteLit`, so `let zero: u8 = b'0';` mis-classified as non-constant pushed the prologue into a 4-branch `karac_par_run`. The captured `let l = 80` became an opaque load downstream, breaking LLVM's const-prop into `k % l` (lowered as `sdiv` instead of `umulh`-reciprocal). Removing the wasteful par-block recovered the final ~34 ms and stripped 263 KiB of par-machinery from the binary.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `decode_ways` | **74.1 ms ± 0.6 ms** | 88.3 ms ± 1.7 ms | 44.4 ms ± 0.4 ms |

Single-file invocations only — the Go module's `go build` mixes module resolution + std-lib link with codegen and is deliberately excluded per BENCH.md.

### Binary size

| Implementation | Bytes | KiB |
|---|---|---|
| c    decode_ways  | 33,456 | 32.7 |
| **kāra decode_ways** | **33,997** | **33.2** |
| rust decode_ways  | 466,488 | 455.6 |
| go   decode_ways  | 2,492,546 | 2,434.1 |

Kāra is now within **~550 bytes of clang's binary** — basically at parity. (The 2026-06-05 re-bench reproduced every size in this table byte-for-byte, kāra's via a fresh rebuild under the May-30 karac.) Two consecutive karac fixes brought it down from the original 312 KiB: the auto-par cost-model fix (commit `1f3f498`) stripped 263 KiB of par-block machinery (per-branch trampolines + return-slot struct + cancel-check globals) when there's no actual par work to run, and the `__TEXT,__jittmpl` segment re-scope (commit `e76f42b`) reclaimed the final 16 KiB by parking the 4-byte JIT-template manifest inside `__TEXT` instead of a fresh page-aligned `__KARA` segment. Rust's 456 KiB and Go's 2.4 MiB both reflect their respective runtimes (GC, panic-unwind tables, reflection).

### Runtime memory (peak)

| Implementation | Bytes | MiB |
|---|---|---|
| c    decode_ways  | 1,081,344 | 1.0 |
| **kāra decode_ways** | **1,064,960** | **1.0** |
| rust decode_ways  | 1,130,496 | 1.1 |
| go   decode_ways  | 2,916,352 | 2.8 |

A single 80-byte buffer + scalar accumulator; the algorithm itself is O(1) extra space. Kāra reads **byte-identical to the C mirror** in the 06-05 sample (the 05-22 sample had kāra two pages above C — single-shot `/usr/bin/time -l` readings are page-level noisy, and the whole table shifted down ~3–5 pages with the environment); either way kāra is at parity with the C mirror — the par-block-runtime overhead that pushed kāra to 1.5 MiB pre-fix (the runtime's worker-pool initialization + spawn-site registry) is no longer paid when there's no actual par work to run.

### Compile memory (cold)

| Compiler invocation | Bytes | MiB |
|---|---|---|
| `clang -O3 decode_ways.c`     | 2,726,298 | 2.6 |
| **`karac build decode_ways.kara`** | **13,736,346** | **13.1** |
| `rustc -O decode_ways.rs`     | 28,311,552 | 27.0 |

Kāra's compile-memory footprint is ~5.0× clang's and ~2.1× lower than rustc's on this kata. The 2026-05-25 5-sample re-measure (range 8.8–9.1 MiB, after the `__TEXT,__jittmpl` segment re-scope, karac `e76f42b`) read ~9.0 MiB; today's 9.7 MiB is the corpus-wide benign compile-mem floor band on the May-30 karac build (+0.7, same band every re-swept kata shows; the emitted binary is byte-identical, so it's compiler-internal footprint, not codegen). rustc held flat at 27.0.

### Numbers published here are reference data

The CI gate's source-of-truth aggregate lives in [`karac-rust/bench/compile_speed/`](../../../../karac-rust/bench/compile_speed/README.md) (different corpus: curated subset + synthetic 10K-LOC stress program).
