# 1718. Construct the Lexicographically Largest Valid Sequence

Given an integer `n`, find a sequence with elements in the range
`[1, n]` that satisfies all of the following:

- The integer `1` occurs once in the sequence.
- Each integer between `2` and `n` occurs twice in the sequence.
- For every integer `i` between `2` and `n`, the **distance** between
  the two occurrences of `i` is exactly `i`.

The **distance** between two numbers on the sequence, `a[i]` and
`a[j]`, is the absolute difference of their indices, `|j - i|`.

Return *the **lexicographically largest** sequence. It is guaranteed
that under the given constraints, there is always a solution.*

A sequence `a` is lexicographically larger than a sequence `b` (of the
same length) if in the first position where `a` and `b` differ, sequence
`a` has a number greater than the corresponding number in `b`. For
example, `[0,1,9,0]` is lexicographically larger than `[0,1,5,6]`
because the first position they differ is at the third number, and `9`
is greater than `5`.

```
n = 3    ->  [3,1,2,3,2]
n = 5    ->  [5,3,1,4,3,5,2,4,2]
```

**Constraints:** `1 <= n <= 20`.

## Approaches

| file | mechanism |
|---|---|
| `sequence.kara` ★ | the sequence filled from the front, the first empty slot taking the largest number still free that fits, a number v > 1 its slot and the one v later; when nothing fits the last choice is undone. Trying larger numbers first, the first complete sequence found is the largest. Exponential in principle, but for n up to 20 it meets few dead ends |
| `sequence_bits.kara` | the same search with the numbers still free as the set bits of an `i64`, handed down by value, so undoing a choice is only the slots; the largest free number is found from `leading_zeros` |
| `sequence_stack.kara` | the same order of search with a stack of (slot, number) choices instead of recursion: when nothing fits the last choice is popped and its slot tried from the number below the one it held |
| `sequence_solution.kara` | a Rust solution as LeetCode's Rust users write it, a nested `fn dfs` taking `&mut Vec<i32>` and `&mut Vec<bool>`, `usize` indices and `n as usize`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 6 lines: LeetCode's two examples, the smallest
two n and the largest; then a checksum of the answers for every n from 1
to 20, all the constraints allow. `sequence.py` mirrors the ★ arm and
its output is byte-identical.

```
[3, 1, 2, 3, 2]
[5, 3, 1, 4, 3, 5, 2, 4, 2]
[1]
[2, 1, 2]
[20, 18, 19, 15, 13, 17, 10, 16, 7, 5, 3, 14, 12, 3, 5, 7, 10, 13, 15, 18, 20, 19, 17, 16, 12, 14, 11, 9, 4, 6, 8, 2, 4, 2, 1, 6, 9, 11, 8]
every n from 1 to 20: 400 values, checksum 160066442
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every way to put each number from n down to 2 in two empty
slots that far apart, and 1 in one, among 2n - 1 slots, all of them
collected and the largest taken. That count grows too fast past n = 7, so the
literal reading answers up to 7, and every n from 1 to 20, the whole
range, is checked against the other properties.

| | property |
|---|---|
| P1 | up to n = 7, the answer is the statement read literally |
| P2 | the answer is valid: 2n - 1 values, 1 once, each of 2 to n twice and that far apart |
| P3 | the answer starts with n |
| P4 | the answer reversed, valid too, is no larger |
| P5 | each arm agrees with at least two of the other three |

The differential prints `20 problems: checksum 518875011, 400 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, every valid sequence up to n = 7 enumerated
and the `max` taken, gives the same checksum. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Four first drafts sent the search
down long dead ends, the ★ arm trying the smallest number first, its
next slot found by one step instead of a walk, a 2 placed only once, and
the solution's second slot not checked empty, and were replaced: each
ran past a minute under the interpreter. M1, M4 and M8 all let a number
be used twice, M2, M6 and M9 all stop a slot short of the end, and M3,
M5 and M10 all leave an undone choice's slot filled; each group fails
the very same checks. M7 alone keeps every answer valid, and only P5
sees that its answers past n = 7 are not the largest.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a number never marked used | P1 5, P2 18, P5 18 |
| M2 | ★: the sequence done one slot before the end | P1 2, P2 3, P3 1, P5 3 |
| M3 | ★: an undone choice's first slot left filled | P1 3, P2 16, P3 3, P5 16 |
| M4 | bits: a number left in the mask once placed | P1 5, P2 18, P5 18 |
| M5 | bits: an undone choice's first slot left filled | P1 3, P2 16, P3 3, P5 16 |
| M6 | stack: the sequence done one slot before the end | P1 2, P2 3, P3 1, P5 3 |
| M7 | stack: a taken-back slot tried from two below the number it held | P5 6 |
| M8 | stack: a used number not refused | P1 5, P2 18, P5 18 |
| M9 | solution: the sequence done one slot before the end | P1 2, P2 3, P3 1, P5 3 |
| M10 | solution: an undone choice's first slot left filled | P1 3, P2 16, P3 3, P5 16 |

## Benchmarks

The bench answers every n from 1 to 20, the whole range, 2000 times by
the ★ arm in all five languages. Every implementation prints `every n
from 1 to 20, 2000 rounds: 800000 values, checksum 171609845`. The work
is the search's recursion and the slots it writes and undoes. The C
build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.464 s |
| Go | 0.529 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.589 s |
| Rust (`rustc -O`) | 0.616 s |
| Kāra (`karac build`) | 0.648 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.651 s |
| Python | 8.2 s |

The sequential Kāra build takes 1.06x Rust's time and 1.11x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.464 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.633 s and 0.633 s on one
run).

## Verification

All four arms print the same output as `sequence.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ and stack arms checked clean as first written. The bits arm first
cleared a number's bit with Rust's `free & !(1 << v)`; in Kāra `!` is
only the logical not and `~` the bitwise one, and `karac fix` wrote
`~(1 << v)`.

LeetCode's Rust template took one `karac fix` of 24 edits:
`struct Solution {}` added, the nested `fn dfs` moved out of the method
to the top level, `usize` written `i64`, `&mut Vec<i32>` and
`&mut Vec<bool>` written `mut ref Vec[i32]` and `mut ref Vec[bool]`,
the calls' `res, used` and `&mut res, &mut used` written `mut res,
mut used`, `&&` and `||` written `and` and `or`, and `vec![0; 2 * n -
1]` and `vec![false; n + 1]` written `Vec.filled(..)`. `n as usize`
became `n as i64`, and `x as i32` carried over as written.

The differential checked clean as first written. `arm_name` in it
indexes a list of string literals for a `Str`, as #1662's does
(B-2026-11-19-131).
