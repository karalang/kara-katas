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

Snapshot — M5 Pro, 2026-05-22, hyperfine `--warmup 2 --runs 10 --shell=none`:

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| rust decode_ways (rustc -O)  | **371.3 ms ± 13.3 ms** | 367.6 ms | 99% |
| c    decode_ways (clang -O3) | **453.2 ms ± 42.0 ms** | 441.7 ms | 97% |
| go   decode_ways             | **496.2 ms ± 18.0 ms** | 489.2 ms | 99% |
| **kāra decode_ways**         | **501.1 ms ± 23.6 ms** | 492.6 ms | 98% |

All four codegen langs land within 1.35× of each other. Kāra is at parity with Go on this workload (501 ms vs 496 ms — within one σ) and ~1.35× slower than the rustc-O baseline. C's wide σ comes from a single 566 ms outlier in the 10-run sample; the median is closer to 425 ms.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `decode_ways` | **61.2 ms ± 1.6 ms** | 83.5 ms ± 9.4 ms | 43.0 ms ± 1.5 ms |

Single-file invocations only — the Go module's `go build` mixes module resolution + std-lib link with codegen and is deliberately excluded per BENCH.md.

### Binary size

| Implementation | Bytes | KiB |
|---|---|---|
| c    decode_ways  | 33,456 | 32.7 |
| **kāra decode_ways** | **319,512** | **312.0** |
| rust decode_ways  | 466,488 | 455.6 |
| go   decode_ways  | 2,492,546 | 2,434.1 |

Go's binary is ~8× larger than Kāra's because `go build` statically links the Go runtime + GC + reflection (a deliberate Go design choice). Kāra sits in the middle — small enough that the LLVM-emitted code dominates over runtime support.

### Runtime memory (peak)

| Implementation | Bytes | MiB |
|---|---|---|
| c    decode_ways  | 1,114,448 | 1.1 |
| rust decode_ways  | 1,163,600 | 1.1 |
| **kāra decode_ways** | **1,540,456** | **1.5** |
| go   decode_ways  | 3,097,176 | 3.0 |

A single 80-byte buffer + scalar accumulator; the algorithm itself is O(1) extra space. The numbers above are dominated by runtime/loader overhead, not working set.

### Compile memory (cold)

| Compiler invocation | Bytes | MiB |
|---|---|---|
| `clang -O3 decode_ways.c`     | 2,720,104 | 2.6 |
| **`karac build decode_ways.kara`** | **9,568,736** | **9.1** |
| `rustc -O decode_ways.rs`     | 28,426,888 | 27.1 |

Kāra's compile-memory footprint is ~3× clang's and ~3× lower than rustc's on this kata.

### Numbers published here are reference data

The CI gate's source-of-truth aggregate lives in [`karac-rust/bench/compile_speed/`](../../../../karac-rust/bench/compile_speed/README.md) (different corpus: curated subset + synthetic 10K-LOC stress program).
