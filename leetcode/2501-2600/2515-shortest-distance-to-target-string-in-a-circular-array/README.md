# 2515. Shortest Distance to Target String in a Circular Array

You are given a **0-indexed** **circular** string array `words` and a
string `target`. A **circular array** means that the array's end
connects to the array's beginning.

- Formally, the next element of `words[i]` is `words[(i + 1) % n]` and
  the previous element of `words[i]` is `words[(i - 1 + n) % n]`, where
  `n` is the length of `words`.

Starting from `startIndex`, you can move to either the next word or the
previous word with `1` step at a time.

Return *the **shortest** distance needed to reach the string* `target`.
If the string `target` does not exist in `words`, return `-1`.

```
words = ["hello","i","am","leetcode","hello"], target = "hello", startIndex = 1  ->  1
words = ["a","b","leetcode"], target = "leetcode", startIndex = 0                ->  1
words = ["i","eat","leetcode"], target = "ate", startIndex = 0                   ->  -1
```

**Constraints:** `1 <= words.length <= 100`; `1 <= words[i].length <=
100` and `1 <= target.length <= 100`; `words[i]` and `target` consist
of only lowercase English letters; `0 <= startIndex < words.length`.

A place `i` that holds the target is `d = |i - start|` steps away one
way round and `n - d` the other, so the answer is the least `min(d, n -
d)` over those places, or `-1` when there is none. The approaches
differ in whether they look at every place or walk out from the start
and stop at the first hit.

## Approaches

| file | mechanism |
|---|---|
| `closest.kara` ★ | every place compared with the target, and each hit's shorter way round kept when it beats the best so far. O(n L) |
| `closest_outward.kara` | the places `k` steps to the right and to the left looked at for `k` from 0 to `n / 2`, and the first `k` with a hit returned |
| `closest_walks.kara` | one walk to the right and one to the left, each counting steps until it stands on the target or has gone all the way round; the shorter walk |
| `closest_rec.kara` | recursion: the answer from `k` steps out is `k` on a hit at either side, `-1` past `n / 2`, and otherwise the answer from `k + 1`. At most 51 deep |
| `closest_iter.kara` | iterators: the places `enumerate`d, the hits kept by `filter`, each `map`ped to its shorter way round, and their `min`, `-1` when there is none |
| `closest_solution.kara` | LeetCode's Rust template: `Vec<String>`, `String` and `i32` in, `i32` out; the places `enumerate`d, `i32::MAX` for no hit yet, and `abs` and `min` for the shorter way round; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's three examples and five
more; then 2000 random lists of 1 to 10 one-letter words from 3, the
target one letter from 4, and 2000 of 1 to 100 words of 1 to 3 letters
from 2, the target a word of the same kind, each as the misses, the sum
of the other answers and a checksum; then the constraints' largest, 100
words of 100 letters: the target only opposite the start, only beside
it on the left, nowhere, and everywhere. `closest.py` mirrors the ★ arm
and its output is byte-identical, and the mirror was checked on 5000
random lists of 1 to 12 one-letter words from 3, the target from 4,
against a walk that looks at the places `k` steps either way for `k`
from 0 up, and the two agreed on every list.

The harness first named its cases' words `Vec[Str]`, the views the
literals are, and `check` refused the list: in a tuple slot of that
type, `["a", "b"].to_vec()` took `Vec[String]` (expected `(Vec[Str],
i64)`, found `(Vec[String], i64)`), where a `let` of the `Vec` alone
takes the slot's `Str` (B-2026-11-23-66). The tuple's slot now names the
element type as the `let` does. The harness names `Vec[String]`, since
every arm takes LeetCode's `Vec<String>`.

`check` first reports 4 errors on the template: `struct Solution;`,
`Vec<String>` in angle brackets, and the two `i32::MAX`. `karac fix`
carries it in one call, reporting 8 edits: `struct Solution {}`; the
brackets; `i32.MAX` twice; and the wrapper's `words.clone()`,
`target.clone()` and lossless `as i64` dropped. The `*w == target`
comparison through the iterator's reference and the `i as i32` stand as
written.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a breadth-first search from the start over the circle, each
place's distance one more than the place it was reached from, its two
neighbours the next and the previous word; the answer is the distance of
the first place taken off the queue that holds the target. No distance
is worked out by a formula. It checks 300 random lists of 1 to 10
one-letter words from 3, the target one letter from 4; then 20 lists of
one word; and 40 of 20 words of 1 to 2 letters from 2. All 360 are
drawn before any arm answers, and 140 of them have no target.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | `-1` exactly when no word is the target, and otherwise from 0 to `n / 2` |
| P3 | the list reversed, the start at `n - 1 - start`: the same answer |
| P4 | the first word moved to the end, the start one place back: the same answer |
| P5 | the list followed by a copy of itself: the same answer |
| P6 | each arm agrees with at least three of the other five |

P5 holds because a walk of `k` steps from the start on the doubled list
reads the same words as on the list, `doubled[(s + k) % 2n]` being
`words[(s + k) % n]`.

The differential prints `360 cases, 140 with no target: checksum
262739632, 12960 checks over 6 arms: 0 failures` under every lane in
Verification; the checksum of the literal answers was checked against a
Python reading that builds the same cases and takes the least of the
two ways round to every place holding the target. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: the last match kept | P1 91, P3 127, P4 44, P5 148, P6 91 |
| M4 | ★: the first word never looked at | P1 43, P2 30, P3 55, P4 62, P5 32, P6 43 |
| M6 | ★: no match read as 0 | P1 266, P2 140, P6 266 |
| M7 | outward: only rightward | P1 39, P2 16, P3 91, P5 16, P6 39 |
| M10 | outward: the steps counted from 1 | P1 220, P2 39, P6 220 |
| M11 | outward: no match read as n | P1 140, P2 140, P5 140, P6 140 |
| M12 | walks: only the right walk | P1 39, P2 16, P3 91, P6 39 |
| M13 | walks: the longer walk | P1 91, P2 38, P6 91 |
| M14 | walks: the left walk two places a step | P1 64, P2 28, P3 59, P6 64 |
| M19 | rec: the search started at 1 | P1 94, P2 36, P5 36, P6 94 |
| M20 | rec: no match read as 0 | P1 140, P2 140, P6 140 |
| M21 | rec: the search stepping two | P1 93, P2 38, P5 13, P6 93 |
| M22 | iter: the way round never taken | P1 12, P2 7, P4 28, P5 7, P6 12 |
| M23 | iter: the largest distance | P1 141, P5 212, P6 141 |
| M24 | iter: the words that miss | P1 360, P2 163, P6 360 |
| M29 | solution: the start one place on | P1 156, P3 120, P6 156 |
| M31 | solution: the length one short | P1 32, P4 36, P5 14, P6 32 |

P1 and P6 kill all seventeen, P2 thirteen, P5 nine, P3 six and P4
four.

Fourteen are not kept. Ten fail exactly as a kept one does: the ★ and
template arms' way round never taken (M1, M27) as the iter arm's (M22);
the ★ arm's way round one short (M2) as the template's length one short
(M31); the ★ arm's distance from the start plus one and the walks arm's
walks started a place on (M5, M16) as the template's start one place on
(M29); the rec arm's only rightward (M18) as the outward arm's (M7); the
iter arm's first word left out (M25) as the ★ arm's first word never
looked at (M4); the iter and template arms' no match read as 0 or as the
bound (M26, M30) as the rec arm's (M20); and the template's last match
kept (M28) as the ★ arm's (M3). Three are killed but give a fourth to an
arm that has its three: the outward arm's one step too few and left side
two steps a time (M8, M9), and the rec arm's search one step short
(M17). One survives and is equivalent: the walks arm's walk given up a
step early (M15). A walk that has taken `n - 1` steps has already
compared the `n`-th place, the last one it has not seen, in the loop's
condition, so stopping there answers as stopping at `n` does.

## Verification

Every arm prints the same output as `closest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.6 to 0.7 s and the differential 0.3 s; under `karac __mir-llvm-asan` the arms take 0.4 to 0.5 s and the differential 0.5 s; and under `karac run` the differential takes 0.4 s.

## Benchmarks

The bench builds 2000 lists of 100 words of 1 to 3 letters from 3 once
from its own generator, then makes 900 passes. Each pass asks every
list for the word at place `check / 100 % 100`, so the target is always
there, from the start `check % 100`, folding each answer plus the pass
into the checksum. The bench uses the ★ arm in all five languages.
Every implementation prints `900 passes over 2000 lists of 100 words:
checksum 384660185`.

BENCHTAB
