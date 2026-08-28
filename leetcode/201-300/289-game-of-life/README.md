# 289. Game of Life

One step of Conway's rules on an `m x n` board of `0` (dead) and `1` (live):

```
live with < 2 live neighbours  ->  dies       (underpopulation)
live with 2 or 3               ->  lives
live with > 3                  ->  dies       (overpopulation)
dead with exactly 3            ->  becomes live (reproduction)
```

```
. # . .            . . . .
. . # .     ->     # . # .
# # # .            . # # .
. . . .            . # . .
```

**Every cell updates simultaneously**, and that one word is the whole problem.
The rules read each cell's neighbourhood in the *old* generation, so an in-place
loop that writes `(0,0)` before reading `(0,1)` has already corrupted the input
for its own next read.

## Approaches

| file | mechanism | extra memory |
|---|---|---|
| `game_of_life.kara` ★ | two generations packed per cell — bit 0 old, bit 1 new | O(1) |
| `game_of_life_copy.kara` | second board; read one, write the other | O(mn) |
| `game_of_life_infinite.kara` | `Set` of live cells only, no rectangle at all | O(live) |
| `differential.kara` | 1800 boards across three densities, three arms, plus oscillator invariants | — |
| `bench/gameoflife.kara` | 256×256 at 35%, 60 generations | benchmark lane |

## Stop thinking of a cell as a bit

The problem says the board holds `0` and `1`. That uses one bit of an `i64` and
leaves 62 idle, so each cell can carry **both** generations at once:

```
bit 0   the old state — never overwritten during the sweep
bit 1   the new state — written during the sweep, read only after
```

A neighbour count reads `v & 1`, so it always sees the old generation no matter
how many neighbours have already been visited. A second pass shifts bit 1 down.
Two passes, no second board, and simultaneity holds **by construction** rather
than by carefully ordering the writes.

The encoding survives because 1 and 2 are different numbers — writing the new
state into bit 1 cannot disturb bit 0. That is the same move as
[#73](../../1-100/73-set-matrix-zeroes/)'s first-row/first-column markers: find
storage the problem already owns but is not using.

`& 1` is the entire trick, and forgetting it is a *silent* wrong answer rather
than a crash — the differential's first mutation, and it fires on 2696 cases.

## What the infinite board changes

LeetCode's own follow-up asks what happens when the active area reaches the
border. A `Vec[Vec[i64]]` cannot answer: a glider walks away forever, so any
rectangle is eventually too small, and one that starts big is mostly zeros.

`game_of_life_infinite.kara` stores only live cells in a `Set[i64]`, and **the
loop inverts**. The array version sweeps every cell asking "how many live
neighbours?", costing O(mn) whether two cells are live or two million. With only
live cells stored there is nothing to sweep, so instead each *live* cell tells
its neighbours about itself, and counting those tallies answers the question for
every cell adjacent to anything live. A cell adjacent to nothing live cannot be
born — its absence from the tally *is* the answer. Cost is O(live), independent
of surrounding emptiness, and coordinates may go negative: the file runs a
blinker at `(-5,-5)` and a glider 40 steps past its starting box.

## The differential had to learn about light cones

Comparing a bounded arm against an unbounded one is not as simple as windowing
the set arm to the original rectangle. Doing that reports **570 mismatches out
of 1800** — and every one is at step 2 or later, none at step 1.

That is not a bug in any arm. The grid arms treat out-of-bounds as permanently
dead; the set arm lets a cell escape at step 1, and from outside it legitimately
feeds a birth back inside at step 2. The two models genuinely differ, and the
interior is common ground for exactly one generation.

Clipping error propagates inward one cell per generation, so the fix is to pad
the grid arm by `steps + 1` dead cells on every side. Inside the original window
the bounded and unbounded models must then agree exactly — and they do, on all
1800 boards. Four planted mutations (a dropped `& 1`, a wrong survival rule in
the copy arm, a survival rule ignoring liveness in the set arm, birth on 2
instead of 3) are each caught, in the arm they were planted in.

## Two compiler bugs, and why only one invariant caught them

Running the differential across all four surfaces found a divergence: the
interpreter reported `invariant failures 1` where JIT, AOT and auto-par-off all
reported `0`. Reduced, it is five lines:

```kara
let orig: Vec[Vec[i64]] = [[1, 1], [1, 1]];
let mut copy = orig.clone();
copy[0][0] = 99i64;
```

| surface | `orig[0][0]` | |
|---|---|---|
| **interp** | **99** | clone aliased the inner Vec |
| JIT / build / par-off | 1 | correct deep copy |

**`B-2026-08-20-32`** — the interpreter's `.clone()` on a nested `Vec[Vec[T]]`
shares the inner Vecs, so writing through the clone writes through the original.
A *flat* `Vec[i64]` clones correctly, which is what makes it a depth bug rather
than a broken `clone`. It is a silent wrong answer, on the surface CLAUDE.md
routes regex, Arrow-IPC and `gpu.dispatch` programs to automatically.

**The vacuous-pass lesson is the part worth keeping.** Four invariants are
checked here; only one caught it. A blinker must *differ* after one step — that
is the only assertion demanding a **difference**. "Block never changes",
"blinker returns after two steps" and "empty stays empty" all assert
**sameness**, and aliasing makes sameness trivially true. An oracle suite built
entirely from stability properties would have gone green on a bug that silently
merges two boards into one.

**`B-2026-08-20-33`** — reducing the repro also found that a three-level
`d[0][0][0] = v` is rejected by codegen with `Index assignment target must be a
variable`, while two levels compile fine. Filed at medium: the compiler refuses
rather than miscompiles, and two fixed siblings
(`B-2026-08-09-21`, `B-2026-08-10-5`) suggest a general place-expression store
path would subsume all three rather than adding a third special case.

## The trick costs you parallelism

Game of Life is a stencil, and a stencil is the textbook parallel workload —
every row's new state depends only on the old state, so rows are independent.
The ★ file's rows genuinely *are* independent, because pass 1 writes only bit 1
and reads only bit 0.

The compiler cannot know that. `board[r][c] = board[r][c] | 2` reads and writes
the same array, and no dependence analysis short of bit-level reasoning can
prove the read and write sets are disjoint. `karac query concurrency` declines
it, correctly.

The copy version has genuinely disjoint read and write sets, and the analyzer
does recognise its row build as a collect-tabulate — but reports
`fanned_out: false`, `cost_gate: n/a`, `reason: "lowered inline,
single-threaded"`. The tabulate lowering is sequential by construction, so
neither shape fans out here.

So **there is no par lane for this kata, and unlike
[#288](../288-unique-word-abbreviation/) that is not a bug.** It is the honest
price of the in-place trick: the aliasing that saves O(mn) memory is exactly
what makes the loop unanalyzable. A hand-written parallel version would be
correct; an automatic one cannot be justified without understanding what the
bits mean.

## Benchmarks
<!-- bench-staleness -->
> **Figures in this section are undated; the feed was last measured 2026-08-28.** Where the two disagree, [`bench/results.json`](bench/results.json) and the [charts](../../../BENCHMARKS.md) are current; the numbers below are kept because the analysis around them explains *why* the shape is what it is, and that reasoning outlives the milliseconds.

> **Host:** the tables below are a shared **x86-64 Linux cloud container**
> snapshot, kept as [`bench/results.container-x86.json`](bench/results.container-x86.json).
> The canonical Apple M5 Pro lane is [`bench/results.json`](bench/results.json) —
> that is the file `scripts/consolidate-bench.sh` feeds into the top-level chart,
> and it is current as of the date stamped above. Absolute milliseconds are NOT
> comparable between the two hosts; only the **within-file cross-language
> ratios** are.

See [BENCHMARKS.md](../../../BENCHMARKS.md) for methodology and caveats. Sink is
`pop 7497 hash 613858477` across Kāra, C, Rust and Go.
