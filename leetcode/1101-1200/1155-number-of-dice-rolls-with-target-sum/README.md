# 1155. Number of Dice Rolls With Target Sum

You have `n` dice, and each die has `k` faces numbered from `1` to `k`.

Given three integers `n`, `k`, and `target`, return the number of
possible ways (out of the `k^n` total ways) to roll the dice so the sum
of the face-up numbers equals `target`. Since the answer may be too
large, return it **modulo** `10^9 + 7`.

```
n = 1, k = 6, target = 3     ->  1
n = 2, k = 6, target = 7     ->  6
n = 30, k = 30, target = 500 ->  222616187
```

**Constraints:** `1 <= n, k <= 30`; `1 <= target <= 1000`.

The arms are `fn num_rolls_to_target(n: i64, k: i64, target: i64) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `num_rolls_to_target.kara` ★ | dice added one at a time: `ways[s]` counts the rolls of the dice so far that sum to `s`, and each new die moves each count up by each of its faces, into a fresh row. O(n · target · k) |
| `num_rolls_to_target_prefix.kara` | the same rows, each read off a running sum of the one before: the rolls of one more die summing to `s` are those summing to `s - k` through `s - 1`, a window a prefix sum answers at once. O(n · target) |
| `num_rolls_to_target_memo.kara` | top down: the ways for `dice` dice to make `left` are those for one die fewer to make what is left after each face, remembered in a `Map[(i64, i64), i64]`; a `left` below `dice` or above `dice · k` is cut at once. O(n · target · k) |
| `num_rolls_to_target_count.kara` | counted by inclusion and exclusion: rolls summing to `target` are the ways to write `target - n` as `n` parts of 0 to `k - 1`; uncapped there are C(target - 1, n - 1), and for each `j` dice forced past the cap the count is taken away or put back: the sum over `j` of (-1)^j C(n, j) C(target - j·k - 1, n - 1), the binomials from Pascal's triangle modulo 10^9 + 7. O(target · n) |
| `num_rolls_to_target_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `i32` arguments cast to `usize`, a `const MOD: i64`, a table `vec![vec![0i64; t + 1]; n + 1]`, inclusive ranges and the faces bounded by `k.min(s)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five properties |

Every arm prints the same 15 lines: LeetCode's three examples; one die
of one face (target 1, 1 way; target 2, none); a target below the
fewest (`2, 5, 1`: 0); three dice of four faces at their most and one
past it (1, 0); thirty dice of one face; thirty of thirty at their
fewest, their most and past it (1, 1, 0); thirty of thirty at the middle
(`465`: 252370474); and ten of thirty at 1000, past their most (0).
Then 1000 random problems, 500 over the whole range and 500 with the
target between the fewest and the most the dice make, with how many have
a roll and a checksum (`1000 random problems: 611 with a roll, checksum
623518084`). `num_rolls_to_target.py` mirrors the ★ arm and its output
is byte-identical; an exact big-integer count, the dice's polynomial
raised to the `n`th power and reduced at the end, agrees on 300 more
random problems.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every one of the `k^n` rolls, the dice turned over like an
odometer, counted when its faces sum to `target`. It checks 1000
problems in four kinds: 500 of 1 to 4 dice of 1 to 6 faces, where the
literal count runs, the target anywhere from 1 to two past the most; 100
over the whole range, 1 to 30 dice of 1 to 30 faces and a target of 1
to 1000; 200 with the target within three of the fewest or the most the
dice make; and 200 at an edge: one die, dice of one face, or faces too
many for the cap to bind. 655 of the 1000 have a roll, and in 44 the
count is past 10^9 + 7, so the modulus takes effect. Every random choice
the properties make is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal count (the small kind) |
| P2 | the answer lies in 0 to 10^9 + 6, and is 0 for a target below the fewest or above the most the dice make |
| P3 | turning each face over (`f` to `k + 1 - f`) mirrors the target: `n · (k + 1) - target` gives the same answer |
| P4 | the fewest and the most the dice make are made one way each |
| P5 | when no die can show more than `k` anyway (`k >= target - n + 1`), one to five more faces change nothing |
| P6 | the answer is the sum, over the last die's faces, of the answers for one die fewer (where `n · k · target <= 20000`, 649 problems) |

All 18,450 checks pass on every arm: `1000 problems: checksum
174022150, 18450 checks over 5 arms: 0 failures`. A Python reading of
the same problems, with the literal count taken by `itertools.product`,
gives the same line.

## Mutation testing

Twenty-seven edits to the differential, five to seven to each arm, each
run under `karac __mir-run` and `karac __mir-llvm-run` with
`KARAC_HASH_SEED=1`, each failing the same way under both. Twenty-four
are caught; three are equivalent. In the ★ arm, `continue` for `break`
when a face passes the target changes nothing, since the faces only grow
from there. The memo arm without its early cut of a `left` below `dice`
or above `dice · k` gives the same answers, only later. And the prefix
arm's running sum left unreduced gives the same answers, since a
thousand sums below 10^9 + 7 stay far inside an `i64` and the difference
is reduced anyway. Sixteen are kept, no two failing the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no way to roll nothing | P1 297, P4 178 |
| M2 | ★: the top face never rolled | P1 189, P3 495, P4 113, P5 108, P6 123 |
| M3 | ★: a face of 0 | P1 186, P2 98, P3 666, P4 44, P5 232, P6 365 |
| M4 | ★: one die too few | P1 325, P2 68, P3 606, P4 169, P5 82, P6 44 |
| M5 | ★: the wrong modulus | P6 12 |
| M6 | prefix: a window of `k + 1` faces | P1 227, P2 138, P3 666, P4 47, P6 270 |
| M7 | prefix: a negative difference left negative | P2 9, P3 20, P6 1 |
| M8 | prefix: started from one, not nothing | P1 303, P2 97, P3 649, P4 156 |
| M9 | memo: the most the dice make refused | P1 189, P3 512, P4 113, P5 108 |
| M10 | memo: no dice make anything | P1 235, P3 586, P4 69 |
| M11 | memo: the key stored backwards | the interpreter's step limit; the compiled run times out |
| M12 | count: the triangle stops short of row `n` | index out of bounds |
| M13 | count: all `n` dice never forced past the cap | P1 66, P2 148, P6 130 |
| M14 | count: the triangle not reduced | integer overflow |
| M15 | count: the uncapped count left out | P1 426, P2 247, P3 666, P4 178, P6 281 |
| M16 | solution: one die of nothing rolls 1 | P1 296, P2 97, P3 649, P4 69 |

Of the twenty caught edits that do not stop the program, P1 catches
seventeen, P4 sixteen, P3 eleven, P6 ten, P2 eight and P5 five. An edit that sends
every answer to 0, or every answer to its negative modulo 10^9 + 7,
keeps the arm consistent with itself under every property but P4 and
P1: the mirror, the extra faces and the last-die sum all hold among
zeros, and among negatives. A wrong modulus shows only where a count is
past 10^9 + 7 and two ways of reaching it are compared, which only P6
does; it sees it on 12 checks. M11 never finishes: with the key stored
backwards the memo answers the wrong subproblems, and the cut no longer
bounds the recursion.

Of the eight caught and not kept, each fails exactly as a kept one: the
memo arm's last die never taking all that is left, the count arm's signs
swapped, and the solution arm's last die never taking all of `s`, last
die never added, and top face never rolled, as M1; the prefix arm's
window of `k - 1` faces, as M2; the solution arm's wrong modulus, as M5;
and the count arm's stars and bars off by one, as M12.

## Verification

Every arm prints the same output as `num_rolls_to_target.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The ★, prefix, memo and count arms were written as Kāra and needed no
fix. `karac fix` carried the solution arm in five rounds:
`Solution::num_rolls_to_target` to `Solution.num_rolls_to_target`; then
`struct Solution {}` declared; then the inner `vec![0i64; t + 1]`'s
suffix and the adapter's `as i64` dropped as redundant; then the inner
`vec![0; t + 1]` to `Vec.filled(t + 1, 0)`; then the outer `vec!` to
`Vec.filled(n + 1, ...)` with the `as usize` casts to `as i64`. The
kata found no gap.

## Benchmarks

`bench/` times the ★ arm against the same rolling counts in C, Rust, Go
and Python. 64 problems are drawn once: 1 to 30 dice of 1 to 30 faces,
the target between the fewest and the most the dice make, at most 1000.
Each of 250 passes answers all 64 in turn. Every program prints `250
passes over 64 problems: checksum 564139143`. Each allocates a fresh
row per die, as the ★ arm does.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `063457c984`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.470 to 0.921 s | 0.506 s |
| Rust (`rustc -O`) | 0.484 to 0.932 s | 0.542 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.547 to 0.778 s | 0.580 s |
| C (`clang -O3`) | 0.549 to 0.935 s | 0.592 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.587 to 0.797 s | 0.623 s |
| Kāra (`karac build`) | 0.609 to 1.063 s | 0.628 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.614 to 0.890 s | 0.652 s |
| Go | 0.803 to 0.948 s | 0.857 s |
| Python | 42.0 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; a plain `karac build` gives the same binary, byte
for byte, so the two Kāra rows are one program timed twice. Kāra ties
overflow-checked Rust, the equal-safety comparison (1.05x at the median,
within the runs' spread). Rust without the checks takes about 0.83x
Kāra's time, C about 0.78x to 0.91x and Go about 1.3x; Python takes
about 64x. The inner loop is one add and one remainder by 10^9 + 7 per
face, which every language pays; the checked builds add an overflow test
on the add and on `s + face`.
