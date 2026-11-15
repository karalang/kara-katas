# 1165. Single-Row Keyboard

There is a special keyboard with all keys in a single row.

Given a string `keyboard` of length 26 indicating the layout of the
keyboard (indexed from 0 to 25), initially your finger is at index 0. To
type a character, you have to move your finger to the index of the
desired character. The time taken to move your finger from index `i` to
index `j` is `|i - j|`.

You want to type a string `word`. Write a function to calculate how much
time it takes to type it with one finger.

```
keyboard = "abcdefghijklmnopqrstuvwxyz", word = "cba"       ->  4
keyboard = "pqrstuvwxyzabcdefghijklmno", word = "leetcode"  ->  73
```

**Constraints:** `keyboard.length == 26`; `keyboard` contains each
English lowercase letter exactly once in some order; `1 <= word.length
<= 10^4`; `word[i]` is an English lowercase letter.

The arms are `fn calculate_time(keyboard: Str, word: Str) -> i64`.

## Approaches

Every arm sums the finger's moves from place 0; they differ in how a
letter's place is found.

| file | mechanism |
|---|---|
| `calculate_time.kara` ★ | a table: each letter's place in a fixed array of 26 (`[0; 26]`), filled once from `keyboard.bytes()`, then the moves summed letter by letter. O(26 + n) |
| `calculate_time_find.kara` | a search per letter: each letter looked up on the keyboard with `find`, which gives its byte place. O(26 n) |
| `calculate_time_map.kara` | a `Map[char, i64]` from `chars().enumerate()`, the word's places read through it, and the moves summed by a `fold` that carries the last place. O(26 + n) |
| `calculate_time_pairs.kara` | the finger's places as a `Vec`, place 0 first, and the time summed over neighbouring pairs from `windows(2)`. O(26 + n) |
| `calculate_time_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `String` parameters, a `[usize; 26]` table from `keyboard.bytes().enumerate()`, `(b - b'a') as usize` indices, the moves as `i32` through `as i32` casts), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's examples (4, 73); one
letter at the start and one at the end (0, 25); a letter repeated
(`"zzzz"`: 25); the alphabet typed on the keyboard in order (25) and
backward (50). Then 2000 random keyboards with words of 1 to 40 letters
over the first 1 to 26 (`2000 random words: total 316019, checksum
806931988`), and two words of 10^4 letters, the constraints' most: random
over 26 (86037) and `a` and `z` in turn on the keyboard in order
(249975). `calculate_time.py` mirrors the ★ arm and its output is
byte-identical; a Python reading that walks the keyboard from its left
end for every letter gives the same output.

The Mend loop: the map arm checks clean as written. The ★ arm takes one
round of two edits, the `as i64` dropped from `place[(c - b'a') as
i64]`, since a `u8` index needs no cast. The search arm takes one,
`keyboard.find(c)` to `keyboard.find(c.to_string())`: Kāra's `find`
takes a `Str`, not a `char`. The pairs arm takes one, `.into_iter()`
after `windows(2)`. The Rust arm takes four rounds (3, 1, 6 and 2
edits): `&str` to `Str` and `Solution::` to `Solution.`; then `struct
Solution {}`; then `[0usize; 26]` to `[0; 26]`, `.iter()` before
`enumerate()`, the `as usize` indices to `as i64`, `ans` annotated `i32`
and the adapter's `as i64` dropped; then the `as i64` indices dropped.
Its output matches on the first run.

The Rust arm's last round is a gap in the Mend loop: an `as usize` index
over a `u8` is first rewritten to `as i64`, which the next round finds
redundant and drops, so every such index costs two rounds and is left
in parentheses, `pos[(b - b'a')]`. That is kara B-2026-11-15-50.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the finger starts at index 0, and each letter is found by
walking the keyboard from its left end. It checks 2000 keyboards and
words in four kinds of 500: words of 1 to 5 letters over the first 1 to
3, of 1 to 40 over the first 1 to 26, and of 100 to 400 over 26, each on
a random keyboard; and words of 1 to 40 over 26 on the keyboard in order
or backward. Every random choice the properties make is drawn before
any arm answers, among them a second word of 1 to 10 letters and a
renaming of the 26 letters.

| | property |
|---|---|
| P1 | the time is the literal one |
| P2 | the second word typed after the word: its own first move from 0 becomes a move from the word's last letter |
| P3 | the keyboard backward keeps every move but the first, which becomes 25 less the first letter's place |
| P4 | every letter typed twice costs nothing more |
| P5 | the keyboard and the word renamed by one permutation keep the time |
| P6 | the word backward keeps every move but the first, which goes to the last letter's place |

All 60,000 checks pass on every arm: `2000 words: checksum 576064516,
60000 checks over 5 arms: 0 failures`, in 17 s under `karac __mir-run`.
A Python reading of the same draws, with the mirror against the literal
reading, gives the same checksum.

## Mutation testing

Thirteen edits to the differential, two to four to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run` with
`KARAC_HASH_SEED=1`, each failing the same way under both. Twelve are
caught and one is equivalent: the search arm taking the last match,
`rfind`, rather than the first (F1), since every letter is on the
keyboard once.

| # | mutation | failures by property |
|---|---|---|
| T1 | ★: every place one to the right | P1 2000, P2 2000 |
| T2 | ★: a move to the left counted negative | P1 1599, P2 969, P3 1513, P6 1513 |
| T3 | ★: every move measured from place 0 | P1 1849, P2 1891, P3 1862, P4 1983, P6 1513 |
| T4 | ★: the finger starting on place 1 | P1 2000, P2 2000, P3 158, P6 101 |
| F2 | find: each press counted as a move | P1 2000, P4 2000 |
| M1 | map: the finger never moves | P1 1849, P2 1891, P3 1862, P4 1983, P6 1513 |
| M2 | map: the keyboard read backward | P1 2000, P2 2000, P3 2000, P6 1513 |
| W1 | pairs: no start at place 0 | P1 1926, P2 1912, P3 2000, P6 1513 |
| W2 | pairs: the last move left out | P1 1641, P2 1681, P3 130, P4 1641, P6 1444 |
| X1 | solution: a move to the left counted negative | P1 1599, P2 969, P3 1513, P6 1513 |
| X2 | solution: the finger back at 0 after each letter | P1 1849, P2 1891, P3 1862, P4 1983, P6 1513 |
| X3 | solution: the finger starting at the right end | P1 2000, P2 2000, P3 2000, P6 1513 |

P1 catches all twelve, P2 eleven, P3 and P6 ten, P4 five, and P5 none: every
edit here treats all letters alike, so renaming the letters on the
keyboard and in the word together cannot expose it. P5 stays as a check
on the arms' reading of the letters themselves. The two edits that
change only the first move (T1, T4) fail P1 and P2 on every word, but
the backward keyboard and backward word (P3, P6) compare first moves
through the arm's own answer and see T4 only rarely, and T1 never.

## Benchmarks

`bench/` times the ★ arm against the same table of 26 places in C, Rust,
Go and Python. 16 keyboards, each a random order of the 26 letters, and
16 words of 10^4 random letters are built once; each of 5000 rounds types
every word from a random place in its first half. Every program prints
`5000 rounds over 16 words of 10^4 letters: total 5261897300, checksum
486861450`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `1bdebaaa70`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.178 to 0.261 s | 0.180 s |
| C (`clang -O3`) | 0.203 to 0.289 s | 0.216 s |
| Rust (`rustc -O`) | 0.329 to 0.454 s | 0.349 s |
| Go | 0.376 to 0.477 s | 0.388 s |
| Kāra (`karac build`) | 0.560 to 0.653 s | 0.589 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.562 to 0.672 s | 0.590 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 2.447 to 2.563 s | 2.469 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.560 to 2.688 s | 2.636 s |
| Python | 30.8 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; a plain `karac build` gives the same binary, so the
two Kāra rows are one program timed twice. Kāra takes about 0.22x
overflow-checked Rust's time, the equal-safety comparison, and about
3.3x C's, which checks nothing. Both Kāra and checked Rust refuse `(next
- at).abs()` on the one value with no positive (`i64` MIN): Kāra stops
with `integer overflow`, as checked Rust panics. The cost in Rust is
that check: with `wrapping_abs()` in its place, and every other check
kept, the checked Rust program takes 0.49 s (one run each). Go takes
about 0.66x Kāra's time and Python about 52x.
