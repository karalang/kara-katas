# 2456. Most Popular Video Creator

You are given two string arrays `creators` and `ids`, and an integer
array `views`, all of length `n`. The `i`th video on a platform was
created by `creators[i]`, has an id of `ids[i]`, and has `views[i]`
views.

The **popularity** of a creator is the **sum** of the number of views
on **all** of the creator's videos. Find the creator with the
**highest** popularity and the id of their **most** viewed video.

- If multiple creators have the highest popularity, find all of them.
- If multiple videos have the highest view count for a creator, find
  the lexicographically **smallest** id.

Return *a 2D array of strings* `answer` *where* `answer[i] =
[creatorsi, idi]` *means that* `creatorsi` *has the **highest**
popularity and* `idi` *is the id of their most popular video.* The
answer can be returned in any order.

```
creators = ["alice","bob","alice","chris"], ids = ["one","two","three","four"], views = [5,10,5,4]
  ->  [["alice","one"],["bob","two"]]
creators = ["alice","alice","alice"], ids = ["a","b","c"], views = [1,2,2]
  ->  [["alice","b"]]
```

**Constraints:** `n == creators.length == ids.length == views.length`;
`1 <= n <= 10^5`; `1 <= creators[i].length, ids[i].length <= 5`;
`creators[i]` and `ids[i]` consist only of lowercase English letters;
`0 <= views[i] <= 10^5`.

Each creator needs a running total and a running best video, the best
replaced by a video with more views, or as many and a lesser id. One
pass fills both, and the answer is every creator whose total is the
largest, with their best. The answer may come in any order, so every
arm returns it sorted, by creator and then by id, and the outputs are
compared as sorted lists.

## Approaches

| file | mechanism |
|---|---|
| `creator.kara` ★ | one pass: a `Map` from each creator to `(total, top views, id)`, updated by `match` on `get`; then the largest total, and every creator at it, sorted. O(n) and the answer's sort |
| `creator_naive.kara` | the statement read directly: each video's creator's popularity summed over the whole list, the highest found, and for each creator at it, answered once at their first video, the list scanned again for their best video. O(n^2) |
| `creator_sorted.kara` | sorting: the indices sorted by `sort_by_key` on `(creator, -views, id)`, so each creator is a run whose first video is their best; each run summed, and the runs at the largest sum answered in creator order. O(n log n) |
| `creator_ordered.kara` | ordered maps: a `SortedMap` of totals and one of best `(views, id)` pairs, so the answer is read off in creator order with no sort. O(n log n) |
| `creator_iter.kara` | iterators: the indices folded by `fold(Map.new(), ..)` into a `Map` from creator to total, best views and best id; the largest total by `map` and `max`, the creators at it by `filter` and `map`, collected and sorted. O(n) and the answer's sort |
| `creator_solution.kara` | LeetCode's Rust template: two `HashMap`s, the totals by `*total.entry(..).or_insert(0) += views[i] as i64` and the best video through the reference `entry(..).or_insert(..)` returns, replaced by `*e = ..`; the answer by `filter(\|(_, &t)\| ..)` and `vec![..]`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines, each answer as `creator/id` pairs:
LeetCode's two examples; one video of no views; one creator's three
equal videos, the least id `ab` taken; two creators tied, each with
their best; one creator's three small videos above another's one large
one, their tie broken to `a`; then 2000 videos by creators of up to 3
letters from 3, views up to `10^5`, and 2000 by creators of one letter
from 2, views up to 3, full of ties, each as a count and checksum; and
3000 random lists of 1 to 8 videos, as a checksum. `creator.py` mirrors
the ★ arm and its output is byte-identical, and the mirror was checked
on 50000 random lists of up to 9 videos against every creator's
popularity summed and their videos sorted by views and id. The random
lists stop at 2000 videos, not the constraints' `10^5`, because the
naive arm is quadratic; the bench takes `10^5`.

`check` first reports 13 errors on the template, and `karac fix`
carries it in one call, reporting 26 edits: `use
std::collections::HashMap;` deleted, since `Map` is in the prelude; the
angle brackets of every `Vec<..>` and `HashMap<..>` made square, `>>`
as one; both `HashMap::new` written with `.`; `||` and `&&` written `or` and `and`;
the `&` of the closure pattern `|(_, &t)|` dropped; `struct Solution;`
given its braces; and, once the template parses, each `HashMap` name
written `Map`, four edits; `views[i] as i64` written `views[i]`, since an `i32`
widens to an `i64` with no cast, and `vec![c.clone(), ..]` written as
the list literal `[c.clone(), ..]`. `*total.entry(..).or_insert(0) +=`,
`let e = best.entry(..).or_insert(..)` with `e.0`, `e.1` and `*e = ..`,
`*total.values().max().unwrap()` and `best[c].1` stand as Kāra. The
views fit an `i32`, as LeetCode's signature has them; the other arms
take `i64`, and the template's answer is sorted by its caller, since
it walks a `Map`.

The iter arm's `fold(Map.new(), ..)` was refused when the arm was
written: the accumulator's type, fixed by the `let`'s annotation, did
not reach the closure, so `match m.get(c)` with a tuple pattern was
called non-exhaustive. It checks on kara 2962b05044, and the change
that carried it was not identified, so it has no ledger row.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the creators listed once each, in order, by a `SortedSet`;
each one's popularity summed over every video; the highest found; and
for each creator at it, the most views among their videos found first,
then the least id among the videos with that many. No running total or
best is kept. It checks 300 random lists of 1 to 10 videos, creators
and ids of 1 to 2 letters from 3, views up to 5; then 30 of up to 40
videos, creators of up to 3 letters from 3, ids of up to 5 from 26,
views up to 49999; then 30 of up to 40 videos, creators and ids of one
letter from 2, views up to 2, full of ties. All 360 are drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the videos in reverse order: the same answer |
| P3 | every view doubled: the same answer |
| P4 | every video listed twice: the same answer |
| P5 | the first answered creator's best video raised by one view: that creator and video alone |
| P6 | each arm agrees with at least three of the other five |

P2 holds because sums and the best by views and id ignore order. P3
and P4 hold because doubling every view, or every video, doubles every
total and keeps which video has the most views. P5 holds because the
raised creator's total is then the only largest, and the raised video
has more views than any other of theirs. The middle cases stop at 49999
views so that P3 and P5 stay within the constraints' `10^5`.

The differential prints `360 cases: checksum 454401773, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and takes each creator's best by sorting. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: a better video resets the total | P1 62, P2 104, P4 45, P6 62 |
| M4 | ★: the least total | P1 352, P5 360, P6 352 |
| M6 | ★: each creator's first video left out of the total | P1 149, P2 75, P4 120, P5 104, P6 149 |
| M8 | naive: every video of a creator answered | P1 226, P4 360, P5 219, P6 226 |
| M10 | naive: the search started at the first video | P1 19, P2 37, P5 7, P6 19 |
| M11 | naive: the last of equal views | P1 26, P2 47, P6 26 |
| M12 | sorted: the least viewed first | P1 160, P5 41, P6 160 |
| M13 | sorted: ties left in list order | P1 27, P2 47, P6 27 |
| M15 | sorted: the run's last video | P1 194, P5 51, P6 194 |
| M17 | ordered: the most viewed video for the total | P1 131, P6 131 |
| M19 | ordered: the least total | P1 313, P5 185, P6 313 |
| M21 | ordered: the best stored one view higher | P1 37, P2 68, P3 18, P6 37 |
| M22 | iter: a worse video not added | P1 60, P2 116, P6 60 |
| M23 | iter: the first video's views forgotten | P1 66, P2 139, P4 66, P6 66 |
| M24 | iter: the best video's views for the total | P1 194, P4 248, P5 149, P6 194 |
| M29 | solution: the id never replaced | P1 125, P2 196, P6 125 |
| M31 | solution: the views taken modulo 3 | P1 183, P3 209, P5 245, P6 183 |

P1 and P6 kill all seventeen, P2 and P5 nine each, P4 five and P3
two.

Fourteen are not kept. Three fail exactly as a kept one: the ★ arm's
least viewed video (M2) as the sorted arm's least viewed first (M12);
the naive arm's other creators' views (M7) as the ordered arm's least
total (M19), both answering the creators with the least popularity;
and the ordered arm's ties keeping the first (M18) as the sorted arm's
ties left in list order (M13), which is the same tie broken another
way. Eleven fail apart from every kept one, though some fail alike,
and were left out because those arms keep their share already: the ★,
naive and template arms' greatest id on a tie (M1, M9, M28), which
fail alike, as do the ★, sorted and template arms' totals one short
admitted (M5, M16, M30), the sorted and template arms' videos counted
(M14, M27), and the ordered and iter arms' every creator but the most
popular and creators below the most (M20, M25); and the iter arm's
creator for the id (M26).

## Verification

Every arm prints the same output as `creator.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

TIMES

## Benchmarks

The bench builds 10 lists of `10^5` videos, the constraints' largest,
once from its own generator: creators of 3 letters, so about 17000 of
them, ids of 5, views up to `10^5`. It then makes 16 passes; each sets
one view of every list from the checksum so far, so no answer carries
over, then answers every list, folding the letters of every pair, and
then the pass, into the checksum. The bench uses the ★ arm, one pass
keeping each creator's total and best video, in all five languages.
Every implementation prints `16 passes over 10 lists of 10^5 videos:
checksum 891136863`. The table is the language's own hash map, `Map` in
Kāra, `HashMap` in Rust, `map` in Go and `dict` in Python; C has none,
and uses an open-addressing table of `2^15` slots keyed by the name,
cleared for every answer. The creator's name is copied into the table
for every video in Kāra and Rust, as the ★ arm does with `clone`.

BENCHTAB
