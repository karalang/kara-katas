# 1147. Longest Chunked Palindrome Decomposition

You are given a string `text`. You should split it to `k` substrings
`(subtext1, subtext2, ..., subtextk)` such that:

- `subtexti` is a non-empty string.
- The concatenation of all the substrings is equal to `text` (i.e.,
  `subtext1 + subtext2 + ... + subtextk == text`).
- `subtexti == subtextk - i + 1` for all valid values of `i` (i.e.,
  `1 <= i <= k`).

Return the largest possible value of `k`.

```
text = "ghiabcdefhelloadamhelloabcdefghi"  ->  7
text = "merchant"                          ->  1
text = "antaprezatepzapreanta"             ->  11
```

**Constraints:** `1 <= text.length <= 1000`; `text` consists only of
lowercase English characters.

The arms are `fn longest_decomposition(text: Str) -> i64`.

## Approaches

Taking the shortest equal chunks off the two ends is never worse than a
longer pair: a longer chunk that the text both starts and ends with has
the shorter one at both of its own ends, so it splits into the shorter
pair around a palindromic decomposition of its own middle.

| file | mechanism |
|---|---|
| `longest_decomposition.kara` ★ | greedy from both ends: the shortest chunk at the front equal to the chunk of its size at the back, compared as slices of the text, is taken off both; what is left with no such chunk is one more. O(n^2) |
| `longest_decomposition_recursive.kara` | recursion on the middle: the shortest front of the text that it also `ends_with` is two chunks, and the rest is the middle's own answer. O(n^2) |
| `longest_decomposition_hashed.kara` | greedy from both ends with rolling hashes, the front chunk growing on its right and the back chunk on its left; the chunks are compared letter by letter only when the hashes agree. O(n) when no hashes agree by chance |
| `longest_decomposition_table.kara` | dynamic programming over the middles, every chunk size tried and the best kept, with a table of how far the text agrees from any two places to compare chunks in O(1). O(n^2) |
| `longest_decomposition_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `text: String` read through `as_bytes()`, one scan of `r` over the whole text that closes a chunk whenever `bytes[l..=r]` equals the slice mirrored at the back, so each chunk is counted once from either half and the middle once), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five properties |

Every arm prints the same 15 lines: LeetCode's three examples; one letter
(1); two alike (2) and unlike (1); `aba` (3); `abab` (2); `ababa` (5);
`elvtoelvto` (2). Then over 2000 random texts over 1, 2, 3 or 26 letters,
every other one of 1 to 60 letters at random and the rest 1 to 10 chunks
mirrored around a middle, the answers summed and a checksum (`2000 random
texts: chunks total 28802, checksum 377024670`), and four texts at the
constraints' end: 1000 a's (1000), `ab` 500 times (500), 999 a's and a b
(1), and 240 chunks of 1 to 3 letters mirrored, 928 letters (700).
`longest_decomposition.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way to cut the text into chunks, the most chunks of a
way whose list of chunks reads the same backwards. It checks 2000 texts
of 1 to 12 letters in four kinds of 500: over two letters; over three;
chunks of 1 to 3 letters mirrored around a middle of 0 to 2; and
palindromes over two letters. Ten more are two different chunks of six
letters whose hashes agree under the hashed arm's base and modulus, found
by a search outside the file, so the hashed arm must compare the chunks
themselves. Every random choice, P3's names and P6's word among them, is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | the text backwards gives the same answer |
| P3 | the letters renamed gives the same answer |
| P4 | a mark no text holds, `#`, at both ends gives two more chunks |
| P5 | the answer is the text's length exactly when the text is a palindrome |
| P6 | any word at both ends gives at least two more chunks |

P5 holds because every letter is its own chunk exactly when the i-th
letter equals the i-th from the end. All 60,300 checks pass on every arm:
`2010 texts: checksum 727153004, 60300 checks over 5 arms: 0 failures`. A
Python reading of the same texts, by the same enumeration, with the five
properties asserted against the ★ arm's mirror, gives the same line.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. Twenty-nine are caught; one is
equivalent: the recursive arm testing whether the text starts with its
last `size` letters rather than ends with its first, which says the same
thing. Fifteen are kept, no two failing the same checks; one of them
stops the run.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a middle of one letter not counted | P1 638, P5 528 |
| M2 | ★: only odd sizes tried | P1 226, P6 479 |
| M3 | ★: the front end moved by one letter | P1 266, P2 202, P6 425 |
| M4 | recursive: a chunk of half the text never tried | P1 996, P4 199, P5 751, P6 157 |
| M5 | recursive: a pair of chunks counted once | P1 1331, P4 2010, P5 751, P6 1589 |
| M6 | recursive: the longest chunk first | P1 661, P5 487, P6 225 |
| M7 | hashed: a chunk of exactly half what is left never tried | P1 557, P5 422 |
| M8 | hashed: equal hashes trusted | P1 10, P2 10, P3 10 |
| M9 | hashed: the back chunk hashed from its end | P1 347, P6 922 |
| M10 | hashed: the power never reset | P1 884, P4 1331, P5 542, P6 1331 |
| M11 | table: the middle after one letter, whatever the size | P1 284, P6 479 |
| M12 | table: a run must outlast the chunk | P1 1331, P4 2010, P5 751, P6 2010 |
| M13 | solution: a chunk's last letter starts the next | P1 999, P4 2010, P5 486, P6 1164 |
| M14 | solution: chunks compared by their first letters | P1 432, P2 501, P4 399, P6 197 |
| M15 | solution: the back chunk read one letter early | stops: index out of bounds |

P1 catches all twenty-eight edits that let the run finish. P5 and P6
catch nineteen each. P5, on the 950 palindromes among the texts, catches
the edits that miscount a text that is all single-letter chunks: a middle
lost or doubled (M1), a size never tried (M4, M7), a pair counted once
(M5), a chunk taken that is not the shortest (M6). P6 catches the edits
whose count can fall when a word wraps the text, mostly those that miss
an equal pair of chunks of some sizes (M2, M3, M9, M11). P4 catches ten,
the edits whose count for the fenced text is not their own count plus
two: an edit that counts a pair as one or never closes it (M5, M12, M13)
is off by the fence's own pair, and an edit that depends on the lengths
(M4) or on where the last chunk ended (M10) answers the longer text
differently. P2 catches five, the edits that treat the front and the
back unlike (M3, M8, M14, and two not kept). P3 catches only M8: the
collisions are hash-specific, so renaming the letters of a colliding pair
leaves two chunks that no longer collide, and the trusting arm answers
the renamed text right and the text as given wrong. The edit that stops
the run reads the back chunk from index `n - 2 - r`, which is -1 at the
last letter.

Of the fourteen caught and not kept, seven fail exactly as a kept one:
the ★ arm not taking a chunk of exactly half what is left, the recursive
arm counting an empty middle, and the hashed and table arms counting an
empty middle, as M7; a chunk of half the middle never tried in the table
arm, as M4; a run never longer than one letter in the table arm, as M9;
and the longest chunk winning in the table arm, as M6. One pair fails
alike: the ★ arm moving its back end by one letter and the recursive arm
keeping all but one letter of the back in its middle. The other five (the
middle counted twice in the ★ arm, the size never reset in the hashed
arm, and the last letter never scanned, the scan stopping past the middle
and a chunk of one letter not counted in the solution arm) each fail in a
way of their own and were not needed.

## Verification

Every arm prints the same output as `longest_decomposition.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The ★, recursive and table arms were written as Kāra and checked clean as
written. In the hashed arm `karac fix` added the `.iter()` that
`text.bytes()`, a `Slice[u8]`, needs before `collect`, and dropped the
`as i64` on each byte, which widens by itself. `karac fix` carried the
solution arm in three rounds: the adapter's `&str` to `Str` and
`Solution::` to `Solution.`; then `struct Solution {}` declared; then
`as_bytes()` to `bytes()` and the adapter's `as i64` dropped.

The kata found one gap, a perf row: `==` on two `Slice[u8]` compares
byte by byte (B-2026-11-13-33; see Benchmarks).

## Benchmarks

`bench/` times the ★ arm against the same greedy in C, Rust, Go and
Python. Each of 20,000 rounds builds one of 20 texts of 1000 letters
anew and answers all 20: a word of 1 to 4 letters over `ab` repeated,
then one letter changed at random, so the ends agree on long runs and
the shortest equal chunks are long. Every program prints `20000 rounds
over 20 texts of 1000 letters: chunks total 249358426, checksum
131443400`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `d59535f2bc`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.480 to 0.613 s | 0.503 s |
| C (`clang -O3`) | 0.506 to 0.711 s | 0.543 s |
| Rust (`rustc -O`) | 0.586 to 0.731 s | 0.622 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.648 to 0.832 s | 0.687 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.652 to 0.832 s | 0.690 s |
| Kāra (`karac build`) | 1.038 to 1.266 s | 1.100 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.022 to 1.367 s | 1.118 s |
| Go | 1.194 to 1.363 s | 1.304 s |
| Python | 32.3 s | |

The two Kāra builds are the same binary: the cost gate parallelizes
nothing here.

Kāra trails overflow-checked Rust by 1.6x, and the two do not compare
the same thing. The ★ arm slices a `Str`, and each slice checks that
both its ends fall on a character's first byte; the C, Rust and Go
programs compare bytes (Rust through `as_bytes()`), which have no such
check. Rust slicing the `&str` itself, which checks the same boundaries,
took 1.29 to 1.36 s in three runs by hand, behind Kāra. The like-for-like
Kāra program, the ★ arm over `text.bytes()`, took 1.30 to 1.34 s in three
runs: `==` on two `Slice[u8]` compiles to a loop over the bytes one at a
time, where `Str` equality and Rust's byte slices call `memcmp`
(B-2026-11-13-33, perf, open).
