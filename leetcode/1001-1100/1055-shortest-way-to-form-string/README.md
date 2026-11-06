# 1055. Shortest Way to Form String

A **subsequence** of a string is a new string that is formed from the
original string by deleting some (can be none) of the characters without
disturbing the relative positions of the remaining characters.

Given two strings `source` and `target`, return the minimum number of
**subsequences** of `source` such that their concatenation equals
`target`. If the task is impossible, return `-1`.

```
source = "abc", target = "abcbc"  ->  2    ("abc" + "bc")
source = "abc", target = "acdbc"  ->  -1   (no "d" in source)
source = "xyz", target = "xzyxz"  ->  3    ("xz" + "y" + "xz")
```

**Constraints:** `1 <= source.length, target.length <= 1000`; both are
lowercase English letters.

## Approaches

Each piece is a subsequence of `source`, and a piece that takes as much of
`target` as one walk along `source` can match is never worse than a
shorter one: whatever the shorter piece leaves, the longer one has already
matched, and the rest can be formed in no more pieces. So the greedy walk
is optimal, and the answer is `-1` exactly when `target` has a letter
`source` lacks.

| file | mechanism |
|---|---|
| `shortest_way.kara` ★ | walk `source` from the start, matching the next letter of `target` wherever it comes; a new piece when the walk ends, `-1` when a walk matches nothing. O(n m) for a source of n and a target of m |
| `shortest_way_next.kara` | a table `next[i][c]` of the first place at or after `i` holding `c`, built from the back in a `Vec` of `[i64; 26]` rows; one look-up a target letter. O(26 n + m) |
| `shortest_way_search.kara` | each letter's places in order, and the first at or after where the piece has got to by `partition_point`. O(n + m log n) |
| `shortest_way_iter.kara` | feasibility by `target.chars().all(..)` and `contains`, then each letter found by `s[pos..].iter().position(..)`, starting again at place 0 when the rest of `source` has none. O(n m) |
| `shortest_way_reach.kara` | `best[i]`, the fewest pieces forming the first `i` letters, each prefix reached offering one more piece to every place its walk can match up to; walks jump through a next-place table. It does not assume the greedy walk is best. O(26 n + m L) for pieces of up to L letters |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 16 lines: the answers for LeetCode's three
examples and seven more; how many of 3000 random pairs of 1 to 8 letters
of 3 can be formed, the total of their answers and a checksum of every
answer, and the same for 300 pairs of 1 to 1000 letters of 26; and four
answers at the limit, a source of 1000 random letters (every letter but
z) against itself reversed, itself, 1000 y's and itself reversed with a z
on the end. `shortest_way.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way of cutting `target` into pieces is tried, each piece
checked as a subsequence of `source` on its own, and the fewest pieces
kept, or `-1` when no cutting works. It checks 3000 random pairs: 2000 of
a source of 1 to 6 letters and a target of 1 to 12, both of 3 letters,
and 1000 of 1 to 20 and 1 to 40 of 6 letters.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is -1 exactly when the target has a letter the source lacks, otherwise from 1 to the target's length, and 1 exactly when the target is a subsequence of the source |
| P3 | the target twice takes at least as many pieces and at most twice as many |
| P4 | every letter moved on by 7 through the alphabet, in both strings, leaves the answer |
| P5 | the source twice takes half the pieces, rounded up |
| P6 | each arm agrees with at least two of the other four |

P3 holds because the pieces for the target twice, cut where the first copy
ends, form each copy, and the pieces for one copy, used twice, form both.
P5 holds because one greedy walk along the source twice is two walks along
the source, one after the other. P4 holds because no arm reads a letter
for anything but which letter it is.

The differential prints `3000 pairs: checksum 573004974, 90000 checks over
5 arms: 0 failures` under `karac __mir-run` (6.7 s), `karac
__mir-llvm-run` and `karac __mir-llvm-asan` with no error, and the same
line under `karac run` and from a `karac build` binary. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Fifteen are kept, three to each
arm. All thirty are killed, each fails the same way under both backends,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a letter matched by any other | P1 2264, P2 1606, P6 2264 |
| M2 | ★: the source walked backwards | P1 545, P2 73, P6 545 |
| M3 | ★: the last letter never matched | P1 761, P2 363, P3 515, P6 761 |
| M4 | next: the table built from the front | P1 1125, P2 1121, P5 18, P6 1125 |
| M5 | next: two pieces at a restart | P1 950, P2 298, P3 727, P5 540, P6 950 |
| M6 | next: a letter missing from the rest of the source taken as missing | P1 950, P2 950, P3 182, P5 168, P6 950 |
| M7 | search: the place at `pos` skipped | P1 752, P2 127, P5 60, P6 752 |
| M8 | search: a restart forgets the letter it took | P1 638, P5 309, P6 638 |
| M9 | search: a restart one place early | P1 1064, P2 387, P5 594, P6 1064 |
| M10 | iter: the place counted from the start, not from where the piece got to | P1 715, P2 227, P3 21, P5 468, P6 715 |
| M11 | iter: a restart at the letter's last place | P1 440, P3 216, P5 668, P6 440 |
| M12 | iter: the letter's last place in the rest | P1 558, P2 82, P5 964, P6 558 |
| M13 | reach: the most pieces, not the fewest | P1 1212, P2 1212, P6 1212 |
| M14 | reach: two pieces for one | P1 1212, P2 703, P5 672, P6 1212 |
| M15 | reach: a piece skips its first letter | P1 1224, P2 547, P3 203, P5 538, P6 1224 |

P1 and P6 kill all fifteen, P2 thirteen, P5 eleven, P3 six and P4 none.
P4 kills nothing because no edit kept, like no arm, reads a letter for
more than which one it is. M8 and M11 escape P2: their answers stay in
range, since the edits change how far a piece reaches, not whether a
letter is there. P3 sees the edits whose answer for the target twice is
not between one and two times the answer, which takes an edit that treats
the end of the target, or the place a piece restarts, in its own way (M3,
M5, M6, M10, M11, M15).

The other fifteen fail as others do. One fails exactly as a kept one: the
next arm with each row of its table knowing only its own letter, as M4.
Twelve fail in groups with no kept member: returning the pieces so far
for a missing letter (★, search); one piece too many (★, iter, reach);
one letter a walk, or pieces of one letter (★, reach); one piece too few
(next, search); and the matched place used again (next, iter, reach).
Two fail in ways of their own: the search arm using its matched place
again, and the iter arm not counting a restart.

## Verification

Every arm prints the same output as `shortest_way.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file. The runs used a release build of kara `5b52632bad`.
Under `karac __mir-run` the arms take 1.1 s (next) to 5.1 s (reach).

The ★ arm, written the way Rust writes it, drew three fixes: `&&` to
`and`, the `&c` pattern dropped, and `as_bytes()` to `bytes()`. The other
four reached a clean check through `karac fix` (`Vec<..>` to `Vec[..]`,
`Vec::new` and `i64::MAX` to `.`, `vec![..]` to `Vec.filled`, `!` to
`not`, `&` patterns dropped, `&places[..]` to `ref places[..]`, and
`contains(c)` to `contains(c.to_string())`), except for one gap:

- The search arm's `Vec<Vec<usize>>`, spelled `Vec[Vec[usize]]` by `karac
  fix`, then drew four `i64`/`usize` coercion and comparison errors with
  no fix. Kāra keeps `usize` for FFI and indexes with `i64` (design.md
  §5), so the fix is to write `Vec[Vec[i64]]`, as the arm now does by
  hand. Filed as kara B-2026-11-06-3.

## Benchmarks

The bench builds 100 sources of 1000 letters, each with a target of 10000,
once in all five languages, the letters random from the first 20 of the
alphabet, then runs the ★ arm on every pair 10 times. Every implementation
prints `100 pairs of 1000 and 10000 letters, 10 rounds: total 200330,
checksum 134548651`. Each target takes about 200 pieces, so the work is
about 200 million steps along a source, each a compare of one letter of
the source against the target's next.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `5b52632bad` on LLVM 22:

| | time | median |
|---|---|---|
| Go | 0.334 to 0.382 s | 0.339 s |
| Kāra (`karac build`) | 0.574 to 0.591 s | 0.583 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.570 to 0.589 s | 0.584 s |
| C (`clang -O3`) | 0.572 to 0.605 s | 0.585 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.576 to 0.599 s | 0.586 s |
| Rust (`rustc -O`) | 0.580 to 0.606 s | 0.588 s |
| Python | 10.0 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.576 s) is below its real time.

Kāra, C and both Rust builds are within 1% of each other. Go takes 0.58
times their time, and the disassembly shows why. Clang compiles C's match
to `i += t[i] == s[k]` without a branch (`sete` then `add`), and Kāra's
binary has the same `sete`. That puts the load of `t[i]` on a chain that
runs from each letter of the source to the next. Go's compiler keeps a
branch (`JNE`) that is taken only about one time in twenty, so the next
compare does not wait for the last one.
