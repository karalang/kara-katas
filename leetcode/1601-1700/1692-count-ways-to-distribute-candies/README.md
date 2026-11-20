# 1692. Count Ways to Distribute Candies

There are `n` **unique** candies (labeled `1` through `n`) and `k` bags.
You are asked to distribute **all** the candies into the bags such that
every bag has **at least** one candy.

There can be multiple ways to distribute the candies. Two ways are
considered **different** if the candies in one bag in the first way are
not all in the same bag in the second way. The order of the bags and the
order of the candies within each bag do not matter.

For example, `(1), (2,3)` and `(2), (1,3)` are considered different
because candies `2` and `3` in the bag `(2,3)` in the first way are not
in the same bag in the second way (they are split between the bags `(2)`
and `(1,3)`). However, `(1), (2,3)` and `(3,2), (1)` are considered the
same because the candies in each bag are all in the same bags in both
ways.

Given two integers, `n` and `k`, return *the **number** of different
ways to distribute the candies*. As the answer may be too large, return
it **modulo** `10^9 + 7`.

```
n = 3, k = 2     ->  3
n = 4, k = 2     ->  7
n = 20, k = 5    ->  206085257
```

**Constraints:** `1 <= k <= n <= 1000`.

## Approaches

The answer is the Stirling number of the second kind, S(n, k).

| file | mechanism |
|---|---|
| `candies.kara` ★ | candy i either has a bag to itself (the ways for i - 1 in j - 1 bags) or joins one of the j bags of a way for i - 1 in j: one vector over j holds row i - 1 and is overwritten from the right with row i. O(nk) time, O(k) space |
| `candies_table.kara` | the same recurrence, every row kept in an (n + 1) by (k + 1) table. O(nk) time and space |
| `candies_inclusion.kara` | inclusion and exclusion over the empty bags: the sum over i of (-1)^i C(k, i) (k - i)^n counts labelled bags, and dividing by k!, by Fermat's inverse through a closure, unlabels them. O(k log n) |
| `candies_memo.kara` | the recurrence from the top, ways(n, k) down, with a `Map` from (i, j) keeping each answer. O(nk) |
| `differential.kara` | the four arms against the statement read literally, five properties |

LeetCode offers no Rust template for this problem, so there is no
Rust-template arm.

Every arm prints the same 9 lines: LeetCode's three examples, one candy
in one bag, 1000 candies in 1000 bags and in one; then the answers
summed and a checksum for 3000 random problems of n up to 10, 300 up to
100 and 10 up to 1000, each with a random k up to n. `candies.py` mirrors
the ★ arm and its output is byte-identical.

```
3
7
206085257
1
1
1
3000 problems of n up to 10: answers sum to 3808569, checksum 395877108
300 problems of n up to 100: answers sum to 105870649432, checksum 628326942
10 problems of n up to 1000: answers sum to 4412493672, checksum 666435377
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: each candy in turn goes into one of the bags used so far or,
while fewer than k are used, into a new one, so that each way is met
once, its bags named in the order they are first used; the ways that
fill all k bags are counted. It checks 3000 random problems of n from 1
to 8 and k from 1 to n. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | n candies in n bags, and in one bag, go one way each |
| P3 | the answer is k times the arm's answer for n - 1 candies in k bags, plus its answer for n - 1 in k - 1 |
| P4 | the arm's answers for 1 to n bags sum to the Bell number of n, from Bell's triangle |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 478012351, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, every map of the candies onto k labelled bags
by `itertools.product` divided by k!, gives the same checksum. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. The memo arm returns 1 for one bag and
for as many bags as candies before it recurses, so its two mutants pass
P2; M10, which files each answer under the wrong key, is wrong only where
a later call reads it back.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the row overwritten from the left | P1 1336, P2 2222, P3 1336, P4 2222, P5 1336 |
| M2 | ★: the column for no bags never cleared | P1 1978, P2 2606, P3 600, P4 2606, P5 1978 |
| M3 | ★: a candy joins one of j - 1 bags | P1 1978, P2 2606, P3 1576, P4 2606, P5 1978 |
| M4 | table: a candy joins one of i bags | P1 1978, P2 2606, P3 1978, P4 2606, P5 1978 |
| M5 | table: the answer read for k - 1 bags | P1 2814, P2 3000, P3 2006, P4 3000, P5 2814 |
| M6 | inclusion: the signs swapped | P1 3000, P2 3000, P3 1378, P4 3000, P5 3000 |
| M7 | inclusion: each power one short | P1 2400, P2 3000, P3 198, P4 3000, P5 2400 |
| M8 | inclusion: the term for no empty bags left out | P1 3000, P2 3000, P3 2006, P4 3000, P5 3000 |
| M9 | memo: a candy joins one of i bags | P1 1378, P3 1378, P4 2222, P5 1378 |
| M10 | memo: each answer kept under j - 1 | P1 547, P3 547, P4 1494, P5 547 |

## Benchmarks

The bench draws 200 problems of 1000 candies, LeetCode's most, each with
a random number of bags up to 1000, all of them first, then answers each
8 times by the ★ arm in all five languages. Every implementation prints
`200 problems of 1000 candies, 8 rounds: answers sum to 760948561544,
checksum 845589506`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.445 s |
| Go | 0.591 s |
| Rust (`rustc -O`) | 0.789 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.790 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.374 s |
| Kāra (`karac build`) | 1.376 s |
| Python | 36 s |

The sequential Kāra build takes 1.74x Rust's time and 1.74x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.445 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (1.430 s and 1.438 s on one
run).

## Verification

All four arms print the same output as `candies.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

All four arms, the differential and the bench checked clean as first
written. The inclusion arm's `inverse` is a closure over `modulus`,
called like a function. `arm_name` in the differential indexes a list of
string literals for a `Str`, as #1662's does (B-2026-11-19-131).
