# 879. Profitable Schemes

There is a group of `n` members, and a list of various crimes they could
commit. The `i`-th crime generates a `profit[i]` and requires
`group[i]` members to participate in it. If a member participates in one
crime, that member can't participate in another crime. Let's call a
profitable scheme any subset of these crimes that generates at least
`minProfit` profit, and the total number of members participating in
that subset of crimes is at most `n`. Return the number of schemes that
can be chosen. Since the answer may be very large, return it modulo
`10^9 + 7`.

```
n = 5, minProfit = 3, group = [2,2], profit = [2,3]  ->  2
n = 10, minProfit = 5, group = [2,3,5], profit = [6,7,8]  ->  7
```

**Constraints:** `1 <= n <= 100`, `0 <= minProfit <= 100`,
`1 <= group.length <= 100`, `1 <= group[i] <= 100`,
`profit.length == group.length`, `0 <= profit[i] <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `profitable_schemes.kara` ★ | a knapsack over members and profit: `ways[m][p]` counts the sets of crimes chosen so far that use exactly m members and make p profit, profit counted no higher than `min_profit`, since any more is just as good. Each crime joins every set it fits, walking the members from the top down so that it joins each set once; the answer sums `ways[m][min_profit]` over every m up to n. O(crimes * n * min_profit) time, O(n * min_profit) space |
| `profitable_schemes_table.kara` | the full table over crimes: `count[c][m][p]` counts the sets among the first c crimes using at most m members with profit at least p, crime c either left out or taken when it fits, needing only `max(p - profit, 0)` more from the rest; every layer is kept. O(crimes * n * min_profit) time and space |
| `profitable_schemes_memo.kara` | memoized recursion: `schemes(c, members, needed)` counts the sets of crimes c.. that fit in `members` and make `needed` more profit, crime c left out plus crime c taken when it fits, with a `Map` keyed by the three. The key's stride is one past the larger of n and `min_profit`, which neither argument ever exceeds |
| `profitable_schemes_complement.kara` | every set that fits, less the unprofitable ones: the sets that fit in n members counted by members alone, less those that fit but make less than `min_profit`, counted by members and their exact profit below it |
| `profitable_schemes_push.kara` | states pushed forward: for each crime a new flat table starts as a copy of the old one, the crime left out, and every reachable state of the old one pushes its count to the state with the crime added when the members fit |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples and eight
more (a crime needing more members than there are, with and without
profit needed; three crimes that make nothing and need nothing, so all
8 subsets count; profit needed that no subset reaches; and four cases of
100 crimes, LeetCode's most: 100 crimes of one member and one profit
needing 100 profit, which only all 100 make, and needing none, which
every one of the 2^100 subsets meets, 976,371,285 modulo 10^9 + 7; 100
crimes of one member and 100 profit, where every subset but the empty
one counts; and 100 crimes each needing all 100 members, where each
counts alone); the counts of 3,000 cases of 1 to 10 crimes, 52,346 in
all; and 8 cases of 100 crimes with n and `minProfit` from 50 to 100,
with a checksum. `profitable_schemes.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every subset of the crimes, as the bits of a number from 0 to
2^k - 1, with its members and its profit added up, counted when it uses
at most n members and makes at least `min_profit`. It checks 1,604
cases: 1,500 of 1 to 12 crimes, against the statement; 100 of 13 to 24
crimes with n up to 40, too many subsets to count one by one at speed,
against the other properties; and 4 of 100 crimes with n and
`min_profit` from 50 to 100, where only the arms can count. The ★ arm's
counts sum to 63,033,107.

| | property |
|---|---|
| P1 | the statement's count, on up to 12 crimes |
| P2 | with no profit needed and n the members of every crime together, all 2^k subsets count |
| P3 | the crimes in another order give the same count |
| P4 | one more member never loses a scheme, and one more unit of profit needed never adds one |
| P5 | a crime needing more than n members changes nothing |
| P6 | on 100 crimes, each arm agrees with at least two of the other four |

P2 to P5 are checked on the first two sets of cases, P6 on the third.
P2 with n the members of every crime together takes the memo arm past
LeetCode's n of 100; the arm's first key, with a fixed stride of 101,
would have let two states share a key there, and the stride now follows
n and `min_profit`. It prints `1604 cases, counts sum to 63033107, 39520
checks over 5 arms: 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the members walked upwards, so a crime can join a set twice | P1 1144, P2 1474, P4 11, P6 4 |
| M2 | ★: only the schemes using all n members counted | P1 905, P2 1600, P4 261, P6 4 |
| M3 | ★: a set that has made `min_profit` not extended | P1 759, P2 1600, P3 637, P4 338, P6 4 |
| M4 | table: a crime's profit ignored | P1 902, P6 4 |
| M5 | table: the empty set counted as making `min_profit` | P1 1312, P6 4 |
| M6 | table: a crime left out when it needs all the members left | P1 809, P2 1600, P6 4 |
| M7 | memo: every set counted when the crimes run out | P1 1413, P6 4 |
| M8 | memo: the crime left out of the key | P1 634, P2 1214, P3 678, P4 160, P5 625, P6 4 |
| M9 | memo: the profit still needed not stopped at 0 | P1 927, P2 1585, P3 267, P4 448, P5 124, P6 4 |
| M10 | complement: an unprofitable set never extended by a crime's profit exactly | P1 1274, P6 4 |
| M11 | complement: the unprofitable sets added | P1 1413, P4 862, P6 4 |
| M12 | complement: the sets using all n members left out | P1 809, P2 1600, P6 4 |
| M13 | push: every crime committed | P1 949, P2 1600, P5 140, P6 4 |
| M14 | push: a crime never filling the last member | P1 809, P2 1600, P6 4 |
| M15 | push: a state reached one way only skipped | P1 987, P2 1600, P6 4 |

P1 kills all fifteen. M6, M12 and M14 are one fault in three arms, the
sets that use every member lost, and fail the same cases. M7 and M11
fail P1 on the same 1,413 cases, those needing any profit, where the
empty set is unprofitable: M7 counts every set that fits and M11 adds
the unprofitable ones where it should take them away. Each mutant fails
P6 on all 4 of the large cases, where the other four arms still agree.
M4, M5, M7 and M10 pass P2 to P5: P2 needs no profit, which those four
leave right, and P3 to P5 compare an arm only with itself, so a fault
that is the same in every order and size passes them. None of the
fifteen tried was equivalent, and none was replaced.

## Verification

Every arm prints the same output as `profitable_schemes.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `89d76e3ff2` and the runtime
archives at `e903d5b111`, with no runtime change between them. Under
`karac __mir-run` the arms take 2 to 10 s each (the memo arm, with a
`Map` lookup for every state, the slowest) and the differential 32 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends (its interpreter and JIT, and `karac build
--legacy` with and without auto-par) print the same output for all five
arms. They refuse the differential at a `*` on a `for` element, saying
the value is not a reference, where v2 yields a reference, as on kata
877. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 600 cases of
100 crimes, LeetCode's most, with n and `minProfit` from 50 to 100; every
other case has groups up to 100 and profits up to 100, and the rest
groups up to 10 and profits up to 10, so that more of the crimes fit.
Each case is drawn from the same generator in each language as it is
solved, and builds its own table of `(n + 1) x (minProfit + 1)` counts,
a `Vec` of `Vec`s in Kāra and Rust, a slice of slices in Go, a list of
lists in Python and an array of `calloc`'d rows in C. Every
implementation prints `600 cases of 100 crimes: counts sum to
158057772462, checksum 963817435`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.44 to 0.49 s | 0.46 s |
| Rust (`rustc -O`) | 0.53 to 0.59 s | 0.55 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.53 to 0.60 s | 0.58 s |
| Go | 0.73 to 0.84 s | 0.75 s |
| Python | 21.7 s | |
| Kāra (`karac build --mir`) | 0.59 to 0.73 s | 0.60 s |
| Kāra legacy (`karac build --legacy`) | 0.58 to 0.63 s | 0.60 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 878's does.

v2 takes 1.05 times Rust's median time under overflow checks, 1.30
times C's and 1.00 times legacy's. Under valgrind's cachegrind C runs
3.94 billion instructions and 0.12 billion branches, Rust with overflow
checks 6.71 billion and 1.16 billion, legacy 7.83 billion and 1.83
billion, and v2 8.05 billion and 1.83 billion: the checked languages
test each cell's indices and sums, and C's loop has no such tests. The
time grows far less than the instructions, so the inner loop's
`% modulus`, which each cell waits on, most likely sets much of it
(inferred, not traced). It is not the instruction set: built for
x86-64-v3, as `karac build` targets, C and Rust with overflow checks
take 0.46 and 0.57 s in five spot runs. The comparison with C and Rust
waits until after M4.
