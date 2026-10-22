# 848. Shifting Letters

You are given a string `s` of lowercase English letters and an integer
array `shifts` of the same length. Shifting a letter moves it to the
next letter of the alphabet, `'z'` wrapping round to `'a'`. For each
`shifts[i] = x`, shift the first `i + 1` letters of `s` `x` times.
Return the string after all the shifts.

```
s = "abc", shifts = [3,5,9]  ->  "rpl"
s = "aaa", shifts = [1,2,3]  ->  "gfd"
```

**Constraints:** `1 <= s.length <= 10^5`, `s` is lowercase English
letters, `shifts.length == s.length`, `0 <= shifts[i] <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `shifting_letters.kara` ★ | suffix sums from the back: letter `i` is shifted by the sum of the shifts from `i` to the end, so walking from the back keeps that sum as it grows, reduced mod 26, and shifts each byte of a copy of the string by it. O(n) |
| `shifting_letters_prefix.kara` | the total less a running prefix, from the front: sum every shift once, mod 26, then walk the characters taking off each shift once its letter is passed, pushing each shifted letter onto a new `String`. O(n) |
| `shifting_letters_iter.kara` | a table of suffix sums mod 26 filled from the back, then one chain, `s.chars().enumerate().map(...).collect()`, that maps each letter and its position to the shifted letter. O(n) time and space |
| `shifting_letters_wide.kara` | whole sums, reduced only at the end: a letter's whole shift is at most 10^5 * 10^9 = 10^14, well inside an `i64`, so the sum from the back is kept unreduced and taken mod 26 only when a letter is shifted, the letters pushed back to front and reversed. O(n) |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 16 lines: LeetCode's two examples; ten more
(`'z'` wrapping, shifts of 0, 25 and 26 on one letter, the wrap at the
second letter, the whole alphabet shifted once from every position, all
shifts 10^9, no shift at all, and multiples of 26); three strings of
LeetCode's longest, 10^5 random letters, with every shift 10^9, every
shift 1, and random shifts, each with its first twelve letters and a
digest; and 500 random strings of up to 30 letters, with a checksum.
`shifting_letters.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: for each `i` in turn, each of the first `i + 1` letters is
moved one letter at a time, `'z'` to `'a'`, `shifts[i] % 26` times, as
26 moves bring a letter back to itself. Its 1,600 cases of up to 30
letters come in four kinds of 400, letters from `x` to `z`, where every
shift wraps soon, or any letters, with shifts below 30, then shifts near
multiples of 26 (one less, equal or one more), and then shifts up to
10^9, with letters from `x` to `z` and any letters in turn.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | a letter appended with a shift of 0 is appended unchanged and changes nothing before it |
| P3 | 26, 52 or 78 added to each shift gives the same answer |
| P4 | every letter of `s` moved on one gives every letter of the answer moved on one |
| P5 | the string and shifts from any position to the end give the answer from that position |

It prints `1600 cases, 32000 checks over 4 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the shifts summed from the front | P1 1535, P2 1489, P5 1257 |
| M2 | ★: the sum reduced mod 25 | P1 1562, P3 1600 |
| M3 | ★: every letter one step short | P1 1600, P2 1600 |
| M4 | prefix: the total started at 1 | P1 1600, P2 1600 |
| M5 | prefix: the first shift taken off at every letter | P1 1475, P2 1464, P5 1307 |
| M6 | prefix: the running total wrapped mod 27 | P1 1506, P2 1516, P5 1287 |
| M7 | iter: the table filled from the front | P1 1527 |
| M8 | iter: each letter given the next letter's sum | P1 1584 |
| M9 | iter: the table seeded with 1 | P1 1600, P2 1600 |
| M10 | wide: the letters left back to front | P1 1522, P2 1598, P5 1356 |
| M11 | wide: the total reset at each letter | P1 1527 |
| M12 | wide: the first letter left out | P1 1600 |

P1 kills all twelve. P2 sees the edits that change a letter shifted by
nothing, the appended one (M3, M4, M9), or that make the answer depend
on what comes after a letter or before it (M1, M5, M6, M10); P5 sees
those last again, since cutting off the front changes what is before
each letter and which shifts come first. M7, M8 and M11 shift a letter
by its own shift alone, or by the next letter's sum, so the appended
letter, shifted by nothing, still matches. P3 sees only M2, the one edit
whose sum is not taken mod 26.

P4 kills nothing, and cannot here: every arm, and every edit, moves
every letter by an amount that does not depend on the letter.

One first draft was replaced: the ★ arm with its wrap past `'z'` left
out made bytes that are not letters, and `String.from_utf8` refused
them, so the run stopped at its `unwrap()` rather than failing a
property.

## Verification

Every arm prints the same output as `shifting_letters.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its lines under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `7fb33738c5`, and the runtime archives are
current with them. Under `karac __mir-run` the arms take 1.7 to 4.0 s
and the differential 3.9 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends refuse every arm and the differential at a
`*b`, `*x` or `*c` read through `.iter()`, in the arm or in the
harness's digest: legacy types the loop variable as the element, not a
reference, though `karac check` accepts it on v2. Legacy refuses the
bench program as moving a string out of an index, which v2's borrowing
parameters do not do. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
cases once, each of LeetCode's longest strings, 10^5 random letters,
with shifts up to 10^9. Each of 2,000 rounds shifts the next case into a
new string and keeps three of its letters. Every implementation prints
`2000 rounds of 64 strings: checksum 454784322`, the Kāra program under
`karac __mir-run` included, in 339 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.20 to 1.32 s |
| Rust (`rustc -O`) | 1.09 to 1.14 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.11 to 1.22 s |
| Go | 0.98 to 1.10 s |
| Python | 20.0 to 20.1 s |
| Kāra (`karac build --mir`) | 1.09 to 1.17 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 1.13 s, against Rust's
1.13 (1.15 under overflow checks), C's 1.25 and Go's 1.07: 0.98 times
Rust's time under overflow checks, 0.90 times C's and 1.06 times Go's.
Under valgrind's cachegrind C runs 6.15 billion instructions, Rust 5.51
billion and v2 6.93 billion, with 407 million, 441 million and 876
million branches, and none of the three mispredicts more than 32
thousand of them. Each letter costs two remainders by 26, and most
likely those divisions, which take the same time in every language, are
where the time goes and what evens the five out (not traced). Built for
`x86-64-v3`, the target `karac build` uses, C takes 1.20 to 1.27 s and
Rust with overflow checks 1.19 to 1.24 s, against v2's 1.15 to 1.22 s in
the same five interleaved runs. Python takes 20.1 s, about 16 times C's
time. The comparison with C and Rust waits until after M4.
