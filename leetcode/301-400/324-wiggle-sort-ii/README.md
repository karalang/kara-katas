# 324. Wiggle Sort II

Reorder `nums` in place so that `nums[0] < nums[1] > nums[2] < nums[3] ...`.
The input is promised to have such an order. Values are in `0..5000`.

```
[1, 5, 1, 1, 6, 4]  ->  [1, 6, 1, 5, 1, 4]
[1, 3, 2, 2, 3, 1]  ->  [2, 3, 1, 3, 1, 2]
```

The answer is not unique, which shapes everything below: arms that use
different methods print different, equally valid arrangements, so they are
checked against what an answer must be rather than against each other.

## Approaches

| file | mechanism | cost |
|---|---|---|
| `wiggle_sort.kara` ★ | sort a copy, deal both halves out from the top | `O(n log n)` time, `O(n)` extra |
| `wiggle_sort_count.kara` | counting pass over `0..5000` instead of the sort | `O(n + 5001)` time and extra |
| `wiggle_sort_select.kara` | quickselect the median, three-way partition through a virtual index | expected `O(n)` time, `O(1)` extra |
| `differential.kara` | the three arms, a backtracking existence oracle, eight properties | — |
| `bench/wiggle_sort.kara` | 16 passes of the select arm over 1,000,000 values | — |

Every arm prints the same seventeen inputs: the two examples, the edge cases
below, three small random inputs and three large ones (up to 50,000 values,
printed as a checksum). The ★ and counting arms print the same arrangements
byte for byte, and `wiggle_sort.py` mirrors them. The select arm prints its
own arrangement, and every line it prints ends in `ok`.

## Three ways to wiggle

**★ Sort, then deal from the top.** Sort a copy. The smaller half (the first
`(n + 1) / 2` values) goes into the even slots and the larger half into the
odd slots, so every odd slot holds a value from the top half and its
neighbours come from the bottom half. Both halves are laid down in
DESCENDING order, and that is the whole trick. Equal values are what make the
problem hard: a value can straddle the two halves, so one copy sits in an even
slot and another in an odd slot. Dealt in descending order, the small half's
copies of the median go to the front of the even slots and the large half's
go to the back of the odd slots, so they never touch. Ascending order puts
them side by side: `[4, 5, 5, 6]` comes out `[4, 5, 5, 6]`, which is not a
wiggle, where descending gives `[5, 6, 4, 5]`.

**Counting.** The values are bounded, so a counting pass replaces the sort.
Walk the values from 5000 down and deal them out, first into the odd slots,
then, once those are full, into the even slots. That is exactly the ★ arm's
deal, so the two print the same arrangement.

**Quickselect and a virtual index.** The ★ arm only needs one fact from its
sort: which values are above the median and which below. Quickselect finds
the median in expected `O(n)` and a three-way partition places everything
around it, in place. The partition runs over a virtual index: virtual slot
`i` is real slot `(1 + 2i) % (n | 1)`, which visits the real odd slots first
(1, 3, 5, ...) and then the even ones. Partitioning the virtual array as
"larger, equal, smaller" puts the larger values in the odd slots, the smaller
ones at the far end of the even slots, and the median's copies at the tail of
the odd slots and the head of the even ones, as far apart as they can get.
The `| 1` matters for even `n`: without it the mapping stops being a
permutation.

## Differential

`differential.kara` runs all three arms on 1,000 small random inputs (up to
8 values over 2 to 4 distinct values, so repeats are everywhere), on eight
large solvable ones, and on one input that reaches the bound 5000. The small
inputs are not filtered for solvability: about a third have no answer at all.
A backtracking search over the distinct values and their counts decides which.

| property | checks |
|---|---|
| P1–P3 | each arm finds a wiggle **exactly when** the oracle says one exists |
| P4 | each arm's output uses exactly the input's values, solvable or not |
| P5 | the counting arm's arrangement is the ★ arm's, byte for byte |
| P6 | the ★ arm's arrangement depends only on the values, not their order |
| P7 | feeding an arm its own wiggle gives a wiggle again |
| P8 | on large solvable inputs, every arm finds a wiggle |

P1–P3 are the strong ones: an arm that "usually" works fails them on the
inputs where it breaks, and an arm that returns a wiggle on an unsolvable
input is impossible (it would contradict the oracle), so the check is
two-sided. The run is sized for `--interp`, which takes about 2.5 minutes,
most of it the counting arm walking its 5001-slot table. Compiled, it takes
well under a second.

## Mutation testing

Seven edits to `differential.kara`, each built and run.

| # | mutation | outcome | properties that fired |
|---|---|---|---|
| M1 | the ★ arm deals both halves ascending | **killed** | P1, P5, P7 |
| M2 | quickselect for the lower median, `(n - 1) / 2` | silent (equivalent) | — |
| M3 | the virtual index drops the `\| 1` | **killed** | P2, P7, P8 |
| M4 | the counting arm deals the even slots first | **killed** | P3, P5, P7, P8 |
| M5 | the counting arm starts its scan at 4999 | **killed** (index panic) | — |
| M6 | quickselect pivots on the first element | silent (speed only) | — |
| M7 | the wiggle check accepts `a[i] == a[i - 1]` | **killed** | P1, P2, P3 |

M2 is an equivalent mutant: for even `n` either median works, and an
exhaustive Python check over every solvable input up to length 9 with values
`0..3` (299,070 inputs) found no counterexample. M6 changes only which pivot
quickselect tries first, so no output can see it. M5 survived until the
`5000` case was added: no generated input reached the bound, so a counting
arm that ignored the largest legal value passed every property.

## Verification

All three arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build`. `scripts/surface-sweep.py --filter
324- --timeout 400` reports `4 programs · 4 clean · 0 DIVERGENCES`. The three
arms are valgrind-clean at `-O0`. The ★ and counting arms' full output is
byte-identical to `wiggle_sort.py`.

The benchmark kernel's sink matches all four language twins and Python
(`sink 637694221 violations 0`). It is not run under `--interp`: at this size
the tree-walk backend would take far too long, and the arms and the
differential cover the same code on every backend.

## Benchmarks

`bench/wiggle_sort.kara` and its four mirrors time the **select arm**, not
the ★ arm. The ★ arm's cost is the standard library's sort, which is a
different algorithm in each of the five languages, so timing it would compare
five sorts rather than five compilers. The select arm is plain loops and
swaps, line for line the same in every mirror.

One buffer of 1,000,000 values is allocated once and run through 16 passes.
Each pass refills it with a fresh solvable input (even slots from `0..k`, odd
slots from `k..2k`, then a Fisher-Yates shuffle), with `k` cycling through 2,
3, 50 and 2500, from nearly every value repeated to nearly every value
distinct. Every draw is two LCG steps, a serial chain that cannot vectorise.
The buffer is then wiggle-sorted in place. After each pass the number of
wiggle violations (always 0) and a stride-9973 sample of the arrangement are
folded into a rolling hash, so the whole arrangement stays observable.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each, 5 warmups, on a 4-core x86-64 Linux container, karac
`0.1.0-dev.10181+gf2907d370` (the `B-2026-10-02-35` fix), measured
2026-10-02. Python is its own lane at 3 runs.

| implementation | mean | vs fastest |
|---|---|---|
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 357.7 ms ± 8.1 | 1.00× |
| c `clang -O3` | 363.8 ms ± 6.6 | 1.02× |
| rust `-O -C overflow-checks=on` (equal-safety) | 363.9 ms ± 9.6 | 1.02× |
| rust `-O` | 365.2 ms ± 13.8 | 1.02× |
| c `-march=x86-64-v3` (matched-ISA) | 366.4 ms ± 8.0 | 1.02× |
| **kāra `karac build`** | **366.9 ms ± 5.5** | **1.03×** |
| go `go build` | 623.6 ms ± 12.8 | 1.74× |
| python 3 | 24558 ms ± 299 | 68.7× |

**Kāra, C and Rust are tied.** The six compiled C, Rust and Kāra builds span
358 to 367 ms, every pair within about one standard deviation. Before
`B-2026-10-02-35` the Kāra row was 571.4 ms (1.57×), all of it in `Vec.swap`:
see Compiler findings. Go is 1.74× behind; that gap was not profiled.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 109.6 ms ± 2.6 | 15.7 KiB | 9.0 MiB |
| rust | 157.0 ms ± 2.5 | 3864.1 KiB | 9.5 MiB |
| kāra | 548.0 ms ± 13.4 | 396.5 KiB | 10.1 MiB |
| go | — | 2180.0 KiB | 9.7 MiB |
| python | — | — | 44.6 MiB |

Peak RSS is dominated by the 8 MB buffer, which every mirror allocates once.
`karac build` is 5.0× clang's cold compile and 3.5× rustc's. Its binary is
25× clang's and 9.7× smaller than rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

**One found, fixed in kara.** No correctness gaps: all three arms and the
differential were byte-identical on every surface from the first run.

- **[`B-2026-10-02-35`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) (perf): `Vec.swap` was a runtime call.** The
  first bench put Kāra at 571 ms against 364 ms for C and Rust, 1.57× slower,
  while Rust with overflow checks on was 367 ms, so checks were not the cause.
  Writing the five `swap` calls out by hand (`let t = a[i]; a[i] = a[j];
  a[j] = t;`) brought the same program to 378 ms, tied with C. Each `swap` had
  lowered to a call to `karac_vec_swap` in the runtime archive, which LLVM
  cannot inline into the partition loop. It is now two loads and two stores of
  the element type, and the bench runs 368 ms against C's 364 in the same
  session. The kata keeps the natural `a.swap(i, j)`.

All four files went through the Mend loop: `karac check` flagged 44
diagnostics over two passes (40, then 4), every one machine-applicable, and
`karac fix` applied them all. The first pass was all C-style operators
(`&&`, `||`, `!`), which Kāra spells `and`, `or` and `not`; they are parse
errors, so nothing later in the pipeline ran until they were gone. The second
pass removed `mut` from calls like `select(mut nums, ..)` where `nums` is
already a `mut ref` parameter, which forwards without a marker. Nothing in
this directory was changed to dodge a compiler gap.
