# 2299. Strong Password Checker II

A password is said to be **strong** if it satisfies all the following
criteria:

- It has at least `8` characters.
- It contains at least **one lowercase** letter.
- It contains at least **one uppercase** letter.
- It contains at least **one digit**.
- It contains at least **one special character**. The special
  characters are the characters in the following string:
  `"!@#$%^&*()-+"`.
- It does **not** contain `2` of the same character in adjacent
  positions (i.e., `"aab"` violates this condition, but `"aba"` does
  not).

Given a string `password`, return *`true` if it is a **strong**
password*. Otherwise, return *`false`*.

```
password = "IloveLe3tcode!"      ->  true
password = "Me+You--IsMyDream"   ->  false
password = "1aB!"                ->  false
```

**Constraints:** `1 <= password.length <= 100`; `password` consists of
letters, digits, and special characters: `"!@#$%^&*()-+"`.

One pass decides it: four flags, one for each kind a strong password
needs, set as its letters go by, and the letter before, which each
letter must differ from. The length is known before the pass. O(n).

## Approaches

| file | mechanism |
|---|---|
| `strong.kara` ★ | one pass over `chars()`: a `match` with the ranges `'a'..='z'`, `'A'..='Z'`, `'0'..='9'` and the twelve special letters as an or-pattern sets one of four flags; the letter before, starting as `' '`, must differ from each one |
| `strong_naive.kara` | each rule on its own: the letters collected into a `Vec[char]`, one scan for two equal letters side by side, then one scan of the whole password for each kind, the special letters compared with each of a list of twelve |
| `strong_mask.kara` | over `bytes()`: each byte ORs its kind's bit into a mask, 1, 2, 4, or 8 for anything else, which the constraints make a special letter; strong is a mask of 15 |
| `strong_iter.kara` | `chars().zip(chars().skip(1)).all(..)` for no two equal side by side, and `chars().map(kind).fold(0, ..)` ORing each kind's bit, the special letters found by `chars().any(..)` over their list |
| `strong_struct.kara` | `enum Kind { Lower, Upper, Digit, Special }` with `#[derive(PartialEq, Eq, Hash)]`, `kind_of` giving each letter's `Option[Kind]`, and the kinds seen kept in a `Set[Kind]` that a strong password fills with all four; the letter before as an `Option[char]` |
| `strong_solution.kara` | LeetCode's Rust template as a Rust user fills it in: the letters collected into a `Vec<char>`, `windows(2)` for a repeat, and four flags in one `let (mut ..)` set by an `if` chain; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's three examples, then the
shortest strong password, one a letter short, one with a repeat at its
very end, each kind missing in turn, a single letter and 100 letters
that alternate, each with its length and answer; then 20000 random
passwords of 1 to 16 letters, the letters of each kind drawn from 1 to
12 of its letters in a row from a random one on, so that a narrow run
repeats letters often, with the count of strong ones and a checksum.
`strong.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one call, reporting 15 edits:
`struct Solution;` to `struct Solution {}`; the brackets of
`Vec<char>`; the four `mut`s of `let (mut lower, mut upper, mut digit,
mut special)` taken out of the pattern and one put before it, `let mut
(..)`, five edits; the `&` of `for &c` dropped and `&s` made `ref s`;
the three `&&` to `and`; then, once those parse, `.into_iter()` after
`s.windows(2)`, and `"!@#$%^&*()-+".contains(c)` to
`contains(c.to_string())`, since `contains` takes a `Str` pattern
(docs/library/strings.md).

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the letters are counted one by one; each kind is looked for
by walking its list of letters (the alphabet, the alphabet in capitals,
the ten digits and the twelve special letters) against every letter of
the password; and each letter is compared with the one after. No
ranges, no flags. It checks 300 random passwords of 1 to 20 letters,
drawn as the arms' are; then 30 built to be strong, 8 to 20 letters
with the four kinds first in a random order, each letter unlike the one
before; then 30 built the same way and broken in one way, a letter
written twice, the length cut to 7, or every letter of one kind made a
letter of another. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | every letter's case swapped: the same answer |
| P3 | the password reversed: the same answer |
| P4 | every letter written twice: not strong |
| P5 | every letter moved one on within its kind, the last to the first: the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 938147161, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
builds the same cases and judges them with `any` and `all`. Of the 360,
128 are strong. On a failure it prints the first ten and then the count
by property.

The random letters were at first drawn from the first 1 to 12 letters
of each kind, as the bench's are. Then no case held a `z`, a `+` was
rare and a `9` was the only digit in almost none, and the edits that
take `z` from the lowercase letters, `+` from the special ones or `9`
from the digits failed nothing. Each run of letters now starts at a
random one and wraps round.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a length of 7 enough | P1 15, P6 15 |
| M3 | ★: `+` not a special letter | P1 2, P5 4, P6 2 |
| M5 | ★: `9` not a digit | P1 3, P5 4, P6 3 |
| M7 | naive: the repeat scan from the third letter | P1 1, P3 6, P6 1 |
| M9 | naive: any letter counted as uppercase | P1 4, P2 12, P6 4 |
| M11 | naive: digits looked for in the first eight letters | P1 9, P3 12, P6 9 |
| M12 | mask: `z` not a lowercase letter | P2 1 |
| M13 | mask: `A` counted special | P1 4, P2 7, P5 5, P6 4 |
| M16 | mask: the bits toggled, not set | P1 116, P6 116 |
| M17 | iter: each letter compared with the one two on | P1 71, P4 153, P6 71 |
| M19 | iter: a digit given the uppercase bit | P1 128, P6 128 |
| M21 | iter: two equal digits side by side allowed | P1 13, P6 13 |
| M22 | struct: three kinds enough | P1 21, P6 21 |
| M23 | struct: the letter before never kept | P1 88, P4 245, P6 88 |
| M25 | struct: a length of 8 refused | P1 6, P6 6 |
| M28 | solution: a length of 9 refused | P1 16, P6 16 |
| M29 | solution: the parentheses not special | P1 5, P5 5, P6 5 |

P1 and P6 kill sixteen, P5 four, P2 three, and P3 and P4 two each. P1
misses only the mask arm's `z` not a lowercase letter: no answer among
the 360 cases turns on a `z`, but swapping the case of one makes `Z` the
only uppercase letter of some password, and P2 sees the answer change.
P5, every letter moved one on within its kind, fails where an edit
treats one letter of a kind unlike its neighbours, `+`, `9`, `A`, or `(`
and `)`: moving one on carries a letter onto it or off it. P2 fails
where the cases are not handled alike: any letter counted as uppercase,
`A` counted special, `z` dropped. P3, the password reversed, fails for
the two edits that look at one end only: the repeat scan that skips the
first pair, and the digits looked for in the first eight letters. P4,
every letter written twice, fails where a repeat is not seen: the letter
before never kept, and each letter compared with the one two on.

Of the thirty-one, fourteen were not kept. The ★ arm's `z` not a
lowercase letter (M2) fails as the mask arm's (M12); its letter before
never moved on (M4) as the struct arm's letter before never kept (M23);
the naive arm's `!` not a special letter (M8) as the ★ arm's `+` (M3);
the length of 8 refused in the naive (M10) and iter (M18) arms and the
mask arm's special letter not needed (M14) as the struct arm's length
of 8 refused (M25); the mask arm's byte compared with the one two back
(M15) and the template's windows of three (M27) as the iter arm's
letter compared with the one two on (M17); the iter arm's kinds summed
(M20), the struct arm's uppercase letter a `Lower` (M24) and hex digit
a `Lower` (M26) and the template's digit counted uppercase (M30) as the
iter arm's digit given the uppercase bit (M19), all of which make a
strong password impossible; and the template's special letter enough
alone (M31) as the struct arm's three kinds enough (M22). The ★ arm's
digit or special letter enough (M6) fails in a way of its own, past the
three kept for its arm.

## Verification

Every arm prints the same output as `strong.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply. It once
had one thing for the differential: `karac fix` turns on the style
lints, and took the `.iter()` off `for kind in [LOWER, UPPER, DIGITS,
SPECIAL].iter()`, which `check` leaves alone; the differential iterates
the list itself.

Under `karac __mir-run` every arm takes 1.5 to 2.1 s, the iterator arm
the longest, and the differential 0.9 s.

## Benchmarks

The bench builds 2 * 10^5 random passwords of 8 to 20 letters once, the
letters of each kind drawn from its first 1 to 12, then makes 20 passes
over all of them with the ★ arm in all five languages, pass `p`
starting at password `7p`. Every implementation prints `20 passes over
2 * 10^5 passwords: checksum 401347018`. C keeps the passwords in a
fixed `char` table with their lengths and tests the special letters
with a `switch`; Rust keeps a `Vec<String>` and the same `match`; Go a
`[]string` and a `switch`; Python a list of `str` and comparisons.

BENCHTAB
