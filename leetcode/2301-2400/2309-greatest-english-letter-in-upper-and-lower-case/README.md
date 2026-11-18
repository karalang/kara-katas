# 2309. Greatest English Letter in Upper and Lower Case

Given a string of English letters `s`, return *the **greatest** English
letter which occurs as **both** a lowercase and uppercase letter in*
`s`. The returned letter should be in **uppercase**. If no such letter
exists, return *an empty string*.

An English letter `b` is **greater** than another letter `a` if `b`
appears **after** `a` in the English alphabet.

```
s = "lEeTcOdE"     ->  "E"
s = "arRAzFif"     ->  "R"
s = "AbCdEfGhIjK"  ->  ""
```

**Constraints:** `1 <= s.length <= 1000`; `s` consists of lowercase and
uppercase English letters.

Which letters occur in each case is two sets of 26, and the answer is
the greatest letter in both: one pass to fill them and at most 26 steps
from `Z` down. O(n).

## Approaches

| file | mechanism |
|---|---|
| `greatest.kara` ★ | two 26-bit masks over `s.bytes()`, one of the lowercase letters and one of the uppercase; the highest bit of `lower & upper`, from 25 down, is the answer |
| `greatest_naive.kara` | each letter from `Z` down, the whole string scanned for its uppercase and its lowercase; the first found both ways is the answer. O(26 n) |
| `greatest_set.kara` | a `Set[char]` of the letters seen: each letter's other case looked up as it comes, and when it is there the uppercase letter is a candidate, the greatest kept in an `Option[char]` |
| `greatest_table.kara` | two `[false; 26]` tables filled by `match`ing each letter on `'a'..='z'` and `'A'..='Z'`, then read with a `while` from 25 down |
| `greatest_iter.kara` | the uppercase letters `filter`ed to those whose both cases the string holds, by `any` over its `chars`, then `max`, `map`ped to a `String`, `unwrap_or` the empty one. O(26 n) |
| `greatest_solution.kara` | LeetCode's Rust template: a `[false; 128]` table indexed by each byte `as usize`, then `(b'A'..=b'Z').rev()` and each letter's lowercase at `c + 32`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples; `qQ`;
`z` and `Z` at the two ends of a string of every lowercase letter;
`Aa`; every uppercase letter alone; then 2000 random strings of 1 to 60
letters, each drawn from its own handful of 1 to 24 of the 52, so that
about half hold a letter both ways, with a checksum of the answers and
the count that have one. `greatest.py` mirrors the ★ arm and its output
is byte-identical.

`karac fix` carries the template in one call, reporting 5 edits:
`struct Solution;` to `struct Solution {}`; `&&` to `and`;
`String::new()` to `String.new()`; in the harness's wrapper,
`Solution::greatest_letter` to `Solution.greatest_letter`; and, in the
harness, an `.iter()` on the array literal that a `for` walks, dropped
since a `for` walks an array as it is. `fix --dry-run` asked for that
last one in every arm's harness, and every arm has it applied. The
`[false; 128]` table, the `b'A'..=b'Z'` byte range, `as usize` and
`as char` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every pair of places in the string, the first holding an
uppercase letter and the second its lowercase, makes that uppercase
letter a candidate, and the greatest candidate, compared as a string,
is the answer, or `""` when there is none. No masks and no tables. It
checks 300 random strings of 1 to 60 letters drawn from a handful of
the 52; then 30 that hold every letter in one case and up to 3 in the
other; then 30 of up to 1000 letters from all 52, where nearly every
letter pairs. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer is `""` or one uppercase letter whose lowercase the string also holds |
| P3 | the string reversed: the same answer |
| P4 | every letter's case swapped: the same answer |
| P5 | the answer's letter taken out in both cases: an answer that is `""` or a smaller letter |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 991464266, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
builds the same cases and takes the greatest uppercase letter of
`set(s)` whose lowercase is in `s`. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the masks ORed, not ANDed | P1 309, P2 309, P6 309 |
| M5 | ★: each uppercase letter one bit higher | P1 181, P2 126, P4 199, P6 181 |
| M6 | ★: `a` and `z` counted as uppercase | P1 39, P6 39 |
| M8 | naive: the lowercase looked for one letter on | P1 183, P2 129, P4 200, P6 183 |
| M10 | naive: the answer from the lowercase table | P1 196, P2 196, P6 196 |
| M11 | naive: the flags kept from the letter before | P1 201, P2 201, P6 201 |
| M13 | set: the latest candidate kept, not the greatest | P1 71, P3 69, P5 56, P6 71 |
| M14 | set: the candidate in the case it came in | P1 166, P2 166, P3 70, P4 70, P6 166 |
| M15 | set: each letter added to the set after its lookup, not before | P1 196, P6 196 |
| M18 | table: `z` never looked at | P1 35, P6 35 |
| M20 | table: `A` never looked at | P1 4, P6 4 |
| M21 | table: the answer one letter on | P1 196, P2 196, P5 196, P6 196 |
| M22 | iter: the least, not the greatest | P1 101, P5 101, P6 101 |
| M23 | iter: the uppercase alone enough | P1 261, P2 261, P4 309, P6 261 |
| M24 | iter: the lowercase alone enough | P1 249, P2 249, P4 309, P6 249 |
| M27 | solution: the lowercase looked for 31 on, not 32 | P1 176, P2 124, P4 199, P6 176 |
| M30 | solution: the table filled from the first half of the string | P1 68, P3 93, P5 1, P6 68 |

P1 and P6 kill all seventeen, P2 ten, P4 six, P5 four and P3 three. P2
fails for any answer that is not an uppercase letter held both ways,
which is most of the edits that test the wrong letters. P4, the cases
swapped, fails where an edit treats the two cases differently: a bit or
a lookup shifted on one side only, or one case alone enough. P5 fails
where the answer is a smaller letter than the greatest one, or a letter
past it, and once for the template's table from the first half. P3, the string reversed, fails only where the order of the
letters matters: the set arm's latest candidate and its candidate in
the case it came in, and the template's table from the first half.

The template's first-half table (M30) and its greatest uppercase
letter the only one tried, below, replace two edits that failed as
others did, Z left out and the letters from A up, so that the template
has two edits of its own to keep.

Of the thirty-one, fourteen were not kept. The masks ORed (M1) fail as
a letter found in one case enough in the naive arm (M7), a letter its
own other case in the set arm (M12) and a letter in either table enough
in the table arm (M19); the least letter found, in the ★ (M2), naive
(M9) and set (M16) arms, as the iter arm's (M22); `z` never looked at
in the ★ arm (M3) and `Z` left out of the iter arm's letters (M25) as
the table arm's `z` (M18); the answer in lowercase in the ★ (M4) and
iter (M26) arms as the naive arm's answer from the lowercase table
(M10); the table arm's uppercase table filled from the lowercase (M17)
and the template's every letter seen as at least `a` (M31) as the set
arm's lookup before the insert (M15); the template's uppercase alone
enough (M28) as the iter arm's (M23). The template's greatest uppercase
letter the only one tried (M29) fails apart from every kept one, and
was left out to keep two to the template.

## Verification

Every arm prints the same output as `greatest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, set, table and template arms take 0.3
s, the naive and iter arms, which scan the string again for each
letter, 1.3 and 1.7 s. The differential takes 7.6 s there, its literal
reading comparing every pair of places in strings up to 1000 long, and
0.5 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 1000 strings of 1000 letters once, each from its own
pool of 1 to 30 of the 52 letters, then makes 100 passes over all of
them with the ★ arm in all five languages, folding each answer's byte,
0 for none, into a checksum. Every implementation prints `100 passes
over 1000 strings of 1000 letters: checksum 693568555`. Each walks the
string's bytes into two 64-bit masks and builds a one-letter string
for the answer, but C, which returns the letter's byte.

BENCHTAB
