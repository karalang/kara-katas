# 375. Guess Number Higher or Lower II

The judge picks a number from 1 to `n`. Each wrong guess `x` costs `x`
dollars, and the judge then says whether the pick is higher or lower.
Return the least amount of money that guarantees a win, whatever the
pick.

```
n = 10   -> 16
n = 1    -> 0
n = 2    -> 1
```

**Constraints:** `1 <= n <= 200`.

## Approaches

Let `cost[i][j]` be the least money that guarantees a win when the pick
is in `[i, j]`. One number costs nothing. Guessing `k` costs `k` when it
is wrong, and the judge then leaves whichever side is dearer, so
`cost[i][j] = min over k of k + max(cost[i][k - 1], cost[k + 1][j])`.
The arms compute the same recurrence in different ways.

| file | mechanism | time |
|---|---|---|
| `money_amount.kara` ★ | fill the table bottom up by interval length, shortest first, with a spare row and column so that the empty sides read 0 | O(n³) |
| `money_amount_memo.kara` | the recurrence top down, each range remembered in a table once solved | O(n³) |
| `money_amount_columns.kara` | bottom up by column: `j` rises and, within a column, `i` falls, so both sides of every guess are already filled | O(n³) |
| `money_amount_deque.kara` | the column order with the inner minimum in O(1) amortized: the left side's cost rises with `k` and the right side's falls, so above a split point `k0` the best guess is `k0 + 1`, and at or below it the cost `k + cost[k + 1][j]` does not depend on `i`; a monotone `VecDeque` keeps the least of those as `i` falls and the window `[i, k0]` slides left | O(n²) |
| `differential.kara` | the four arms against a minimax oracle for every `n` from 1 to 70, 1,400 checks, five properties | — |

A widely shared speed-up tries only guesses `k` in the upper half of
`[i, j]`. It is not a valid pruning, and it was left out for that reason:
filling a table for `n = 200` that way in Python gives the wrong cost
for 1,584 of its ranges, the shortest being `[9, 20]` (50 against the
true 49). None of the wrong ranges starts at 1, so it still returns the
right answer for every `n` up to 200, which is all that LeetCode's tests
ask for.

Every arm prints the same 7 lines: the three LeetCode examples, the
costs for `n` from 1 to 20, `n = 100` and `n = 200`, and a checksum over
every `n` from 1 to 60. `money_amount.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. The oracle is the
recurrence with no table at all for `n` up to 10, where it is cheap
enough to try every guess at every level, and the recurrence with a
`Map` of solved ranges above that.

| | property |
|---|---|
| P1 | each arm gives the oracle's cost |
| P2 | the cost never falls as `n` grows |
| P3 | `cost(n + 1) <= n + cost(n - 1)`, the price of guessing `n` first |
| P4 | the cost is at most what binary search pays in the worst case, guessing the lower middle |
| P5 | the same, guessing the upper middle |

It prints `n = 1 to 70, 1400 checks, 0 failures` under `karac __mir-run`
and `karac __mir-llvm-run`. The legacy backends cannot run it; see
Compiler findings.

## Mutation testing

Eight edits to the copies inside `differential.kara`, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | how |
|---|---|---|
| M1 | by length: the cheaper side decides | P1, 68 failures |
| M2 | by length: never guesses the low end of a range | P1 and P4, 3 failures |
| M3 | memo: a single number costs its own value | P1, P3, P4 and P5, 156 failures |
| M4 | by column: each column starts at `i = j` | P1, P3, P4 and P5, 152 failures |
| M5 | deque: drops the smaller values from the back instead of the larger | P1, P3, P4 and P5, 123 failures |
| M6 | deque: guesses above `k0` stay in the window | P1, 67 failures |
| M7 | deque: `k0 + 1` is never tried | P1 and P5, 28 failures |
| M8 | oracle: the cheaper side decides | P1, 32 failures |

M2 is killed by only three checks: leaving out the low end matters only
for the ranges where it is the one best guess, such as `[1, 2]`.

## Verification

All four arms print the same output as `money_amount.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`
(the same MIR compiled to LLVM). On the legacy backends only the memo
arm runs everywhere (`karac run --interp`, LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`); the by-length and by-column arms run
under `karac run --interp` only, and the deque arm under none of them.

## Benchmarks

The bench program runs the ★ arm for every `n` from 1 to 200, the
problem's largest, and folds the costs into a checksum. The C mirror
keeps the table in one flat allocation. The C, Rust, Go and Python
mirrors all print `checksum 596238495`, and so does
`karac __mir-llvm-run`. `bench.sh` cannot run yet, because it builds the
Kāra side with the legacy `karac build`, which refuses the ★ arm (see
Compiler findings). Timings are not taken yet; they need a quiet machine.

## Compiler findings

Both are in the legacy backends, which are frozen, so neither is filed;
the MIR interpreter and mir-llvm run every arm.

- **Legacy codegen refuses a method call on a doubly indexed element.**
  `karac build` and LLJIT stop at `cost[i][k - 1].max(cost[k + 1][j])`
  with `chained indexed receivers (a[i][j].max(...)) are deferred to
  v1.x; bind the inner element to a temporary first`. The arms keep the
  natural form.
- **The legacy backends do not know `VecDeque.back`.** The legacy
  interpreter stops with `method 'back' not found on type 'Vec' (no
  interpreter dispatch arm)`, and legacy codegen with `Vec/String method
  'back' is not yet supported in codegen`: both treat the `VecDeque` as a
  `Vec`.
