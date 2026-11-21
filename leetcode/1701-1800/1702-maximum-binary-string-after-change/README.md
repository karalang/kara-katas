# 1702. Maximum Binary String After Change

You are given a binary string `binary` consisting of only `0`'s or
`1`'s. You can apply each of the following operations any number of
times:

- Operation 1: If the number contains the substring `"00"`, you can
  replace it with `"10"`. For example, `"00010" -> "10010"`.
- Operation 2: If the number contains the substring `"10"`, you can
  replace it with `"01"`. For example, `"00010" -> "00001"`.

Return *the **maximum binary string** you can obtain after any number of
operations. Binary string `x` is greater than binary string `y` if `x`'s
decimal representation is greater than `y`'s decimal representation.*

```
binary = "000110"  ->  "111011"
binary = "01"      ->  "01"
```

**Constraints:** `1 <= binary.length <= 10^5`; `binary` consist of `'0'`
and `'1'`.

## Approaches

| file | mechanism |
|---|---|
| `binary.kara` ★ | the 1s before the first 0 stay; from there `"10" -> "01"` brings every later 0 back next to the first, and `"00" -> "10"` turns a run of k zeros into k - 1 ones and a 0. So with the first 0 at f and z zeros in all, the answer is all 1s but a 0 at f + z - 1, built a digit at a time. O(n) |
| `binary_greedy.kara` | the moves made one at a time, from the left: at the first 0 still at i, the next 0 after it, at j, is walked back to i + 1 and `"00" -> "10"` makes i a 1; the digits are a `Vec[u8]`, j only moves right, and `String.from_utf8` gives the answer back. O(n) |
| `binary_iter.kara` | the ★ arm's count said with iterators: `let Some(first) = ...position(..) else { return binary; }`, the zeros by `filter(..).count()`, and the digits by a `map` over the indexes, collected. O(n) |
| `binary_solution.kara` | a Rust solution as LeetCode's Rust users write it, `into_bytes()`, `position(\|&c\| c == b'0')`, every byte set by `iter_mut` and `String::from_utf8(s).unwrap()`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's two examples, a lone 1,
four zeros, and no zero at all; then the zeros left and a checksum of
every answer's digits for 3000 random strings of up to 12 digits, 300 of
up to 1000 and 10 of up to `10^5`, each digit a 1 with a chance of its
string's own, 0 to 10 in 10. `binary.py` mirrors the ★ arm and its
output is byte-identical.

```
111011
01
1
1110
1111
3000 strings of up to 12 digits: 2354 zeros left, checksum 154187210
300 strings of up to 1000 digits: 274 zeros left, checksum 704110348
10 strings of up to 100000 digits: 8 zeros left, checksum 353365975
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every string the two operations can reach, anywhere and any
number of times, found by a search from the given one into a
`SortedSet[String]`; the largest of them wins, compared as strings since
all are the same length. It checks 3000 random strings of 1 to 10 digits
drawn as the arms' batches are. Every case is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is as long, has one 0 if the string has any and none if not, and keeps at least the string's leading 1s |
| P3 | a 1 put in front gives a 1 and then the same answer |
| P4 | a 0 put at the end gives a 1 and then the same answer, or the string and the 0 if it had no 0 |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 500668297, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, the same search over Python strings, gives the
same checksum. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Three first drafts were replaced: the
★ arm returning the string as it is when it has one 0, not none, is
right (one 0 cannot move), and so is the greedy arm's j started afresh
at i + 1 each time, only slower; the iter arm's `rposition` is no method
of `chars()`, and the solution arm's zeros counted past the first ran
off the front of the string. M2 and M7 both put the 0 one place early
and fail the same checks, as do M4 and M9, which both leave a second 0.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last 0 taken as the first | P1 1756, P2 1497, P4 841, P5 1756 |
| M2 | ★: the 0 left one place early | P1 2338, P2 582, P3 267, P4 929, P5 2338 |
| M3 | ★: a string that starts with 0 returned as it is | P1 1261, P2 1261, P3 1261, P4 1528, P5 1261 |
| M4 | greedy: the 0 walked back left where it was | P1 875, P4 809, P5 875 |
| M5 | greedy: the new 0 put at j - 1, not i + 1 | P1 1572, P2 1027, P4 1941, P5 1572 |
| M6 | greedy: a leading 1 treated as a 0 | P1 405, P2 255, P3 810, P4 506, P5 405 |
| M7 | iter: the zeros counted after the first | P1 2338, P2 582, P3 267, P4 929, P5 2338 |
| M8 | iter: the first 1 taken for the first 0 | P1 2178, P2 1280, P3 2338, P4 1390, P5 2178 |
| M9 | solution: only the first run of zeros counted | P1 875, P4 1362, P5 875 |
| M10 | solution: the 0 put at the length less the zeros | P1 1870, P4 2338, P5 1870 |

## Benchmarks

The bench draws 50 random strings of `10^5` digits, LeetCode's longest,
each digit a 1 with a chance of its string's own, all of them first,
then answers each 40 times by the ★ arm in all five languages; the sink
folds the place of each answer's 0 and one digit at a place the checksum
so far picks. The bench's arm borrows its string and hands back a clone
when it has no 0, as the C mirror copies it and Go's `strings.Clone`
does. Every implementation prints `50 strings of 100000 digits, 40
rounds: 199998200 ones, checksum 248590720`. The C build also runs clean
under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.180 s |
| Rust (`rustc -O`) | 0.248 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.594 s |
| Kāra (`karac build`) | 0.601 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.610 s |
| Go | 0.708 s |
| Python | 15 s |

The sequential Kāra build takes 2.46x Rust's time and 1.03x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.180 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.607 s and 0.613 s on one
run).

## Verification

All four arms print the same output as `binary.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The greedy arm checked clean as first written. The ★ and iter arms each
returned their borrowed parameter when it has no 0 (E0200, a parameter
cannot be given away); `karac fix` took it `own String`, and in each
harness dropped the five examples' `.to_string()`, since a literal is
an owned `String` already. The greedy arm's harness was then written the
same way by hand, so the harness is one text in all four.

LeetCode's Rust template took one `karac fix` of 10 edits:
`struct Solution {}` added, the closures' `|&c|` and `|&&c|` written
`|c|`, `String::from_utf8` written `String.from_utf8`, and
`binary.into_bytes()` written `binary.bytes().to_vec()`: the parameter
only borrows, so its bytes are copied rather than taken, and the
signature stays LeetCode's. The other five were the harness's
`.to_string()`s, as in the ★ arm.

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
