# 2213. Longest Substring of One Repeating Character

You are given a **0-indexed** string `s`. You are also given a
**0-indexed** string `queryCharacters` of length `k` and a
**0-indexed** array of integer **indices** `queryIndices` of length `k`,
both of which are used to describe `k` queries.

The `i`th query updates the character in `s` at index `queryIndices[i]`
to the character `queryCharacters[i]`.

Return *an array* `lengths` *of length* `k` *where* `lengths[i]` *is the
**length** of the **longest substring** of* `s` *consisting of **only
one repeating** character **after** the* `i`th *query is performed.*

```
s = "babacc", queryCharacters = "bcb", queryIndices = [1,3,3]  ->  [3,3,4]
s = "abyzz",  queryCharacters = "aa",  queryIndices = [2,1]    ->  [2,3]
```

**Constraints:** `1 <= s.length <= 10^5`; `s` consists of lowercase
English letters; `k == queryCharacters.length == queryIndices.length`;
`1 <= k <= 10^5`; `queryCharacters` consists of lowercase English
letters; `0 <= queryIndices[i] < s.length`.

A stretch of letters is summed up by its longest run from the start,
its longest run from the end and its longest run inside; two stretches
side by side join the first's end run to the second's start run when the
letters where they meet match. A segment tree of these sums mends the
log n nodes above a changed letter, and its root holds the answer.
O((n + k) log n).

## Approaches

| file | mechanism |
|---|---|
| `repeating.kara` ★ | a recursive segment tree over three `Vec[i64]`s passed as `mut ref`, `pull` joining two halves when the letters either side of the middle match |
| `repeating_runs.kara` | the runs of one letter in a `SortedMap` from start to end, and a second `SortedMap` counting the runs of each length; a query splits the run it lands in (found by `floor`) and joins the letter with a matching run on either side, and the longest is the counts' `last` key |
| `repeating_blocks.kara` | blocks of about sqrt(n) letters, each summed up by its three runs; a query rescans its own block, and the answer walks the blocks carrying the run that reaches each block's start. O(n + k sqrt n) |
| `repeating_struct.kara` | a `#[derive(Copy, Clone)] struct Stretch` of its end letters, length and three runs, with `join` (`ref self`), in a bottom-up tree padded to a power of two with empty stretches |
| `repeating_iter.kara` | the tree as a `Vec` of levels, each built from the one below by `chunks(2)`, `enumerate` and `map` over tuples, a lone last node carried up; the queries answered by a `map` whose closure sets the letter and mends one node a level |
| `repeating_solution.kara` | LeetCode's Rust template: two `String`s and a `Vec<i32>` in, `Vec<i32>` out, the word by `into_bytes`, a `struct SegTree` of three `Vec<i32>` built by `vec![0; 4 * n]`, its methods taking `&mut self` and `&[u8]` with `usize` indices; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one letter, a run broken in the middle and mended, two runs joined, and
letters set to what they were), each with its lengths; then a checksum
of 3000 random words of 1 to 30 letters with 1 to 30 queries, the
letters drawn from 2, 3 and 26 in turn; then the constraints' largest,
10^5 letters of `'a'` and `'b'` with 10^5 random queries, and 10^5 `'a'`s
with the middle letter broken and mended in turn. An index into 10^5
letters is drawn from two draws, since one stops at 32767.
`repeating.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one round of 53 edits: the
`Vec<..>`s to `Vec[..]`, every `usize` to `i64` and `as usize` to `as
i64`, `&mut self` to `mut ref self`, `&[u8]` to `Slice[u8]` and the
`&s` arguments to `s`, `into_bytes()` to `bytes().to_vec()` and
`as_bytes()` to `bytes()`, the three `vec![0; 4 * n]` to `Vec.filled(4 *
n, 0)`, `&&` to `and`, the `&c` and `|&x|` patterns dropped, `SegTree::`,
`Vec::` and `Solution::` to `.`, and `struct Solution;` to `struct
Solution {}`. The `(mid - lo + 1) as i32` casts stay as they are.

The iter arm was first written `levels[..].chunks(2).enumerate()`, as
Rust chains it. Kāra's `chunks` returns a `Vec` of slices, not an
iterator; the check says so and `karac fix` inserts the `.into_iter()`.
The differential's table of letters was first typed `[char; 26]`, Rust's
array type; the parser names Kāra's `Array[char, 26]` and `karac fix`
writes it.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: after each query the letter is set and every substring is
checked letter by letter for one repeating letter, the longest kept; no
runs and no tree. It checks 300 random words of 1 to 12 letters with 1
to 12 queries, the letters drawn from 2, 3 and 26 in turn; then 30 words
of one letter queried with two; then 30 with every query at one index.
All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the lengths are the statement read literally |
| P2 | one length for each query, each from 1 to the word's length |
| P3 | the word reversed and every index mirrored: the same lengths |
| P4 | every letter moved 7 on in the alphabet, round from z to a: the same lengths |
| P5 | the queries cut in two, the second half asked of the word the first half left: the same lengths |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 386978763, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that groups
the word after each query with `itertools.groupby`. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-seven edits to the differential, six to the ★ arm and to the
blocks and struct arms, nine to the runs arm, five to the iter arm and to
the template arm, each run under `karac __mir-llvm-run` and `karac
__mir-run`. Seventeen are kept, three to each Kāra arm and two to the
Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a run from the start joined past a break | P1 47, P3 72, P6 47 |
| M2 | ★: no run across the middle | P1 272, P6 272 |
| M6 | ★: the middle letter mended on the right | P1 131, P3 162, P5 44, P6 131 |
| M7 | runs: a run's count never taken away | P1 17, P5 13, P6 17 |
| M10 | runs: the shortest run reported | P1 254, P6 254 |
| M37 | runs: the word first cut at every letter | P1 207, P5 109, P6 207 |
| M13 | blocks: the run reaching a block not carried in | P1 165, P3 112, P6 165 |
| M16 | blocks: the block rescanned before the letter is set | P1 213, P3 109, P5 51, P6 213 |
| M17 | blocks: the runs inside a block not counted | P1 15, P3 25, P6 15 |
| M19 | struct: a run from the start joined past a mismatch | P1 163, P3 176, P6 163 |
| M21 | struct: the root never joined again | P1 182, P3 188, P5 53, P6 182 |
| M24 | struct: an empty right side taken whole | P1 255, P2 255, P6 255 |
| M25 | iter: a run from the start one letter short of whole | P1 123, P3 131, P6 123 |
| M27 | iter: the top level never mended | P1 218, P5 129, P6 218 |
| M28 | iter: the run from the start reported | P1 212, P3 220, P6 212 |
| M31 | solution: the longest of the right half lost | P1 105, P3 166, P6 105 |
| M33 | solution: the tree mended before the letter is set | P1 223, P3 97, P5 70, P6 223 |

P1 and P6 kill all seventeen, P3 eleven, P5 seven, P2 one and P4 none.
P4 moves every letter along the alphabet, and every arm compares letters
only for being equal, so no edit here can tell the letters apart. P3
reverses the word, so it kills the edits that treat the two ends of a
stretch apart: a run from the start but not from the end, or the right
half's length but not the left's. P5 cuts the queries in two, and kills
the edits whose answer depends on what earlier queries left behind: a
node or block not mended, a letter set after the mending, a count never
taken away, or the first runs cut at every letter, which a later query
mends only around itself (M6, M7, M16, M21, M27, M33, M37). P2 kills only the struct
arm's empty right side taken whole (M24), which pads the tree with
lengths of 0.

Of the thirty-seven, twenty were not kept. Fourteen are killed and fail
as a kept one does or their own way: the iter arm's run across the
middle dropped (M29) as the ★ arm's M2, and the ★ arm's root never
mended (M5) as the iter arm's M27; the ★ and struct arms' single letter
taken as a run of 0 (M4, M23) fail alike, and so do the ★ arm's and the
template's right half one letter longer (M3, M32), and none of the four
is kept; nine fail their own way and are left out for the count of
three (two for the template): the runs arm's join to the right or to
the left dropped and its lengths counted at most 6 (M8, M36, M35), the
blocks arm's whole block not carried through and its run from the start
cut to one letter (M14, M15), the struct arm's run across a mismatch and
its last letter taken from the left (M20, M22), and the template's
indices capped at 5 and its leaf's run from the end 0 (M30, M34). Two
stop with a panic, both in the runs arm, whose map no longer covers the
word: a join to the right ending at its first letter (M11) finds no run
at a later letter, and a run's length counted one more (M12) looks up a
length never counted. Three survive, and each is equivalent. The runs
arm's letter set to itself split and joined again (M9) puts back the
very runs it took out. The blocks arm's blocks of 2 letters (M18) only
changes the cost, since the walk is right for any width. The iter arm's
last node's end past the word (M26) reads a wrong length only for the
last node of a level, whose run from the end is never used: a last node
is a left half only when it stands alone, and then it is carried up as
it is.

## Verification

Every arm prints the same output as `repeating.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the tree arms take 10 s to 13 s, the runs arm
22 s, as the interpreter keeps a `SortedMap` as one sorted array whose
inserts and removals move up to 5 * 10^4 runs, and the blocks arm 106 s,
rescanning a block of 317 letters and walking 316 blocks for each of
the 2 * 10^5 queries of the long words; the differential takes 1.6 s.

## Benchmarks

The bench draws 6 words of 10^5 letters once, from 2, 3 and 26 letters
in turn, each with 10^5 random queries, then answers every query with
the ★ arm in all five languages, the checksum running over every length.
Every implementation prints `6 words of 10^5: checksum 240887663`.

BENCHTAB
