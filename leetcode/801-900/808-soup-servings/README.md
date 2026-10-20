# 808. Soup Servings

There are two soups, A and B, with `n` ml of each. Each turn, one of
four pours is chosen, each with probability 1/4:

1. 100 ml of A and 0 ml of B,
2. 75 ml of A and 25 ml of B,
3. 50 ml of A and 50 ml of B,
4. 25 ml of A and 75 ml of B.

A pour that asks for more of a soup than is left pours what is left.
Serving stops as soon as either soup is empty. Return the probability
that A runs out first, plus half the probability that both run out at
the same turn. Answers within `1e-5` of the true value are accepted.

```
n = 50   ->  0.62500
n = 100  ->  0.71875
```

**Constraints:** `0 <= n <= 10^9`.

## Approaches

Every arm counts soup in servings of 25 ml, rounding up, since a part
serving ends the same way a whole one does: `n` ml is `m = ceil(n / 25)`
servings. Past 4800 ml the answer is within `1e-5` of 1, so every arm
returns 1 there, as LeetCode's solutions do.

| file | mechanism |
|---|---|
| `soup_servings.kara` ★ | a table built bottom up: `p[a][b]` is the answer with `a` servings of A and `b` of B left, 1 if only A is empty, 0 if only B is, 1/2 if both, and otherwise the mean of the four states one pour on. O(m²) |
| `soup_servings_memo.kara` | the same definition top down, each state worked out once and kept in a `Map[(i64, i64), f64]` keyed by the pair |
| `soup_servings_forward.kara` | push the chance forward pour by pour: every pour takes four servings in all, so after `t` pours a state still being served has `a + b = 2m - 4t` and the servings of A alone name it; each pour splits each state's chance four ways, and a pour that empties a soup adds its share to the answer instead of going on. O(m²) |
| `soup_servings_rolling.kara` | the table kept five rows at a time, since row `a` needs only rows `a - 1` to `a - 4`; a state with a soup empty is worked out on the spot. O(m²) time, O(m) room |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 12 lines: LeetCode's two examples; 0 ml, where
both soups are empty from the start; 1, 25 and 26 ml, which are one
serving like 50 ml; 4800 and 4801 ml on each side of the cutoff, and
10^9 ml; the answers for every 25 ml up to 300; the first size whose
answer is above 0.99999 (4475 ml, 0.9999902), found by trying each
serving count in turn; and the answers for 136 sizes from 0 to 5000 ml
added up. Answers print to five places, so arms that add the same
chances in another order still print alike. `soup_servings.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition by
following every sequence of pours from `n` ml of each soup, in ml, each
pour a quarter as likely as the turn before it, and adding up the chance
of the endings that count. Every chance is a quarter to a power, so for
up to 8 servings every sum is exact in floating point, and the arms must
match it exactly, not to a tolerance. Its 1,600 cases come in four kinds
of 400: up to 200 ml, against the definition; up to 4800 ml; 4400 to
6000 ml, around where the answer is taken as 1; and up to 10^9 ml.

| | property |
|---|---|
| P1 | the definition's answer exactly, up to 200 ml; past that, the ★ arm's to within `1e-12` |
| P2 | only the servings count matters: `n` ml, the whole servings `25 * ceil(n / 25)` ml, and one ml past the last whole serving below it give the same answer |
| P3 | one more serving of each soup never makes the answer smaller |
| P4 | the answer is from 1/2 to 1; it is 1 past 4800 ml, and above 0.99999 from 4475 ml |

It prints `1600 cases (400 walked), 4 arms, 25600 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: both soups empty at once counted as A's | P1 1915, P3 56 |
| M2 | ★: the second pour taking 50 ml of B, not 25 | P1 1784, P3 118, P4 116 |
| M3 | ★: the answer taken as 1 past 4000 ml | P1 498 |
| M4 | memo: the servings rounded down | P1 815, P2 858 |
| M5 | memo: both soups empty at once counted as B's | P1 905, P4 83 |
| M6 | memo: the second pour taking 25 ml of A and 75 of B | P1 848, P3 380, P4 792 |
| M7 | forward: both soups empty at once counted whole | P1 904, P3 56 |
| M8 | forward: a state with B empty kept going | P1 756, P3 386 |
| M9 | forward: three servings taken each turn | P1 802, P4 27 |
| M10 | rolling: four rows kept, not five | P1 740, P3 464, P4 162 |
| M11 | rolling: both soups empty at once counted as A's | P1 905, P3 56 |
| M12 | rolling: the last row of the table never filled | P1 904, P3 70, P4 252 |

P1 kills all twelve. P2 sees only the memo arm's servings rounded down
(M4), the one edit that tells apart sizes within one serving count. P3
misses four: the ★ arm's cutoff at 4000 ml (M3), whose answers of 1 past
it are still never smaller than the ones before; the rounding down (M4),
which shifts every answer by one serving and keeps their order; both
soups empty at once counted as B's (M5), which lowers every answer and
keeps their order too; and three servings taken each turn in the forward
arm (M9). P4 sees the edits that take an answer below 1/2 or above 1, or
keep one below 0.99999 past 4475 ml: the second pour changed (M2, M6),
both soups empty counted as B's (M5), three servings a turn (M9), four
rows kept for five (M10) and the last row never filled (M12). A first
M6, the memo keyed by the pair turned round, ran past the 40-minute
limit rather than failing a property: the memo then never finds a state
it kept, and the recursion is exponential. It was replaced by the edit
in the table.

## Verification

Every arm prints the same output as `soup_servings.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`393f6f8862`, which is its last compiler change. The runtime archives
were built after the last runtime change, `1a04b0f88d`.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`), the legacy JIT
(`karac run`), `karac build` and an auto-par build print the same output
for all four arms, and all but the legacy interpreter for the
differential, which ran past its 50-minute limit. The legacy build warns
that `rows` is used after a move in the rolling arm and the
differential, legacy taking a bare parameter as owned rather than
borrowed, and prints the right output all the same. Legacy is frozen, so
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. Each of 30,000
rounds works out the answer for a size from 3750 to 4800 ml, 150 to 192
servings, the largest the table is built for, building its table afresh.
Every implementation prints `30000 rounds of 3750 to 4800 ml: sum
29999.451677, 9991 above 0.99999`, the Kāra program under `karac
__mir-run` included, in 5,916 s with `KARAC_MIR_MAX_STEPS` raised past
its default of 40 billion steps.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 2.31 to 2.57 s |
| Rust (`rustc -O`) | 3.52 to 4.00 s |
| Rust (`rustc -O -C overflow-checks=on`) | 3.53 to 4.05 s |
| Go | 10.56 to 11.89 s |
| Python | 720.13 to 734.09 s |
| Kāra (`karac build --mir`) | 2.07 to 2.35 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 44.7 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 2.23 s,
against C's 2.41, Rust's 3.74 (3.80 under overflow checks) and Go's
11.27. C and Rust are slower than their instruction counts suggest
because each round frees its whole table, and glibc's `free` hands the
top of the heap back to the kernel and the next round asks for it again:
the C program makes 67,853 `brk` calls and spends about 1.2 s of its
time in the kernel, the Rust program 99,279 calls and about the same
time, and the Kāra program makes no `brk` call and spends none. Under
valgrind's cachegrind v2 runs 34.2 billion instructions and 6.68 billion
branches, against Rust's 43.3 billion and 7.60 billion and C's 17.9
billion and 1.34 billion. The legacy build ran 2.24 to 2.54 s, a median
of 2.33 s in the interleaved runs, with 35.3 billion instructions and
6.70 billion branches, so v2 takes 0.96 times legacy. The comparison
with C and Rust waits until after M4.

## Compiler findings

`karac check` first refused the memo arm and the differential: the
memo's recursive calls passed `memo` with no `mut` mark. Since kara
`dfe519983b` (B-2026-10-14-25) every argument to a `mut ref` parameter
is marked, a `mut ref` binding's included, and `karac fix` added the
four marks in each file. `karac __mir-run` ran both before the marks, as
it does not apply that check. Nothing new in v2.
