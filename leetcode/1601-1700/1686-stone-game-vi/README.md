# 1686. Stone Game VI

Alice and Bob take turns playing a game, with Alice starting first.

There are `n` stones in a pile. On each player's turn, they can **remove**
a stone from the pile and receive points based on the stone's value.
Alice and Bob may **value the stones differently**.

You are given two integer arrays of length `n`, `aliceValues` and
`bobValues`. Each `aliceValues[i]` and `bobValues[i]` represents how
Alice and Bob, respectively, value the `i`th stone.

The winner is the person with the most points after all the stones are
chosen. If both players have the same amount of points, the game results
in a draw. Both players will play **optimally**. Both players know the
other's values.

Determine the result of the game, and:

- If Alice wins, return `1`.
- If Bob wins, return `-1`.
- If the game results in a draw, return `0`.

```
aliceValues = [1,3], bobValues = [2,1]          ->  1
aliceValues = [1,2], bobValues = [3,1]          ->  0
aliceValues = [2,4,3], bobValues = [1,6,7]      ->  -1
```

**Constraints:** `n == aliceValues.length == bobValues.length`;
`1 <= n <= 10^5`; `1 <= aliceValues[i], bobValues[i] <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `stones.kara` ★ | taking a stone gains its worth to the taker and keeps its worth from the other, so it weighs `alice + bob` to whoever moves, and both take the heaviest left: the indexes sorted by weight (`sort_by_key`), heaviest first, taken in turn; the sign of the difference by `signum()`. O(n log n) |
| `stones_count.kara` | a weight is 2 to 200, and among the stones of one weight w the order does not matter (the difference is their worth to Alice less w for each Bob takes), so each weight keeps a count and that worth in a fixed array, and from the heaviest down Bob takes the odd turns. O(n + 200) |
| `stones_heap.kara` | a max-first `PriorityQueue` of `(alice + bob, alice, bob)`, popped in turn into the two totals, compared by `cmp` and a `match` on the `Ordering`. O(n log n) |
| `stones_solution.kara` | a Rust solution as LeetCode's Rust users write it, `(sum, alice, bob)` tuples by `zip`, `sort_unstable_by` on the sum descending, and `alice.cmp(&bob) as i32`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's three examples, one stone,
and two stones alike; then Alice's wins, Bob's and the draws, and a
checksum, for 3000 random games of up to 10 stones worth up to 5, 300
of up to 1000 worth up to 100, and 10 of up to `10^5` worth up to 100.
`stones.py` mirrors the ★ arm and its output is byte-identical.

```
1
0
-1
1
0
3000 games of up to 10 stones up to 5: Alice 2304, Bob 402, draws 294, checksum 644699359
300 games of up to 1000 stones up to 100: Alice 149, Bob 151, draws 0, checksum 372844335
10 games of up to 100000 stones up to 100: Alice 5, Bob 5, draws 0, checksum 774975756
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the whole game searched, every stone the player to move could
take, over a table of the stones taken, each player making the most of
the difference between their total and the other's. The outcome is that
difference's sign, since a better difference is never a worse result.
It checks 3000 random games of 1 to 10 stones, each worth 1 to between 1
and 6 to each player. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the stones in reverse order give the same answer |
| P3 | every value doubled gives the same answer |
| P4 | two stones worth 100 to both added give the same answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 117138398, 60000 checks
over 4 arms: 0 failures` under every lane in Verification. A Python
reading of the statement that searches the win, draw or loss itself,
Alice taking the best outcome and Bob the worst for her, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. P3 and P4 fail for no mutant: every
edit is as wrong at twice the values, or with two heavy stones that the
players share, as without. Pairs of edits that come to the same game fail
the same checks: M2 and M4 let Bob move first, M3 and M8 let Alice win
whenever she scores at all, and M5 and M9 take the lightest stones first.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the stones sorted by Alice's worth alone | P1 444, P2 492, P5 444 |
| M2 | ★: Bob takes the even turns | P1 2088, P5 2088 |
| M3 | ★: Bob's stones added to the difference | P1 931, P5 931 |
| M4 | count: Bob takes the even turns | P1 2088, P5 2088 |
| M5 | count: the lightest weight first | P1 718, P5 718 |
| M6 | count: each weight keeps Bob's worth | P1 1154, P5 1154 |
| M7 | heap: the stones weighed `alice - bob` | P1 615, P5 615 |
| M8 | heap: the turn never passes to Bob | P1 931, P5 931 |
| M9 | solution: the sort ascending | P1 718, P5 718 |
| M10 | solution: Alice adds her stones' worth to Bob | P1 917, P2 563, P5 917 |

## Benchmarks

The bench draws 50 games of `10^5` stones worth 1 to 100 to each
player, LeetCode's largest, all of them first, then answers each 10
times by the ★ arm in all five languages: each sorts a new vector of
indexes by weight, by Kāra's and Rust's `sort_by_key`, C's `qsort`, Go's
`slices.SortFunc` and Python's `sorted`. The answer does not depend on
how stones of one weight are ordered, so a stable sort and an unstable
one agree. Every implementation prints `50 games of 100000 stones, 10
rounds: Alice 300, Bob 200, draws 0, checksum 658735261`. The C build
also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 1.011 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.014 s |
| Kāra (`karac build`) | 2.799 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 2.844 s |
| Go | 3.571 s |
| C (`clang -O3`) | 4.357 s |
| Python | 18 s |

The sequential Kāra build takes 2.81x Rust's time and 2.80x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (2.693 s and 2.711 s on one
run).

## Verification

All four arms print the same output as `stones.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The count and heap arms checked clean as first written. The ★ arm began
`let mut difference = 0`, which keeps the literal's `i64`, and returned
its `signum()` as the `i32` the signature names; the refusal (E0200)
named the binding, and `karac fix` declared it `difference: i32`.

LeetCode's Rust solution ends `alice.cmp(&bob) as i32`, Rust's -1, 0 or 1
from `Ordering`'s `#[repr(i8)]`. Kāra's `Ordering` holds no numbers and
casts to none, and the refusal was a bare `cannot cast 'Ordering' to
'i32'` with nothing to write instead. Since kara `93fd9b2078` (B-2026-11-20-38) it
says why and gives the `match` that names the three numbers, and `karac
fix` writes it. The rest took the same `karac fix`: `struct Solution {}`
added, each `Vec<..>` written `Vec[..]`, the `&a`, `&b` and `&(_, a, b)`
patterns and the `&` arguments dropped, `let (mut alice, mut bob)`
written `let mut (alice, bob)`, `sort_unstable_by` written `sort_by`, and
the harness's `alice.clone()` and `bob.clone()` passed as they are
(`redundant_clone`).

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
