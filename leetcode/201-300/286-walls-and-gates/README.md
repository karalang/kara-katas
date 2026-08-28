# 286. Walls and Gates

A grid of rooms. `-1` is a wall, `0` is a gate, `INF` is an empty room. Fill
every empty room with the distance to its **nearest** gate, moving only up, down,
left and right. A room no gate can reach stays `INF`.

```
INF  -1   0 INF          3  -1   0   1
INF INF INF  -1    ->    2   2   1  -1
INF  -1 INF  -1          1  -1   2  -1
  0  -1 INF INF          0  -1   3   4
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `walls_and_gates.kara` ★ | multi-source BFS — seed every gate, expand once | O(mn) |
| `walls_and_gates_enum.kara` | the same BFS with the grid as a sum type | O(mn) |
| `walls_and_gates_dfs.kara` | DFS flood from each gate, relaxing on arrival | O(mn) amortized |
| `walls_and_gates_brute.kara` | one BFS per room, outward to the nearest gate | O((mn)²) |
| `differential.kara` | 1296 grids, three wall/gate mixes, four solvers | — |
| `bench/wallsgates.kara` | 16 boards × 512² × 8 solves, seq and par lanes | benchmark lane |

## Turning the problem around

The phrase "distance to the nearest gate" describes a search **from each room**,
and taken literally that is `walls_and_gates_brute.kara` at O((mn)²). Inverting
it costs nothing:

```
seed the queue with EVERY gate at distance 0
pop a cell, and claim each untouched neighbour at distance+1
```

A room is first reached by whichever gate's wave arrives soonest, so the first
arrival **is** the answer and one sweep fills the whole grid — however many gates
there are.

The part worth stating carefully is why first-arrival wins with many sources.
Single-source BFS is layer-by-layer, so the argument is the familiar one. Seeding
all gates at 0 makes the queue a *merge* of every gate's wave, and the distances
in it are still non-decreasing — so a cell popped at distance `d` has no shorter
route from any gate. That property, not the specific gates, is what makes one
pass enough.

**`INF` doubles as the visited mark.** There is no `seen` array: a room still
holding `INF` has not been reached, and the instant it is reached it takes a
finite distance that is both its answer and its mark. That only works because
the first arrival is already final — the DFS variant, which relaxes, cannot use
the trick and needs a real comparison instead.

## The grid is a three-way choice, so one file says so

LeetCode packs three unrelated meanings into one `i64`: `-1` is "wall", `0` is
"gate", `2147483647` is "no answer yet". None of them is a distance, and every
read has to know which of the four readings applies.
`walls_and_gates_enum.kara` writes the type out:

```kara
enum Cell { Wall, Reached(i64), Room }
```

A gate is `Reached(0)` — not a special case, just the distance-0 member of the
variant a filled room lands in. `Room` is uninhabited by any number, so it cannot
collide with a real distance, and `2147483647` leaves the algorithm entirely
(it survives only at the I/O boundary, because the problem asks for it back).
The relax step's guard becomes a `match` arm that a wall cannot reach, rather
than an equality test that misses walls only because `-1 != 2147483647`.

**It is also a deliberate compiler probe.** Before this kata, no kata in the
corpus declared a payload-carrying enum at all — 285 katas, zero — while two
compiler fixes that week landed squarely on that surface
([`B-2026-08-18-48`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.md),
freeing a POD-struct boxed enum payload moved into a call, and `B-2026-08-18-39`,
transferring one out of a par branch). This file makes the construct routine:
built into a `Vec`, matched with bindings, passed and returned by value.
It found nothing — the surface is correct on all four execution surfaces — but
"zero katas exercise this" was not a state worth leaving.

## Relaxations: the property the answer hides

Every solver reports how many times it wrote a distance into a room, and the
harness checks that count against a bound rather than against the other solvers:

- BFS, the sum-type BFS and the per-room oracle each write a reachable room
  **exactly once**, so all three must equal the reachable-room count.
- The DFS **relaxes**, so it is only bounded below by that count.

Across the 1296 grids the BFS performs **6373** relaxations and the DFS
**25075** — 3.9× — for byte-identical output on every grid. That gap is the
whole reason the second property is measured: two correct algorithms doing
wildly different amounts of work is exactly the case an answer-only oracle
cannot see, and an implementation whose visited-marking is broken can produce
the right grid while doing a multiple of the work.

Kata 277 counted API calls and kata 283 counted stores for the same reason. This
is the first one where the counts of two *correct* solvers legitimately differ,
so the check had to become a bound rather than an equality.

## The guard in the DFS is not an optimization

```kara
if g[cell] == -1i64 { return; }
if g[cell] < d { return; }
```

The second line reads like a pruning step and is load-bearing for
**termination**: without it the flood walks back where it came from, one step
longer each time, forever. With it, every step either lowers a room's value or
stops, and a value can only be lowered finitely often.

Reversing it to `>` is the one injection in the table below that does not produce
a disagreement — it **hangs**. Two adjacent gates ping-pong, each overwriting the
other with a larger distance, and the harness never returns. That is a stronger
demonstration of what the guard does than any count.

## The differential

1296 grids: sizes 1×1 through 6×6, three wall/gate mixes (ordinary 25/12,
maze 45/5, gate-rich 10/30), 12 grids each. All four solvers run on every grid;
the per-room oracle is the reference.

`differential.py` generates the same grids from the same LCG and runs the same
four solvers. The two must agree line for line — and on the first run they did
**not**, in exactly one number: the digest. **Kāra's `%` truncates toward zero
(`-1 % 1000 == -1`), Python's floors (`999`)**, and the digest is the only
statistic that hashes a wall rather than a distance. The mirror carries an
explicit `trunc_mod` now, because Kāra is the artifact under test and Python is
the side that bends.

**659 of the 1296 grids contain a room no gate reaches**, 2731 such cells in
total. The maze shape exists to keep that number large; if it went to zero the
harness would be quietly weaker while still reporting green.

### Injections

| injected fault | bfs | enum | dfs | relax. violations | unreachable cells |
|---|---:|---:|---:|---:|---:|
| bfs: seed only the first gate | **492** | 0 | 0 | 307 | 2731 |
| bfs: left-edge guard dropped (`cell > 0`) | **206** | 0 | 0 | 46 | 2731 |
| enum: `distance_at` reports `0` for `Wall` | 0 | **908** | 0 | 565 | 2731 |
| dfs: guard reversed (`>`) | *does not terminate* | | | | |
| **oracle: won't step onto a gate** | **799** | **799** | **799** | **799** | **9104** |

The last row is the shape worth recognising: three identical counts *and* a
second independent counter moving (2731 → 9104). When every solver disagrees
with the oracle by the same amount, the oracle is what broke.

**Two injections did not inject, and are recorded rather than dropped:**

- *bfs: relax instead of first-arrival* (`g[n] > d` in place of `g[n] == inf()`)
  changes nothing. For a wall `-1 > d` is false, for a gate `0 > d` is false, and
  BFS distances are non-decreasing so a filled room is never improved. The two
  spellings are genuinely equivalent here.
- *oracle: search the grid it is filling* changes nothing either — and it
  disproved a comment this kata originally shipped. The claim was that filling
  in place would let a fresh distance be mistaken for a gate; that is false,
  because every distance written is ≥ 1 and a gate is 0. The snapshot stays,
  but the file now says why honestly: it makes the per-room independence true by
  construction rather than true by an accident of which sentinels the problem
  uses.

## Benchmarks
<!-- bench-staleness -->
> **Figures in this section are undated; the feed was last measured 2026-08-28.** Where the two disagree, [`bench/results.json`](bench/results.json) and the [charts](../../../BENCHMARKS.md) are current; the numbers below are kept because the analysis around them explains *why* the shape is what it is, and that reasoning outlives the milliseconds.
> Comparative claims below ("ahead of C", "leads Rust", ratios) were true of the snapshot and have **not** been re-verified against the current feed — treat them as historical, not as the standing result.

> **Host:** the tables below are a shared **x86-64 Linux cloud container**
> snapshot, kept as [`bench/results.container-x86.json`](bench/results.container-x86.json).
> The canonical Apple M5 Pro lane is [`bench/results.json`](bench/results.json) —
> that is the file `scripts/consolidate-bench.sh` feeds into the top-level chart,
> and it is current as of the date stamped above. Absolute milliseconds are NOT
> comparable between the two hosts; only the **within-file cross-language
> ratios** are.

Workload: 16 independent 512×512 boards, 20% walls and 1% gates, each solved
eight times over. **Build once, punch many** — generating a board and solving it
are both O(cells) with comparable constants, so a one-solve-per-board loop spent
40% of its time in the LCG (0.177 s of 0.445 s). Eight solves per generated
board drops that to 3.6%, so what is timed is the BFS.

Sink: summed finite distance plus the unreachable-cell count, both sums, so the
par lane may finish boards in any order and must print the same two numbers.
All five languages use a flat array with a head cursor rather than a deque, so
the lanes measure the same data structure.

### Sequential — 4-core x86 container, 30 runs

| implementation | mean | vs C |
|---|---|---|
| `clang -O3 -march=x86-64-v3` (matched ISA) | 641.8 ms ± 17.6 | 0.98× |
| `clang -O3` | 653.2 ms ± 17.5 | 1.00× |
| `rustc -O` | 715.5 ms ± 18.8 | 1.10× |
| **`karac build`, `KARAC_AUTO_PAR=0`** | **773.2 ms ± 16.0** | **1.18×** |
| `rustc -O -C overflow-checks + target-cpu=x86-64-v3` | 779.4 ms ± 15.0 | 1.19× |
| **`rustc -O -C overflow-checks=on`** (equal safety) | **795.0 ms ± 18.9** | **1.22×** |
| `go build` | 833.0 ms ± 36.3 | 1.28× |
| `python3` | 11.29 s ± 0.13 | 17.3× |

Kāra is **1.18× off C** and **tied with the equal-safety Rust twin**. The 3%
that separates them is not a result: BENCHMARKS.md's gate for this shared 4-core
host is ~1.15× (median relative σ 5.7%, p90 15.7%), so everything from `rustc -O`
down through Go is one undifferentiated band and only the C gap and the Python
gap are large enough to read.

### Parallel — the same workload, 4 cores

| implementation | mean | vs floor |
|---|---|---|
| `clang -O3` + pthreads (metal floor) | 157.0 ms ± 6.4 | 1.00× |
| **`karac build`, `#[par_order_free]`** | **226.9 ms ± 10.3** | **1.45×** |
| Go, goroutines + `WaitGroup` | 239.9 ms ± 11.5 | 1.53× |

**3.41× over its own sequential lane on 4 cores**, from one attribute on the
board loop. That speedup is a within-file ratio out of a single interleaved
`hyperfine` call, which is the one comparison this host measures reliably.

The 1.45× to the pthreads floor is real; the 6% to Go is **not** — it is inside
the same noise gate, so the honest statement is that Kāra's auto-par and
hand-written goroutines tie here, and that both sit meaningfully behind C.

The fan-out is over the outer loop because that is where the independence lives
— inside one board the wavefront is sequential and always will be.

That placement is the criterion this corpus has converged on, and it is about
**work per branch, not whether independence exists**: kata 285's queries were
independent too, but each was ~20 ns, so a par lane there would have measured
dispatch. Each board here is ~4 ms.

### A harness defect this kata caught

The par row's first run measured **773 ms — the sequential number**. The bench
harness `scripts/new-bench.sh` generates builds the kara binary with
`KARAC_AUTO_PAR=0`, which is right for a one-lane kata; a par lane added by hand
pointing at that same binary compiles the `#[par_order_free]` source with the
auto-parallelizer switched off. The env var is that pass's kill switch and the
attribute is an opt-in hint *to* the pass, not an explicit `par {}` block, so
what comes out is an ordinary sequential binary.

Worse than a wrong number, it is **intermittent**: the generated helper rebuilds
only when the source is newer than the output, so a binary left from an earlier
auto-par build survives and the run reports honest figures. Whether a bench
measures what it claims came down to file mtimes. (Checked: the published
numbers for katas 276, 277, 278 and 282 were unaffected — their recorded par and
seq figures differ by 1.7×, 3.8×, 3.9× and 4.6×, which a sequential binary
cannot do against itself.)

Fixed in all five two-lane benches, and `scripts/lint-par-lane.py` now gates it
in CI.

## Compiler findings

| id | severity | what |
|---|---|---|
| [`B-2026-08-19-2`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.md) | low | `karac run --interp prog \| head` dumps a Rust panic + backtrace on SIGPIPE; the JIT and the AOT binary exit silently |

Found by piping a solver's output through `head -2`. It is a genuine run-vs-build
divergence in observable behaviour, invisible to this corpus's A/B rule only
because that rule compares stdout.

## Running

```bash
karac run walls_and_gates.kara          # or _enum / _dfs / _brute
karac run differential.kara             # 1296 grids, four solvers
python3 differential.py                 # must match line for line
bash bench/bench.sh                     # seq + par lanes
```
