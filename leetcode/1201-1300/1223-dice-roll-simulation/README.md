# 1223. Dice Roll Simulation

A die simulator generates a random number from `1` to `6` for each roll.
You introduced a constraint to the generator such that it cannot roll the
number `i` more than `rollMax[i]` (**1-indexed**) consecutive times.

Given an array of integers `rollMax` and an integer `n`, return the
number of distinct sequences that can be obtained with exactly `n` rolls.
Since the answer may be too large, return it **modulo** `10^9 + 7`.

Two sequences are considered different if at least one element differs
from each other.

```
n = 2, rollMax = [1,1,2,2,2,3]  ->  34    36 sequences less "11" and "22"
n = 2, rollMax = [1,1,1,1,1,1]  ->  30
n = 3, rollMax = [1,1,1,2,2,3]  ->  181
```

**Constraints:** `1 <= n <= 5000`; `rollMax.length == 6`; `1 <=
rollMax[i] <= 15`.

The arms are `fn die_simulator(n: i64, roll_max: Vec[i64]) -> i64`. The
two Rust arms keep the method LeetCode gives Rust users, on `i32`, inside
`impl Solution`, and a one-line `die_simulator` calls it.

## Approaches

| file | mechanism |
|---|---|
| `dice_roll_simulation.kara` ★ | the sequences counted by their last face and how many times in a row it has come up; a roll of the same face lengthens the run while it stays within that face's limit, and any other face starts a run of one. O(n · 6 · 15 · 6) time, O(6 · 15) space |
| `dice_roll_simulation_subtract.kara` | every sequence of `i − 1` rolls can take face `j` next, except those whose last `roll_max[j] + 1` rolls would all be `j`: the sequences of `i − roll_max[j] − 1` rolls not ending in `j`, then `roll_max[j]` `j`'s, which are subtracted. O(36 n) |
| `dice_roll_simulation_memo.kara` | top-down: the ways to finish with `left` rolls to go after a run of `run` of face `last`, summed over the six faces that may come next, each answer kept in a `Map[(i64, i64, i64), i64]`. Recurses n deep |
| `dice_roll_simulation_blocks.kara` | a sequence as blocks, each a face rolled 1 to its limit times, no two neighbours the same face: the sequences of `i` rolls whose last block is face `j` are, over that block's length, the sequences of the rest not ending in `j`. O(n · 6 · 15) |
| `dice_roll_simulation_cube.kara` | a Rust solution as LeetCode's Rust users write it (`dp[i][face][run]` in a `vec![vec![vec![0i64; 16]; 6]; n + 1]`, every length kept, indexed through `as usize`), carried to Kāra by `karac fix` |
| `dice_roll_simulation_sums.kara` | another Rust solution (the subtraction over `vec![[0i64; 6]; n + 1]` and a `sum` vector, `usize` lengths), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 7 lines: LeetCode's three examples and `n = 1`
(`6`), a checksum of the answers for 300 random cases with `n` up to 60
(`361517142`), and three answers at the constraints' top, `n = 5000`:
with no face twice in a row (`82766332`, which is `6 · 5^4999` modulo
`10^9 + 7`), with every limit 15 (`549903798`), and with random limits
(`117825566`). `dice_roll_simulation.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, subtract, memo and blocks arms check clean as
written. The cube arm takes one round of 11 fixes (among them `Vec<i32>` to
`Vec[i32]`, `vec![..; n + 1]` to `Vec.filled(n + 1, ..)`, the program's
`usize`s to `i64`, and a cast the comparison no longer needs) and the
sums arm one round of 9, and both check clean.

## Gaps

None found.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every sequence of `n` rolls, as the `n` digits of a number in
base 6, kept when no face comes up more than its limit times in a row,
for `n` up to 5. 2000 cases, a third with `n` from 1 to 5, a third from
6 to 40 and a third from 41 to 120, each with six random limits from 1
to 15.

| | property |
|---|---|
| P1 | the statement read literally (`n` up to 5) |
| P2 | with every limit 15, `6^n` (`n` up to 15) |
| P3 | from 0 to `10^9 + 6` |
| P4 | the limits reversed give the same answer |
| P5 | a limit raised by one never lowers the count (`n` up to 11) |
| P6 | the ★ arm's answer |

P4 holds because the faces are interchangeable: which face carries which
limit does not change the count. P5 holds because raising a limit only
admits more sequences; past `n = 11`, `6^n` passes the modulus and the
counts wrap.

All 72,000 checks pass on every arm: `2000 cases: checksum 556485416,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python's counts for
the same cases give the same checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: no face twice in a row | P1 548, P2 732, P6 9405 |
| S2 | ★: the total left unreduced | P2 68, P3 1216, P6 6080 |
| U1 | subtract: the sequences ending in j taken off too | P1 225, P6 1553 |
| U2 | subtract: the limit one short | P1 478, P2 18, P6 1809 |
| M1 | memo: an answer remembered under a run of one | P1 217, P4 1550, P5 1, P6 1542 |
| M2 | memo: a finished sequence counted twice | P1 667, P2 851, P6 2000 |
| K1 | blocks: a block one roll short of its limit | P1 667, P2 851, P6 2000 |
| K2 | blocks: a block may follow one of its own face | P1 548, P2 732, P6 1881 |
| C1 | cube: the first roll counted as a run of none | P1 667, P2 851, P6 2000 |
| C2 | cube: a sixth face's run never grows | P1 91, P4 1375, P6 1357 |
| D1 | sums: the first face's limit for every face | P1 358, P4 1375, P6 1687 |
| D2 | sums: the total of a length left unreduced | P2 68, P3 1122, P6 1208 |

All twelve are caught. A mutation of the ★ arm fails P6 on the five
other arms. P1, the statement read literally, catches ten. The two that
leave a total unreduced (S2, D2) give the right count while it stays
below the modulus, which it does for every `n` up to 5, so P1 cannot see
them; P3 catches the totals past the modulus, and P2 the 68 cases with
every limit 15 and `n` large enough that `6^n` passes it. M2, K1 and C1
miscount from the first roll and fail every case. S1 (no face twice in a
row), K2 (a block after one of its own face) and U2 fail most cases, and
P2, with every limit 15, catches each of them. Three break the symmetry
between the faces: M1 remembers an answer under the wrong run, C2 never
lets the sixth face's run grow, and D1 gives every face the first face's
limit, so the limits reversed (P4) give them another count. P5, a
raised limit never lowering the count, catches M1 once.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm, count the sequences by their last face and run length, for 50
random sets of limits at n = 5000; checksum of the answers. Every
program prints `50 sets of limits at n = 5000: checksum 784694884`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.120 to 0.226 s | 0.137 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.115 to 0.238 s | 0.135 s |
| Rust (`rustc -O`) | 0.119 to 0.219 s | 0.136 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.133 to 0.245 s | 0.145 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.127 to 0.208 s | 0.151 s |
| C (`clang -O3`) | 0.099 to 0.172 s | 0.107 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.094 to 0.152 s | 0.101 s |
| Go | 0.238 to 0.349 s | 0.278 s |
| Python | 8.969 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 7% ahead of Rust with overflow checks on (0.135 s
against 0.145 s), and the two ranges overlap. C is about 21% ahead of
Kāra (0.107 s against 0.135 s); Go takes about 2.1x Kāra's time. Python
takes about 66x Kāra's time. No profile was taken.
