# 352. Data Stream as Disjoint Intervals

Non-negative integers arrive one at a time. At any point, report the numbers
seen so far as a sorted list of disjoint intervals `[start, end]`.

```
add 1  ->  [1, 1]
add 3  ->  [1, 1] [3, 3]
add 7  ->  [1, 1] [3, 3] [7, 7]
add 2  ->  [1, 3] [7, 7]
add 6  ->  [1, 3] [6, 7]
```

**Constraints:** `0 <= value <= 10^4`; at most `3 * 10^4` calls to `addNum`
and at most `10^2` to `getIntervals`. The follow-up asks for the case where
there are many merges and few disjoint intervals.

## Approaches

| file | mechanism | cost |
|---|---|---|
| `summary_ranges.kara` ★ | a `SortedMap` from each interval's start to its end; a new value looks at the interval starting at or before it (`floor`) and the one starting just after it (`ceiling`), then joins the left one, the right one, both, or neither | `add_num` `O(log k)`, `get_intervals` `O(k)` for `k` intervals |
| `summary_ranges_sorted_vec.kara` | two sorted `Vec`s of starts and ends and a hand-written binary search; joining two intervals removes an entry, a lone value inserts one | `O(log k)` to find the place plus `O(k)` to shift |
| `summary_ranges_union_find.kara` | union-find over the values `0..=10000`; every link points left to right, so `find(x)` is the end of `x`'s run | `add_num` near `O(1)` amortized, `get_intervals` `O(range)` |
| `summary_ranges_bitset.kara` | 157 words of 64 bits; a run is found by counting trailing zeros, so empty and full words are skipped 64 values at a time | `add_num` `O(1)`, `get_intervals` `O(range / 64 + k)` |
| `differential.kara` | the four arms and an independent oracle, 2551 checks, five properties | — |

Every arm prints the same 18 lines: the example step by step, an empty
report, a set of edge cases (a repeat, a value inside an interval, both ends
of the range, a bridge, a descending run), and a stream of 30,000 values over
`0..=10000` with a report every 3,000 values and a checksum over every
report. `summary_ranges.py` mirrors the ★ arm with `bisect` standing in for
the sorted map, and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and an oracle that shares
no code with them: it marks each value in a presence table and rebuilds the
intervals by a plain scan after every value. Four streams over ranges of 10,
41, 301 and 10,001 values feed all of them, and the widest stream is forced
through `0`, `1`, `9999` and `10000` so runs touch both ends of the range.

| | property |
|---|---|
| P1 | after every value, all four arms report the oracle's intervals |
| P2 | the intervals are sorted, disjoint and not adjacent (each start is at least the previous end + 2), and cover exactly the distinct values seen |
| P3 | adding a value already seen changes nothing |
| P4 | adding a new value changes the interval count by +1, 0 or -1, as decided by whether `v - 1` and `v + 1` were seen |
| P5 | the same 200 values added forwards, backwards and sorted give the same intervals |

It prints `failures 0` and all properties hold on every surface, with
`2551 checks, checksum 227241706`. An independent Python replay of the
streams and the oracle gives the same check count and checksum.

## Mutation testing

Twelve edits to the copies inside `differential.kara`, each built and run.
All twelve are killed.

| # | mutation | how |
|---|---|---|
| M1 | map: treat a value equal to an interval's end as new | P1–P5, 1365 failures |
| M2 | map: join the left interval when it ends at `v` rather than `v - 1` | P1–P5, 1620 failures |
| M3 | map: keep the right interval after merging it | P1–P5, 1600 failures |
| M4 | vectors: binary search for the first start `>= v` instead of `> v` | P1 and P5, 733 failures |
| M5 | vectors: a bridge keeps `v` as the end instead of the right interval's end | P1, 468 failures |
| M6 | union-find: never link `v - 1`'s run to `v` | P1, 755 failures |
| M7 | union-find: step one value at a time after a run instead of jumping past it | P1, 778 failures |
| M8 | bitset: stop complementing the words when searching for a clear bit | P1, 604 failures |
| M9 | bitset: set bit `v % 63` instead of `v % 64` | P1, 699 failures |
| M10 | oracle: stop a run one short of the top of the range | P1, 225 failures |
| M11 | P2: require a gap of two values between intervals instead of one | P2, 837 failures |
| M12 | union-find: link `v + 1`'s run to `v` instead of the reverse | the program never finishes: the reversed link makes a cycle |

Three earlier candidates were equivalent and were replaced: removing either
of two equal ends after a bridge, jumping two values past a run's end (the
value after a run is never seen), and linking `v` straight to `v + 1` rather
than to its root.

## Verification

All four arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build` (`scripts/surface-sweep.py`, 5
programs, 0 divergences), and the four arms match `summary_ranges.py` byte
for byte. Built with `KARAC_AUTO_PAR=0`, all five are valgrind-clean:
`0 errors` and `0 bytes in use at exit`. The differential takes 26 seconds
under `karac run --interp` on a release build.

## Benchmarks

`bench/summary_ranges.kara` and its four mirrors time the **sorted-vector
arm**, the one arm that is the same algorithm in C, Rust, Go and Python (the
★ arm's `SortedMap` has no C equivalent). Each of 150 rounds starts an empty
structure, feeds it a 30,000-value stream over `0..=10000` seeded by the
round, and folds every 3,000th report into the sink with the round number,
so no round can be skipped or hoisted. All five print `sink 232124774`.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each, 5 warmups, on a 4-core x86-64 Linux container, karac
`0.1.0-dev.10553+g87d927e95` (kara main with both fixes below), measured
2026-10-06, with the timed lane built with `KARAC_AUTO_PAR=0`. Python is its
own lane at 3 runs.

| implementation | mean | vs fastest |
|---|---|---|
| rust `-O -C overflow-checks=on` (equal-safety) | 445 ms ± 15 | 1.00× |
| **kāra `karac build`** | **455 ms ± 10** | **1.02×** |
| c `-march=x86-64-v3` (matched-ISA) | 455 ms ± 15 | 1.02× |
| c `clang -O3` | 457 ms ± 14 | 1.03× |
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 471 ms ± 46 | 1.06× |
| rust `-O` | 477 ms ± 38 | 1.07× |
| go `go build` | 701 ms ± 25 | 1.57× |
| python 3 | 7129 ms ± 1071 | 16.0× |

**Kāra ties equal-safety Rust (1.02×) and C (level).** The work is a binary
search over a few thousand starts plus a `memmove` per insert or remove, and
every compiled language compiles it to much the same loop. Go is 1.57× behind, as
on most of the vector-heavy katas. Python is 16× behind, against 40× on the
recursion-heavy #351; its list `insert` and `del` shift in C, which probably
accounts for some of that, though it was not measured.

Outside the harness, the ★ arm built as written takes 10.1 ms against 4.7 ms
for the sorted-vector arm (hyperfine, 20 runs), so the `SortedMap` costs about
2× here. Before the fix below it took 2.27 s.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 108.5 ms ± 5.6 | 15.8 KiB | 1.6 MiB |
| rust | 158.0 ms ± 10.0 | 3865.4 KiB | 2.2 MiB |
| kāra | 369.2 ms ± 11.3 | 341.6 KiB | 2.4 MiB |
| go | — | 2178.9 KiB | 7.0 MiB |
| python | — | — | 8.3 MiB |

`karac build` is 3.4× clang's cold compile and 2.3× rustc's. Its binary is
22× clang's and 11× smaller than rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

The ★ arm is the natural way to write this problem, and it found two
performance gaps in the compiler, both fixed in the kara repo, plus two gaps
in the documented `SortedMap` / `SortedSet` surface, filed there.

- **B-2026-10-06-65 (runtime and codegen): compiled `SortedMap` `floor` /
  `ceiling` / `min` / `max` sorted every key on every call.** A compiled
  `SortedMap` is a hash table, and each ordered query gathered all of its
  keys into a fresh buffer, sorted it and scanned it, so the ★ arm took
  2.27 s against 8 ms for the same algorithm on a sorted `Vec`. The runtime
  now keeps an ordered index beside the table, and the ★ arm runs in 10 ms.
- **B-2026-10-06-66 (interpreter): every method call on a `SortedMap` or
  `SortedSet` copied the whole tree.** Under `karac run --interp` the ★ arm
  took 23 s, nine times its sorted-`Vec` arm. Sorted containers now share
  their storage as `Map` and `Set` already did, and the ★ arm takes 1.2 s,
  the fastest of the four.
- **B-2026-10-06-67 (open): `SortedSet.range` is documented but missing.** The
  design document lists it, and every surface rejects it.
- **B-2026-10-06-68 (open): the `SortedMap` table in the design document does
  not match the implementation.** It calls `range(from, to)` half-open, while
  both backends return the inclusive `[from, to]`, and it leaves out `floor`
  and `ceiling`, the two methods this kata is built on.

Writing a test for the interpreter fix also turned up B-2026-10-06-69 (open,
codegen): a `Set` copied through a struct field gets the wrong value size,
and a later `remove` on it overwrites the stack. None of the arms do this.

The author already knows the language, so none of this counts toward the
machine-fix rate.
