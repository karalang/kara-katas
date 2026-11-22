# 2830. Maximize the Profit as the Salesman

You are given an integer `n` representing the number of houses on a
number line, numbered from `0` to `n - 1`.

Additionally, you are given a 2D integer array `offers` where
`offers[i] = [starti, endi, goldi]`, indicating that `ith` buyer
wants to buy all the houses from `starti` to `endi` for `goldi`
amount of gold.

As a salesman, your goal is to **maximize** your earnings by
strategically selecting and selling houses to buyers.

Return *the maximum amount of gold you can earn*.

**Note** that different buyers can't buy the same house, and some
houses may remain unsold.

```
n = 5, offers = [[0,0,1],[0,2,2],[1,3,2]]   ->  3
n = 5, offers = [[0,0,1],[0,2,10],[1,3,2]]  ->  10
```

**Constraints:** `1 <= n <= 10^5`; `1 <= offers.length <= 10^5`;
`offers[i].length == 3`; `0 <= starti <= endi <= n - 1`; `1 <= goldi
<= 10^3`.

## Approaches

| file | mechanism |
|---|---|
| `profit.kara` ★ | the offers filed by their last house in a `Vec` of lists, and best[i] the most gold from the first i houses: house i unsold, or the end of an offer from s, best[s] plus its gold |
| `profit_sorted.kara` | the offers sorted by end, best[j] the most from the first j of them: offer j skipped, or taken after the last offer ending before its start, found by `partition_point` on the ends |
| `profit_back.kara` | from the back: the offers filed by their first house in a `Map` of lists through `entry().or_insert()`, and after[i] the most gold from house i on |
| `profit_memo.kara` | recursion over the offers sorted by start, each skipped or sold and followed by the first offer starting past its end, found by a hand-written binary search, the answers memoized in a `Vec[Option[i64]]` held by a struct with a `mut ref self` method |
| `profit_solution.kara` | a Rust solution as LeetCode's Rust users write it: the offers grouped by end in a `vec![vec![]; n]` of `(usize, i32)`, and `f[i + 1] = f[i + 1].max(f[s] + g)`, `as usize` on every index, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; one house;
1000 houses each offered alone for its number against one offer of
1000 for them all; the same with an offer of 600000 for all; then 3000
random cases of 1 to 10 houses with 1 to 8 offers, and 50 of up to
2000 houses with up to 2000 offers of up to 50 houses, as checksums.
`profit.py` mirrors the ★ arm and its output is byte-identical.

```
3
10
7
500500
600000
3000 small streets: checksum 378770188
50 long streets: checksum 247162030
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every set of offers, by a bit mask, each house marked
as its offers are laid down, kept when no house is marked twice, and
the most gold. It draws 2000 random cases of 1 to 10 houses with 1 to 8
offers, then 50 of up to 1500 houses with up to 1500 offers of up to 50
houses, all before any arm answers; the literal reading is asked only
of the first 2000.

| | property |
|---|---|
| P1 | up to 8 offers, the answer is the literal reading's |
| P2 | the offers in reverse order: the same answer |
| P3 | an offer of no gold for the whole street added: the same answer |
| P4 | every offer's gold doubled: the answer doubled |
| P5 | the street mirrored, house i as n - 1 - i: the same answer |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 459128781, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an unsold house losing what came before | P1 778, P5 1273, P6 827 |
| M2 | ★: an offer added to the gold up to its own end | P1 872, P5 1258, P6 922 |
| M3 | sorted: an offer ending on the start counted as before it | P1 964, P5 1110, P6 1014 |
| M4 | sorted: a skipped offer losing the best so far | P1 1177, P2 1524, P3 2050, P5 906, P6 1227 |
| M5 | back: an unsold house losing what follows | P1 1309, P5 1273, P6 1358 |
| M6 | back: the next sale allowed on the offer's last house | P1 1280, P2 426, P5 583, P6 1330 |
| M7 | memo: an offer starting on the last house counted free | killed under both: fatal runtime error: stack overflow |
| M8 | memo: skipping never tried | P1 1303, P3 1159, P5 1041, P6 1353 |
| M9 | solution: the best so far not carried to the next house | P1 778, P5 1273, P6 827 |
| M10 | solution: an offer's gold counted from house 0 | P1 1088, P6 1138 |

## Benchmarks

The bench draws 20 streets of 10^5 houses with 10^5 offers of up to
100 houses each, LeetCode's most, all of them first, then answers each
10 times by the ★ arm in all five languages. C files the offers by a
count of each end and a prefix sum into one array, where the others
push onto a list per house; the walk is the same. Every implementation
prints `20 streets of 100000, 10 rounds: gold totals 986380610,
checksum 25908693`.

BENCHTAB

## Verification

All five arms print the same output as `profit.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

Three of the four own arms checked clean as first written. The memo
arm's binary search opened with `let (mut lo, mut hi) = ..`, Rust's
pattern, and `karac check` reported E0001 twice, `mut` going before
the whole pattern in Kāra; `karac fix` made it `let mut (lo, hi)`.

LeetCode's Rust template took 25 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; `Vec<..>`
became `Vec[..]` and `usize` `i64`; `vec![vec![]; n]` became
`Vec.filled(n, Vec.new())`; `groups[o[1] as usize]` lost its cast,
an `i32` index widening, and the pushed pair's `o[0] as usize` became
`as i64`, as `n as usize` did; `for &(s, g)` and `|&v|` lost their `&`;
`vec![0; n + 1]` became `Vec.filled(n + 1, 0i32)`, its literal settled
to `i64` by the `.max(..)` method (design.md §8) where `f[n]` returns
an `i32`; `Solution::` took `.`, and the wrapper's `as i64` went.
