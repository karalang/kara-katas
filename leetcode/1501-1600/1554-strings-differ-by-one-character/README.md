# 1554. Strings Differ by One Character

Given a list of strings `dict` where all the strings are of the same
length, return `true` if there are two strings that differ by exactly one
character at the same index; otherwise return `false`.

```
dict = ["abcd","acbd","aacd"]           ->  true    ("abcd" and "aacd")
dict = ["ab","cd","yz"]                 ->  false
dict = ["abcd","cccc","abyd","abab"]    ->  true    ("abcd" and "abyd")
```

**Constraints:** the number of characters in `dict` is at most `10^5`;
`dict[i].length == dict[j].length`; the strings are unique; `dict[i]`
holds lower-case English letters only.

## Approaches

| file | mechanism |
|---|---|
| `differ.kara` ★ | two words differ in exactly one place `j` when they are equal with place `j` blotted out: every word goes into a `Set[String]` once per place, that place replaced by a `*`, and a repeated pattern is the pair. O(n m²) for n words of m letters |
| `differ_hash.kara` | the blotted patterns hashed rather than built: a word's polynomial hash with place `j`'s letter taken back out, a `Map[(i64, i64), Vec[i64]]` from (place, hash) to the words seen there through `entry(..).or_insert(..)`, and words sharing a key checked letter by letter, so a collision cannot answer wrongly. O(n m) expected |
| `differ_sorted.kara` | place by place, the words with that place cut out (`w[..j]` and `w[j + 1..]`) are sorted, and two that differ only there end up next to each other: `windows(2)` with `any`. O(m² n log n) |
| `differ_solution.kara` | LeetCode's Rust template (`differ_by_one(dict: Vec<String>) -> bool`, the ★ arm over each word's bytes, the pattern a `Vec<u8>` in a `HashSet`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples, then
`[a]`, `[a, b]`, `[ab, ba]`, `[abc, xbz, xyc, ayz]` and
`[aaaa, aaab, zzzz]`; then the count of `true` answers and a checksum for
3000 random lists of up to 8 distinct words of up to 5 letters, 300 of up
to 1000 of up to 20 and 30 of up to 10000 of up to 10, each list over its
own first few letters. `differ.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: some two words, zipped character by character, differ in
exactly one place. It checks 3000 lists of 1 to 8 distinct words of one
length from 1 to 5, each list over its own first 1 to 3 letters, every
random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | one word is `false`, and the first word with its first letter made a `z`, put after the list, makes it `true` |
| P3 | every word reversed leaves the answer |
| P4 | every letter moved on by one (`c` back to `a`) leaves the answer |
| P5 | the list in reverse order, a `q` put after every word, leaves the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 222973746, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: nothing blotted, the word itself entered once per place | P1 1742, P2 1649, P5 604, P6 1742 |
| M2 | ★: the first place never blotted | P1 435, P2 2087, P3 163, P6 435 |
| M3 | ★: the first place blotted every time | P1 1395, P2 1045, P5 257, P6 1395 |
| M4 | hash: a pair needs two places differing | P1 1348, P2 3000, P6 1348 |
| M5 | hash: the letter taken out at the first place's power | P1 273, P3 305, P6 273 |
| M6 | hash: no word recorded | P1 1348, P2 3000, P6 1348 |
| M7 | sorted: nothing cut, the word kept whole | P1 1348, P2 3000, P6 1348 |
| M8 | sorted: neighbours that differ taken as the pair | P1 697, P2 604, P5 347, P6 697 |
| M9 | template: the first byte blotted every time | P1 1395, P2 1045, P5 257, P6 1395 |
| M10 | template: the last place never blotted | P1 422, P2 604, P3 163, P5 422, P6 422 |

## Benchmarks

The bench builds 20 lists of 1000 random words of 100 letters once, half
of them with a pair planted that differs in one place, and asks each 3
times by the ★ arm, in all five languages. Every pattern is built as the
Kāra arm builds it: the word's characters copied, one replaced, collected
into a new string. Kāra's `Set` and Rust's `HashSet` are SipHash-1-3, Go's
is its own map over strings built from `[]rune`, C's an open-addressing
table hashed by FNV-1a over heap copies, and Python slices the string
instead of copying characters. Every implementation prints `3 passes over
20 lists of 1000 words of 100 letters: 30 true, checksum 487928683`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 1.135 s |
| Kāra (`karac build`) | 1.624 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.657 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.720 s |
| Rust (`rustc -O`) | 1.834 s |
| Python | 2.3 s |
| Go | 5.350 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (1.57 s and 1.58 s on one run).

Kāra is 0.96x Rust under overflow checks by median. Not traced. Each
pattern is a copy of a 100-character vector, a collect into a string and
a hash of it, so allocation and hashing are most of every compiled row.
Python is close behind because its slices copy bytes in C, and Go is last
because each pattern goes through `[]rune` and back.

## Verification

All four arms print the same output as `differ.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The ★ arm was written in Kāra and checked as written. The shared harness
took one edit from `karac fix`: `Vec[&str]` to `Vec[Str]`, from a parse
error that names it.

The sorted arm joined its two pieces as `w[..j].to_string() + &w[j + 1..]`,
Rust's spelling, and took two rounds of `karac fix`: the `&` dropped
(a slice is already a view), then `.to_string()` added to the right-hand
piece (`+` on a `String` appends an owned `String`).

The hash arm turned each word into numbers with
`w.bytes().iter().map(|b| b - 96).collect()` into a `Vec[i64]`, and the
checker refused it: `trait bound C: FromIterator[u8] is not satisfied;
Vec[i64] implements FromIterator[i64], not FromIterator[u8]`, with
nothing for `karac fix`. A `u8` widens to `i64` on its own where a value
is bound (`let n: i64 = w.bytes()[0]` checks), so the collect reads as if
it should too; refusing it is consistent, since a closure's result is its
own type, but the refusal names no way forward. That is filed as
B-2026-11-14-12. The arm was edited by hand to `b as i64 - 96`, which
checks and is not reported as an unnecessary cast.

The differential took two edits from `karac fix`: `c as u8` on a `char`
to `c as u32 as u8`, from a refusal that names it (a `char` does not fit
in 8 bits), and `"z".to_string() + ..` to `"z" + ..`, which `karac check`
does not report.

The Rust template took 5 changed lines and the `use` removed, then 2 and
1, over three rounds: `use std::collections::HashSet` dropped, the
`Vec<..>` and `HashSet<..>` types to `Vec[..]` and `HashSet[..]` with
`HashSet::new()` to `HashSet.new()`, `for word in &dict` to
`for word in ref dict`, `!seen.insert(..)` to `not seen.insert(..)` and
`Solution::` to `Solution.`; then `struct Solution {}` added and
`HashSet` to `Set`; then `word.as_bytes()` to `word.bytes()`. It checks
and agrees with no hand edit.
