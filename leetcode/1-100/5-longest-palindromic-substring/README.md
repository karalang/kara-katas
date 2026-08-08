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


<!-- placement-caveat -->
**Measurement caveat — code placement.** This kata's runtime moves by up to **7%** with code placement alone: rebuilt with its machine code sitting at a different address, the same program, same compiler and same input runs that much faster or slower. That is wider than the **1.1%** margin against `rustc -O -C overflow-checks=on` quoted below, so read that comparison as a tie rather than as a result. Measured across four code placements against a same-binary control — see [`placement-spread.json`](../../../placement-spread.json) and [BENCHMARKS.md](../../../BENCHMARKS.md#code-placement-arm64).

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`500000`). Workload: expand_around_center n=5000, K=100; O(n²) (py timed separately).

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-07-28 (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 286.5 ms | 0.87× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 324.1 ms | 0.99× |
| **Kāra (codegen)** | 327.7 ms | 1.00× |
| Rust `-O` | 345.9 ms | 1.06× |
| Go | 419.9 ms | 1.28× |

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`, karac f80bb80b605f); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

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

> **Update 2026-07-28 — seq gap narrowed, not closed; an earlier claim here was wrong.** The karac inline-hint fix (ledger `B-2026-07-24-1`) was real: the inline-hint pass had been under-inlining the loop-hot `ref Vec[char]` helper (`expand`), leaving its bounds checks un-elided, and inlining it moved the seq lane **478.0 → 318.8 ms (−33%)** on this machine. But the claim that followed — "parity with Rust *and now leads C `clang -O3`*" — was read off a single x86 container run and does not hold on the canonical M5 host. Measured 2026-07-28: Kāra **leads `rustc -O` by 1.06×** and remains **1.11× behind C `clang -O3`**. Kāra is no longer last in this lane, but it does not lead C. The tables below are the current M5 standing; the 2026-06-05 pre-fix figures are quoted inline where they show the delta.
>
> One caveat this kata cannot yet discharge: it has **no equal-safety Rust twin** (`-C overflow-checks=on`). The Rust rows below are wrapping `rustc -O`, so beating them is a *stronger* result than beating checked Rust would be — but the comparison Kāra's default-checked arithmetic actually deserves is still missing here.

Per [`../../../BENCH.md`](../../../BENCH.md), the inner expand loop carries a strict `chars[lo] == chars[hi]` data dependency that gates the next step — so each `longest_palindrome` call stays serial. But the **outer K=100 loop is a sum-over-calls reduction**, and at K=100 the per-call O(n²) work clears the runtime auto-par gate, so karac's auto-par-on-reduction parallelizes the outer loop by default. The kata therefore has both a **seq lane** (codegen quality, `KARAC_AUTO_PAR=0`) and a **par lane** (auto-par vs hand-tuned). The seq Kāra binary is verified single-threaded via `nm -gU bench/target/expand_around_center_kara_seq | grep karac_par` (no auto-par symbols present) per BENCH.md § Implicit auto-par.

**Workload.** N = 5000 copies of `'a'` — the worst-case shape for expand-around-center: every one of the `2n − 1` centers expands all the way to the boundary, and no `chars[lo] != chars[hi]` check ever short-circuits the inner loop (≈n²/2 ≈ 12.5M character comparisons per call). K = 100 outer iterations. All four mirrors agree on the sink line `500000 = K × (best_start + best_length) = 100 × (0 + 5000)` before any timing runs — `bench.sh` fails loudly on mismatch.

The bench binaries use the `Vec[char]` snapshot shape (matching Rust's `Vec<char>`) for apples-to-apples comparison; the shipped [`expand_around_center.kara`](expand_around_center.kara) uses `s.bytes()` directly. A future bench refresh can switch both languages to byte-array equivalents — the headline numbers below would shift downward correspondingly.

| File | What it does |
|---|---|
| [`bench/expand_around_center.kara`](bench/expand_around_center.kara) | N=5000 single-char `'a'` input, K=100 outer iterations, `Vec[char]` snapshot + indexed access |
| [`bench/expand_around_center.rs`](bench/expand_around_center.rs) | Algorithmic mirror; `Vec<char>`; compiled with `rustc -O` |
| [`bench/expand_around_center.c`](bench/expand_around_center.c) | Algorithmic mirror; `int32_t*` snapshot; compiled with `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | Algorithmic mirror; `[]rune` snapshot; compiled with `go build` |
| [`bench/expand_around_center.py`](bench/expand_around_center.py) | Algorithmic mirror — same N, K, sink |

### Runtime — seq lane

Snapshot — M5 Pro (6P+12E), 2026-07-28, hyperfine `--warmup 5 --runs 30 --shell=none`, native binaries via `karac build` (`KARAC_AUTO_PAR=0`), `rustc -O`, `clang -O3`, `go build`. All four rows sit at 99.7–99.8% CPU, i.e. genuinely single-threaded.

| Implementation | Wall time | CPU | Within-workload ratio |
|---|---|---|---|
| c    expand_around_center (clang -O3) | **287.6 ms ± 1.9 ms** | 99.7% | 0.90× of Kāra |
| **kāra expand_around_center (codegen)** | **318.8 ms ± 19.1 ms** | 99.7% | **1.00×** (baseline) |
| rust expand_around_center (rustc -O) | 337.4 ms ± 12.4 ms | 99.7% | 1.06× of Kāra |
| go   expand_around_center | 420.0 ms ± 22.4 ms | 99.8% | 1.32× of Kāra |

Inner-loop-bound shape: a tight two-pointer `chars[lo] == chars[hi]` comparison loop running 12.5M times per `longest_palindrome` call, with the `Vec[char]` snapshot built once per outer iteration. This is exactly where karac's bounds-checked indexed `Vec[char]` reads cost the most against C's raw `int32_t*` arithmetic.

**Kāra is third of four here: 1.11× behind C, 1.06× ahead of `rustc -O`, 1.32× ahead of Go.** That is a real improvement on the 2026-06-05 pre-fix snapshot, where Kāra was **last** at 478.0 ms (1.67× behind C, 1.38× behind Rust, 1.15× behind Go). Inlining the loop-hot `expand` helper — so the caller's range facts reach it and the surviving half-bounds-checks fold away — bought **−33%** on this lane and moved Kāra past Rust and Go. It did not move Kāra past C, and an earlier revision of this README claimed otherwise on the strength of one x86 container run; see the update banner.

Note the error bars: Kāra's ±19.1 ms overlaps Rust's ±12.4 ms, so the 1.06× lead over `rustc -O` is the weakest claim in the table. The 1.11× deficit to C (±1.9 ms) is comfortably outside noise.

### Runtime — par lane (auto-par vs hand-tuned)

The outer K=100 loop is a sum-over-`longest_palindrome`-calls reduction; all four languages parallelize that *same* reduction across the M5 Pro's cores — the difference is what the programmer wrote. Per [BENCH.md](../../../BENCH.md)'s two-lane discipline these are *not* comparable to the single-thread seq rows above.

| | parallel code written | wall time | CPU | within-lane ratio |
|---|---|---|---|---|
| rust + rayon | `rayon` crate + `.into_par_iter()` | **27.8 ms ± 2.1 ms** | 1493% | 0.95× of Kāra |
| **kāra (auto-par)** | **none** — compiler parallelized the `for _` reduction | **29.3 ms ± 1.8 ms** | 1418% | **1.00×** (baseline) |
| c + pthreads | raw `pthread_create`/`join` + chunk + merge | 47.7 ms ± 2.5 ms | 672% | 1.63× of Kāra |
| go goroutines | chunk + `sync.WaitGroup` + merge | 69.6 ms ± 2.7 ms | 746% | 2.38× of Kāra |

**Kāra's auto-par — with zero parallel source — lands 1.63× ahead of the hand-written C+pthreads mirror and 2.38× ahead of Go's goroutine chunking, behind only hand-tuned rayon by 1.05×.** It is a **10.9× speedup** over Kāra's own seq binary (318.8 → 29.3 ms).

The gap to rayon (1.4 ms) sits inside the combined error bars, so treat auto-par and rayon as a tie on this workload rather than a rayon win. The C and Go mirrors are the more interesting rows: both are *hand-written* parallel code and both leave throughput on the table, drawing 672% and 746% CPU against Kāra's 1418% — their fixed chunking maps poorly onto the M5's 6P+12E asymmetry, while the runtime's work-stealing keeps every core fed. That is the case for auto-par in one line: not that it beats a tuned rayon pipeline, but that it beats what a competent programmer actually writes by hand.

### Runtime — long workloads (Python)

Same snapshot, hyperfine `--warmup 2 --runs 10 --shell=none`:

| Run | Mean ± σ |
|---|---|
| `py   expand_around_center` | 25.934 s ± 0.052 s |

Python is **54× slower** than the Kāra binary — the textbook "compiled vs interpreted" curve for O(n²) algorithms with tight inner loops, where CPython's per-iteration overhead dominates and there's no C-implemented stdlib type (like `dict`) to amortize the interpreter cost away.

### Compile elapsed (cold)

Snapshot — M5 Pro, 2026-07-28, hyperfine `--warmup 1 --runs 10 --shell=none` with `--prepare` deleting the artifact before each run:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `expand_around_center` | **99.7 ± 1.1 ms** | 94.5 ± 0.8 ms | 41.4 ± 0.3 ms |

**This claim has inverted.** Earlier revisions of this README read `karac build` at 78.9 ms against `rustc -O` at 111.4 ms and called it "1.41× faster than rustc". On 2026-07-28 `karac` is **1.06× slower** than `rustc -O` on this file: karac drifted 78.9 → 99.7 ms (+26%) while rustc moved 111.4 → 94.5 ms (−15%) on a byte-identical input. Part of that is toolchain churn on both sides — rustc is a different release — but the karac direction is worth a look rather than a shrug, and this kata is not the place to diagnose it. Compile-cost figures across the suite span three karac generations; `env.karac_build` (added 2026-07-28) fingerprints the binary so future rows are attributable.

Multi-file projects (Go modules, Cargo) are deliberately excluded from this table — first-invocation `go build` and `cargo build` mix dep resolution + link and aren't comparable to a single-file `karac`/`rustc`/`clang` invocation.

### Binary size

| Implementation | Size |
|---|---|
| c    expand_around_center | 32.8 KiB |
| **kāra expand_around_center** | **33.6 KiB** |
| rust expand_around_center | 455.4 KiB |
| go   expand_around_center | 2434.4 KiB |

**Back to within ~180 bytes of clang.** The binary spent part of 2026-06-05 at 49.3 KiB: karac's phase-9 contract-fault categorization (`8183f6c7`) made every panic site (bounds checks included) reference `karac_runtime_panic_prefix`, whose thread-local data dragged one page-aligned writable `__DATA` segment (16 KiB on Apple Silicon) into every binary — even contract-free ones. Katas [#6](../6-zigzag-conversion/README.md) and [#88](../88-merge-sorted-array/README.md) measured the same +16 KiB the same day, and on this kata the same panic-site change also cost **runtime** (§ Runtime). The same-day karac fix (`3f3b34a9`) folds the fault prefix to a static string when the program declares no contract, so the symbol — and its `__DATA` page — dead-strips; the evening re-bench read **33.4 KiB**, within ~640 bytes of the pre-regression artifact (2026-07-28: **33.6 KiB**, holding). There's history rhyming here: the `__TEXT,__jittmpl` segment re-scope (karac `e76f42b`, 2026-05-25) reclaimed a *different* 16 KiB page that had kept this kara at 49.1 KiB — this parity has now been won twice. The rest of the lean profile is unchanged: cross-archive LTO + DCE strips runtime surface this workload doesn't reach (HTTP, JSON, tokio subgraph, `Map`, shared structs). Rust's 455 KiB and Go's 2.4 MiB both reflect their respective runtimes (GC, panic-unwind tables, reflection) on every single-file binary.

### Runtime memory (peak, RSS)

| Implementation | Peak |
|---|---|
| c    expand_around_center | 1.0 MiB |
| **kāra expand_around_center (codegen)** | **1.2 MiB** |
| rust expand_around_center | 1.1 MiB |
| go   expand_around_center | 4.7 MiB |
| py   expand_around_center | 7.0 MiB |

At parity with C/Rust — the algorithm is O(1) extra space and the per-call `Vec[char]` snapshot allocates 5000 × 4 bytes = 20 KiB that's freed before the next outer iteration. Go's baseline includes the runtime + GC; Python's includes the CPython interpreter.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 expand_around_center.c | 2.5 MiB |
| karac build expand_around_center.kara | 24.7 MiB |
| rustc -O expand_around_center.rs | 30.0 MiB |

`karac` compiles this file in **24.7 MiB peak** — still between clang and rustc, but the gap to rustc has closed from 2.2× to 1.2×. The trend on this one file: 8.9 MiB (2026-05-24) → 13.5 MiB (2026-06-05) → 24.7 MiB (2026-07-28), i.e. +83% since June against a byte-identical input.

That is a **fixed-floor shift, not a regression on this kata**: across the 250-kata corpus karac's compile-memory peak now reads median 24.5 MiB (p25 21.1, p75 25.2), so this file sits exactly at the median, and the floor moved under everything at once. Kāra also remains below `rustc` on compile memory across the whole corpus — median 0.83×, p90 0.91×, and **not one of 243 comparable katas** puts karac above rustc. What did *not* survive the check is the older "11.5–12.3 MiB on peer single-file katas" figure quoted in earlier revisions; the peer band is now ~21–25 MiB.

Go is omitted from the compile-memory row per BENCH.md — `go build`'s first invocation mixes module resolution + std-lib link and isn't comparable to a single-file invocation.

### Why this kata is in the harness

Longest Palindromic Substring is the canonical "tight inner-loop on a byte-comparison hot path" entry: an O(n²) two-pointer expand where every iteration is one indexed read + one equality test + two integer increments, repeated millions of times with no allocator, no map lookup, and no generic dispatch in the way. This is where Kāra's codegen has to compete with rustc and clang step-for-step on instruction count — there's nowhere to hide behind stdlib quality. On the 2026-06-05 M5 Pro snapshot Kāra landed **last in the seq lane** (~1.67× behind C, ~1.38× behind Rust), with bounds-checked `Vec[char]` reads carrying most of the gap; inlining the loop-hot `expand` helper (ledger `B-2026-07-24-1`) **narrowed** it by 33%, moving Kāra past Rust and Go — but **not** past C, where a 1.11× deficit stands as of 2026-07-28. It was an honest "we're behind here, and the chart shows it" measurement that the harness then drove to a partial fix, and the kata is more useful for still showing the residue than it would be if the story ended in a clean win — paired with the par lane, where Kāra's free auto-parallelism of the outer reduction puts it well ahead of the hand-written C+pthreads and Go mirrors and level with hand-tuned rayon. The same inner-loop sensitivity also makes this kata a reliable canary for karac codegen regressions: a panic-site inline-threshold regression on 2026-06-05 was caught here the day it shipped, A/B-attributed within hours, and fixed (karac `3f3b34a9`).

---

**Bug ledger:** this kata surfaced `B-2026-06-12-7` — see the [`karac` bug ledger](../../../../kara/docs/bug-ledger.md).
