# 1447. Simplified Fractions

Given an integer `n`, return a list of all simplified fractions between
`0` and `1` (exclusive) such that the denominator is
less-than-or-equal-to `n`. You can return the answer in any order.

```
n = 2  ->  ["1/2"]
n = 3  ->  ["1/2","1/3","2/3"]
n = 4  ->  ["1/2","1/3","1/4","2/3","3/4"]
```

**Constraints:** `1 <= n <= 100`.

Each arm is `fn simplified_fractions(n: i32) -> Vec[String]`. The answer
may come in any order, so the harness and the differential sort each
answer before comparing or printing it.

## Approaches

| file | mechanism |
|---|---|
| `simplified_fractions.kara` ★ | every numerator below every denominator up to n, kept when the two share no factor, by Euclid's `gcd` written as a recursion. O(n² log n) |
| `simplified_fractions_marks.kara` | a grid of numerator and denominator: each fraction is met first in its lowest terms, and its multiples are then marked to pass over. No `gcd`. O(n² log n) |
| `simplified_fractions_farey.kara` | the Farey sequence of order n from 0/1, each next fraction found from the two before it, until 1/1, by a four-way assignment. O(n²) |
| `simplified_fractions_tree.kara` | the Stern-Brocot tree between 0/1 and 1/1: the mediant of two neighbours while its denominator is at most n, by a recursion with the fractions on either side of it before and after. O(n²) |
| `simplified_fractions_solution.kara` | a Rust solution as LeetCode's Rust users write it (two loops, `Self::gcd` on each pair, `format!` for each fraction kept), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and n = 1
(`[] [1/2] [1/2, 1/3, 2/3] [1/2, 1/3, 1/4, 2/3, 3/4]`); the constraints'
most (`n = 100: 3043 fractions, checksum 505625353`); and every n from 1
to 100 (`every n to 100: 104259 fractions, checksum 318222481`).
`simplified_fractions.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, marks and tree arms check clean as first written.
The Farey arm moved on by `(a, b, c, d) = (c, d, k * c - a, k *
d - b);`, which `karac check` refuses, saying a parenthesized tuple is a
value and not a place, and `karac fix` drops the parentheses, `a, b, c,
d = c, d, ..`; `b` then started at a bare `1` and fed `d`, an `i32` from
`n`, and is refused as the default `i64`, and `karac fix` writes `1i32`,
2 fixes. The Rust solution takes one round of 10 fixes by `karac fix`'s
count: `struct Solution;` to `struct Solution {}`, `Vec<String>` to
`Vec[String]`, `Vec::new()` to `Vec.new()`, `Self::gcd` to
`Solution.gcd`, `format!("{}/{}", m, d)` to `f"{m}/{d}"`, and
`Solution::` to `Solution.`. Every arm's output matches on the first
run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every fraction between 0 and 1 with a denominator up to n,
kept when no fraction with a smaller denominator is the same number,
while n is at most 40. The input is one number from 1 to 100, so the
differential runs every n the constraints allow.

Two of its first lines are refused and fixed. Reading a fraction back as
`f.split("/").map(|p| p.parse().unwrap())` into a `Vec[i64]` is refused,
`parse` taking its type from an expected `Option[T]`, and `karac fix`
writes `i64.parse(p)`. P1's `if let Some(w) = want` inside the loop over
the arms is refused, as it moves `want` on the first pass, and `karac
fix` writes `Some(ref w)`. 2 fixes.

| | property |
|---|---|
| P1 | the statement read literally, while n is at most 40 |
| P2 | every fraction for n - 1 is there, and the rest have the denominator n |
| P3 | written plainly, each between 0 and 1 with a denominator up to n, and no two the same number |
| P4 | a/d is there exactly when (d - a)/d is |
| P5 | as many as the totients of 2 to n add to |
| P6 | the ★ arm's answer |

All 2,700 checks pass on every arm: `100 cases: checksum 318222481, 2700
checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac run`,
`karac build` and `karac __mir-llvm-run`. Python, by the set of each n's
`Fraction` values, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a pair kept when its greatest common factor is 2 | P1 37, P3 97, P5 97, P6 388 |
| M2 | ★: the common factor taken as soon as a remainder of 1 is met | P1 39, P5 99, P6 396 |
| M3 | marks: no multiple ever marked | P1 37, P3 97, P5 97, P6 97 |
| M4 | marks: the doubles of a fraction left unmarked | P1 37, P3 97, P5 97, P6 97 |
| M5 | farey: the walk stopped at 1/2, the first fraction one short of 1 | P1 39, P4 98, P5 99, P6 99 |
| M6 | farey: the fractions with the denominator n left out | P1 39, P2 98, P5 99, P6 99 |
| M7 | tree: no mediant with the denominator n | P1 39, P2 98, P5 99, P6 99 |
| M8 | tree: the right of each mediant searched one denominator short | P1 38, P2 92, P4 98, P5 98, P6 98 |
| M9 | solution: no numerator 1 | P1 39, P4 98, P5 99, P6 99 |
| M10 | solution: no denominator n | P1 39, P2 98, P5 99, P6 99 |

## Benchmarks

The bench asks the ★ arm for every n from 1 to 100, 100 times over, and
folds the count of each answer's letters to a checksum. Each
implementation builds each fraction's text with its own library's
formatting: Rust's `format!`, C's `snprintf` into a fresh allocation,
Go's `fmt.Sprintf` and Python's f-string. Every implementation prints
`10000 answers: checksum 58343962`.

BENCHTAB

Kāra is ahead of Rust here, measured by hand at 0.68 to 0.77 s against
Rust's 1.25 s (1.22 to 1.23 s with overflow checks on), C's 1.23 s and
Go's 2.8 s; Python takes 5.5 s.
