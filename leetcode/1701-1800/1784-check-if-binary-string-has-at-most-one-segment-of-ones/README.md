# 1784. Check if Binary String Has at Most One Segment of Ones

Given a binary string `s` without leading zeros, return `true` if `s`
contains at most one contiguous segment of ones. Otherwise, return
`false`.

```
s = "1001"  ->  false
s = "110"   ->  true
```

**Constraints:** `1 <= s.length <= 100`, `s[i]` is either `'0'` or
`'1'`, and `s[0]` is `'1'`.

The arms are `fn check_ones_segment(s: String) -> bool`.

## Approaches

| file | mechanism |
|---|---|
| `check_ones_segment.kara` ★ | the string starts with a 1, so a second segment of ones can only begin right after a 0, and `"01"` appears exactly when there is one: `not s.contains("01")`. O(n) |
| `check_ones_segment_scan.kara` | a scan over the characters counting the segments, each 1 that comes first or after a 0 starting one. O(n) |
| `check_ones_segment_split.kara` | the string split on `"0"`, and the pieces that are not empty, which are the segments, counted. O(n) |
| `check_ones_segment_trim.kara` | the leading ones stripped with `strip_prefix` in a loop, and one segment exactly when no 1 is left. O(n) |
| `check_ones_segment_solution.kara` | a Rust solution as LeetCode's Rust users write it (`s.as_bytes()`, `for &c in b`, `b'0'`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`false
true`); five edges, one digit, a 1 then a 0, two segments of one, all
ones, and two segments far apart (`true true false true false`); the
constraints' most, 100 ones, 50 ones then 50 zeros, and a 1 at each end
of 98 zeros (`the most: true true false`); and 3000 random strings of 1
to 20 digits, each digit after the first a 0 with a chance of 0 to 3 in
4 (`3000 random cases: checksum 548996069`). `check_ones_segment.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`.

The Mend loop: the ★, scan and split arms check clean as first written.
The trim arm was first written with Rust's `s.trim_start_matches("1")`;
check said Kāra strips a prefix with `strip_prefix(p)`, which removes
one occurrence and returns an `Option[Str]`, to be repeated in a loop to
strip every one, and has no machine fix for that, so the loop was
written by hand as it says: `while let Some(after) =
rest.strip_prefix("1") { rest = after; }`. The Rust solution takes one
round of 4 fixes by `karac fix`'s count, and its diff is: `struct
Solution;` to `struct Solution {}`, `s.as_bytes()` to `s.bytes()`, `for
&c in b` to `for c in b`, and `Solution::` to `Solution.`. Its `b'0'`
stays. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every run of digits from `i` to `j` that is all ones and
cannot grow at either end is a segment, and at most one is allowed.
LeetCode's examples, the edges, the constraints' most, and 1990 random
strings of 1 to 14 digits. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | a 0 at the end never changes the answer |
| P3 | a 1 at the end leaves one segment exactly when every digit is a 1 |
| P4 | one segment exactly when the digits are already in descending order |
| P5 | the string twice over has one segment exactly when every digit is a 1 |
| P6 | the ★ arm's answer |

The differential checks clean as first written. All 60,000 checks pass
on every arm: `2000 cases: checksum 792646340, 60000 checks over 5 arms:
0 failures`, under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. Python, counting the runs of ones, gives the
same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a 1 followed by a 0 taken as a second segment | P1 249, P2 754, P4 249, P6 996 |
| M2 | ★: two zeros in a row taken as a second segment | P1 512, P2 185, P3 459, P4 512, P5 459, P6 2048 |
| M3 | scan: the first segment never counted | P1 482, P3 509, P4 482, P5 249, P6 482 |
| M4 | scan: no segment at all required | P1 1003, P3 754, P4 1003, P5 754, P6 1003 |
| M5 | split: a segment of a single 1 not counted | P1 639, P3 774, P4 639, P5 407, P6 639 |
| M6 | split: the string split only at two zeros in a row | P1 467, P2 214, P3 459, P4 467, P5 459, P6 467 |
| M7 | trim: a 0 left after the leading ones taken as a second segment | P1 249, P2 754, P4 249, P6 249 |
| M8 | trim: only the first leading 1 trimmed | P1 733, P3 754, P4 733, P5 754, P6 733 |
| M9 | solution: a 0 never remembered | P1 997, P3 1246, P4 997, P5 1246, P6 997 |
| M10 | solution: a 1 before any 0 taken as a second segment | P1 1003, P3 754, P4 1003, P5 754, P6 1003 |

## Benchmarks

The bench builds 4000 strings of 100 digits once, each some ones then
zeros, and half of them with one more 1 among the zeros, and makes
4000000 calls of the ★ arm, each string drawn from the checksum so far.
The bench was first written with `s.slice(0, at)`, which check marks
deprecated, and `karac fix` wrote the view `s[0..at]`, 2 fixes. Every
implementation prints `4000000 calls over 4000 strings: checksum
320357194`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.16 s against Rust's 0.12 s (0.12 s with overflow checks
on), C's 0.11 s and Go's 0.30 s; Python takes 1.2 s.
