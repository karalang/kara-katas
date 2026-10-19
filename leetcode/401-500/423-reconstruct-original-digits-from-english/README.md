# 423. Reconstruct Original Digits from English

Given a string `s` containing an out-of-order English representation
of digits 0-9, return the digits in ascending order.

```
s = "owoztneoer"  -> "012"
s = "fviefuro"    -> "45"
```

**Constraints:** `1 <= s.length <= 10^5`; `s[i]` is one of the
characters `"e","g","f","i","h","o","n","s","r","u","t","w","v","x","z"`;
`s` is guaranteed to be valid.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `original_digits.kara` ★ | unique letters: z, w, u, x and g each belong to one digit's word (zero, two, four, six, eight). With those counted, h, f, s, o and i each belong to one remaining digit (three, five, seven, one, nine), less the counted digits that share them | O(n) | O(1) |
| `original_digits_peel.kara` | peel words: take the words out of the letter counts in the order zero, two, four, six, eight, three, five, seven, one, nine; each digit occurs as often as its scarcest letter allows | O(n) | O(1) |
| `original_digits_search.kara` | search: choose each digit's count from 0 to 9, most copies first, backtracking when the letters cannot be used up. A letter that only digits up to `d` use must be used up after choosing `d`, which the search reads off a table of the last digit using each letter, not from any reasoning about the words | O(n) here | O(1) |
| `original_digits_solve.kara` | linear algebra: the 26 letter counts are a linear function of the 10 digit counts, and Gaussian elimination on whole numbers (scale by the pivot, subtract, divide by the gcd) recovers them | O(n) | O(1) |
| `differential.kara` | the four arms on 2,000 random strings, five properties, one of them the digits the string was built from | — | — |

Every arm prints the same 11 lines: the two LeetCode examples, eight
more strings (two single words, two words run together, a digit twice,
two digits twice each, one digit three times, the digits 1 to 9 once
each, three digits whose words share letters), and for 2,000 random strings of 1
to 30 digits' words with the letters shuffled, the total number of
letters and a checksum of the answers. `original_digits.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. Each of 2,000 random
cases draws 1 to 25 digits from a random run of 1 to 10 consecutive
digits, so that some digits repeat many times and others are absent,
writes their words and shuffles the letters:

| | property |
|---|---|
| P1 | the answer is the digits the string was built from, in order |
| P2 | the same digits shuffled another way give the same answer |
| P3 | the answer's words, written out, have exactly the input's letters |
| P4 | the letters of one more digit added give the answer with that digit added |
| P5 | `k` copies of one word give `k` copies of its digit, and the ten words in order give `0123456789` |

It prints `2000 cases, 4 arms, 40000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | unique: three does not discount eight's h | P1 776, P3 776, P4 886, P5 2000 |
| M2 | unique: nine does not discount six's i | P1 1028, P3 1028, P4 1135, P5 2000 |
| M3 | peel: one is taken before two, four and the rest | P1 706, P3 706, P4 880, P5 2000 |
| M4 | peel: each digit's letters are removed once, not once per copy | P1 1929, P3 1929, P4 1971, P5 1585 |
| M5 | search: the used-up check is gone | P1 740, P3 740, P4 934, P5 2000 |
| M6 | search: zero copies is never tried | P1 1977, P3 1977, P4 1972, P5 2000 |
| M7 | solve: rows above the pivot are not eliminated | P1 1941, P3 1941, P4 1994, P5 2000 |
| M8 | solve: the pivot row is added, not subtracted | P1 1986, P3 1986, P4 2000, P5 2000 |

No mutant fails P2: every arm reads only the letter counts, which a
reshuffle keeps. P1 and P3 fail together on every mutant, since a wrong
digit list never spells the same letters. A first M8, which skipped
dividing each count by its pivot, survived: the coefficient matrix is
the same for every input, and every pivot ends as 1 after the gcd step,
so for these ten words the division never changes anything.

M5 shows that the search arm's only check is that pruning step. With
it gone, the search takes the most copies of every digit and stops at
the end without checking that the letters were used up.

## Verification

All four arms print the same output as `original_digits.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run` and
`karac run --interp`, and `karac check` passes on every file. The
differential prints `40000 checks, 0 failures` on the same three.

LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac build` panic in the
frozen legacy codegen on `for b in s.bytes()` over a `Str` parameter
(`into_struct_value` in `control_flow_for.rs`), which every arm uses,
as kata 383 recorded. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm on one text of 359,611 letters:
20,000 blocks, each the words of 1 to 8 random digits with the letters
shuffled within the block. Each of 100,000 calls takes a run of 50 to
249 whole blocks as a slice of the text, so the input is valid and no
call copies it; the answer is a new string every call, and the program
folds every digit of it into a checksum. Every implementation prints
`100000 calls on 359611 letters: 67212547 digits, checksum 974218869`;
a 100-call cut of the Kāra program under `karac __mir-run` prints the
same as the C program cut the same way. Spot timings on a shared
4-core container, three runs each (`bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.56 to 0.61 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.67 to 0.73 s |
| Rust (`rustc -O`) | 0.71 to 0.76 s |
| Go | 0.85 to 0.91 s |
| Python | 25 s |

No `karac build` time: the frozen legacy codegen panics on the ★ arm's
`for b in s.bytes()` over a `Str` parameter (`into_struct_value` in
`control_flow_for.rs`), as kata 383 recorded. The Kāra program prints
the same line under `karac __mir-llvm-run` in 6.6 s, compile included;
that JITs the MIR's IR without optimization passes, so it is not a
benchmark.

## Compiler findings

- **`karac fix` rewrites `abs(a)` into `a(a)`** (B-2026-10-12-18). The
  linear-algebra arm's first gcd helper wrote `abs(a)`, though `abs` is
  a method (`a.abs()`). `karac check` answers "undefined name 'abs',
  did you mean 'a'?" with a machine-applicable replacement, and
  `karac fix` applies it, turning the call into `a(a)`, which then
  fails as "type 'i64' is not callable". A callee suggestion should
  offer only names that can be called, and here the useful one is the
  method. The arm uses `a.abs()`.

### Migrated to the v2 checker

At kara `5656fc5a1c` `karac check` refused the differential:
`split_whitespace` returns an iterator now, and `mut` markers were
missing. `karac fix` offers the right edits but applies none of them: an
ownership fix-it that follows from the uncollected iterator suggests
`#[derive(Clone)]` on the stdlib's `StrWords`, at an offset into the
stdlib's source, so the fix aborts with "fix would write past end of
file" (kara B-2026-10-19-17; kata 425's differential hits the same).
The other edits, taken from `karac check --output=json`, were applied by
script, and the differential prints the same output as its corpus
`expected.out`.
