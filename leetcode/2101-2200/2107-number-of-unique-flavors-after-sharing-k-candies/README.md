# 2107. Number of Unique Flavors After Sharing K Candies

You are given a 0-indexed integer array `candies`, where `candies[i]`
represents the flavor of the `i`th candy. Your mom wants you to share
these candies with your little sister by giving her `k` consecutive
candies, but you want to keep as many flavors of candies as possible.

Return the maximum number of unique flavors of candy you can keep after
sharing with your sister.

```
candies = [1,2,2,3,4,3], k = 3   ->  3
candies = [2,2,2,2,3,3], k = 2   ->  2
candies = [2,4,5], k = 0         ->  3
```

**Constraints:** `1 <= candies.length <= 10^5`; `1 <= candies[i] <=
10^5`; `0 <= k <= candies.length`.

The shared candies are a window of `k`, and every start from 0 to `n -
k` is a choice. Moving the window one place right takes back the candy
leaving it and gives away the one entering it, so the flavors kept can
be kept up to date in constant time per start, with a count per flavor.

## Approaches

| file | mechanism |
|---|---|
| `flavors.kara` ★ | a `Map` of every flavor's count with the first `k` candies taken out, then slid: the candy entering the window given away, the one leaving it kept again, and the flavors with a count above zero tracked as counts cross zero. O(n) |
| `flavors_array.kara` | the same window over a flat array of counts indexed by flavor, `Vec.filled(100001, 0)`, written as a `while` loop over the window's start, the first window given away inside it. O(n + F) |
| `flavors_spans.kara` | each flavor's first and last place, in two `Map`s: a flavor is lost exactly for the starts from `last - k + 1` to `first`, so each such range is marked in a difference array and the start with the fewest marks wins. O(n) |
| `flavors_struct.kara` | a `struct Jar` of counts and the flavors present, its `add` and `remove` methods (`mut ref self`) keeping that number as counts cross zero, filled over `enumerate()` with the candies past the first `k` and slid |
| `flavors_fold.kara` | one `fold` over the later starts, its state the counts, the flavors present and the best so far, a tuple moved through each step and taken apart with `let mut (kept, present, best) = state` |
| `flavors_solution.kara` | LeetCode's Rust template (`Vec<i32>`, `k as usize`, a `HashMap` through `entry().or_insert`, `get_mut` and `remove` so that `len()` is the answer), carried by `karac fix` in four rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples and four
more (every candy given; one flavor only; every flavor once with one
given; a flavor only a middle window takes away), each with its answer;
then the total for 3000 random rows of 1 to 40 candies of 1 to 8
flavors, sharing 0 to all of them, and a checksum of the answers; then
the constraints' largest, 10^5 candies: 1000 flavors in turn sharing
half, every flavor once sharing all but one, and every flavor once
sharing 777. `flavors.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every start in turn, the `k` candies from it given away, and
the flavors among the rest counted with a `Set`. It checks 300 random
rows of 1 to 12 candies of 1 to 5 flavors, sharing 0 to all of them;
then 30 of 1 to 300 candies of up to 10^5 flavors, nearly all distinct;
then 30 of 1 to 300 candies of 1 to 3 flavors. All 360 are drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is at most the flavors among all the candies, and at least that less `k` |
| P3 | the candies reversed: the same answer |
| P4 | every flavor `c` renamed `100001 - c`: the same answer |
| P5 | one candy fewer shared: an answer no smaller |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 rows: checksum 314189720, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
rows. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept, three
to each Kāra arm and two to the Rust-template arm. Each kept one is
killed, fails the same way under both backends and not by a crash, and
no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: a flavor counted present at zero | P1 170, P2 38, P3 47, P5 23, P6 170 |
| M3 | ★: a flavor lost never subtracted | P1 180, P2 125, P5 32, P6 180 |
| M4 | ★: a candy kept back counted present at two | P1 104, P2 79, P3 68, P5 29, P6 104 |
| M7 | array: one candy too few shared at first | P1 110, P3 17, P6 110 |
| M9 | array: a flavor lost while one candy remains | P1 31, P3 35, P5 1, P6 31 |
| M10 | array: a flavor's first candy not counted | P1 306, P2 126, P6 306 |
| M11 | spans: a flavor whose span fits counted kept | P1 118, P5 15, P6 118 |
| M13 | spans: the last place taken as the first | P1 21, P3 26, P6 21 |
| M14 | spans: the most lost taken | P1 338, P2 306, P6 338 |
| M16 | struct: a flavor removed at one | P1 95, P2 33, P3 47, P5 28, P6 95 |
| M19 | struct: the first window never counted | P1 4, P3 10, P6 4 |
| M20 | struct: a flavor present again at any count | P1 254, P2 224, P3 47, P6 254 |
| M22 | fold: a flavor lost kept present | P1 102, P2 56, P5 25, P6 102 |
| M23 | fold: a flavor taken back counted present at one | P1 133, P2 106, P3 25, P5 39, P6 133 |
| M24 | fold: each window one flavor short | P1 38, P3 45, P6 38 |
| M26 | solution: flavors five apart taken as one | P1 27, P2 27, P6 27 |
| M27 | solution: an emptied flavor kept in the map | P1 73, P6 73 |

P1 and P6 kill all seventeen, P2 ten, P3 ten, P5 eight and P4 none. P3
sees the edits that favour one end of the row: the first window left
out (M19), or given one candy too few (M7), the last place read as the
first (M13), and the edits whose miscount builds up as the window moves
right (M2, M4, M9, M16, M20, M23, M24). P2 sees the edits that count a
flavor no candy is left of, or lose one that is (M3, M10, M14, M20,
M22), or merge flavors (M26). P5 sees the edits whose error grows with
`k`, so that one candy fewer shared can answer less. P4 kills none: no
kept edit reads a flavor's value, only whether two are equal, and the
renaming keeps that; it guards an arm that would, as the array arm
indexes by flavor.

Of the thirty, thirteen were not kept, and one survives, equivalent to
the arm it edits: the struct arm's candy given before the one taken
back (M18). When they are the same flavor, `remove` first takes its
count to one less and `add` brings it back, with `present` unchanged
either way. Of the other twelve, all killed, eight fail as a kept one
or as each other: the ★ arm's shared candies never taken out, the spans
arm's lost runs closed where they open, the struct arm's every candy
kept at first and the fold arm's every candy in the first window all
fail as P1 143, P6 143, the answer for nothing shared; the fold arm's
first window's best left out and the Rust arm's first window never
counted fail as M19; and the ★ arm's last window only and the Rust
arm's last window taken fail alike, P1 39, P3 47, P6 39. Four are
killed with checks of their own but were left out because their arm
keeps its share: the array arm's last window never tried and its candy
taken back never counted present, the spans arm's starts counted one
short, and the ★ arm's candy taken back on odd steps not counted.

## Verification

Every arm prints the same output as `flavors.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.9 s to 7.4 s, the array arm the
slowest, its `Vec.filled(100001, 0)` made once per call over 3000 rows.
The differential takes 4.7 s there and 0.6 s compiled.

`karac fix` carries the template in four rounds of 16, 2, 2 and 1
edits: Rust's spellings (`use std::collections::HashMap` dropped,
`Vec<..>` and `HashMap<..>` to brackets, `::` to `.`, the `&c` pattern
and the `&` before `candies[k..]` and each key dropped, `struct
Solution;` to `struct Solution {}`, the adapter's `&Vec` to `ref`);
then `HashMap` to `Map`; then `k as usize` to `k as i64` and the
adapter's `as i64` dropped as widening; then the adapter's `ref`
parameter to a bare one.

The third round needed a compiler fix (kara RANGESHA). The template's
`for i in k..candies.len()` has a `usize` start and Kāra's `i64`
`len()`, and the range's bounds check let the two meet, so the template
ran with its FFI-only `usize` and nothing said. The same pair under an
operator, `k + candies.len()`, was already an error whose fix turns the
`as usize` into `as i64`; a range's bounds of opposite signedness are
now the same error with the same fix. `tests/kata_2107_mixed_sign_range.rs`
pins it.

## Benchmarks

The bench builds 20 rows of 10^5 candies once, each of up to 5000
flavors; then shares each 5 times, up to 10^5 candies at a time, with
the ★ arm in all five languages: the counts in a hash map and the
sliding window. Every implementation prints `100 shares: 202769 flavors
kept, checksum 393718393`.

BENCHTAB
