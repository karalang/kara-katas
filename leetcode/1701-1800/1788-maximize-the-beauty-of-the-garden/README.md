# 1788. Maximize the Beauty of the Garden

There is a garden of `n` flowers in a line, and each flower has a
beauty, given as `flowers`. A garden is valid if it has at least two
flowers and its first and last flowers have the same beauty. You may
remove any flowers, possibly none, to make the garden valid. The beauty
of a garden is the sum of its flowers' beauties. Return the most
beautiful valid garden you can make.

```
flowers = [1, 2, 3, 1, 2]     ->  8    (keep [2, 3, 1, 2])
flowers = [100, 1, 1, -3, 1]  ->  3    (keep [1, 1, 1])
flowers = [-1, -2, 0, -1]     ->  -2   (keep [-1, -1])
```

**Constraints:** `2 <= flowers.length <= 10^5`, `-10^4 <= flowers[i] <=
10^4`, and a valid garden can always be made.

The arms are `fn maximum_beauty(flowers: Vec[i32]) -> i32`.

## Approaches

A garden whose first and last flowers have beauty `v` keeps both, and of
the flowers between them every positive one.

| file | mechanism |
|---|---|
| `maximum_beauty.kara` ★ | a prefix sum of the positive beauties, and a `Map` of each beauty's first position: the best garden that ends at a flower starts at the first flower of the same beauty, since the sum of positives only grows to the left, so each later flower of a beauty closes a candidate `2 * v + positive[j] - positive[i + 1]`. O(n) |
| `maximum_beauty_twopass.kara` | a first pass records each beauty's last position; the second, at each beauty's first position, closes the garden at its last, the best kept in an `Option`. O(n) |
| `maximum_beauty_sorted.kara` | the positions sorted by beauty with the stable `sort_by_key`, which keeps each beauty's positions in order, so each run of one beauty starts at its first position and ends at its last, and a run of two or more is a garden. O(n log n) |
| `maximum_beauty_beststart.kara` | one pass that keeps, for each beauty, the best garden opened so far less the positives up to there, with no use of the first position being best: opening at `i` is worth `v` less the positive sum through `i`, and closing at `j` adds `v` and the positive sum before `j`. O(n) |
| `maximum_beauty_solution.kara` | a Rust solution as LeetCode's Rust users write it (`HashMap<i32, usize>` from `std::collections`, `vec![0i64; n + 1]`, `for (j, &v) in flowers.iter().enumerate()`, `if let Some(&i) = first.get(&v)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples (`8 3 -2`);
five edges, two flowers alike positive and negative, a negative pair
around a large positive, a best pair that is not the largest beauty, and
two pairs of which the inner is better (`10 -10 48 22 8`); the
constraints' most, 100000 flowers of `10^4`, whose garden is `10^9`,
100000 of `-10^4`, and 100000 at random (`the most: 1000000000 -20000
163362508`); and 3000 random gardens of 2 to 30 flowers from -10 to 10,
each with two flowers made alike (`3000 random cases: checksum
777318062`). `maximum_beauty.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, twopass, sorted and beststart arms and the harness
check clean as first written. The Rust solution takes one round of 21
fixes by `karac fix`'s count, and its diff is: the `use
std::collections::HashMap;` line deleted, `struct Solution;` to `struct
Solution {}`, `Vec<i32>` to `Vec[i32]`, `vec![0i64; n + 1]` to
`Vec.filled(n + 1, 0)`, the `as i64` after `flowers[i].max(0)` dropped,
`HashMap<i32, usize>` to `Map[i32, i64]` and `HashMap::new()` to
`Map.new()`, `i64::MIN` to `i64.MIN`, `for (j, &v)` to `for (j, v)`, `if
let Some(&i) = first.get(&v)` to `if let Some(i) =
first.get(v).cloned()`, and `Solution::` to `Solution.`. Its `2 * v as
i64` stays. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every set of flowers left, at least two whose first and last
are alike, its beauties summed, while there are at most 12 flowers.
LeetCode's examples, the five edges, 20000 flowers three ways (all
`10^4`, all `-10^4`, at random), and 1989 random gardens, half of 2 to
12 flowers from -6 to 6 and half of 2 to 40 from `-10^4` to `10^4`. Each
arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally, while there are at most 12 flowers |
| P2 | the flowers reversed give the same answer |
| P3 | a flower of `10^4 + 1`, above every other, at each end: the answer is those two and every positive flower |
| P4 | never less than two flowers alike side by side, nor more than the largest repeated beauty twice and every positive flower |
| P5 | every beauty doubled doubles the answer |
| P6 | the ★ arm's answer |

The differential checks clean as first written. All 56,455 checks pass
on every arm: `2000 cases: checksum 568486931, 56455 checks over 5 arms:
0 failures`, under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. Python, running the ★ arm's mirror over the same
cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the first flower's own positive part counted twice | P1 731, P3 2000, P6 4056 |
| M2 | ★: the negative flowers between kept too | P1 631, P2 128, P3 1893, P4 23, P6 4920 |
| M3 | twopass: a lone flower taken as a garden | P1 482, P4 377, P6 827 |
| M4 | twopass: the closing flower left out | P1 1205, P3 2000, P4 529, P6 1914 |
| M5 | sorted: each garden closed at the second flower alike | P1 204, P2 140, P6 206 |
| M6 | sorted: beauties one apart taken as alike | P1 447, P2 441, P3 2, P4 126, P5 456, P6 456 |
| M7 | beststart: the closing flower's positive part counted twice | P1 731, P3 2000, P6 1014 |
| M8 | beststart: the opening flower's positive part counted twice | P1 731, P3 2000, P6 1014 |
| M9 | solution: the closing flower's positive part counted twice | P1 731, P3 2000, P6 1014 |
| M10 | solution: each garden opened at the last flower alike seen | P1 176, P6 178 |

## Benchmarks

The bench builds 400 gardens of 2000 random flowers from `-10^4` to
`10^4` once, the last flower of each made alike to its first, and makes
10000 calls of the ★ arm, each garden drawn from the checksum so far. It
checks clean as first written. Every implementation prints `10000 calls
over 400 gardens: checksum 913279325`. The C mirror keeps the first
positions in a small open-addressing hash table, as the other languages'
maps do.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.62 s against Rust's 0.88 s (0.84 s with
overflow checks on), C's 0.17 s and Go's 1.9 s; Python takes 3.7 s.
