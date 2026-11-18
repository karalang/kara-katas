# 2226. Maximum Candies Allocated to K Children

You are given a **0-indexed** integer array `candies`. Each element in
the array denotes a pile of candies of size `candies[i]`. You can divide
each pile into any number of **sub piles**, but you **cannot** merge two
piles together.

You are also given an integer `k`. You should allocate piles of candies
to `k` children such that each child gets the **same** number of
candies. Each child can be allocated candies from **only one** pile of
candies and some piles of candies may go unused.

Return *the **maximum number of candies** each child can get.*

```
candies = [5,8,6], k = 3   ->  5
candies = [2,5],   k = 11  ->  0
```

**Constraints:** `1 <= candies.length <= 10^5`; `1 <= candies[i] <=
10^7`; `1 <= k <= 10^12`.

A binary search on the answer: x candies each can be handed out when the
piles cut into x-sized shares give at least k of them, and fewer candies
each only gives more shares, so the largest such x lies between 0 and
the largest pile. O(n log max). The shares at x = 1 are the candies in
all, up to 10^12, past `i32`.

## Approaches

| file | mechanism |
|---|---|
| `candies.kara` ★ | a binary search on the answer between 0 and the largest pile, the middle rounded up, the shares counted by a `for` loop of divisions |
| `candies_bits.kara` | the answer built a bit at a time from 2^23 (the first power of two past 10^7) down, a bit kept when the answer with it still feeds k; a helper `feeds` |
| `candies_bound.kara` | a half-open search for the first share size that cannot feed k, below one past the tighter of the largest pile and the candies in all over k; the count of shares stops once it reaches k |
| `candies_struct.kara` | a `struct Piles` holding the candies and the largest pile, with `shares` and `best` (`ref self`) |
| `candies_iter.kara` | the shares a `map` and `sum` over the piles inside a closure `feeds`, which the binary search calls |
| `candies_solution.kara` | LeetCode's Rust template: `Vec<i32>` and `i64` in, `i32` out, the bounds a tuple `(mut lo, mut hi) = (0, *candies.iter().max().unwrap())`, the middle as `lo + (hi - lo + 1) / 2`, the shares `map(\|&c\| (c / mid) as i64).sum()` typed `i64`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples and four
more (one pile for one child, the largest pile, a pile split three ways,
and an answer the smallest pile cannot give), each with its answer; then
a checksum of 3000 random cases of 1 to 20 piles of up to 10, 1000 and
10^7 candies in turn, k from 1 to a little past the candies in all; then
the constraints' largest, 10^5 piles of up to 10^7 with k of 1, 10^5,
10^9 and 10^12. The piles are drawn from two draws each, since one stops
at 32767. `candies.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in three rounds of 9 edits: `Vec<i32>`
to `Vec[i32]`, `let (mut lo, mut hi)` to `let mut (lo, hi)`, `|&c|` to
`|c|` and `struct Solution;` to `struct Solution {}`; then the `0` that
seeds `lo` to `0i32`, since an unsuffixed literal beside an `i32` keeps
`i64`; then the adapter's `as i64` on the answer, which widens anyway.
At first the second round also deleted the `as i64` in `(c / mid) as
i64` as redundant, judged while `mid` was still `i64`: after the retype
`mid` is `i32`, the shares were summed in `i32`, and 10^5 piles of 10^7
overflowed at run time. karac now holds a cast lint's fix back while any
error stands, as it already did `redundant_clone` (kara B-2026-11-17-140).

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every share size from the largest pile down tried, each pile
cut by taking that many candies off it again and again, and the first
size that hands k children a share is the answer, else 0; no division,
no search. It checks 300 random cases of 1 to 8 piles of up to 10, 50
and 200 candies in turn, k from 1 to a little past the candies in all;
then 30 with k the candies in all; then 30 with k one. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | it is at least 0 and at most both the largest pile and the candies in all over k |
| P3 | the piles reversed: the same answer |
| P4 | one more child: no more candies each |
| P5 | every pile doubled: twice the answer, or one more than that |
| P6 | each arm agrees with at least three of the other five |

P5 holds because a share of y from the doubled piles gives a share of
y / 2, rounded down, from the piles themselves: halving both sides of
`2p / y` loses nothing.

The differential prints `360 cases: checksum 456484111, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that scans
every share size with `//`. On a failure it prints the first ten and
then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to each
of the others, each run under `karac __mir-llvm-run`, and the kept ones
under `karac __mir-run` too. Seventeen are kept, three to each Kāra arm
and two to the Rust-template arm. Each kept one is killed, fails the
same way under both backends and not by a crash, and no two kept ones
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: a pile's remainder counted as a share | P1 71, P2 61, P6 71 |
| M4 | ★: the high end moved two below a failed middle | P1 129, P5 171, P6 129 |
| M5 | ★: the remainders counted, not the shares | P1 293, P2 73, P5 69, P6 293 |
| M7 | bits: the answer built from 2^7 down | P5 8 |
| M8 | bits: each kept bit replacing the ones before it | P1 84, P4 12, P5 137, P6 84 |
| M10 | bits: every other bit tried | P1 257, P5 320, P6 257 |
| M12 | bound: the bound itself never tried | P1 278, P5 75, P6 278 |
| M14 | bound: the count stopping at k - 1 | P1 80, P3 61, P4 61, P5 12, P6 80 |
| M15 | bound: the first failing size returned | P1 360, P2 318, P5 247, P6 360 |
| M19 | struct: k - 1 shares enough | P1 48, P2 23, P6 48 |
| M20 | struct: the search capped at half the largest pile | P1 51, P6 51 |
| M21 | struct: the high end halved after a failure | P1 53, P5 118, P6 53 |
| M22 | iter: one share too many from every pile | P1 107, P2 97, P6 107 |
| M24 | iter: the search capped at the smallest pile | P1 57, P6 57 |
| M26 | iter: the first pile skipped | P1 206, P3 102, P6 206 |
| M28 | solution: more than k shares needed | P1 105, P6 105 |
| M29 | solution: the low end starting at 1 | P1 40, P2 40, P5 40, P6 40 |

P1 and P6 kill all but one, P5 ten, P2 six, and P3 and P4 two each. The
one P1 misses is M7: an answer built from 2^7 down reaches at most 255,
and the differential's piles stop at 200, so only P5's doubled piles, up
to 400, ask for more; the arm's own harness, with piles up to 10^7,
fails it too. P3 kills only the edits that treat
one pile unlike the others (M14, whose stopped count depends on which
piles come first, and M26), and P4 only those that can give more with
one more child (M8, M14).

Of the thirty-one, fourteen were not kept. Three survive and are
equivalent: the ★ arm's count stopping once it reaches k (M6), since
more shares cannot turn a yes into a no; the bits arm's bit added rather
than or'ed in (M11), since the bits below the one tried are still 0;
and the template's middle rounded down plus one (M27), which is another
middle strictly above `lo`, so the search still narrows to the same
answer. None crashes, and none differs between the backends. Five fail
as a kept one does: the ★, bits and iter arms' more than k needed (M1,
M9, M23) as the template's (M28); the struct arm's search capped at the
smallest pile (M17) as the iter arm's (M24); and the template's first
pile skipped (M31) as the iter arm's (M26). Six fail their own way and
are left out for the count of three (two for the template): the ★ arm's
largest pile left out (M2), the bound arm's bound one short and last
pile skipped (M13, M16), and the struct, iter and template arms' shares
of x + 1 (M18, M25, M30), which fail alike.

## Verification

Every arm prints the same output as `candies.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.3 s to 1.9 s, and the iter and
template arms, whose shares go through `map` and `sum`, 7.1 s to 7.2 s.
The differential takes 0.4 s.

## Benchmarks

The bench draws 4 lists of 10^5 piles of up to 10^7 once, then answers
each 25 times, for 10^3, 10^6, 10^9 and 10^11 children by list, one pile
drawn again before each answer, with the ★ arm in all five languages.
Every implementation prints `100 answers over 10^5 piles: checksum
786234540`.

BENCHTAB
