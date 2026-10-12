# 440. K-th Smallest in Lexicographical Order

Given integers `n` and `k`, return the `k`-th smallest integer in the
range `[1, n]` in lexicographical order, the order of their decimal
text.

```
n = 13, k = 2  ->  10     (1, 10, 11, 12, 13, 2, 3, 4, 5, 6, 7, 8, 9)
n = 1,  k = 1  ->  1
```

**Constraints:** `1 <= k <= n <= 10^9`.

## Approaches

In lexicographical order the numbers form a tree, 1 above 10 to 19, 10
above 100 to 109 and so on, read in preorder. With `n` up to `10^9`,
only an arm that skips whole subtrees meets the constraints; the
others walk the order one number at a time, or sort it.

| file | mechanism |
|---|---|
| `find_kth_number.kara` ★ | counting down the tree: from 1, count the numbers in `[1, n]` under the current prefix, one span per length; if the k-th lies past them all, skip to the next sibling, otherwise step down to the first child. O(log^2 n) |
| `find_kth_number_walk.kara` | k - 1 steps of the lexicographical successor: the first child when it is at most n, otherwise climb while the number ends in 9 or its successor passes n, then step to the next sibling. O(k), amortized O(1) a step |
| `find_kth_number_dfs.kara` | a recursive preorder walk that counts k down at each visit and stops when it reaches zero. O(k), recursion as deep as n has digits |
| `find_kth_number_sort.kara` | the plain reference: list 1 to n, sort them by their decimal text with `sort_by_key`, take the k-th. O(n log n) time and O(n) space |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 9 lines: the two LeetCode examples, six edge
cases (a step into the second subtree, the last of 100 and of 1,000,
the middle of 10,000, a k deep in 99,999, and the first of 100,000),
and for 300 random cases, n of 1 to 4 digits and k anywhere in
`[1, n]`, the total of the answers and a checksum. The edge cases stay
at or below 100,000 so that the O(k) and O(n log n) arms finish.
`find_kth_number.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases: n of 1 to 3 digits and k anywhere in `[1, n]`. The
numbers stay below 1,000 because the sort arm sorts all of them on
every call.

| | property |
|---|---|
| P1 | the answer is in `[1, n]`, and exactly k - 1 numbers in `[1, n]` come before it by their text |
| P2 | the first is 1, and the last is reached from 9 by stepping to the largest child at most n while there is one |
| P3 | the k-th comes before the (k + 1)-th by their text |
| P4 | adding n + 1 to the range moves the k-th as inserting n + 1 into the order says: no change when n + 1 falls after it, n + 1 when it falls at it, and the (k - 1)-th when it falls before it |
| P5 | the first d answers are 1, 10, ..., 10^(d - 1), where n has d digits |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.
P1 alone pins the answer, since a rank names one number; the other
four come from different sides of the problem.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | tree: stepping down counts twice | P1 764, P2 515, P3 82, P4 10, P5 472 |
| M2 | tree: a subtree exactly as large as what is left is entered, not skipped | P1 1230, P2 1428, P4 24 |
| M3 | walk: climbing ignores a trailing 9 | P1 766, P2 871, P3 12, P4 71 |
| M4 | walk: the child equal to n is never stepped into | P1 13, P2 85, P3 2, P4 89, P5 5 |
| M5 | dfs: the child ending in 9 is never visited | P1 778, P2 874, P3 105, P4 65 |
| M6 | dfs: n itself is never visited as a child | P1 177, P2 934, P3 29, P4 84, P5 5 |
| M7 | sort: sorted by value, not text | P1 913, P2 881, P3 16, P4 225, P5 934 |
| M8 | sort: the k-th counted from the end | P1 1373, P2 1434, P3 1434, P4 1247, P5 1434 |

P5's chain 1, 10, 100 never passes a 9 or a subtree whose size matches
what is left, so it misses M2, M3 and M5. M4 only goes wrong when n
is exactly ten times a number the walk reaches, a multiple of 10, so
it fails the fewest cases; P4, which moves n by one and so off and on
a multiple of 10, finds it most often. Two first picks were replaced. Counting
a prefix's span past n (dropping the `min`) never terminates: the walk
passes n, where every count is zero and nothing moves. And sorting by
`*x` is refused, since `sort_by_key` hands its key function the
element itself, an `i64`, so the mutant sorts by `x`.

## Verification

All four arms print the same output as `find_kth_number.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends:

- The tree and walk arms match under `karac run --interp`, LLJIT,
  `karac build` and `KARAC_AUTO_PAR=1 karac build`.
- The recursive arm matches under `karac run --interp`, and crashes
  with a segmentation fault (exit 139) under LLJIT and from
  `karac build`.
- The sort arm matches under `karac run --interp`; LLJIT and
  `karac build` stop at LLVM module verification ("Instruction does
  not dominate all uses!", on the cleanup of the f-string buffer the
  key closure builds). The differential, which holds
  a copy of the sort arm, prints `0 failures` under
  `karac run --interp` and fails to build the same way.

Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm on 1,000,000 random queries: n drawn
up to `10^9` and k anywhere in `[1, n]`, the only arm that meets the
constraints. Every implementation prints `1000000 queries with n up to
10^9: total 218570167892627, checksum 940615486`, the Kāra program
under `karac __mir-run` included (in 128 s).
Spot timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.33 to 0.36 s |
| Rust (`rustc -O`) | 0.32 to 0.35 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.45 to 0.49 s |
| Go | 0.36 to 0.39 s |
| Kāra (frozen legacy `karac build`) | 0.50 to 0.52 s |
| Python | 39 to 40 s |

The Kāra program prints the same line under `karac __mir-llvm-run` in
2.2 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark. The legacy build checks integer
overflow, so its fair comparison is Rust with overflow checks on.

## Compiler findings

No new findings.
