# 1130. Minimum Cost Tree From Leaf Values

Given an array `arr` of positive integers, consider all binary trees
such that:

- each node has either `0` or `2` children;
- the values of `arr` correspond to the values of each leaf in an
  in-order traversal of the tree;
- the value of each non-leaf node is equal to the product of the largest
  leaf value in its left and right subtree, respectively.

Among all possible binary trees considered, return the smallest possible
sum of the values of each non-leaf node. It is guaranteed this sum fits
into a 32-bit integer.

```
arr = [6,2,4]   ->  32
arr = [4,11]    ->  44
```

**Constraints:** `2 <= arr.length <= 40`; `1 <= arr[i] <= 15`.

The arms are `fn mct_from_leaf_values(arr: Vec[i64]) -> i64`.

## Approaches

Every non-leaf node joins two neighbouring runs of leaves, and the run
it makes stands for its largest leaf afterwards. A smallest leaf is best
joined first, to the smaller of its neighbours: it can only ever be
multiplied by something at least that large.

| file | mechanism |
|---|---|
| `mct_from_leaf_values.kara` ★ | a stack of leaves in decreasing order: a leaf that a larger or equal one comes after is joined to the smaller of its two neighbours, the leaf below it on the stack and the one arriving; what is left pairs off from the top. O(n) |
| `mct_from_leaf_values_dp.kara` | interval dynamic programming: the least cost over leaves `i..=j` is the least over every split of the two sides' costs and the product of their largest leaves, the widths in increasing order. O(n^3) |
| `mct_from_leaf_values_memo.kara` | the same recursion over ranges, top down: a range gives back its least cost and its largest leaf together, and each range's pair is kept in a `Map` keyed by `(lo, hi)`. O(n^3) |
| `mct_from_leaf_values_greedy.kara` | greedy removal: while more than one leaf is left, the smallest is joined to the smaller of its neighbours, the product paid and the smallest removed. O(n^2) |
| `mct_from_leaf_values_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, a `Vec<i32>` stack started with `i32::MAX`, `*stack.last().unwrap()`, `std::cmp::min`, a `for &a in arr.iter()` pattern), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 12 lines: the answers for LeetCode's two
examples and seven more (rising, falling, a valley, all alike, peaks
between ones, 1 to 15, and 40 of the largest, `8775`), then over 2000
random arrays of 2 to 40 leaves from 1 to 15 the costs summed and a
checksum (`2000 random arrays: costs total 3712815, checksum
857534466`), and two of LeetCode's largest: 40 leaves at random
(`3735`), and 40 rising and falling (`2634`). `mct_from_leaf_values.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every binary tree whose leaves are the array in order, each
non-leaf node the product of the largest leaf on its left and on its
right, and the least sum over all of them. It checks 2000 problems of 2
to 8 leaves in five kinds of 400: leaves from 1 to 15; from 1 to 3, so
many tie; from 1 and 2 alone; a mountain, sorted leaves rising then
falling; and a valley, falling then rising. Every random choice is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | the answer splits: it is the least, over every place to split the leaves, of the arm's answers for the two sides (a single leaf costing nothing) and the product of their largest leaves |
| P3 | the leaves reversed give the same answer |
| P4 | every leaf doubled makes every product, and the answer, four times as large |
| P5 | a new leaf above every other at the end adds it times the old largest, since it is joined last |
| P6 | a leaf of 1 at the end, at or below every other, adds the old last leaf, since it is joined first |

All 60,000 checks pass on every arm: `2000 problems: checksum
228815600, 60000 checks over 5 arms: 0 failures`. A Python reading of
the same problems, an interval recursion over every split, gives the
same checksum.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`
(the memo arm keeps a `Map`), each failing the same way under both. All
thirty are caught. Fifteen are kept, no two failing the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a leaf joined to the larger of its neighbours | P1 915, P2 793, P3 675, P5 1277, P6 367 |
| M2 | ★: a leaf with nothing below it on the stack paying nothing | P1 1457, P2 1285, P3 1716, P5 2000, P6 35 |
| M3 | ★: the first leaf skipped | P1 2000, P2 1874, P3 1465, P5 543 |
| M4 | dp: the right side's largest taken from the split leaf on | P1 1359, P2 1277, P3 1679, P5 1277, P6 1598 |
| M5 | dp: the widest ranges first | P1 1706, P2 1706, P5 2000, P6 2000 |
| M6 | dp: each range's first leaf left out of its largest | P1 2000, P2 2000, P5 2000, P6 2000 |
| M7 | memo: a single leaf costing its value | P1 2000, P2 1829, P4 2000, P5 2000, P6 2000 |
| M8 | memo: the root always split after the first leaf | P1 968, P2 867, P3 1271, P5 2000 |
| M9 | memo: a remembered range one too dear | P1 811, P2 706, P3 1125, P4 811, P5 1706, P6 420 |
| M10 | greedy: the last leaf never taken for the smallest | P1 523, P2 418, P3 835, P5 523, P6 910 |
| M11 | greedy: the last pair never paid | P1 2000, P2 1775, P5 2000 |
| M12 | greedy: the leaves sorted first | P1 854, P2 566, P6 1250 |
| M13 | solution: a leaf joined to the arriving one always | P1 240, P2 200, P3 530, P5 1277 |
| M14 | solution: leaves above 9 clipped to 9 | P1 1048, P2 1048, P4 1186, P5 1092, P6 464 |
| M15 | solution: the cost counted from 1 | P1 2000, P2 493, P4 2000 |

P1 and P2 catch all fifteen, P5 thirteen, P6 ten, P3 eight and P4
four. P2 calls the arm again on the two sides of every split, so an edit
that is wrong the same way on every array can still agree with itself:
it sees the cost counted from 1 (M15) on 493 problems, where a single
leaf's side costs nothing and the others carry the extra 1. P4 sees only
the edits that add or clip a constant (M7, M9, M14, M15): every other
wrong answer is made of the same products and grows fourfold with them.
P3 sees eight, edits whose answer for the leaves reversed differs from
their answer for the leaves as given. P5 and P6 see nearly everything that gets a
join wrong, since a new largest leaf is joined last and a new smallest
first, and the sorted greedy (M12) only through P6: a new largest leaf
at the end is already in sorted place.

Of the fifteen not kept, none fails exactly as a kept one, and two pairs
fail alike: the last two leaves left never paired, in the ★ and solution
arms, and the right side's cost taken from the split leaf on or the left
side's cost dropped, in the dp arm. The other eleven fail each in a way
of its own and were not needed.

## Verification

Every arm prints the same output as `mct_from_leaf_values.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The kata found no gap. The ★, dp, memo and greedy arms were written as
Kāra and checked clean as written. The memo arm first read each side's
largest leaf off a slice, `arr[lo..k].iter().max()`, at every split:
O(n^4), and 100 s under `karac __mir-run`, past the corpus's 60 s. It
now has each range give back its largest leaf with its cost.

`karac fix` carried the solution arm in three rounds: `Vec<..>` to `[..]`, `i32::MAX` to `i32.MAX`, the `&a`
and `&x` patterns to `a` and `x`, `std::cmp::min` to `min` and `::` to
`.`; then `struct Solution {}` declared; then `vec![..]` to `[..]`, the
cost declared `i32` where it is summed from `i32` products, and the `as
i64` at the call dropped, an `i32` widening by itself.

## Benchmarks

The bench builds 4096 random arrays of 40 leaves once, LeetCode's
largest, their leaves 1 to 15. Each of 400 rounds changes one leaf of
every array and answers the array with the ★ arm: 1,638,400 calls.
Every implementation prints `400 rounds over 4096 arrays of 40 leaves:
costs total 6000540134, checksum 269597299`. Each keeps an array as its
own allocation (`Vec[i64]`, `Vec<i64>`, `[]int64`, a Python list, and
C's `int64_t *`) and grows a fresh stack in every call.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `2d47b8e713`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.429 to 0.523 s | 0.489 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.464 to 0.562 s | 0.505 s |
| Rust (`rustc -O`) | 0.493 to 0.639 s | 0.526 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.542 to 0.604 s | 0.565 s |
| Kāra (`karac build`) | 0.487 to 0.622 s | 0.567 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.498 to 0.588 s | 0.573 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.537 to 0.629 s | 0.587 s |
| Go | 0.616 to 0.737 s | 0.679 s |
| Python | 9.4 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra takes about 1.17x C's time and about Rust's under overflow
checks (1.01x); all three walk the same leaves and push to a stack that
is allocated and grown in every call. Go takes about 1.18x Kāra's time.
Python takes about 16x Kāra's time.
