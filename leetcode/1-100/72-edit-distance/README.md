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

> ⚠️ **Machine caveat.** Measured on a **shared x86-64 Linux cloud container** (Intel Xeon @ 2.10 GHz, 4 vCPU, Linux 6.18.5; karac from current `main`). Don't compare absolute times/sizes/RSS against sibling katas' M5 tables; `bench/results.json` records the real host. Re-run `bench/bench.sh` on the M5 to fold comparable numbers in.

**Workload.** The rolling O(n)-space Levenshtein DP, run **K = 400,000** times over per-iteration-generated length-24 string pairs (a 4-letter alphabet, both strings varying with `k` so nothing is hoistable and matches/mismatches mix). The sink is a rolling hash `acc = (acc*131 + d) % 1_000_000_007`; all four compiled mirrors must agree on `313564903` before timing.

### A benchmark-fairness note (this is the headline)

The kata builds each DP row with **`Vec.new()` + `push`** — a *growing* dynamic array. A first draft of these mirrors used fixed **stack arrays** in C/Rust/Go (`int64_t prev[L+1]`), which do **zero heap allocation** — and against those kāra looked **~6× slower**. That comparison is **apples-to-oranges**: heap `Vec` vs stack array is a data-structure difference, not a codegen one. So every mirror here instead builds its rows by **appending to a growing dynamic array** — Rust `Vec::push`, Go `append`, C `realloc`-doubling, Python `list.append` — matching kāra's `Vec.new()+push`. At **equal data-structure semantics**:

`--warmup 2 --runs 10 --shell=none`. All single-threaded. **Cloud-container numbers.**

| Implementation | Wall time | Row storage |
|---|---|---|
| **kāra edit_distance**              | **2153 ± 36 ms** | `Vec.new()+push` (grows) |
| c    edit_distance (clang -O3)      | 2354 ± 28 ms | `realloc`-doubling |
| rust edit_distance (rustc -O)       | 2860 ± 53 ms | `Vec::push` (grows) |
| go   edit_distance                  | 3640 ± 78 ms | `append` (grows) |

**Kāra is the fastest of the four** when everyone builds rows the way the kata does — ahead of C's `realloc`-grow (1.09×), Rust's `Vec::push` (1.33×), and Go's `append` (1.69×). The story fully inverts from the naive stack-array draft: kāra's growing-`Vec` codegen + allocator path is *efficient*, and the earlier "6×" was a measurement artifact. This is the counterpart to the equal-*safety* row in [#69](../69-sqrtx/) and the equal-*memory-semantics* row in [#98](../98-validate-binary-search-tree/) — a reminder that the honest cross-language number requires matching the data-structure discipline, not just the algorithm.

Two honest qualifiers: (1) this is **allocation/`realloc`-dominated** — all four spend 2–3.6 s mostly on growing arrays, so it measures growing-dynamic-array throughput as much as the DP itself. A fixed/pre-sized-array discipline is ~6× faster for everyone (a stack-array C measured ~358 ms) but is a *different* data structure than the kata's `Vec`. (2) The row length is statically knowable, so a pre-sizing codegen pass — kāra's `Vec.new()`+counted-`push` → pre-sized fill (ledger `B-2026-07-08-7`, currently **reverted** for regressing kata #63) — would cut the allocation for kāra specifically; even without it, kāra leads here.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py edit_distance` (K=40k) | 2875 ± 62 ms |

Python at K=40k is ~2.9 s; projecting to the compiled mirrors' K=400k (~28.7 s) puts it **~13× slower than kāra seq** — narrowed by the workload being allocation- rather than compute-bound.

### Compile elapsed (cold)

| Compiler | Time |
|---|---|
| clang -O3 edit_distance.c          | **130.5 ms** |
| rustc -O edit_distance.rs          | 167.2 ms |
| **karac build edit_distance.kara** | **243.6 ms** |

On this container karac compiles at ~1.87× clang and ~1.46× rustc.

### Binary size

| Implementation | Size |
|---|---|
| c    edit_distance                | 15.8 KiB |
| **kāra edit_distance**            | **324.6 KiB** |
| go   edit_distance                | 2.12 MiB |
| rust edit_distance                | 3.77 MiB |

Unlike the all-scalar katas ([#69](../69-sqrtx/)/[#70](../70-climbing-stairs/), ~15 KiB), the `Vec`-heavy DP links the runtime's allocation/panic floor, so kāra's binary is 324.6 KiB — still far below Rust's 3.8 MiB and Go's 2.1 MiB, above C's 15.8 KiB (the same ~324 KiB floor as the DP katas [#62](../62-unique-paths/)–[#66](../66-plus-one/)).

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| **kāra edit_distance**            | **6.89 MiB** |
| c    edit_distance                | 6.89 MiB |
| rust edit_distance                | 6.89 MiB |
| go   edit_distance                | 9.95 MiB |

Kāra/C/Rust sit at the same ~6.89 MiB floor (each row allocated and freed inside the loop — flat steady state, no leak across 400,000 iterations); Go's 9.95 MiB reflects its GC arena churning the `append`-grown slices.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| **karac build edit_distance.kara** | **82.8 MiB** |
| clang -O3 edit_distance.c          | 94.8 MiB |
| rustc -O edit_distance.rs          | 108.2 MiB |

On this container karac has the lowest compile-memory footprint of the three.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — and here, with both building rows via a growing `Vec`, **kāra leads Rust 1.33×** (and C 1.09×, Go 1.69×). C calibrates the `realloc` floor, Go is the GC/`append` data point, Python the ergonomic foil. The load-bearing facts: the five-language sink agreement, that kāra is the *fastest* of the four at equal growing-`Vec` semantics, and the reminder that comparing kāra's heap `Vec` against native *stack arrays* (the naive draft) understates it by ~6×.
