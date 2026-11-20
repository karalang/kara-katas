# 2370. Longest Ideal Subsequence

You are given a string `s` consisting of lowercase letters and an
integer `k`. We call a string `t` **ideal** if the following conditions
are satisfied:

- `t` is a **subsequence** of the string `s`.
- The absolute difference in the alphabet order of every two
  **adjacent** letters in `t` is less than or equal to `k`.

Return *the length of the **longest** ideal string*.

A **subsequence** is a string that can be derived from another string
by deleting some or no characters without changing the order of the
remaining characters.

**Note** that the alphabet order is not cyclic. For example, the
absolute difference in the alphabet order of `'a'` and `'z'` is `25`,
not `1`.

```
s = "acfgbd", k = 2  ->  4
s = "abcd", k = 3    ->  4
```

**Constraints:** `1 <= s.length <= 10^5`; `0 <= k <= 25`; `s` consists
of lowercase English letters.

An ideal subsequence that ends in letter `c` extends one that ends in a
letter within `k` of `c`, and only the longest of those matters, so 26
running bests, one per letter, carry the whole answer.

## Approaches

| file | mechanism |
|---|---|
| `ideal.kara` ★ | `best[c]`, the longest ideal subsequence so far ending in `c`; a new letter `c` becomes one more than the largest best within `k` of it. O(26 n) |
| `ideal_tree.kara` | the 26 bests in the leaves of a segment tree of 32, so the largest best within `k` of `c` is one range query. O(n log 26) |
| `ideal_last.kara` | by place: `dp[i]` is one more than the largest `dp` at the last place of any letter within `k` of `s[i]`, since a letter's last place has the largest `dp` of its places. O(26 n) |
| `ideal_suffix.kara` | from the right: `from[p]`, the longest ideal subsequence of the letters read so far whose first letter is within `k` of `p`, with `p = 26` for any first letter. O(26 n) |
| `ideal_iter.kara` | iterators: the bytes folded into the 26 bests, the largest best within `k` found by `map` and `max` over the range of letters |
| `ideal_solution.kara` | LeetCode's Rust template: an array `[0i32; 26]`, the letters within `k` from `saturating_sub` and `min`, and the largest best over the slice `dp[lo..=hi]`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; one letter;
`10^5` letters running through the alphabet again and again, with `k`
of 0, 1 and 25; `10^5` letters `a` and `z` in turn, with `k` of 24 and
25; then 2000 random strings of 1 to 40 letters from the first 1 to 26
of the alphabet, with `k` of 0 to 25, with a checksum and how many are
ideal whole. `ideal.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 3000 random strings of up
to 12 letters against trying every subsequence.

`check` first reports 2 errors on the template, and `karac fix` carries
it in one call, reporting 3 edits: `struct Solution;` given its braces,
and `Solution::` written with a dot and the glue's `as i64` on the
template's `i32` answer dropped. The `[0i32; 26]` array, the `usize`
casts, `saturating_sub`, `for b in s.bytes()`, `b'a'`, the inclusive
slice `dp[lo..=hi]` and `*dp.iter().max().unwrap()` all stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every subsequence, one mask of the places at a time, kept
when each two letters next to each other in it are at most `k` apart,
and the longest kept. No table of letters. It checks 300 random strings
of 1 to 14 letters from the first 1 to 26 of the alphabet with `k` of 0
to 25; then 30 of up to 2000 letters; then 30 of up to 300 letters,
half of them `a` or `z`, with `k` of 20 to 25. All 360 are drawn before
any arm answers, and the literal reading answers the 301 of them with
at most 14 letters. `karac fix` added the `.into_iter()` the
differential's own `flat_map` closure needs on the vector it returns,
in 1 edit.

| | property |
|---|---|
| P1 | up to 14 letters, the answer is the literal reading's |
| P2 | from 1 to `n`, and `n` when `k` is 25 |
| P3 | every letter written as its mirror, `a` as `z` and `z` as `a`: the same answer |
| P4 | the string reversed: the same answer |
| P5 | every letter written twice in its place: twice the answer |
| P6 | each arm agrees with at least three of the other five |

P3 and P4 hold because neither the distance between two letters nor
which letters stand next to each other in a subsequence changes. P5
holds because an ideal subsequence written with each letter twice is
ideal, and an ideal subsequence of the doubled string, with each
place's pair taken back to its one letter, leaves at least half its
length.

The differential prints `360 cases: checksum 709794992, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tries every subsequence. On a failure it prints the
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
| M1 | ★: the lowest letter one too high | P1 29, P2 2, P3 68, P4 68, P5 8, P6 65 |
| M2 | ★: z never read as an earlier letter | P1 2, P2 2, P3 171, P4 10, P5 6, P6 33 |
| M6 | ★: the last best taken, not the largest | P1 264, P2 16, P3 196, P4 59, P5 342, P6 323 |
| M7 | tree: the left end read at even nodes | P1 47, P3 95, P4 94, P6 86 |
| M9 | tree: a node taking its left child only | P1 281, P2 168, P3 203, P4 41, P5 29, P6 339 |
| M11 | tree: each leaf written one letter low | P1 141, P2 12, P3 217, P4 126, P5 60, P6 200 |
| M12 | last: the first place of each letter kept | P1 184, P2 11, P4 100, P5 337, P6 243 |
| M13 | last: a letter at place 0 never extended | P1 237, P2 16, P4 41, P5 312, P6 293 |
| M14 | last: the answer the last place's | P1 17, P4 27, P6 19 |
| M17 | suffix: a letter starting one more than the best of any | P1 95, P6 135 |
| M19 | suffix: the last letter never read | P1 268, P2 35, P4 41, P5 323, P6 323 |
| M21 | suffix: each from set, not raised | P1 5, P4 47, P6 41 |
| M23 | iter: each letter counted twice | P1 301, P2 330, P6 360 |
| M24 | iter: the smallest best within k | P1 272, P2 16, P4 2, P5 349, P6 331 |
| M25 | iter: only a and z read at the end | P1 250, P2 164, P4 154, P6 292 |
| M29 | solution: a letter never extending what it follows | P1 278, P2 16, P5 360, P6 337 |
| M31 | solution: k halved | P1 130, P2 4, P6 180 |

P1 and P6 kill all seventeen, P2 and P4 thirteen, P5 ten and P3 six.
P3, every letter mirrored, fails the edits that treat the low end of
the alphabet unlike the high end: the lowest letter one too high, `z`
never read, the last best taken, and the tree's left end at even nodes,
left child only and leaves one letter low. P2 fails, beyond the edits
that count too much, those that miss the whole string when `k` is 25.

Of the thirty-one, fourteen were not kept. The highest letter within
`k` left out in the ★ arm (M3), the tree's high end left out (M8) and
the suffix arm's highest letter never raised (M20) fail alike; so do
each place started at one in the last arm (M16) and every best started
at one in the iter arm (M26), which add one to every answer, and only
letters at or below `c` in the last arm and the template (M15, M28).
The iter arm's `a` never read as an earlier letter (M22) leaves the
range of letters empty for an `a` when `k` is 0, and stops on an
`unwrap` of `None`. Each letter extending only its own and the bests
summed in the ★ arm (M4, M5), the tree's answer read at the leaf of `a`
(M10), the suffix arm's answer never raised (M18), and the template's
only letters at or above `c` and smallest best returned (M27, M30) fail
apart from every kept one, and were left out to keep three to an arm
and two to the template.

## Verification

Every arm prints the same output as `ideal.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 4.9 to 11 s, the long lines
walking up to 26 letters for each of their `10^5` places, and the
differential 20 s there and 0.75 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 strings of `10^5` random letters once from the
harness's generator, then makes 10 passes, pass `p` answering string `a`
with `k` of `a` and of `2a + 5` and folding each answer plus `p` into
the checksum, with the ★ arm in all five languages. Every
implementation prints `10 passes over 10 strings of 10^5 letters:
checksum 603019954`. Every implementation builds its 26 bests afresh
in each call, C on the stack and the others on the heap.

BENCHTAB
