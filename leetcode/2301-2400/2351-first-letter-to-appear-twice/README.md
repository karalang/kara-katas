# 2351. First Letter to Appear Twice

Given a string `s` consisting of lowercase English letters, return *the
first letter to appear **twice***.

**Note:**

- A letter `a` appears twice before another letter `b` if the **second**
  occurrence of `a` is before the **second** occurrence of `b`.
- `s` will contain at least one letter that appears twice.

```
s = "abccbaacz"  ->  "c"
s = "abcdd"      ->  "d"
```

**Constraints:** `2 <= s.length <= 100`; `s` consists of lowercase
English letters; `s` has at least one repeated letter.

The answer is the letter at the first place whose letter has appeared
before, so a scan from the left can stop there. By the pigeonhole
principle that place is at most the 27th, whatever the length.

## Approaches

| file | mechanism |
|---|---|
| `twice.kara` ★ | a table of 26 marks, one per letter; the first letter met that is already marked is the answer. O(n) |
| `twice_mask.kara` | the same marks as the bits of one `i64`, tested and set with shifts. O(n) |
| `twice_set.kara` | the letters met so far in a `Set`, whose `insert` returns false for one already there. O(n) |
| `twice_naive.kara` | no table: for each place from the left, every earlier place compared with it. O(n^2) |
| `twice_iter.kara` | iterators: the letters with their places by `enumerate`, and `find` for the first whose prefix before it already `contains` it |
| `twice_solution.kara` | LeetCode's Rust template: a `HashSet` and `!seen.insert(c)`, ending in `unreachable!()`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; two letters;
the alphabet then its first letter; the alphabet backwards then `m`; 100
letters stepping 7 through the alphabet; then 2000 random strings of 2
to 30 letters from the first 2 to 26 of the alphabet, one with no letter
twice getting a copy of one of its letters, with a checksum and how
often `a`, `b` and `z` were the answer. `twice.py` mirrors the ★ arm and
its output is byte-identical, and the mirror was checked against the
literal reading on 3000 random strings.

`karac fix` carries the template in one call, reporting 7 edits.
`check` first reports 6 errors, each with its edit: the
`use std::collections::HashSet` import deleted, `struct Solution;`
written `struct Solution {}`, the two `::` paths written with `.`, `!`
written `not`, and `unreachable!()` written `unreachable()`, since Kāra
has no macros. The seventh follows from the first: with the import gone,
`HashSet.new` becomes the prelude's `Set.new`. The set's element type is
inferred from the `insert(c)` below it, as in Rust.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each place in turn, every earlier place checked for the
same letter, and the first place with a match gives the answer. It
checks 300 random strings of 2 to 30 letters from the first 2 to 26 of
the alphabet, then 30 of up to 2000 letters, then 26 that are the
alphabet from one letter on, wrapped, and then a letter of it again. A
string with no letter twice gets a copy of one of its letters. All 356
are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer is in the string at least twice |
| P3 | every letter moved 7 on in the alphabet, wrapping: the answer moved 7 on too |
| P4 | the string with its own letters appended: the same answer |
| P5 | the string cut just after the answer's second place: the same answer |
| P6 | each arm agrees with at least three of the other five |

P4 holds because the first repeat is already inside the first copy, and
P5 because nothing after it can change which repeat comes first.

The differential prints `356 cases: checksum 128819106, 12816 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and finds the first repeat with a set. On a failure it
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
| M1 | ★: no letter ever marked | P1 356, P2 356, P3 356, P5 356, P6 356 |
| M2 | ★: z taken for a | P1 25, P2 25, P3 38, P5 25, P6 25 |
| M4 | ★: letters merged in pairs | P1 150, P2 84, P3 185, P5 84, P6 150 |
| M7 | mask: only the last letter remembered | P1 196, P2 111, P3 111, P4 19, P5 198, P6 196 |
| M8 | mask: letters 16 apart merged | P1 57, P2 48, P3 40, P5 48, P6 57 |
| M10 | mask: the next letter marked | P1 294, P2 151, P3 45, P4 13, P5 164, P6 294 |
| M12 | set: the first new letter returned | P1 236, P2 128, P5 128, P6 236 |
| M15 | set: a's repeat ignored | P1 36, P2 8, P3 40, P4 8, P5 8, P6 36 |
| M16 | set: the third new letter returned | P1 195, P2 110, P5 110, P6 195 |
| M17 | naive: the letter just before never compared | P1 76, P2 15, P3 15, P4 15, P5 61, P6 76 |
| M18 | naive: the first letter with a later copy | P1 139, P4 128, P6 139 |
| M20 | naive: the last letter never reached | P1 64, P2 64, P3 64, P4 64, P5 356, P6 64 |
| M24 | iter: the last repeat, not the first | P1 221, P4 79, P6 221 |
| M25 | iter: the first two letters skipped | P1 15, P2 5, P3 5, P4 5, P5 24, P6 15 |
| M26 | iter: only the first half before looked at | P1 165, P2 52, P3 52, P4 52, P5 111, P6 165 |
| M27 | solution: the string read backwards | P1 233, P5 94, P6 233 |
| M31 | solution: a returned at a repeat | P1 320, P2 203, P3 356, P5 203, P6 320 |

P1 and P6 kill all seventeen, P5 sixteen, P2 fourteen, P3 twelve and P4
nine. P5 misses only the first letter with a later copy, which still
answers the cut string with the same letter, since its first place
comes before every other letter's second. P4, the string doubled, fails
the edits that can miss every repeat of a short string and then find
one in the copy, and the two that pick a later repeat than the first.
P3 fails the edits tied to particular letters (z taken for a, letters
merged in pairs or 16 apart, a's repeat ignored, a returned) and those
that lose places, but not the ones that only pick the wrong repeat.

Of the thirty-one, fourteen were not kept. A letter marked before it is
checked and the first letter returned at a repeat in the ★ arm (M3,
M6), the first letter returned in the naive arm (M19) and each letter
found among the letters through itself in the iter arm (M22) all return
the first letter, as the kept set arm's first new letter (M12) does. A
space returned in the set arm (M14) fails as no letter ever marked
(M1); a never marked in the ★ arm (M5) as a's repeat ignored (M15); each
letter looked for after itself in the iter arm (M23) as the naive arm's
first letter with a later copy (M18); the set arm's string read
backwards (M13) as the template's (M27); and the template's first z
returned (M28) as the mask arm's z marked from the start (M11). Every
letter a repeat once a is seen (M9), z marked from the start (M11) and
the naive arm's first letter never matched (M21) fail apart from every
kept one and were left out to keep three to an arm. The template's
repeat with one letter so far ignored (M29) and first letter skipped
(M30) end in its `unreachable()` on a string such as `"aa"`, a crash,
so they are not kept either.

## Verification

Every arm prints the same output as `twice.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.3 to 0.4 s. The differential
takes 1.2 s there and 0.47 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds `10^5` strings once from the harness's generator,
string `t` being the first 2 to 26 letters of the alphabet shuffled and
then one of them again, so the answer is always the last letter, and
then makes 50 passes, pass `p` folding each answer plus `p` into the
checksum, with the ★ arm in all five languages. Every implementation
prints `50 passes over 10^5 strings: checksum 738520035`. No
implementation allocates in the counted loop.

BENCHTAB
