# 1535. Find the Winner of an Array Game

Given an integer array `arr` of distinct integers and an integer `k`, a
game is played between the first two elements of the array (`arr[0]` and
`arr[1]`). In each round, the larger of the two wins and stays at
position 0, and the smaller moves to the end of the array. The game ends
when an integer wins `k` consecutive rounds. Return the integer that wins.
It is guaranteed that there will be a winner.

```
arr = [2,1,3,5,4,6,7], k = 2               ->  5
arr = [3,2,1], k = 10                      ->  3
arr = [1,9,8,2,3,7,6,4,5], k = 7           ->  9
arr = [1,11,22,33,44,55,66,77,88,99], k = 1000000000  ->  99
```

**Constraints:** `2 <= arr.length <= 10^5`; `1 <= arr[i] <= 10^6`; the
values are distinct; `1 <= k <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `winner.kara` ★ | one pass. The front only ever meets the values after it in order, and a loser goes behind everything still to come, so the front is a running maximum and its streak counts the values it has beaten since it got there. A streak reaching `k` wins; with none by the end, the front is the largest value, which wins any `k`. O(n) whatever `k` is |
| `winner_deque.kara` | the game played as written on a `VecDeque`: two values off the front, the larger back on the front and the smaller on the back. A streak of `k` wins, and a streak of `n - 1` means the front has beaten every other value. O(n) rounds |
| `winner_iter.kara` | the ★ arm as a `try_fold` over the values after the first, a streak reaching `k` breaking out with the winner as the `Err` |
| `winner_solution.kara` | LeetCode's Rust template (`arr: Vec<i32>`, `for &x in arr.iter().skip(1)`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's four examples, `[5, 1]`
and `[1, 5]` with `k = 1`, `[4, 3, 2, 1, 5]` with `k = 3`, 1 to 100000
with `k = 1` and `k = 99999`, then checksums of the answers for 3000
random arrays of 2 to 12 values with `k` up to 15, 300 of 2 to 1000 with
`k` up to 2000 and 3 of 2 to 100000 with `k` up to 10^9, the values
distinct multiples of 3, shuffled. `winner.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the game played round by round on a `Vec`, the loser removed
and pushed on the end, until a value has won `k` rounds in a row. It
checks 3000 arrays of 2 to 12 distinct values with `k` from 1 to 15,
every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | `k` of `n - 1` or more gives the largest value |
| P3 | `k = 1` gives the larger of the first two values |
| P4 | every value `v` made `2v + 1` makes the answer `2 * answer + 1` |
| P5 | one more win needed never gives a smaller winner |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 155017276, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends; M5 by a hang (no streak ever grows),
stopped after 40 s under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a new front starts its streak at 0 | P1 99, P3 468, P6 99 |
| M2 | ★: with no streak of `k`, the last value | P1 1631, P2 2408, P5 168, P6 1631 |
| M3 | ★: the second value never met | P1 787, P2 580, P3 1968, P6 787 |
| M4 | deque: a streak of `n - 2` taken as the end | P1 179, P2 216, P6 179 |
| M5 | deque: the winner sent to the back and the loser to the front | hangs |
| M6 | deque: a new front starts its streak at 0 | P1 99, P3 468, P6 99 |
| M7 | iter: a new front starts its streak at 0 | P1 99, P3 468, P6 99 |
| M8 | iter: with no streak of `k`, the first value | P1 1725, P2 2462, P5 161, P6 1725 |
| M9 | template: the second value skipped | P1 787, P2 580, P3 1968, P6 787 |
| M10 | template: `k + 1` wins needed | P1 163, P3 949, P6 163 |

## Benchmarks

The bench builds 100 random arrays of 100000 distinct values once (the
multiples of 3 shuffled), each with its own `k` from 1 to 200000, and
answers each 20 times by the ★ arm, in all five languages. Every
implementation prints `20 passes over 100 arrays of 100000 values:
checksum 43107105`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `3d1fc8e26` on LLVM 22:

| | median |
|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.204 s |
| Kāra (`karac build`) | 0.214 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.224 s |
| C (`clang -O3`) | 0.240 s |
| Rust (`rustc -O`) | 0.240 s |
| Go | 0.263 s |
| Python | 16.9 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.17 s and 0.18 s on one run).

Kāra is 0.91x Rust under overflow checks by median. Not traced. Building
the arrays (10 million draws and swaps) is a large share of every row,
and the rows sit within 30% of one another, so the order among the
compiled languages here says little.

## Verification

All four arms print the same output as `winner.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `3d1fc8e26`.

## Writing it

The ★ and iterator arms were written in Kāra and checked as written. The
deque arm took one edit: `Deque[i64]` is refused as an undefined type,
with `VecDeque` as the fix, applied.

The deque arm then did not finish under `karac __mir-run` in 300 s,
though `karac __mir-llvm-run` ran it at once. The interpreter keeps a
deque as a `Vec` with an offset to its front, and `pop_front` dropped the
empty front slots as soon as they outnumbered the elements; the
`push_front` after it opened as many again, so each round of this game
moved the whole deque twice. Fixed in kara `3d1fc8e26` (B-2026-11-14-4): the
slots are dropped once they are more than twice the elements.

The Rust template took 5, 1 and 1 changed lines over three rounds:
`Vec<i32>` to `Vec[i32]` (and `Vec<i64>` and `Vec<i32>` in the wrapper),
`for &x in` to `for x in`, the wrapper's `|&x|` to `|x|` and `Solution::`
to `Solution.`; then the `struct Solution {}` the template leaves out
added; then the closing `as i64` dropped (an `i32` widens). It checks and
agrees with no hand edit.
