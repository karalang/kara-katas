# 2318. Number of Distinct Roll Sequences

You are given an integer `n`. You roll a fair 6-sided dice `n` times.
Determine the total number of **distinct** sequences of rolls possible
such that the following conditions are satisfied:

1. The **greatest common divisor** of any **adjacent** values in the
   sequence is equal to `1`.
2. There is **at least** a gap of `2` rolls between **equal** valued
   rolls. More formally, if the value of the `i`th roll is **equal** to
   the value of the `j`th roll, then `abs(i - j) > 2`.

Return *the **total number** of distinct sequences possible*. Since the
answer may be very large, return it **modulo** `10^9 + 7`.

Two sequences are considered distinct if at least one element is
different.

```
n = 4  ->  184
n = 2  ->  22
```

**Constraints:** `1 <= n <= 10^4`.

Whether a roll can follow depends only on the two rolls before it: it
must be coprime with the last and unlike both. So the count of
sequences ending in each of the 36 pairs of rolls is all a step needs,
and each roll moves that table forward once. O(216 n).

## Approaches

| file | mechanism |
|---|---|
| `rolls.kara` ★ | a `[[0; 6]; 6]` table of the sequences ending in each pair, rolled forward `n - 2` times into a fresh table |
| `rolls_memo.kara` | top down: `ways(left, a, b)` recursing on each next roll, 0 for no roll yet, memoized in a flat `Vec` by `left`, `a` and `b` through a `mut ref` |
| `rolls_table.kara` | every length kept: a `Vec` of `n - 1` layers of 6 by 6 counts, each built from the one before |
| `rolls_matrix.kara` | the 36 pairs as states of a 36 by 36 matrix of which pair can follow which, raised to the power `n - 2` by repeated squaring and applied to the 30 opening pairs. O(36^3 log n) |
| `rolls_iter.kara` | the 36 counts in one flat `Vec`, each step `map`ping every pair to the `sum` of the pairs `filter`ed to precede it, and the last `fold`ed into the total |
| `rolls_solution.kara` | LeetCode's Rust template: a `gcd` nested in the method, `vec![vec![0i64; 7]; 7]` over the rolls 1 to 6, a `const MOD` in the body, and an `i32` answer; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's two examples; one roll,
three, ten, a hundred, and `10^4` rolls; then every count of rolls from
1 to 300, with a checksum and the counts in all. `rolls.py` mirrors the
★ arm and its output is byte-identical.

`karac fix` carries the template in one call, reporting 22 edits.
`check` first reports eight errors and offers 9 edits for them:
`struct Solution;` to `struct Solution {}`; the nested `fn gcd`, which
captures nothing, moved above `impl Solution`, one edit to write it
there and one to delete it here; the three `&&` to `and`; `&dp` to
`ref dp` and the pattern `&x` to `x`; and `Solution::` to `Solution.`
in the harness's wrapper. The other thirteen follow from those:
`gcd`'s three `usize` to `i64`; the four `vec!` of the two tables to
`Vec.filled` and the suffixes of their `0i64` and of the total's
dropped; and the wrapper's `as i64` on the `i32` answer. The `const
MOD: i64 = 1_000_000_007;` inside the method stands as Kāra, and so
does `total as i32`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every sequence is built one roll at a time, a roll refused
when it shares a factor from 2 to 6 with the roll before it or equals
any roll within two places of it, and every sequence that reaches `n`
rolls is counted. No table of pairs. That walk is run for 1 to 12
rolls, up to 742408 sequences; every arm answers for each count of
rolls from 1 to 360. The input is one number, so the properties are
about how an arm's answers sit together.

| | property |
|---|---|
| P1 | from 1 to 12 rolls, the answer is the literal reading's |
| P2 | the answer is below `10^9 + 7`, and from 2 to 16 rolls, where nothing has been reduced yet, at least the answer for one roll fewer and at most five times it |
| P3 | from 9 rolls on, the answer is `12 t(n-3) + 15 t(n-4) + 32 t(n-5) + 18 t(n-6) + 24 t(n-7)` modulo `10^9 + 7`, `t` the arm's own answers |
| P4 | from 2 to 16 rolls the answer is even |
| P5 | each arm agrees with at least three of the other five |

P2's bounds hold because every sequence of `n - 1` rolls can be
extended by at most five rolls, any but the last, and by at least one:
a 1 or a 5 when one of them is not among the last two, any of 2, 3, 4
and 6 after a 1 and a 5. P3's recurrence is the least one the true
counts follow from 2 rolls on: Berlekamp-Massey over the exact counts
for 2 to 81 rolls, more than twice the 36 states of the matrix arm,
finds it, of order 7, so it holds for every count after; at 8 rolls it
does not yet hold. P4 holds because a 1 and a 5 are coprime with every
other roll, so swapping them pairs up the sequences, and the only
sequences the swap leaves alone, 2 3, 3 2, 3 4 and 4 3, then 2 3 4 and
4 3 2, and none longer, come in even numbers too.

The differential prints `360 counts of rolls: checksum 684225888, 6594
checks over 6 arms: 0 failures` under every lane in Verification; the
checksum of the literal answers was checked against a Python reading
that counts the sequences with `itertools.product` up to 7 rolls and by
recursion after. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: an opening pair of equal rolls allowed | P1 11, P3 1, P4 2, P5 359 |
| M4 | ★: a single roll counted once | P1 1, P2 1, P5 1 |
| M6 | ★: the total not reduced | P2 342, P3 342, P5 342 |
| M7 | memo: nothing left to roll counted as no way | P1 12, P5 360 |
| M8 | memo: the first roll held to the coprime test | P1 12, P4 1, P5 360 |
| M10 | memo: the memo keyed without the roll two back | P1 9, P3 352, P4 3, P5 357 |
| M13 | table: the pair before read the wrong way round | P1 9, P3 352, P5 357 |
| M14 | table: the last layer never filled | P1 10, P2 1, P3 1, P5 358 |
| M15 | table: the opening pairs not held to the coprime test | P1 11, P3 1, P5 359 |
| M17 | matrix: the square taken on even exponents | P1 10, P2 12, P3 352, P5 358 |
| M18 | matrix: one power too many | P1 11, P2 1, P5 359 |
| M19 | matrix: the second factor read transposed | P1 10, P3 352, P5 358 |
| M23 | iter: a repeated roll fitting | P1 11, P3 352, P4 2, P5 359 |
| M24 | iter: one roll too few | P1 10, P3 1, P5 358 |
| M26 | iter: the largest count, not the total | P1 11, P2 1, P3 339, P4 8, P5 359 |
| M28 | solution: the walk stopped at the first empty pair | P1 10, P2 3, P3 4, P4 1, P5 358 |
| M30 | solution: the modulus `10^9 + 9` | P3 342, P5 342 |

P5 kills all seventeen, P1 fifteen, P3 thirteen, P2 seven and P4 six.
P1 misses the two edits that differ only once a count passes `10^9 +
7`, past the 12 rolls the literal reading reaches: the total not
reduced and the wrong modulus, which P3, its recurrence taken modulo
`10^9 + 7`, and P2's bound catch. P3 misses the edits whose answers
still follow the true counts' recurrence: the answers shifted by a
roll, as one power too many is, and all zeros, as nothing left to roll
counted as no way gives, which P2's bounds and P4's evenness also let
through. The opening pairs wrong, the last layer never filled and one
roll too few each break P3 on a single count. P4, an even answer from 2 to 16 rolls, fails where an
edit breaks the swap of 1 and 5 that pairs the sequences: equal rolls
in the opening pair, the first roll held to the coprime test, the memo
or the repeat test losing the roll two back.

Of the thirty-one, fourteen were not kept. A roll equal to the one two
back allowed fails alike in the ★ (M2), memo (M9), table (M12) and
matrix (M20) arms, and so does the iter arm's roll equal to the last
allowed in its place (M22): none is kept, since one would stand for
all five. The ★ arm's roll sharing a factor with the last (M1) and the
template's roll equal to the last (M27) fail alike, and neither is
kept. The ★ arm's one roll too many (M5) and the template's opening
pairs counted twice (M31) fail as the matrix arm's one power too many
(M18); the table arm's total from the first layer (M16) and the
template's 1 never rolled after the opening pair (M29) as the matrix
arm's second factor transposed (M19); the matrix arm's opening pairs
not held to the coprime test (M21) as the table arm's (M15); and the
iter arm's pair before read the wrong way round (M25) as the table
arm's (M13). The memo arm's 6 never rolled (M11) fails apart from
every kept one, and was left out to keep three to an arm.

## Verification

Every arm prints the same output as `rolls.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run`, timed while other work ran on the machine,
the memo, table and template arms take about 5 s for their `10^4` rolls
and the 300 counts after, the ★ and iter arms, which build a fresh
table or `Vec` at every roll, 12 and 14 s, and the matrix arm, with its
36 by 36 products, 31 s. The differential takes 129 s there, every arm
answering for each count of rolls from 1 to 360 and the literal walk
building up to 742408 sequences, and 1.8 s under `karac
__mir-llvm-run`.

## Benchmarks

The bench makes 5 passes over every count of rolls from 9981 to 10000,
pass `p` folding each answer plus `p` into the checksum, with the ★ arm
in all five languages. Every implementation prints `5 passes over 20
counts of rolls up to 10^4: checksum 342000518`. Each keeps the two 6
by 6 tables of 64-bit counts on the stack, or in Python as lists, and
calls a recursive `gcd` for each test; nothing is allocated on the heap
but Python's tables.

BENCHTAB
