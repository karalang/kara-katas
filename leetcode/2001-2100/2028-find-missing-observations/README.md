# 2028. Find Missing Observations

You have observations of `n + m` six-sided dice rolls, each from 1 to 6.
`n` of them are missing; you know the other `m`, in `rolls`, and the
average of all `n + m` rolls, `mean`, which is a whole number. Return `n`
values, each from 1 to 6, that give the `n + m` rolls the average `mean`.
If several answers exist, return any of them; if none does, return an
empty array.

```
rolls = [3,2,4,3],  mean = 4,  n = 2  ->  [6,6]
rolls = [1,5,6],    mean = 3,  n = 4  ->  [2,3,2,2]
rolls = [1,2,3,4],  mean = 6,  n = 4  ->  []
```

**Constraints:** `1 <= n, m <= 10^5`; `1 <= rolls[i], mean <= 6`.

The missing rolls must add up to `need = mean * (n + m) - sum(rolls)`,
which `n` dice can show exactly when `n <= need <= 6 n`. Any `n` faces
with that total are right, so the arms differ in which ones they pick.

## Approaches

| file | mechanism |
|---|---|
| `observe.kara` ★ | `need` spread evenly: every roll `need / n` and the first `need % n` one more, built by `(0..n).map(..).collect()`. O(m + n) |
| `observe_high.kara` | each roll as high as it can be while the rolls after it can still reach the rest at one pip each: sixes, one roll in between, then ones. O(m + n) |
| `observe_raise.kara` | every roll starts at 1, and one pip at a time goes to each roll in turn until they reach `need`, a roll at 6 skipped. O(m + 6 n) |
| `observe_lower.kara` | every roll starts at 6, and the surplus comes off from the last roll back, at most 5 from each; the sum by `fold`, the bounds by `(n..=6 * n).contains(need)` |
| `observe_faces.kara` | the even spread kept as a `SortedMap` from face to how many rolls show it, read back in face order |
| `observe_solution.kara` | LeetCode's Rust template (`iter().sum::<i32>()`, `||`, `vec![]`, `vec![q; n as usize]`, a unit struct, a `&Vec` wrapper with `|&x|`), carried by `karac fix` to a clean check |
| `differential.kara` | all six arms against the statement read literally, six properties |

Since any right rolls will do, each arm prints a verdict rather than its
rolls: `N rolls adding to S` when it returns `n` faces from 1 to 6 with
the needed total, `none` when it returns nothing and no rolls fit, and a
line starting `WRONG` otherwise. Every arm prints the same 10 lines: the
verdicts for LeetCode's three examples and five more; then the count
answered and a checksum of the verdicts for 3000 problems of 1 to 20 rolls
and 1 to 20 missing, and for 5 problems of 100000 rolls and 100000
missing. `observe.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: whether some `n` rolls fit is found from the set of totals `n`
dice can show, built one die at a time, never from the `n <= need <= 6 n`
bound the arms use. It checks 1500 problems of 1 to 8 rolls, a mean from 1
to 6, and 1 to 8 missing rolls. An answer is judged, not compared: right
when it is empty and no rolls fit, or when it holds `n` faces from 1 to 6
with the needed total. Every random choice of a problem is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is right by the statement read literally |
| P2 | the rolls reversed: still right, and empty exactly when before |
| P3 | the rolls with the answer added, asked for one more roll at the same mean, give exactly `[mean]` |
| P4 | every roll `r` turned to `7 - r` and the mean to `7 - mean`: still right, and empty exactly when before |
| P5 | every roll listed twice and twice as many missing: still right, and empty exactly when before |
| P6 | each arm's verdict agrees with at least three of the other five |

P2 holds because the sum ignores order. P3 holds because rolls averaging
`mean` stay at `mean` with one more roll exactly when it shows `mean`.
P4 holds because a face `r` maps to the face `7 - r` and a total `T` over
`k` dice to `7 k - T`. P5 holds because doubling the rolls and the missing
count doubles `need` and the bounds alike.

The differential prints `1500 problems: checksum 678566073, 54000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Sixteen are kept, two or
three to each arm. All thirty are killed, each fails the same way under
both backends, none by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one pip over six accepted | P1 25, P2 25, P4 55, P5 25, P6 25 |
| M2 | ★: all ones refused | P1 47, P2 47, P4 87, P5 47, P6 47 |
| M3 | ★: the missing rolls left out of the count | P1 1029, P2 1029, P3 685, P4 1340, P5 1029, P6 1029 |
| M4 | high: no roll above five | P1 136, P2 136, P3 121, P4 140, P5 136, P6 136 |
| M5 | high: the need never lowered | P1 629, P2 629, P3 629, P4 627, P5 669, P6 629 |
| M6 | high: the first roll left out of the total | P1 822, P2 841, P4 927, P5 822, P6 822 |
| M7 | raise: one pip short | P1 662, P2 662, P3 49, P4 669, P5 662, P6 662 |
| M8 | raise: two pips counted for one | P1 621, P2 621, P3 547, P4 635, P5 662, P6 621 |
| M9 | raise: all sixes refused | P1 40, P2 40, P4 87, P5 40, P6 40 |
| M10 | lower: a roll lowered to nothing | P1 487, P2 487, P4 485, P5 603, P6 487 |
| M11 | lower: one pip too few taken off | P1 669, P2 669, P3 38, P4 662, P5 669, P6 669 |
| M12 | faces: one more roll on the higher face | P1 475, P2 475, P3 279, P4 475, P5 475, P6 475 |
| M13 | faces: a single extra pip lost | P1 146, P2 146, P3 146, P4 126, P6 146 |
| M14 | faces: sevens accepted | P1 104, P2 104, P4 217, P5 104, P6 104 |
| M15 | Rust: too many pips accepted | P1 396, P2 396, P4 791, P5 396, P6 396 |
| M16 | Rust: a raised roll raised twice | P1 475, P2 475, P3 475, P4 475, P5 475, P6 475 |

P1, P2, P4 and P6 kill all sixteen, P5 fifteen and P3 nine. P2, P4 and
P5 judge the answer to a changed problem the way P1 judges the original,
so they see nearly every edit P1 sees; their counts differ from P1's where
the change moves a problem into or out of the edit's reach. P4 turns
every face `r` into `7 - r`, which swaps a problem near the top of the
bounds with one near the bottom; its counts run well above P1's for the
edits at one bound (M1, M2, M9, M13, M14). P5 doubles the rolls and the
missing count; it misses only the faces arm losing a single extra pip
(M12), which needs `need % n` to be exactly 1, and doubling makes it even.
P3 is judged only on a non-empty answer: it appends the answer and asks
for the one roll that brings everything to the mean, which is exactly
`mean` when the answer's total is right. An answer with the right total
and a face out of range passes it, so it misses the bound edits that
accept too much (M1, M13, M14) and the lower arm's roll lowered to nothing
(M10), and the edits that refuse too much answer nothing for it to judge
(M2, M9); it also misses the high arm with no roll above five (M6). It
sees the other nine, which get the total wrong.

The other fourteen fail as a kept one does, or with counts of their own.
The raise arm's last pip never given fails as M7, the lower arm's sixes
refused as M9. The ★ and Rust arms' one roll too many raised fail alike
(P1 709, P3 5), as do their one roll short with the lower arm's rolls
started at five (P1 709, P3 662); the raise arm's one roll fewer in the
mean and the Rust arm's known roll left out fail alike (P1 860, P4 1020).
With counts of their own: the high arm's rolls after it counted the wrong
way (P1 662, P5 709) and too few pips accepted (P1 395, P4 791), the lower
arm's total started at one (P1 734), and the faces arm's lower face kept
at every roll (P1 475, P3 262) and each face one roll short (P1 709, P3
636).

One draft was replaced: the raise arm raising a roll past six survived,
and is equivalent. The pips go to the rolls in turn, so every roll
reaches 6 before any would pass it, and the bound `need <= 6 n` stops the
raising first.

## Verification

Every arm prints the same output as `observe.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them. Under `karac __mir-run` the arms take 1.9 s to 3.3 s, most of it
the two problems of 100000 rolls, and the differential 9.6 s.

The faces arm's `for _ in 0..count`, over the `ref i64` counts that a
`SortedMap` walk yields, crashed the MIR interpreter of an older build
with "scalar constant of a non-scalar type"; kara cdb6382000 had already
fixed it on main, and the arm runs on every lane of a current build.

The five arms were written in Kāra and checked clean with no fix.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` alone, in three rounds (16, 3 and 1 edits). The
first carries the `Vec<..>` types, the `sum::<i32>()` turbofish, `||`, the
unit struct, the `&Vec` parameter, the `|&x|` pattern and the `::` path;
the second turns `vec![]` into `Vec.new()` and `vec![q; n as usize]` into
`Vec.filled(n as usize, q)`, and drops the wrapper's `ref`; the third turns
that `as usize` into `as i64`. The loop bound `0..r as usize` keeps its
`usize` (B-2026-11-08-49 is about `karac fix` rewriting `usize` only in
part); it checks, since a range of `usize` indexes a `Vec` as well.

## Benchmarks

The bench builds 20 lists of 100000 rolls once in all five languages, each
asked for 1 to 100000 missing rolls at a mean from 2 to 5, and runs the ★
arm on each for 50 rounds: 1000 calls. Every implementation prints
`1000 calls: 4617800 rolls, checksum 813418332`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 0.047 to 0.059 s | 0.049 s |
| C (`clang -O3`) | 0.047 to 0.061 s | 0.050 s |
| Kāra (`karac build`) | 0.069 to 0.097 s | 0.074 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.069 to 0.130 s | 0.079 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.069 to 0.098 s | 0.082 s |
| Go | 0.088 to 0.114 s | 0.100 s |
| Python | 1.5 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.065 s) is not above its real time (0.074 s).

The sequential Kāra program is 1.04x Rust under overflow checks and 1.65x
C.