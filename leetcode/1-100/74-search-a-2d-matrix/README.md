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

> ✅ **M5-confirmed (2026-07-11).** Re-measured on the corpus's **Apple M5 Pro reference machine** (arm64, 6P+12E; clang 21 / rustc 1.95 / go 1.26; karac from current `main`), replacing the earlier x86-64 cloud-container snapshot. **Kāra's relative position improves on the M5** — from mid-pack on the container (4th) to **2nd of five**, ahead of both Rust builds and C, behind only Go (and neck-and-neck with it on instructions retired). `bench/results.json` records the M5 host.

**Workload.** The flattened O(log m·n) binary search (the ★), over a 100×100 sorted matrix **built once**, then hammered with **K = 10,000,000** queries. Targets cycle `k mod 20000` against a matrix of the even values `0, 2, … , 19998`, so almost exactly **half the queries hit and half miss** — defeating any branch-prediction shortcut. This is a **build-once + punch** workload (per the corpus's benchmark-design rule): the one-time O(m·n) matrix build is negligible, so what's timed is the search itself. All five compiled mirrors must agree on `844187512` before timing.

**Equal safety.** Kāra checks integer overflow on every arithmetic op by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. **M5 Pro numbers.** All single-threaded, ~99.7 % CPU (the loop-carried hash is not a reduction the auto-par pass can split — `karac build --concurrency-report` reports `<no parallelization opportunities detected>`). Two independent 30-run samples put kāra at 360.6 and 361.3 ms — a stable mean, though kāra carries higher run-to-run jitter (±~21 ms) than the native binaries; its instruction count is deterministic at **3.55 G, within 1.2 % of Go's 3.51 G** (identical work — see below).

| Implementation | Wall time |
|---|---|
| go   search_a_2d_matrix                         | **341.8 ± 10.8 ms** |
| **kāra search_a_2d_matrix**                     | **361.3 ± 20.7 ms** |
| rust search_a_2d_matrix (rustc -O, overflow-checks=on) | 371.0 ± 8.0 ms |
| rust search_a_2d_matrix (rustc -O)              | 384.7 ± 1.2 ms |
| c    search_a_2d_matrix (clang -O3)             | 386.8 ± 4.6 ms |

A **tight cluster inside 13 %**, with kāra **2nd of five** — ahead of wrapping `rustc -O` (1.06×), C (1.07×), and — the load-bearing comparison — ahead of the equal-safety `rustc -O -C overflow-checks=on` (371.0 ms) by **1.03×**. Kāra checks overflow on every op by default, so `rust -C overflow-checks=on` is the faithful peer, and kāra's bounds-check-eliminated binary-search codegen *beats* it here rather than merely tying (it sat within noise on the container). Only Go is ahead (1.06×), and by instruction count the two are neck-and-neck (kāra 3.55 G vs Go 3.51 G, within 1.2 %) — Go's edge is a small wall-clock margin on identical work. This *improves* on the x86 container, where kāra was mid-pack (4th of five); on the M5 kāra's search codegen pulls ahead of both Rust and C. Python at 1/10 the query count is ~0.71 s (so ~7.1 s projected to full K, timed separately, not sink-checked).

Compile-cold on the M5 is clang 43.5 ms < **karac 82.9 ms** < rustc 84.6 ms — karac edges rustc, at ~1.9× the clang floor. Binary size: c 32.7 KiB, **kāra 33.4 KiB** (at C parity — the runtime floor dead-strips on the M5), rust 455.9 KiB, go 2.38 MiB. Peak RSS is a tight band among the non-GC mirrors — **kāra 1.11 MiB** (the leanest), c 1.13, rust 1.20 — with Go at 2.83 MiB. See [`bench/results.json`](bench/results.json) for the exact records.

The load-bearing facts: the five-language sink agreement on `844187512`, and that on a **compute-bound, allocation-free** search kāra's codegen lands 2nd of five — ahead of both Rust builds and C, a tie in work with Go — the opposite regime from the allocation-heavy `Vec`-of-`Vec` katas ([#72](../72-edit-distance/)/[#73](../73-set-matrix-zeroes/)), and a favorable one for kāra's bounds-check-eliminated search loop.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — and at **equal safety** (both overflow-checked) kāra is **ahead** on the M5 (361 vs 371 ms, 1.03×) on this pointer-chasing search, and ahead of wrapping `rustc -O` too. C calibrates the metal floor, Go is the other native data point (fastest here, but within 1.2 % of kāra on instructions retired — identical work), Python (run at 1/10 the query count, timed separately) the ergonomic foil.
