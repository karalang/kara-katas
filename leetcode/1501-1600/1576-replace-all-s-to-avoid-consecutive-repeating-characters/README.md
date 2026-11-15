# 1576. Replace All ?'s to Avoid Consecutive Repeating Characters

Given a string `s` containing only lowercase English letters and the
`'?'` character, convert all the `'?'` characters into lowercase letters
such that the final string does not contain any consecutive repeating
characters. You cannot modify the non-`'?'` characters. It is
guaranteed that there are no consecutive repeating characters in the
given string except for `'?'`. Return the final string after all the
conversions (possibly zero) have been made. If there is more than one
solution, return any of them.

```
s = "?zs"       ->  "azs"
s = "ubv?w"     ->  "ubvaw"
```

**Constraints:** `1 <= s.length <= 100`; `s` consists of lowercase
English letters and `'?'`.

## Approaches

The statement accepts any valid answer, so every arm settles the same
one, the first valid string in dictionary order: each `'?'`, left to
right, gets the first letter that differs from both neighbours. Three
letters always leave one, and that choice never blocks a later `'?'`.

| file | mechanism |
|---|---|
| `replace.kara` ★ | the chars in a `Vec[char]`, each `'?'` made the first of `['a', 'b', 'c']` that is neither the char before it (already settled) nor the char after it, then collected back into a `String`. O(n) |
| `replace_peek.kara` | one pass that builds the answer over `s.chars().peekable()`: each `'?'` pushed as the first letter that is neither the last char pushed nor `peek()`'s. O(n) |
| `replace_bytes.kara` | over the bytes (`s.bytes().to_vec()`): each `b'?'` overwritten in place with the first byte from `b'a'` up that matches neither neighbour, then `String.from_utf8(b).unwrap()`. O(n) |
| `replace_solution.kara` | LeetCode's Rust template (`modify_string(s: String) -> String` over `s.into_bytes()` and `b'a'..=b'c'`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's two examples, then
`j?qg??b`, `??yw?ipkj?`, `?`, `??`, `a?a`, `a?b`, seven `'?'`s and
`ab?ba`; then the number of `'?'`s and a checksum over every answer's
chars for 3000 random strings of up to 8 characters over 3 letters, 300
of up to 1000 over all 26, and 30 of up to 100 over 2. `replace.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every filling of the `'?'`s from `'a'`, `'b'` and `'c'` tried
in dictionary order, and the first with no two equal neighbours kept.
No filling that uses a later letter can come first, so this is the first
valid filling over the whole alphabet. It checks 3000 strings of 1 to 7
characters, each a `'?'` or a letter from `'a'` to `'d'` that differs
from the letter before it, every random choice drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | no two neighbours of the answer are equal |
| P3 | every char that was not a `'?'` is unchanged, and so is the length |
| P4 | the answer given back as the input comes back unchanged |
| P5 | every `'?'` became one of `'a'`, `'b'`, `'c'` |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 251320275, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the char after a `'?'` not looked at | P1 363, P2 363, P6 363 |
| M2 | ★: `'b'` tried before `'a'` | P1 1988, P6 1988 |
| M3 | ★: the search goes on after a letter fits, so the last that fits wins | P1 2511, P6 2511 |
| M4 | peek: `'a'` chosen without looking at the char before | P1 1679, P2 1679, P6 1679 |
| M5 | peek: the char before remembered as the `'?'` it was | P1 1457, P2 1457, P6 1457 |
| M6 | peek: the end of the string read as an `'a'` | P1 1102, P6 1102 |
| M7 | bytes: the char after not looked at when it is the last | P1 120, P2 120, P6 120 |
| M8 | bytes: the letters tried two at a time | P1 1784, P5 187, P6 1784 |
| M9 | template: the test of the char after always passes | P1 363, P2 363, P6 363 |
| M10 | template: a `'?'` in first place left as it is | P1 1821, P5 1821, P6 1821 |

## Benchmarks

The bench builds 20 strings of 500000 characters, half of them `'?'`
and the rest letters that never repeat their neighbour, once; then it
answers all 20 four times over, 80 answers, by the ★ arm, each answer
folded to its count of `'a'`s, in all five languages. Every
implementation prints `80 answers over 20 strings of 500000 characters:
'a' total 13597380, checksum 524619760`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `76e5a13ad` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.341 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.403 s |
| Kāra (`karac build`) | 0.419 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.430 s |
| Rust (`rustc -O`) | 0.431 s |
| Go | 0.796 s |
| Python | 8.8 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.406 s and 0.436 s on one run).

Kāra is 1.07x Rust under overflow checks by median. Building the strings
one `push` at a time is a large share of every language's time.

## Verification

All four arms print the same output as `replace.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `76e5a13ad`.

## Writing it

The ★ and peek arms were written in Kāra and checked as written. The
bytes arm was first written `let mut b = s.bytes();`, which is a
read-only `Slice[u8]` view of the string, so the write `b[i] = c` is
refused; `karac fix` added `.to_vec()` in one round. The harness first
made a letter with `('a' as i64 + k) as char`, which is refused by
design (not every integer is a `char`, `E_INT_AS_CHAR`, with the
`char.try_from` hint); it writes Rust's `(b'a' + k as u8) as char`.

The Rust template took three rounds of `karac fix`, 3 changed lines,
then 1, then 1:

1. `&&` and `||` to `and` and `or`, and `String::` and `Solution::` to
   `String.` and `Solution.`;
2. `s.into_bytes()` to `s.bytes().to_vec()`;
3. the wrapper's `s.clone()` to `s` (`redundant_clone`: the parameter
   only borrows).

It then checks and agrees with no hand edit.
