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

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`500000`). Workload: expand_around_center n=5000, K=100; O(n²) (py timed separately). Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`expand_around_center.{kara,rs,c}`, `go-seq/main.go`, plus the par-lane mirrors `expand_around_center_par.c`, `go-par/`, `rayon/`). Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

Snapshot for every table below: Apple M5 Pro (6P+12E), karac `0.1.0-dev.13686+g04628b0eb` (build `5a437b660b0f`; the v2/MIR backend, which replaced the legacy backend on 22 October), `rustc 1.95.0`, Apple clang 21.0.0, go 1.26.3, hyperfine 1.20.0, measured 2026-10-29 (UTC). Source of truth: [`bench/results.json`](bench/results.json); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats.

> **Re-bench 2026-10-29 — what moved.** This kata regressed on the MIR backend; every non-Kāra row is flat to within 2%.
>
> - **Seq runtime: Kāra 327.7 → 410.7 ms (+25%)** while C (287.9 ms), `rustc -O` (351.3 ms), equal-safety Rust (321.2 ms) and Go (421.0 ms) did not move. Kāra went from beating `rustc -O` (0.95× of Rust's time) to **1.17× behind `rustc -O`, 1.28× behind equal-safety Rust and 1.43× behind C**. This is a real regression, not noise: a matched same-commit instruction-count A/B attributes it to the backend — the MIR backend executes **13.80 G instructions vs legacy's 11.28 G (+22%), cycles +45%**. Tracked as `B-2026-10-28-33`.
> - **Par runtime: Kāra auto-par 28.7 → 38.2 ms (+33%)** — the same seq-path loss carried into each parallel worker. Rayon (26.9 ms), C+pthreads (46.9 ms) and Go (69.9 ms) are flat.
> - **Binary size: +302 KB on the seq binary (33.6 → 329.1 KiB) and +84 KB on the par binary** — a regression, tracked as `B-2026-10-28-36`.
> - **Compile cost: `karac build` 97.5 → 182.4 ms and 24.3 → 69.3 MiB peak**, with `rustc` and `clang` flat — a regression, tracked as `B-2026-10-28-37`.
>
> The earlier "seq gap narrowed" story (the `B-2026-07-24-1` inline-hint fix that moved this lane 478.0 → 318.8 ms) is history; the numbers below supersede every earlier revision of this section.

Per [`../../../BENCH.md`](../../../BENCH.md), the inner expand loop carries a strict `chars[lo] == chars[hi]` data dependency that gates the next step — so each `longest_palindrome` call stays serial. But the **outer K=100 loop is a sum-over-calls reduction**, and at K=100 the per-call O(n²) work clears the runtime auto-par gate, so karac parallelizes the outer loop in the par-lane build. The kata therefore has both a **seq lane** (codegen quality, `KARAC_AUTO_PAR=0`) and a **par lane** (auto-par vs hand-tuned). On the MIR backend the auto-par entry point is `karac_mir_task_spawn` (the legacy `karac_par_reduce` symbol no longer exists), so the seq Kāra binary is verified single-threaded via `nm -gU bench/target/expand_around_center_kara_seq | grep karac_mir_task_spawn` returning nothing, per BENCH.md § Implicit auto-par.

**Workload.** N = 5000 copies of `'a'` — the worst-case shape for expand-around-center: every one of the `2n − 1` centers expands all the way to the boundary, and no `chars[lo] != chars[hi]` check ever short-circuits the inner loop (≈n²/2 ≈ 12.5M character comparisons per call). K = 100 outer iterations. All mirrors agree on the sink line `500000 = K × (best_start + best_length) = 100 × (0 + 5000)` before any timing runs — `bench.sh` fails loudly on mismatch.

The bench binaries use the `Vec[char]` snapshot shape (matching Rust's `Vec<char>`) for apples-to-apples comparison; the shipped [`expand_around_center.kara`](expand_around_center.kara) uses `s.bytes()` directly.

| File | What it does |
|---|---|
| [`bench/expand_around_center.kara`](bench/expand_around_center.kara) | N=5000 single-char `'a'` input, K=100 outer iterations, `Vec[char]` snapshot + indexed access |
| [`bench/expand_around_center.rs`](bench/expand_around_center.rs) | Algorithmic mirror; `Vec<char>`; compiled with `rustc -O` and, for the equal-safety row, `rustc -O -C overflow-checks=on` |
| [`bench/expand_around_center.c`](bench/expand_around_center.c) | Algorithmic mirror; `int32_t*` snapshot; compiled with `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | Algorithmic mirror; `[]rune` snapshot; compiled with `go build` |
| [`bench/expand_around_center.py`](bench/expand_around_center.py) | Algorithmic mirror — same N, K, sink |

### Runtime — seq lane

hyperfine, 30 runs, `--shell=none`, native binaries via `karac build` (`KARAC_AUTO_PAR=0`), `rustc -O`, `rustc -O -C overflow-checks=on`, `clang -O3`, `go build`. Every row sits at 99.7–99.8% CPU, i.e. genuinely single-threaded.

| Implementation | Wall time | CPU | Within-workload ratio |
|---|---|---|---|
| c    expand_around_center (clang -O3) | **287.9 ms ± 0.6 ms** | 99.7% | 0.70× of Kāra |
| rust expand_around_center (rustc -O -C overflow-checks=on, equal-safety) | 321.2 ms ± 23.7 ms | 99.7% | 0.78× of Kāra |
| rust expand_around_center (rustc -O) | 351.3 ms ± 19.7 ms | 99.7% | 0.86× of Kāra |
| **kāra expand_around_center (codegen)** | **410.7 ms ± 17.4 ms** | 99.7% | **1.00×** (baseline) |
| go   expand_around_center | 421.0 ms ± 27.5 ms | 99.8% | 1.03× of Kāra |

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`.

**Kāra is fourth of five here: 1.43× behind C, 1.28× behind equal-safety Rust, 1.17× behind `rustc -O`, and ahead of Go only by 1.03×** — inside Go's ±27.5 ms error bar, so call Kāra and Go a tie. On the previous (2026-07-28, legacy-backend) snapshot Kāra beat `rustc -O` at 327.7 ms; the +25% since then is the MIR-backend regression `B-2026-10-28-33`, attributed by instruction count (13.80 G vs 11.28 G, +22%) rather than by wall time.

Inner-loop-bound shape: a tight two-pointer `chars[lo] == chars[hi]` comparison loop running 12.5M times per `longest_palindrome` call, with the `Vec[char]` snapshot built once per outer iteration. This is exactly where karac's bounds-checked indexed `Vec[char]` reads cost the most against C's raw `int32_t*` arithmetic, and where any extra instruction per inner iteration in the backend's output shows up undiluted.

### Runtime — par lane (auto-par vs hand-tuned)

The outer K=100 loop is a sum-over-`longest_palindrome`-calls reduction; all four languages parallelize that *same* reduction across the M5 Pro's cores — the difference is what the programmer wrote. Per [BENCH.md](../../../BENCH.md)'s two-lane discipline these are *not* comparable to the single-thread seq rows above.

| | parallel code written | wall time | CPU | within-lane ratio |
|---|---|---|---|---|
| rust + rayon | `rayon` crate + `.into_par_iter()` | **26.9 ms ± 1.0 ms** | 1557% | 0.70× of Kāra |
| **kāra (auto-par)** | **none** — compiler parallelized the `for _` reduction | **38.2 ms ± 1.1 ms** | 1366% | **1.00×** (baseline) |
| c + pthreads | raw `pthread_create`/`join` + chunk + merge | 46.9 ms ± 1.1 ms | 686% | 1.23× of Kāra |
| go goroutines | chunk + `sync.WaitGroup` + merge | 69.9 ms ± 2.4 ms | 745% | 1.83× of Kāra |

**Kāra's auto-par — with zero parallel source — still lands 1.23× ahead of the hand-written C+pthreads mirror and 1.83× ahead of Go's goroutine chunking, but now trails hand-tuned rayon by 1.42×.** It is a **10.7× speedup** over Kāra's own seq binary (410.7 → 38.2 ms). The rayon gap (11.3 ms) is well outside the combined error bars, so it is a rayon win, not a tie; it is the seq-lane regression `B-2026-10-28-33` multiplied across workers, not a scheduling loss — Kāra still draws 1366% CPU against C's 686% and Go's 745%, whose fixed chunking maps poorly onto the M5's 6P+12E asymmetry.

### Runtime — long workloads (Python)

The 2026-10-29 re-run did not time the Python lane (`bench/results.json` has no `py` row), so no Python number is quoted here; the earlier 25.9 s figure has been dropped rather than kept stale. Re-run with `KARA_BENCH_INCLUDE_PY=1` to restore it.

### Compile elapsed (cold)

hyperfine, 10 runs, `--shell=none`, with `--prepare` deleting the artifact before each run:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `expand_around_center` | **182.4 ± 1.5 ms** | 96.6 ± 0.6 ms | 42.9 ± 0.6 ms |

`karac build` is **1.89× slower than `rustc -O`** on this file. On the 2026-07-28 snapshot it read 97.5 ms against rustc's 92.9 ms; karac nearly doubled on a byte-identical input while rustc and clang moved by under 4%. That is a karac regression, tracked as `B-2026-10-28-37`.

Multi-file projects (Go modules, Cargo) are deliberately excluded from this table — first-invocation `go build` and `cargo build` mix dep resolution + link and aren't comparable to a single-file `karac`/`rustc`/`clang` invocation.

### Binary size

Seq-lane binaries:

| Implementation | Size |
|---|---|
| c    expand_around_center | 32.8 KiB |
| **kāra expand_around_center** | **329.1 KiB** |
| rust expand_around_center | 455.4 KiB |
| go   expand_around_center | 2434.4 KiB |

**The near-parity with clang is gone.** The Kāra binary held at 33.6 KiB through 2026-07-28 (within ~860 bytes of C, after the `3f3b34a9` fix for the panic-prefix `__DATA` page); on the MIR backend it is 329.1 KiB, +302 KB, and the auto-par binary grew +84 KB to 394.5 KiB. Kāra is still smaller than Rust and Go, but the lean-profile dead-stripping this kata used to demonstrate no longer happens. Tracked as `B-2026-10-28-36`. Rust's 455 KiB and Go's 2.4 MiB reflect their respective runtimes (GC, panic-unwind tables, reflection) on every single-file binary.

### Runtime memory (peak, RSS)

| Implementation | Peak |
|---|---|
| c    expand_around_center | 1.0 MiB |
| **kāra expand_around_center (codegen)** | **1.3 MiB** |
| rust expand_around_center | 1.1 MiB |
| go   expand_around_center | 4.7 MiB |

At parity with C/Rust — the algorithm is O(1) extra space and the per-call `Vec[char]` snapshot allocates 5000 × 4 bytes = 20 KiB that's freed before the next outer iteration. Go's baseline includes the runtime + GC. (No Python row: the Python lane was not run on 2026-10-29.)

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 expand_around_center.c | 2.6 MiB |
| rustc -O expand_around_center.rs | 30.0 MiB |
| karac build expand_around_center.kara | 69.3 MiB |

`karac` now compiles this file in **69.3 MiB peak, 2.31× rustc's 30.0 MiB** — up from 24.3 MiB on the 2026-07-28 snapshot, when karac sat below rustc. Earlier revisions noted that no comparable kata in the corpus put karac above rustc on compile memory; that no longer holds for this file, and the corpus-wide figures quoted then predate the MIR backend. Part of the same compile-cost regression, `B-2026-10-28-37`.

Go is omitted from the compile-memory row per BENCH.md — `go build`'s first invocation mixes module resolution + std-lib link and isn't comparable to a single-file invocation.

### Why this kata is in the harness

Longest Palindromic Substring is the canonical "tight inner-loop on a byte-comparison hot path" entry: an O(n²) two-pointer expand where every iteration is one indexed read + one equality test + two integer increments, repeated millions of times with no allocator, no map lookup, and no generic dispatch in the way. This is where Kāra's codegen has to compete with rustc and clang step-for-step on instruction count — there's nowhere to hide behind stdlib quality. That makes it a reliable canary for karac codegen regressions, and it has now caught three: a panic-site inline-threshold regression on 2026-06-05 (fixed in karac `3f3b34a9`), the under-inlined `expand` helper (`B-2026-07-24-1`, −33% when fixed), and the MIR-backend instruction-count regression `B-2026-10-28-33` that this re-bench surfaced. Paired with the par lane, it also shows the case for auto-par: zero parallel source still beats the hand-written C+pthreads and Go mirrors.

---

**Bug ledger:** this kata surfaced `B-2026-06-12-7` — see the [`karac` bug ledger](../../../../kara/docs/bugs-v2.md).
