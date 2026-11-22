# 2767. Partition String Into Minimum Beautiful Substrings

Given a binary string `s`, partition the string into one or more
**substrings** such that each substring is **beautiful**.

A string is **beautiful** if:

- It doesn't contain leading zeros.
- It's the **binary** representation of a number that is a power of
  `5`.

Return *the **minimum** number of substrings in such partition.* If it
is impossible to partition the string `s` into beautiful substrings,
return `-1`.

A **substring** is a contiguous sequence of characters in a string.

```
s = "1011"  ->  2
s = "111"   ->  3
s = "0"     ->  -1
```

**Constraints:** `1 <= s.length <= 15`, `s[i]` is either `'0'` or `'1'`.

## Approaches

In 15 binary digits there are seven powers of 5, from 1 to 15625
(`11110100001001`), and every piece must be one of them.

| file | mechanism |
|---|---|
| `beautiful.kara` ★ | the fewest pieces for each prefix: every last piece `s[j..i]` tried, kept when it starts with a 1 and its value, read by `i64.from_str_radix`, is a power of 5. O(n^3) |
| `beautiful_search.kara` | every way to cut the string found by a recursive search from the left: at each place every piece starting there with a 1 that reads as a power of 5 taken in turn, and the fewest pieces over the cuts that reach the end kept; no table. Exponential in the worst case |
| `beautiful_bfs.kara` | the places between characters as nodes, an edge from i to j wherever `s[i..j]` is one of the seven powers written in binary, found by `starts_with` on the slice from i; a breadth-first search over a `VecDeque` from 0 reaches n in the fewest pieces. O(n) |
| `beautiful_memo.kara` | the fewest pieces from each place to the end, by a recursive call remembered in a `Vec[Option[i64]]`, the string's bits read once into a `Vec[i64]` and every piece's value built a bit at a time; a power of 5 asked of a closure. O(n^2) |
| `beautiful_solution.kara` | a Rust solution as LeetCode's Rust users write it, `s.as_bytes()`, a `vec![i32::MAX; n + 1]` table, each piece's value built in a `u32` and divided down by 5, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples; one 1;
25, 125 and 625 whole; 5 twice; 15625 whole, the greatest power of 5
that fits; every string of 1 to 10 binary digits; and 3000 strings of
powers of 5 joined while they fit in 15 digits, LeetCode's most, half
of them with one place flipped, the last two with the count that split,
the sum of the pieces and a checksum. `beautiful.py` mirrors the ★ arm
and its output is byte-identical.

```
2
3
-1
1
1
1
2
1
1
2046 strings up to 10 long: 129 split, pieces sum to 569, checksum 452604175
3000 joined powers: 1864 split, pieces sum to 4345, checksum 14255844
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every choice of cuts among the n - 1 places between
characters, as the bits of a number, kept when every piece has no
leading zero and equals one of the powers of 5 below `2^15` written out
in binary, and the fewest pieces over those kept, or -1; no table. It
takes every string of 1 to 8 digits, then draws 1500 strings of powers
of 5 joined while they fit in 12 digits, half of them with one place
flipped, and 500 the same up to 15, all before any arm answers; the
literal reading is asked only up to 12 digits.

| | property |
|---|---|
| P1 | up to 12 digits, the answer is the literal reading's |
| P2 | a 1 put at the end of a string that splits: at most one more piece |
| P3 | the string written twice, when it splits: at most twice the pieces |
| P4 | a 0 put at the front: -1 |
| P5 | -1 or from 1 to n, and -1 whenever the string starts with a 0 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2510 cases: checksum 654274142, 75300 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same cuts gives the same checksum. On
a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M1 and M8 fail the same checks in the same
numbers, as do M4 and M5; so do M7 and M9, each leaving 1 the only
power of 5. M6 is the bfs arm as first written, without 15625, and only
P6 sees it: the literal reading stops at 12 digits.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a piece with a leading zero let through | P1 726, P4 2027, P5 243, P6 818 |
| M2 | ★: no piece cut from the start | P1 1185, P6 1307 |
| M3 | search: 3 taken as a power of 5 | P1 256, P6 273 |
| M4 | search: the first cut found kept, not the fewest | P1 281, P6 310 |
| M5 | bfs: a place reached again written over | P1 281, P6 310 |
| M6 | bfs: 5^6 left out of the powers | P6 40 |
| M7 | memo: every digit read as a 1 | P1 1117, P6 1239 |
| M8 | memo: a piece with a leading zero let start | P1 726, P4 2027, P5 243, P6 818 |
| M9 | solution: 5 itself never divided down | P1 1117, P6 1239 |
| M10 | solution: no split answered as 0 | P1 1101, P2 1146, P3 408, P4 2417, P5 1203, P6 1203 |

## Benchmarks

The bench draws 100000 strings of 15 binary digits, LeetCode's most:
powers of 5 joined while they fit, the rest filled with random digits,
and half the time one place flipped. It draws all of them first, then
answers each 5 times by the ★ arm in all five languages. Kāra and Rust
read each piece by `from_str_radix`, Go by `strconv.ParseInt`, Python
by `int(.., 2)`, and C digit by digit. Every implementation prints
`100000 strings of 15, 5 rounds: 117225 split, pieces sum to 411785,
checksum 61242312`.

BENCHTAB

## Verification

All five arms print the same output as `beautiful.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The bfs arm first listed six powers of 5, to 3125, and missed 15625,
which has 14 digits; on `11110100001001` it answered -1. Every arm
agreed and the differential passed: the literal reading stops at 12
digits, and its joined strings were drawn from the same six powers. The
harness now joins all seven and prints 15625 whole, and the differential
draws a power again when it is longer than the string may be.

The ★, search and bfs arms checked clean as first written. The memo arm
read the bits by `s.bytes().map(|b| b - b'0')`; `karac check` refused
it, `bytes` giving a `Slice[u8]`, and `karac fix` wrote
`s.bytes().iter().map(|b| (b - b'0') as i64)`. The harness took each
power by `powers[..]`, a `String` moved out of the list, and `karac
fix` wrote `let p = ref powers[..]`.

LeetCode's Rust template took 10 `karac fix` edits, the wrapper
included: `struct Solution {}` added; `s.as_bytes()` became
`s.bytes()`; `vec![i32::MAX; n + 1]` became `Vec.filled(n + 1,
i32.MAX)`; the other `i32::MAX`s became `i32.MAX`; `||` became `or`;
`(s[k] - b'0') as u32` dropped its cast, a `u8` widening into the `u32`
as it is; and `Solution::` became `Solution.`, with the wrapper's `as
i64` dropped.
