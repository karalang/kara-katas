# 925. Long Pressed Name

Your friend is typing his `name` into a keyboard. Sometimes, when typing
a character `c`, the key might get long pressed, and the character will
be typed 1 or more times.

You examine the `typed` characters of the keyboard. Return `True` if it
is possible that it was your friend's name, with some characters
(possibly none) being long pressed.

```
name = "alex",  typed = "aaleex"   ->  true    ('a' and 'e' were long pressed)
name = "saeed", typed = "ssaaedd"  ->  false   ('e' must have been pressed twice, but it was not in the typed output)
```

**Constraints:** `1 <= name.length, typed.length <= 1000`; `name` and
`typed` consist of only lowercase English letters.

## Approaches

Split both strings into runs of one letter: `typed` comes from `name`
exactly when the runs have the same letters in the same order and each
run of `typed` is at least as long as its run of `name`.

| file | mechanism |
|---|---|
| `is_long_pressed_name.kara` ★ | two pointers: walking `typed`, a character that is `name`'s next moves both pointers, one that repeats the typed character before it is a long press and is skipped, and anything else fails; at the end all of `name` must be used. O(n + m), O(1) extra space |
| `is_long_pressed_name_runs.kara` | both strings encoded as a `Vec` of `Run` structs, a letter and a length, then compared run for run. O(n + m), O(n + m) space |
| `is_long_pressed_name_groups.kara` | the runs measured side by side, a group of equal letters from each string at a time, without storing them. O(n + m), O(1) extra space |
| `is_long_pressed_name_dp.kara` | `ok[i][j]` says whether the first `j` typed characters can come from the first `i` of `name`: the last one is either `name[i - 1]` typed once more or a long press of it, and must match it; two rows. O(n * m) time, O(m) space |
| `is_long_pressed_name_backward.kara` | the ★ arm's two pointers run from the right, since reversing both strings keeps a long press a long press. O(n + m) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's two examples and nine
more (typed exactly, one letter held, a letter missing, a letter added at
the end, a wrong letter, repeated groups, an extra letter after a held
one, a name with several held letters, and typed too short); for 300
random names of 1 to 200 letters from 2, 3 or 26 letters by turns, each
typed with some keys held down and perhaps mistyped once, how many are
long pressed (228) and a checksum; and four of LeetCode's largest, 1,000
letters: one letter against itself, "ab" 500 times against itself, 500
letters each typed twice, and the same the other way round.
`is_long_pressed_name.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: try every way of typing `name`, each character typed one or
more times, and say whether one of them is `typed`. It checks 3,200
random cases built as the harness builds them, typed with some keys
held down and then, three times in four, a character deleted, inserted
or changed: 3,000 names of 1 to 5 letters against the statement, and 200
of 1 to 150 letters against the other properties; 35,919 letters typed in
all, 1,714 of the cases long pressed.

| | property |
|---|---|
| P1 | the statement's answer, on the small cases |
| P2 | a name typed exactly is long pressed |
| P3 | the same answer with both strings reversed |
| P4 | the same answer with every character of both strings doubled |
| P5 | a long pressed name stays long pressed with one typed character pressed once more |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 cases, 35919 letters typed, 1714 long pressed, 95000
checks over 5 arms: 0 failures` under `karac __mir-run` (6 s) and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `name` not required to be typed to the end | P1 213, P3 298, P6 216 |
| M2 | ★: a long press allowed for the first typed character | P1 217, P3 243, P6 218 |
| M3 | ★: a long press tried before a match | P1 731, P2 1377, P4 876, P6 838 |
| M4 | runs: a typed run allowed to be one shorter | P1 110, P4 125, P6 125 |
| M5 | runs: the run lengths never compared | P1 110, P6 125 |
| M6 | runs: a letter matching the run before last added to the last run | P1 126, P3 143, P6 156 |
| M7 | groups: `typed` allowed to run on past `name` | P1 138, P3 384, P6 141 |
| M8 | groups: typed groups measured one short | P1 1283, P2 3200, P6 1397 |
| M9 | groups: `name` allowed to stop short | P1 143, P3 248, P6 146 |
| M10 | dp: no long press allowed | P1 1082, P5 518, P6 1196 |
| M11 | dp: a long press taken without comparing the characters | P1 436, P3 243, P6 476 |
| M12 | dp: the answer read one typed character short as well | P1 25, P3 243, P4 25, P5 6, P6 25 |
| M13 | backward: `name` not required to be typed to the start | P1 221, P3 298, P6 224 |
| M14 | backward: the last typed character allowed as a long press | P1 25, P3 243, P6 25 |
| M15 | backward: the first typed character never examined | P1 1155, P2 3200, P3 854, P4 218, P5 58, P6 1231 |

P1 and P6 kill all fifteen; P3 ten, P4 four, and P2 and P5 three each.
P3 sees the mistakes made at one end of the strings, which reversing
moves to the other end where the arm is right (M1, M2, M7, M9, M11 to
M15), and M6, whose mistake depends on which run comes first. P4 doubles every
run, so it sees the mistakes of one press (M4, M12) and those that turn
on a run of length 1 (M3, M15). P2 sees only the mutants that fail on a
name with no long press at all (M3, M8, M15), and P5 only those that
reject a long press (M10, M12, M15). M5 depends only on the runs'
letters, which reversing and doubling keep in step, so only the
statement and the other arms see it.

Eleven other edits were tried and set aside. Three are equivalent, since
the arm checks the same thing another way: ★ taking any repeat of the
last character of `name` matched as a long press (the typed character
before it is always that character), groups never comparing the letters
(a group of the wrong letter measures 0 and fails anyway), and backward
taking any character matching `name` after its pointer. One stopped at
runtime on an index out of bounds (runs not comparing the number of
runs). Five failed exactly the same checks as another: groups allowing a
longer group of `name`, as M4; dp letting a typed character stand for a
dropped one, as M5; backward trying a long press before a match, as M3;
groups measuring `name`'s groups one long, as M8; and groups allowing no
long press, as M10. The other two were sound but beyond three an arm.

## Verification

Every arm prints the same output as `is_long_pressed_name.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 0.3 to 2.8 s each (dp, which fills
a row for every letter of the name, the longest) and the differential
6 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy compiler refuses every arm and the differential at
the first `*` on an element of a `Vec[u8]`'s `.iter()`, in the harness's
`random_case` ("unary '*' requires 'ref T', ... found 'u8'"), legacy's
older rule; under v2 the element is a reference and the `*` is required.
Legacy refuses the bench program, which passes `names[p]` and
`typings[p]` straight to the function: "cannot move ... out of an
index", legacy's owned parameters, where v2's parameters borrow them.
Legacy is frozen, so none of this is filed.

## Benchmarks

The bench program builds 1,000 names of 400 letters from "abc" once,
each typed with about one key in four held down for up to three more
presses and every third one mistyped once, and in each of 150 rounds
runs the ★ arm on every pair, each round starting from a different one.
Every implementation prints `150 rounds over 1000 names of 400 letters:
118950 long pressed, checksum 810278901`. The Kāra arm copies both
strings' bytes into a `Vec[u8]` on every call, as it reads them by
index; C, Rust and Go read the strings in place.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.30 to 0.32 s | 0.31 s |
| Rust (`rustc -O`) | 0.30 to 0.33 s | 0.31 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.29 to 0.33 s | 0.32 s |
| Go | 0.29 to 0.32 s | 0.30 s |
| Python | 8.1 s | |
| Kāra (`karac build --mir`) | 0.29 to 0.31 s | 0.30 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about 26 times C's.

v2 takes 0.95 times Rust's median time under overflow checks and 0.99
times C's: the four compiled programs are within their run to run spread
of each other. Every typed letter is a branch on a random key, and under
valgrind's cachegrind all of them mispredict about one branch in ten:
v2 runs 1.00 billion instructions and 0.39 billion branches and
mispredicts 32.0 million, Rust with overflow checks 0.88 billion, 0.27
billion and 26.0 million, and C 1.09 billion, 0.27 billion and 28.7
million.
