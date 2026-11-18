# 2305. Fair Distribution of Cookies

You are given an integer array `cookies`, where `cookies[i]` denotes
the number of cookies in the `i`th bag. You are also given an integer
`k` that denotes the number of children to distribute **all** the bags
of cookies to. All the cookies in the same bag must go to the same
child and cannot be split up.

The **unfairness** of a distribution is defined as the **maximum**
**total** cookies obtained by a single child in the distribution.

Return *the **minimum** unfairness of all distributions*.

```
cookies = [8,15,10,20,8], k = 2         ->  31
cookies = [6,1,3,2,2,4,1,2], k = 3      ->  7
```

**Constraints:** `2 <= cookies.length <= 8`; `1 <= cookies[i] <= 10^5`;
`2 <= k <= cookies.length`.

With at most 8 bags and 8 children there are at most `8^8`, about
`1.7 * 10^7`, distributions. Backtracking over them, bag by bag, cuts
that down two ways: a child whose load would reach the best unfairness
found so far is not given the bag, and of the children with no bags
yet only the first is tried, since they are interchangeable. The
largest unfairness is `8 * 10^5`.

## Approaches

| file | mechanism |
|---|---|
| `cookies.kara` ★ | backtracking: `place` gives bag `i` to each child whose load stays under `*best`, through `mut ref` loads and best, and stops after the first child with nothing; a full distribution's largest load lowers the best |
| `cookies_naive.kara` | every distribution: the numbers 0 to `k^n - 1` written in base `k`, digit `i` the child of bag `i`, each one's largest load taken and the least kept. O(n k^n) |
| `cookies_subsets.kara` | over subsets: `sum[mask]` built from `mask` less its lowest bit, and for each child after the first `dp[mask]` the least over subsets `sub` of `mask`, walked by `sub = (sub - 1) & mask`, of `sum[sub]` against `dp[mask ^ sub]`. O(k 3^n) |
| `cookies_search.kara` | a binary search on the answer between the largest bag and all the cookies, each limit tried by backtracking the bags, largest first, with the same one-empty-child rule |
| `cookies_iter.kara` | iterators over subsets: each subset's `sum` from the bags it `filter`s in, then `(1..k).fold` of a `map` taking each subset to the `min` over every `sub` that `filter` finds inside it. O(k 4^n) |
| `cookies_solution.kara` | LeetCode's Rust template: a `dfs` helper nested in the method, taking `&Vec<i32>` and `&mut` loads and best, the same backtracking as the ★ arm; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; a child
for every bag; eight bags of `10^5` between two children; eight bags
of 9 to 1 among three children; then 500 random cases of 2 to 6 bags
of 1 to `10^5` among 2 to as many children as bags, with a checksum and
the answers in all. `cookies.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one call, reporting 24 edits.
`check` first reports ten errors and offers 14 edits for them:
`struct Solution;` to `struct Solution {}`; the six brackets of the
three `Vec<i32>`; `&Vec<i32>` to `ref Vec[i32]`, and the two `&mut` to
`mut ref`; `i32::MAX` to `i32.MAX`; and the three `&` at the call to
`dfs` dropped. The other ten follow from those: the nested `fn dfs`,
which Kāra has no place for and which captures nothing, moved above
`impl Solution` with the method's indentation taken off; `i: usize` to
`i: i64`, the type of an index; the `ref` on `cookies` dropped, since
a bare parameter already borrows; `vec![0; k as usize]` to
`Vec.filled(k, 0)`; `mut` written before `loads` and `best`,
which `dfs` writes, at both calls to it; and, in the harness's wrapper, the `as i64`
on the template's `i32` answer, which widens on its own.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every distribution, each bag given to each child in turn by
recursion on a copy of the loads, its unfairness the most any child
holds, and the least kept. No pruning and no symmetry rule. It checks
300 random cases of 2 to 6 bags of 1 to 20 cookies, where loads tie
often; then 30 whose bags are all equal; then 30 of bags of up to
`10^5`. Each case has 2 to as many children as bags. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer is at least the largest bag and all the cookies over `k`, rounded up, and at most all the cookies |
| P3 | the bags in reverse order: the same answer |
| P4 | one child more, where there are fewer children than bags: no larger an answer; as many children as bags: the largest bag |
| P5 | every bag doubled: the answer doubled |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 326417090, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
builds the same cases and takes the least over `itertools.product` of
the children. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: the best the smallest load, not the largest | P1 360, P2 360, P4 150, P6 360 |
| M5 | ★: the last bag never given | P1 164, P2 157, P3 195, P4 47, P6 164 |
| M6 | ★: one child fewer | P1 276, P4 99, P6 276 |
| M7 | naive: the digits divided by `k + 1` | P1 14, P3 14, P6 14 |
| M8 | naive: the digits read in base 2 | P1 14, P3 1, P6 14 |
| M10 | naive: the first bag never given | P1 167, P2 161, P3 195, P4 47, P6 167 |
| M13 | subsets: the two shares summed, not the larger taken | P1 360, P4 150, P6 360 |
| M15 | subsets: only the last share of each mask tried | P1 169, P3 184, P6 169 |
| M16 | subsets: the rest read at the share, not the bags left | P1 347, P2 347, P4 137, P6 347 |
| M18 | search: a fitting limit not kept | P1 58, P2 24, P5 86, P6 58 |
| M19 | search: a limit fitting with a child over it | P1 117, P2 112, P6 117 |
| M20 | search: a fit found with a bag left over | P1 71, P2 63, P6 71 |
| M22 | iter: a subset's bags counted twice | P1 360, P2 153, P4 150, P6 360 |
| M23 | iter: the rest given to one child | P1 178, P4 74, P6 178 |
| M25 | iter: one child more | P1 110, P2 104, P6 110 |
| M29 | solution: the bag taken back twice | P1 356, P2 356, P3 316, P4 207, P6 356 |
| M30 | solution: the best begun at 1000 | P1 30, P2 30, P4 11, P5 30, P6 30 |

P1 and P6 kill all seventeen, P2 eleven, P4 ten, P3 six and P5 two.
P2 fails for an answer below the largest bag or the fair share, or
above all the cookies, which most miscounts reach. P4, one child more,
fails where an edit's answer does not move with `k` as it should: a
child too few or too many, the shares summed, a bag never given. P3,
the bags reversed, fails only where the order of the bags matters: the
first or the last bag never given, the naive arm's digits read wrongly,
the subsets arm's last share alone, and the template's bag taken back
twice. P5, every bag doubled, fails only where a constant stands apart
from the cookies: the search's fitting limit not kept, which can stop
below the least by a step that does not double with the bags, and the
template's best begun at 1000.

Of the thirty-one, fourteen were not kept. Five are equivalent and
killed by nothing: the naive arm's `k^(n - 1)` ways (M11), which only
keeps the last bag with the first child, as the children are
interchangeable; the subsets arm's first bag never a share alone
(M12), since the first child, whose share is any subset, can hold it;
the search from 0 (M17), which finds the same least limit from further
down; and the template's load equal to the best kept (M27) and its
empty children all tried (M28), which only prune less. The ★ arm's
unfairness taken as all the cookies (M1), bag never taken back (M2)
and search stopped at the first child (M3), the naive arm's loads kept
from the way before (M9), the iter arm's most over the subsets (M24)
and the template's bag given to the child after (M31) all fail as the
subsets arm's shares summed (M13), every one of them on every case; the
subsets arm's one child fewer (M14) fails as the ★ arm's (M6), the
iter arm's answer for all but the last bag (M26) as the ★ arm's last
bag never given (M5). The search arm's search capped at twice the largest bag (M21)
fails apart from every kept one, and was left out to keep three to an
arm.

M1, M7, M12, M15, M16 and M23 replace edits that were equivalent or
failed as others did: a load equal to the best kept in the ★ arm, one
way fewer and then the first child's load as the unfairness in the
naive arm, the empty share never left out and then the first child
given nothing in the subsets arm, its subsets summed without their
lowest bag and walked from one below the mask, and the iter arm's
subsets of every number up to the mask.

## Verification

Every arm prints the same output as `cookies.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, subsets, search and template arms take
0.3 to 0.4 s, the iter arm, which tries every number below each mask
as a share, 1.6 s, and the naive arm, which walks all `k^n` ways for
every case, 10.4 s. The differential takes 40 s there, most of it the
literal reading's every distribution and the naive arm's, and 0.8 s
under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 2000 lists of 8 bags of 1 to `10^5` cookies once, then
makes 50 passes, list `a` in pass `p` shared among `2 + (a + p) % 7`
children, with the ★ arm in all five languages. Every implementation
prints `50 passes over 2000 lists of 8 bags: checksum 57443587`. Each
keeps the bags and the loads as 64-bit integers, the loads in one array
for each call passed down the recursion, and the best through a
pointer, a `&mut`, a `mut ref` and, in Python, a one-element list.

BENCHTAB
