# 1090. Largest Values From Labels

There is a set of `n` items. You are given two integer arrays `values`
and `labels` where the value and the label of the `i`th element are
`values[i]` and `labels[i]`. You are also given two integers `numWanted`
and `useLimit`.

Choose a subset `s` of the `n` elements such that:

- the size of the subset `s` is **less than or equal to** `numWanted`;
- there are **at most** `useLimit` items with the same label in `s`.

The **score** of a subset is the sum of the values in the subset.
Return the maximum **score** of a subset `s`.

```
values = [5,4,3,2,1], labels = [1,1,2,2,3], numWanted = 3, useLimit = 1  ->  9
values = [5,4,3,2,1], labels = [1,3,3,3,2], numWanted = 3, useLimit = 2  ->  12
values = [9,8,8,7,6], labels = [0,0,0,1,1], numWanted = 3, useLimit = 1  ->  16
```

**Constraints:** `n == values.length == labels.length`; `1 <= n <= 2 * 10^4`;
`0 <= values[i], labels[i] <= 2 * 10^4`; `1 <= numWanted, useLimit <= n`.

The arms are `fn largest_vals_from_labels(values: Vec[i64], labels:
Vec[i64], num_wanted: i64, use_limit: i64) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `largest_values_from_labels.kara` ★ | greedy: the items as (value, label) pairs, sorted by value from the largest (`sort_by(\|a, b\| b.0.cmp(a.0))`), taken in that order, skipping one whose label is spent, until `num_wanted` are taken; uses per label in a `Map[i64, i64]`. Taking the largest value that fits never stops a better choice, since the choices form a matroid. O(n log n) |
| `largest_values_from_labels_heap.kara` | a max-heap: every pair pushed into `PriorityQueue.max_first()` and popped until `num_wanted` are taken or the heap is empty, a spent label's item popped and dropped. O(n log n), less when `num_wanted` is small |
| `largest_values_from_labels_groups.kara` | by label: the values grouped in a `Map[i64, Vec[i64]]` (`entry(..).or_insert(Vec.new()).push(..)`), each group sorted, reversed and cut to `use_limit` (`truncate`), the survivors pooled, sorted, and the first `num_wanted` summed (`iter().take(..).sum()`). O(n log n) |
| `largest_values_from_labels_buckets.kara` | counting by value: values and labels are small integers, so the labels go into a bucket per value (`Vec.filled(top + 1, [])`, a `Vec[Vec[i64]]`) and the buckets are walked from the top down, uses per label in a `Vec[i64]`. No comparison sort. O(n + V + L) for V and L the largest value and label |
| `largest_values_from_labels_chain.kara` | one iterator chain: the indices sorted by value from the largest (`sort_by_key(\|i\| -values[i])`), a `filter` whose closure counts each label's uses in a captured `Map` through `entry(..).or_insert(0)` and passes an item while its label has uses left, `take(num_wanted)`, the values `map`ped and `sum`med. The closure's count is right because `take` stops pulling once it has enough. O(n log n) |
| `largest_values_from_labels_solution.kara` | LeetCode's Rust template (`use std::collections::HashMap`, `struct Solution;`, `values.into_iter().zip(labels.into_iter())`, `sort_unstable_by(\|a, b\| b.0.cmp(&a.0))`, `*used.entry(l).or_insert(0)`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the best choice found without the greedy, six properties |

Every arm prints the same 14 lines: LeetCode's three examples and nine
more (one item, all values 0, every label alike, every label distinct,
a tie at the cut), a sum and checksum over 2000 random problems of 1 to
20 items (`answers sum to 142896, checksum 667507229`), and three
answers on one problem of 2 * 10^4 items, LeetCode's largest
(`126516296, 79857585, 1991377`). `largest_values_from_labels.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and two ways to find
the best choice that do not take the largest values first: every subset
of a problem of up to 12 items, and above that a knapsack over labels
(`best[j]`, the most `j` items can sum to from the labels seen so far,
each label adding its `t` largest values for each `t` up to
`use_limit`). It checks 2000 problems: 1400 of 1 to 12 items and 600 of
1 to 30, values 0 to 20 and labels 0 to 5, so ties and spent labels are
common, `num_wanted` and `use_limit` 1 to n. Every random choice is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the best choice found without the greedy |
| P2 | one more wanted loses nothing and adds no more than the largest value |
| P3 | a looser limit loses nothing, and a limit of n gives the sum of the `num_wanted` largest values |
| P4 | the items in the other order give the same answer |
| P5 | every value raised by `shift` (1 to 5) adds `shift` for each item taken, which is as many as the labels allow, up to `num_wanted` |
| P6 | every value doubled and the labels renamed (`(5 - l) * 7 + 3`) doubles the answer |

All 72,000 checks pass on every arm: `2000 problems: checksum 522706986,
72000 checks over 6 arms: 0 failures`. A Python reading of the same
problems, with `itertools.combinations` for the small ones and each
label's `use_limit` largest values pooled for the rest, gives the same
checksum.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. Three are equivalent on purpose and must survive, and do:
the heap arm's `None => break` spelled another way, the chain arm's
`take` moved after its `map`, and the buckets arm never visiting the 0
bucket (a 0 adds nothing). The other 27 are all caught. Fifteen are
kept, no two failing the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one item fewer than wanted | P1 1787, P3 1915, P5 1860 |
| M2 | ★: the items sorted by label | P1 1439, P3 1410, P4 890, P6 1363 |
| M3 | ★: each label used once more than the limit | P1 197, P5 140 |
| M4 | heap: `PriorityQueue.new()`, smallest first | P1 1615, P3 1566 |
| M5 | heap: each item counted twice | P1 1487, P3 1534, P5 1505 |
| M6 | heap: (label, value) pairs | P1 1996, P3 1996, P5 2000, P6 1997 |
| M7 | groups: each label keeps its smallest values | P1 376 |
| M8 | groups: the pool summed from the smallest | P1 1419, P3 1566 |
| M9 | groups: the largest value dropped | P1 1955, P3 1952, P5 579 |
| M10 | buckets: the largest value never visited | P1 1995, P3 1995, P5 492 |
| M11 | buckets: labels summed in place of values | P1 1995, P2 1, P3 1995, P4 225, P5 2000, P6 2000 |
| M12 | buckets: a bucket finished past `num_wanted` | P1 258, P2 116, P3 289, P5 273 |
| M13 | chain: one fewer per label | P1 623, P3 147, P5 569 |
| M14 | chain: one more than wanted | P1 1356, P3 1485, P5 1421 |
| M15 | solution: the labels paired in reverse | P1 189 |

P1 catches all fifteen. P3 catches twelve, P5 ten, P6 three, P4 two
and P2 two. P2 is the weakest: one more item wanted moves the answer by
no more than the largest value under every edit but the two that take
too many or sum labels. M7 and M15 show why P1 is needed: each label
keeping its smallest values and the labels paired in reverse pass all
five properties, giving a consistent wrong answer that only the best
choice refutes. A label used once too often (M3) is seen besides only
by P5, which predicts how many items are taken from the labels alone.

Of the twelve caught but not kept, eleven fail exactly as a kept edit:
the ★ arm from the smallest value and the chain arm's likewise as M4;
the ★ arm's label never spent, the groups arm keeping one more per
label, the buckets arm allowing one more, the chain arm's label never
spent and the solution arm's two likewise as M3; the solution arm
sorted by label as M2; the heap arm's one pop too many and the
solution arm's one more wanted as M14. The groups arm summing labels
fails on its own (`P1 1996, P3 1996, P5 2000, P6 1998`), next to M6,
and was not needed.

## Verification

Every arm prints the same output as `largest_values_from_labels.py`
under `karac __mir-run` (the v2 MIR interpreter), `karac
__mir-llvm-run`, and `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer) with no error. `karac run` and a `karac build` binary
print the same output for every arm and the differential. `karac check
--output=json` reports nothing on any file. Under `karac __mir-run` the
differential takes 15 s.

Every file went through `karac fix`. The ★ arm was written with Rust's
`used.get(label).copied().unwrap_or(0)`; Kāra's `Option[ref T]` has no
`copied`, and the fix wrote `.cloned()`. The buckets arm was written
with `&&`, which the fix made `and`. The Rust arm reaches a clean check
in three rounds: first the syntax (`HashMap<i32, i32>` to `HashMap[i32,
i32]`, `HashMap::new` to `HashMap.new`, `struct Solution;` to `struct
Solution {}`, `&a.0` to `a.0`, the `use` line deleted); then `HashMap`
to `Map`; then `sort_unstable_by` to `sort_by`, `sum` typed `i32` for
the return, and `values.into_iter()` on a borrowed parameter to
`values.clone().into_iter()`. The fix left a blank line where the `use`
line was, which the arm does not keep.

The heap arm was first written as a Rust reader expects a heap to work,
`PriorityQueue.new()`, and gave the smallest answers: Kāra's
`PriorityQueue.new()` pops the smallest first, as Java's and Python's
do, and `max_first()` the largest (docs/library/collections.md). That
is the documented design, not a gap. The fix knows it from the Rust
side: `BinaryHeap::new()` becomes `PriorityQueue.max_first()` in two
rounds, with a message naming the difference.

## Benchmarks

The bench builds 100 random problems of 2 * 10^4 items, LeetCode's
largest, values 0 to 20000 and labels 0 to 999, once. Each of 20 rounds
answers every problem with the ★ arm at its own `num_wanted` (1 to
20000) and `use_limit` (1 to 20), folding the answers into a checksum.
Every implementation prints `20 rounds over 100 problems of 2 * 10^4
items: answers sum to 175942311587, checksum 466448257`. Each mirror
builds the pairs, sorts them by value with its language's library sort
and counts uses in its hash map: Rust `sort_by` and `HashMap`, Go
`slices.SortStableFunc` and a `map`, Python `list.sort` and a `dict`, C
`qsort` and an open-addressing table rebuilt per call, as Kāra's `Map`
is. `qsort` is not stable; the answer does not need it, since items of
equal value are interchangeable to the greedy.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `038e120694`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.451 to 1.676 s | 1.538 s |
| Kāra (`karac build`) | 1.478 to 1.794 s | 1.537 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 1.684 to 1.824 s | 1.747 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.638 to 1.898 s | 1.760 s |
| Rust (`rustc -O`) | 1.662 to 1.915 s | 1.805 s |
| C (`clang -O3 -march=x86-64-v3`) | 6.798 to 7.350 s | 6.954 s |
| C (`clang -O3`) | 6.803 to 7.265 s | 7.076 s |
| Go | 11.257 to 12.435 s | 11.572 s |
| Python | 18.0 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte.

The sort is most of the work: 2000 sorts of 2 * 10^4 pairs, against
2000 walks that stop at `num_wanted`. Without its `sort_by` the Kāra
program takes 0.59 s, so the sort is about 0.95 s of its 1.54 s. That
is also why the languages spread so far: each runs its library's sort.
Kāra's compiled `sort_by` samples its input and, finding no runs to
merge, partitions it and merge-sorts the short ranges left (kara
`src/backend/mir/callable.rs`, `build_part_sort`); Rust's is its own
hybrid (driftsort). Kāra is 12% ahead of overflow-checked Rust and 15%
ahead of plain `rustc -O`, which here is no faster than the checked
build. glibc's `qsort` calls its comparison through a pointer for every
pair and puts C at 4.6x Kāra; a C port of the bottom-up merge sort Kāra
uses when it does not partition (kara `runtime/src/mir.rs`,
`merge_widths`, whose schedule the compiled merge shares) took 4.5 s, so the plain merge alone
does not reach Kāra either. Go's stable sort is insertion sort and
in-place merging, O(n log^2 n), and puts Go at 7.5x; its `sort.SliceStable`,
which also swaps through reflection, took 36.7 s. Python takes 12x.
