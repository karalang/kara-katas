# 75. Sort Colors

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Two Pointers · Sorting &nbsp;·&nbsp; **Source:** [leetcode.com/problems/sort-colors](https://leetcode.com/problems/sort-colors/)

Given an array of `n` objects coloured **red (0)**, **white (1)**, or **blue (2)**, sort them **in place** so that objects of the same colour are adjacent, in the order `0, 1, 2`. Don't use a library sort.

```
[2,0,2,1,1,0]  ->  [0,0,1,1,2,2]
[2,0,1]        ->  [0,1,2]
```

**Constraints:** `1 ≤ n ≤ 300`; every value is `0`, `1`, or `2`. **Follow-up:** the two-pass counting sort is easy — can you do it in **one pass** with **O(1)** extra space?

## Approaches

| Approach | Passes | Kāra | Python |
|---|---|---|---|
| **Dutch National Flag** ★ — three pointers, one pass | 1 | [`sort_colors.kara`](sort_colors.kara) ✓ via `karac run` / `karac build` | [`sort_colors.py`](sort_colors.py) ✓ |
| **Counting sort** — tally, then overwrite | 2 | [`sort_colors_counting.kara`](sort_colors_counting.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output across all twelve test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other and with the Python mirror.

## The one-pass partition — three pointers, four regions

Dijkstra's **Dutch National Flag** partition carries three indices that split the array into four regions:

```
[0, low)      settled 0s
[low, mid)    settled 1s
[mid, high]   UNKNOWN — still to classify
(high, n)     settled 2s
```

Walk `mid` forward; each step restores the invariant with exactly one move:

```
a[mid] == 0  ->  swap a[low], a[mid];  low++, mid++
a[mid] == 1  ->  mid++
a[mid] == 2  ->  swap a[mid], a[high]; high--        # mid does NOT advance
```

**Dutch National Flag** ([`sort_colors.kara`](sort_colors.kara)) is the ★ — one pass, O(1) space. The lone subtlety is that the `== 2` case must **not** advance `mid`: the value swapped in from `high` has not been examined yet, so it must be re-classified on the next iteration. (The `== 0` case *can* advance both, because the value swapped in from `low` is a value `mid` already passed — necessarily a settled `1`.) The swap `a[i], a[j] = a[j], a[i]` is Kāra's parallel-assignment, the 1-D form of kata [#48](../48-rotate-image/)'s four-way rotate.

**Counting sort** ([`sort_colors_counting.kara`](sort_colors_counting.kara)) is the two-pass baseline the follow-up improves on: tally `c0`/`c1`/`c2`, then overwrite the array with that many `0`s, then `1`s, then `2`s. O(n) time, O(1) extra space (three counters), but it touches every element twice where the Dutch-flag partition touches each once. Kept as the obvious cross-check; it agrees with the ★ on every case.

## Kāra features exercised

- **`mut ref Vec[i64]` in-place index swap** — `sort_colors(a: mut ref Vec[i64])` mutates `a[i]` through parallel assignment `a[low], a[mid] = a[mid], a[low]`; the 1-D relative of kata [#48](../48-rotate-image/)'s four-target rotate.
- **Three-pointer `while mid <= high` loop** — the O(1)-space partition invariant, the three-way generalisation of the two-pointer scans in katas [#26](../26-remove-duplicates-from-sorted-array/)/[#27](../27-remove-element/).
- **`ref Vec[i64]` read-only scan** — `print_arr`/`hash_arr` read `a[i]` through an immutable borrow; the same borrow-then-index idiom as the mutating solver, minus the writes.
- **Array literals of varied shape** — `[2,0,2,1,1,0]`, `[0]`, `[2,2,2]`, `[2,1,0]` drive single-element, all-one-colour, already-sorted and reversed edge cases through both solvers.

**v1 note.** Values are only `0`/`1`/`2` and the hash fold stays non-negative, so the sink is cross-language-identical. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — the in-place `Vec[i64]` swap-partition lowers consistently across all engines.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   sort_colors.kara
karac build sort_colors.kara && ./sort_colors

# The two-pass counting sort (identical output):
karac run sort_colors_counting.kara

# Python
python3 sort_colors.py

# Verify they all agree
diff <(karac run sort_colors.kara) <(python3 sort_colors.py)                 && echo OK
diff <(karac run sort_colors.kara) <(karac run sort_colors_counting.kara)    && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`sort_colors.{kara,rs,c,py}`, `go-seq/main.go`, plus the parallel comparators `sort_colors_par.c`, `rayon/`, `go-par/`).

> ✅ **M5-confirmed (2026-07-11).** Re-measured on the corpus's **Apple M5 Pro reference machine** (arm64, 6P+12E = 18 logical cores; clang 21 / rustc 1.95 / go 1.26; karac from current `main`), replacing the earlier x86-64 cloud-container snapshot. **On the M5 both lanes improve for kāra:** the seq lane pulls *ahead* of Rust (1.12×, not just tying it), and the par lane's auto-par *overtakes* hand-tuned rayon (it sat behind rayon on the 4-vCPU container). `bench/results.json` records the M5 host.

**Workload — a batch that exposes both lanes.** Like kata [#1](../1-two-sum/), Sort Colors is benched as **K = 2,000 independent** Dutch-flag sorts (the ★) of `n = 59,999`-element `{0,1,2}` arrays, each grown by `push`/`append`/`realloc` (matching Kāra's `Vec.new()+push`, the [#72](../72-edit-distance/) fairness lesson), hashed, and combined through a **plain associative sum**. The length is deliberately *not* a multiple of 3, so the sorted result genuinely depends on the seed (no constant-fold/hoist). Because the reduction is an associative `sum`, the **default `karac build` auto-parallelizes the `for i in 0..K` loop with no hand-written parallel code** — giving both a single-threaded lane and a parallel lane over the *same* work. All nine seq+par mirrors agree on `315566453719` before timing.

#### Seq lane — single-threaded

`--warmup 3 --runs 20 --shell=none`. `rustc -O -C overflow-checks=on` is the equal-safety row (Kāra checks overflow by default; kata [#69](../69-sqrtx/)'s discipline). **M5 Pro numbers.**

| Implementation | Wall time |
|---|---|
| c    sort_colors (clang -O3)                     | **460.6 ± 1.2 ms** |
| **kāra sort_colors (KARAC_AUTO_PAR=0)**          | **462.0 ± 4.0 ms** |
| rust sort_colors (rustc -O)                      | 516.5 ± 4.7 ms |
| rust sort_colors (rustc -O, overflow-checks=on)  | 518.6 ± 6.5 ms |
| go   sort_colors                                 | 812.1 ± 17.6 ms |

Kāra **ties the C floor** (462.0 vs 460.6 ms, 1.00×) and **beats both Rust builds by 1.12×** — including, at **equal safety**, `rustc -O -C overflow-checks=on` (518.6 ms). Go trails at ~812 ms — its GC churns on the per-iteration 60 k-element `append` allocations (spilling onto a second core, 142 % CPU), where Kāra/C/Rust free deterministically at ~100 % CPU.

#### Par lane — auto-par vs hand-tuned

The **same batch**, parallel: `karac build`'s auto-parallelizer splits the sum reduction across cores with **zero parallel source**, raced against hand-tuned C-pthreads (the bare-metal floor), rayon, and goroutines. `--warmup 5 --runs 30`, across all 18 logical cores. Not comparable to the seq rows above.

| Implementation | Wall time | Cores used |
|---|---|---|
| c    sort_colors (pthreads — metal floor)        | **35.5 ± 2.7 ms** | 15.4 |
| **kāra sort_colors (auto-par, NO parallel code)**| **37.9 ± 3.5 ms** | 14.4 |
| rust sort_colors (rayon par_iter)                | 38.7 ± 2.1 ms | 16.2 |
| go   sort_colors (goroutines + WaitGroup)        | 195.9 ± 4.2 ms | 6.1 |

**This is the headline.** Kāra's auto-par — emitted from a plain `for i in 0..K { sum = sum + sort_and_hash(i) }` with **no threads, no `par`, no parallel library** — **overtakes hand-tuned rayon** (37.9 vs 38.7 ms) and lands within **1.07×** of the bare-metal C-pthreads floor, a **12.2× speedup** over its own single-threaded twin (462.0 → 37.9 ms) on the M5's 18 cores. It beats rayon on *total work* too: kāra spends **538.6 ms of CPU — matching C-pthreads' 538.5 ms** — to rayon's 615.3 ms, so the compiler-emitted split is as efficient as the metal floor's and leaner than rayon's. On the 4-vCPU container kāra sat *behind* rayon (220.6 vs 216.4 ms); the M5's wider core count is exactly where the auto-parallelizer's split pulls ahead. The same zero-parallel-code auto-par showcase as kata [#1](../1-two-sum/); the entire parallelization is a compiler decision off the associative reduction.

Compile-cold on the M5 is clang 40.4 ms < rustc 80.1 ms < **karac 83.3 ms** (~2.1× clang, within noise of rustc). Binary size: c 32.8 KiB, **kāra 33.4 KiB seq / 296.1 KiB par** (the par binary carries the auto-par scheduler), rust 455.6 KiB, go 2.38 MiB. Runtime peak RSS: **kāra 2.5 MiB seq / 15.1 MiB par** (thread pool + per-core buffers), vs c 1.7, rust 2.2, go 11.1 MiB. Python at 1/10 K is ~0.88 s. See [`bench/results.json`](bench/results.json) for the exact records.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline seq ratio is the codegen-vs-Rust gap — kāra ahead by 1.12× at equal safety on the M5 — and in the par lane rayon is the hand-tuned-parallel yardstick that Kāra's auto-par **overtakes** (37.9 vs 38.7 ms, and on less total CPU). C calibrates the metal floor (seq clang and pthreads), Go is the GC data point (slow here on the allocation-heavy batch), Python the ergonomic foil.
