# 1021. Remove Outermost Parentheses

A valid parentheses string is empty, `"(" + A + ")"` or `A + B` for
valid strings `A` and `B`. It is primitive when it is not empty and
cannot be split as `A + B` with both non-empty. Every valid string `s`
splits into primitives `P1 + P2 + ... + Pk` in exactly one way. Return
`s` with the outermost pair of brackets of every primitive removed.

```
s = "(()())(())"          ->  "()()()"        ("(()())" + "(())")
s = "(()())(())(()(()))"  ->  "()()()()(())"
s = "()()"                ->  ""
```

**Constraints:** `1 <= s.length <= 10^5`, each character is `'('` or
`')'`, and `s` is valid.

## Approaches

A primitive ends exactly where the depth of nesting first comes back to
0, so its outermost brackets are the open brackets met at depth 0 and
the close brackets that bring the depth back to 0.

| file | mechanism |
|---|---|
| `remove_outer.kara` ★ | a depth counter: walk the characters keeping the depth, and write each bracket out unless it opens at depth 0 or closes back to it. O(n) |
| `remove_outer_split.kara` | cutting out primitives: walk the bytes, and where the depth comes back to 0 append the slice `s[start + 1..i]` between the primitive's first and last bracket in one piece. O(n) |
| `remove_outer_match.kara` | matching brackets: pair every bracket with its match using a stack of open brackets, then jump from primitive to primitive, each starting at `i` and ending at its match `j`, keeping `i + 1` to `j - 1`. O(n) |
| `remove_outer_recursive.kara` | recursive descent: parse the string as the grammar it is, a sequence of groups each made of an open bracket, a sequence of groups and a close bracket, writing a group's brackets only below the top level. O(n), recursion as deep as the nesting |
| `remove_outer_iter.kara` | a depth profile: work out the depth just inside each bracket, zip the characters with their depths and keep those deeper than 1 with an iterator filter collected into a `String`. O(n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 15 lines: the answers for eight strings,
LeetCode's three examples among them; for six groups of random valid
strings (5 to 2,000 pairs, opening with probability 2/8 to 7/8 wherever
both an open and a close are allowed), the characters kept, the
primitives removed and a checksum of the answers; and the answers for
one primitive nested 3,000 deep and 3,000 primitives side by side.
`remove_outer.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: the first primitive is the shortest non-empty prefix
that is valid, checked from scratch for each length; drop its first and
last bracket and go on with the rest. It checks 3,160 strings: every
valid string of 1 to 8 pairs (2,055), 1,000 random strings of 9 to 40
pairs, 100 of 41 to 300 and 5 of 1,000, opening with probability 2/8 to
7/8. Each string is also asked with the next string after it, inside
one and two more pairs, and mirrored: read right to left with each
bracket turned round.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the answer is valid, and two brackets shorter than `s` for each primitive, counted as the places the depth comes back to 0 |
| P3 | two strings one after the other answer the two answers one after the other |
| P4 | inside one more pair the answer is `s` itself, and inside two it is `"(" + s + ")"` |
| P5 | the mirror image of `s` answers the mirror image of the answer |
| P6 | each arm agrees with at least two of the other four |

The differential prints `3160 strings: checksum 627608670, 94800 checks
over 5 arms: 0 failures` under `karac __mir-run` (18 s) and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Thirty-six edits to the differential, each run under `karac __mir-run`
and `karac __mir-llvm-run`; fifteen are kept, three to each arm, all
fifteen are killed, each fails the same checks under both, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every open bracket kept | P1 3160, P2 3160, P4 3160, P5 3160, P6 3160 |
| M2 | ★: open brackets at depth 1 dropped too | P1 3151, P2 3151, P4 3160, P5 3151, P6 3151 |
| M3 | ★: a close bracket counted twice | P1 3151, P2 3151, P3 2548, P4 3160, P5 2963, P6 3151 |
| M4 | split: the next start one early | P1 2120, P2 2120, P3 3160, P5 2120, P6 2120 |
| M5 | split: a primitive cut at depth 1 | string slice bounds panic, exit 101 |
| M6 | split: the last character never read | P1 2323, P2 2323, P3 2323, P4 3160, P5 1743, P6 2323 |
| M7 | match: each primitive's inside written backwards | P1 3151, P2 3151, P4 3160, P6 3151 |
| M8 | match: the brackets the wrong way round | `unwrap()` on `None` panic, exit 101 |
| M9 | match: the first primitive skipped | P1 2074, P2 2074, P3 2074, P4 3160, P5 1743, P6 2074 |
| M10 | recursive: a group taken to end one character late | index out of bounds panic, exit 101 |
| M11 | recursive: only a group's first child read | P1 2821, P2 2821, P4 3129, P5 1988, P6 2821 |
| M12 | recursive: starting at the third character | P1 2074, P2 2074, P3 2074, P4 3160, P5 2227, P6 2074 |
| M13 | iter: depth 1 kept | P1 3160, P2 3160, P4 3160, P6 3160 |
| M14 | iter: the depth never back to 0 | P1 2120, P2 2120, P3 3160, P5 2112, P6 2120 |
| M15 | iter: the depths read back to front | P1 1971, P2 1971, P3 2264, P6 1971 |

P1, P2 and P6 kill the twelve that finish, P4 and P5 nine each and P3
seven; M5, M8 and M10 are killed by their own bounds and `unwrap`
checks. Nine strings, `"()"` repeated one to eight times and one random
one, have nothing inside any primitive, so their answer is empty, and
the edits that go wrong wherever there is something inside fail on the
other 3,151. M4 and M14 go wrong only on the 2,120 strings of two or
more primitives, which every joined string of P3 is. M15 passes P4 and
P5: inside one or two more pairs only the outer brackets are at depth 1
read either way round, and a mirror image's depths are the original's
reversed, so it answers a string and its mirror alike. The checks draw
no random number that depends on an answer, so every mutant sees the
same strings and their counts can be compared.

Twenty-one other edits were tried and set aside. Two change no answer:
match pairing a close bracket with the bottom of the stack, since the
last close bracket of a primitive, the only one whose partner is read,
meets its own open bracket at the bottom; and match stopping two short
of the end, which skips only a last primitive of `"()"`, whose inside
is empty. Nineteen failed exactly the same checks as a kept one: six
keeping an outer bracket (★ testing a close bracket before the depth
drops, split keeping the first or last bracket, match keeping the open
or close one, recursive keeping the top open one), as M1; seven
writing or dropping the wrong inner brackets (★ writing a close bracket
as an open one and resetting the depth at every open bracket, recursive
dropping close brackets at depth 1 and writing them as open ones, iter
taking a close bracket's depth after it, an open one's before it, and
the depths one place out), as M2; three (recursive reading nested
groups at their parent's depth, iter dropping depth 2 and turning every
bracket round), as M7; recursive putting the top level at depth 1, as
M13; match skipping the last primitive, as M6; and split starting one
character late, which panics on its slice bounds, as M5.

## Verification

Every arm prints the same output as `remove_outer.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with
no error; the differential prints its line under all three. `karac
check --output=json` reports no diagnostic for the five arms, the
differential and the bench program, so `karac fix` had nothing to do.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. The release build is kara `56c60bdf7c`, with
runtime archives rebuilt at `ce706dd131`, the last commit before it to
change the runtime. Under `karac __mir-run` the arms take 1.2 s (split) to 5.3 s (iter).

The iter arm's filter reads its depth as `|(_, d)| d > 1`, though `d`
comes from `inside.iter()` and is a `ref i64`; `*d > 1` is accepted
too, and both run the same. No compiler gap turned up.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench builds 100 random valid strings of 1 to 50,000 pairs (up to
LeetCode's `10^5` characters, 5,512,438 in all), opening with
probability 2/8 to 6/8, once in all five languages, and runs the ★ arm
on each string 30 times, folding each answer's length and middle byte
into a sum and a checksum: 165 million characters read, each pushed
onto a growing string unless it is an outer bracket. Rust and Kāra walk
`chars()` and push each `char`, Go ranges over the string's runes into
a `strings.Builder`, and C walks the bytes into a buffer it doubles
with `realloc`. Every implementation prints `100 strings, 5512438
characters, 30 rounds: 126886020 kept, checksum 546331738`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.748 to 0.828 s | 0.774 s |
| Rust (`rustc -O`) | 0.645 to 0.758 s | 0.684 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.765 to 0.844 s | 0.792 s |
| Go | 1.265 to 1.396 s | 1.297 s |
| Python | 11.0 s | |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.876 to 0.925 s | 0.911 s |
| Kāra (`karac build`) | 0.849 to 1.008 s | 0.899 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(its user time stays below its real time) and runs as fast as the
sequential one.

v2 took 1.15 times Rust's median time under overflow checks and 1.18
times C's. Rust's own overflow checks cost it 16% here; we did not
measure where Kāra's gap goes.
