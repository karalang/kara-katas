# 397. Integer Replacement

Given a positive integer `n`, you may replace it with `n / 2` if it is
even, and with `n + 1` or `n - 1` if it is odd. Return the fewest
replacements that turn `n` into 1.

```
n = 8  -> 3   (8 -> 4 -> 2 -> 1)
n = 7  -> 4   (7 -> 8 -> 4 -> 2 -> 1, or 7 -> 6 -> 3 -> 2 -> 1)
n = 4  -> 2
```

**Constraints:** `1 <= n <= 2^31 - 1`. The arms work in `i64`, so the
`n + 1` from `2^31 - 1` needs no special case.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `integer_replacement.kara` ★ | greedy on the last two bits: halve an even value; an odd value ending in `01` steps down and one ending in `11` steps up, since the carry clears a whole run of ones; 3 is the one exception (3 -> 2 -> 1) | O(log n) | O(1) |
| `integer_replacement_memo.kara` | both choices, memoized in a `Map[i64, i64]`: `f(n) = 1 + f(n / 2)` for even `n`, `2 + min(f((n - 1) / 2), f((n + 1) / 2))` for odd; every value it reaches is `n >> k` or one more | O(log n) | O(log n) |
| `integer_replacement_bfs.kara` | breadth-first search from `n` with a `VecDeque` of (value, distance) and a `Set` of values seen; each level holds a few values near `n >> k` | O(log n) levels | O(log n) |
| `integer_replacement_carry.kara` | dynamic programming over the bits: after `k` halvings the value is `(n >> k) + c` with carry `c` 0 or 1, so keep the cheapest cost of each carry and read `n`'s bits from the bottom | O(log n) | O(1) |
| `differential.kara` | the four arms on 3,000 random cases whose answers are known by construction, five properties | — | — |

Every arm prints the same 11 lines: the three LeetCode examples, seven
edge cases (1, 2, 3, 15, 65535, 2^30, 2^31 - 1), and for 3,000 random
values from 1 to 2^31 - 1 the sum of the answers and a checksum.
`integer_replacement.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms. For each of 3,000
random cases:

| | property |
|---|---|
| P1 | `2^m` (`m` from 0 to 30) takes `m` steps: every step is a forced halving |
| P2 | `2n` takes one step more than `n`: its first step is a forced halving |
| P3 | an odd `n` > 1 takes one step more than the cheaper of `n - 1` and `n + 1` |
| P4 | `2^m - 1` takes `m + 1` steps for `m` from 3 to 31: add 1, then halve `m` times |
| P5 | with `n` of `b` bits and `p` ones, the answer is at least `b - 1`, since a step shortens `n` by at most one bit, and at most `(b - 1) + (p - 1)`, the cost of always stepping down |

It prints `3000 cases, 60000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | greedy: no exception for 3 | P5 76 |
| M2 | greedy: the choice for odd values is reversed | P3 3000, P4 2907, P5 3000 |
| M3 | memo: an odd value only steps down | P3 759, P4 2907 |
| M4 | memo: an odd value's halving is not counted | P3 3000, P4 3000 |
| M5 | bfs: new values go to the front of the queue | P3 724, P5 1528 |
| M6 | bfs: an odd value only steps down | P3 759, P4 2907 |
| M7 | carry: stepping down costs one step | P3 3000, P4 3000 |
| M8 | carry: a value of 1 reached by a carry is not an answer | P4 2907 |

M1 is caught by P5 alone, and only where its upper bound is tight. P2
and P3 compare an arm with itself, and the mutant adds the same extra
step to every value whose path passes through 3, so `n` and its
neighbours stay consistent; P1 and P4 never pass through 3. M3 and M6
are one mistake in two arms and fail the same checks. M5 turns the
search depth-first, so it returns the first path it finds rather than
the shortest.

## Verification

All four arms print the same output as `integer_replacement.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The greedy, search and carry
arms also match under `karac run --interp`, LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`. The differential prints `60000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`.

The memo arm and the differential read the memo with
`if let Some(known) = memo.get(v) { return *known; }`, since the library
gives `Map.get` as `Option[ref V]`. The frozen legacy typechecker types
the item as a plain `i64` and refuses the `*`, so the legacy backends do
not run those two files. Not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 5,000,000 calls, each on a
random `n` from 1 to 2^31 - 1, and folds the answers into a sum and a
checksum. Every implementation prints `5000000 calls: total 188896827,
checksum 870225727`; a 20,000-call cut of the Kāra program under
`karac __mir-run` prints the same as the C program cut the same way.
Spot timings on a shared 4-core container (`bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.78 s |
| Rust (`rustc -O`) | 0.81 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.89 s |
| Kāra (legacy `karac build`) | 0.94 s |
| Go | 1.0 s |
| Python | 17 s |

The Kāra program also prints the same line under `karac __mir-llvm-run`
in 2.9 s, compile included. That JITs the MIR's IR without optimization
passes, so it is not a benchmark. The `karac build` time is the frozen
legacy backend; like `rustc -C overflow-checks=on`, it checks integer
overflow.

## Compiler findings

No new findings. The differential's first draft wrote `step(mut seed)`
inside a function whose `seed` is already a `mut ref`; `karac check`
refused it and `karac fix` dropped the marker, as the spec asks.
