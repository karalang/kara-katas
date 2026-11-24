# 1311. Get Watched Videos by Your Friends

There are `n` people, each person has a unique id between `0` and `n-1`.
Given the arrays `watchedVideos` and `friends`, where `watchedVideos[i]`
and `friends[i]` contain the list of watched videos and the list of
friends respectively for the person with `id = i`.

Level **1** of videos are all watched videos by your friends, level **2**
of videos are all watched videos by the friends of your friends and so
on. In general, the level `k` of videos are all watched videos by people
with the shortest path **exactly** equal to `k` with you. Given your `id`
and the `level` of videos, return the list of videos ordered by their
frequencies (increasing). For videos with the same frequency order them
alphabetically from least to greatest.

```
watchedVideos = [["A","B"],["C"],["B","C"],["D"]], friends = [[1,2],[0,3],[0,3],[1,2]], id = 0, level = 1  ->  ["B","C"]
watchedVideos = [["A","B"],["C"],["B","C"],["D"]], friends = [[1,2],[0,3],[0,3],[1,2]], id = 0, level = 2  ->  ["D"]
```

**Constraints:** `2 <= n <= 100`, `0 <= watchedVideos[i].length <= 100`,
`1 <= watchedVideos[i][j].length <= 8`, `0 <= friends[i].length < n`,
`0 <= friends[i][j] < n`, `0 <= id < n`, `1 <= level < n`, and if
`friends[i]` contains `j`, then `friends[j]` contains `i`.

The arms are `fn watched_videos_by_friends(watched_videos:
Vec[Vec[String]], friends: Vec[Vec[i64]], id: i64, level: i64) ->
Vec[String]`.

## Approaches

| file | mechanism |
|---|---|
| `watched_videos_by_friends.kara` ★ | a breadth-first walk from `id` a level at a time, the people of each level those of the level before's friends not yet seen, `level` times; the videos of the people left counted in a `Map`, then sorted as (count, title) pairs, so that a tie in count goes to the title first in order. O(n + friendships + v log v) |
| `watched_videos_by_friends_distances.kara` | every person's distance from `id` found by one breadth-first walk in a `VecDeque`, the people at exactly `level` picked out; their videos counted in a `SortedMap`, which hands the titles over in order, and a stable sort by count alone then keeps that order within a tie. O(n + friendships + v log v) |
| `watched_videos_by_friends_relax.kara` | every distance brought down by sweeping every friendship, each sweep letting a person's distance be one more than a friend's, until a sweep changes nothing; no map at all: the videos of the people at the level gathered and sorted, so that equal titles sit together, each run of them made a (count, title) pair, and the pairs sorted. O(n friendships + v log v) |
| `watched_videos_by_friends_sets.kara` | each level a `Set` of people, the next level the friends of its people taken out of the `Set` of everyone seen so far; the videos counted in a `Map` and the titles sorted by a comparison that looks at the count first and the title only on a tie. O(n + friendships + v log v) |
| `watched_videos_by_friends_solution.kara` | a Rust solution as LeetCode's Rust users write it (a level-by-level walk in a `VecDeque<usize>`, `for _ in 0..q.len()` draining one level a round, the videos counted in a `HashMap<&String, i32>` that borrows the titles, then `into_iter().collect()` into pairs sorted by `a.1.cmp(&b.1).then(a.0.cmp(b.0))`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, a level past
everyone reached (nothing, shown `-`), a friend's friend who is also a
friend, counted at level 1 only, a tie in count broken by title, and a
video watched twice by one person, counted twice (`B,C D - w c,ab,bb
j,k,m`); then 600 random groups of 2 to 40 people, each pair friends with
a chance of 1 in 2 to 1 in 12, each person watching 0 to 6 videos from a
pool of 3, 12 or 60 titles, asked from a random person at a random level,
most of them small (`600 random groups: 3185 videos, checksum
760461302`). `watched_videos_by_friends.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the four Kāra arms checked clean as first written. The
Rust arm takes one round of 40 fixes by `karac fix`'s count, from 20
errors: the `use std::collections::{HashMap, VecDeque};` line deleted,
since both are in Kāra's prelude, `struct Solution;` to `struct Solution
{}`, `Vec<..>` to `Vec[..]`, `vec![false; n]` to `Vec.filled(n, false)`,
`HashMap<&String, i32>` to `Map[ref String, i32]` and `Vec<(&String,
i32)>` to `Vec[(ref String, i32)]`, `for &v in &friends[u]` to `for v in
ref friends[u]`, `for &u in` to `for u in`, `&watched_videos[u]` to `ref
watched_videos[u]`, `!` to `not`, `&b.1` to `b.1`, `::` to `.`, and the
wrapper's `|&x|` to `|x|`. Its output matches on the first run. The map
of borrowed titles is the surface this kata found on 2026-11-21: `karac
check` passed it, and `into_iter` then failed the MIR borrow check at
`run` (B-2026-11-21-60, fixed since).

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every shortest path found by Floyd and Warshall's sweep over a
table of distances, every video of the people at exactly `level`
gathered, each title counted by looking through all of them, and the
least (count, title) taken again and again. 2000 groups of 2 to 9 people
watching 0 to 4 videos each from 1 to 4 titles (`a`, `ab`, `b`, `ba`), so
that ties are common, asked from a random person at a random level, in
four kinds, 500 each: each pair friends with a chance of 1 in 2; 1 in 4,
so that some are out of reach; a chain through everyone in a random order
with one more friendship, so that the levels run deep; and a star around
person 0 with a chance of 1 in 5 for the rest, each watching up to 6.
Every group, level and renumbering is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | everyone renumbered: the same answer |
| P3 | every list of videos and of friends back to front: the same answer |
| P4 | every video watched twice: the same answer |
| P5 | one more person, a friend of `id` alone, who watched `zz`: the same answer once `zz` is taken out, and `zz` in it at level 1 only |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 groups: checksum 110967660,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under both
`karac __mir-llvm-run` and `karac __mir-run`. Every one is killed, fails
the same way under both backends and not by a crash, and no two fail the
same checks, so all ten are kept.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `id` never marked seen | P1 211, P5 28, P6 844 |
| M2 | ★: every title counted once | P1 251, P6 1004 |
| M3 | distances: the people past the level taken too | P1 248, P6 248 |
| M4 | distances: the titles never sorted by count | P1 251, P6 251 |
| M5 | relaxing: one sweep only | P1 277, P2 154, P6 277 |
| M6 | relaxing: the videos not sorted before the runs are counted | P1 309, P2 90, P3 135, P6 309 |
| M7 | sets: a level's people never marked seen | P1 766, P6 766 |
| M8 | sets: a tie going to the later title | P1 253, P6 253 |
| M9 | solution: one level short | P1 1137, P5 1135, P6 1137 |
| M10 | solution: the queue taken from the back | P1 189, P3 224, P6 189 |

P1 and P6 kill all ten, P2, P3 and P5 two each; P4 kills none. Only the
relaxing arm visits people in the order of their numbers, in its sweeps
and in gathering their videos, so only its edits fail a renumbering
(P2). Reading the lists back to front (P3) changes which friend the Rust
arm's queue hands back first once it is taken from the back (M10), and
which titles the unsorted runs split (M6). A new friend of `id` (P5)
sits at level 1 and nowhere else, so it catches the arm one level short
(M9) and the ★ arm whose `id` comes back two levels out through the new
friend (M1). Doubling every video
(P4) doubles every count and keeps their order, and no edit here looks
at a count's size rather than its order.

## Benchmarks

The bench builds 50 groups of 100 people, the constraints' most, each
pair friends with a chance of 1 in 25 and each person watching 100
videos, the constraints' most, from 400 titles of 1 to 8 letters, once
from its own generator; then makes 200 passes, each changing one video of
one person in every group and asking from a person at a level from 1 to
3, all chosen by the checksum so far, so no answer carries over,
answering it with the ★ arm and folding the answer's length, its first
and last titles and the pass into the checksum. The count is the
language's own map: `Map` in Kāra, `HashMap` in Rust, `map` in Go and
`dict` in Python; C counts in an open-addressing table of its own over
FNV-1a hashes, keyed by pointers to the shared titles, as Go's and
Python's maps share theirs, where Kāra and Rust clone each title into the
map. Every implementation prints `200 passes over 50 groups of
100: checksum 895756150`.

BENCHTAB
