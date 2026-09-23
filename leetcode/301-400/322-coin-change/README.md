# 322. Coin Change

Given distinct positive coin denominations `coins`, each usable any number of
times, and a target `amount`, return the fewest coins that add up to `amount`,
or -1 if no combination does.

```
coins = [1, 2, 5]   amount = 11  ->  3     (5 + 5 + 1)
coins = [2]         amount = 3   ->  -1
coins = [1]         amount = 0   ->  0
```

The first idea is greedy: take the largest coin that fits, and repeat. That is
right for real currencies and wrong in general. With coins `[1, 3, 4]` and
amount 6, greedy takes `4 + 1 + 1`, three coins, when `3 + 3` is two. Without
a 1-coin it can also get stuck: with `[4, 6]` and amount 14 it takes 6 and 6,
has 2 left and nothing that fits, while `6 + 4 + 4` works.

What is always true is that the **last** coin of an optimal answer is some
coin `c`, and the coins before it are an optimal answer for `amount - c`:

```
best(0) = 0
best(a) = 1 + min over coins c <= a of best(a - c)     (unreachable if every a - c is)
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `coin_change.kara` ★ | fill `best(a)` for every amount from 0 up | `O(amount · coins)` time, `O(amount)` space |
| `coin_change_bfs.kara` | shortest path from the target down to 0, one coin per edge | `O(amount · coins)` worst, stops at the first 0 |
| `coin_change_memo.kara` | the same recurrence top down, `None` for unreachable | `O(amount · coins)`, recursion `amount / min(coins)` deep |
| `coin_change_brute.kara` | every vector of per-coin counts | `Π (amount / cᵢ + 1)` |
| `differential.kara` | four arms, fourteen properties | — |
| `bench/coin_change.kara` | 24 tables, each up to 1,000,000 amounts × 20 coins | — |

All four arms print the same fourteen fixed cases and three small random ones.
The ★ arm also prints three large random cases (amounts up to 100,000), which
only it and the Python mirror (`coin_change.py`) print.

## Four ways to count coins

**★ Bottom-up table.** `best` has one cell per amount from 0 to the target.
Cell `a` looks at `best[a - c]` for every coin `c <= a`, and all of those cells
are already filled. Unreachable amounts hold a sentinel, `amount + 1`, which is
one more than any real answer can be (the most coins an answer can use is
`amount`, all 1s). A sentinel is a number, so it takes part in the
arithmetic: `best[a - c] + 1` on an unreachable cell is `amount + 2`, which
loses every comparison and never gets stored. That is the reason the sentinel
has to be larger than every real answer, not just different from it.

**Breadth-first search.** Read the problem as a graph whose nodes are the
amounts, where every coin `c` is an edge from `a` to `a - c`. The answer is the
length of the shortest path from the target to 0, and every edge has the same
weight, so BFS finds it one level at a time. A remainder is enqueued the first
time it is seen, which is at its smallest level. This arm never asks "what is
best for every amount?". It only follows edges out of the target, so it stops
the moment 0 comes off the queue and never visits an amount the target cannot
reach.

**Memoised recursion.** This is the ★ recurrence asked from the top. It
recurses only into the amounts it needs and says "unreachable" with `None`
instead of a number. So a sentinel that is off by one, or that leaks into a
sum, cannot hide here the way it can in a table. The memo maps an amount to an
`Option[i64]`. An amount absent from the memo has not been solved yet. One
present with `None` has been solved and is unreachable, and caching that is
what stops the recursion from proving it again.

**Brute force.** An answer is a count for each denomination with
`Σ kᵢ · coins[i] == amount`. This arm enumerates every such count vector and
keeps the smallest `Σ kᵢ`. It has no recurrence over amounts, no queue and no
memo. It reads straight off the statement, which makes it the oracle, and it
only runs where the number of vectors stays small.

## Differential

`karac run differential.kara` has three tiers:

- Every nonempty subset of `1..=6` as the coin set, at every target from 0 to
  24. The brute force joins in wherever it visits at most 4,000 count vectors.
- Eight hand-picked cases: greedy traps, and sets with no 1-coin.
- 24 random cases with up to six coins in `1..=60` and targets up to 300.

```
cases 1607 brute-cases 1464 reachable 1389 samples 25712 hits 18747
DIFFERENTIAL OK
```

| # | property |
|---|---|
| P1 | the BFS arm agrees with the ★ arm |
| P2 | the memo arm agrees with the ★ arm |
| P3 | the brute force agrees with the ★ arm (where it is cheap) |
| P4 | the answer is -1 exactly when a plain reachability sieve says the target cannot be made |
| P5 | a **witness** exists: a multiset of exactly `answer` given coins that sums to the target |
| P6 | no random walk through the statement's space (draw coins that still fit until the target is hit) uses fewer coins (16 per case) |
| P7 | reversing or rotating the coin list changes nothing |
| P8 | one more denomination never makes the answer worse |
| P9 | `best(a) <= best(a - c) + 1` for every coin, with equality for some coin, at every reachable `a` up to min(target, 60) |
| P10 | `best(x + y) <= best(x) + best(y)` for random reachable `x`, `y` |
| P11 | scaling the coins and the target by `s` changes nothing, and target `+ 1` becomes unreachable |
| P12 | `⌈target / max coin⌉ <= answer <= target / min coin` |
| P13 | greedy, when it finishes, never uses fewer coins than the answer |
| P14 | adding the target itself as a coin makes the answer 1 |

P5 and P6 check the answer, not an arm. P5 says the answer can be **built**:
an arm that reports a count no combination achieves fails it, however
plausible the number. P6 checks the other half. It samples the statement's own
search space and asks whether anything it finds is cheaper, and it keeps
working at sizes the brute force cannot reach. "Buildable" and "not beaten"
together are the whole definition of the problem.

The sizes are set by the tree-walk interpreter, not by the JIT. The whole
harness takes 0.5 s under `karac run` and about 2 min 15 s under
`karac run --interp`.

## Mutation testing

Sixteen content-anchored edits to `differential.kara`, each run through the
full harness under `karac run`. A panic or hang would count as a kill
alongside `DIFFERENTIAL FAILED`.

| # | mutation | predicted | outcome | properties that fired |
|---|---|---|---|---|
| M1 | the ★ relax uses `<=` instead of `<` | *silent* | silent | — |
| M2 | the ★ sentinel is `amount`, not `amount + 1` | kill | **killed** | P1, P2, P3, P4, P6, P9, P11, P13, P14 |
| M3 | the ★ table stops one amount short | kill | **killed** | P1, P2, P3, P4, P6, P9, P13, P14 |
| M4 | the ★ relax never uses a coin equal to the amount | kill | **killed** | P1, P2, P3, P4, P6, P9, P13, P14 |
| M5 | the ★ arm returns the sentinel instead of -1 | kill | **killed** | P1, P2, P3, P4, P5, P9, P10, P11, P12 |
| M6 | the ★ arm skips the first coin | kill | **killed** | P1, P2, P3, P4, P5, P6, P7, P9, P13, P14 |
| M7 | the ★ table forgets `best[0] = 0` | kill | **killed** | P1, P2, P3, P4, P6, P13, P14 |
| M8 | the BFS counts a level per pop, not per layer | kill | **killed** | P1 |
| M9 | the BFS would enqueue 0 (`next > 0` → `next >= 0`) | *silent* | silent | — |
| M10 | the memo skips a coin equal to the amount | kill | **killed** | P2 |
| M11 | the memo keeps its best on `<` instead of `<=` | *silent* | silent | — |
| M12 | the brute force never lets one coin finish the remainder | kill | **killed** | P3 |
| M13 | the brute force takes a tie on `<=` | *silent* | silent | — |
| M14 | the random walk may draw a coin larger than what is left | kill | **killed** | P6 |
| M15 | greedy starts from the smallest coin | *silent* | silent | — |
| M16 | P12's upper bound becomes strict | kill | **killed** | P12 |

**11 killed, 5 silent, and every prediction held.** The five silent mutants
are equivalent, each for a reason that can be stated. M1, M11 and M13 change
only which of two equal counts is kept, and the count is all anyone reads. M9
can never fire, because `next == 0` has already returned one line above. M15
makes greedy worse, and P13 only checks that greedy is never *better*, which
a worse greedy satisfies.

M14 is the one that shows P6 is alive. A walk allowed to overshoot stops below
zero and reports how many coins it drew, which can be fewer than the answer.
Nothing else in the harness would notice, because every arm is untouched.
M16 does the same for P12: it breaks no arm, only the bound, and P12 alone
fires. M5 shows why a sentinel needs P5: an arm that returns `amount + 1` for
an unreachable target reports a count, and P5 is the property that asks for
the coins.

## Verification

All four arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build`. `scripts/surface-sweep.py --filter
322-coin --timeout 400` reports `5 programs · 5 clean · 0 DIVERGENCES`. (At the
default 60 s budget the differential's `--interp` run times out, which the sweep
reports as a timeout and not a divergence.) The ★ arm's full output,
including the three large cases, is byte-identical to `coin_change.py`.

The benchmark kernel is verified on JIT, AOT-sequential and AOT-auto-par, and
its sink matches all four language twins (`sink 437809599 reached 16`). It is
not run under `--interp`, because at this size the tree-walk backend would take
far too long. The kata's semantics are covered by the arms and the
differential, which do run on every backend.

## Benchmarks

`bench/coin_change.kara` and its four mirrors run 24 passes. Each pass draws
20 distinct coins up to 3000 and a target between 500,000 and 1,000,000 from an
LCG, then fills the ★ arm's table once: one pass over every amount, trying
every coin at each, which comes to about 360 million relaxations per run. Two
passes in three draw their coins on a grid of 2 or 3, and 8 of those 16 targets
are off the grid, so the -1 path is timed along with the rest. The answer and a
stride-9973 sample of each table are folded into a rolling hash, so every cell
stays observable.

The table is allocated once at full size, and each pass overwrites the prefix it
uses, writing each cell once from a running minimum. There is no refill loop for
an optimizer to erase, and the inner loop carries a dependence on `best[a - c]`,
so there is nothing to vectorise either. The C twin gains nothing from
`x86-64-v3`, which confirms it.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`, the file
> `scripts/consolidate-bench.sh` feeds into the top-level chart) is not
> measured yet, and `bench-lib.sh` refuses to write it from Linux. Absolute
> milliseconds are NOT comparable between hosts. Only the **within-file
> cross-language ratios** are.

30 runs each, 5 warmups, on a 4-core x86-64 Linux container, karac
`0.1.0-dev.9471+g03b67200d`, measured 2026-09-23. Python is its own lane at
3 runs.

| implementation | mean | vs fastest |
|---|---|---|
| c `clang -O3` | 243.8 ms ± 7.3 | 1.00× |
| c `-march=x86-64-v3` (matched-ISA) | 253.8 ms ± 15.4 | 1.04× |
| rust `-O` | 328.7 ms ± 5.9 | 1.35× |
| **kāra `karac build`** | **439.9 ms ± 16.6** | **1.80×** |
| rust `-O -C overflow-checks=on` (equal-safety) | 449.4 ms ± 7.8 | 1.84× |
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 453.1 ms ± 16.7 | 1.86× |
| go `go build` | 512.2 ms ± 5.3 | 2.10× |
| python 3 | 16292 ms ± 51 | 66.8× |

**Kāra is 1.80× behind `clang -O3` and 34% behind unchecked `rustc -O`. At
equal safety it is level with Rust**, 2% ahead, which is inside one standard
deviation. This kata is close to a pure measure of what overflow checking
costs. The inner loop is one subtraction for the index, one addition and one
compare, and nothing else, so the checks are a large share of the work. Rust
pays 37% for them here (328.7 → 449.4 ms), and Kāra, which checks the same
arithmetic by default, lands on the checked Rust build. Neither C nor Rust gains
from `x86-64-v3`.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 99.4 ms ± 4.5 | 15.7 KiB | 9.0 MiB |
| rust | 162.6 ms ± 2.7 | 3864.3 KiB | 9.6 MiB |
| kāra | 337.0 ms ± 14.4 | 341.6 KiB | 10.1 MiB |
| go | — | 2179.1 KiB | 9.5 MiB |
| python | — | — | 25.1 MiB |

Peak RSS is dominated by the 8 MB table, which every mirror allocates once.
`karac build` is 3.4× clang's cold compile and 2.1× rustc's. Its binary is 22×
clang's and 11× smaller than rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

**Five filed, all five fixed in kara `16b434fc5`.** None of them touched the
four arms as written. They came from probing other ways to write the same
problem, seventeen spellings in all, each run on all four surfaces. The ★ arm
never needed them, and nothing in this directory had to be changed to dodge
one.

- **[`B-2026-09-23-10`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) (high): slicing a `ref Vec` parameter crashed
  compiled code.** `fn total(v: ref Vec[i64])` with `let s = v[1..3]` inside
  printed `50` under `--interp`, panicked "slice range out of bounds" under the
  JIT, and segfaulted both AOT binaries. The borrowed parameter's slot holds a
  pointer to the Vec, and the slice lowering read that pointer's own bytes as
  the Vec's data and length. It is the only one of the five that built
  cleanly and then failed at run time.
- **[`B-2026-09-23-8`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl): a `for` over a `u8`, `u32`, `i8` or `i16` range
  did not build.** `for b in lo..m` with `u8` bounds type-checked and ran under
  `--interp`, and failed LLVM module verification on every compiled surface.
  The loop counter is always an `i64`, and the bounds arrived at their own
  width. Only 64-bit ranges had ever been compiled, which is why it hid.
- **[`B-2026-09-23-7`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl): `1..m` with `m: u8` was refused.** An unsuffixed
  literal bound was typed as `i64` before the two bounds were compared, so a
  range over any other integer type needed a suffix (`1u8..m`). `m + 1`
  already promoted the same literal. All four surfaces refused alike.
- **[`B-2026-09-23-9`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl): `for x in v[1..]` did not build.** A range slice
  bound to a name (`let s = v[1..]; for x in s`) compiled, and the same slice
  used directly as the loop's source, with or without `.iter()`, had no
  lowering.
- **[`B-2026-09-23-11`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) (low): one type error reported twice.**
  `s = s + y` with `s: u8` and `y: i64` printed the same `cannot mix integer
  types` error at the same column two times, because an assignment's
  right-hand side is checked twice.

The runs also print an error-return trace on stderr for a `?` whose `None` is
handled by the caller. That is by design (the trace is handling-agnostic, see
`B-2026-07-11-8`) and was not filed. No `KARAC_AUTO_PAR=0`-only pass, and
nothing contorted.
