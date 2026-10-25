# 1003. Check If Word Is Valid After Substitutions

Given a string `s`, determine if it is **valid**.

A string `s` is **valid** if, starting with an empty string `t = ""`,
you can **transform** `t` **into** `s` after performing the following
operation **any number of times**:

- Insert string `"abc"` into any position in `t`. More formally, `t`
  becomes `tleft + "abc" + tright`, where `t == tleft + tright`. Note
  that `tleft` and `tright` may be **empty**.

Return `true` *if* `s` *is a **valid** string, otherwise, return*
`false`.

```
s = "aabcbc"        ->  true
s = "abcabcababcc"  ->  true
s = "abccba"        ->  false
```

**Constraints:** `1 <= s.length <= 2 * 10^4`; `s` consists of letters
`'a'`, `'b'`, and `'c'`.

## Approaches

The last `"abc"` put in is still whole in `s`, so it can be taken out,
and what is left must be valid in turn; taking out any whole `"abc"`
leaves a valid string valid and an invalid one invalid. So `s` is valid
exactly when taking out whole `"abc"`s, in any order, ends at the empty
string. Three arms take them out, by a stack or by rounds of
replacement; two read `s` as pieces begun and finished, one by the
letter each piece waits for and one by a grammar.

| file | mechanism |
|---|---|
| `is_valid.kara` ★ | a stack: `s` read left to right onto a stack, and an `"abc"` on top taken off as soon as its `c` arrives; valid when nothing is left. O(n) |
| `is_valid_replace.kara` | rounds of replacement: every `"abc"` taken out at once, again and again while that changes anything; valid when the empty string is left. O(n²) at worst |
| `is_valid_pieces.kara` | pieces waiting for their next letter: an `a` begins a piece waiting for `b`, a `b` must find the top piece waiting for it, which then waits for `c`, and a `c` must find the top piece waiting for it, which is finished; valid when every letter finds its piece and none is left. O(n) |
| `is_valid_grammar.kara` | a grammar: a valid string is a sequence of pieces `a V b V c`, each `V` valid itself, parsed from the front by recursive descent; valid when the parse takes all of `s`. O(n), with recursion as deep as the nesting |
| `is_valid_inplace.kara` | the stack in place: a write place runs behind the read place in `s`'s own letters, each letter is copied down to it, and the write place steps back over an `"abc"` just below it; valid when it ends at 0. O(n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 18 lines. The first ten are LeetCode's three
examples and seven more: `"abc"` itself; one letter; `"abc"` reversed;
each letter twice in turn, which is not valid; two pieces, the second
put in the middle of the first; three pieces in a row; and `"abacbc"`,
which has as many of each letter in every prefix as a valid string
needs and still is not valid. Then four strings of LeetCode's longest
size, 19,998 letters: `"abc"` 6,666 times; 6,666 `a`s and then `"bc"`
6,666 times, each piece put inside the one before, as deep as the
nesting goes; the same less its last `c`; and 6,666 of each letter in
turn. Then totals over random strings, each made of pieces put in at
random places and, half of the time, spoiled by one random edit, a
letter changed, two neighbours swapped, a letter dropped or one added:
300 strings of up to 4 pieces, 3,000 of up to 20, 300 of up to 200 and
3 of up to 6,666. `is_valid.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every string `t` can become by putting `"abc"` in at
any place, any number of times, starting from the empty string, made up
to 15 letters, and `s` is valid when it is one of them. It checks 3,200
random strings: 3,000 against the statement, half made as the arms'
random strings are from up to 5 pieces and half any 1 to 12 of the
three letters, and 200 made from up to 200 pieces against the other
properties.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 strings |
| P2 | `"abc"` put in at a random place gives the same answer |
| P3 | `s` between two random valid strings gives the same answer |
| P4 | `s` reversed, with `a` and `c` swapped, gives the same answer |
| P5 | valid only when every prefix has at least as many `a` as `b` and `b` as `c`, and the whole as many of each |
| P6 | each arm agrees with at least two of the other four |

P2 and P3 hold because a whole `"abc"` can always be taken out again,
and P4 because reversing `"abc"` and swapping `a` with `c` gives
`"abc"` back, so every way of building `s` turns into a way of building
the other. P5's counts are needed, not enough: `"abacbc"` meets them.

It prints `3200 strings of 85818 letters: 918 valid, checksum
59313530, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (6.2 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-five edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the `a` not checked | P1 62, P4 163, P5 69, P6 69 |
| M2 | ★: two letters taken off, not three | P1 809, P6 918 |
| M3 | ★: up to two letters may be left | P1 485, P5 496, P6 496 |
| M4 | replace: one round only | P1 520, P2 156, P3 230, P6 628 |
| M5 | replace: `"cba"` taken out, not `"abc"` | P1 812, P2 3, P3 3, P5 3, P6 921 |
| M6 | replace: any length of 3 left over valid | P1 804, P5 778, P6 847 |
| M7 | pieces: an `a` waits for `c` | P1 836, P2 27, P3 27, P5 27, P6 945 |
| M8 | pieces: a `b` finishes its piece | P1 840, P2 31, P3 31, P4 55, P5 31, P6 949 |
| M9 | pieces: the letter waited for not checked | P1 193, P5 162, P6 231 |
| M10 | grammar: the `b` not checked | P1 40, P4 82, P5 42, P6 42 |
| M11 | grammar: nothing between `b` and `c` | P1 342, P2 119, P3 255, P4 361, P6 450 |
| M12 | grammar: one piece in a sequence at most | P1 518, P2 158, P3 293, P6 625 |
| M13 | inplace: the letter never copied down | P1 462, P2 277, P3 972, P4 440, P5 97, P6 551 |
| M14 | inplace: any letter but `c` taken as the `a` | P1 39, P4 98, P5 43, P6 43 |
| M15 | inplace: the first letter skipped | P1 973, P2 60, P3 164, P4 69, P5 164, P6 1082 |

P1 and P6 kill all fifteen, P5 eleven, P2 and P3 eight each and P4
seven. The checks draw no random number that depends on an answer, so
every mutant sees the same strings and their counts can be compared:
809 of the 3,000 small strings are valid, 918 of all 3,200, and M2,
which never empties its stack and so answers false for every string,
fails exactly those. An answer of false is never refuted by P2 to P5:
putting in or around a whole piece, or turning the string round,
leaves an invalid string invalid, and P5 asks only of a true answer.
So P2 to P5 see the edits that call some invalid string valid, or that
are right on a string and wrong once it grows.

P5 sees eleven that accept a string whose letters cannot balance: M1,
M10 and M14, which let another letter stand in for the one they do not
check; M3 and M6, which forgive what is left over; M9, which takes any
letter as the one awaited; M5, M7 and M8, which accept wrong pieces;
M13, which compares letters it never wrote; and M15, which accepts any
letter put in front of a valid string. P2 and P3 see the edits that go
wrong as pieces are added: M4, which needs one round for each level of
nesting; M11 and M12, which allow no piece between `b` and `c`, or none
after the first in a row; and M5, M7, M8, M13 and M15. P4 turns `s`
round and swaps `a` with `c`, so it sees edits that treat the two ends
of a piece differently: M1, M10 and M14, which check one end and not the
other; M15, which skips the first letter but not the last; and M8, M11
and M13.

Ten other edits were tried and set aside. Four failed exactly the same
checks as a kept one: ★ never taking off an `"abc"` at the bottom of
the stack, pieces never finishing a piece at its `c`, and inplace
stepping back over two letters, which all answer false for every
string, as M2; and inplace allowing up to two letters left, as M3. Six
were sound but beyond three an arm: ★ taking off `"acb"`; replace
taking out `"bc"`, and stopping once a round takes out one piece;
pieces allowing pieces left over; and grammar allowing nothing between
`a` and `b`, and taking a valid start for the whole. None survived and
none crashed.

## Verification

Every arm prints the same output as `is_valid.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `af85e1ac8d`, after the
pattern rule of B-2026-10-24-36, which made the harness drop a `*` on
the numbers it reads out of a tuple, and the runtime archives were
rebuilt at the same commit. The mutants' `karac __mir-run` lane ran on
the build before, at `395f71ae05`, whose checks of the differential
are the same; their `karac __mir-llvm-run` lane was run again on the
new build and gave the same verdicts. Under `karac __mir-run` the arms
take 1.4 s (replace) to 2.2 s (★), and the differential 6.2 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. The program draws 20
strings of 6,666 pieces, 19,998 letters, LeetCode's longest, once, each
written left to right by a random walk that either begins a new piece
with its `a` or writes the next letter of the latest piece begun; the
odd ones then have one letter changed, which makes them invalid. In
each of 250 rounds it runs the arm on every string, each round
starting from a different one, and folds every answer into a checksum.
Every implementation prints `250 rounds over 20 strings of 19998
letters: 2500 valid, checksum 12715072`. Each call allocates its stack
once and reads all 19,998 letters; Go's stack is a byte slice and C's a
`malloc`'d byte array.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `af85e1ac8d`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.405 to 0.546 s | 0.440 s |
| Rust (`rustc -O`) | 0.483 to 0.625 s | 0.533 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.498 to 0.608 s | 0.529 s |
| Go | 0.595 to 0.636 s | 0.616 s |
| Python | 19.4 s | |
| Kāra (`karac build --mir`) | 0.572 to 0.730 s | 0.629 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 31 times
Kāra's.

v2 took 1.19 times Rust's median time under overflow checks and 1.43
times C's. Under valgrind's cachegrind v2 ran 3,225 million
instructions and 1,163 million branches with 40.5 million
mispredicted, Rust with overflow checks 2,082 million, 621 million and
62.9 million, and C 1,477 million, 375 million and 43.0 million. Over
the 100 million letters the calls read that is about 32 instructions
and 12 branches a letter for v2, 21 and 6 for Rust, and 15 and 4 for C.
All three mispredict about once every two or three letters, which fits
the test for an `"abc"` on top, whose outcome follows the random
letters (inferred); v2 mispredicts less than Rust and runs nearly
twice its branches, and where those go was not traced.
