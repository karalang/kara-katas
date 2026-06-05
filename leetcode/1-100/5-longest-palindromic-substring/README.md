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
| c    expand_around_center (clang -O3) | **30.6 ms ± 0.2 ms** | 29.4 ms | 0.59× of Kāra |
| rust expand_around_center (rustc -O) | 37.3 ms ± 2.4 ms | 36.0 ms | 0.72× of Kāra |
| go   expand_around_center | 45.3 ms ± 2.4 ms | 43.6 ms | 0.87× of Kāra |
| **kāra expand_around_center (codegen)** | **52.0 ms ± 2.8 ms** | 50.6 ms | **1.00×** (baseline) |

**The kāra row is carrying an active, attributed karac regression — these are not the codegen's true numbers.** The 2026-05-24 snapshot had kāra at **parity with rustc within σ** (36.7 ± 1.5 vs 36.7 ± 1.4 ms) and 1.23× ahead of Go; today's rebuild under the post-`a3acedaf` karac reads 52.0 ms while the Rust and C binaries are **byte-identical to the May artifacts and flat** (37.3 / 30.6 ms), pinning the move on the kāra binary alone. Same-day A/B on this exact source: the pre-`a3acedaf` backup karac builds a binary that runs **39.9 ± 1.9 ms** vs the current karac's 53.6 ± 1.5 ms (1.34×). Control: the [`get_unchecked` sibling](bench/expand_around_center_unchecked.kara) — same loop, no bounds checks, hence no panic sites on the hot path — is **flat across the same two karacs** (39.5 ± 2.0 vs 37.5 ± 2.9 ms). The regression rides exclusively on panic-site-bearing code: karac's phase-9 contract-fault categorization (`8183f6c7`) makes every bounds-check failure block call `karac_runtime_panic_prefix()` at runtime, degrading codegen around the 2 × 125M bounds-checked reads in the inner loop (~0.2 cycles/check). Filed karac-side with the binary-size instance of the same defect (see § Binary size); when the fix lands this kata should snap back to ~40 ms rustc parity.

Inner-loop-bound shape: a tight two-pointer `chars[lo] == chars[hi]` byte-comparison loop running 12.5M times per `longest_palindrome` call, with the `Vec[char]` snapshot built once per outer iteration. The underlying story — "Kāra codegen tracks rustc step-for-step on inner-loop byte-comparison workloads once stdlib surface is in shape" — is unchanged (the pre-regression karac still measures it, same day, same machine); C's lead is bounds-check overhead on indexed `Vec[char]` reads vs raw `int32_t*` arithmetic, with dominator-aware bounds-check elision tracked as the karac follow-up that closes it.

### Runtime — long workloads (Python)

Same snapshot, hyperfine `--warmup 2 --runs 10 --shell=none`:

| Run | Mean ± σ |
|---|---|
| `py   expand_around_center` | 2.677 s ± 0.040 s |

Python is **51× slower** than today's regression-carrying Kāra binary (~67× against the pre-regression ~40 ms estimate) — the textbook "compiled vs interpreted" curve for O(n²) algorithms with tight inner loops, where CPython's per-iteration overhead dominates and there's no C-implemented stdlib type (like `dict`) to amortize the interpreter cost away.

### Compile elapsed (cold)

Snapshot — M5 Pro, 2026-06-05, hyperfine `--warmup 1 --runs 10 --shell=none` with `--prepare` deleting the artifact before each run:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `expand_around_center` | **86.1 ± 3.7 ms** | 107.6 ± 5.2 ms | 47.5 ± 0.7 ms |

`karac build` is **1.25× faster than `rustc -O`** on this file, sitting between clang (the floor for an LLVM-backed single-file compile) and rustc (which carries more frontend work per file). (The 2026-05-24 snapshot read karac at 60.9 ± 0.5 ms; the drift is the recurring reinstall-day band — today's karac reads 75–86 ms across the suite — and rustc/clang also moved +9/+2.5 ms on byte-identical inputs, so part of today's spread is environment.) Multi-file projects (Go modules, Cargo) are deliberately excluded from this table — first-invocation `go build` and `cargo build` mix dep resolution + link and aren't comparable to a single-file `karac`/`rustc`/`clang` invocation.

### Binary size

| Implementation | Size |
|---|---|
| c    expand_around_center | 32.8 KiB |
| **kāra expand_around_center** | **49.3 KiB** |
| rust expand_around_center | 455.4 KiB |
| go   expand_around_center | 2434.4 KiB |

**The binary was 33.0 KiB — within ~200 bytes of clang's — until 2026-06-05; it now reads 49.3 KiB.** The +16.3 KiB is the same karac-side regression katas [#6](../6-zigzag-conversion/README.md) and [#88](../88-merge-sorted-array/README.md) measured the same day: karac's phase-9 contract-fault categorization (`8183f6c7`) makes every panic site (bounds checks included) reference `karac_runtime_panic_prefix`, whose thread-local data drags one page-aligned writable `__DATA` segment (16 KiB on Apple Silicon) into every binary — even contract-free ones. On this kata the same defect also costs **runtime** (see § Runtime — the 1.34× inner-loop regression rides on the identical panic-site change; the `get_unchecked` sibling carries neither the page nor the slowdown). Filed karac-side with a fix pointer; when it lands this kata returns to clang parity. There's history rhyming here: the `__TEXT,__jittmpl` segment re-scope (karac `e76f42b`, 2026-05-25) reclaimed a *different* 16 KiB page that had kept this kara at 49.1 KiB — the parity story was won once already. The rest of the lean profile is unchanged: cross-archive LTO + DCE strips runtime surface this workload doesn't reach (HTTP, JSON, tokio subgraph, `Map`, shared structs). Rust's 455 KiB and Go's 2.4 MiB both reflect their respective runtimes (GC, panic-unwind tables, reflection) on every single-file binary.

### Runtime memory (peak, RSS)

| Implementation | Peak |
|---|---|
| c    expand_around_center | 1.0 MiB |
| **kāra expand_around_center (codegen)** | **1.2 MiB** |
| rust expand_around_center | 1.1 MiB |
| go   expand_around_center | 3.0 MiB |
| py   expand_around_center | 6.9 MiB |

At parity with C/Rust — the algorithm is O(1) extra space and the per-call `Vec[char]` snapshot allocates 5000 × 4 bytes = 20 KiB that's freed before the next outer iteration. Go's baseline includes the runtime + GC; Python's includes the CPython interpreter.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 expand_around_center.c | 2.5 MiB |
| karac build expand_around_center.kara | 11.7 MiB |
| rustc -O expand_around_center.rs | 30.0 MiB |

`karac` compiles this file in **~12 MiB peak** — between clang and rustc, with no algorithmic blowup signature. (Was 8.9 MiB at the 2026-05-24 snapshot; the +2.8 MiB matches the probe-confirmed fixed-floor karac growth measured across the suite — today's karac reads 11.5–12.3 MiB on peer single-file katas — not a workload-proportional regression.) Go is omitted from the compile-memory row per BENCH.md — `go build`'s first invocation mixes module resolution + std-lib link and isn't comparable to a single-file invocation.

### Why this kata is in the harness

Longest Palindromic Substring is the canonical "tight inner-loop on a byte-comparison hot path" entry: an O(n²) two-pointer expand where every iteration is one indexed read + one equality test + two integer increments, repeated millions of times with no allocator, no map lookup, and no generic dispatch in the way. This is where Kāra's codegen has to compete with rustc step-for-step on instruction count and dispatch overhead — there's nowhere to hide behind stdlib quality. The parity-with-rustc / ~1.2×-behind-clang shape is the load-bearing measurement that "yes, on inner-loop algorithms once the stdlib surface is in shape, kara codegen is competitive with rustc" — and that same sensitivity is what made this kata the canary that caught the 2026-06-05 panic-site runtime regression (§ Runtime) the day it shipped: the headline number is temporarily 1.39× of rustc until the filed karac fix lands, with the pre-regression karac still measuring parity on the same day and machine.
