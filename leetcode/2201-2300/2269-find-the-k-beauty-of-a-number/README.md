# 2269. Find the K-Beauty of a Number

The **k-beauty** of an integer `num` is defined as the number of
**substrings** of `num` when it is read as a string that meet the
following conditions:

- It has a length of `k`.
- It is a divisor of `num`.

Given integers `num` and `k`, return *the k-beauty of* `num`.

Note:

- **Leading zeros** are allowed.
- `0` is not a divisor of any value.

A **substring** is a contiguous sequence of characters in a string.

```
num = 240, k = 2     ->  2
num = 430043, k = 2  ->  2
```

**Constraints:** `1 <= num <= 10^9`; `1 <= k <= num.length` (taking
`num` as a string).

There are at most ten digits, so every window of `k` of them can be
read back as a number and tested. O(d k) for d digits, or O(d) when the
window's value rolls along.

## Approaches

| file | mechanism |
|---|---|
| `beauty.kara` ★ | `num.to_string()`, every `s[i..i + k]` parsed by `i64.parse`, counted when it is not 0 and divides `num` |
| `beauty_arith.kara` | no string: the window `i` digits from the right is `num / 10^i % 10^k`, while the number still reaches its top digit |
| `beauty_rolling.kara` | the digits from the left over `chars()`, the window's value `(value * 10 + digit) % 10^k` dropping the digit that falls out |
| `beauty_struct.kara` | `struct Window` of the value, the digits seen, `k` and `10^k`; `push` (`mut ref self`) takes a digit and `full` says it is `k` wide |
| `beauty_iter.kara` | one chain: `bytes().windows(k)`, each folded to its number, `filter`, `count` |
| `beauty_solution.kara` | LeetCode's Rust template: `i32`s in, `i32` out; `k as usize`, `s[i..i + k].parse()` into `t: i32`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples and five
more (one digit, 1; the whole number as its only window, 1; a zero
window beside `10`, 1; nine ones by threes, 7; 10^9 by ones, 1), each
with its beauty; then 3000 numbers of 1 to 9 digits, each with a
random `k`, with the total beauty (2025) and a checksum; then every
`k` for three numbers at the constraints' reach: 10^9, 999999999 and
735134400. `beauty.py` mirrors the ★ arm and its output is
byte-identical.

The iter arm was written `.windows(k).map(..)` and the struct arm
`window.push((b - b'0') as i64)`. `karac check` asks for `.into_iter()`
after `windows(k)`, which returns a `Vec`, and calls the `as i64`
unnecessary, a `u8` widening implicitly; `karac fix` applies both. The
struct arm's fix left `window.push((b - b'0'))`, and the arm drops the
parentheses.

`karac fix` carries the template in one round, reporting 6 edits:
`k as usize` to `k as i64`, `s[i..i + k].parse()` into the annotated
`t: i32` to `i32.parse(s[i..i + k])`, `&&` to `and`, `struct
Solution;` to `struct Solution {}`, `Solution::` to `Solution.`, and the
adapter's `as i64` dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the number's digits taken off by `% 10`, every substring by
its start and end, kept when it is `k` long, its value built digit by
digit, and counted when it is not 0 and divides the number. No string
of the number and no window. It checks 300 random numbers of 1 to 8
digits, each with a random `k`; then 30 of one digit repeated; then 30
of one digit followed by zeros. All 360 are drawn before any arm
answers. The numbers stop at 8 digits so that P4's `num * 10` stays
within the template's `i32`.

| | property |
|---|---|
| P1 | the beauty is the literal reading's |
| P2 | `k` the number of digits: exactly 1 |
| P3 | at least 0 and at most the number of windows, `digits - k + 1` |
| P4 | a 0 put after the number: at least the same beauty |
| P5 | `k` 1: the nonzero digits that divide the number, counted digit by digit |
| P6 | each arm agrees with at least three of the other five |

P2 holds because the only window is the number, which divides itself.
P4 holds because `num * 10` keeps every window of `num` and every
divisor of `num` divides it.

The differential prints `360 cases: checksum 883733750, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
counts the `int(s[i:i + k])` that divide the number. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the number dividing the window | P1 97, P4 133, P5 253, P6 97 |
| M3 | ★: a window dividing the next number | P1 219, P2 354, P4 28, P5 275, P6 219 |
| M6 | ★: the whole number left out | P1 133, P2 360, P5 54, P6 133 |
| M7 | arith: the window with a leading 1 and zeros left out | P1 19, P2 12, P5 39, P6 19 |
| M8 | arith: every other window | P1 56, P4 161, P5 151, P6 56 |
| M10 | arith: the lowest window skipped | P1 186, P2 360, P5 198, P6 186 |
| M12 | rolling: the first window missed | P1 194, P2 360, P5 186, P6 194 |
| M13 | rolling: the old digits never dropped | P1 195, P5 210, P6 195 |
| M14 | rolling: the digits added | P1 165, P2 236, P5 220, P6 165 |
| M18 | struct: a window one digit long | P1 131, P5 209, P6 131 |
| M20 | struct: the window full one digit early | P1 51, P2 63, P3 25, P6 51 |
| M21 | struct: the digits read from the right | P1 70, P2 236, P6 70 |
| M22 | iter: windows one longer | P1 248, P2 360, P5 260, P6 248 |
| M23 | iter: every nonzero window | P1 186, P5 233, P6 186 |
| M24 | iter: the digits summed | P1 88, P2 236, P6 88 |
| M29 | solution: each counted twice | P1 230, P2 360, P3 159, P5 307, P6 230 |
| M30 | solution: every suffix | P1 173, P5 191, P6 173 |

P1 and P6 kill all seventeen, P5 fourteen, P2 eleven, P4 three, and P3
two. P5 is the strongest after P1: at `k` 1 every window is one digit,
so any edit to how a window is cut, rolled or tested shows. P2 catches
every edit that loses the whole number as its own window, by skipping
an end, cutting too long, or changing the value. P4 catches the edits
whose test is not a divisor of `num`: the number dividing the window,
the next number, every other window lost when a 0 shifts them. P3
catches only counts out of range: a window full a digit early, and
each counted twice. The digits read from the right are wrong only for
a number that is not a palindrome, and the digits summed only where
the sum differs from the window as a number.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Eight fail as a kept one does: the ★ arm's and
the template's last window missed (M1, M27) as the arith arm's lowest
window skipped (M10); the ★ arm's first window skipped, the rolling
arm's first digit dropped, the struct arm's full only past `k` and the
iter arm's first window skipped (M4, M16, M17, M26) as the rolling arm's
first window missed (M12); the arith arm's window one digit long (M11)
as the iter arm's windows one longer (M22); and the template's whole
number left out (M28) as the ★ arm's (M6). Six fail in ways of their
own and are left out because their arms keep enough: the ★ arm's
beauty from 1 and the template's answer from 1 (M5, M31) alike; the
arith arm's window one digit short and the rolling arm's width one
digit short (M9, M15) alike; the struct arm's digits never counted
(M19); and the iter arm's windows that do not divide (M25).

## Verification

Every arm prints the same output as `beauty.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, arith and struct arms take 0.2 s, the
rolling arm and the template 0.2 s, the iter arm 0.3 s, and the
differential 0.4 s.

## Benchmarks

The bench answers 200000 random numbers below 10^9, `k` from 1 to 9 in
turn and cut to the number's length, with the ★ arm in all five
languages. Every implementation prints `200000 numbers: checksum
210683679`. Each formats the number and parses every window: Rust by
`to_string` and `parse`, Go by `strconv`, Python by `str` and `int`,
and C by `snprintf` and `strtoll` on a copied window.

BENCHTAB
