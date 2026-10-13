# 464. Can I Win

In the "100 game" two players take turns adding, to a running total,
any integer from `1` to `10`. The player who first causes the running
total to reach or exceed `100` wins. What if we change the game so that
players cannot re-use integers? Given two integers `maxChoosableInteger`
and `desiredTotal`, return `true` if the first player to move can force
a win, otherwise return `false`. Assume both players play optimally.

```
maxChoosableInteger = 10, desiredTotal = 11  ->  false
maxChoosableInteger = 10, desiredTotal = 0   ->  true
maxChoosableInteger = 10, desiredTotal = 1   ->  true
```

**Constraints:** `1 <= maxChoosableInteger <= 20`;
`0 <= desiredTotal <= 300`.

## Approaches

Every arm is `fn can_i_win(max_choosable: i64, desired_total: i64) ->
bool`. A total of 0 or less is a win before anyone moves, and a total
above `1 + 2 + ... + m` can never be reached, so it is a loss. Past
those two checks, a position is the set of numbers already taken: the
running total follows from it. The player to move wins if some free
number reaches what is left, or leaves a position the other player
loses.

| file | mechanism |
|---|---|
| `can_i_win.kara` ★ | search from the empty position, the taken numbers as a bitmask of `m` bits, each position's answer kept in a `Map[i64, bool]`. O(2^m × m) |
| `can_i_win_array.kara` | the same search, with the answers in a `Vec` of `2^m` entries indexed by the bitmask (0 unknown, 1 win, 2 loss). O(2^m × m) |
| `can_i_win_table.kara` | every position bottom up: positions only gain numbers, so work from the full bitmask down, each one's running total built from the mask without its lowest number. Always O(2^m × m) |
| `can_i_win_free.kara` | the same search, with a position spelled out as the sorted `Vec` of numbers still free and the memo a `Map[Vec[i64], bool]`; taking a number removes it from a copy. O(2^m × m²) |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 14 lines: the three LeetCode examples, ten
small games (among them totals equal to all the numbers, with an odd
and an even count of them, and one total past them), and for 300 random
games with `m` up to 12 and a total from 0 to a little past all the
numbers, how many the first player wins and a checksum. `can_i_win.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases.

| | property |
|---|---|
| P1 | on numbers up to 7, the answer is brute force's: every line of play, with no memo |
| P2 | a total of at most `m` is a win: take it at once |
| P3 | a total of `m + 1`, for `m` of at least 2, is a loss: whatever the first player takes, the second can take a number that reaches it |
| P4 | a total of all `m` numbers is a win exactly when `m` is odd (the game then runs to the last number), and anything more is a loss |
| P5 | on numbers up to 10, every arm agrees with the ★ arm |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a number must pass the total, not reach it | P1 243, P2 220, P3 1369, P5 993 |
| M2 | ★: the largest number is never taken | P1 428, P2 239, P3 1362, P4 506, P5 1494 |
| M3 | array: a remembered loss reads as a win | P1 93, P4 259, P5 173 |
| M4 | array: a move is good when the other player wins after it | P1 206, P3 1500, P4 255, P5 227 |
| M5 | table: a position's total counts its numbers, not their values | P1 200, P3 670, P5 313 |
| M6 | table: a move is good when the next position is a win | P1 206, P3 1500, P4 255, P5 227 |
| M7 | free: only reaching the total exactly wins | P1 200, P3 670, P5 313 |
| M8 | free: a taken number stays free | P1 228, P4 250, P5 314 |

P1, the only property with an independent answer, sees all eight. P5
compares with the ★ arm, so a ★ mutant shows up there as failures of
the other three arms. P2 sees only the ★ mutants: every other mutant still
finds the number that reaches a total of at most `m`, while M1 must
pass the total and M2 cannot take `m`. M4 and M6, the same mistake in
two arms, fail the same checks; so, by these counts, do M5 and M7.

## Verification

All four arms print the same output as `can_i_win.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends every arm and the differential match
under `karac run --interp`, LLJIT and `karac build` (also with
`KARAC_AUTO_PAR=1`).

## Benchmarks

The bench program uses the ★ arm on 10 games with the numbers 1 to 20
and a random total from 100 to 210, each searched from scratch with a
fresh memo. Every implementation prints `10 games of 1 to 20: the first
player wins 6, checksum 89737476`, the Kāra program under
`karac __mir-run` included (in 40 s).

The mirrors keep the ★ arm's structure, a recursive search with the
bitmask as the memo key. Rust uses its `HashMap`, Go its `map`, and
Python its `dict`; C has no map, so its mirror carries a small
open-addressing table with linear probing and a 64-bit mixing hash,
doubled when half full. Spot timings on a shared 4-core container,
three runs each (two for Python; `bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.70 to 0.82 s |
| Rust (`rustc -O`) | 0.82 to 0.83 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.89 to 0.92 s |
| Go | 1.06 to 1.10 s |
| Python | 6.3 to 6.7 s |
| Kāra (legacy `karac build`) | 0.98 to 1.16 s |
| Kāra (`karac build --mir`) | 1.46 to 1.76 s |

`bench.sh` builds with legacy `karac build`. The `--mir` row is timed
at kara `5f01de4c5c`, after the compiled backend's map was fixed
(B-2026-10-12-29, kara `8acdc0bdb5`). Under `karac __mir-llvm-run` the
program prints the same line in 7.4 s, compile included; that JITs the
MIR's IR without optimization passes, so it is not a benchmark.

## Compiler findings

No new findings.
