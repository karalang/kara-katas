# 1744. Can You Eat Your Favorite Candy on Your Favorite Day?

You are given a **(0-indexed)** array of positive integers
`candiesCount` where `candiesCount[i]` represents the number of candies
of the `ith` type you have. You are also given a 2D array `queries`
where `queries[i] = [favoriteTypei, favoriteDayi, dailyCapi]`.

You play a game with the following rules:

- You start eating candies on day **`0`**.
- You **cannot** eat **any** candy of type `i` unless you have eaten
  **all** candies of type `i - 1`.
- You must eat **at least** **one** candy per day until you have eaten
  all the candies.

Construct a boolean array `answer` such that `answer.length ==
queries.length` and `answer[i]` is `true` if you can eat a candy of type
`favoriteTypei` on day `favoriteDayi` without eating **more than**
`dailyCapi` candies on **any** day, and `false` otherwise. Note that you
can eat different types of candy on the same day, provided that you
follow rule 2.

Return *the constructed array* `answer`.

```
candiesCount = [7,4,5,3,8], queries = [[0,2,2],[4,2,4],[2,13,1000000000]]
  ->  [true,false,true]
candiesCount = [5,2,6,4,1], queries = [[3,1,2],[4,10,3],[3,10,100],[4,100,30],[1,3,1]]
  ->  [false,true,true,false,false]
```

**Constraints:** `1 <= candiesCount.length <= 10^5`; `1 <=
candiesCount[i] <= 10^5`; `1 <= queries.length <= 10^5`;
`queries[i].length == 3`; `0 <= favoriteTypei < candiesCount.length`;
`0 <= favoriteDayi <= 10^9`; `1 <= dailyCapi <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `eat.kara` ★ | type t is the candies after the running total `before[t]` and up to `before[t + 1]`. By the end of day d at least d + 1 candies are eaten and at most (d + 1) * cap, so type t can be eaten that day exactly when d + 1 <= `before[t + 1]` and (d + 1) * cap > `before[t]`. O(n + q) |
| `eat_scan.kara` | the running totals from `scan`; the candy eaten last on day d is numbered from d + 1 to (d + 1) * cap, type t's are numbered from `before[t] + 1` to `before[t + 1]`, and the answer is whether those two ranges meet. O(n + q) |
| `eat_search.kara` | `partition_point` over the running totals finds the type of the (d + 1)-th candy and of the ((d + 1) * cap)-th, the slowest and fastest pace's last candy of the day; type t can be eaten exactly when it lies between them. O(n + q log n) |
| `eat_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `vec![0i64; n + 1]` of prefix sums and each query's `d < pre[t + 1] && (d + 1) * c > pre[t]` mapped and collected, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 7 lines: LeetCode's two examples, then one
candy eaten on day 0 and not on day 1, and three types of `10^5` candies
asked about a cap too small to reach the last type, the first candy a
cap can just reach, and days at either end of the first type; then how
many answers are yes and a checksum of all of them for 3000 random
problems of up to 6 types of up to 5 candies with 6 queries each, 100 of
up to 1000 types of up to `10^5` with 1000 queries, and 2 of up to
`10^5` types of up to `10^5`, LeetCode's limits, with `10^5` queries.
Days reach a little past the last candy, and one cap in ten is `10^9`.
`eat.py` mirrors the ★ arm and its output is byte-identical.

```
[true, false, true]
[false, true, true, false, false]
[true, false]
[false, false, true, true, false]
3000 problems of up to 6 types of up to 5 candies, 6 queries each: 8904 yes, checksum 2713288
100 problems of up to 1000 types of up to 100000 candies, 1000 queries each: 40672 yes, checksum 945250564
2 problems of up to 100000 types of up to 100000 candies, 100000 queries each: 129447 yes, checksum 955044815
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: day by day, every count of candies that can have been eaten
so far, one to `cap` a day and never more than there are; then, on the
favourite day, every count eaten that day, and whether any candy so
eaten is of the favourite type, found by walking the types in order. It
checks 3000 random problems of 1 to 6 types of 1 to 5 candies, each
with 6 queries of days up to two past the last candy and caps of 1 to
8. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | a cap one larger never turns a yes into a no |
| P3 | one more type at the end leaves every answer as it was |
| P4 | on day 0 a cap of every candy reaches every type |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 476310561, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading, each candy number from d + 1 to (d + 1) * cap tested against
type t's numbers in turn, gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the slowest pace must stop short of type t's last candy | P1 1264, P4 610, P5 1264 |
| M2 | ★: the fastest pace counted over d days, not d + 1 | P1 1234, P4 3000, P5 1234 |
| M3 | ★: the fastest pace allowed to stop at type t's start | P1 200, P5 200 |
| M4 | scan: type t's candies numbered from one before its first | P1 200, P5 200 |
| M5 | scan: either range's start before the other's end, not both | P1 2970, P5 2970 |
| M6 | search: the type of a candy at a total taken as the next one | P1 1408, P4 610, P5 1408 |
| M7 | search: the fastest pace's type itself left out | P1 977, P4 3000, P5 977 |
| M8 | search: the slowest pace's last candy the d-th, not the (d + 1)-th | P1 1261, P5 1261 |
| M9 | solution: `d < pre[t + 1]` made `<=` | P1 1261, P5 1261 |
| M10 | solution: the prefix sums each type's count alone | P1 2040, P5 2040 |

## Benchmarks

The bench draws 10 random problems of `10^5` types of 1 to 20 candies
and `10^5` queries, LeetCode's largest, with days anywhere among the
candies and caps of 1 to 30, all of them first, then answers each 30
times by the ★ arm in all five languages; each answer builds its prefix
sums anew. Every implementation prints `10 problems of 100000 types and
100000 queries, 30 rounds: 13004970 yes, checksum 156668838`. The C
build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `21cdf88b69` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.382 s |
| Rust (`rustc -O`) | 0.545 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.619 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.626 s |
| Kāra (`karac build`) | 0.638 s |
| Go | 0.914 s |
| Python | 12 s |

The sequential Kāra build takes 1.14x Rust's time and 0.99x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md).
The gap to plain Rust is the overflow checks: with them on, Rust takes
Kāra's time. C is the fastest here at 0.382 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.618 s and
0.682 s on one run).

## Verification

All four arms print the same output as `eat.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★ arm checked clean as first written. The search arm took one
`karac fix`: an `as i64` on the `i32` cap, which widens by itself, was
dropped.

The scan arm's closure was written `|sum, c| { sum += c; Some(sum) }`:
it writes Kāra's by-value state in place, as Kāra allows, but returns
only the item where Kāra's `scan` wants `Some((next_state, item))`.
`karac check` refused it with two bare type errors, `expected
'Option[(i64, _)]', found 'Option[i64]'`, and no fix; the existing
fix-it for Rust's shape knew only a state written through `*sum`. Since
kara `039abec2c1` (B-2026-11-20-91) the closure gets one error naming Kāra's shape,
and the arm took one `karac fix` of 2 edits: the tail became `Some((sum,
sum))`, and an `as i64` on the cap was dropped.

LeetCode's Rust template took one `karac fix` of 12 edits: `struct
Solution {}` added, `Vec<..>` written `Vec[..]`, `vec![0i64; n + 1]`
written `Vec.filled(n + 1, 0)`, the `as i64` on `candies_count[i]`
dropped, and `&&` written `and`. `q[0] as usize`, the `as i64` casts on
the day and cap, and the `.iter().map(..).collect()` chain carried over
as written.

The differential took one `karac fix`: an `as i64` on a candy count
added to an `i64` was dropped.
