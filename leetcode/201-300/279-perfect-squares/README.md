# 279. Perfect Squares

Given `n`, return the least number of perfect squares that sum to it.

```
12  ->  3     4 + 4 + 4
13  ->  2     4 + 9
43  ->  3     25 + 9 + 9
9999 -> 4
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `perfect_squares.kara` ★ | bottom-up DP over every value ≤ n | O(n√n) time, O(n) space |
| `perfect_squares_bfs.kara` | shortest path from n to 0 | O(n√n) worst case, usually far less |
| `perfect_squares_theory.kara` | Lagrange + Legendre, no search | **O(√n) time, O(1) space** |
| `differential.kara` | every n from 1 to 1200, four checks | — |

## Greedy is wrong, and 12 is where it breaks

Take the largest square that fits and 12 gives 9, leaving 3 = 1+1+1, for a total
of 4 against the true 3. It's the first counterexample and it's small — a solver
tested only on 13 (where greedy happens to be right) passes.

The DP is the definition read backwards: any optimal decomposition of `i` ends in
*some* square `j²`, and what remains must itself be optimally decomposed, or you
could improve it and contradict optimality.

```kara
least[i] = 1 + min over j*j <= i of least[i - j*j]
```

## The same answer as a shortest path

Nodes are `0..n`; from `k` there's an edge to `k - j²`. A path of length L *is* a
decomposition into L squares, so the answer is the shortest path from `n` to `0`,
and BFS's first arrival at 0 is it.

Both are searches, but they explore in opposite directions and stop for different
reasons: the DP computes every value up to `n` and reads off the last, while BFS
computes `n` alone and usually touches a small fraction of the range.

## Two theorems decide it completely

- **Lagrange (1770)** — every natural number is a sum of four squares. So the
  answer is *always* 1, 2, 3, or 4.
- **Legendre** — `n` needs four exactly when `n = 4^a(8b + 7)`. Strip factors of
  4, check mod 8.

Everything else falls out by elimination: 1 if `n` is square, 4 by Legendre, 2 if
some `i² + j² = n`, otherwise 3. **O(√n), no table, no search.**

This is the oracle, because the DP and the BFS are *not independent enough* —
they search in opposite directions but over the same edge relation `k → k - j²`,
so a misunderstanding of that relation is shared and invisible between them. The
closed form never builds the graph at all.

**And the check runs both ways.** The closed form is the only solver here not
obviously correct by inspection — it's correct by *citation*, resting on two
theorems this repo hasn't proved. So the searches validate the theory exactly as
much as the theory validates the searches. "It agrees with the textbook" and "the
textbook agrees with 1200 enumerated cases" are different claims, and the second
is the one this kata can make.

```
n from 1 to 1200
answers: 1 -> 34, 2 -> 354, 3 -> 614, 4 -> 198
Lagrange violations (an answer above 4) 0
Legendre numbers counted independently 198
...and answers of 4 198 — these must be equal
digest 947958474
DP vs BFS 0
DP vs closed form 0
```

Three of those lines are self-checking without reference to any solver: the four
counts sum to 1200, `1 → 34` is exactly the count of perfect squares ≤ 1200
(34² = 1156), and the 198 Legendre numbers are counted straight from the form
`4^a(8b+7)` rather than from anyone's answer.

## What the injected bugs did

| injection | DP vs BFS | DP vs theory | Lagrange | 4s = Legendre |
|---|---:|---:|---:|---|
| dp: bound `j*j < i` | 705 | 705 | **198** | **mismatch** |
| dp: start `j` at 0 | *traps* | | | |
| **bfs: same off-by-one** | 1200 | **0** | 0 | ok |
| both searches, same off-by-one | 1200 | 705 | 198 | mismatch |
| **theory: drop the Legendre case** | **0** | **198** | 0 | ok |
| theory: forget to strip factors of 4 | 0 | 48 | 0 | ok |

Four independent signals, and different bugs trip different subsets. The two
theory rows are caught *only* by the searches; the BFS row *only* by the pair.
The DP rows trip all four, including the two structural checks that never compare
solvers at all.

**One row didn't do what I designed it to.** "Both searches, same off-by-one" was
meant to show the shared-blind-spot failure that
[#276](../276-paint-fence/)/[#277](../277-find-the-celebrity/)/[#278](../278-alien-dictionary/)
each demonstrate — two solvers from one derivation agreeing on a wrong answer.
They don't agree: the identical *edit* produces different distortions in `j*j < i`
and `j*j < cur`, so the pair still catches it (1200). The row shows the oracle
working, not the pair failing, and it's the weaker claim.

## Kāra features exercised

- **`mut ref Vec[i64]`** — the DP table is grown once across the whole sweep
  rather than rebuilt per `n`, which is sound because the DP is prefix-closed.
- **Level-synchronous BFS** with two `Vec[i64]` frontiers swapped per level.
- **Integer-only `is_square`** by incremental search — no floating point, so no
  `sqrt` rounding to argue about.

## Running

```bash
karac run perfect_squares.kara
karac run perfect_squares_bfs.kara
karac run perfect_squares_theory.kara

diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in perfect_squares perfect_squares_bfs perfect_squares_theory differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```

The differential's range is set by the slowest surface: BFS rebuilds an O(n)
`seen` array per query, making the sweep O(limit²). At 1200 the interpreter takes
~2m40s against 0.02 s compiled; at 2500 it took 13 minutes, which is too slow to
re-verify casually.
