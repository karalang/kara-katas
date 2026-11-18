# 2306. Naming a Company

You are given an array of strings `ideas` that represents a list of
names to be used in the process of naming a company. The process of
naming a company is as follows:

1. Choose 2 **distinct** names from `ideas`, call them `idea_A` and
   `idea_B`.
2. Swap the first letters of `idea_A` and `idea_B` with each other.
3. If **both** of the new names are not found in the original `ideas`,
   then the name `idea_A idea_B` (the **concatenation** of `idea_A` and
   `idea_B`, separated by a space) is a valid company name.
4. Otherwise, it is not a valid name.

Return *the number of **distinct** valid names for the company*.

```
ideas = ["coffee","donuts","time","toffee"]  ->  6
ideas = ["lack","back"]                      ->  0
```

**Constraints:** `2 <= ideas.length <= 5 * 10^4`;
`1 <= ideas[i].length <= 10`; `ideas[i]` consists of lowercase English
letters; all the strings in `ideas` are **unique**.

An idea is its first letter and its suffix. Swapping the first letters
of an idea with letter `a` and one with letter `b` makes valid names
exactly when the first suffix is not among `b`'s and the second not
among `a`'s; two ideas with the same letter swap into themselves, which
are ideas. So for each pair of letters the valid names are the suffixes
of `a` that `b` lacks times those of `b` that `a` lacks, twice for the
two orders, and every pair of ideas gives a different name. That is
`26 * 25 / 2` pairs of sets, at most `5 * 10^4` suffixes each walked
against the other set. The count reaches about `2.5 * 10^9`, so it is
an `i64`.

## Approaches

| file | mechanism |
|---|---|
| `names.kara` ★ | 26 `Set[String]`s of suffixes by first letter; for each pair of letters the shared suffixes counted by walking one set and looking each up in the other, and `2 * (|a| - shared) * (|b| - shared)` added |
| `names_naive.kara` | every ordered pair of ideas: both swapped words built with `f"{b[0..1]}{a[1..]}"` and looked up in a `Set[String]` of all the ideas. O(n^2) |
| `names_masks.kara` | a `Map[String, i64]` from each suffix to the bits of its first letters; a suffix with letter `a` and not `b` can move from `a` to `b`, so `movable[a][b]` counts those and each ordered pair of letters gives `movable[a][b] * movable[b][a]` |
| `names_sorted.kara` | no hashing: the ideas as `(suffix, letter)` pairs, `sort`ed so each suffix's letters lie in a run that folds into one mask, then counted as in the masks arm. O(n log n) |
| `names_iter.kara` | iterators: each letter's group `collect`ed into a `Set[String]` from the ideas that `filter` to it, then every ordered pair of different letters from `flat_map`, `map`ped to its product, the shared suffixes found by `filter` and `count`, and `sum`med |
| `names_solution.kara` | LeetCode's Rust template: `vec![HashSet::new(); 26]` of suffixes, `as_bytes()[0] - b'a'` as the index, and `intersection(&groups[b]).count()` for the shared suffixes; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; two ideas
of one letter each; one suffix under four letters; two letters sharing
no suffix; 600 ideas over all 26 letters; then 300 random cases of 2 to
40 ideas, first letters from up to 6 and suffixes of up to 2 letters
from 3, so that suffixes repeat across letters, with a checksum and
the counts in all. `names.py` mirrors the ★ arm and its output is
byte-identical. The count does not depend on the order in which a
`Set` is walked, so every arm's output is the same from run to run.

`karac fix` carries the template in one call, reporting 20 edits.
`check` first reports seven errors and offers 10 edits for them: the
`use std::collections::HashSet;` line deleted, since `Set` is in the
prelude; `struct Solution;` to `struct Solution {}`; the six brackets
of `Vec<String>` and `Vec<HashSet<String>>`; `HashSet::new` to
`HashSet.new`; `for idea in &ideas` to `for idea in ref ideas`; and the
`&` before `groups[b]` dropped. The other ten follow from those:
`HashSet` to `Set` in the type and the call; `vec![Set.new(); 26]` to
`Vec.filled(26, Set.new())`; `as_bytes()` to `bytes()`; the suffix of
`0i64` dropped; the three `as i64` dropped, since a length is already
an `i64`; `.count()` on the intersection to `.len()`, since Kāra's
`intersection` gives a `Set`, not an iterator; and, in the harness's
wrapper, a `.clone()` of the ideas that the call does not need. The
`as usize` index stands as Kāra.

The iter arm was first written with `(0..26).map(move |b| (a, b))`
inside its `flat_map`, as in Rust. Kāra infers a closure's captures and
has no `move`: `karac check` says so, and `karac fix` deletes the
keyword, one edit.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every ordered pair of distinct ideas has its first letters
swapped, and when neither swapped word is an idea the name, the two
words with a space between, goes into a `Set[String]`; the answer is how
many distinct names it holds. Nothing is grouped and nothing is
multiplied. It checks 300 random cases of 2 to 40 ideas, first letters
from up to 6 and suffixes of up to 2 letters from 3; then 30 whose
suffixes are only `""` and `"a"`, where nearly every suffix is shared;
then 30 of up to 150 ideas over 25 first letters and suffixes of up to
3 letters from all 26, where few are. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer is even and at most `n (n - 1)` |
| P3 | the ideas in reverse order: the same answer |
| P4 | every first letter moved 7 on in the alphabet, wrapping: the same answer |
| P5 | one idea more, `z` and a suffix no idea has: `2 n` names more |
| P6 | each arm agrees with at least three of the other five |

P5's new idea starts with `z`, which no case uses, and its suffix
`zzzzz` is in no group, so it pairs with every idea both ways.

The differential prints `360 cases: checksum 305584958, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
builds the same cases and the same set of names. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the first group's shared suffixes not taken off | P1 280, P4 26, P6 280 |
| M4 | ★: the suffixes not shared counted as shared | P1 351, P2 6, P4 26, P5 360, P6 351 |
| M5 | ★: neighbouring letters never paired | P1 287, P4 24, P5 26, P6 287 |
| M7 | naive: a name valid when either swapped word is new | P1 294, P6 294 |
| M9 | naive: each name counted twice | P1 296, P2 74, P5 360, P6 296 |
| M10 | naive: the first idea left out of the set | P1 360, P2 360, P3 240, P6 360 |
| M12 | masks: each suffix keeping only the letter it came with last | P1 324, P3 244, P5 338, P6 324 |
| M13 | masks: a suffix movable to a letter it already has | P1 351, P2 202, P5 360, P6 351 |
| M14 | masks: the moves one way squared | P1 360, P2 351, P5 360, P6 360 |
| M17 | sorted: the runs grouped by letter, not suffix | P1 342, P4 11, P5 223, P6 342 |
| M18 | sorted: each run's mask its last letter alone | P1 285, P4 26, P5 338, P6 285 |
| M19 | sorted: the pairs never sorted | P1 321, P6 321 |
| M22 | iter: each pair of letters in one order | P1 296, P2 141, P5 360, P6 296 |
| M23 | iter: every suffix counted shared | P1 296, P5 360, P6 296 |
| M24 | iter: the second group's shared suffixes not taken off | P1 294, P2 119, P6 294 |
| M28 | solution: one suffix too many shared | P1 360, P2 308, P5 360, P6 360 |
| M29 | solution: the first group taken twice | P1 360, P2 352, P4 360, P5 360, P6 360 |

P1 and P6 kill all seventeen, P5 twelve, P2 nine, P4 six and P3 two.
P5, one idea more under `z` with a suffix no one has, adds exactly `2 n`
names in a correct arm, and nearly any miscount of a pair of letters
shows in it; it misses the edits that leave a fresh suffix's pairs
right: a shared suffix not taken off on one side only, a name valid
when either word is new, the first idea left out of the set, the pairs
never sorted. P4, the letters moved
7 on, fails where an edit leans on which letters are neighbours or come
first: neighbouring letters never paired, a group taken twice, and the
edits whose error depends on how many of a group's suffixes the other
shares, which moving the letters past `z` and round to `a` reorders.
P2 fails for a count above `n (n - 1)` or odd, and P3, the ideas
reversed, only where the order of the ideas matters: the first idea
left out, and the last letter kept for a suffix.

Of the thirty-one, fourteen were not kept. The ★ arm's pairs counted
once (M1) and the template's (M27) fail as the iter arm's one order
(M22); the naive arm's first swapped word alone looked up (M8) as the
iter arm's second group's shared suffixes not taken off (M24); the
sorted arm's moves counted one way only (M21) and the iter arm's
groups of every letter up to their own (M25) as its every suffix
shared (M23). The whole idea grouped as its suffix in the ★ (M3), iter
(M26) and template (M30) arms all fail alike, and none is kept; so do
the ★ arm's letter `a` never paired (M6) and the masks arm's no suffix
movable from `a` (M15). The naive arm's swapped word keeping the
other's first letter too (M11), the masks arm's letters one bit higher
(M16), the sorted arm's idea after each run skipped (M20) and the
template's letters from `n` on never first (M31) fail apart from every
kept one, and were left out to keep three to an arm. M16 is the one
edit P1 and P6 miss: no case starts an idea with `z`, the one letter
that moves out of range, until P4 and P5 bring it in.

## Verification

Every arm prints the same output as `names.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, masks, sorted and template arms take
0.4 to 0.7 s, and the naive and iter arms 2.2 s: the naive arm builds
both swapped words for every pair of the 600 ideas, and the iter arm
`filter`s all the ideas once for each of the 26 letters. The
differential takes 24 s there, most of it the literal reading's set of
names for the 150-idea cases, and 1.0 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 lists of `5 * 10^4` distinct ideas once, a first
letter from all 26 and up to 6 more from the first 6, so that suffixes
repeat across letters, then makes 4 passes over all of them with the ★
arm in all five languages. Every implementation prints `4 passes over
10 lists of 5 * 10^4 ideas: checksum 342176131`. Each keeps 26 hash
sets of suffixes: Kāra's `Set[String]` and Rust's `HashSet<String>`,
both SipHash-1-3; Go's `map[string]struct{}`; Python's `set`; and, as C
has none, an open-addressing table of 8-byte keys under FNV-1a, its
filled slots listed for walking. The C build is the one whose hashing
differs, and the lightest.

BENCHTAB
