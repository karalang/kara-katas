# 365. Water and Jug Problem

You have two jugs holding `x` and `y` litres and an unlimited water supply.
You may fill a jug, empty a jug, or pour one jug into the other until the
first is empty or the second is full. Return whether you can end with
exactly `target` litres in the two jugs together.

```
x = 3, y = 5, target = 4   -> true    (the Die Hard puzzle)
x = 2, y = 6, target = 5   -> false
x = 1, y = 2, target = 3   -> true
```

**Constraints:** `1 <= x, y, target <= 1000`.

## Approaches

| file | mechanism | time |
|---|---|---|
| `water_jug.kara` ★ | Bézout's identity: the target is measurable exactly when it is at most `x + y` and a multiple of `gcd(x, y)` | O(log min(x, y)) |
| `water_jug_bfs.kara` | breadth-first search over the states `(a, b)` of both jugs, six moves each, with a flat visited table and a `VecDeque` queue | O(x · y) |
| `water_jug_set.kara` | the same six moves explored depth-first from a `Vec` stack, with the visited states in a `Set` of pairs | O(x · y) |
| `water_jug_total.kara` | a search over the total alone, in steps of `±x` and `±y` within `0..=x+y` | O(x + y) |
| `differential.kara` | the gcd, set and total arms against the breadth-first search, 72,000 checks, five properties | — |

The total arm is a model, not a simulation: one jug move does not always
change the total by `x` or `y` (filling a half-full jug raises it by less).
It is still exact, because both reach precisely the multiples of
`gcd(x, y)` from 0 to `x + y`.

Every arm prints the same 13 lines: the three LeetCode examples, nine edge
cases (both jugs full, more than both hold, one jug's capacity, equal jugs
at and away from their capacity, coprime jugs, a target that is and one
that is not a multiple of the gcd, a one-litre jug), and the count and a
checksum over 3,000 random triples. `water_jug.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. The breadth-first search
over both jugs is the oracle, because it simulates the moves as the problem
states them. The test draws 3,000 random triples with capacities in
`[1, 30]` and targets in `[0, 70]`, so that targets above `x + y` and the
target 0 both appear.

| | property |
|---|---|
| P1 | each arm gives the oracle's answer |
| P2 | swapping the jugs changes no answer |
| P3 | multiplying `x`, `y` and the target by 2 or 3 changes no answer |
| P4 | the target and `x + y - target` have the same answer |
| P5 | `x`, `y` and `x + y` are always measurable, and anything above `x + y` never is |

It prints `3000 cases, 72000 checks, 0 failures` under `karac __mir-run`
and `karac run --interp`.

## Mutation testing

Ten edits to the copies inside `differential.kara`, each run under
`karac __mir-run`. Nine are killed; the tenth is equivalent.

| # | mutation | how |
|---|---|---|
| M1 | gcd: no `x + y` bound | P1 and P5, 3473 failures |
| M2 | gcd: `target < x + y` | P1, P4 and P5, 3121 failures |
| M3 | gcd: divides by `min(x, y)`, not the gcd | P1, P4 and P5, 5889 failures |
| M4 | set: cannot empty a jug | P1 and P4, 869 failures |
| M5 | set: pouring ignores the destination's room | P1 and P4, 869 failures |
| M6 | set: tests one jug against the target, not both | P1, P4 and P5, 3939 failures |
| M7 | total: steps of `x` only | P1, P2, P4 and P5, 6596 failures |
| M8 | total: bounded by the larger jug, not both | P1, P4 and P5, 3861 failures |
| M9 | oracle: tests jug `a` against the target, not both | P1, 1416 failures |
| M10 | oracle: cannot pour from `b` into `a` | equivalent, 0 failures |

M10 survives because pouring in one direction is enough: filling `a`,
pouring it into `b` and emptying `b` whenever it is full already reaches
every multiple of the gcd, which is the classic one-directional solution.

## Verification

All four arms print the same output as `water_jug.py` under
`karac run --interp`, `karac __mir-run` (the v2 MIR interpreter), LLJIT,
`karac build` and `KARAC_AUTO_PAR=1 karac build`.

## Benchmarks

The bench program answers five million random triples, capacities up to a
million, with the ★ arm's gcd test. The Kāra build and the C, Rust, Go and
Python mirrors all print `4006994 measurable, checksum 638676715`.
`karac __mir-run` prints the same line, in 162 seconds against Python's 6.4.
Timings are not taken yet; they need a quiet machine.

## Compiler findings

- **MIR: an index panic prints nothing.** An earlier draft of mutation M8
  indexed one past the visited table. `karac __mir-run` exited 101 with an
  empty stderr, where core-semantics §10.2 asks for the message, location
  and trace. This is the panic-message gap the interpreter thread already
  has in hand; noted here, not filed again.
