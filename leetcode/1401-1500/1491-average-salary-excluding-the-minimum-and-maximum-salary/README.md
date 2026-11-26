# 1491. Average Salary Excluding the Minimum and Maximum Salary

You are given an array of unique integers `salary` where `salary[i]` is
the salary of the `i`th employee. Return the average salary of employees
excluding the minimum and maximum salary. Answers within `10^-5` of the
actual answer will be accepted.

```
[4000,3000,1000,2000]  ->  2500.00000
[1000,2000,3000]       ->  2000.00000
```

**Constraints:** `3 <= salary.length <= 100`, `1000 <= salary[i] <=
10^6`, and all the integers of `salary` are unique.

The arms are `fn average(salary: Vec[i32]) -> f64`.

## Approaches

| file | mechanism |
|---|---|
| `average.kara` ★ | one pass keeping the sum, the least and the most; the average of the rest is the sum without those two over n - 2. O(n) |
| `average_sort.kara` | a sorted copy, whose first and last are the least and the most; the average of the slice `sorted[1..len - 1]` between them. O(n log n) |
| `average_fold.kara` | one `fold` carrying the least, the most and the sum in a tuple, its closure taking the tuple apart as `\|(lo, hi, s), x\|`. O(n) |
| `average_minmax.kara` | the iterator's `min`, `max` and `sum`, three passes, the sum taken as `i64`. O(n) |
| `average_solution.kara` | a Rust solution as LeetCode's Rust users write it (`*salary.iter().max().unwrap()`, `let sum: i32 = salary.iter().sum()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 8 lines, each average to five places:
LeetCode's two examples; four edges, the least and the most salaries
with one between, three close together, the most first and the least
last, and a mean that does not end (`500000.00000`, `1001.00000`,
`6000.00000`, `2001.33333`); the constraints' most, 100 salaries (`100
salaries: 237764.22449`); and 3000 random lists of 3 to 100 salaries,
each average folded to its cents (`3000 random lists: checksum
70326359`). `average.py` mirrors the ★ arm, and its output is
byte-identical; it rounds the cents half away from zero, as Kāra's
`round` does, where Python's own `round` would round half to even. Every
arm gives the same output under `karac __mir-run`, `karac run`, `karac
build` and `karac __mir-llvm-run`.

The Mend loop: the four Kāra arms check clean as first written. The Rust
solution takes one round of 6 fixes by `karac fix`'s count, and its diff
is: `struct Solution;` to `struct Solution {}`, each `Vec<i32>` to
`Vec[i32]` and `Solution::` to `Solution.`. Every arm's output matches
on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the salaries that have a lower one and a higher one in the
list, each found by comparing it with every other, summed and counted.
LeetCode's examples, the edges, and 1994 random lists of 3 to 12
different salaries from 2000 to 500000, so a doubled list and one with a
new least and most stay within the constraints. Each arm meets six
properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally, exactly |
| P2 | between the second least and the second most salary |
| P3 | the salaries in reverse order give the same average |
| P4 | every salary doubled doubles the average, exactly |
| P5 | a new least and a new most leave the mean of all the others |
| P6 | the ★ arm's answer |

The sums are whole numbers well within `f64`'s exact range and each
average is one division, so P1, P4 and P5 compare exactly. All 60,000
checks pass on every arm: `2000 cases: checksum 534313852, 60000 checks
over 5 arms: 0 failures`, under `karac __mir-run`, `karac run`, `karac
build` and `karac __mir-llvm-run`. Python, averaging the sorted list's
middle, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the least kept as the most | P1 2000, P2 616, P5 2000, P6 8000 |
| M2 | ★: the sum shared among n - 1 | P1 2000, P2 355, P5 2000, P6 8000 |
| M3 | sort: the most kept in the slice | P1 2000, P2 327, P5 2000, P6 2000 |
| M4 | sort: the copy not sorted, so its ends are not the least and the most | P1 1825, P2 269, P6 1825 |
| M5 | fold: the least started at 1000 | P1 1998, P2 222, P4 2000, P5 1994, P6 1998 |
| M6 | fold: each salary counted one more | P1 2000, P2 212, P4 2000, P5 2000, P6 2000 |
| M7 | minmax: the most taken out twice, the least kept | P1 2000, P2 616, P5 2000, P6 2000 |
| M8 | minmax: the first salary left out of the sum | P1 2000, P2 419, P3 2000, P5 2000, P6 2000 |
| M9 | solution: the least kept in the sum | P1 2000, P2 232, P5 2000, P6 2000 |
| M10 | solution: the first salary taken as the least | P1 1711, P2 333, P3 2000, P5 2000, P6 1711 |

## Benchmarks

The bench keeps 100 salaries, each in its own band of 9000 so they stay
different, and makes 2000000 calls of the ★ arm, each first moving one
salary within its band by the checksum so far, and folding the average's
cents into the checksum. C rounds the cents as `(int64_t)(x + 0.5)`, the
same as `round` for a positive value, so the bench needs no `-lm`. Every
implementation prints `2000000 calls: checksum 670134277`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.18 s against Rust's 0.18 s (0.19 s with overflow checks
on), C's 0.18 s and Go's 0.19 s; Python takes 10.4 s.
