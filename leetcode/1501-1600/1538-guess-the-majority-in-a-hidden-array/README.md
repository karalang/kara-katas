# 1538. Guess the Majority in a Hidden Array

You are given an array `nums` of `0`s and `1`s that you cannot read. You
only have an `ArrayReader` API:

- `query(a, b, c, d)` for `0 <= a < b < c < d < length` returns the
  distribution of the four values `nums[a], nums[b], nums[c], nums[d]`:
  `4` if all four are equal, `2` if three are equal and one differs, `0`
  if two are `0` and two are `1`;
- `length()` returns the array's length.

Return any index of the more frequent value, or `-1` if there are as many
`0`s as `1`s. You may call `query` at most `2 * n` times.

```
nums = [0,0,1,0,1,1,1,1]  ->  5   (any index of a 1: 2, 4, 5, 6 or 7)
nums = [0,0,1,1,0]        ->  0   (any index of a 0: 0, 1 or 4)
nums = [1,0,1,0,1,0,1,0]  ->  -1
```

**Constraints:** `5 <= nums.length <= 10^5`; `0 <= nums[i] <= 1`.

## Approaches

Every arm is `fn guess_majority(reader: ArrayReader) -> i64` over the same
reader. `ArrayReader` is the judge's side, written with LeetCode's `i32`
API: a `shared struct` holding the bits and a `mut calls` count, `shared`
because the API takes the reader by a plain borrow, as LeetCode's `&self`
does, while the judge still counts every query. Any index of the majority
bit is right, so the harness judges an answer rather than printing it:
the majority bit it points at, `-1` for `-1`, or `-2` for a wrong answer.

The arms rest on one fact: two queries that differ in one place are equal
exactly when the two places swapped hold the same bit.

| file | mechanism |
|---|---|
| `majority.kara` ★ | every bit compared with bit 0: with `q0123 = query(0, 1, 2, 3)`, `query(1, 2, 3, i)` equals it exactly when bit `i` is bit 0's, for every `i` from 5 and from 4 by `query(1, 2, 3, 4)` itself; bits 1, 2 and 3 are each swapped out for bit 0 against `query(1, 2, 3, 4)`. Then the count. `n` queries |
| `majority_last.kara` | the same from the other end, every bit compared with the last: below `n - 4` against `query(n - 4, n - 3, n - 2, n - 1)`, and `n - 4` to `n - 2` each swapped for the last against `query(n - 5, n - 4, n - 3, n - 2)`. `n + 1` queries |
| `majority_iter.kara` | the ★ arm with iterators: the first five bits in an array literal, the rest a `map` over the queries `chain`ed after them, then `filter(..).count()` and `position` |
| `majority_solution.kara` | LeetCode's Rust template (`guess_majority(reader: &ArrayReader) -> i32`, the ★ arm with `vec![true; n as usize]` and iterator counting), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 11 lines: the three LeetCode examples, then
`[1,1,1,1,1]`, `[0,1,1,1,1]` and `[1,0,0,0,0,1]`; 100000 alternating
bits (a tie) and 100001; then the ties and a checksum of the judged
answers for 3000 random arrays of 5 to 12 bits, 300 of 5 to 1000 and 30
of 5 to 100000, each with its own chance of a 1. `majority.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the bits counted outright, the answer judged against the more
frequent one. It checks 3000 arrays of 5 to 40 bits, every random choice
drawn before any arm answers.

| | property |
|---|---|
| P1 | the judged answer is the statement read literally |
| P2 | the arm asks at most `n + 1` queries (the problem allows `2n`) |
| P3 | every bit flipped flips the judged answer, and keeps a tie |
| P4 | the bits reversed keep the judged answer |
| P5 | one more of the winning bit (a `1` after a tie) makes that bit win |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 573338526, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: bit 4 taken as bit 0's without asking | P1 119, P3 119, P4 182, P5 54, P6 119 |
| M2 | ★: bit 1 placed with `!=` | P1 271, P3 271, P4 188, P5 122, P6 271 |
| M3 | ★: the loop from 6, bit 5 never asked | P1 113, P3 113, P4 163, P5 65, P6 113 |
| M4 | last: the loop stops one short, at `a - 1` | P1 141, P3 141, P4 182, P6 141 |
| M5 | last: bit `n - 4` compared against `t`, not `u` | P1 154, P3 154, P4 183, P5 67, P6 154 |
| M6 | last: a tie read as the last bit winning (`>=`) | P1 83, P3 83, P6 83 |
| M7 | iter: the chain from 4, bit 4 asked twice | P1 98, P3 98, P4 127, P5 57, P6 98 |
| M8 | iter: the answer for a losing bit 0 is a place of bit 0 | P1 667, P3 667, P4 960, P5 704, P6 667 |
| M9 | template: bit 3 against `query(0, 1, 2, 3)` | P1 139, P3 139, P4 183, P5 84, P6 139 |
| M10 | template: a tie read as the other bit winning (`<=`) | P1 83, P3 83, P6 83 |

## Benchmarks

The bench builds 100 readers of 5 to 50000 bits once, each with its own
chance of a 1, and asks each 20 times by the ★ arm, in all five languages.
Each language's reader keeps the query count as the API's judge would:
Kāra's in a `shared struct`'s `mut` field, Rust's in a `Cell` behind
`&self`, C's and Go's through a pointer. Every implementation prints `20
passes over 100 readers of up to 50000 bits: checksum 335452702, 50412680
calls`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `3d1fc8e26` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.109 s |
| Rust (`rustc -O`) | 0.124 s |
| Kāra (`karac build`) | 0.252 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.260 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.279 s |
| Go | 0.480 s |
| Python | 8.3 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time equals its real time (0.25 s and 0.25 s on one run).

Kāra is 0.93x Rust under overflow checks by median. Not traced. Plain
Rust and C are about twice as fast as either checked build, which fits
the counting loop: unchecked, `with_zero += 1` over a `bool` vector can
be vectorized, and an overflow check on each add stops that.

## Verification

All four arms print the same output as `majority.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `3d1fc8e26`.

## Writing it

The ★ arm was written in Kāra and checked as written. The last and iter
arms each took one edit from `karac fix`: the `filter` closure's `**s`
to `*s`, since Kāra's `filter` hands the closure one borrow, not
Rust's two.

The Rust template took 5, 1, 3, 2 and 2 edits over five rounds: `&ArrayReader`
to `ref ArrayReader`, `|&&s| s` to `|s| s`, `|&s| !s` to `|s| not s`,
`Solution::` to `Solution.` and `&reader` to `reader`; then
`struct Solution {}` added; then `ref ArrayReader` to `ArrayReader`
(a parameter borrows already), `vec![true; n as usize]` to
`Vec.filled(n as usize, true)` and the closing `as i64` dropped; then
`as usize` to `as i64` in two places; then those `as i64` casts dropped.
It checks and agrees with no hand edit.
