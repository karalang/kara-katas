# 2730. Find the Longest Semi-Repetitive Substring

You are given a digit string `s` that consists of digits from `0` to `9`.

A string is called **semi-repetitive** if there is **at most** one
adjacent pair of the same digit. For example, `"0010"`, `"002020"`,
`"0123"`, `"2002"`, and `"54944"` are semi-repetitive while the following
are not: `"00101022"` (adjacent same digit pairs are 00 and 22), and
`"1101234883"` (adjacent same digit pairs are 11 and 88).

Return the length of the **longest semi-repetitive substring** of `s`.

```
s = "52233"    ->  4   ("5223")
s = "5494"     ->  4
s = "1111111"  ->  2   ("11")
```

**Constraints:** `1 <= s.length <= 50`, `'0' <= s[i] <= '9'`.

## Approaches

| file | mechanism |
|---|---|
| `semi.kara` ★ | a sliding window over the bytes counts the adjacent equal pairs inside it; while a second pair is in, the left edge moves on, counting a pair out as it leaves. O(n) |
| `semi_last.kara` | only the latest pair is remembered, as an `Option[i64]`: when a new pair begins at i - 1, the window jumps to just past the previous pair's first digit, and the new pair becomes the latest. O(n) |
| `semi_extend.kara` | from each start the substring grows a digit at a time until a second pair would enter it; the longest growth wins. O(n^2) |
| `semi_pairs.kara` | the places of the pairs, found by `windows(2)` with `enumerate`, cut the string, with the two ends standing in as pairs before the first and after the last; the best substring runs from one cut to the next but one. O(n) |
| `semi_solution.kara` | a Rust solution as LeetCode's Rust users write it, `as_bytes()`, `usize` indices and a `while cnt > 1` left edge, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples; one digit;
50 ones, LeetCode's longest string; 50 digits with no pair; a pair at
each end only; a pair every third place; and 5000 random strings of 1 to
50 digits from the first 1 to 10, with the sum of their answers and a
checksum. `semi.py` mirrors the ★ arm and its output is byte-identical.

```
4
4
2
1
2
50
49
6
5000 strings: lengths sum to 63290, checksum 833786881
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every substring, each with its adjacent equal pairs counted,
and the longest with at most one. It draws 1000 random strings of 1 to
12 digits from the first 1 to 4, where pairs are dense, then 500 of 1 to
50 from the first 1 to 10, all before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the string reversed: the same answer |
| P3 | every digit moved 1 to 9 places on round the ten: the same answer |
| P4 | one digit more on the end: no smaller, and at most one more |
| P5 | the answer is between the shorter of the length and 2, and the length; and it is the length when the string holds one pair or none |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1500 cases: checksum 559139394, 45000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by brute force over every substring gives the
same checksum. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M1 and M5 fail the same checks, since both
allow no pair at all, as LeetCode's "1111111" answered 1 would. Two first
choices were replaced: the ★ arm never counting a leaving pair out, which
loops for ever once a second pair is in, and the solution's left edge
jumping two places, which runs off the end of the bytes and stops the
run rather than failing a property.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the window shrinks while one pair is inside | P1 1233, P5 519, P6 1233 |
| M2 | ★: a pair leaving counted out twice | P1 697, P2 426, P6 697 |
| M3 | last: the window starts at the previous pair's first digit | P1 793, P2 367, P6 793 |
| M4 | last: the latest pair never remembered | P1 712, P2 410, P6 712 |
| M5 | extend: growth stops at the first pair | P1 1233, P5 519, P6 1233 |
| M6 | extend: the start's own digit not counted | P1 1500, P5 786, P6 1500 |
| M7 | pairs: a pair's place is its second digit | P1 651, P2 436, P6 651 |
| M8 | pairs: the span between neighbouring pairs, not the next but one | P1 964, P4 96, P5 250, P6 964 |
| M9 | solution: the answer starts at 0 | P1 115, P4 115, P5 115, P6 115 |
| M10 | solution: a pair at the very start never counted | P1 515, P2 323, P6 515 |

## Benchmarks

The bench draws 200000 strings of 50 digits, LeetCode's longest, each
from the first 2 to 10 digits so that pairs range from dense to rare, all
of them first, then answers each 20 times by the ★ arm's sliding window
in all five languages. Every implementation prints `200000 strings of 50
digits, 20 rounds: lengths sum to 82259420, checksum 159499425`.

BENCHTAB

## Verification

All five arms print the same output as `semi.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The harness first passed the pairs-at-both-ends string as an f-string
inside the `println` f-string's braces; f-strings do not nest, so it is
bound to `ends` first.

LeetCode's Rust template took one `karac fix` of 7 edits, the wrapper
included: `struct Solution {}` added, `s.as_bytes()` became `s.bytes()`,
the `1usize` and `0usize` suffixes dropped, since an index is `i64`, and
in the wrapper `Solution::` became `Solution.`, with the `.clone()` and
the `as i64` dropped, since a parameter borrows and `i32` widens by
itself.
