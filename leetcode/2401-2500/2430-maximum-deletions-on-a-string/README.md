# 2430. Maximum Deletions on a String

You are given a string `s` consisting of only lowercase English letters.
In one operation, you can:

- Delete **the entire string** `s`, or
- Delete the **first** `i` letters of `s` if the first `i` letters of
  `s` are **equal** to the following `i` letters in `s`, for any `i` in
  the range `1 <= i <= s.length / 2`.

For example, if `s = "ababc"`, then in one operation, you could delete
the first two letters of `s` to get `"abc"`, since the first two letters
of `s` and the following two letters of `s` are both equal to `"ab"`.

Return *the **maximum** number of operations needed to delete all of*
`s`.

```
s = "abcabcdabc"  ->  2
s = "aaabaab"     ->  4
s = "aaaaa"       ->  5
```

**Constraints:** `1 <= s.length <= 4000`; `s` consists only of
lowercase English letters.

What is left after any operation is a suffix of `s`, so `best[i]`, the
most operations that clear the suffix from `i`, is 1 for deleting it
whole or one more than `best[i + j]` for each `j` whose first `j`
letters repeat at once. Those `j` are the ones where the suffixes at `i`
and `i + j` share a prefix of at least `j`, and the longest common
prefix of two suffixes is one more than that of the suffixes after them
when their first letters agree, so the whole table of them takes O(n^2)
and every check after that is a lookup.

## Approaches

| file | mechanism |
|---|---|
| `deletions.kara` ★ | `best[i]` from the back, the common prefixes of the suffix at `i` with every later one kept in two rows, each row from the one after it and the two swapped. O(n^2) time, O(n) space |
| `deletions_naive.kara` | the statement read directly: `best[i]` from the back, each `j` tried by comparing the slices `b[i..i + j]` and `b[i + j..i + 2 * j]` themselves. O(n^3) at worst |
| `deletions_hash.kara` | polynomial prefix hashes modulo `10^9 + 7` under the consts `MOD` and `BASE`, any slice's hash by a closure, and each match of hashes confirmed letter by letter, so a collision never counts. O(n^2) expected |
| `deletions_z.kara` | the Z-function: a `z_array` of each suffix, taken as a slice, so `j` letters repeat at once exactly when `z[j] >= j`. O(n^2) |
| `deletions_iter.kara` | iterators: the ★ arm's rows, each by `map` and `collect` from the one after it, and `best[i]` by `filter` over the lengths that repeat, `map` and `max`, `unwrap_or(1)` when none does. O(n^2) |
| `deletions_solution.kara` | LeetCode's Rust template: `s.as_bytes()`, the whole square table of common prefixes as `vec![vec![0; n + 1]; n + 1]`, and `dp` over an inclusive range `1..=(n - i) / 2`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples; one
letter; two different; the constraints' run of one letter, 1000 long;
`ab` 500 times and `aab` 333 times; random words of 1000 letters from 2
and from 26, each letter often a copy of one just before it; and 3000
random words of 1 to 14 letters from the first 1 to 3, as a checksum and
the total. The largest cases hold 1000 letters, not the constraints'
4000, because the naive arm compares slices. `deletions.py` mirrors the
★ arm and its output is byte-identical, and the mirror was checked on
every word of 1 to 10 letters from `abc`, 88572 of them, against every
sequence of operations tried by plain recursion.

`check` first reports 1 error on the template, `struct Solution;`, and
`karac fix` carries it in one call, reporting 6 edits: `struct Solution;`
given its braces; `s.as_bytes()` written `s.bytes()`; each of the three
`vec!` written `Vec.filled`; and, once the template parses, `dp`'s
literal `1` written `1i32`, since it otherwise keeps the default `i64`
against the function's `i32` answer. The inclusive range, the `usize`
indices, `(0..n).rev()` and `max` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the operations tried every way by recursion on the string
left, which is always a suffix, each deletion of the first `i` letters
allowed when the substrings `[0, i)` and `[i, 2 i)` are equal as
strings; the most found for each suffix is kept in a `Map` by where it
starts. No common prefix is measured. It checks 300 random words of 1
to 12 letters from the first 1 to 3; then 30 of up to 60 letters from
2; then 30 of a random block of 1 to 4 letters repeated 2 to 6 times, a
random tail after it. Every letter of a random word is often a copy of
one just before it. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | every letter renamed to the next, `z` to `a`: the same answer |
| P3 | a letter the word lacks put in front: 1 |
| P4 | the word written twice: at least one more |
| P5 | the first letter doubled: at least one more, and no answer past the word's length |
| P6 | each arm agrees with at least three of the other five |

P2 holds because renaming is one-to-one, so it keeps every equality of
slices. P3 holds because the new first letter appears nowhere after it,
so no prefix repeats and only the whole deletion is left. P4 holds
because the first copy can be deleted in one operation, leaving the
word, and P5 because the extra letter can, and each operation deletes
at least one letter.

The differential prints `360 cases: checksum 272789196, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and runs the same recursion. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: a repeat needed past its length | P1 240, P4 221, P5 150, P6 240 |
| M5 | ★: the last repeat kept, not the best | P1 144, P5 128, P6 144 |
| M6 | ★: each match grown by two | P1 54, P6 54 |
| M9 | naive: single letters never deleted | P1 210, P4 26, P5 262, P6 210 |
| M10 | naive: only the first letters compared | P1 75, P6 75 |
| M11 | naive: the first start never tried | P1 360, P3 360, P4 360, P5 360, P6 360 |
| M12 | hash: every power 1 | P1 247, P4 360, P5 360, P6 247 |
| M15 | hash: the hash left negative | P1 4, P2 6, P4 78, P6 4 |
| M16 | hash: the whole deletion counted twice | P1 360, P3 360, P5 157, P6 360 |
| M17 | z: the box taken whole | P1 12, P6 12 |
| M19 | z: the last letter never matched | P1 141, P4 214, P5 26, P6 141 |
| M21 | z: the match grown two at a time | P1 76, P6 76 |
| M22 | iter: each letter matched against the one before | P1 203, P3 360, P6 203 |
| M24 | iter: the fewest kept | P1 145, P4 104, P5 128, P6 145 |
| M25 | iter: no repeat counted as nothing | P1 360, P3 360, P6 360 |
| M27 | solution: each match a prefix of one | P1 64, P4 203, P6 64 |
| M28 | solution: the longest half never tried | P1 169, P4 188, P5 53, P6 169 |


P1 and P6 kill all seventeen, P4 and P5 nine, P3 four and P2 one.

Fourteen are not kept, and every one fails exactly as a kept one. Six
never see a repeat, so every answer is 1, as the hash arm's every power
1 (M12) does: the ★ arm's match not counted (M1), the naive arm's second
slice one short and repeat counted as no deletion (M7, M8), the hash
arm's prefix hash a plain sum and hashes required to differ (M13, M14),
and the template's last start answered (M31). The ★ arm's whole deletion
not counted (M3) is one short everywhere, as the iter arm's no repeat
counted as nothing (M25). The ★ arm's longest half never tried (M4) is
the template's (M28). The z arm's repeat one short taken (M18) fails as
the iter arm's letter matched against the one before (M22), both
finding a repeat behind a letter that appears nowhere else. The z arm's
offset 1 never measured and the template's single letters never deleted
(M20, M30) fail as the naive arm's single letters never deleted (M9).
The iter arm's any shared first letter taken as a repeat (M23) fails as
the naive arm's only the first letters compared (M10); its rows never
handed on (M26) as the template's each match a prefix of one (M27), a
row of zeros after it leaving every common prefix at most one; and the
template's every start counted twice (M29) as the hash arm's whole
deletion counted twice (M16).

The first run had no valid choice: once the hash and naive arms took
the only three signatures each could, the ★ and iter arms and the
template had six signatures between them for their eight places. The
★ arm's next letter never compared and the iter arm's, a fifth and sixth
copy of the single letters never deleted, were replaced by each match
grown by two (M6) and each letter matched against the one before (M22);
a first replacement for the iter arm, a repeat of one letter never
tried, was a seventh copy.

## Verification

Every arm prints the same output as `deletions.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 2.9 to 8.3 s, the hash arm the
slowest: its closure is called twice for every length tried. The
differential takes 2.7 s under `karac __mir-run`, 0.9 s under `karac
__mir-llvm-asan` and 0.5 s under `karac run`.

## Benchmarks

The bench builds 8 words of 4000 letters, the constraints' longest,
once from its own generator, from `a` and `b`, each letter a copy of one
up to 3 before it half the time. It then makes 6 passes; each sets one
letter of every word, so no answer can be carried from one pass to the
next, then answers every word, folding the answer plus the pass into
the checksum. The bench uses the ★ arm, the two rows of common prefixes,
in all five languages. Every implementation prints `6 passes over 8
words of 4000 letters: checksum 652644516`. Each answer allocates its
three rows afresh in every language.

BENCHTAB
