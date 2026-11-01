# 72. Edit Distance

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String · Dynamic Programming &nbsp;·&nbsp; **Source:** [leetcode.com/problems/edit-distance](https://leetcode.com/problems/edit-distance/)

Return the minimum number of single-character edits — **insert**, **delete**, or **replace** — needed to turn string `a` into string `b` (the **Levenshtein distance**).

```
"horse" → "ros"          =  3     rose→ros (replace h→r), roros… : replace, delete, delete
"intention" → "execution" =  5
"kitten" → "sitting"     =  3     replace k→s, replace e→i, insert g
```

**Constraints:** `0 ≤ a.length, b.length ≤ 500`; both consist of lowercase English letters.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Full 2-D DP table** ★ — `dp[i][j]` over every prefix pair | O(m·n) time, O(m·n) space | [`edit_distance.kara`](edit_distance.kara) ✓ via `karac run` / `karac build` | [`edit_distance.py`](edit_distance.py) ✓ |
| **Rolling two rows** — keep only the previous row + the one being built | O(m·n) time, O(n) space | [`edit_distance_rolling.kara`](edit_distance_rolling.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter, JIT (`karac run`), and codegen (`karac build`) produce identical output across all thirteen test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other and with the Python mirror.

## The recurrence — a min over three edits

Let `dp[i][j]` be the edit distance between the first `i` characters of `a` and the first `j` of `b`. Compare the last character of each prefix:

```
a[i-1] == b[j-1]  →  dp[i][j] = dp[i-1][j-1]                       (free match)
a[i-1] != b[j-1]  →  dp[i][j] = 1 + min( dp[i-1][j-1],   replace
                                         dp[i-1][j],     delete a[i-1]
                                         dp[i][j-1] )    insert b[j-1]
```

with the borders forced: `dp[i][0] = i` (delete a's whole prefix) and `dp[0][j] = j` (insert b's whole prefix); the answer is `dp[m][n]`. This is the two-string cousin of the grid DP in katas [#62](../62-unique-paths/)–[#64](../64-minimum-path-sum/): a 2-D table filled in a fixed scan order, each interior cell a `min` of already-computed neighbours. The difference from those is the **min over three** in-neighbours — the point where a real choice is made (replace vs delete vs insert), so, like kata [#64](../64-minimum-path-sum/), the recurrence is a genuine optimisation rather than a count.

**Full 2-D table** ([`edit_distance.kara`](edit_distance.kara)) is the ★: materialise the whole `(m+1)×(n+1)` grid, seed the borders, fill the interior row-major. Every cell it reads (`dp[i-1][j-1]`, `dp[i-1][j]`, `dp[i][j-1]`) is final before it is reached — no aliasing subtlety.

**Rolling two rows** ([`edit_distance_rolling.kara`](edit_distance_rolling.kara)) drops the space to O(n): row `i` depends only on row `i-1` and the current row's left cell, so keep `prev` (the finished previous row) and build `cur`, then roll `prev = cur`. Note it carries a *full second row*, unlike kata [#62](../62-unique-paths/)'s single updated-in-place array — Edit Distance reads **both** `prev[j-1]` (diagonal) and `prev[j]` (up), which a single in-place row would clobber before the diagonal is used.

## Kāra features exercised

- **`Vec[Vec[i64]]` table with nested index-write** — the ★ builds the grid with `Vec.new()`/`push`, then *writes* interior cells `dp[r][c] = …` reading three neighbours — the nested read-and-write idiom shared with kata [#64](../64-minimum-path-sum/)'s in-place solver, here on a two-string table.
- **`std.cmp` `min` over three values** — `1 + min(diag, min(up, left))`; the built-in `min[T: Ord]` (the same one katas [#42](../42-trapping-rain-water/)/[#64](../64-minimum-path-sum/) use since it landed) composed to a three-way minimum.
- **`String.bytes()` byte comparison** — `a.bytes()`/`b.bytes()` give `Slice[u8]` views; `ab[r-1] == bb[c-1]` compares characters (ASCII, so byte index == char position), the zero-copy string-scan idiom of katas [#28](../28-find-the-index-of-the-first-occurrence-in-a-string/)/[#58](../58-length-of-last-word/).
- **Rolling `Vec[i64]` rows with `prev = cur`** — the rolling solver replaces the previous row wholesale each step, the O(n)-space DP shape of kata [#62](../62-unique-paths/) adapted to carry a full row (both diagonal and up are read).
- **Empty-`String` inputs** — `""` exercises the borders directly (`m == 0` or `n == 0`), and `String.bytes()` / `String.len()` on an empty string; the harness includes `("", "")`, `("", "abc")`, `("abc", "")`, `("x", "")`.

**v1 note.** Distances are bounded by `max(m, n) ≤ 500`, so every `dp` cell fits i64 trivially; all arithmetic is `1 + min(…)` with no overflow risk. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — the `Vec[Vec[i64]]` fill and the three-way `min` lower consistently across all engines.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   edit_distance.kara
karac build edit_distance.kara && ./edit_distance

# The rolling O(n)-space approach (identical output):
karac run edit_distance_rolling.kara

# Python
python3 edit_distance.py

# Verify they all agree
diff <(karac run edit_distance.kara) <(python3 edit_distance.py)                && echo OK
diff <(karac run edit_distance.kara) <(karac run edit_distance_rolling.kara)    && echo OK
```

## Benchmarks
Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`edit_distance.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5 re-bench (2026-11-01).** Re-measured on the corpus's **Apple M5 Pro reference machine** (arm64, 6P+12E; clang 21 / rustc 1.95 / go 1.26), with Kāra built by karac `g6697158fa` (v2/MIR backend). **Kāra leads every mirror outright, on wall-clock and on CPU work** — 0.26× Rust, 0.26× equal-safety Rust, 0.28× Go, 0.15× C. The July feed (karac 0.1.0, 2026-07-28) read 0.26× Rust / 0.16× C / 0.34× Go, so the Rust and C ratios are flat; the Go ratio improved because Go's own time grew ~26 % this session (vs −4 to +11 % for the Rust and C rows) while it spent more of a second core on GC (163 % CPU vs 113 % in July). Because this workload is allocation/`realloc`-bound (see the fairness note below), the absolute ordering of the *comparators* tracks the platform's allocator and GC, not DP compute: C's `realloc`-doubling is the slowest. (History: in the 2026-07-10 snapshot kāra ran 1069.9 ms and Go's concurrent GC took the lowest wall-clock; by the 2026-07-28 feed kāra had dropped to 335.5 ms with the comparators unchanged, and it now leads outright.) `bench/results.json` records the M5 host.

**Workload.** The rolling O(n)-space Levenshtein DP, run **K = 400,000** times over per-iteration-generated length-24 string pairs (a 4-letter alphabet, both strings varying with `k` so nothing is hoistable and matches/mismatches mix). The sink is a rolling hash `acc = (acc*131 + d) % 1_000_000_007`; all four compiled mirrors must agree on `313564903` before timing.

### A benchmark-fairness note (load-bearing)

The kata builds each DP row with **`Vec.new()` + `push`** — a *growing* dynamic array. A first draft of these mirrors used fixed **stack arrays** in C/Rust/Go (`int64_t prev[L+1]`), which do **zero heap allocation** — and against those kāra looked **~6× slower**. That comparison is **apples-to-oranges**: heap `Vec` vs stack array is a data-structure difference, not a codegen one. So every mirror here instead builds its rows by **appending to a growing dynamic array** — Rust `Vec::push`, Go `append`, C `realloc`-doubling, Python `list.append` — matching kāra's `Vec.new()+push`. At **equal data-structure semantics**:

`--warmup 5 --runs 30 --shell=none`, `KARAC_AUTO_PAR=0`. **M5 Pro numbers, 2026-11-01.** kāra/Rust/C are strictly single-threaded (~99.5 % CPU); Go's runtime uses ~1.6 cores (163 % CPU) for concurrent GC, so its wall-clock is *not* a like-for-like single-core number — its *user*-CPU time is higher than its wall time.

| Implementation | Wall time | User-CPU | CPU % | Row storage |
|---|---|---|---|---|
| **kāra edit_distance**              | **350.5 ± 20.0 ms** | **348 ms** | 99.4 % | `Vec.new()+push` (grows) |
| go   edit_distance                  | 1239.7 ± 6.2 ms | 1301 ms | 163 % | `append` (grows) |
| rust edit_distance (`-C overflow-checks=on`) | 1345.2 ± 51.2 ms | 1340 ms | 99.8 % | `Vec::push` (grows) |
| rust edit_distance (rustc -O)       | 1362.0 ± 59.6 ms | 1359 ms | 99.9 % | `Vec::push` (grows) |
| c    edit_distance (clang -O3)      | 2331.1 ± 257.2 ms | 2323 ms | 99.8 % | `realloc`-doubling |

**Kāra is the fastest implementation outright** — 3.9× faster than Rust (3.8× than equal-safety Rust), 3.5× faster than Go's wall-clock and 3.7× less CPU work than Go, and 6.7× faster than C. Go's concurrent GC no longer buys it a wall-clock lead (in the 2026-07-10 snapshot it did, by 1.09×), but the comparators' ordering still shows the point of this kata: the run is **allocation/`realloc`-bound**, so absolute wall-clock tracks the platform's allocator + GC, not the DP — Go, overlapping GC on a second core, beats Rust's and C's single-threaded growth; C's `realloc`-doubling is slowest. It's the allocation-side counterpart to the equal-*safety* row in [#69](../69-sqrtx/) and the equal-*memory-semantics* row in [#98](../98-validate-binary-search-tree/) — the honest cross-language number requires matching both the data-structure discipline *and* the core budget.

Two honest qualifiers: (1) this is **allocation/`realloc`-dominated** — the comparators spend ~1.2–2.3 s mostly on growing arrays, so it measures growing-dynamic-array throughput as much as the DP itself. A fixed/pre-sized-array discipline is several times faster for everyone but is a *different* data structure than the kata's `Vec`. (2) The row length is statically knowable, so a pre-sizing codegen pass — kāra's `Vec.new()`+counted-`push` → pre-sized fill (ledger `B-2026-07-08-7`, currently **reverted** for regressing kata #63) — would cut the allocation for kāra specifically; even without it, kāra leads the field here.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py edit_distance` (K=40k) — last measured 2026-07-10, not re-run | 944 ± 7 ms |

Python at K=40k was ~0.94 s; projecting to the compiled mirrors' K=400k (~9.4 s) put it **~8.8× slower than that snapshot's kāra seq** (1069.9 ms) — narrowed by the workload being allocation- rather than compute-bound. The 2026-11-01 re-bench did not set `KARA_BENCH_INCLUDE_PY`, so this row is not re-measured.

### Compile elapsed (cold)

| Compiler | Time |
|---|---|
| clang -O3 edit_distance.c          | **51.3 ms** |
| rustc -O edit_distance.rs          | 96.8 ms |
| **karac build edit_distance.kara** | **127.7 ms** |

On the M5 karac compiles at ~2.5× clang and ~1.32× rustc — slower than both (the 2026-07-10 snapshot had it ~1.07× *faster* than rustc, 83.7 vs 89.8 ms).

### Binary size

| Implementation | Size |
|---|---|
| c    edit_distance                | 32.8 KiB |
| **kāra edit_distance**            | **295.8 KiB** |
| rust edit_distance                | 455.9 KiB |
| go   edit_distance                | 2.38 MiB |

Kāra's `Vec`-heavy DP binary is **295.8 KiB** — between C's 32.8 KiB and Rust's 455.9 KiB, well below Go's 2.38 MiB, and the same size as the scalar katas [#69](../69-sqrtx/)/[#70](../70-climbing-stairs/). Every v2/MIR Kāra binary is ~300–390 KB where the legacy backend's were ~34 KB (this kata's was 33.4 KiB in July); that growth is tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md).

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| **kāra edit_distance**            | **1.05 MiB** |
| rust edit_distance                | 1.11 MiB |
| c    edit_distance                | 1.16 MiB |
| go   edit_distance                | 10.59 MiB |

Kāra/Rust/C sit at the same ~1.1 MiB floor (each row allocated and freed inside the loop — flat steady state, no leak across 400,000 iterations), kāra marginally the leanest; Go's 10.59 MiB reflects its GC arena churning the `append`-grown slices. (Absolute figures are lower than the container's because macOS `time -l` "peak memory footprint" accounts differently than Linux max-RSS — compare within a host, not across.)

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 edit_distance.c          | **2.6 MiB** |
| rustc -O edit_distance.rs          | 27.9 MiB |
| **karac build edit_distance.kara** | **56.3 MiB** |

On the M5 karac's compile-memory footprint is now the highest of the three — ~2.0× rustc's 27.9 MiB (it was 19.7 MiB, under rustc's, in the 2026-07-10 snapshot).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — and here, with both building rows via a growing `Vec`, **kāra leads Rust 3.9×** (and C 6.7×). C calibrates the `realloc` floor, Go is the GC/`append` data point — and the cautionary multicore-GC case (its wall-clock leans on ~1.6 cores), Python the ergonomic foil. The load-bearing facts: the five-language sink agreement, that kāra is the *fastest* mirror and does the *least total CPU work* of all four at equal growing-`Vec` semantics, and the reminder that comparing kāra's heap `Vec` against native *stack arrays* (the naive draft) understates it by ~6×.
