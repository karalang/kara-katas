# 2134. Minimum Swaps to Group All 1's Together II

A **swap** is defined as taking two **distinct** positions in an array
and swapping the values in them.

A **circular** array is defined as an array where we consider the
**first** element and the **last** element to be **adjacent**.

Given a **binary circular** array `nums`, return the minimum number of
swaps required to group all `1`'s present in the array together at
**any location**.

```
nums = [0,1,0,1,1,0,0]        ->  1
nums = [0,1,1,1,0,0,1,1,0]    ->  2
nums = [1,1,0,0,1]            ->  0
```

**Constraints:** `1 <= nums.length <= 10^5`; `nums[i]` is either `0`
or `1`.

With k 1s in all, the 1s end up filling some k places in a row round
the circle. Every 0 among those places has to swap with a 1 outside
them, and one swap mends one such pair, so the answer is k less the
most 1s that any window of k places holds. O(n).

## Approaches

| file | mechanism |
|---|---|
| `swaps.kara` ★ | a window of k slid once round the circle by index mod n, its count of 1s kept as it goes |
| `swaps_prefix.kara` | the array laid twice end to end in a prefix sum, so that every window round the circle is a plain range counted by one subtraction |
| `swaps_zeros.kara` | the 0s instead: round a circle the 1s are together exactly when the 0s are, so a window of the n - k places the 0s will take slides over the array `chain`ed to itself, and the fewest 1s inside it is the answer |
| `swaps_struct.kara` | a `struct Window` that knows its size, start and count, built by `at_start` and moved on by `slide` (`mut ref self`) |
| `swaps_fold.kara` | the first window summed with `take(k)`, then one `fold` over the later ends carrying the pair (1s now, most so far), its closure taking a tuple pattern |
| `swaps_solution.kara` | LeetCode's Rust template: k as a `usize` from `filter` and `count`, the window's count changed by `as usize` casts; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more (one 0, one 1, 1 and 0 in turn, and no 1 at all), each with its
answer; then the total and a checksum over 2000 random arrays of 1 to
12, a 1 one time in 2, 3 or 5 in turn; then the constraints' largest,
100000 values: 1 and 0 in turn, 1s at both ends grouped across the
wrap, and at random. `swaps.py` mirrors the ★ arm and its output is
byte-identical.

No compiler gap was met. `karac fix` carries the template in three
rounds of 10, 3 and 3 edits: Rust's spellings (`Vec<..>` to `Vec[..]`,
the `&&x` and `&v` patterns to `x` and `v`, `struct Solution;` to
`struct Solution {}`, the adapter's `&Vec` to `ref Vec`, `Solution::` to
`.`); then the two `as usize` casts that change the window's count to
`as i64`, since `count` gives an `i64`, and the adapter's `as i64`
dropped, since an `i32` widens on return; then those two `as i64` casts
dropped in turn, since an `i32` widens there too, and the `ref` dropped
from the adapter's parameter, which borrows already. The `(k - mx) as
i32` is kept, since it narrows.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a search, breadth first, over every arrangement that swaps
of two values reach from the array, until one has its 1s together round
the circle, that is with at most one place where a 1 is followed by a
0; no window is assumed. It checks 300 random arrays of 1 to 8, a 1 one
time in 2, 3 or 5 in turn; then 30 of 1 to 8 with a single 0 or a single
1; then 30 of 9 or 10 at random. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the array turned by one, the first moved last: the same answer |
| P3 | the array reversed: the same answer |
| P4 | every 0 made 1 and every 1 made 0: the same answer |
| P5 | the array sorted, its 1s first: 0 |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 arrays: checksum 311724304, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
arrays by the same search. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Twenty-nine edits to the differential, four to five to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the window never wrapping | P1 38, P2 57, P3 57, P4 87, P6 38 |
| M4 | ★: the value left taken one place late | P1 131, P2 150, P3 134, P4 235, P6 131 |
| M5 | ★: the fewest 1s rather than the most | P1 242, P5 251, P6 242 |
| M6 | prefix: the prefix over one copy only | P1 43, P2 43, P4 109, P6 43 |
| M7 | prefix: the last start never tried | P1 59, P2 92, P3 73, P4 127, P5 12, P6 59 |
| M9 | prefix: k counted over both copies | P1 134, P4 92, P5 149, P6 134 |
| M10 | zeros: the 0s' window the size of the 1s' | P1 111, P4 305, P5 84, P6 111 |
| M11 | zeros: the window's first value never taken off | P1 178, P2 141, P3 143, P4 143, P5 251, P6 178 |
| M26 | zeros: the first window one place on | P1 141, P2 167, P3 143, P4 185, P5 188, P6 141 |
| M15 | struct: the window started with one fewer | P1 121, P2 148, P3 117, P4 258, P5 272, P6 121 |
| M16 | struct: one slide fewer | P1 47, P2 92, P3 73, P4 89, P6 47 |
| M17 | struct: the value reached read one place on | P1 106, P2 137, P3 114, P4 155, P6 106 |
| M18 | fold: the first window over k + 1 | P1 114, P2 137, P3 114, P4 158, P6 114 |
| M21 | fold: the 1s now never carried | P1 103, P2 136, P3 143, P4 143, P5 251, P6 103 |
| M28 | fold: the 1s now kept for the most | P1 165, P2 136, P3 143, P4 143, P6 165 |
| M22 | solution: the empty case returning 1 | P1 88, P4 109, P5 88, P6 88 |
| M23 | solution: the adapter dropping the first value | P1 27, P2 16, P3 18, P6 27 |

P1 and P6 kill all seventeen, P4 fifteen, P2 thirteen, P3 twelve and P5
nine. P4 trades the 1s for the 0s, which changes k for the window and
every count in it, so nearly any edit to the window shows: all but the
fewest-1s edit (M5), which stays wrong the same way, and the adapter's
lost first value (M23), whose loss the flip keeps. P2 and P3 turn and
reverse the circle, which every right answer ignores; they see an edit
that ties the answer to where the array starts or which way it runs: a
window that does not wrap (M1), a start left untried (M7, M16), a
window or a count off by a place (M4, M11, M15, M17, M18, M21, M26,
M28), the prefix over one copy (M6), and the adapter's lost first value
(M23). P5 sorts the 1s to the front, which needs no swap; it sees the
edits that answer that array wrongly, by the fewest 1s (M5), by the
wrong k or the wrong window size (M9, M10, M15, M26), by a count that is
never taken down (M11, M21), by a start left untried (M7), or by the
empty case (M22), since every array of 0s sorts to itself.

Of the twenty-nine, twelve were not kept. Six are equivalent, and five
of them for one reason: the slide visits n + 1 windows round a circle
of n, so the last is the first again, and an edit that loses either one
of the two loses nothing. They are the ★ arm's slide stopping one short
and its first window never counted, the zeros arm's last window never
tried, and the fold's most taken before its last step and started at
0. The sixth is the struct arm's start never wrapped, since it slides
only n - 1 times and never reaches the end. One fails by a crash: the
prefix arm's window one place short, which reads before the table when
k is 0. One fails as a kept one does: the zeros arm counting its 1s as
0s, as M10. Four are killed with checks of their own but were left out
because their arms keep their share: the zeros arm's slide turned round
(P1 216, P2 141, P3 143, P4 143, P5 251, P6 216), the fold's value left
read at the window's end (P1 73, P2 96, P3 93, P4 146, P6 73), and the
template's window wrapping one early (P1 110, P2 134, P3 134, P4 237, P6
110) and its 0s counted as k (P1 232, P4 305, P5 221, P6 232).

## Verification

Every arm prints the same output as `swaps.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.75 s to 1.6 s and the
differential 0.45 s.

## Benchmarks

The bench builds 20 arrays of 100000 once, a 1 one time in 2 to 21 by
array; then solves every array 10 times, one value flipped before each
solve so that no solve repeats one before, with the ★ arm in all five
languages. Every implementation prints `200 solves: 2031370 swaps in
all, checksum 239205856`.

BENCHTAB
