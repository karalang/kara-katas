# 1237. Find Positive Integer Solution for a Given Equation

Given a callable function `f(x, y)` with a hidden formula and a value
`z`, reverse engineer the formula and return all positive integer pairs
`x` and `y` where `f(x, y) == z`. You may return the pairs in any order.

While the exact formula is hidden, the function is monotonically
increasing, i.e.:

- `f(x, y) < f(x + 1, y)`
- `f(x, y) < f(x, y + 1)`

The judge has a list of 9 hidden implementations of `CustomFunction`,
and a way to generate an answer key of all valid pairs for a specific
`z`. It receives `function_id` (which implementation to test) and `z`,
calls `findSolution`, and compares the result with the answer key.

```
function_id = 1, z = 5  ->  [[1,4],[2,3],[3,2],[4,1]]    f(x, y) = x + y
function_id = 2, z = 5  ->  [[1,5],[5,1]]                f(x, y) = x * y
```

**Constraints:** `1 <= function_id <= 9`; `1 <= z <= 100`; it is
guaranteed that the solutions of `f(x, y) == z` are within `1 <= x, y <=
1000`; it is also guaranteed that `f(x, y)` fits in a 32-bit signed
integer for `1 <= x, y <= 1000`.

The judge here is a `pub struct CustomFunction { id: i32 }` whose `pub
fn f(self, x: i32, y: i32) -> i32` is one of the nine functions LeetCode
uses (`x + y`, `x * y`, `x² + y`, `x + y²`, `x² + y²`, `(x + y)²`, `x³ +
y³`, `x² · y`, `x · y²`), and the arms are `fn find_solution(
customfunction: CustomFunction, z: i32) -> Vec[Vec[i32]]`, the function
borrowed.

## Approaches

| file | mechanism |
|---|---|
| `find_positive_integer_solution_for_a_given_equation.kara` ★ | two pointers: `x` rising from 1 and `y` falling from 1000. Since `f` increases in both, a value below `z` can only be helped by a larger `x` and one above it by a smaller `y`, so each step moves one of them and every solution is met. O(x + y) calls |
| `find_positive_integer_solution_for_a_given_equation_bisect.kara` | for each `x`, a binary search over `y` for the least `y` with `f(x, y) >= z`, kept when it is equal; `x` stops once `f(x, 1)` is past `z`. O(x log y) calls |
| `find_positive_integer_solution_for_a_given_equation_grid.kara` | the grid walked row by row, each row of `y` cut short by `take_while` at the first value past `z`, the pairs gathered by `flat_map` and `filter` over ranges. O(x · y) calls at worst |
| `find_positive_integer_solution_for_a_given_equation_pointers.kara` | a Rust solution as LeetCode's Rust users write it (two pointers from `(1, 1000)`, a `match` on `customfunction.f(x, y).cmp(&z)` over `std::cmp::Ordering`'s three variants, each pair pushed as `vec![x, y]`), carried to Kāra by `karac fix` |
| `find_positive_integer_solution_for_a_given_equation_search.kara` | another Rust solution (the `y`s collected into a `Vec<i32>`, and for each `x` an `if let Ok(i)` over `ys.binary_search_by(\|&y\| customfunction.f(x, y).cmp(&z))`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples, and the
number of pairs and a checksum of them for all nine functions and every
`z` from 1 to 100 (`7097 pairs, checksum 657848550`). Every arm lists
the pairs by rising `x`, and the checksum reads them in that order.
`find_positive_integer_solution_for_a_given_equation.py` mirrors the ★
arm, and its output is byte-identical. Every arm gives the same output
under `karac run` and `karac build`, and under the AddressSanitizer
build.

The Mend loop: the ★, bisect and grid arms check clean as written. The
pointers arm takes one round of 19 fixes (among them `&CustomFunction`
to `CustomFunction`, `Vec<Vec<i32>>` to `Vec[Vec[i32]]`, `vec![]` to
`Vec.new()`, `let (mut x, mut y)` to `let mut (x, y)`, `&&` to `and`,
`.cmp(&z)` to `.cmp(z)`, `std::cmp::Ordering::Less` to `Ordering.Less`,
`vec![x, y]` to `[x, y]`) and the search arm one round of 13 (among them
`|&y|` to `|y|`, and the `if let Ok(i)` over `binary_search_by` to two
`partition_point` searches, the pair kept when the first `y` not below
`z` comes before the first `y` above it), and both check clean.

## Gaps

None.

## Differential

`differential.kara` holds copies of the five arms, a judge of its own
and the statement read literally: every pair in the square from 1 to
`z`, since `f(x, y) >= max(x, y)`. The judge is LeetCode's nine
functions for a quarter of the cases and `a·x^p + b·y^q + c·x·y` for the
rest, with `p` and `q` from 1 to 3, positive `a` and `b` and `c` from 0
to 100 (a third of them with every coefficient 1, so that `z` is often
reached), each value of `x, y <= 1000` fitting an `i32`; `swap` reads it
as `f(y, x)`. 2000 cases, `z` from 1 to 100.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | every pair solves it, both values in 1 to 1000 |
| P3 | no pair twice |
| P4 | the function's arguments swapped give the pairs swapped |
| P5 | one pair at most for each `x` |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 cases: checksum 6451153,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python, with the
same judge, gives the same checksum and the same 7511 pairs in its 686
cases with any.

## Mutation testing

Ten edits to the differential, one to three to each arm, each run under
`karac __mir-run` and `karac run`.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a pair never recorded, an equal value read as below | P1 686, P6 2744 |
| S2 | ★: the pointers stop before either edge | P1 418, P4 620, P6 1672 |
| S3 | ★: after a pair only `x` moves | NOT CAUGHT |
| B1 | bisect: the walk stops at the first `x` that reaches `z` | P1 418, P4 620, P6 418 |
| B2 | bisect: the search finds the first value above `z` | P1 686, P6 686 |
| G1 | grid: each column cut below `z` | P1 686, P6 686 |
| G2 | grid: the filter left out | P1 1065, P2 1065, P5 1005, P6 1065 |
| P1 | pointers: `x` starts at 2 | P1 429, P4 620, P6 429 |
| P2 | pointers: a value above `z` moves `x` | P1 686, P6 686 |
| R1 | search: the upper bound taken as the lower | P1 686, P6 686 |

Nine of the ten are caught, each by P1, the statement read literally,
and P6. The tenth, S3, the ★ arm moving only `x` after a pair, is an
equivalent mutant: `f` is increasing in each argument, so the next step
finds `f(x + 1, y) > z` and moves `y` down then, one step later, to the
same pairs. Five mutations lose every pair in all 686 cases that have
one: an equal value read as below (S1), the bisect arm's search for the
first value above `z` (B2), the grid's columns cut below `z` (G1), the
pointers arm moving `x` on a value above `z` (P2), and the search arm
taking the upper bound as the lower (R1). Three lose the pairs at an
edge, 418 to 429 cases: the ★ pointers stopping before either edge (S2),
the bisect walk stopping at the first `x` that reaches `z` (B1), and the
pointers arm starting at `x = 2`; P4, the function's arguments swapped,
catches those three, since swapping moves the lost edge to the other
side. G2, the grid without its filter, returns every pair under `z` and
fails P2, every pair solving the equation, and P5, one pair for each
`x`, as well. P3, no pair twice, catches none.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm, two pointers, `x` rising from 1 and `y` falling from 1000. O(x + y)
calls. Every program prints `9 functions, z from 1 to 100, 30 passes:
checksum 792243272`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.067 to 0.099 s | 0.069 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.066 to 0.089 s | 0.070 s |
| Rust (`rustc -O`) | 0.062 to 0.086 s | 0.064 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.054 to 0.085 s | 0.056 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.054 to 0.082 s | 0.056 s |
| C (`clang -O3`) | 0.055 to 0.086 s | 0.058 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.055 to 0.062 s | 0.057 s |
| Go | 0.074 to 0.106 s | 0.076 s |
| Python | 6.057 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on is about 20% ahead of Kāra (0.056 s
against 0.070 s), and the two ranges overlap. C is about 17% ahead of
Kāra (0.058 s against 0.070 s); Kāra is about 8% ahead of Go (0.070 s
against 0.076 s). Python takes about 87x Kāra's time. No profile was
taken.
