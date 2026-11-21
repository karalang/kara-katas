# 2522. Partition String Into Substrings With Values at Most K

You are given a string `s` consisting of digits from `1` to `9` and an
integer `k`.

A partition of a string `s` is called **good** if:

- Each digit of `s` is part of **exactly** one substring.
- The value of each substring is less than or equal to `k`.

Return *the **minimum** number of substrings in a **good** partition of*
`s`. If no **good** partition of `s` exists, return `-1`.

**Note** that the **value** of a string is its result when interpreted
as an integer, and a **substring** is a contiguous sequence of
characters within a string.

```
s = "165462", k = 60  ->  4
s = "238182", k = 5   ->  -1
```

**Constraints:** `1 <= s.length <= 10^5`; `s[i]` is a digit from `'1'`
to `'9'`; `1 <= k <= 10^9`.

A partition exists exactly when every single digit is at most `k`.
Then taking the longest first part that fits never costs a part: any
good partition's first part is no longer, so the rest the greedy leaves
is a suffix of that partition's rest, and a suffix needs no more parts
than the string it ends, dropping a part's leading digits only lowering
its value. A part has at most
10 digits, `k` being at most `10^9`, so the values fit in an `i64`. The
approaches differ in how the parts are found and compared.

## Approaches

| file | mechanism |
|---|---|
| `greedy.kara` ★ | greedy: the current part's value grown by each digit while it stays at most `k`, a digit that would pass `k` starting the next part; -1 for a digit above `k`. O(n) |
| `greedy_dp.kara` | dynamic programming: the fewest parts for every prefix, from the best over every last part of at most 10 digits whose value is at most `k`. No greedy argument. O(10 n) |
| `greedy_text.kara` | the text: no part becomes a number; a part is compared with `k` written out, a shorter digit string being the smaller number and one of the same length comparing as text |
| `greedy_rec.kara` | recursion: a part's end found by a recursion that takes the next digit while the grown value stays at most `k`; the parts counted one after another. At most 11 deep |
| `greedy_iter.kara` | iterators: -1 when `any` digit is above `k`; otherwise a `fold` over the digits carrying the parts so far and the last part's value |
| `greedy_solution.kara` | LeetCode's Rust template: `String` and `i32` in, `i32` out; the digits of `s.chars()` read by `to_digit(10)`, greedy as the ★ arm; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's two examples and six
more; then 2000 random strings of 1 to 10 digits with `k` from 1 to 100
and 2000 of 1 to 60 digits with `k` from 1 to `10^9`, as the sum, how
many have no good partition, and a checksum; then the constraints'
largest, `10^5` digits: all 9 with `k` 9, and random with `k` 500,
`10^9` and 8. `greedy.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 3000 random strings of 1
to 12 digits with `k` to 100 or to `10^6` against the fewest parts over
every way to cut the string, and the two agreed on every string.

`check` reported one error and two warnings on the arms as first
written. The iter arm walked its mapped digits twice through `clone()`,
and an iterator that holds a closure is not `Clone`: the error says to
build it again or `collect` it once into a `Vec`, and the arm collects
it. The dp and rec arms cast `b - b'0'` to `i64` where the `u8` widens
implicitly, and `karac fix` dropped both casts.

`check` first reports 2 errors on the template: `struct Solution;` and
the path call `Solution::minimum_partition`. `karac fix` carries it in
one call, reporting 4 edits: `struct Solution {}`;
`Solution.minimum_partition`; the wrapper's `s.clone()` written `s`,
the parameter only borrowing it; and the wrapper's lossless `as i64`
dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to cut the string, one for each set of the gaps
between its digits, each part's value read and checked against `k`;
the fewest parts of a cut that passes, and -1 when none does. No greedy
and no table. It checks 300 random strings of 1 to 10 digits with `k`
from 1 to 100, 30 with `k` from 1 to `10^9`, and 30 with `k` from 1 to
9. Every case keeps the constraints, and so does every `k + 1` that P3
asks, no drawn `k` being `10^9`. All 360 are drawn before any arm
answers, and 37 of them have no good partition.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | -1 exactly when some digit is above `k`; otherwise from the digits over `k`'s length, rounded up, to the number of digits |
| P3 | `k` one more: not -1 and at most the answer, unless the answer is -1 |
| P4 | the string written twice: from the answer to twice it, unless -1 |
| P5 | `k` = `10^9`: the digits over 9, rounded up |
| P6 | each arm agrees with at least three of the other five |

P5 holds because every 9-digit string is below `10^9` and every
10-digit one of digits 1 to 9 is above it.

The differential prints `360 cases, 37 with -1: checksum 798696391,
12960 checks over 6 arms: 0 failures` under every lane in
Verification; the checksum of the literal answers was checked against a
Python reading that builds the same cases and tries every cut. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a value of k refused | P1 11, P2 2, P6 11 |
| M3 | ★: the parts counted from 0 | P1 323, P2 157, P4 240, P5 360, P6 323 |
| M5 | ★: the value grown by addition | P1 251, P2 222, P5 37, P6 251 |
| M8 | dp: a value of k refused | P1 14, P2 5, P6 14 |
| M10 | dp: the empty prefix needing a part | P1 323, P2 92, P5 360, P6 323 |
| M11 | dp: the last part only one digit | P1 231, P5 332, P6 231 |
| M12 | text: a part as long as k always fitting | P1 203, P2 37, P5 37, P6 203 |
| M14 | text: the first digit not tested | P1 5, P2 5, P4 5, P6 5 |
| M16 | text: parts compared as text alone | P1 292, P2 291, P3 10, P5 359, P6 292 |
| M17 | rec: the end counted as a refusal | P1 323, P2 323, P5 360, P6 323 |
| M19 | rec: the digit not added | P1 293, P2 280, P5 37, P6 293 |
| M20 | rec: the end one digit on | P1 278, P2 165, P5 37, P6 278 |
| M23 | iter: the new part begun empty | P1 193, P2 62, P6 193 |
| M25 | iter: all digits above k needed for -1 | P1 29, P2 29, P6 29 |
| M26 | iter: the value not carried | P1 135, P2 86, P5 37, P6 135 |
| M30 | solution: no -1 for a digit above k | P1 5, P2 5, P6 5 |
| M31 | solution: k cut by 10 | P1 293, P2 224, P5 39, P6 293 |

P1 and P6 kill all seventeen, P2 sixteen, P5 eleven, P4 two, and P3
one.

Two of the first thirty-one edits were replaced. The dp arm's parts of
at most 9 digits survived: a part of 10 digits from 1 to 9 is at least
1111111111, past any `k` the constraints allow, so the edit is
equivalent. And no edit of the first run broke P3: every one kept the
answer from growing when `k` grows. The text arm's part tested before it
grows, which failed exactly as its next part begun a digit late (M15),
gave way to the text arm's parts compared as text alone (M16), which
reads `"9"` as above `"10"`, so a larger `k` can refuse a digit that a
smaller one took; P3 kills it. The dp arm's survivor became the last
part not counted (M7).

Fourteen are not kept, and none survives. Twelve fail exactly as a kept
one. The ★ arm's and the template's new part begun empty (M2, M28) fail
as the iter arm's (M23); the ★ arm's digit equal to `k` refused (M6) as
the template's no -1 for a digit above `k` (M30); the dp arm's last
part not counted (M7) as the rec arm's end counted as a refusal (M17);
the dp arm's place not raised (M9) as the ★ arm's value grown by
addition (M5); the text and rec arms' value of `k` refused (M13, M18)
as the dp arm's (M8); the rec arm's parts counted from 1 (M21) as the
dp arm's empty prefix needing a part (M10); the iter arm's value of `k`
starting a part and the template's value of `k` refused (M22, M27) as
the ★ arm's (M1); and the iter arm's fold begun at 0 parts and the
template's count from 0 (M24, M29) as the ★ arm's parts counted from 0
(M3). The ★ arm's no -1 for a digit above `k` (M4) and the text arm's
next part begun a digit late (M15) fail in ways of their own, but their
arms already hold their kept edits.

## Verification

Every arm prints the same output as `greedy.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.5 to 2.8 s and the differential 0.7 s; under `karac __mir-llvm-asan` the arms take 0.4 to 0.8 s and the differential 0.5 s; and under `karac run` the differential takes 0.5 s.

## Benchmarks

The bench builds 20 random strings of `10^5` digits from 1 to 9 once
from its own generator, then makes 50 passes. Each pass asks every
string with `k` from 9 to `10^9`, `check % 999999992 + 9`, folding each
answer plus the pass into the checksum. The bench uses the ★ arm in all
five languages. Every implementation prints `50 passes over 20 strings
of 10^5 digits: checksum 788179912`.

BENCHTAB
