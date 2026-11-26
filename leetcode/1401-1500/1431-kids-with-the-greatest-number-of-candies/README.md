# 1431. Kids With the Greatest Number of Candies

There are `n` kids with candies. You are given an integer array
`candies`, where each `candies[i]` represents the number of candies the
`i`th kid has, and an integer `extraCandies`, denoting the number of
extra candies that you have. Return a boolean array `result` of length
`n`, where `result[i]` is `true` if, after giving the `i`th kid all the
`extraCandies`, they will have the greatest number of candies among all
the kids, or `false` otherwise. Note that multiple kids can have the
greatest number of candies.

```
candies = [2,3,5,1,3], extraCandies = 3    ->  [true,true,true,false,true]
candies = [4,2,1,1,2], extraCandies = 1    ->  [true,false,false,false,false]
candies = [12,1,12], extraCandies = 10     ->  [true,false,true]
```

**Constraints:** `n == candies.length`, `2 <= n <= 100`, `1 <=
candies[i] <= 100`, `1 <= extraCandies <= 50`.

Each arm is `fn kids_with_candies(candies: Vec[i32], extra_candies: i32)
-> Vec[bool]`.

## Approaches

| file | mechanism |
|---|---|
| `kids_with_candies.kara` ★ | the most any kid has, by `iter().max()`, and each kid against it with the extra, by `map` and `collect`. O(n) |
| `kids_with_candies_sort.kara` | the candies sorted, the most the last of them, and the answers pushed one kid at a time. O(n log n) |
| `kids_with_candies_fold.kara` | the most found by `fold` from nothing, each kid then checked against it. O(n) |
| `kids_with_candies_pairs.kara` | each kid against every kid by `all`: with the extra, at least as many as all of them, so none has more. O(n²) |
| `kids_with_candies_solution.kara` | a Rust solution as LeetCode's Rust users write it (the most read through `*candies.iter().max().unwrap()`, each kid by `map(\|&c\| ..)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and three
more, each answer as a `T` or an `F` for each kid (`TTTFT TFFFF TFT TT
TT TF`); the constraints' most, 100 drawn kids with 1, 25 and 50 extra,
as the kids that can have the most (`100 kids: 3 28 52 can have the
most`); and 2000 random cases of 2 to 100 kids, of up to 1 to 100
candies, with 1 to 50 extra (`2000 random cases: 57903 can have the
most, checksum 486502646`). `kids_with_candies.py` mirrors the ★ arm,
and its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★, sort, fold and pairs arms check clean as first
written. The Rust solution takes one round of 14 fixes by `karac fix`'s
count: `struct Solution;` to `struct Solution {}`, `Vec<..>` to
`Vec[..]`, the closure's `|&c|` to `|c|`, and `Solution::` to
`Solution.`; its `*candies.iter().max().unwrap()` is taken as written.
Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each kid given the extra candies in turn, on a copy of the
kids, and asked whether any other kid then has more. LeetCode's
examples, four edge cases (two kids alike, the extra just reaching the
most, one short of it, and two kids tied for the most), the constraints'
most four ways (100 kids of 100 candies, and 100 drawn kids with 1, 25
and 50 extra), and 1992 random cases of 2 to 100 kids, of up to 1 to 100
candies, with 1 to 50 extra.

The three drawn cases were first pushed from `for extra in [1, 25, 50]`,
whose `extra` keeps the default `i64` of the list's literals, which
`karac check` says, naming the list, and `karac fix` writes `[1i32, 25,
50]`, 1 fix.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | an answer for every kid, and the kid with the most among those that can have it |
| P3 | one extra candy more takes no kid's answer away |
| P4 | the kids turned round give the answers turned round |
| P5 | a candy more for every kid changes no answer |
| P6 | the ★ arm's answer |

All 60,090 checks pass on every arm: `2003 cases: checksum 693382934,
60090 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by `max`, gives
the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a kid who only ties the most not counted | P1 792, P6 3168 |
| M2 | ★: the fewest any kid has taken for the most | P1 1409, P6 5636 |
| M3 | sort: the second most taken for the most | P1 575, P6 575 |
| M4 | sort: one extra candy fewer given | P1 792, P6 792 |
| M5 | fold: the fewest found, not the most | P1 1409, P6 1409 |
| M6 | fold: the most found from 100, not from nothing | P1 1950, P2 1483, P5 259, P6 1950 |
| M7 | pairs: a kid against any kid, not every kid | P1 1409, P6 1409 |
| M8 | pairs: the extra candies not given | P1 1918, P6 1918 |
| M9 | solution: the last kid's candies taken for the most | P1 1312, P4 1051, P6 1312 |
| M10 | solution: each kid's candies doubled in place of the extra | P1 1819, P5 592, P6 1819 |

## Benchmarks

The bench draws a pool of 10^6 kids of 1 to 100 candies and runs the ★
arm, taking its window as a `Slice[i32]`, on 10^6 windows of 100 of
them, each window's start and its extra drawn, each answer folded to the
sum of the places of the kids that can have the most. Each
implementation collects the answers into a fresh array, as the ★ arm
collects a `Vec[bool]`. Every implementation prints `10^6 windows of 100
kids: checksum 919274694`.

BENCHTAB

Measured by hand, Kāra takes 0.63 to 0.65 s against Rust's 0.42 to 0.46
s (0.48 to 0.49 s with overflow checks on), C's 0.14 to 0.17 s and Go's
0.29 to 0.32 s; Python takes 7.0 s.
