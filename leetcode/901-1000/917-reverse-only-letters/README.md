# 917. Reverse Only Letters

Given a string `s`, reverse the string according to the following
rules:

- All the characters that are not English letters remain in the same
  position.
- All the English letters (lowercase or uppercase) should be reversed.

Return `s` after reversing it.

```
s = "ab-cd"                 ->  "dc-ba"
s = "a-bC-dEf-ghIj"         ->  "j-Ih-gfE-dCba"
s = "Test1ng-Leet=code-Q!"  ->  "Qedo1ct-eeLg=ntse-T!"
```

**Constraints:** `1 <= s.length <= 100`, `s` consists of characters
with ASCII values in the range `[33, 122]`, and `s` does not contain
`'\"'` or `'\\'`.

## Approaches

| file | mechanism |
|---|---|
| `reverse_only_letters.kara` ★ | two pointers over a copy of the bytes, one from each end; each skips a non-letter, and when both rest on letters they swap and step inward. O(n) |
| `reverse_only_letters_stack.kara` | every letter pushed on a stack, then the answer built from the front over `s.chars()`: a letter is replaced by what the stack pops, anything else copied through. Letters tested with `char.is_ascii_alphabetic()`. O(n) |
| `reverse_only_letters_positions.kara` | the positions holding letters collected in order; the letter at the t-th position goes to the (k-1-t)-th, written into a copy so that every letter is read from the original, and the copy turned back into a `String` with `String.from_utf8`. O(n) |
| `reverse_only_letters_backward.kara` | the answer built front to back while a second index walks from the end: a non-letter is copied as it stands, and a letter is taken from wherever the backward index next lands on one. O(n) |
| `reverse_only_letters_recursive.kara` | the two-pointer walk as a recursion on the window [i, j): a window narrower than two is done, a non-letter at either end is dropped, and two letters at the ends are swapped with `Vec.swap`. Depth at most n. O(n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's three examples and seven
more (no letters at all, one letter, one non-letter, a repeated letter,
two letters, a letter between brackets, and `a`, `z`, `A` and `Z`
among digits, three of the characters between `Z` and `a`, and `{`,
just past `z`); for 500 random strings of 1 to 100 characters,
from no letters to all letters, the letters counted (19,756) and a
checksum; and a checksum over 10,000 strings of the longest length,
100. `reverse_only_letters.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally, as a check on an answer rather than another way to build
one: `r` answers `s` when it is as long, each character of `s` that is
not an English letter stands at the same place in `r`, letters stand
where letters stood, and the letters of `r` read in order are the
letters of `s` read from the end. It checks 3,200 random strings: 3,000
of 1 to 8 characters from `a`, `z`, `A`, `Z` and the four characters
just outside the letter ranges (`@`, `[`, `` ` ``, `{`), against the
statement; and 200 of 1 to 100 characters from every allowed
character, from no letters to all letters, against the other
properties; 23,612 characters in all, 14,977 of them letters.

| | property |
|---|---|
| P1 | the statement, on the small strings |
| P2 | done twice, the string comes back unchanged |
| P3 | every letter's case swapped first swaps it in the answer |
| P4 | the string reversed first reverses the answer |
| P5 | a non-letter put in at a random place just stands there in the answer |
| P6 | each arm agrees with at least two of the other four |

P4 holds because reversing `s` puts its non-letters at the mirrored
places and lists its letters backwards, and reversing the answer does
exactly the same to it. It prints `3200 strings, 23612 characters,
14977 letters, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (4.5 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: z not taken for a letter | P1 935, P3 1347, P6 1033 |
| M2 | ★: the back pointer left in place after a swap | P1 959, P2 1339, P4 1339, P6 1153 |
| M3 | ★: A not taken for a letter | P1 886, P3 1320, P6 984 |
| M4 | stack: letters copied through, never popped | P1 1573, P6 1771 |
| M5 | stack: digits pushed with the letters | P2 148, P4 153, P5 554, P6 148 |
| M6 | stack: only lowercase letters popped into place | P1 1517, P2 1156, P3 1856, P4 1465, P6 1714 |
| M7 | positions: letters read from the copy being written | P1 1573, P2 1771, P4 1771, P6 1771 |
| M8 | positions: the letters rotated by one place, not reversed | P1 1690, P4 1339, P6 1888 |
| M9 | positions: the first character never a letter | P1 1001, P4 1473, P5 185, P6 1156 |
| M10 | backward: an a copied through, the reader not moved | P1 1025, P2 811, P3 1648, P4 1081, P6 1119 |
| M11 | backward: the reader stopping on `{` | P1 841, P2 841, P4 1141, P6 841 |
| M12 | backward: the character at the mirrored place taken | P1 1972, P2 2157, P5 2281, P6 2157 |
| M13 | recursive: a window two wide taken as done | P1 520, P5 98, P6 597 |
| M14 | recursive: a non-letter at the front skips the next character too | P1 609, P4 1102, P5 683, P6 775 |
| M15 | recursive: a non-letter at the back also drops the front | P1 816, P4 1305, P5 387, P6 977 |

P6 kills all fifteen and P1 fourteen; P4 ten, P2 seven, P5 six and P3
four. M5 is the one P1 misses: the small strings hold no digits, so
only the large ones, over every allowed character, find it. P3 kills
only the mutants that treat the two cases differently (M1, M3, M6,
M10). M4 leaves the string unchanged, which P2, P4 and P5 all accept,
since doing nothing twice, to a reversed string or around an inserted
character still does nothing; the statement and the other arms catch
it.

The small alphabet first used `a`, `b`, `Y` and `Z` as its letters;
then P1 could not see M1 or M3 (P3 1018 and 1000, P6 98 each), because
neither `z` nor `A` ever appeared. With the letters at both ends of both
ranges it kills them. Two mutants were replaced because each failed
exactly the same checks as another, so told nothing new: the first M8,
writing only the first half of the positions, leaves the second half's
letters where they were, which is what M7's reading back from the copy
produces too; and the first M14, keeping the back end after a swap,
is M2's mistake made in the same walk.

## Verification

Every arm prints the same output as `reverse_only_letters.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 3.0 to 6.3 s
each (the stack arm over `chars()` the longest) and the differential
4.5 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The stack, positions, backward and recursive arms print the same output
under the frozen legacy interpreter, the legacy JIT and both legacy
builds, with and without auto-par. Legacy refuses the ★ arm, the
differential and the bench program at the `*b` on an element of a
`Vec[u8]`'s `.iter()` ("unary '*' requires 'ref T', ... found 'u8'"),
legacy's older rule; under v2 the element is a reference and the `*` is
required. Legacy is frozen, so none of this is filed.

## Benchmarks

The bench program uses the ★ arm on a pool of 1,000 strings of 100
characters, the c-th with c mod 101 in 100 of its characters letters,
built once. Each of 1,000 rounds reverses the letters of every string
in the pool and folds the answer's first and last characters into a
checksum; a million calls in all. Every implementation prints `1000
rounds over 1000 strings of 100: checksum 352888577`. Each copies the
bytes, swaps them in place and builds a new string a byte at a time,
as the ★ arm does: C into a `malloc`ed buffer, Rust by `String::push`,
Go with a `strings.Builder`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.25 to 0.29 s | 0.28 s |
| Rust (`rustc -O`) | 0.42 to 0.48 s | 0.44 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.41 to 0.50 s | 0.46 s |
| Go | 1.05 to 1.21 s | 1.09 s |
| Python | 17.4 s | |
| Kāra (`karac build --mir`) | 0.51 to 0.55 s | 0.53 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification).

v2 takes 1.15 times Rust's median time under overflow checks and 1.91
times C's. Under valgrind's cachegrind v2 runs 4.99 billion instructions
and 1.10 billion branches, against 4.41 billion and 0.80 billion for
Rust with overflow checks and 1.39 billion and 0.24 billion for C. Rust
and Kāra build the answer by pushing one byte at a time onto a growable
string, while C writes into a buffer of the right size; that is the
likely cause of most of the gap to C, but it was not profiled. Go takes
3.9 times C's time; why was not profiled either.
