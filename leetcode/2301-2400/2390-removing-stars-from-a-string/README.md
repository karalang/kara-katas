# 2390. Removing Stars From a String

You are given a string `s`, which contains stars `*`.

In one operation, you can:

- Choose a star in `s`.
- Remove the closest **non-star** character to its **left**, as well
  as remove the star itself.

Return *the string after **all** stars have been removed*.

**Note:** The input will be generated such that the operation is
always possible, and it can be shown that the resulting string will
always be unique.

```
s = "leet**cod*e"  ->  "lecoe"
s = "erase*****"   ->  ""
```

**Constraints:** `1 <= s.length <= 10^5`; `s` consists of lowercase
English letters and stars `*`; the operation above can be performed on
`s`.

The closest letter to a star's left that is still there is the last
one kept so far, so the letters kept make a stack: a letter is pushed,
a star pops.

## Approaches

| file | mechanism |
|---|---|
| `stars.kara` ★ | a stack of bytes: a letter pushed, a star popping the top. O(n) |
| `stars_back.kara` | from the right: each star adds to a count of letters owed, a letter is dropped while one is owed, and the kept letters are reversed. O(n) |
| `stars_write.kara` | in place, two pointers: each letter written back at the answer's length so far, a star moving that index back one, the bytes cut to it at the end. O(n), no second buffer |
| `stars_string.kara` | the answer as a `String` that is its own stack, `push` and `pop` by `char`. O(n) |
| `stars_iter.kara` | iterators: the bytes `fold`ed into a stack. O(n) |
| `stars_solution.kara` | LeetCode's Rust template: a `Vec<char>` stack from `Vec::with_capacity`, each char `match`ed, `collect`ed with a turbofish; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; a star
taking the first letter, stars in a row, no stars; `10^5` characters
with a star a third of the time, and with a star half the time, as
checksums and lengths; then 3000 random strings of 1 to 30 characters,
with a checksum, the total length left, and how many come back empty.
Each answer is printed in brackets, so an empty one shows. `stars.py`
mirrors the ★ arm and its output is byte-identical, and the mirror was
checked on 20000 random strings of up to 14 characters against the
statement done step by step.

`stars_write.kara` first had `let mut b = s.bytes();`: `bytes()` is a
read-only `Slice[u8]`, so `check` reported the write through it and the
missing `truncate`, with a hint to copy with `.to_vec()`, and `karac
fix` applied that one edit, which cleared both.

`check` first reports 4 errors on the template, and `karac fix` carries
it in one call, reporting 5 edits: `struct Solution;` given its braces;
`Vec<char>` its brackets; `Vec::with_capacity` written with a dot; and
the turbofish of `collect::<String>()` dropped, the return type saying
what is collected. The `match` on a `char`, the `pop` in a block arm and
`into_iter().collect()` into a `String` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: while a star is left, the last one is chosen, and it and the
closest letter to its left are deleted from the string. No stack. It
checks 300 random strings of 1 to 30 characters, which the literal
reading answers; then 30 of up to 2000; then 30 made of runs, letters
and then stars, where whole runs vanish. All 360 are drawn before any
arm answers.

| | property |
|---|---|
| P1 | up to 30 characters, the answer is the literal reading's |
| P2 | the answer's length is the letters less the stars |
| P3 | the answer is the input's letters with some left out, in order |
| P4 | any prefix answered first, then the rest after it: the same answer |
| P5 | every letter shifted one along the alphabet: the answer shifted |
| P6 | each arm agrees with at least three of the other five |

The literal reading takes the last star where every arm takes the
first, which the statement's note says cannot matter. P4 holds because
what a prefix leaves is all the rest can see of it, and P5 because no
arm looks at which letter it moves.

The differential prints `360 cases: checksum 987674470, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and deletes star by star. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: the first character skipped | P1 122, P2 138, P4 186, P6 138 |
| M5 | ★: the answer reversed | P1 191, P3 210, P4 159, P6 221 |
| M6 | ★: a star taking the bottom letter | P1 168, P6 197 |
| M7 | back: a debt never paid | P1 168, P2 197, P6 197 |
| M10 | back: a letter kept while one is owed | P1 282, P2 328, P4 205, P6 328 |
| M11 | back: the last character skipped | P1 314, P2 360, P4 262, P6 360 |
| M14 | write: the bytes never cut | P1 282, P2 328, P3 328, P4 134, P6 328 |
| M15 | write: a letter never moved | P1 213, P3 173, P4 177, P6 250 |
| M16 | write: a star at length one written | P1 192, P2 222, P3 222, P6 222 |
| M17 | string: a star doing nothing | P1 282, P2 328, P6 328 |
| M18 | string: a star pushed in place of a pop | P1 282, P2 328, P3 328, P6 328 |
| M19 | string: an a taken for the star | P1 288, P2 331, P3 328, P5 191, P6 334 |
| M23 | iter: every letter pushed twice | P1 314, P2 360, P3 320, P4 333, P6 360 |
| M24 | iter: the bytes folded right to left | P1 297, P2 188, P3 256, P4 257, P6 343 |
| M25 | iter: the test turned around | P1 314, P2 343, P3 188, P6 360 |
| M27 | solution: a star leaving an x behind | P1 282, P2 328, P3 326, P5 328, P6 328 |
| M29 | solution: each letter put at the front | P1 204, P3 206, P4 117, P6 234 |

P1 and P6 kill all seventeen, P2 thirteen, P3 eleven, P4 nine and P5
two. P5, the letters shifted, fails only the two edits that single out
one letter, an `a` taken for the star (M19) and a star leaving an `x`
(M27). P4, a prefix answered first, fails the edits that treat an end
of the string unlike the rest, as the first or last character skipped
(M4, M11), the answer reversed (M5), the bytes never cut (M14) and the
fold run right to left (M24). P2, the length, passes the edits that
leave the right number of letters in the wrong places: the answer
reversed (M5), a star taking the bottom letter (M6), a letter never
moved (M15) and each letter put at the front (M29).

Of the thirty-one, fourteen were not kept, each failing exactly as a
kept one. A star doing nothing in the ★, write and iter arms (M1, M12,
M22) fails as the string arm's (M17); the ★ arm's star kept as a letter
(M2) as the string arm's star pushed in place of a pop (M18); a star
taking two letters in the ★ and string arms, a star owing two and a
star clearing the answer (M3, M20, M9, M13) as the back arm's debt
never paid (M7); the back arm's kept letters not reversed and the
template's stack collected backwards (M8, M30) as the ★ arm's answer
reversed (M5); the string arm's characters right to left (M21) as the
iter arm's fold right to left (M24); the iter arm's last character left
out (M26) as the back arm's (M11); and the template's `a` matched for
the star and first character skipped (M28, M31) as the string arm's
(M19) and the ★ arm's (M4). The template's first edit, a star doing
nothing, failed as M17 did and was replaced by the star leaving an `x`
(M27).

## Verification

Every arm prints the same output as `stars.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.6 to 1.0 s, and the
differential 1.8 s there and 0.44 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 20 strings of `10^5` characters, a star a third of the
time, once from the harness's generator, then makes 100 passes,
answering every string and folding each letter left, and the length
plus the pass, into the checksum, with the ★ arm in all five languages.
Every implementation prints `100 passes over 20 strings of 10^5
characters: checksum 48371874`. Every implementation allocates a fresh
stack in each call and grows it as it goes, except C's, which allocates
the input's length once.

BENCHTAB
