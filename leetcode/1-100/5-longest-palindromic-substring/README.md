# 5. Longest Palindromic Substring

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String, Two Pointers, Dynamic Programming &nbsp;·&nbsp; **Source:** [leetcode.com/problems/longest-palindromic-substring](https://leetcode.com/problems/longest-palindromic-substring/)

Given a string `s`, return *a* longest palindromic substring of `s`.

**Constraints:** `1 ≤ s.length ≤ 1000`, `s` consists of digits and English letters. (The kata also exercises `s.length == 0` because the algorithm is well-defined there.)

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Expand around center | O(n²) time, O(1) extra space | [`expand_around_center.kara`](expand_around_center.kara) ✓ | [`expand_around_center.py`](expand_around_center.py) ✓ |

### Why expand-around-center

Every palindromic substring has a unique **center**: a single character for odd lengths, a gap between two characters for even lengths. There are exactly `2n − 1` centers in a string of length `n` (`n` odd centers + `n − 1` even centers). For each center, the maximal palindrome around it is found by walking two pointers outward in lockstep and stopping as soon as they go out of range or disagree. The overall answer is the longest palindrome found across all centers.

There is no faster *general* algorithm in this complexity class with constant auxiliary memory — Manacher's algorithm gets you to O(n), but at the cost of significantly more code and a transformed-string scratch array. For Kāra's current shape (no fancy string types, no `&str` slicing) expand-around-center is the most direct expression.

**LeetCode admits multiple valid answers** when palindromes tie for the maximum length. For `"babad"`, both `"bab"` (start=0) and `"aba"` (start=1) are accepted; this kata's strict `>` tiebreak picks the leftmost (`(0, 3)`). The Python and Kāra implementations make the same choice, so the diff stays clean across all cases.

## Kāra features exercised

- **`ref String` + `s.bytes()`** — read-only string borrow plus a zero-copy `Slice[u8]` view; LeetCode alphabet is ASCII so byte == codepoint and indexing is O(1) with no `Vec[char]` snapshot.
- **`Slice[u8]` parameter on a helper** — the `expand` helper takes the byte view by value; `.len()` and indexed reads are both O(1) over the slice header.
- **`Array[i64, 2]` return + tuple-style indexing** — same `[start, length]` shape kata [#1](../1-two-sum/) uses; can become a real tuple once `Option[(i64, i64)]` is solid in the interpreter.
- **`while ... and ... and ...` short-circuit** — three-way conjunction with bounds check before byte compare, so out-of-range indexing never happens.
- **Mutable accumulator pattern** — strict `>` (not `>=`) preserves the left-to-right tiebreak among equal-length palindromes.

No `Map`, no `Set`, no shared structs.

## Running

```bash
# Kāra (compiled or interpreted — both work)
karac run   expand_around_center.kara
karac build expand_around_center.kara && ./expand_around_center

# Python
python3 expand_around_center.py
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, and Go. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`expand_around_center.{kara,rs,c}`, `go-seq/main.go`). The Python mirror is included in the long-workloads table below; it's skipped from the sink check by default (≈110 ms at this N) — set `KARA_BENCH_INCLUDE_PY=1` to opt in.

Per [`../../../BENCH.md`](../../../BENCH.md), the inner expand loop carries a strict `chars[lo] == chars[hi]` data dependency that gates the next step, and the outer K=10 loop is too small to amortize par dispatch — so kata #5 is **seq-only**. The Kāra binary is verified seq via `nm -gU bench/target/expand_around_center_kara | grep karac_par_run` (no auto-par symbols present) per BENCH.md § Implicit auto-par.

**Workload.** N = 5000 copies of `'a'` — the worst-case shape for expand-around-center: every one of the `2n − 1` centers expands all the way to the boundary, and no `chars[lo] != chars[hi]` check ever short-circuits the inner loop (≈n²/2 ≈ 12.5M character comparisons per call). K = 10 outer iterations. All four mirrors agree on the sink line `50000 = K × (best_start + best_length) = 10 × (0 + 5000)` before any timing runs — `bench.sh` fails loudly on mismatch.

The bench binaries use the `Vec[char]` snapshot shape (matching Rust's `Vec<char>`) for apples-to-apples comparison; the shipped [`expand_around_center.kara`](expand_around_center.kara) uses `s.bytes()` directly. A future bench refresh can switch both languages to byte-array equivalents — the headline numbers below would shift downward correspondingly.

| File | What it does |
|---|---|
| [`bench/expand_around_center.kara`](bench/expand_around_center.kara) | N=5000 single-char `'a'` input, K=10 outer iterations, `Vec[char]` snapshot + indexed access |
| [`bench/expand_around_center.rs`](bench/expand_around_center.rs) | Algorithmic mirror; `Vec<char>`; compiled with `rustc -O` |
| [`bench/expand_around_center.c`](bench/expand_around_center.c) | Algorithmic mirror; `int32_t*` snapshot; compiled with `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | Algorithmic mirror; `[]rune` snapshot; compiled with `go build` |
| [`bench/expand_around_center.py`](bench/expand_around_center.py) | Algorithmic mirror — same N, K, sink |

### Runtime — seq lane

Snapshot — M5 Pro, 2026-05-24, hyperfine `--warmup 5 --runs 30 --shell=none`, native binaries via `karac build`, `rustc -O`, `clang -O3`, `go build`.

| Implementation | Wall time | User-CPU | Within-workload ratio |
|---|---|---|---|
| c    expand_around_center (clang -O3) | **31.1 ms ± 0.1 ms** | 29.6 ms | 0.85× of Kāra |
| **kāra expand_around_center (codegen)** | **36.7 ms ± 1.5 ms** | 35.1 ms | **1.00×** (baseline) |
| rust expand_around_center (rustc -O) | 36.7 ms ± 1.4 ms | 35.1 ms | 1.00× of Kāra |
| go   expand_around_center | 45.0 ms ± 1.1 ms | 43.0 ms | 1.23× of Kāra |

Inner-loop-bound shape: a tight two-pointer `chars[lo] == chars[hi]` byte-comparison loop running 12.5M times per `longest_palindrome` call, with the `Vec[char]` snapshot built once per outer iteration. **Kāra is at parity with rustc-O within σ** (36.7 ± 1.5 vs 36.7 ± 1.4 ms — every dispatched instruction matters on a workload this tight), and 1.23× faster than Go. C still leads by 1.18× — the residual is bounds-check overhead on indexed `Vec[char]` reads vs C's raw `int32_t*` pointer arithmetic. Bounds-check elision on monotonic indexed reads remains tracked as a karac follow-up; once it lands the residual closes.

An earlier snapshot of this kata (2026-05-18) read **1.10× faster than Rust** (35.7 vs 39.3 ms); subsequent rustc/LLVM drift on the M5 Pro tightened the Rust mirror back to parity. The headline story — "Kāra codegen tracks rustc step-for-step on inner-loop byte-comparison workloads once stdlib surface is in shape" — holds; the ordering between the two within σ is run-to-run noise.

### Runtime — long workloads (Python)

Same snapshot, hyperfine `--warmup 2 --runs 10 --shell=none`:

| Run | Mean ± σ |
|---|---|
| `py   expand_around_center` | 2.617 s ± 0.010 s |

Python is **71.3× slower** than Kāra codegen on this workload — the textbook "compiled vs interpreted" curve for O(n²) algorithms with tight inner loops, where CPython's per-iteration overhead dominates and there's no C-implemented stdlib type (like `dict`) to amortize the interpreter cost away.

### Compile elapsed (cold)

Snapshot — M5 Pro, 2026-05-24, hyperfine `--warmup 1 --runs 10 --shell=none` with `--prepare` deleting the artifact before each run:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `expand_around_center` | **60.9 ± 0.5 ms** | 98.8 ± 0.7 ms | 45.0 ± 0.5 ms |

`karac build` is **1.62× faster than `rustc -O`** on this file, sitting between clang (the floor for an LLVM-backed single-file compile) and rustc (which carries more frontend work per file). Multi-file projects (Go modules, Cargo) are deliberately excluded from this table — first-invocation `go build` and `cargo build` mix dep resolution + link and aren't comparable to a single-file `karac`/`rustc`/`clang` invocation.

### Binary size

| Implementation | Size |
|---|---|
| c    expand_around_center | 32.8 KiB |
| **kāra expand_around_center** | **49.1 KiB** |
| rust expand_around_center | 455.4 KiB |
| go   expand_around_center | 2434.4 KiB |

Kāra sits within ~1.5× of clang's binary — the cross-archive LTO + DCE pass strips runtime surface this workload doesn't reach (HTTP, JSON, tokio subgraph, `Map`, shared structs) cleanly. Rust's 455 KiB and Go's 2.4 MiB both reflect their respective runtimes (GC, panic-unwind tables, reflection) on every single-file binary.

### Runtime memory (peak, RSS)

| Implementation | Peak |
|---|---|
| c    expand_around_center | 1.1 MiB |
| **kāra expand_around_center (codegen)** | **1.3 MiB** |
| rust expand_around_center | 1.2 MiB |
| go   expand_around_center | 3.1 MiB |
| py   expand_around_center | 7.0 MiB |

At parity with C/Rust — the algorithm is O(1) extra space and the per-call `Vec[char]` snapshot allocates 5000 × 4 bytes = 20 KiB that's freed before the next outer iteration. Go's baseline includes the runtime + GC; Python's includes the CPython interpreter.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 expand_around_center.c | 2.6 MiB |
| karac build expand_around_center.kara | 8.9 MiB |
| rustc -O expand_around_center.rs | 30.0 MiB |

`karac` compiles this file in **~9 MiB peak** — between clang and rustc, with no algorithmic blowup signature. Go is omitted from the compile-memory row per BENCH.md — `go build`'s first invocation mixes module resolution + std-lib link and isn't comparable to a single-file invocation.

### Why this kata is in the harness

Longest Palindromic Substring is the canonical "tight inner-loop on a byte-comparison hot path" entry: an O(n²) two-pointer expand where every iteration is one indexed read + one equality test + two integer increments, repeated millions of times with no allocator, no map lookup, and no generic dispatch in the way. This is where Kāra's codegen has to compete with rustc step-for-step on instruction count and dispatch overhead — there's nowhere to hide behind stdlib quality. The current parity-with-rustc / 1.18× behind clang shape is the load-bearing measurement that "yes, on inner-loop algorithms once the stdlib surface is in shape, kara codegen is competitive with rustc."
