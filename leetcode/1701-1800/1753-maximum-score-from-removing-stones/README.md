# 1753. Maximum Score From Removing Stones

You are playing a solitaire game with **three piles** of stones of sizes
`a`, `b`, and `c` respectively. Each turn you choose two **different
non-empty** piles, take one stone from each, and add `1` point to your
score. The game stops when there are **fewer than two non-empty** piles
(meaning there are no more available moves).

Given three integers `a`, `b`, and `c`, return *the* ***maximum***
***score*** *you can get.*

```
a = 2, b = 4, c = 6    ->  6
a = 4, b = 4, c = 6    ->  7
a = 1, b = 8, c = 8    ->  8
```

**Constraints:** `1 <= a, b, c <= 10^5`.

## Approaches

| file | mechanism |
|---|---|
| `stones.kara` ★ | a closed form: when the largest pile holds at least the other two together, every turn can pair it with one of them and the game ends when they run out; otherwise the turns can be spread so that at most one stone is left. The answer is the smaller of the two smaller piles' sum and half the stones. O(1) |
| `stones_greedy.kara` | the greedy game played out on a sorted `[a, b, c]` array: a stone from each of the two largest piles every turn, sorted again after it, until two piles are empty. O(a + b + c) |
| `stones_heap.kara` | the non-empty piles in a `PriorityQueue.max_first()`: each turn pops the two largest, takes a stone from each and pushes back the ones that still hold stones, until fewer than two are left. O(a + b + c) |
| `stones_solution.kara` | a Rust solution as LeetCode's Rust users write it, the piles sorted in a `vec!`, then the two smaller piles' sum or half the stones, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's three examples, then all
ones, one pile larger than the other two together, and the largest
piles; then the sum of the answers and a checksum for 3000 random sets
of piles of up to 6, 3000 of up to 1000 and 300 of up to 100000,
LeetCode's limit. `stones.py` mirrors the ★ arm and its output is
byte-identical.

```
6
7
8
1
3
150000
3000 sets of piles of up to 6: scores add to 14459, checksum 518973433
3000 sets of piles of up to 1000: scores add to 2062892, checksum 727152521
300 sets of piles of up to 100000: scores add to 20545141, checksum 476120106
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: from the three piles, every move that takes a stone from two
different non-empty piles is tried, recursively, and the most points
any sequence of moves scores, each position worked out once in a `Map`.
It checks 3000 random sets of three piles of 1 to 9 stones, each with a
random pile to add a stone to. Every case is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the piles in another order give the same answer |
| P3 | one more stone in a pile raises the answer by 0 or 1 |
| P4 | the answer is at least the smallest pile and at most half the stones |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 549766397, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading, the same search memoized with `lru_cache`, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. A first M9, the solution's test
loosened to `v[0] + v[1] < v[2] - 1`, is equivalent: at a sum of `v[2]`
or `v[2] - 1` both branches give the same score. It was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: half the stones never the limit | P1 1516, P4 1516, P5 1516 |
| M2 | ★: half the stones rounded up | P1 850, P4 850, P5 850 |
| M3 | ★: the largest pile taken from a and b only | P1 230, P2 455, P5 230 |
| M4 | greedy: each turn takes from the smallest and the largest pile | P1 2988, P4 2988, P5 2988 |
| M5 | greedy: the piles not sorted again after a turn | P1 2903, P5 2903 |
| M6 | greedy: the game stops once the smallest pile is empty | P1 2150, P5 2150 |
| M7 | heap: the queue pops the smallest first | P1 2903, P5 2903 |
| M8 | heap: the second pile never pushed back | P1 2882, P4 1431, P5 2882 |
| M9 | solution: the test on the largest pile reversed | P1 2189, P4 1516, P5 2189 |
| M10 | solution: half of one stone fewer | P1 666, P5 666 |

## Benchmarks

The bench draws 2000000 random sets of three piles of up to 100000,
LeetCode's limit, all of them first, then answers each 5 times by the ★
arm in all five languages. Every implementation prints `2000000 sets of
piles, 5 rounds: scores add to 687543441500, checksum 909523834`. The C
build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `21cdf88b69` on LLVM 22:

| | median |
|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.103 s |
| Kāra (`karac build`) | 0.104 s |
| Rust (`rustc -O`) | 0.104 s |
| C (`clang -O3`) | 0.105 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.106 s |
| Go | 0.150 s |
| Python | 6.6 s |

The sequential Kāra build is level with Rust and level with Rust with overflow checks on, the equal-safety comparison (BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.096 s and
0.096 s on one run).

## Verification

All four arms print the same output as `stones.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★, greedy and heap arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 3 edits: `struct
Solution {}` added, `vec![a, b, c]` written `[a, b, c]`, and
`Solution::maximum_score` written `Solution.maximum_score`. The
in-place `sort` and the `if` on the sorted piles carried over as
written.

The differential and the bench checked clean as generated.
