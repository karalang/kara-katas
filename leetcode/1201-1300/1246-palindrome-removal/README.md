# 1246. Palindrome Removal

You are given an integer array `arr`. In one move, you can select a
palindromic subarray `arr[i], arr[i + 1], ..., arr[j]` where `i <= j`,
and remove that subarray from the given array. When a subarray is
removed, the elements on its left and on its right move to fill the gap.

Return *the minimum number of moves needed to remove all numbers from
the array*.

```
arr = [1, 2]           ->  2
arr = [1, 3, 4, 1, 5]  ->  3   (remove [4], then [1, 3, 1], then [5])
```

**Constraints:** `1 <= arr.length <= 100`; `1 <= arr[i] <= 20`.

The arms are `fn minimum_moves(arr: Vec[i64]) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `palindrome_removal.kara` ★ | interval dynamic programming, rows from the last: `arr[i]` goes in a move of its own, with an equal `arr[i + 1]`, or riding along on the last move that clears everything between it and a later equal `arr[k]` |
| `palindrome_removal_memo.kara` | the same recurrence asked from the top: a recursive `clear(i, j)` with a `mut ref` table of answers, `-1` for not yet known |
| `palindrome_removal_split.kara` | interval dynamic programming by length, split form: the best split into two parts cleared one after the other, or, for equal ends, the inside with the ends riding along on its last move |
| `palindrome_removal_flat.kara` | the ★ recurrence in one flat `Vec` indexed `i * (n + 1) + j`, the later equal values a `filter`, `map` and `min` over a range |
| `palindrome_removal_solution.kara` | a Rust solution as LeetCode's Rust users write it (`vec![vec![0i32; n]; n]`, inclusive ranges `(i + 2)..=j`, `if` expressions for the empty edges), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, four more properties |

Every arm prints the same 3 lines: LeetCode's two examples; the total of
the answers and a checksum of them for 1000 random arrays of 1 to 100
values drawn from 1 to `v` distinct values, `v` itself random from 1 to
20, so that palindromes are common in some and rare in others (`total
17449, checksum 838854406`); and three arrays of 100 values, the
constraints' top: from 1 to 20, from 1 to 2, and a hill up from 1 to 50
and back down. `palindrome_removal.py` mirrors the ★ arm, and its output
is byte-identical. Every arm gives the same output under `karac run`
and `karac build`, and under the AddressSanitizer build.

The Mend loop: the four Kāra arms checked clean as first written. The
solution arm takes one round of fixes, 5 by `karac fix`'s count, and
then checks clean: `struct Solution;` to `struct Solution {}`,
`Vec<i32>` to `Vec[i32]`, and `vec![vec![0i32; n]; n]` to
`Vec.filled(n, Vec.filled(n, 0i32))`. Its `usize` arithmetic, inclusive
ranges and `if` expressions carry over as written.

A tempting shortcut, collapsing runs of equal values first (`dedup`),
is wrong, and the differential's literal reading is what showed it:
`[1, 1, 2, 2, 1, 1, 1, 2, 1]` takes 2 moves, but collapsed it is `[1, 2,
1, 2, 1]`, one palindrome. A run can be split between two moves, and
collapsing it makes a palindrome the array never had.

## Gaps

None found: every arm, as written, checks after its fixes, and runs and
builds alike.

## Differential

`differential.kara` holds copies of the five arms, renamed, and the
statement read literally: every move there is, every subarray that
reads the same both ways taken out and the rest closed up, recursively,
the fewest moves over all of them, each array met once kept in a
`Map[Vec[i64], i64]`. 2000 random arrays of 1 to 10 values from 1 to
`v`, `v` from 1 to 4.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the array reversed gives the same answer |
| P3 | between 1 and `n`, and 1 exactly when the array is a palindrome |
| P4 | the values renamed by a random permutation of 1 to 20 give the same answer |
| P5 | the array and another of up to 10 values end to end take no more moves than the two apart |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 arrays: checksum 620575255,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the
same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: two equal neighbours removed in no move at all | P1 1025, P3 721, P6 4100 |
| S2 | ★: a later equal value two or more away never paired | P1 719, P3 277, P6 2876 |
| M1 | memo: the paired value cleared again on the right | P1 1377, P2 206, P3 520, P6 1377 |
| M2 | memo: neighbours paired when they differ, not when equal | P1 916, P3 486, P6 916 |
| P1 | split: equal ends cost one more than their inside | P1 1431, P3 520, P6 1431 |
| P2 | split: the split after the first value never tried | P1 239, P2 377, P5 25, P6 239 |
| F1 | flat: no later equal value read as a cost of 0 | P1 2000, P3 2000, P6 2000 |
| F2 | flat: later values paired with `arr[i + 1]`, not `arr[i]` | P1 599, P2 517, P3 171, P6 599 |
| L1 | solution: a value on its own costs two moves | P1 623, P2 511, P3 148, P5 78, P6 623 |
| L2 | solution: one value left after the paired one taken as already cleared | P1 425, P2 456, P3 174, P5 15, P6 425 |

All ten are caught, every one by P1, the statement read literally, and
by P6, which fails on the other four arms too when the ★ arm is the one
mutated (S1, S2). P3, the bounds, catches all but P2: a missed split
still gives an answer between 1 and `n`, and a palindrome still in one
move. P2, the array reversed, catches five (M1, P2, F2, L1, L2), and P5,
two arrays end to end, three (P2, L1, L2). P4, the values renamed, catches none: no mutation looks at what the
values are, only at which are equal.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (interval dynamic programming, rows from the last) on 1000 random
arrays of 100 values built once, each from 1 to v distinct values with v
from 1 to 20, each asked twice; every answer folded into a checksum.
Every program prints `2 rounds of 1000 arrays of 100 values: checksum
33024857`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.490 to 0.563 s | 0.498 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.491 to 0.527 s | 0.510 s |
| Rust (`rustc -O`) | 0.444 to 0.533 s | 0.461 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.382 to 0.437 s | 0.395 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.386 to 0.444 s | 0.392 s |
| C (`clang -O3`) | 0.508 to 0.576 s | 0.526 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.462 to 0.561 s | 0.475 s |
| Go | 0.560 to 0.650 s | 0.603 s |
| Python | 18.07 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on is about 23% ahead of Kāra (0.395 s
against 0.510 s). C runs level with Kāra (0.526 s against 0.510 s); Kāra
is about 15% ahead of Go (0.510 s against 0.603 s). Python takes about
35x Kāra's time. No profile was taken.
