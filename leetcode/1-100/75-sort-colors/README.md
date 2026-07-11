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

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`sort_colors.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5-confirmed (2026-07-11).** Re-measured on the corpus's **Apple M5 Pro reference machine** (arm64, 6P+12E; clang 21 / rustc 1.95 / go 1.26; karac from current `main`), replacing the earlier x86-64 cloud-container snapshot. **Kāra ties C for the lead and beats both Rust builds and Go** — while doing overflow-checked arithmetic C skips entirely (see below). `bench/results.json` records the M5 host.

**Workload.** The Dutch National Flag one-pass sort (the ★) over an `n=500` `{0,1,2}` array **allocated once and reused**: each of **K = 200,000** iterations refills it in place with a `k`-dependent pattern, sorts it in place, and folds the sorted result into a rolling hash `acc = (acc*131 + v) % 1_000_000_007`. Allocating once and refilling in place (rather than growing a fresh `Vec` per iteration — kata [#73](../73-set-matrix-zeroes/)'s regime) keeps the measured work the **sort's data-dependent branches and swaps**, not allocation. All five compiled mirrors must agree on `90962821` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. **M5 Pro numbers.** All single-threaded, ~99.7 % CPU (the loop-carried hash is not a reduction the auto-par pass can split — `karac build --concurrency-report` reports `<no parallelization opportunities detected>`). Tight variance (±1–4 ms) across all mirrors.

| Implementation | Wall time |
|---|---|
| c    sort_colors (clang -O3)                     | **360.0 ± 1.6 ms** |
| **kāra sort_colors**                             | **362.8 ± 1.4 ms** |
| rust sort_colors (rustc -O, overflow-checks=on)  | 367.9 ± 3.1 ms |
| rust sort_colors (rustc -O)                      | 369.4 ± 3.7 ms |
| go   sort_colors                                 | 396.9 ± 2.7 ms |

**Kāra ties C for the lead** — 362.8 ms vs clang's 360.0 ms is a 1.01× dead heat — and **beats both Rust builds** (equal-safety `rustc -O -C overflow-checks=on` 367.9 ms by 1.01×, wrapping `rustc -O` 369.4 ms by 1.02×) and Go (396.9 ms, 1.09×). The result is sharper than "tied": kāra retires **2.90 G instructions to C's 2.57 G** — ~13 % *more* — because it overflow-checks every arithmetic op while C wraps silently; yet the two finish within 1 % on the clock, because those extra check-branches are perfectly predicted and near-free. So kāra ties *unchecked* C's wall-time while carrying the safety, and edges *checked* Rust outright. Python at 1/10 the iteration count is ~0.77 s (so ~7.7 s projected to full K, timed separately, not sink-checked).

Compile-cold on the M5 is clang 39.4 ms < **karac 79.4 ms** < rustc 80.3 ms — karac edges rustc, ~2× the clang floor. Binary size: c 32.7 KiB, **kāra 33.4 KiB** (at C parity — the runtime floor dead-strips on the M5), rust 455.4 KiB, go 2.38 MiB. Peak RSS is tight among the non-GC mirrors — **kāra 1.00 MiB** (the leanest), c 1.02, rust 1.06 — with Go at 2.70 MiB. See [`bench/results.json`](bench/results.json) for the exact records.

The load-bearing facts: the five-language sink agreement on `90962821`, and that on this **branch-heavy, in-place** sort kāra ties the C floor and beats both Rust builds — carrying default overflow checks (~13 % more instructions) at wall-clock parity with unchecked C — the same compute-bound regime as [#74](../74-search-a-2d-matrix/), distinct from the allocation-bound [#72](../72-edit-distance/)/[#73](../73-set-matrix-zeroes/).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — and at **equal safety** (both overflow-checked) kāra is **ahead** on the M5 (362.8 vs 367.9 ms) on this data-dependent branch-and-swap loop, and ahead of wrapping `rustc -O` too. C calibrates the metal floor (kāra ties it while doing checked arithmetic C skips), Go the other native data point, Python (run at 1/10 the iteration count, timed separately) the ergonomic foil.
