# 1152. Analyze User Website Visit Pattern

You are given two string arrays `username` and `website` and an integer
array `timestamp`. All the given arrays are of the same length and the
tuple `[username[i], timestamp[i], website[i]]` indicates that the user
`username[i]` visited the website `website[i]` at time `timestamp[i]`.

A **pattern** is a list of three websites (not necessarily distinct). The
**score** of a pattern is the number of users that visited all the
websites in the pattern in the same order they appeared in the pattern.
The websites need not be visited contiguously.

Return the pattern with the largest score. If there is more than one
pattern with the same largest score, return the lexicographically
smallest such pattern.

```
username = ["joe","joe","joe","james","james","james","james","mary","mary","mary"],
timestamp = [1,2,3,4,5,6,7,8,9,10],
website = ["home","about","career","home","cart","maps","home","home","about","career"]
    ->  ["home","about","career"]
username = ["ua","ua","ua","ub","ub","ub"], timestamp = [1,2,3,4,5,6],
website = ["a","b","a","a","b","c"]
    ->  ["a","b","a"]
```

**Constraints:** `3 <= username.length <= 50`; `1 <= username[i].length
<= 10`; `timestamp.length == username.length`; `1 <= timestamp[i] <=
10^9`; `website.length == username.length`; `1 <= website[i].length <=
10`; `username[i]` and `website[i]` consist of lowercase English letters;
at least one user visited at least three websites; all the tuples
`[username[i], timestamp[i], website[i]]` are unique.

The arms are `fn most_visited_pattern(username: Vec[String], timestamp:
Vec[i64], website: Vec[String]) -> Vec[String]`.

## Approaches

A user scores a pattern once however many ways their visits follow it,
so every arm collects each user's patterns as a set before counting: the
three-visit subsequences of the user's sites in time order, duplicates
dropped.

| file | mechanism |
|---|---|
| `most_visited_pattern.kara` ★ | maps: the visits put in time order by `sort_by_key`, a `Map` from each user to their sites, a `Set` of each user's patterns as tuples, a `Map` of scores, and the best by score and then the smaller tuple. O(u k^3) for u users of at most k visits |
| `most_visited_pattern_sorted.kara` | sorted lists: the visits sorted as (user, time, site) tuples so each user is one run in time order, each user's patterns sorted and `dedup`ed, then every user's patterns sorted together so each pattern is one run whose length is its score; the first longest run wins, the runs coming in pattern order. O(u k^3 log) |
| `most_visited_pattern_ordered.kara` | ordered collections: a `SortedMap` from each user to a `SortedMap` of their visits by time, each user's patterns in a `SortedSet`, the scores in a `SortedMap`, walked in pattern order keeping the first strictly higher score, so a tie never needs the patterns compared. O(u k^3 log) |
| `most_visited_pattern_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `timestamp: Vec<i32>`, the visits zipped and sorted by time, a `HashMap<String, Vec<String>>` of each user's sites, a `HashSet<Vec<String>>` of their patterns, a `HashMap` of scores, and the best by `max_by` on the score then the reversed pattern), carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, nine properties |

Every arm prints the same 8 lines: LeetCode's two examples; one user
whose visits come out of time order (`[a, b, c]`); two users whose
visits come in reverse time order (`[p, r, q]`); two users whose
patterns all score one, the smallest belonging to the second (`[x, y,
z]`). Then 2000 random problems of 3 to 50 visits by 1 to 6 users to 2
to 5 sites, with how many answers start at each site and a checksum
(`2000 random problems: first sites [1377, 370, 158, 66, 29], checksum
564875726`), and two problems at the constraints' end: one user visiting
50 sites in turn, 19,600 patterns all scoring one (`[s10, s11, s12]`),
and 16 users each visiting `c`, `a`, `b`, the first then visiting `a`
twice more (`[c, a, b]`). The harness names users and sites with digits
(`u0`, `s10`), which the letters-only constraint leaves out and no arm
reads. `most_visited_pattern.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every pattern of three of the sites, in order, scored by the
users who visited its first site, then its second later, then its third
later still, looked for among all triples of visits; the first of the
highest scores wins. It checks 2000 problems of 3 to 20 visits in four
kinds of 500: 1 to 4 users and 2 to 4 sites; 2 to 5 users and 2 sites,
so that many patterns tie; 2 to 4 users who each follow one route of 3 to
5 sites, half of them with one site changed, so that scores run high; and
1 to 3 users visiting 2 to 5 named sites (`home`, `about`, ...) at times
up to 10^9. Visits are dealt out in a random order. Every random choice
the properties make is drawn before any arm answers. The best score is 1
in 1322 problems, 2 in 421, 3 in 167 and 4 in 90, and 1269 problems have
two or more patterns at the best score.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | the visits in another order give the same answer |
| P3 | each time replaced by its rank, spread by a gap from an offset, gives the same answer |
| P4 | the users renamed, the k-th to appear to another name, give the same answer |
| P5 | the sites renamed in order, the k-th smallest to `s{offset + gap * k}`, give the answer renamed |
| P6 | one more user visiting the answer's three sites after everyone gives the same answer |
| P7 | every user twice, the copies under new names and visiting later, gives the same answer |
| P8 | some user followed the answer |
| P9 | no fewer users followed the answer than followed a pattern drawn from one user's visits |

All 72,000 checks pass on every arm: `2000 problems: checksum 132964605,
72000 checks over 4 arms: 0 failures`. A Python reading of the same
problems, by the same literal search, with the nine properties asserted
against the ★ arm's mirror, gives the same line.

## Mutation testing

Twenty-eight edits to the differential, seven to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. All twenty-eight are caught, and
eighteen are kept, no two failing the same checks; one of them stops the
run.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the third visit may repeat the second | P1 1332, P8 939, P9 1072 |
| M2 | ★: each user's visits in reverse time | P1 1071, P6 331, P8 867, P9 911 |
| M3 | ★: a pattern counted for each way a user follows it | P1 955, P9 53 |
| M4 | ★: ties keep the largest pattern | P1 1269 |
| M5 | ★: the second visit never right after the first | stops: `unwrap()` on `None` |
| M6 | ★: the third site read as the second | P1 1099, P8 770, P9 869 |
| M7 | sorted: visits grouped by user, left in input order | P1 1013, P2 1024, P8 730, P9 813 |
| M8 | sorted: a pattern needs two users | P1 1322, P7 1322, P8 1322, P9 1322 |
| M9 | sorted: all users' patterns left unsorted | P1 383, P4 309, P9 131 |
| M10 | sorted: the pattern's last two sites swapped | P1 932, P6 405, P8 780, P9 857 |
| M11 | ordered: visits grouped by site, not user | P1 1410, P7 558, P8 1020, P9 1127 |
| M12 | ordered: no pattern starts at the third visit from the end | P1 895, P8 541, P9 598 |
| M13 | ordered: times halved, visits at one time kept once | P1 812, P2 326, P3 808, P7 151, P8 272, P9 329 |
| M14 | ordered: each user's first visit dropped | P1 1157, P8 541, P9 634 |
| M15 | solution: the lowest score wins | P1 1591, P6 1529, P9 330 |
| M16 | solution: times cut to thousands | P1 707, P3 315, P6 161, P7 3, P8 581, P9 634 |
| M17 | solution: sites paired with the visits reversed | P1 1288, P2 1226, P6 1367, P8 934, P9 1038 |
| M18 | solution: every pattern scores one | P1 398, P9 237 |

P1 catches all twenty-six edits that let the run finish. P9 catches
twenty-two: every edit but the four that break ties toward the largest
pattern (M4 and its three copies), which P1 alone sees, on exactly the
1269 problems with a tie at the best score. P8 catches seventeen, the
edits that answer a pattern nobody followed, or nothing: visits out of
time order, a visit used twice, a site misread. P6 catches six, P7 five,
P2 four, P3 two (the edits that read times other than by their order,
M13 and M16) and P4 one: M9's patterns, never sorted together, come in
the order of the users' names, so renaming the users moves the answer.
P5 catches none. No edit reads a site's name except through its order,
which the renaming keeps.

The edit that stops the run, a second visit at least two after the
first, finds no pattern for a user of three visits, and the arm unwraps
the best of an empty map. Of the ten caught and not kept, each fails
exactly as a kept one: the sorted and solution arms letting the third
visit repeat the second, as M1; the ordered arm reversing time, as M2;
the sorted arm keeping a user's repeated patterns, as M3; the sorted,
ordered and solution arms breaking ties toward the largest pattern, as
M4; the solution arm leaving the visits in input order, as M7; the
ordered arm needing two users, as M8; and the ★ arm starting no pattern
at a user's first visit, which stops the run as M5 does.

## Verification

Every arm prints the same output as `most_visited_pattern.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The ★, sorted and ordered arms were written as Kāra. `karac fix` changed
the ★ arm's `Some((q, t))` to `Some((ref q, t))`, a match on the best so
far that would otherwise move it, and in the harness each
`"u0".to_string()` pushed onto a `Vec[String]` to the bare literal and a
`(byte - b'a') as i64` index to `(byte - b'a')`. `karac fix` carried the
solution arm in four rounds: `Vec<i32>` to `Vec[i32]`, `HashMap::new()`
to `HashMap.new()`, `&b.1` to `b.1`, `|&t|` to `|t|`, the adapter's
`&Vec<String>` to `ref Vec[String]` and `Solution::` to `Solution.`, and
the `use std::collections` line dropped; then `struct Solution {}`
declared and `HashMap` and `HashSet` renamed `Map` and `Set`; then a
`.clone()` before each `into_iter()` on a parameter, which borrows, `for
x in v` and `for p in set` written with `.into_iter()`, and `vec![...]`
written `[...]`; then the adapter's `ref` dropped. The adapter keeps the
`username.clone()` it was written with, which the arm, now borrowing,
clones again.

The kata found no gap.

## Benchmarks

`bench/` times the ★ arm against the same maps and sets in C, Rust, Go
and Python. 64 problems of 50 visits, LeetCode's most, by 5 users to 8
sites at the times 1 to 50 in a random order, are built once; then each
of 5000 rounds re-sites 4 visits of one problem, in turn, and answers it.
Every program prints `5000 rounds over 64 problems of 50 visits: 2913
patterns of three sites, checksum 249576583`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `43b61ed0fe`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.287 to 0.342 s | 0.299 s |
| C (`clang -O3`) | 0.289 to 0.357 s | 0.302 s |
| Go | 0.531 to 0.604 s | 0.568 s |
| Rust (`rustc -O`) | 0.593 to 0.667 s | 0.609 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.592 to 0.656 s | 0.614 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.600 to 0.687 s | 0.618 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.621 to 0.720 s | 0.653 s |
| Kāra (`karac build`) | 0.632 to 0.726 s | 0.657 s |
| Python | 0.620 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; a plain `karac build` gives the same binary, byte
for byte. Kāra takes about 1.06x overflow-checked Rust's median time,
and Rust without the checks is no faster: the work is hashing, copying
and comparing short strings, not arithmetic. Each user of about 10
visits holds up to 120 patterns, and Kāra and Rust build every one as
three new copies of its sites' strings before the set keeps or drops it,
and Kāra copies it once more as the key of its score. C, Go and Python
build the same sets and maps but share the strings: C stores pointers,
Go copies string headers, Python references the same objects and caches
each string's hash. That this sharing is what puts Python level with
Kāra and Rust, and C at about half their time, is inferred, not
measured; C's table also hashes with FNV-1a where Kāra and Rust use
SipHash-1-3.