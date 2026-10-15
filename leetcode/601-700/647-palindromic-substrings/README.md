# 647. Palindromic Substrings

Given a string `s`, return how many of its substrings are palindromes,
reading the same forwards and backwards. Substrings at different
positions count separately, even when their letters are the same.

```
s = "abc"  ->  3    "a", "b", "c"
s = "aaa"  ->  6    three "a", two "aa", one "aaa"
```

**Constraints:** `s` holds 1 to 1,000 lowercase English letters.

## Approaches

Every arm is `fn count_substrings(s: String) -> i64` and reads the
letters through `s.bytes()`.

| file | mechanism |
|---|---|
| `palindromic_substrings.kara` ★ | from each of the `2n - 1` centers, a letter or the gap between two, the window widens while its two ends match, each step one more palindrome; O(n^2) time, O(1) space |
| `palindromic_substrings_table.kara` | a table of whether each substring is a palindrome: its two ends match and what lies between is empty, one letter or itself a palindrome, filled from the last row up; O(n^2) time and space |
| `palindromic_substrings_manacher.kara` | Manacher's algorithm, once for odd and once for even palindromes: a center inside the rightmost palindrome found so far starts from its mirror image's count, so the window only ever widens past that palindrome's right edge; O(n) |
| `palindromic_substrings_ends.kara` | the starts of the palindromes ending at each letter: the letter alone, two equal letters, or a palindrome ending one letter earlier with a matching letter just before it; O(n^2) time, O(n) space |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 15 lines: the two LeetCode examples; nine more
(one letter; two different and two equal; an odd and an even palindrome
as the whole string; one palindrome inside another; a run broken by one
letter; alternating letters, with palindromes overlapping; and a string
whose longest palindromes are short), each with its answer; the total
and a checksum of the answers to 300 random cases of 1 to 40 letters
from the first 1 to 4 of the alphabet; and three cases of the problem's
largest size, 1,000 letters: all one letter, from two letters and from
all 26. `palindromic_substrings.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every substring compared letter by letter with itself read backwards.
Each of 1,000 cases has 1 to 14 letters from the first 1 to 3 of the
alphabet, so most cases are full of repeats.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the answer is at least the number of letters and at most the number of substrings |
| P3 | the string reversed gives the same answer |
| P4 | the letters renamed, a to b, b to c and c to a, give the same answer |
| P5 | a letter the string does not hold, put on the end, adds exactly one |

It prints `1000 cases (7486 letters), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every center taken as a character | P1 881, P2 308, P5 1000 |
| M2 | ★: the last center skipped | P1 1000, P2 122 |
| M3 | table: two equal letters not a palindrome by themselves | P1 840 |
| M4 | table: the cell one to the left read, not the one inside | P1 464 |
| M5 | manacher: an odd mirror trusted one letter past the edge | P1 414, P2 131, P3 274, P5 359 |
| M6 | manacher: the even mirror one place off | P1 120, P3 147 |
| M7 | ends: two equal letters never counted | P1 840 |
| M8 | ends: the start's own letter compared, not the one before it | P1 458, P3 360 |
| E1 | ★: one center past the last | 0 |
| E2 | table: three letters with equal ends counted without the middle | 0 |
| E3 | manacher: the right edge moved on a tie too | 0 |
| E4 | ends: the starts holding 0 before the first letter | 0 |

P1 kills all eight. M3 and M7 fail in exactly the same 840 cases because
both lose every even palindrome: the table's two-letter cells start
every longer even one, and the ends arm grows its longer even
palindromes out of two-letter ones. M1 counts every odd palindrome
twice, so P5 sees it every time, the new letter counting twice; M2 never
counts the last letter alone, which P5 cannot see, since after the
append the letter it misses is the new one. P3 sees M5, M6 and M8, whose
errors depend on direction: Manacher's algorithm scans left to right and
reads its mirror one place off, and the ends arm compares the wrong
letter on one side. P4 sees nothing, and cannot: every arm compares
letters only for equality, so renaming them all consistently changes no
answer, right or wrong. The four survivors cannot change an answer: the
extra center's window starts past the end; the middle of a three-letter
window is one letter, always a palindrome; a palindrome with the same
right edge serves as well to mirror from; and a start at 0 can never
move left.

## Verification

Every arm prints the same output as `palindromic_substrings.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` (the release build is from `4497546898`, whose compiler
source is the same), with runtime archives newer than the last
`runtime/src` change.

The frozen legacy backends refuse every arm and the differential at type
checking: the harness hands `seed`, already a `mut ref` parameter, on
with the `mut` marker design.md asks for, which legacy rejects, and the
ends arm also reads `*start` from `starts.iter()`, which legacy types by
value. Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 texts of 2,000 letters
once, each from the first 1 to 3 letters of the alphabet, the count
picked for each text; then 300 rounds each answer one text, picked by
the round, adding up the answers and putting each into a checksum. A
text of one letter repeated has 2,001,000 palindromes, and each
palindrome is one step of a window widening, so the total below is also
the number of those steps. Every implementation prints `20 inputs,
300 rounds: total 241018950, checksum 232179054`, the Kāra program under
`karac __mir-run` included (in 179 s).

Each implementation is the same expansion from each center over the
text's bytes: Rust over `as_bytes()`, C over a `char` array, Go indexing
a `string` and Python indexing a `str`. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine), each including making the texts:

| | time |
|---|---|
| C (`clang -O3`) | 0.20 to 0.21 s |
| Rust (`rustc -O`) | 0.18 to 0.23 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.26 to 0.29 s |
| Go | 0.28 to 0.29 s |
| Python | 16.8 to 17.0 s |
| Kāra (`karac build --mir`) | 0.28 to 0.30 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program: its parameters are still owned rather than borrowed, so handing
`texts[(r * 7) % inputs]` to `count_substrings` moves an element out of
a `Vec`. That edit is by hand, on top of the `scripts/new-bench.sh`
output. A copy outside the kata whose parameter is `ref String` builds
under legacy and takes 0.21 s in all three runs. Under `karac
__mir-llvm-run` the program prints the same line in 2.4 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

So the v2 build is level with Go and Rust's overflow-checked build and
takes about 1.4 times as long as legacy, inside the M2 bar of 1.5 times.
In the source, each step of the inner loop is two range tests, two
indexed byte reads, a comparison and three checked additions or
subtractions; the comparison with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The legacy refusals
above are not filed because legacy is frozen.
