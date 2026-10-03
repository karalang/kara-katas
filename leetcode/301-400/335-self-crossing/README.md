# 335. Self Crossing

Starting at the origin, move `distance[0]` north, `distance[1]` west,
`distance[2]` south, `distance[3]` east, and so on, turning
counter-clockwise after every move. Return whether the path crosses or
touches itself.

```
[2, 1, 1, 2]  ->  true
[1, 2, 3, 4]  ->  false
[1, 1, 1, 2]  ->  true    (the fourth move ends on the start)
```

## Approaches

A new segment can only meet the segment three, four or five moves back
before it would have met a later one. Two arms test those three cases as
inequalities, one tests them geometrically, and one follows the spiral's
shape instead.

| file | mechanism | cost |
|---|---|---|
| `self_crossing.kara` ★ | the three local cases as inequalities on `d[i]` and the five moves before it | `O(n)` time, `O(1)` space |
| `self_crossing_stream.kara` | the same three cases over a `for x in d` stream, with the previous five moves in shift registers and a count of how many are real | `O(n)` time, `O(1)` space |
| `self_crossing_window.kara` | the path as `Seg` structs with end points. Two axis-aligned segments meet exactly when their x ranges and y ranges both overlap, ends included, and each new segment is checked against the three segments 3, 4 and 5 moves back | `O(n)` time and space |
| `self_crossing_phases.kara` | an outward spiral until the first move that is not longer than the one two before it, then an inward spiral that must keep shrinking. The turning move can shorten the move before it, which this arm does on a copy | `O(n)` time and space |
| `differential.kara` | the four arms, a brute-force oracle and eight properties on 23,845 paths | — |
| `bench/self_crossing.kara` | 100 solves of a 1,000,000-move spiral, by the ★ arm | — |

The three cases, for move `i`:

- **3 back:** move `i` reaches as far as move `i - 2` while move `i - 1` is no
  longer than move `i - 3`.
- **4 back:** move `i - 1` is exactly as long as move `i - 3`, and moves `i`
  and `i - 4` together cover move `i - 2`.
- **5 back:** the spiral was shrinking (`i - 1` no longer than `i - 3`, and
  `i - 2` at least as long as `i - 4`), and move `i` comes back across move
  `i - 5` from the inside.

Every arm prints the same 24 lines: the three examples, twelve edge cases
(empty, one move, three moves, a touch four back, a near miss, a crossing
five back, an inward turn that misses, strictly growing and strictly shrinking
spirals, two late crossings, and four moves near 10^9), eight random paths of
4 to 18 moves, and a 100,000-move outward spiral that is turned inward with
a move of 1 and then crossed with one long move. The four arms' output is
byte-identical, and `self_crossing.py` mirrors the ★ arm.

## Differential

`differential.kara` checks every path of 0 to 7 moves of length 1 to 4
(21,845 paths) against a brute-force oracle. The oracle walks the path one
unit at a time and reports the first time it steps on a point it has already
visited, including the start. Every move has length at least 1 and every
turn is a right angle, so two segments can only meet at a lattice point, and
stepping on one twice is exactly the path crossing or touching itself. It
then runs the same checks on 2,000 random paths of 0 to 40 moves, with move
lengths up to 2, 5, 20 and 1,000. Two in five of the random paths are an
outward spiral that turns inward at a random move and then shrinks, which is
where the 4-back and 5-back cases live. Small lengths cross almost every
time, so those spirals carry most of the `false` answers.

| | property |
|---|---|
| P1 | the four arms agree |
| P2 | the answer equals the oracle (exhaustive and random) |
| P3 | the reversed path has the same answer. Walked backwards, the path turns clockwise, and its mirror image turns counter-clockwise again over the same shape |
| P4 | multiplying every move by 3 keeps the answer |
| P5 | a path that crosses still crosses with one more move |
| P6 | the shortest prefix that crosses ends at the move where the oracle first steps on an old point |
| P7 | adding `2000 · i` to move `i` gives an outward spiral, which never crosses |
| P8 | moves of `200 - 2i`, less one where move `i` was odd, give an inward spiral from the first move, which never crosses either |

`21845 exhaustive arrays (20660 crossing), 2000 random arrays (1492
crossing), 0 failures`, on every surface.

## Mutation testing

Fourteen edits to the copies inside `differential.kara`, each built and run.

| # | mutation | outcome | how |
|---|---|---|---|
| M1 | ★: 3 back needs move `i` strictly longer than move `i - 2` | **killed** | P1, P2, P3, P4, P6 |
| M2 | ★: 3 back needs move `i - 1` strictly shorter than move `i - 3` | **killed** | P1, P2, P3, P4, P6 |
| M3 | ★: drop the 4-back case | **killed** | P1, P2, P3, P4, P6 |
| M4 | ★: 4 back needs strict cover | **killed** | P1, P2, P3, P4, P6 |
| M5 | ★: drop the 5-back case | **killed** | P1, P2, P3, P4, P6 |
| M6 | ★: 5 back without "move `i - 2` at least as long as move `i - 4`" | **killed** | P1, P2, P3, P4, P5, P8 |
| M7 | ★: 5 back without "move `i - 1` no longer than move `i - 3`" | **killed** | P1, P2, P3, P4, P5, P7 |
| M8 | phases: never shorten the move before the turn | **killed** | P1, P3, P4, P5, P6 |
| M9 | phases: no shortening when the turn is move 3 | **killed** | P1, P3, P4, P5, P6 |
| M10 | phases: shorten only when the turn strictly passes | **killed** | P1, P3, P4, P5, P6 |
| M11 | window: check only 3 and 4 back | **killed** | P1, P3, P4, P5, P6 |
| M12 | window: touching ends do not count | **killed** | P1, P3, P4, P5, P6 |
| M13 | stream: test 5 back once four moves are real | silent (equivalent) | — |
| M14 | oracle: the start is not a visited point | **killed** | P2, P6 |

M13 is equivalent. With only four real moves the fifth register is 0, so the
5-back test reduces to "move `i - 1` as long as move `i - 3`, and moves `i`
and `i - 4` cover move `i - 2`", which is the 4-back test that has already
returned. M7 turns a growing spiral into a false crossing, which P7 sees by
itself. P3 and P4 catch most of what P1 catches because each one compares
every arm against the ★ arm's answer on the original path. M14 is the touch
at the start in `[1, 1, 1, 2]`: only the oracle can get it wrong, so only
P2 and P6 see it.

## Verification

All four arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build`, and all five programs are
valgrind-clean at `-O0` with `KARAC_AUTO_PAR=0` and `KARAC_BUF_CACHE=0`
(`All heap blocks were freed`, no errors). The differential keeps the
oracle's visited points in a `Set`, so it hashes. It is clean without pinning
`KARAC_HASH_SEED` because the runtime it was linked with carries the fix for
B-2026-10-03-11, the hash seed's leaked block that kata 331 found. The four
arms' output is byte-identical to `self_crossing.py`.

## Benchmarks

`bench/self_crossing.kara` and its four mirrors time the ★ arm as written.
One path of 1,000,000 moves is built once as an outward spiral, each move one
to three longer than the move two before it, so it never crosses. Each of
100 punches picks a random move. Half of the punches shorten it to 1, which
turns the spiral inward so that the next move crosses, and the other half
leave the path alone, so that solve scans all of it. Then the move is put
back. The sink is a rolling hash of each answer and position.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each (Python: 3), on a 4-core x86-64 Linux container, karac built
from `main` at `b453e71f0` with this thread's unpushed hash-seed fixes (they
change only the runtime's hash seed, which this kernel never uses), measured
2026-10-03. Python is its own lane.

| implementation | mean | vs fastest |
|---|---|---|
| rust `-O` | 74.0 ms ± 4.3 | 1.00× |
| c `clang -O3` | 100.3 ms ± 3.7 | 1.36× |
| rust `-O -C overflow-checks=on` (equal-safety) | 100.8 ms ± 4.6 | 1.36× |
| rust `-C target-cpu=x86-64-v3` (matched) | 102.4 ms ± 6.8 | 1.38× |
| c `-march=x86-64-v3` (matched-ISA) | 107.0 ms ± 6.8 | 1.45× |
| **kāra `karac build`** | **124.1 ms ± 7.2** | **1.68×** |
| go `go build` | 128.6 ms ± 10.7 | 1.74× |
| python 3 | 14320 ms ± 255 | 194× |

**Kāra is 23% behind equal-safety Rust and C here.** The build phase alone
is a tie (6.8 ms against 6.3 ms for Rust with 0 punches), so the gap is all
in the scan. The two hot loops are close to identical: no bounds checks, the
same four loads into rotating registers, the same three overflow branches.
Kāra's loop also recomputes the function's answer from the loop counter on
every iteration (`lea; cmp; setb`), where Rust sets it once on each exit
path. That this is the whole gap is inferred from the disassembly, not
measured. Recompiling karac's own unoptimised IR with clang gives the same
time, so it comes from the shape of the IR rather than from karac's choice
of optimisation passes. Filed as B-2026-10-03-20. Plain `rustc -O`, which
skips overflow checks, is fastest by a wide margin, which is why the
equal-safety row is the comparison that counts.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 85.2 ms ± 5.3 | 15.7 KiB | 9.0 MiB |
| rust | 124.8 ms ± 5.2 | 3863.5 KiB | 9.7 MiB |
| kāra | 322.3 ms ± 8.3 | 354.0 KiB | 10.6 MiB |
| go | — | 2162.0 KiB | 9.7 MiB |
| python | — | — | 46.1 MiB |

`karac build` is 3.8× clang's cold compile and 2.6× rustc's. Kāra's binary is
22× clang's and 11× smaller than rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

The benchmark kernel's sink matches all four language twins and Python
(`sink 1031868521`).

## Compiler findings

- **B-2026-10-03-20 (perf, low, open): a scan loop with several early
  returns is about 23% slower compiled than in Rust or C with overflow
  checks.** Once the function is inlined into the benchmark, the optimiser
  merges its `return true` and `return false` exits into one flag that it
  recomputes on every iteration. Details are under Benchmarks.

Nothing else. Every arm was byte-identical on every surface and
valgrind-clean from the first run. `karac check` flagged eight `mut`
markers on `failures` in the differential, where the argument was already a
`mut ref` parameter, and `karac fix` removed them. Both are correct
diagnostics, and they say little about the diagnostics overall: the author
already knows the language, which is why authoring like this never counts
toward the machine-fix rate.
