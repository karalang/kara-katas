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


## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`500000`). Workload: expand_around_center n=5000, K=100; O(n²) (py timed separately).

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O` | 808.4 ms | 1.00× |
| **Kāra (codegen)** | 809.3 ms | 1.00× |
| Go | 905.8 ms | 1.12× |
| C `clang -O3` | 1.10 s | 1.35× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

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

> **Update 2026-07-24 — per-core seq gap closed.** The M5 Pro snapshot below (2026-06-05) predates the karac inline-hint fix (ledger `B-2026-07-24-1`): the compiler-driven inline-hint pass was under-inlining a small loop-hot `ref Vec[char]` helper (`expand`), leaving its bounds checks un-elided. With the helper now inlined, the surviving half-bounds-checks fold away and the per-core seq lane reaches **parity with Rust** (and now leads C `clang -O3`) — see the fresh x86 container table above (`bench/results.container-x86.json`, 2026-07-24). The M5 Pro numbers and "Kāra last in the seq lane" framing that follow are the **pre-fix** historical snapshot, kept for provenance; treat the container table above as the current standing.

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

Snapshot — M5 Pro, 2026-06-05, hyperfine `--warmup 5 --runs 30 --shell=none`, native binaries via `karac build`, `rustc -O`, `clang -O3`, `go build`.

| Implementation | Wall time | User-CPU | Within-workload ratio |
|---|---|---|---|
| c    expand_around_center (clang -O3) | **286.9 ms ± 1.4 ms** | 285.0 ms | 0.60× of Kāra |
| rust expand_around_center (rustc -O) | 347.4 ms ± 29.2 ms | 345.0 ms | 0.73× of Kāra |
| go   expand_around_center | 415.3 ms ± 19.2 ms | 412.0 ms | 0.87× of Kāra |
| **kāra expand_around_center (codegen)** | **478.0 ms ± 6.5 ms** | 476.0 ms | **1.00×** (baseline) |

Inner-loop-bound shape: a tight two-pointer `chars[lo] == chars[hi]` byte-comparison loop running 12.5M times per `longest_palindrome` call, with the `Vec[char]` snapshot built once per outer iteration. **Kāra is slowest of the four in this seq lane** (478.0 ms; C 286.9 at 0.60×, Rust 347.4 at 0.73×, Go 415.3 at 0.87×) — roughly 1.67× behind C, 1.38× behind Rust, 1.15× behind Go on this re-bench. The inner expand loop is exactly the shape where karac's bounds-checked indexed `Vec[char]` reads cost the most against C's raw `int32_t*` arithmetic and against rustc's loop optimizer. **This gap has since been closed** (see the 2026-07-24 update banner above): the fix was inlining the loop-hot `expand` helper so the caller's range facts reach it and the surviving half-bounds-checks fold away — on the post-fix x86 container table above the seq lane now ties Rust and leads C. The M5 Pro row below is the pre-fix historical snapshot.

### Runtime — par lane (auto-par vs hand-tuned)

The outer K=100 loop is a sum-over-`longest_palindrome`-calls reduction; all four languages parallelize that *same* reduction across the M5 Pro's cores — the difference is what the programmer wrote. Per [BENCH.md](../../../BENCH.md)'s two-lane discipline these are *not* comparable to the single-thread seq rows above.

| | parallel code written | wall time | within-lane ratio |
|---|---|---|---|
| rust + rayon | `rayon` crate + `.into_par_iter()` | **27.1 ms ± 0.9 ms** | 0.61× of Kāra |
| **kāra (auto-par)** | **none** — compiler parallelized the `for _` reduction | **44.8 ms ± 1.3 ms** | **1.00×** (baseline) |
| c + pthreads | raw `pthread_create`/`join` + chunk + merge | 48.1 ms ± 2.6 ms | 1.07× of Kāra |
| go goroutines | chunk + `sync.WaitGroup` + merge | 69.5 ms ± 2.7 ms | 1.55× of Kāra |

**Kāra's auto-par — with zero parallel source — lands ahead of the hand-written C+pthreads mirror (1.07×) and Go's goroutine chunking (1.55×), behind only hand-tuned rayon (1.65× ahead).** It is a ~10.7× speedup over Kāra's own seq binary (478.0 → 44.8 ms). On this pre-fix M5 Pro snapshot the per-core codegen gap that put Kāra last in the seq lane was largely absorbed here by the free parallelism anyway; post-fix (see the update banner above) the seq lane itself reaches parity, so the par lane now stacks free parallelism on top of an already-competitive per-core binary.

### Runtime — long workloads (Python)

Same snapshot, hyperfine `--warmup 2 --runs 10 --shell=none`:

| Run | Mean ± σ |
|---|---|
| `py   expand_around_center` | 25.934 s ± 0.052 s |

Python is **54× slower** than the Kāra binary — the textbook "compiled vs interpreted" curve for O(n²) algorithms with tight inner loops, where CPython's per-iteration overhead dominates and there's no C-implemented stdlib type (like `dict`) to amortize the interpreter cost away.

### Compile elapsed (cold)

Snapshot — M5 Pro, 2026-06-05, hyperfine `--warmup 1 --runs 10 --shell=none` with `--prepare` deleting the artifact before each run:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `expand_around_center` | **78.9 ± 0.4 ms** | 111.4 ± 1.2 ms | 46.9 ± 0.4 ms |

`karac build` is **1.41× faster than `rustc -O`** on this file, sitting between clang (the floor for an LLVM-backed single-file compile) and rustc (which carries more frontend work per file). (The 2026-05-24 snapshot read karac at 60.9 ± 0.5 ms; the drift is the recurring reinstall-day band — today's karac reads ~75–86 ms across the suite — and rustc/clang also moved on byte-identical inputs, so part of the spread is environment.) Multi-file projects (Go modules, Cargo) are deliberately excluded from this table — first-invocation `go build` and `cargo build` mix dep resolution + link and aren't comparable to a single-file `karac`/`rustc`/`clang` invocation.

### Binary size

| Implementation | Size |
|---|---|
| c    expand_around_center | 32.8 KiB |
| **kāra expand_around_center** | **33.4 KiB** |
| rust expand_around_center | 455.4 KiB |
| go   expand_around_center | 2434.4 KiB |

**Back to within ~180 bytes of clang.** The binary spent part of 2026-06-05 at 49.3 KiB: karac's phase-9 contract-fault categorization (`8183f6c7`) made every panic site (bounds checks included) reference `karac_runtime_panic_prefix`, whose thread-local data dragged one page-aligned writable `__DATA` segment (16 KiB on Apple Silicon) into every binary — even contract-free ones. Katas [#6](../6-zigzag-conversion/README.md) and [#88](../88-merge-sorted-array/README.md) measured the same +16 KiB the same day, and on this kata the same panic-site change also cost **runtime** (§ Runtime). The same-day karac fix (`3f3b34a9`) folds the fault prefix to a static string when the program declares no contract, so the symbol — and its `__DATA` page — dead-strips; the evening re-bench reads **33.4 KiB**, within ~640 bytes of the pre-regression artifact. There's history rhyming here: the `__TEXT,__jittmpl` segment re-scope (karac `e76f42b`, 2026-05-25) reclaimed a *different* 16 KiB page that had kept this kara at 49.1 KiB — this parity has now been won twice. The rest of the lean profile is unchanged: cross-archive LTO + DCE strips runtime surface this workload doesn't reach (HTTP, JSON, tokio subgraph, `Map`, shared structs). Rust's 455 KiB and Go's 2.4 MiB both reflect their respective runtimes (GC, panic-unwind tables, reflection) on every single-file binary.

### Runtime memory (peak, RSS)

| Implementation | Peak |
|---|---|
| c    expand_around_center | 1.0 MiB |
| **kāra expand_around_center (codegen)** | **1.2 MiB** |
| rust expand_around_center | 1.1 MiB |
| go   expand_around_center | 4.9 MiB |
| py   expand_around_center | 7.0 MiB |

At parity with C/Rust — the algorithm is O(1) extra space and the per-call `Vec[char]` snapshot allocates 5000 × 4 bytes = 20 KiB that's freed before the next outer iteration. Go's baseline includes the runtime + GC; Python's includes the CPython interpreter.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 expand_around_center.c | 2.6 MiB |
| karac build expand_around_center.kara | 13.5 MiB |
| rustc -O expand_around_center.rs | 30.0 MiB |

`karac` compiles this file in **~14 MiB peak** — between clang and rustc, with no algorithmic blowup signature. (Was 8.9 MiB at the 2026-05-24 snapshot; the +2.8 MiB matches the probe-confirmed fixed-floor karac growth measured across the suite — today's karac reads 11.5–12.3 MiB on peer single-file katas — not a workload-proportional regression.) Go is omitted from the compile-memory row per BENCH.md — `go build`'s first invocation mixes module resolution + std-lib link and isn't comparable to a single-file invocation.

### Why this kata is in the harness

Longest Palindromic Substring is the canonical "tight inner-loop on a byte-comparison hot path" entry: an O(n²) two-pointer expand where every iteration is one indexed read + one equality test + two integer increments, repeated millions of times with no allocator, no map lookup, and no generic dispatch in the way. This is where Kāra's codegen has to compete with rustc and clang step-for-step on instruction count — there's nowhere to hide behind stdlib quality. On the 2026-06-05 M5 Pro snapshot Kāra landed **last in the seq lane** (~1.67× behind C, ~1.38× behind Rust), with bounds-checked `Vec[char]` reads carrying most of the gap; that gap has **since been closed** by inlining the loop-hot `expand` helper (ledger `B-2026-07-24-1`, see the update banner above), and the post-fix x86 container table now shows the seq lane at parity with Rust and ahead of C. It was an honest "we're behind here, and the chart shows it" measurement that the harness then drove to a fix — paired with the par lane, where Kāra's free auto-parallelism of the outer reduction puts it ahead of the hand-written C+pthreads and Go mirrors and behind only hand-tuned rayon. The same inner-loop sensitivity also makes this kata a reliable canary for karac codegen regressions: a panic-site inline-threshold regression on 2026-06-05 was caught here the day it shipped, A/B-attributed within hours, and fixed (karac `3f3b34a9`).

---

**Bug ledger:** this kata surfaced `B-2026-06-12-7` — see the [`karac` bug ledger](../../../../kara/docs/bug-ledger.md).
