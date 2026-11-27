# 1805. Number of Different Integers in a String

You are given a string `word` that consists of digits and lowercase
English letters. You will replace every non-digit character with a
space. For example, `"a123bc34d8ef34"` will become `" 123  34 8  34"`.
Notice that you are left with some integers that are separated by at
least one space: `"123"`, `"34"`, `"8"`, and `"34"`. Return the number
of different integers after performing the replacement operations on
`word`. Two integers are considered different if their decimal
representations without any leading zeros are different.

```
word = "a123bc34d8ef34"    ->  3
word = "leet1234code234"   ->  2
word = "a1b01c001"         ->  1
```

**Constraints:** `1 <= word.length <= 1000`, and `word` consists of
digits and lowercase English letters.

The arms are `fn num_different_integers(word: String) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `num_different_integers.kara` ★ | one walk of the word's chars: a run of digits gathered into a `String` until a letter ends it, its leading zeros left out as they come, and each run put in a `Set[String]`, whose size is the answer. O(n) |
| `num_different_integers_split.kara` | the word's chars collected into a `Vec[char]` and split at every letter by the sequence's `split`, each run stripped of its leading zeros by `skip_while` and collected into a `String` for the `Set`. O(n) |
| `num_different_integers_sorted.kara` | no `Set`: the runs gathered as the ★ arm gathers them into a `Vec[String]`, sorted so that equal numbers sit side by side, and counted where a number differs from the one before it. O(n log n) |
| `num_different_integers_views.kara` | no copies: the word's bytes walked by index, each run found past its leading zeros, and kept as a `Str` view into the word in a `Set[Str]`. O(n) |
| `num_different_integers_solution.kara` | a Rust solution as LeetCode's Rust users write it (`word.split(\|c: char\| c.is_ascii_alphabetic())`, `trim_start_matches('0')`, a `HashSet` of the pieces), carried to Kāra by `karac fix`, then by hand where no fix applies |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples (`3 2 1`);
five edges, no digits, one 0, zeros alone, which are all 0, a run of 400
nines past any machine integer beside the same run behind five zeros,
and `x10y010z100`, where 10 and 010 are one number (`0 1 1 1 2`); the
constraints' most, 1000 digits, 1000 letters and 500 pairs of a digit
and a letter (`the most: 1 0 1`); and 3000 random words of 1 to 30
characters, mostly 0, 1 and 2 among the letters a to c so that numbers
repeat (`3000 random words: checksum 738620508`).
`num_different_integers.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★ arm was first written as the Rust solution is,
`word.split(|c: char| c.is_ascii_lowercase())` and
`run.trim_start_matches('0')`, and check refused both, with no fix. A
string's patterns are `Str` only in v1, a predicate deferred to a
`Pattern` trait (`docs/deferred.md` § String Patterns), and the refusal
of `trim_start_matches` names `strip_prefix` in a loop, but the refusal
of the split was a bare "expected 'Str', found 'Fn(char) -> bool'" that
named neither the deferral nor a way to write it: that is
B-2026-11-27-70, fixed at c3b1ab46de, after which check names the
deferral and the sequence's `split`, which the split arm uses. The ★ arm
is now the one walk above. In the harness, check refused two `&` on
`"0".repeat(5)` and `"9".repeat(400)` in a string sum and rewrote
`char.from_u32(..)` to `char.try_from(..).ok()`, 3 fixes. The split
arm's `skip_while(|c| **c == '0')` dereferenced a `char` that is copied,
and the views arm's `word.as_bytes()` is `word.bytes()` in Kāra; `karac
fix` made each change, 1 fix each. The sorted arm checks clean as first
written. The Rust solution takes 5 fixes by `karac fix`'s count, and its
diff is: `use std::collections::HashSet;` dropped; `struct Solution;` to
`struct Solution {}`; `HashSet::new()` to `Set.new()`; and
`!s.is_empty()` to `not s.is_empty()`. Its split and
`trim_start_matches` keep the two refusals, so it was changed by hand as
the messages say: the word's chars collected into a `Vec[char]` and
split by the sequence's `split`, and each run's zeros dropped by
`skip_while`, collected into a `String`. The first hand edit wrote
`.collect::[String]()` inside the `insert`, which check refused as a
turbofish and `karac fix` removed; the `Set.new()` then had nothing to
fix its type, and check said to annotate a binding, so the run is bound
to `let digits: String` first. Every arm's output matches on the first
run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every letter replaced with a space, the integers left between
the spaces split by `split_whitespace`, each stripped of its leading
zeros with `strip_prefix` in a loop, and an integer counted when no
integer before it is the same. LeetCode's examples, the edges, the
constraints' most, and 1988 random words of 1 to 30 characters over all
26 letters and up to 10 digits. Each arm meets six properties on each
case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | a letter added at each end, or every letter changed to `z`, gives the same answer |
| P3 | a zero written before every run of digits gives the same answer |
| P4 | the word written twice with a letter between gives the same answer |
| P5 | the answer is at most the number of runs of digits and at most the number of digits |
| P6 | the ★ arm's answer |

The differential checks clean as first written. All 60,000 checks pass
on every arm: `2000 cases: checksum 233896940, 60000 checks over 5 arms:
0 failures`, under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. Python, running the ★ arm's mirror over the same
cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a run's leading zeros kept | P1 206, P6 824 |
| M2 | ★: a run that ends the word left out | P1 571, P2 571, P4 571, P6 2284 |
| M3 | split: the ones skipped at a run's start, not the zeros | P1 261, P3 103, P6 261 |
| M4 | split: the empty runs between letters counted | P1 1272, P2 147, P5 1098, P6 1272 |
| M5 | sorted: the runs never sorted | P1 252, P4 1053, P6 252 |
| M6 | sorted: a run never cleared after a letter | P1 401, P4 1261, P6 401 |
| M7 | views: a run's leading zeros kept | P1 206, P6 206 |
| M8 | views: the view taken from the word's start | P1 526, P4 1433, P6 526 |
| M9 | solution: every zero dropped, not only the leading ones | P1 111, P6 111 |
| M10 | solution: the one-digit runs left out | P1 1006, P3 1006, P6 1006 |

## Benchmarks

The bench builds 64 random words of 1000 characters once, half of them
digits from 0 to 3 so that runs repeat and lead with zeros, and makes
20000 calls of the ★ arm, each word drawn from the checksum so far. It
checks clean as first written. The C mirror keeps the set as an
open-addressed table of copied runs hashed by FNV-1a. Every
implementation prints `20000 calls over 64 words of 1000 characters:
checksum 89906081`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.51 s against Rust's 0.57 s (0.58 s with
overflow checks on), C's 0.32 s and Go's 0.57 s; Python takes 1.5 s.
