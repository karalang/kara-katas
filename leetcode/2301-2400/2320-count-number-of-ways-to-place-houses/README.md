# 2320. Count Number of Ways to Place Houses

There is a street with `n * 2` **plots**, where there are `n` plots on
each side of the street. The plots on each side are numbered from `1`
to `n`. On each plot, a house can be placed.

Return *the number of ways houses can be placed such that no two houses
are adjacent to each other on the same side of the street*. Since the
answer may be very large, return it **modulo** `10^9 + 7`.

Note that if a house is placed on the `i`th plot on one side of the
street, a house can also be placed on the `i`th plot on the other side
of the street.

```
n = 1  ->  4
n = 2  ->  9
```

**Constraints:** `1 <= n <= 10^4`.

The two sides do not constrain each other, so the answer is the count
for one side squared. On one side, a placement of `i` plots ends in an
empty plot after any placement of `i - 1`, or in a house after one of
`i - 1` that ends empty: the counts are the Fibonacci numbers, `F(n +
2)` for `n` plots. O(n), or O(log n) by matrix powers.

## Approaches

| file | mechanism |
|---|---|
| `houses.kara` ★ | one side's placements ending in an empty plot and in a house, rolled forward a plot at a time, their sum squared |
| `houses_joint.kara` | both sides at once: four states for each plot index as two bits, no house, one on either side, or both, a state following another when they share no bit; the counts of the four in a `[1, 1, 1, 1]` array rolled forward. O(16 n) |
| `houses_table.kara` | every length kept: `ways[i] = ways[i - 1] + ways[i - 2]` in a `Vec.filled` of `n + 1`, and `ways[n]` squared. O(n) space |
| `houses_matrix.kara` | `[[1, 1], [1, 0]]` raised to `n + 1` by repeated squaring of `Array[Array[i64, 2], 2]` values, the top left `F(n + 2)` squared. O(log n) |
| `houses_iter.kara` | the pair of counts `fold`ed over `1..n` as a tuple, and their sum squared |
| `houses_solution.kara` | LeetCode's Rust template: `i32` in and out, a `const MOD` in the method, and a `vec!` table over `usize` indices; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five properties |

Every arm prints the same 7 lines: LeetCode's two examples; three plots
a side, ten, a hundred, and `10^4`; then every count of plots from 1
to 300, with a checksum and the counts in all. `houses.py` mirrors the
★ arm and its output is byte-identical.

`karac fix` carries the template in one call, reporting 6 edits.
`check` first reports two errors and offers 2 edits for them: `struct
Solution;` to `struct Solution {}`, and `Solution::` to `Solution.` in
the harness's wrapper. The other four follow from those: `n as usize`
to `n as i64`, the type of an index; `vec![0i64; n + 2]` to
`Vec.filled(n + 2, 0)`, the macro and the suffix of its `0i64`; and
the wrapper's `as i64` on the `i32` answer dropped, as it widens on its
own. The `const MOD: i64 = 1_000_000_007;` inside the method stands as
Kāra, and so does `as i32`.

The matrix arm was first written with Rust's `[[i64; 2]; 2]` for its
matrices. `karac check` names Kāra's `Array[T, N]` for each, and `karac
fix` rewrites them in 14 edits, writing the type on the two matrices'
`let`s as well.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to put a house or none on each of the `2 n`
plots, as the bits of a number, is tried, and counted when no two
houses stand on adjacent plots of the same side. No Fibonacci and no
squaring. That runs for 1 to 9 plots a side, up to `2^18` ways; every
arm answers for each count of plots from 1 to 360. The input is one
number, so the properties are about how an arm's answers sit together.

| | property |
|---|---|
| P1 | from 1 to 9 plots, the answer is the literal reading's |
| P2 | the answer is below `10^9 + 7`, and from 2 to 20 plots, where nothing has been reduced yet, a square, more than the answer for one plot fewer and at most four times it |
| P3 | from 4 plots on, `a(n) = 2 a(n-1) + 2 a(n-2) - a(n-3)` modulo `10^9 + 7`, `a` the arm's own answers |
| P4 | from 3 plots on, `a(n) a(n-2) = (a(n-1) + 1)^2` for an odd `n` and `(a(n-1) - 1)^2` for an even one, modulo `10^9 + 7` |
| P5 | each arm agrees with at least three of the other five |

P2's bounds hold because one side's count grows by less than twice a
plot, so its square by less than four times. P3 is the recurrence the
squares of Fibonacci numbers follow, and P4 is Cassini's identity,
`F(k+1) F(k-1) - F(k)^2 = (-1)^k`, squared, for `k = n + 1`.

The differential prints `360 counts of plots: checksum 367934163, 8664
checks over 6 arms: 0 failures` under every lane in Verification; the
checksum of the literal answers was checked against a Python reading
that tries the same `2^(2n)` ways. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the loop one plot short | P1 8, P2 1, P3 1, P4 358, P5 359 |
| M3 | ★: one side only, not squared | P1 9, P2 18, P3 357, P4 358, P5 360 |
| M6 | ★: the modulus `10^9 + 9` | P3 259, P4 339, P5 339 |
| M7 | joint: a house on both sides never at the first plot | P1 9, P2 18, P4 358, P5 360 |
| M8 | joint: two states fitting when together they leave a side empty | P1 8, P2 19, P3 357, P4 358, P5 359 |
| M11 | joint: each step reduced modulo `10^9 + 9` | P3 319, P4 338, P5 338 |
| M13 | table: no plots no way | P1 8, P2 1, P4 358, P5 359 |
| M14 | table: three plots back counted too | P1 7, P2 3, P3 357, P4 358, P5 358 |
| M15 | table: the table stopped one short | P1 8, P2 19, P3 1, P4 358, P5 359 |
| M18 | matrix: the base all ones | P1 8, P2 6, P3 357, P4 358, P5 359 |
| M19 | matrix: the even bits taken | P1 9, P2 19, P3 20, P4 358, P5 360 |
| M21 | matrix: the first term of each product left out | P1 9, P2 19, P4 358, P5 360 |
| M22 | iter: the fold begun with no house | P1 9, P4 358, P5 360 |
| M23 | iter: the house count kept, not the empty count | P1 7, P3 357, P4 179, P5 358 |
| M26 | iter: the side times the plots | P1 9, P2 19, P3 357, P4 358, P5 360 |
| M29 | solution: the modulus `10^9 + 6` | P3 250, P4 339, P5 339 |
| M30 | solution: the table filled from 3 | P1 8, P2 3, P4 358, P5 359 |

P4 and P5 kill all seventeen, P1 fourteen, P2 and P3 twelve each. P4,
Cassini's identity, holds for the squares of consecutive Fibonacci
numbers and almost nothing else, so every wrong sequence breaks it at
nearly every count. P1 misses only the three wrong moduli, since the
literal reading stops at 9 plots, long before a count reaches
`10^9`. P3 misses the edits that leave a sequence of squares of
numbers that add like Fibonacci's from some other start: no plots
counted as no way, a house on both sides never at the first plot, the
fold begun with no house, the first term of each product left out, and
the table filled from 3, where only the first steps are wrong. P2 misses the moduli
again, and the edits whose answers are still squares that grow by
less than four times.

Of the thirty-one, fourteen were not kept. Seven fail as the iter
arm's fold begun with no house (M22), each answering for a count of
plots one off or a Fibonacci sequence shifted by one: the table's (M12)
and the template's (M27) one plot one way, the matrix arm's power `n`
(M17) and top right read for the count (M20), and the iter arm's fold
over every plot (M24) and side the placements ending empty (M25). The
★ arm's house allowed after a house (M1) and house count taken after
the empty count moves on (M5) fail as the matrix arm's base all ones
(M18), counting `2^n` a side; the joint arm's state allowed after
itself (M9) as its two states fitting when they leave a side empty
(M8); its houses on both sides left out of the total (M10) as its
house on both sides never at the first plot (M7); the table's count
for one plot fewer on the second side (M16) and the template's answer
read one plot on (M28) as the matrix arm's first term of each product
left out (M21); the template's no plots no way (M31) as the table's
(M13). The ★ arm's two sides added, not multiplied (M4), fails apart
from every kept one, and was left out to keep three to an arm.

M11 replaces the joint arm's counts never moved on, which failed as its
two states fitting when they leave a side empty (M8). Its houses on
both sides counted twice in the total and a house on the second side
never after an empty plot index were tried for it and fail as M21 and
M8; no more than 300 plots walked fails apart from every kept one.

## Verification

Every arm prints the same output as `houses.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★ and table arms take 0.2 s, the matrix,
iter and template arms 0.25 s, and the joint arm, which tries 16 pairs
of states a plot, 0.4 s. The differential takes 2.3 s there, most of it
the literal reading's `2^18` ways for 9 plots, and 0.6 s under `karac
__mir-llvm-run`.

## Benchmarks

The bench makes 10 passes over every count of plots from 1 to `10^4`,
pass `p` folding each answer plus `p` into the checksum, with the ★ arm
in all five languages: about `5 * 10^8` steps of an addition and a
remainder. Every implementation prints `10 passes over every count of
plots up to 10^4: checksum 54735521`. Each keeps the two counts in
64-bit integers, and none holds any data.

BENCHTAB
