# 1128. Number of Equivalent Domino Pairs

Given a list of `dominoes`, `dominoes[i] = [a, b]` is equivalent to
`dominoes[j] = [c, d]` if and only if either (`a == c` and `b == d`), or
(`a == d` and `b == c`), that is, one domino can be rotated to be equal
to another domino.

Return the number of pairs `(i, j)` for which `0 <= i < j <
dominoes.length`, and `dominoes[i]` is equivalent to `dominoes[j]`.

```
dominoes = [[1,2],[2,1],[3,4],[5,6]]              ->  1
dominoes = [[1,2],[1,2],[1,1],[1,2],[2,2]]        ->  3
```

**Constraints:** `1 <= dominoes.length <= 4 * 10^4`;
`dominoes[i].length == 2`; `1 <= dominoes[i][j] <= 9`.

The arms are `fn num_equiv_domino_pairs(dominoes: Vec[Vec[i32]]) -> i64`.

## Approaches

Each arm reads a domino by its smaller number and its larger one, so a
domino and its turn are the same kind; `c` dominoes of one kind make
`c * (c - 1) / 2` pairs.

| file | mechanism |
|---|---|
| `num_equiv_domino_pairs.kara` ★ | one pass: each domino is one of 100 keys `10 * low + high`, and each new domino pairs with every one already counted under its key, in an array of 100 counts. O(n) |
| `num_equiv_domino_pairs_map.kara` | the same pass with a `Map` from the `(low, high)` tuple to how many came before. O(n) |
| `num_equiv_domino_pairs_sort.kara` | each domino's key in a list, the list sorted, and every run of `r` equal keys giving `r * (r - 1) / 2` pairs. O(n log n) |
| `num_equiv_domino_pairs_grid.kara` | a 10 by 10 grid counts the dominoes by their low and high number, then each cell of `c` gives `c * (c - 1) / 2` pairs. O(n) |
| `num_equiv_domino_pairs_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, a `HashMap<(i32, i32), i32>` counted through `entry().or_insert()`, the pairs summed from the counts with a `&v` pattern), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 11 lines: the answers for LeetCode's two
examples and six more (one domino, four alike, a pair and its turn
twice, the highest numbers, a ring of three, and a mix), then over 2000
random sets of up to 400 dominoes, their numbers up to 1 to 9, the
pairs summed and a checksum (`2000 random sets: pairs total 11594013,
checksum 388455082`), and two of LeetCode's largest: 40,000 dominoes at
random, and 40,000 alike, half of them turned (`799980000 pairs`).
`num_equiv_domino_pairs.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every pair `i < j`, equivalent when `a == c and b == d` or
`a == d and b == c`. It checks 2000 problems in four kinds of 500: up to
30 dominoes of any numbers; up to 30 of the numbers 1 to 3; up to 40 of
1 and 2 alone; and up to 40 drawn from three dominoes, each turned or
not. Every random choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | by a second reading, two dominoes alike when their sums and their products agree: each domino counts the others it matches, and the total is twice the answer |
| P3 | each domino turned gives the same answer |
| P4 | the dominoes in reverse order give the same answer |
| P5 | a copy of every domino appended gives `4 * answer + n`: a kind of `c` becomes `2c`, and `2c * (2c - 1) / 2 = 4 * c * (c - 1) / 2 + c` |
| P6 | each number `k` relabelled `10 - k` gives the same answer |

All 60,000 checks pass on every arm: `2000 problems: checksum
791917642, 60000 checks over 5 arms: 0 failures`. A Python reading of
the same problems, comparing every pair as sorted lists, gives the same
checksum.

## Mutation testing

Twenty-five edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`
(the Map and solution arms keep a `Map`), each failing the same way
under both. All twenty-five are caught. Fifteen are kept, no two failing
the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: keyed by the sum of its numbers | P1 803, P2 803 |
| M2 | ★: the most pairs one domino makes kept | P1 1640, P2 1640, P5 1946 |
| M3 | ★: the first domino skipped | P1 1460, P2 1460, P4 1033, P5 2000 |
| M4 | Map: a domino keyed as written | P1 1589, P2 1589 |
| M5 | Map: a kind counted once however often it comes | P1 1462, P2 1462, P5 1789 |
| M6 | Map: a turned domino keyed by its smaller number twice | P1 1648, P2 1648, P3 1369, P6 1523 |
| M7 | sort: the keys left unsorted | P1 1683, P2 1683, P5 1920 |
| M8 | sort: the key after each run skipped | P1 1609, P2 1609, P5 1896, P6 1359 |
| M9 | sort: keyed by the smaller number alone | P1 1522, P2 1522, P6 1525 |
| M10 | grid: the row the first number, not the smaller | P1 1622, P2 1622, P3 1344, P6 1519 |
| M11 | grid: the row of 1s never read | P1 1343, P2 1343, P5 1670, P6 1471 |
| M12 | grid: the column of 9s never read | P1 385, P2 385, P5 653, P6 1471 |
| M13 | solution: each kind counted from 1 | P1 2000, P2 2000, P5 2000 |
| M14 | solution: each pair counted from both ends | P1 1789, P2 1789, P5 2000 |
| M15 | solution: the commonest kind's pairs alone | P1 1575, P2 1575, P5 1920 |

P1 and P2 catch all fifteen, P5 ten, P6 six, P3 two and P4 one. P2
fails on exactly the problems P1 does: it reads the answer as a count of
matched ends, which pins it as tightly as the literal count. P5 sees
the edits that get a kind's pairs wrong from its count, since doubling
every count moves the answer by a rule the wrong count breaks. P6 sees
the edits that treat some number apart from the others (the 1s, the
9s, the smaller number alone), since relabelling moves which one that
is. P3 sees only the edits that read the two halves of a domino
differently, and P4 only the arm that skips a domino by its place.

P3 to P6 together catch thirteen. M1 and M4 pass every self-comparison:
an arm keyed by a domino's sum, or by its numbers as written, answers
the turned, reversed, doubled and relabelled sets consistently wrong,
since each of those changes every domino the same way. Only the two
readings of the answer see them.

Of the ten not kept, seven fail exactly as a kept one: keying a domino
as written in the ★ and solution arms as M4; a domino pairing with
itself in the ★ arm, a new kind taken for seen once in the Map arm, a
cell of `c` giving `c * (c + 1) / 2` in the grid arm, all as M13; a
domino pairing with at most one before it in the Map arm and a run of
`r` giving `r - 1` pairs in the sort arm, both as M5; the grid arm's
column taken from the second number as M6; and the solution arm
counting each kind once as M14. The sort arm's run of `r` giving `r * r
/ 2` fails in a way of its own but was not needed.

## Verification

Every arm prints the same output as `num_equiv_domino_pairs.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The kata found two gaps, both fixed. The ★, Map, sort and grid arms
were written as Kāra, the solution arm as Rust writes it.

The harness builds the 40,000 alike dominoes with `(0..40000).map(|i|
if i % 2 == 0 { [4, 7] } else { [7, 4] }).collect()` into a
`Vec[Vec[i32]]`, which was refused: `Vec[Vec[i32]]` implements
`FromIterator[Vec[i32]]`, not `FromIterator[Vec[i64]]`. The closure is
checked against `map`'s return parameter, which nothing had fixed yet,
and a number it gives was typed `i64` on the spot. The values a closure
gives such a parameter (its tail, a block's, each branch of an `if` or
`match`) are now open as a `let`'s value is, and a `collect` whose
target the body fixed types them before the body's numbers take their
defaults (B-2026-11-11-86).

The sort arm measures a run as Rust does, `let run = (j - i) as i64;`.
`karac fix` deleted the redundant `as i64` and left `let run = (j -
i);`, parentheses that group nothing. Around a `let`'s whole value
nothing binds, so they now go with the `as` (B-2026-11-11-87). `karac
fix` then carried the sort arm to a clean check in two rounds, `&&` to
`and` and the cast. It carried the solution arm in three: the `use`
line dropped, `Vec<..>` and `HashMap<..>` to `[..]`, `::` to `.`, and
the `&v` pattern to `v`; then `struct Solution {}` declared and
`HashMap` to `Map`; then the `as i64` at the call dropped, an `i32`
widening by itself.

## Benchmarks

The bench builds 16 random sets of 4 * 10^4 dominoes once, LeetCode's
largest, their numbers 1 to 9. Each of 300 rounds changes one number of
one domino in every set and counts the set's pairs with the ★ arm: 4800
passes over 4 * 10^4 dominoes. Every implementation prints `300 rounds
over 16 sets of 4 * 10^4 dominoes: pairs total 89540929641, checksum
333758423`. Each keeps the dominoes as LeetCode hands them, a list of
two-number lists (`Vec[Vec[i32]]`, `Vec<Vec<i32>>`, `[][]int`, Python
lists, and C's `int **` with each domino allocated by itself), and the
counts in an array of 100.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `0385ddd3ac`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.371 to 0.522 s | 0.464 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.374 to 0.518 s | 0.466 s |
| Rust (`rustc -O`) | 0.427 to 0.547 s | 0.528 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.428 to 0.557 s | 0.528 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.440 to 0.576 s | 0.529 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.516 to 0.572 s | 0.540 s |
| Kāra (`karac build`) | 0.447 to 0.572 s | 0.542 s |
| Go | 1.332 to 1.494 s | 1.424 s |
| Python | 17.2 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra takes about the time of Rust, a few percent more, and about
1.2x C's; the three walk the same pointers to the same two-number
allocations and count in the same array of 100. Go takes about 2.6x
Kāra's time, and as much with its collector off (`GOGC=off`, 1.38 s on
one run against 1.29 s with it), so the gap is not its collector; it was
not traced further. Python takes about 32x Kāra's time.
