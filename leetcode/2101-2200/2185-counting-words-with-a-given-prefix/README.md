# 2185. Counting Words With a Given Prefix

You are given an array of strings `words` and a string `pref`.

Return *the number of strings in* `words` *that contain* `pref` *as a
**prefix***.

A **prefix** of a string `s` is any leading contiguous substring of `s`.

```
words = ["pay", "attention", "practice", "attend"], pref = "at"    ->  2
words = ["leetcode", "win", "loops", "success"],    pref = "code"  ->  0
```

**Constraints:** `1 <= words.length <= 100`; `1 <= words[i].length,
pref.length <= 100`; `words[i]` and `pref` consist of lowercase English
letters.

Each word is asked whether it begins with the prefix: whether it is at
least as long, and its first letters are the prefix's. O(n * |pref|).

## Approaches

| file | mechanism |
|---|---|
| `prefix_count.kara` ★ | each word asked whether it `starts_with` the prefix, and those counted |
| `prefix_count_bytes.kara` | a word shorter than the prefix passed over, and the rest compared byte by byte with the prefix until one differs; counted when every byte of the prefix was matched |
| `prefix_count_trie.kara` | every word walked into a trie of letters, its children in one flat `Vec` of 26 slots a node, each node keeping how many words pass through it; the answer the count at the node the prefix leads to, or 0 if it leads nowhere; O(total letters + \|pref\|) |
| `prefix_count_struct.kara` | a `struct Prefix` of its letters, made `of` a string, that says whether it `opens` a word, letter by letter over `chars` (`ref self`), and how many of a list it opens, its `count_in` (`ref self`) |
| `prefix_count_iter.kara` | the words `filter`ed to those at least as long as the prefix whose bytes, `zip`ped with the prefix's, are `all` equal, and `count`ed |
| `prefix_count_solution.kara` | LeetCode's Rust template: `Vec<String>`, `starts_with(&pref)` in a `filter` closure, `count() as i32`, `struct Solution;`, `Solution::`; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(one word that is the prefix, a prefix longer than two of the words,
every word, and a prefix found inside a word but not at its start), each
with its count; then the total and a checksum over 2000 random lists of
1 to 20 words of 1 to 6 letters, from a to b, a to c or a to z in turn,
with a prefix of 1 to 3 letters; then the constraints' largest, 100
words of 100 letters, half all a and half ending in b, against prefixes
of 100 a, 99 a and one b. `prefix_count.py` mirrors the ★ arm and its
output is byte-identical.

`karac fix` carries the template in two rounds of 7 and 1 edits: Rust's
spellings (`Vec<String>` to `Vec[String]`, `starts_with(&pref)` to
`starts_with(pref)`, `struct Solution;` to `struct Solution {}`, and
`Solution::` to `.`, among them); then the adapter's widening `as i64`
dropped, as the `i32` widens to the `i64` it returns.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a word counted when it is at least as long as the prefix and
its slice of the prefix's length equals the prefix. No `starts_with`, no
byte loop and no trie. It checks 300 random lists of 1 to 8 words of 1
to 4 letters, from a to b or a to c in turn, with a prefix of 1 to 3
letters; then 30 whose prefix is cut from one of the words; then 30 of
one word repeated. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | the words reversed: the same count |
| P3 | the prefix one letter longer, for each of a to c: counts that add up to the count, less the words that are the prefix itself |
| P4 | the same letter, c, put before every word and the prefix: the same count |
| P5 | the count at most the words that start with the prefix's first letter; and one more with the prefix itself added as a word |
| P6 | each arm agrees with at least three of the other five |

P2 holds since a word does not care where in the list it is. P3 holds
since a word that begins with the prefix either is the prefix or goes
on with one letter more, and every word here is of a to c. P4 holds
since a word begins with the prefix exactly when c and the word begins
with c and the prefix. P5 holds since a word that begins with the
prefix begins with its first letter, and the prefix begins with itself.

The differential prints `360 lists: checksum 575489014, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
lists. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Twenty-eight edits to the differential, five to each Kāra arm and three
to the template, each run under `karac __mir-llvm-run` and `karac
__mir-run`. Seventeen are kept, three to each Kāra arm and two to the
Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `ends_with` for `starts_with` | P1 135, P3 137, P4 117, P5 31, P6 135 |
| M3 | ★: a word equal to the prefix not counted | P1 93, P3 127, P5 360, P6 93 |
| M4 | ★: the first word skipped | P1 77, P2 94, P3 22, P6 77 |
| M7 | bytes: the first byte never compared | P1 203, P3 81, P4 203, P5 150, P6 203 |
| M8 | bytes: a match on all but the last byte | P1 196, P3 217, P5 114, P6 196 |
| M9 | bytes: each byte compared against the prefix's first | P1 60, P3 157, P4 149, P5 156, P6 60 |
| M11 | trie: a node's count only where a word ends | P1 150, P3 79, P6 150 |
| M12 | trie: a prefix leading nowhere counted as every word | P1 173, P3 356, P5 173, P6 173 |
| M14 | trie: a fresh node for every letter | P1 121, P2 40, P3 49, P4 78, P5 155, P6 121 |
| M16 | struct: a word shorter than the prefix opened | P1 82, P3 162, P6 82 |
| M17 | struct: a letter that differs skipped, not refused | P1 143, P3 127, P5 94, P6 143 |
| M18 | struct: the prefix's letters reversed | P1 55, P3 155, P4 152, P5 126, P6 55 |
| M22 | iter: `any` letter equal, not `all` | P1 173, P3 303, P4 214, P5 87, P6 173 |
| M23 | iter: the word's bytes from the second | P1 179, P3 154, P4 183, P5 224, P6 179 |
| M25 | iter: the words that fail counted | P1 337, P3 360, P5 360, P6 337 |
| M27 | solution: one more | P1 360, P3 360, P5 202, P6 360 |
| M28 | solution: the adapter's prefix doubled | P1 174, P3 110, P4 56, P5 360, P6 174 |

P1, P3 and P6 kill all seventeen, P5 fourteen, P4 eight and P2 two. P3
asks each arm about four prefixes and checks them against each other,
so any edit that miscounts one of them shows. P5 misses an edit whose
count stays within its bounds: the first word skipped (M4), only the
words equal to the prefix (M11), and a shorter word opened (M16); each
still counts the prefix added as a word, the last one in the list. P4
puts a c before everything, and sees an edit that treats the first
letter or the letters' order apart, or that reads a letter's value:
`ends_with` (M1), the first byte never compared (M7), every byte
against the first (M9), a fresh node (M14), the letters reversed (M18),
`any` (M22), the bytes from the second (M23), and the prefix doubled
(M28). P2 reverses the list, and sees only the edits that depend on the
order of the words: the first word skipped (M4), and the trie whose
prefix follows only the last word written into each slot (M14).

Of the twenty-eight, eleven were not kept. None is equivalent. One
crashes: the bytes arm's word one shorter than the prefix let through
(M6) indexes past its end. Two fail as a kept one does: the iter arm's
length never checked, as M16, and its longer words only, as M3; each is
the same edit as that one, written another way. Eight were left out to
keep three to an arm: the ★ arm's `contains` (M2) and the prefix's last
letter dropped (M5), the bytes arm's count of the bytes matched (M10),
the trie arm's last letter never walked (M13) and its slot by the
letter alone (M15), the struct arm's last word never asked (M19) and a
word opened by its first letter (M20), and the template's words that
hold the prefix's first letter (M26), which fails as M20.

## Verification

Every arm prints the same output as `prefix_count.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, template, bytes and struct arms take
0.3 s, the iter arm 0.5 s and the trie arm 0.7 s. The differential
takes 0.7 s.

## Benchmarks

The bench builds 100 words of 1 to 100 letters of a and b once, the
constraints' longest list; then solves 100000 prefixes of 1 to 8
letters of a and b, each drawn afresh, with the ★ arm in all five
languages. C compares with `memcmp` after the length, Go with
`strings.HasPrefix`, Rust and Kāra with `starts_with` and Python with
`str.startswith`. Every implementation prints `100000 solves: checksum
557557699`.

BENCHTAB
