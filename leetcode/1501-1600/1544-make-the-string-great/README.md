# 1544. Make The String Great

Given a string `s` of lower and upper case English letters, a good string
has no two adjacent characters `s[i]` and `s[i + 1]` where one is a letter
in lower case and the other the same letter in upper case. To make the
string good, repeatedly remove two such adjacent characters. Return the
string once it is good; the answer is unique, and may be empty.

```
s = "leEeetcode"  ->  "leetcode"
s = "abBAcC"      ->  ""        (bB, then aA and cC)
s = "s"           ->  "s"
```

**Constraints:** `1 <= s.length <= 100`; `s` contains only lower and upper
case English letters.

## Approaches

| file | mechanism |
|---|---|
| `great.kara` ★ | a `Vec[char]` stack: each letter either cancels the letter on top (a `match` on `stack.last()` with a guard, the two equal under `to_ascii_lowercase` but not equal) or is pushed. A removal can only bring two letters together at the top, so what is left has no bad pair. O(n) |
| `great_inplace.kara` | the stack kept in the string's own bytes: `kept` bytes at the front form it, each byte either cancels the last kept one (they differ by 32, the gap between the cases in ASCII) or is written after it; then `truncate` and `String.from_utf8`. O(n), no second buffer |
| `great_passes.kara` | the statement repeated in passes: each pass walks left to right dropping every bad pair it meets, until a pass drops nothing. O(n²) at worst |
| `great_fold.kara` | the ★ arm's stack as a `String` carried through a `fold`, the top read with `chars().last()` and compared with `eq_ignore_ascii_case` |
| `great_solution.kara` | LeetCode's Rust template (`make_good(s: String) -> String`, a `Vec<u8>` stack with `if let Some(&top) = stack.last()` and `u8::eq_ignore_ascii_case`), carried by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's three examples, then `aA`,
`Aa`, `aa`, `abBA`, `aBbAcCdD`, `AbBa`, `xyzZYX` and `abcCBAd`; then the
count of empty answers and a checksum of every answer for 3000 random
strings of up to 12 letters over the first 1 to 3, 300 of up to 100 over
the first 1 or 2 and 300 of up to 100 over the first 1 to 26, both cases.
`great.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a bad pair, here the last one found, removed until none is
left. It checks 3000 strings of 1 to 14 letters, each over its own run of
1 to 3 letters starting anywhere in the alphabet (z wraps to a), both
cases, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer has no bad pair, and is shorter than the string by an even count |
| P3 | every case swapped swaps every case of the answer |
| P4 | the string followed by itself backwards with every case swapped leaves nothing |
| P5 | the answer is left as it is, and every letter moved on by one (z to a) moves the answer's letters on by one |
| P6 | each arm agrees with at least two of the other four |

The differential prints `3000 problems: checksum 506639540, 90000 checks
over 5 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M9 was first written as
`top.to_ascii_lowercase() == b` on the template's bytes, which the
checker refused: `u8` had no `to_ascii_lowercase` (B-2026-11-14-9, see
Writing it). It was rewritten as below.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: two equal letters also cancel | P1 1887, P6 1887 |
| M2 | ★: the letter that cancels the top is pushed as well | P1 1904, P2 1692, P4 3000, P5 957, P6 1904 |
| M3 | inplace: bytes 31 apart cancel | P1 2362, P2 2062, P3 1319, P4 3000, P5 73, P6 2362 |
| M4 | inplace: at least one byte always kept | P1 193, P2 193, P4 3000, P6 193 |
| M5 | passes: one pass only | P1 601, P2 601, P4 2576, P5 601, P6 601 |
| M6 | passes: a bad pair steps past one letter, dropping only the first | P1 1797, P2 1133, P4 3000, P6 1797 |
| M7 | fold: the top read from the front of the string | P1 1233, P2 727, P4 1693, P6 1233 |
| M8 | fold: two equal letters also cancel | P1 1887, P6 1887 |
| M9 | template: the byte compared with the next byte up | P1 2498, P2 1849, P4 3000, P5 136, P6 2498 |
| M10 | template: the cancelling byte pushed as well | P1 1904, P2 1692, P4 3000, P5 957, P6 1904 |

## Benchmarks

The bench builds 1000 strings of 1 to 100 letters (the constraint's
bound) once, each over its own first 1 to 3 letters in both cases, and
makes each great 500 times by the ★ arm, in all five languages. Every
call builds its own stack and result, as the Kāra arm does; C's stack is
a fresh heap buffer per call. Every implementation prints `500 passes
over 1000 strings of up to 100 letters: 11095500 letters kept, checksum
798320444`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.121 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.203 s |
| Kāra (`karac build`) | 0.203 s |
| Rust (`rustc -O`) | 0.218 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.218 s |
| Go | 0.290 s |
| Python | 2.3 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time equals its real time (0.19 s and 0.19 s on one run).

Kāra is 0.93x Rust under overflow checks by median. Not traced. Each call
allocates a stack and a result string for at most 100 letters, so the
allocator is a large share of every row; C's single buffer per call is
why it leads.

## Verification

All five arms print the same output as `great.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The ★, inplace and passes arms were written in Kāra and checked as
written. The fold arm compared the top with `top.eq_ignore_ascii_case(c)`,
as Rust's `char` does, and the checker answered `no method
'eq_ignore_ascii_case' on type 'char'`. That was a gap, filed and fixed
as B-2026-11-14-9: `eq_ignore_ascii_case` now exists on `char` and `u8`,
and `to_ascii_lowercase` / `to_ascii_uppercase` on `u8` (the gap M9 met),
on every backend. The arm is as first written. The shared harness took
one edit from `karac fix`: `mix(check, b as i64)` to `mix(check, b)`, a
`u8` widening on its own.

The Rust template took 5 changed lines and 1 over two rounds:
`Vec<u8>` to `Vec[u8]` with `Vec::new()` to `Vec.new()`,
`if let Some(&top) = stack.last()` to
`if let Some(top) = stack.last().cloned()`, `&&` to `and` with
`eq_ignore_ascii_case(&b)` to `eq_ignore_ascii_case(b)`,
`String::from_utf8` to `String.from_utf8`, and `Solution::` to
`Solution.`; then `struct Solution {}` added. It checks and agrees with no
hand edit.
