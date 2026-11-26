# 1461. Check If a String Contains All Binary Codes of Size K

Given a binary string `s` and an integer `k`, return `true` if every
binary code of length `k` is a substring of `s`. Otherwise, return
`false`.

```
s = "00110110", k = 2  ->  true
s = "0110", k = 1      ->  true
s = "0110", k = 2      ->  false
```

**Constraints:** `1 <= s.length <= 5 * 10^5`, `s[i]` is either `'0'` or
`'1'`, and `1 <= k <= 20`.

The arms are `fn has_all_codes(s: Str, k: i64) -> bool`.

## Approaches

| file | mechanism |
|---|---|
| `has_all_codes.kara` ★ | the last k digits kept as a number, each new digit shifted in from `s.bytes().iter().enumerate()` and the rest masked off, each window marked once in a `Vec[bool]` of 2^k and counted, returning as soon as all 2^k are found. O(n + 2^k) |
| `has_all_codes_set.kara` | every window of k digits put in a `Set[Str]` as the slice `s[i..i + k]` over `0..=s.len() - k`, and all the codes there when the set holds `1 << k`. O(nk) |
| `has_all_codes_windows.kara` | too few windows for 2^k codes answered first, then the digits collected as `i64`s and each of `windows(k)` folded to its number by `fold(0, \|code, d\| code * 2 + d)`, collected into a `Set[i64]`. O(nk) |
| `has_all_codes_counts.kara` | how many times each code has been seen in a `Vec[i32]` of 2^k, the window read by `c.to_digit(2)` over `chars()`, and how many codes are still missing counted down as each turns up for the first time. O(n + 2^k) |
| `has_all_codes_solution.kara` | a Rust solution as LeetCode's Rust users write it (every window `&s[i..i + k]` put in a `HashSet<&str>` and the set's size compared with `1 << k`, `k` taken as an `i32` and cast to `usize`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and four
more, k of 1 on "0" and on "01", and the de Bruijn sequence of order 20,
every code of 20 digits once in 1,048,595 digits, whole and with its
last digit cut off (`true true false false true true false 1048595`);
the constraints' most, 5 * 10^5 random digits half of them ones, for k
from 1 to 20 (`5 * 10^5 digits: every code up to k = 15`); and 3000
random strings of 1 to 400 digits, k from 1 to 8, the ones from 1 to 7
in 8 (`3000 random strings: 1227 with every code, checksum 961734421`).
`has_all_codes.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run`,
`karac build` and `karac __mir-llvm-run`.

The Mend loop: the set arm checks clean as first written. The ★ arm
walked `s.bytes().enumerate()`, which `karac check` refuses, `bytes()`
being a `Slice` whose iterator adaptors need an explicit `.iter()`, and
`karac fix` writes `s.bytes().iter().enumerate()`, and it drops the `as
i64` on `(b - b'0')`, which widens without one, 2 fixes. The windows arm
mapped `digits.windows(k)` directly, which `karac fix` writes
`windows(k).into_iter().map(..)`, 1 fix; the counts arm's `as i64` on
`to_digit(2).unwrap()` is dropped the same way, 1 fix. The Rust solution
takes one round of 6 fixes by `karac fix`'s count: the `use` line
deleted, `struct Solution;` to `struct Solution {}`, `k as usize` to `k
as i64`, `HashSet::new()` to `Set.new()`, and the `&` on the slice
dropped. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every code of k digits written out, 0 to 2^k - 1 in binary
with its leading zeros, and each looked for in `s` by `contains`, while
k is at most 8 and there are at most 400 digits. LeetCode's examples,
five edge cases (one digit of each value, "01" with k of 3, longer than
the string, and ten zeros), the de Bruijn sequences of order 10 and 20
whole and with their first digit cut off, the constraints' most at k of
20 and of 15, and 1983 random strings drawn as the harness draws them.

| | property |
|---|---|
| P1 | the statement read literally, while k is at most 8 and there are at most 400 digits |
| P2 | the digits reversed give the same answer |
| P3 | every digit flipped gives the same answer |
| P4 | a digit more at each end keeps a true answer |
| P5 | true for k + 1 means true for k, and fewer than 2^k windows means false |
| P6 | the ★ arm's answer |

All 59,880 checks pass on every arm: `1997 cases: checksum 45031832,
59880 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, putting every
window's substring in a set, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the first full window never marked | P1 3, P2 4, P6 20 |
| M2 | ★: true one code short of all of them | P1 134, P5 5, P6 544 |
| M3 | set: the last window never read | P1 3, P2 4, P6 5 |
| M4 | set: half the codes taken as enough | P1 666, P5 33, P6 668 |
| M5 | windows: exactly 2^k windows taken as too few | P1 1, P6 3 |
| M6 | windows: each window read as its count of ones | P1 585, P6 588 |
| M7 | counts: the first full window never counted | P1 3, P2 4, P6 5 |
| M8 | counts: the window's highest digit dropped | P1 829, P6 832 |
| M9 | solution: a string shorter than k taken as holding every code | P1 26, P4 16, P5 34, P6 26 |
| M10 | solution: each window taken one digit short | P1 829, P6 832 |

## Benchmarks

The bench draws 20 strings of 5 * 10^5 random digits, the constraints'
most, once; each is asked for k from 11 to 20 with the ★ arm after one
digit is flipped at a place chosen from the checksum so far, so no
answer carries over, and the answer is folded into the checksum. Each
implementation keeps the digits as bytes, copies them into a fresh
string for every call (`String.from_utf8` in Kāra and Rust, `memcpy` in
C, `string(..)` in Go and `decode()` in Python) and walks the string's
bytes. Every implementation prints `20 strings of 5 * 10^5 digits, k
from 11 to 20: checksum 500286988`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.22 s against Rust's 0.17 s (0.18 s with overflow checks
on), C's 0.17 s and Go's 0.31 s; Python takes 16.8 s.
