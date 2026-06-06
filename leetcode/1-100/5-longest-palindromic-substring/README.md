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

Snapshot — M5 Pro, 2026-06-05, hyperfine `--warmup 5 --runs 30 --shell=none`, native binaries via `karac build`, `rustc -O`, `clang -O3`, `go build`.

| Implementation | Wall time | User-CPU | Within-workload ratio |
|---|---|---|---|
| c    expand_around_center (clang -O3) | **31.8 ms ± 0.6 ms** | 30.6 ms | 0.86× of Kāra |
| rust expand_around_center (rustc -O) | 39.4 ms ± 2.9 ms | 38.0 ms | 1.06× of Kāra |
| go   expand_around_center | 46.9 ms ± 2.7 ms | 45.3 ms | 1.26× of Kāra |
| **kāra expand_around_center (codegen)** | **37.2 ms ± 3.3 ms** | 35.9 ms | **1.00×** (baseline) |

**Regression caught, fixed, and re-measured the same day (2026-06-05).** The mid-day re-bench read kāra at 52.0 ± 2.8 ms while the Rust and C binaries were byte-identical to the May artifacts and flat — a live karac regression this kata caught the day it shipped. Same-day A/B pinned it (pre-regression backup karac: 39.9 ± 1.9 ms vs regressed: 53.6 ± 1.5 ms = 1.34×) and the [`get_unchecked` sibling](bench/expand_around_center_unchecked.kara) — no bounds checks, hence no panic sites on the hot path — was flat across both karacs, isolating it to panic-site-bearing code. Root cause (karac `3f3b34a9`, the fix): the 2026-05-31 fault-prefix (`8183f6c7`) + panic-location (`290e454c`) changes grew the panic-site `printf` from 1 operand to 7, pushing the `expand` helper past LLVM's O2 **inline threshold** — the un-inlined copy re-ran two loop-invariant guards on every one of the 2 × 125M inner-loop iterations. karac now outlines each panic body into a per-site `cold`+`noinline` function so a panic landing pad costs the enclosing function a single zero-operand call; `expand` inlines again and this evening's re-bench reads **37.2 ± 3.3 ms — ahead of rustc (39.4 ± 2.9) within σ**, the kata's best measurement to date (2026-05-24 snapshot: 36.7 vs 36.7 parity).

Inner-loop-bound shape: a tight two-pointer `chars[lo] == chars[hi]` byte-comparison loop running 12.5M times per `longest_palindrome` call, with the `Vec[char]` snapshot built once per outer iteration. The story — "Kāra codegen tracks rustc step-for-step on inner-loop byte-comparison workloads once stdlib surface is in shape" — holds; C's lead is bounds-check overhead on indexed `Vec[char]` reads vs raw `int32_t*` arithmetic, with dominator-aware bounds-check elision tracked as the karac follow-up that closes it.

### Runtime — long workloads (Python)

Same snapshot, hyperfine `--warmup 2 --runs 10 --shell=none`:

| Run | Mean ± σ |
|---|---|
| `py   expand_around_center` | 2.674 s ± 0.010 s |

Python is **72× slower** than the Kāra binary — the textbook "compiled vs interpreted" curve for O(n²) algorithms with tight inner loops, where CPython's per-iteration overhead dominates and there's no C-implemented stdlib type (like `dict`) to amortize the interpreter cost away.

### Compile elapsed (cold)

Snapshot — M5 Pro, 2026-06-05, hyperfine `--warmup 1 --runs 10 --shell=none` with `--prepare` deleting the artifact before each run:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `expand_around_center` | **76.1 ± 2.5 ms** | 98.7 ± 1.4 ms | 45.8 ± 1.1 ms |

`karac build` is **1.30× faster than `rustc -O`** on this file, sitting between clang (the floor for an LLVM-backed single-file compile) and rustc (which carries more frontend work per file). (The 2026-05-24 snapshot read karac at 60.9 ± 0.5 ms; the drift is the recurring reinstall-day band — today's karac reads ~75–86 ms across the suite — and rustc/clang also moved on byte-identical inputs, so part of the spread is environment.) Multi-file projects (Go modules, Cargo) are deliberately excluded from this table — first-invocation `go build` and `cargo build` mix dep resolution + link and aren't comparable to a single-file `karac`/`rustc`/`clang` invocation.

### Binary size

| Implementation | Size |
|---|---|
| c    expand_around_center | 32.8 KiB |
| **kāra expand_around_center** | **33.0 KiB** |
| rust expand_around_center | 455.4 KiB |
| go   expand_around_center | 2434.4 KiB |

**Back to within ~180 bytes of clang.** The binary spent part of 2026-06-05 at 49.3 KiB: karac's phase-9 contract-fault categorization (`8183f6c7`) made every panic site (bounds checks included) reference `karac_runtime_panic_prefix`, whose thread-local data dragged one page-aligned writable `__DATA` segment (16 KiB on Apple Silicon) into every binary — even contract-free ones. Katas [#6](../6-zigzag-conversion/README.md) and [#88](../88-merge-sorted-array/README.md) measured the same +16 KiB the same day, and on this kata the same panic-site change also cost **runtime** (§ Runtime). The same-day karac fix (`3f3b34a9`) folds the fault prefix to a static string when the program declares no contract, so the symbol — and its `__DATA` page — dead-strips; the evening re-bench reads **33.0 KiB**, byte-count parity with the pre-regression artifact. There's history rhyming here: the `__TEXT,__jittmpl` segment re-scope (karac `e76f42b`, 2026-05-25) reclaimed a *different* 16 KiB page that had kept this kara at 49.1 KiB — this parity has now been won twice. The rest of the lean profile is unchanged: cross-archive LTO + DCE strips runtime surface this workload doesn't reach (HTTP, JSON, tokio subgraph, `Map`, shared structs). Rust's 455 KiB and Go's 2.4 MiB both reflect their respective runtimes (GC, panic-unwind tables, reflection) on every single-file binary.

### Runtime memory (peak, RSS)

| Implementation | Peak |
|---|---|
| c    expand_around_center | 1.0 MiB |
| **kāra expand_around_center (codegen)** | **1.2 MiB** |
| rust expand_around_center | 1.1 MiB |
| go   expand_around_center | 3.0 MiB |
| py   expand_around_center | 6.8 MiB |

At parity with C/Rust — the algorithm is O(1) extra space and the per-call `Vec[char]` snapshot allocates 5000 × 4 bytes = 20 KiB that's freed before the next outer iteration. Go's baseline includes the runtime + GC; Python's includes the CPython interpreter.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 expand_around_center.c | 2.5 MiB |
| karac build expand_around_center.kara | 11.6 MiB |
| rustc -O expand_around_center.rs | 29.9 MiB |

`karac` compiles this file in **~12 MiB peak** — between clang and rustc, with no algorithmic blowup signature. (Was 8.9 MiB at the 2026-05-24 snapshot; the +2.8 MiB matches the probe-confirmed fixed-floor karac growth measured across the suite — today's karac reads 11.5–12.3 MiB on peer single-file katas — not a workload-proportional regression.) Go is omitted from the compile-memory row per BENCH.md — `go build`'s first invocation mixes module resolution + std-lib link and isn't comparable to a single-file invocation.

### Why this kata is in the harness

Longest Palindromic Substring is the canonical "tight inner-loop on a byte-comparison hot path" entry: an O(n²) two-pointer expand where every iteration is one indexed read + one equality test + two integer increments, repeated millions of times with no allocator, no map lookup, and no generic dispatch in the way. This is where Kāra's codegen has to compete with rustc step-for-step on instruction count and dispatch overhead — there's nowhere to hide behind stdlib quality. The parity-with-rustc / ~1.2×-behind-clang shape is the load-bearing measurement that "yes, on inner-loop algorithms once the stdlib surface is in shape, kara codegen is competitive with rustc" — and that same sensitivity is what made this kata the canary that caught the 2026-06-05 panic-site runtime regression (§ Runtime) the day it shipped: re-benched at 1.39× of rustc mid-day, A/B-attributed within hours, karac fixed (`3f3b34a9` — panic bodies outlined so landing pads stop bloating the inline cost of hot functions), and re-measured to its best-ever number (ahead of rustc within σ) the same evening. One bench cycle, full loop: detect → attribute → fix → verify.
