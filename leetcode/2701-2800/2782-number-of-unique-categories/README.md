# 2782. Number of Unique Categories

You are given an integer `n` and an object `categoryHandler` of class
`CategoryHandler`.

There are `n` elements, numbered from `0` to `n - 1`. Each element has a
category, and your task is to find the number of unique categories.

The class `CategoryHandler` contains the following function, which may
help you:

- `boolean haveSameCategory(integer a, integer b)`: Returns `true` if
  `a` and `b` are in the same category and `false` otherwise. Also, if
  either `a` or `b` is not a valid number (i.e. it's greater than or
  equal to `n` or less than `0`), it returns `false`.

Return *the number of unique categories.*

```
n = 6, categories = [1, 1, 2, 2, 3, 3]  ->  3
n = 5, categories = [1, 2, 3, 4, 5]     ->  5
n = 3, categories = [1, 1, 1]           ->  1
```

**Constraints:** `1 <= n <= 100`.

## Approaches

The problem is interactive: the categories are hidden, and a solution
learns about them only by asking the handler whether two elements share
one. Each arm takes the handler as a `mut ref CategoryHandler`, which
counts the questions; the harness plays LeetCode's judge.

| file | mechanism |
|---|---|
| `unique.kara` ★ | one representative of each category found so far; each element asked against them by `any`, and made one itself when it shares with none. At most n k questions, k the count of categories |
| `unique_earlier.kara` | by first elements: an element opens a category when no earlier element shares it, each element asked against every earlier one until one does. At most n(n - 1) / 2 questions |
| `unique_union.kara` | by union-find: every pair asked, those that share a category joined, the roots found with path halving, and the roots left counted. n(n - 1) / 2 questions |
| `unique_peel.kara` | by peeling: the elements not yet placed in a list; each round the first taken, the rest asked against it by `filter`, those that share its category dropped, one category per round. At most n k questions |
| `unique_solution.kara` | a Rust solution as LeetCode's Rust users write it, the handler by `&mut CategoryHandler` and each element counted when `(0..i).any(..)` finds no earlier one of its category, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples; 100
elements, LeetCode's most, all of one category and each of its own;
3000 random sets of 1 to 12 elements from 1 to 4 categories; and 300 of
100 elements from up to 100, the last two with the sum of the counts and
a checksum. `unique.py` mirrors the ★ arm and its output is
byte-identical.

```
3
5
1
1
100
3000 sets of up to 12: categories sum to 6398, checksum 914467063
300 sets of up to 100: categories sum to 12321, checksum 712010389
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the categories read straight from the judge's hidden list and
counted as a set; no questions. Its handler also counts the questions
about an element that is not there. It draws 2000 random sets of 1 to 12
elements from 1 to 4 categories, then 50 of up to 100 elements,
LeetCode's most, from up to 100, all before any arm answers; the literal
reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 12 elements, the count is the literal reading's |
| P2 | every category renamed, 1000 more: the same count |
| P3 | the elements reversed: the same count |
| P4 | an element of a new category put at the end: one more |
| P5 | from 1 to n, and 1 when every element has the first one's category; no question about an element that is not there, and no more than n(n - 1) / 2 questions |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 676862798, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a new element never made a representative | P1 2000, P4 2050, P5 2050, P6 2050 |
| M2 | ★: the first representative never asked | P1 1553, P3 288, P5 1871, P6 1584 |
| M3 | earlier: each element asked against itself as well | P1 2000, P4 2050, P5 2050, P6 2050 |
| M4 | earlier: the element just before never asked | P1 1326, P3 617, P5 1871, P6 1351 |
| M5 | union: a root found without climbing | none |
| M6 | union: the pairs that share a category left apart | P1 1696, P5 1871, P6 1746 |
| M7 | peel: a lone last element never given a round | P1 721, P3 340, P4 1288, P5 179, P6 762 |
| M8 | peel: the elements that share the first's category kept | P1 1567, P3 675, P4 2050, P5 1871, P6 1617 |
| M9 | solution: only the first half of the earlier elements asked | P1 1544, P3 798, P5 1871, P6 1593 |
| M10 | solution: a category counted when an earlier element shares it | P1 1759, P4 2050, P5 1965, P6 1808 |

## Benchmarks

The bench draws 1000 sets of 100 elements, LeetCode's most, from up to
100 categories, all of them first, then answers each 100 times by the ★
arm in all five languages, through a handler that counts its questions.
Every implementation prints `1000 sets of 100, 100 rounds: categories
sum to 3902400 after 173903500 questions, checksum 861265494`.

BENCHTAB

## Verification

All five arms print the same output as `unique.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written, but the harness did
not. Its handler's constructor took `categories: Vec[i64]` and moved it
into the struct, which `karac check` refused, a bare parameter
borrowing; and its `asked` counter was declared `mut asked: i64`, which
it warned is deprecated on a plain struct, whose fields are mutable
through the binding. `karac fix` made the parameter `own Vec[i64]` and
dropped the `mut`.

LeetCode's Rust template took 9 `karac fix` edits, the wrapper and the
harness included: `struct Solution {}` added; `&mut CategoryHandler`
became `mut ref CategoryHandler` in the solution and the wrapper, and
the wrapper's argument `mut handler`; `!` became `not`; the wrapper's
`as i64` on the answer, an `i32` widening by itself, was dropped;
`Solution::` became `Solution.`; and the harness's two fixes above.
