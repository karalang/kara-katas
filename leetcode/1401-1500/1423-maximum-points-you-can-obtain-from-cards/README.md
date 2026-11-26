# 1423. Maximum Points You Can Obtain from Cards

There are several cards arranged in a row, and each card has an
associated number of points. The points are given in the integer array
`cardPoints`. In one step, you can take one card from the beginning or
from the end of the row. You have to take exactly `k` cards. Your score
is the sum of the points of the cards you have taken. Given the integer
array `cardPoints` and the integer `k`, return the maximum score you can
obtain.

```
cardPoints = [1,2,3,4,5,6,1], k = 3      ->  12    the last three cards, 1 + 6 + 5
cardPoints = [2,2,2], k = 2              ->  4     any two cards
cardPoints = [9,7,7,9,7,7,9], k = 7      ->  55    every card
```

**Constraints:** `1 <= cardPoints.length <= 10^5`, `1 <= cardPoints[i]
<= 10^4`, `1 <= k <= cardPoints.length`.

Each arm is `fn max_score(card_points: Vec[i32], k: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `max_score.kara` ★ | the first k cards taken, then one at a time the last of those given back for the next card from the far end, the best total kept. O(k) |
| `max_score_prefix.kara` | the sums of every prefix in a table, and for each count i taken from the front the k - i from the back read off the same table, the most by `map` and `max`. O(n) time and space |
| `max_score_scan.kara` | the trades of a front card for a back card, as pairs from the innermost out by `zip` over two reversed slices, run through `scan` to the total after each, and the most of those and the first k cards' total. O(k) |
| `max_score_circle.kara` | the last k cards laid before the first k in a `VecDeque`, as if the row were a circle cut between them, and the best k in a row across the cut found by a sliding sum. O(k) |
| `max_score_solution.kara` | a Rust solution as LeetCode's Rust users write it (the cards not taken are a window of `n - k as usize` in the middle, so the total less the least such window, slid with `usize` indices), carried to Kāra by `karac fix`. O(n) |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and three
more (`12 4 55 1 202 248`); the constraints' most, 10^5 cards of 10^4
points all taken and 10^5 drawn cards with k = 1, 5 * 10^4 and 10^5 - 1
(`10^5 cards: 1000000000 8592 236224345 471626796`); and 2000 random
cases of 1 to 60 cards of up to 10, 100 or 10^4 points (`2000 random
cases: 58507141 in all, checksum 611983343`). `max_score.py` mirrors the
★ arm, and its output is byte-identical. Every arm gives the same output
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★, prefix, scan and circle arms check clean as first
written. The Rust solution takes one round of 16 fixes by `karac fix`'s
count: `struct Solution;` to `struct Solution {}`, `Vec<i32>` to
`Vec[i32]`, `n - k as usize` to `n - k`, and `Solution::` to
`Solution.`. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way to make k steps, each taking the card at the
beginning or at the end of what is left of the row, played out on a
`VecDeque`, and the most points kept, while k is at most 12. LeetCode's
examples, five edge cases (a large card out of reach in the middle, one
card, the best all from the front, all from the back, and split), the
constraints' most four ways (10^5 cards of 10^4 all taken, and 10^5
drawn cards with k = 1, 5 * 10^4 and 10^5 - 1), and 1991 random cases, 1
to 60 cards two times in three and up to 2000 otherwise, of up to 10,
100 or 10^4 points, k up to every card, or up to 12 half the time. Each
case also draws a lift of 1 to 10 points for P5.

The fixed cases were first written as a typed list of tuples, `let
fixed: Vec[(Vec[i32], i64)] = [([1, 2, 3, 4, 5, 6, 1].to_vec(), 3),
..].to_vec()`, which is refused at each tuple, "expected '(Vec[i32],
i64)', found '(Vec[i64], i64)'", with advice to annotate the binding,
which already is, and no fix: the slot's `i32` reached a `[..].to_vec()`
at a `let` of its own, but not one inside a tuple
([B-2026-11-26-78](https://github.com/karalang/kara/blob/main/docs/bugs-v2.jsonl),
fixed). The fixed cases are then moved into the list of cases with `for
(c, k) in fixed`, which moves out of a borrowed element; `karac fix`
writes `fixed.into_iter()`, 1 fix.

| | property |
|---|---|
| P1 | the statement read literally, while k is at most 12 |
| P2 | at least the first k cards or the last k, and at most the k largest |
| P3 | the row turned round gives the same points |
| P4 | one step more, while cards are left, takes more points |
| P5 | a lift of every card by the same points lifts the score by k times as much |
| P6 | the ★ arm's answer |

All 56,405 checks pass on every arm: `2003 cases: checksum 29083555,
56405 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by the first k
cards traded one at a time for the last, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the last window's sum taken, not the best | P1 903, P2 928, P3 1885, P6 6008 |
| M2 | ★: the window slides off the wrong front card | P1 775, P2 85, P3 1548, P6 5548 |
| M3 | prefix: all k cards from the back never tried | P1 323, P2 360, P3 738, P6 360 |
| M4 | prefix: each prefix holds one card, not the sum | P1 1245, P2 1879, P3 1888, P4 1006, P5 1844, P6 1896 |
| M5 | scan: the front cards alone never counted | P1 323, P2 360, P3 738, P6 360 |
| M6 | scan: the back cards taken from the wrong end | P1 797, P2 101, P3 1548, P6 1418 |
| M7 | circle: the last window never summed | P1 323, P2 360, P3 738, P6 360 |
| M8 | circle: the back cards taken in the wrong order | P1 797, P2 101, P3 1548, P6 1418 |
| M9 | solution: the last window's sum taken as the least | P1 921, P2 957, P3 1885, P6 1516 |
| M10 | solution: the last window never tried | P1 323, P2 360, P3 738, P6 360 |

## Benchmarks

The bench draws a pool of 10^6 cards of 1 to 10^4 points and runs the ★
arm, taking its window as a `Slice[i32]`, on 5 * 10^4 windows of 10^5 of
them, each window's start and its k drawn. Every implementation prints
`5 * 10^4 windows of 10^5 cards: checksum 203995922`.

BENCHTAB

Measured by hand, Kāra takes 0.90 s against Rust's 0.66 s (0.90 to 1.00
s with overflow checks on), C's 0.67 s and Go's 1.06 s; Python takes 130
s.
