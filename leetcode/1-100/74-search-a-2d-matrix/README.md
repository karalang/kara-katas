# 74. Search a 2D Matrix

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Binary Search · Matrix &nbsp;·&nbsp; **Source:** [leetcode.com/problems/search-a-2d-matrix](https://leetcode.com/problems/search-a-2d-matrix/)

Given an `m × n` matrix with two sorted properties — **each row ascends**, and **the first element of every row is greater than the last element of the row above** — decide whether a `target` value is present. Required: **O(log(m·n))** time.

```
matrix = [[ 1,  3,  5,  7],
          [10, 11, 16, 20],
          [23, 30, 34, 60]]

target = 3   -> true
target = 13  -> false
```

**Constraints:** `1 ≤ m, n ≤ 100`; `-10⁴ ≤ matrix[i][j], target ≤ 10⁴`; the two sorted properties hold.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Flattened binary search** ★ — treat the grid as one sorted array | O(log m·n) | [`search_a_2d_matrix.kara`](search_a_2d_matrix.kara) ✓ via `karac run` / `karac build` | [`search_a_2d_matrix.py`](search_a_2d_matrix.py) ✓ |
| **Two binary searches** — pick the row, then search it | O(log m + log n) | [`search_a_2d_matrix_two_phase.kara`](search_a_2d_matrix_two_phase.kara) ✓ | — |
| **Staircase from top-right** — the weaker-property walk | O(m + n) | [`search_a_2d_matrix_staircase.kara`](search_a_2d_matrix_staircase.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output across all fourteen queries, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and all three approaches agree with each other and with the Python mirror.

## The key insight — the whole grid is one sorted array

The two sort properties together say exactly this: reading the matrix **row-major** produces a single ascending sequence of `m·n` values. So the whole grid *is* a sorted array, and one binary search over the flat index range finds the target:

```
lo, hi = 0, m·n - 1
mid    -> m[mid / cols][mid % cols]      # unflatten the index
  == target  ->  found
  <  target  ->  lo = mid + 1
  >  target  ->  hi = mid - 1
```

**Flattened binary search** ([`search_a_2d_matrix.kara`](search_a_2d_matrix.kara)) is the ★ — the plain `lo`/`hi`/`mid` loop of katas [#35](../35-search-insert-position/) / [#69](../69-sqrtx/), with the one twist that `mid` indexes a *flattened* grid via `/` and `%`. The midpoint is computed `lo + (hi - lo) / 2` to stay overflow-safe.

**Two binary searches** ([`search_a_2d_matrix_two_phase.kara`](search_a_2d_matrix_two_phase.kara)) uses the axes separately: binary-search the rows for the last one whose first element is `≤ target` (the only row that could hold it, since row starts strictly increase), then binary-search that row. Same asymptotics (`log m + log n = log m·n`), a different decomposition.

**Staircase from top-right** ([`search_a_2d_matrix_staircase.kara`](search_a_2d_matrix_staircase.kara)) needs only the *weaker* "rows sorted, columns sorted" property (it is the canonical solution to the harder [#240](https://leetcode.com/problems/search-a-2d-matrix-ii/)). From the top-right corner — the largest in its row, smallest in its column — each comparison drops a whole row or column, giving O(m+n). Slower asymptotically, but the more general shape, kept as a third bug-finding surface.

## Kāra features exercised

- **`ref Vec[Vec[i64]]` read-only nested indexing** — `search_matrix(m: ref Vec[Vec[i64]], target: i64) -> bool` reads `m[r][c]` without mutation; the borrowed-matrix read idiom shared with kata [#48](../48-rotate-image/)'s `print_grid`.
- **Flatten/unflatten with `/` and `%`** — `m[mid / cols][mid % cols]` turns one linear index into a `(row, col)` pair, the arithmetic core of the ★.
- **`bool` return + `f`-string bool interpolation** — `search_matrix` returns `bool`; the harness prints `f"search({target}) = {found}"`, exercising Kāra's `true`/`false` rendering (the Python mirror lowercases `True`/`False` to match).
- **`and` short-circuit loop guard** — the staircase walks `while r < rows and c >= 0i64` (Kāra spells it `and`, not `&&`).
- **Matrix literals of varied shape** — `[[5]]` (1×1), `[[1,2,3,4,5]]` (single row), `[[1],[3],[5],[7]]` (single column) drive the degenerate cases through all three solvers.

**v1 note.** The overflow-safe midpoint `lo + (hi - lo) / 2` never overflows for these bounds, and all values fit i64 trivially. All three solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   search_a_2d_matrix.kara
karac build search_a_2d_matrix.kara && ./search_a_2d_matrix

# The other two approaches (identical output):
karac run search_a_2d_matrix_two_phase.kara
karac run search_a_2d_matrix_staircase.kara

# Python
python3 search_a_2d_matrix.py

# Verify they all agree
diff <(karac run search_a_2d_matrix.kara) <(python3 search_a_2d_matrix.py)                    && echo OK
diff <(karac run search_a_2d_matrix.kara) <(karac run search_a_2d_matrix_two_phase.kara)      && echo OK
diff <(karac run search_a_2d_matrix.kara) <(karac run search_a_2d_matrix_staircase.kara)      && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`search_a_2d_matrix.{kara,rs,c,py}`, `go-seq/main.go`).

> ⚠️ **Machine caveat.** Measured on a **shared x86-64 Linux cloud container** (Intel Xeon @ 2.80 GHz, 4 vCPU, Linux 6.18.5; karac from current `main`). These are container numbers only — this kata has **no M5 `results.json` yet**; it will be re-benched on the corpus's Apple M5 Pro and the canonical table added then. Don't compare absolute times/sizes/RSS against sibling katas' M5 tables; [`bench/results.container-x86.json`](bench/results.container-x86.json) records the real host.

**Workload.** The flattened O(log m·n) binary search (the ★), over a 100×100 sorted matrix **built once**, then hammered with **K = 10,000,000** queries. Targets cycle `k mod 20000` against a matrix of the even values `0, 2, … , 19998`, so almost exactly **half the queries hit and half miss** — defeating any branch-prediction shortcut. This is a **build-once + punch** workload (per the corpus's benchmark-design rule): the one-time O(m·n) matrix build is negligible, so what's timed is the search itself. All five compiled mirrors must agree on `844187512` before timing.

**Equal safety.** Kāra checks integer overflow on every arithmetic op by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded (the loop-carried hash is not a reduction the auto-par pass can split; the default build is verified equal to `KARAC_AUTO_PAR=0`). **Cloud-container numbers.**

| Implementation | Wall time |
|---|---|
| c    search_a_2d_matrix (clang -O3)              | **763.9 ± 7.1 ms** |
| rust search_a_2d_matrix (rustc -O, overflow-checks=on) | 780.9 ± 11.3 ms |
| rust search_a_2d_matrix (rustc -O)              | 797.6 ± 9.4 ms |
| **kāra search_a_2d_matrix**                     | **807.3 ± 10.5 ms** |
| go   search_a_2d_matrix                         | 817.2 ± 8.4 ms |

A **five-way tie inside 7%**. On this compute-bound, allocation-free search kāra lands within **1.06×** of the clang floor and squarely among the natives — and at **equal safety** (kāra checks overflow by default) the faithful peer `rustc -O -C overflow-checks=on` (780.9 ms) sits within noise of kāra (807.3 ms). Python at 1/10 the query count is ~1.36 s (so ~13.6 s projected to full K, timed separately, not sink-checked).

Compile-cold (clang 76 ms < rustc 123 ms < karac 168 ms) and binary size (c 15.7 KiB, **kāra 324.5 KiB**, go 2.11 MiB, rust 3.77 MiB — kāra links the runtime floor but stays far under the Rust/Go binaries); peak RSS is a ~0.7 MiB spread (c 1.66, go 1.90, rust 2.21, kāra 2.35 MiB). See [`bench/results.container-x86.json`](bench/results.container-x86.json) for the exact records.

The load-bearing facts: the five-language sink agreement on `844187512`, and that on a **compute-bound, allocation-free** search this is a tight cluster — the opposite regime from the allocation-heavy `Vec`-of-`Vec` katas ([#72](../72-edit-distance/)/[#73](../73-set-matrix-zeroes/)). See the JSON for the exact per-language times, binary sizes, and peak-RSS on this host.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — and at **equal safety** (both overflow-checked) the two are within measurement noise on this pointer-chasing search. C calibrates the metal floor, Go is the other native data point, Python (run at 1/10 the query count, timed separately) the ergonomic foil.
