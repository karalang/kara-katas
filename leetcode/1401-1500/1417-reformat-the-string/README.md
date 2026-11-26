# 1417. Reformat The String

You are given an alphanumeric string `s` (a string of lowercase English
letters and digits). Find a permutation of the string where no letter is
followed by another letter and no digit is followed by another digit,
that is, no two adjacent characters have the same type. Return the
reformatted string, or an empty string if it is impossible to reformat
it.

```
s = "a0b1c2"        ->  "0a1b2c"    "a0b1c2", "0a1b2c" and "c2a1b0" are also valid
s = "leetcode"      ->  ""          only letters
s = "1229857369"    ->  ""          only digits
```

**Constraints:** `1 <= s.length <= 500`, `s` consists of only lowercase
English letters and/or digits.

Each arm is `fn reformat(s: String) -> String`. LeetCode accepts any
valid permutation; every arm here gives the same one, so that the arms
can be compared: the kind there is more of first, a letter on a tie, and
each kind in the order `s` has it.

## Approaches

| file | mechanism |
|---|---|
| `reformat.kara` ★ | the letters and the digits collected apart, and woven together from the larger group; no weave when one group has two or more over the other, by `abs_diff`. O(n) |
| `reformat_places.kara` | the larger group's characters written to the even places of a `Vec[char]` and the other's to the odd ones, in one pass over `s`. O(n) |
| `reformat_zip.kara` | the two groups split by `partition`, zipped pair by pair, the larger first, and its one left over put at the end. O(n) |
| `reformat_turns.kara` | one index into each group, and the turn passed back and forth; whoever has more starts, and a turn with nothing left ends it with no answer. O(n) |
| `reformat_solution.kara` | a Rust solution as LeetCode's Rust users write it (two `Vec<char>`, `(a, b)` as references to the larger and the smaller, `String::with_capacity`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and four
more, `-` for no answer (`a0b1c2 - - c2o0v1i9d a 7 a1b2c`); the
constraints' most, 500 drawn characters, 250 digit and letter pairs, and
the same with its first digit gone (`500 characters: 0
q0q1q2q3q4q5q6q7q8q9 499`); and 2000 random strings of 1 to 30
characters, a digit one time in 2 or 3 (`2000 random strings: 1432
empty, checksum 9027292`). `reformat.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the harness's `shown`, which returns its parameter when
it is not empty, took the parameter bare, and `karac fix` makes it `own
String`; it also drops a `half.clone()` passed where a borrow does. The
harness first built its 250 pairs, and the zip arm its woven pairs, by
collecting `f"..."` pieces straight into a `String`, Rust's
`FromIterator<String> for String`. A `String` is built by `collect` only
from `char`s, and the refusal says to collect the pieces into a
`Vec[String]` and join them. For the zip arm `karac fix` writes that,
`Vec[String].from_iter(..).join("")`, which the arm keeps as a `let
pairs: Vec[String]` and a `join`. For the harness's `(0..250).map(|i|
f"{i % 10}q").collect()` it has no fix: the rewrite's span starts inside
the `(` that opens the chain, so the edit would leave a stray `(`, and
`karac fix` refuses to write it
([B-2026-11-26-13](https://github.com/karalang/kara/blob/main/docs/bugs-v2.jsonl)).
The harness collects into a `Vec[String]` and joins it by hand. The Rust
solution takes one round of 20 fixes by `karac fix`'s count: `struct
Solution;` to `struct Solution {}`, `Vec<char>` to `Vec[char]`,
`Vec::new()` and `String::new()` to `Vec.new()` and `String.new()`,
`(&letters, &digits)` to `(ref letters, ref digits)`,
`String::with_capacity` to `String.with_capacity`, the harness's `own`,
and `Solution::` to `Solution.`. Its `(letters.len() as
i32 - digits.len() as i32).abs() > 1` is taken as written. Every arm's
output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a permutation built a character at a time, each one any not
yet used whose kind differs from the one before, tried from a letter
first and from a digit first, and an answer exactly when one of them
reaches the full length. LeetCode's examples, ten edge cases (one
character of each kind, two of one, a tie in either order, one more of
either kind), the constraints' most three ways (250 pairs, one character
fewer, one more), and 1987 random strings of 1 to 30 characters, half
drawn as in the arms' harness and half as shuffled pairs with one more
or one fewer of either kind.

| | property |
|---|---|
| P1 | the statement read literally: an answer exactly when some permutation alternates |
| P2 | an answer is a permutation of `s` |
| P3 | no two letters and no two digits side by side |
| P4 | each kind in the order `s` has it |
| P5 | the larger kind first, a letter on a tie |
| P6 | the ★ arm's answer |

All 45,710 checks pass on every arm: `2003 cases: checksum 969492765,
45710 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, writing the
larger kind to the even places and the other to the odd ones, gives the
same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a weave tried when one kind has two over the other | P1 155, P3 155, P6 620 |
| M2 | ★: the digits first on a tie | P5 405, P6 1620 |
| M3 | places: the digits on the even places on a tie | P5 405, P6 405 |
| M4 | places: the larger kind written to every place from the first, not every other | P2 1137, P3 1106, P4 1137, P6 1137 |
| M5 | zip: a weave tried when one kind has two over the other | P1 155, P2 155, P4 155, P6 155 |
| M6 | zip: the larger kind's first character put at the end, where its last goes | P2 688, P4 688, P6 688 |
| M7 | turns: the letters always start | P1 409, P6 409 |
| M8 | turns: the turn never passed, so one kind is written until it runs out | P1 1226, P3 40, P6 1226 |
| M9 | solution: the smaller kind's last character left out | P2 1186, P3 781, P4 1186, P6 1186 |
| M10 | solution: the larger kind's character written twice, in place of the other's | P2 1186, P3 1186, P4 1186, P6 1186 |

## Benchmarks

The bench builds a pool of 10^5 letter and digit pairs, each pair in a
drawn order, and runs the ★ arm on 20000 windows of 500 characters, each
window's start drawn. Every implementation prints `20000 windows of 500
characters: checksum 134902125`.

BENCHTAB

Kāra is level with Rust and Go here, measured by hand at 0.14 to 0.18 s
against Rust's 0.15 to 0.17 s (0.15 s with overflow checks on) and Go's
0.14 to 0.17 s; C takes 0.09 s and Python 1.68 s.
