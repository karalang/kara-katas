# 823. Binary Trees With Factors

Given an array of unique integers `arr`, each greater than 1, count the
binary trees that can be made from them, each value used any number of
times, where every node that is not a leaf holds the product of its two
children's values. Return the count modulo `10^9 + 7`.

```
arr = [2,4]       ->  3     2, 4, and 4 over (2, 2)
arr = [2,4,5,10]  ->  7     2, 4, 5, 10, 4 over (2, 2), 10 over (2, 5) and 10 over (5, 2)
```

**Constraints:** `1 <= arr.length <= 1000`, `2 <= arr[i] <= 10^9`, and
the values are unique.

## Approaches

A tree with root x is a leaf, or a tree of a beside a tree of b, for any
two values a and b, in either order, with a * b = x. Both factors are
smaller than x, so x's count follows from the counts of smaller values:
1 plus, for each ordered pair of factors, the product of their counts.

| file | mechanism |
|---|---|
| `num_factored_binary_trees.kara` ★ | the values sorted, and each value's count from every smaller value that divides it whose cofactor is in a map of the counts so far. O(n^2) |
| `num_factored_binary_trees_pointers.kara` | the values sorted, and for each value two pointers, one up from the smallest and one down from the value below, meeting at each pair of factors; a pair of two different values counts twice, a square once. No map. O(n^2) |
| `num_factored_binary_trees_memo.kara` | the definition as a recursion over a set of the values, every value tried as the left factor, with a memo of the counts worked out; no sorting. O(n^2) |
| `num_factored_binary_trees_iter.kara` | a `fold` over the sorted values building the map of counts, each value's count 1 and a `sum` over a `filter_map` of its factor pairs, and the answer a `fold` over the map's `values()` |
| `differential.kara` | the four arms against the statement counted tree by tree, four properties |

Every arm prints the same 11 lines: LeetCode's two examples; six small
cases (one value; powers of 2 to 8 and to 16; two sets of small values
in no order with several factor pairs each; and 10^9 with its factors
10^4 and 10^5, 10 and a value that divides nothing); two sets of
LeetCode's largest size, 1,000 values, the smallest numbers 2^a 3^b 5^c,
which have many factor pairs, and 1,000 odd values that have none; and
300 random sets of up to 15 values up to 60, with a total and a
checksum. `num_factored_binary_trees.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement
counted tree by tree: the values taken smallest first, and for each one
every ordered pair of values tried by multiplying, with no division, no
lookup and no modulus. Its 1,600 cases have up to 12 values each and
come in four kinds of 400: values up to 60; values 2^a 3^b up to 2^7
3^4, with many factor pairs; values up to 1,000, with few; and large
values, two random factors up to 31,622 with their product and a random
value up to 10^9 for each draw. 654 cases have a value that is the
product of two.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the values in reverse order give the same answer |
| P3 | a value above the square of the largest, which divides none and is no product, adds exactly 1 |
| P4 | the answer is the number of values when none is a product of two, and more otherwise |

It prints `1600 cases (654 with a value that is a product of two), 25600
checks over 4 arms: 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each pair of factors in one order only | P1 609 |
| M2 | ★: a leaf not counted | P1 1600, P3 1600, P4 1600 |
| M3 | ★: the right child's trees not counted | P1 73 |
| M4 | pointers: a square's pair counted twice | P1 129 |
| M5 | pointers: a pair of two values counted once | P1 609 |
| M6 | pointers: the value just below never a factor | P1 142, P4 56 |
| M7 | memo: a cofactor that is no value accepted | stack overflow |
| M8 | memo: a leaf not counted | P1 1600, P3 1600, P4 1600 |
| M9 | memo: the right child's trees not counted | P1 73 |
| M10 | iter: each pair counted twice | P1 654 |
| M11 | iter: the values not sorted | P1 196, P2 607, P4 95 |
| M12 | iter: a square's pair dropped | P1 129, P4 45 |

P1 kills eleven, and M7 dies of a stack overflow: with every value
accepted as a cofactor, a value is its own left factor, so the recursion
calls itself on the same value before that value's count is stored. M10
fails on all 654 cases with a product, since every count with a pair
grows. The same mistake in two arms fails on the same numbers of cases:
one order only in M1 and M5, the right child left out in M3 and M9, and
a square's pair miscounted in M4 and M12, twice or not at all. P2 sees
only M11, the one arm whose answer depends on the order of its input. P4
sees an edit only when it loses a value's only pair or every leaf.

## Verification

Every arm prints the same output as `num_factored_binary_trees.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The release build
that runs `check` and `__mir-run` and the debug build that runs
`__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` are both at kara
`36a43d8e50`, with the runtime archives built from that tree.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`), the legacy JIT
(`karac run`), `karac build` and an auto-par build print the same output
for the ★, two-pointer and memo arms. Legacy's checker refuses the
iterator arm and the differential, finding no `Add` for the item type of
the `filter_map` it is asked to `sum`, and the bench program, as it
takes `sets[round % count]` passed to a function as a move out of an
index. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It lists the
5,193 numbers 2^a 3^b 5^c 7^d from 2 to 10^9, which have many factor
pairs, and draws 64 sets of 1,000 of them once, LeetCode's largest, in
random order. Each of 1,000 rounds answers the next set afresh: a copy
sorted, then about 500,000 trial divisions, a map lookup for each that
divides, and a modulus for each pair found. Every implementation prints
`5193 values, 1000 rounds of 64 sets: total 23003517862, checksum
961133017`, the Kāra program under `karac __mir-run` included, in 102 s
with the interpreter's step limit raised by `KARAC_MIR_MAX_STEPS`.

Spot timings on a shared 4-core container, six runs of each compiled
program and nine of v2's, five of them interleaved, and one of Python
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.78 to 1.97 s |
| Rust (`rustc -O`) | 2.03 to 2.21 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.02 to 2.12 s |
| Go | 2.99 to 3.09 s |
| Python | 22.2 s |
| Kāra (`karac build --mir`) | 2.46 to 2.68 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 2.61 s, against C's
1.92, Rust's 2.09 (2.07 under overflow checks) and Go's 3.05: 1.4 times
C's time and 1.25 times Rust's. Most likely all five spend most of their
time on the 64-bit division of the trial divisions, which none of them
can avoid, and so stand closer together than in most katas (not traced).
Under valgrind's cachegrind v2 runs 18.6 billion instructions, against
Rust's 16.5 billion and C's 7.8 billion. Built for `x86-64-v3`, the
target `karac build` uses, C takes 1.86 to 1.90 s and Rust with overflow
checks 2.10 to 2.19 s, against v2's 2.47 to 2.63 s in the same five
interleaved runs. Python takes 22 s, about 12 times C's time. The
comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new in v2: every arm, the differential and the bench program run
on every v2 lane as written, and in the first spelling tried.
