# 2106. Maximum Fruits Harvested After at Most K Steps

Fruits are available at some positions on an infinite x-axis. You are
given a 2D integer array `fruits` where `fruits[i] = [positioni,
amounti]` depicts `amounti` fruits at the position `positioni`.
`fruits` is already sorted by `positioni` in ascending order, and each
`positioni` is unique.

You are also given an integer `startPos` and an integer `k`. Initially,
you are at the position `startPos`. From any position, you can either
walk to the left or right. It takes one step to move one unit on the
x-axis, and you can walk at most `k` steps in total. For every position
you reach, you harvest all the fruits at that position, and the fruits
will disappear from that position.

Return the maximum total number of fruits you can harvest.

```
fruits = [[2,8],[6,3],[8,6]], startPos = 5, k = 4                          ->  9
fruits = [[0,9],[4,1],[5,7],[6,2],[7,4],[10,9]], startPos = 5, k = 4      ->  14
fruits = [[0,3],[6,4],[8,5]], startPos = 3, k = 2                          ->  0
```

**Constraints:** `1 <= fruits.length <= 10^5`; `fruits[i].length == 2`;
`0 <= startPos, positioni <= 2 * 10^5`; `positioni-1 < positioni`;
`1 <= amounti <= 10^4`; `0 <= k <= 2 * 10^5`.

A walk harvests an interval around the start, and the cheapest walk
covering `lo..=hi` crosses it once and walks its shorter side twice:
`(hi - lo) + min(start - lo, hi - start)`. So the answer is the richest
run of consecutive fruits whose interval, stretched to include the
start, costs at most `k`, and a run's cost only grows as it widens, which
is what a sliding window needs. At the constraints' largest the total
is 10^9, within `i32`.

## Approaches

| file | mechanism |
|---|---|
| `harvest.kara` ★ | a sliding window over the sorted fruits, grown on the right and shrunk on the left while `steps(l, r, start)` exceeds `k`; `steps` takes the three cases, all left of the start, all right of it, or around it with the shorter side doubled. O(n) |
| `harvest_prefix.kara` | every route in turn: a prefix sum over every position up to the farthest reachable one, and for each `x` from 0 to `k`, `x` steps one way and then back past the start with what is left, both ways round, each interval read with a captured closure `between(l, r)`. O(P + k) |
| `harvest_search.kara` | a prefix sum over the fruits and `partition_point` on the positions: for each fruit left of the start as the left end, the farthest right end the steps allow, `max(k - 2L, (k - L) / 2)` past the start, plus the walk right only. O(n log n) |
| `harvest_struct.kara` | a `struct Walk` (start, steps) with `cost` and `fits` methods, the cost written as the distance covered plus the shorter side, and a `struct Window` (first fruit, total) grown with `take` and shrunk with `drop_first` (`mut ref self`), over `enumerate()` |
| `harvest_deque.kara` | a `VecDeque[(i64, i64)]` of the fruits in the window, pushed at the back and popped from the front, the cost from the span with the start and the shorter side, in a `loop` with destructuring `let (l, _) = window.front().unwrap()` |
| `harvest_solution.kara` | LeetCode's Rust template (`Vec<Vec<i32>>`, `start_pos: i32`, a cost closure with a `-> i32` return type and `std::cmp::min`, a `usize` left index), carried by `karac fix` in four rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and four
more (no steps on a fruit; a start right of every fruit; a long way to
the richer side; a turn that costs less going right first), each with
its answer; then the total for 3000 random fields of 1 to 40 fruits on
positions 0 to 60, from a random start with 0 to 40 steps, and a
checksum of the answers; then the constraints' largest, 10^5 fruits of
10^4 on every even position from 0, from the middle with 2 * 10^5 steps
and with 1000. `harvest.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every interval whose ends are the start or a fruit, around
the start, is tried, and one whose cheapest walk, end to end once and
the shorter side twice, fits in `k` steps gives the fruits in it. It
checks 300 random fields of 1 to 10 fruits on positions 0 to 20, from a
start in 0 to 20 with 0 to 15 steps; then 20 of 1 to 30 fruits of up to
10^4 on positions up to 2 * 10^5 with up to 2 * 10^5 steps; then 20 with
every fruit on one side of the start, up to 50 positions off. All 340
are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is at most every fruit together, and at least the richest single fruit within `k` steps |
| P3 | the field mirrored, `p` to `200000 - p` and the start with it: the same answer |
| P4 | one more step: an answer no smaller |
| P5 | every position and the start moved 5 right: the same answer |
| P6 | each arm agrees with at least three of the other five |

The moved field may reach 200005, five past the constraints, which no
arm depends on. The differential prints `340 fields: checksum 586169981,
12240 checks over 6 arms: 0 failures` under every lane in Verification;
the checksum of the literal answers was checked against a Python reading
of the same fields that tries the same intervals. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept, three
to each Kāra arm and two to the Rust-template arm. Each kept one is
killed, fails the same way under both backends and not by a crash, and
no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the longer route taken | P1 48, P6 48 |
| M2 | ★: a route of exactly `k` steps refused | P1 96, P2 33, P6 96 |
| M3 | ★: a fruit dropped from the window kept in the sum | P1 304, P6 304 |
| M5 | prefix: no way back after turning | P1 60, P6 60 |
| M7 | prefix: each fruit counted one place left | P1 117, P2 19, P3 145, P5 15, P6 117 |
| M8 | prefix: an interval's right end left out | P1 79, P2 20, P3 97, P6 79 |
| M9 | search: only the turn at the left end | P1 25, P3 48, P6 25 |
| M10 | search: a left end exactly `k` away skipped | P1 36, P2 13, P3 72, P6 36 |
| M11 | search: the right end at the reach left out | P1 38, P3 49, P6 38 |
| M13 | struct: the longer side walked twice | P1 221, P2 82, P6 221 |
| M14 | struct: a left end right of the start counted as steps back | P1 128, P3 213, P6 128 |
| M16 | struct: a taken fruit replacing the total | P1 227, P2 37, P3 61, P4 7, P6 227 |
| M17 | deque: the start ignored in the span | P1 194, P6 194 |
| M18 | deque: the shorter side walked three times | P1 38, P6 38 |
| M20 | deque: each fruit pushed at the front | P1 126, P6 126 |
| M22 | solution: the adapter halving the steps | P1 231, P2 84, P6 231 |
| M23 | solution: the last window taken | P1 162, P2 131, P3 225, P6 162 |

P1 and P6 kill all seventeen, P3 eight, P2 eight, P4 one and P5 one. P3
sees the edits that treat left and right differently: one turn order
only (M9), a right end left out (M8, M11), a left end skipped (M10), a
cost that goes wrong for a left end right of the start (M14), and the
fruits counted one place left (M7). P2 sees the edits that can miss the
richest fruit within reach, as the longer route (M13), an exact-`k`
route refused (M2, M10) and half the steps (M22) do, or that count
fruits twice (M7, M8, M16, M23). P4 sees only the struct arm's total
replaced by each fruit taken (M16), which one more step can lower. P5
sees only the prefix arm's fruits shifted a place left (M7), whose
off-by-one meets position 0 differently once the field moves.

Of the thirty, thirteen were not kept, and three of them survive, each
equivalent to the arm it edits. The ★ arm's and the Rust arm's cost of
a window left of the start measured to its right end (M4, M21): the
window's left fruit entered it as a right end, when its own cost, from
the start to it, was checked, so the window's true cost was already
within `k`. The search arm's walk right only starting past a fruit at
the start (M12): a fruit at the start is already counted as a left end
with no steps back. Of the other ten, all killed, four fail as a kept
one: the deque arm's dropped fruit kept in the sum as M3; the deque
arm's no side walked twice as M5; and the prefix arm's right-first
routes dropped and the Rust arm's right-first route walking both sides
twice as M9. Six are killed with checks of their own but were left out
because their arm keeps its share: the ★ arm's first fruit never taken,
the prefix arm's left-first route one place short, the search arm's
positions summed as amounts, the struct arm's two fruits dropped at a
time and its lone fruit too far kept, and the Rust arm's lone fruit too
far kept (the last two fail alike, P1 95, P6 95).

## Verification

Every arm prints the same output as `harvest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.2 s to 3.8 s. The differential
takes 67 s there, most of it the prefix arm walking up to 2 * 10^5 steps
for each wide field, five times per arm; compiled it takes 0.9 s.

`karac fix` carries the template in four rounds of 16, 3, 1 and 1 edits:
Rust's spellings (`Vec<..>` to brackets, the closure's `-> i32`
dropped, `std::cmp::min` to `min`, `&&` to `and`, `struct Solution;` to
`struct Solution {}`, the adapter's `&Vec` to `ref`, `&x` pattern
dropped and `Solution::` to `.`); then `ans` given `: i32`, the `0usize`
suffix dropped and the adapter's `as i64` dropped as widening; then
`sum` given `: i32`, which the first round's `ans: i32` brought to light
at `ans.max(sum)`; then the adapter's `ref` parameter to a bare one.
Rust infers `sum` and `ans` as `i32` from `sum += fruits[right][1]`;
Kāra does not let an operator fix a literal's type (design.md §8), so
the template needs the two annotations, which `karac fix` writes.

## Benchmarks

The bench builds 20 fields of about 10^5 fruits once, each position up
to 2 * 10^5 holding a fruit with even odds, amounts up to 10^4; then 10
walks per field from random starts with up to 2 * 10^5 steps, with the
★ arm in all five languages: the sliding window. Every implementation
prints `200 walks: 50238720125 fruits, checksum 648287792`.

BENCHTAB
