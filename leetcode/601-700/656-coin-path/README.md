# 656. Coin Path

Given a row of coins, numbered from 1, and a longest jump `max_jump`,
start on coin 1 and reach the last coin, each step jumping ahead 1 to
`max_jump` places, never landing on a coin marked -1. Every coin landed
on, the first and last included, is paid for. Return the indices of the
cheapest such path; if several are cheapest, the lexicographically
smallest (at the first place two differ, the smaller index; if one runs
out first, the shorter). If the last coin cannot be reached, return an
empty list.

```
coins = [1,2,4,-1,2], max_jump = 2  ->  [1,3,5]
coins = [1,2,4,-1,2], max_jump = 1  ->  []
```

**Constraints:** 1 to 1,000 coins, each from -1 to 100, the first never
-1; `max_jump` from 1 to 100.

## Approaches

Every arm is `fn cheapest_jump(coins: Vec[i64], max_jump: i64) ->
Vec[i64]`. The cheapest path is easy; the work is in the tie. Working
forwards and keeping, for each coin, the first way found to reach it at
its cheapest does not give the smallest path: on four free coins with
jumps of 2 it reaches coin 3 straight from coin 1 and so returns
`[1,2,4]`, not `[1,2,3,4]`. The choice that matters is the earliest one,
so three arms use each coin's cheapest cost to the end, and the fourth
compares whole paths.

| file | mechanism |
|---|---|
| `coin_path.kara` ★ | from the end, each coin's cheapest cost to the last and the first jump that achieves it, the smallest index winning a tie; following those jumps from coin 1 spells the path; O(n * max_jump) |
| `coin_path_forward.kara` | from the start, each coin's best path kept whole and compared index by index on a tie; O(n^2 * max_jump) |
| `coin_path_window.kara` | the ★ costs, with the cheapest of the next `max_jump` read off the front of a `VecDeque` of rising costs instead of scanned for; O(n) |
| `coin_path_both.kara` | costs from the start and to the end, then a walk from coin 1 that takes the smallest next coin on a cheapest path; O(n * max_jump) |
| `differential.kara` | the four arms against every path, five properties |

Every arm prints the same 11 lines: the two LeetCode examples; five more
rows (one coin; the last blocked; every coin free, where the smallest
index wins every tie; free coins that make the longest of the cheapest
paths the smallest; and a tie between a short path and a longer one that
starts smaller), each with its path; how many of 300 random rows of 1 to
60 coins have a path, with their steps, cost and a checksum; and three
rows of the problem's largest size, 1,000 coins: random with jumps of
100, all free with jumps of 100, and one blocked with jumps of 1, each
with its steps, cost and checksum. `coin_path.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which tries every path from coin 1 to the last, smaller next index
first. That order is lexicographic, so the first path found at the
cheapest cost is the answer. Each of 1,000 random rows has 1 to
14 coins, from 0 to 1 or 0 to 5 so that ties are common, about one in
six blocked, and jumps of 1 to 4.

| | property |
|---|---|
| P1 | the path is the definition's |
| P2 | empty, or from coin 1 to the last in rising steps of 1 to `max_jump`, over no blocked coin |
| P3 | it costs as little as the cheapest path |
| P4 | it is empty exactly when a sweep that counts no cost cannot reach the last coin |
| P5 | blocking a coin it does not use leaves it the same |

It prints `1000 rows (7665 coins), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a tie taking the later index | P1 269 |
| M2 | ★: the path's indices counted from 0 | P1 686, P2 686, P3 512, P5 102 |
| M3 | forward: a tie taking the later path | P1 112 |
| M4 | forward: jumps one short | P1 456, P3 234, P4 196 |
| M5 | window: an index dropped one jump early | P1 456, P3 234, P4 196 |
| M6 | window: an equal cost keeping the later index in front | P1 269 |
| M7 | both: the walk not checking a step's own cost | P1 122, P3 122 |
| M8 | both: no jump from the first index counted | P1 616, P4 616 |
| E1 | ★: the sweep starting at the last index | 0 |
| E2 | forward: of two paths, one a prefix, the longer taken as smaller | 0 |
| E3 | window: at most one index dropped off the front a step | 0 |
| E4 | both: the first coin left out of the costs from the start | 0 |

P1 kills all eight, and three of them, M1, M3 and M6, only P1 sees: each
breaks a tie the wrong way, which gives a path just as cheap and just as
valid, and only the definition knows it is not the smallest. P2 sees
only M2, whose indices count from 0. P3 sees the four that lose the
cheapest path, M2, M4, M5 and M7; P4 the three that lose a path
altogether, M4, M5 and M8. P5 catches M2 alone, by accident: counting
from 0, it calls a coin on the path unused. The four survivors cannot
change an answer: the sweep's step at the last coin finds no jump; one
coin's path is never a prefix of another's, both ending at it; the
window loses at most one index a step, since the reach moves back one
place a step; and leaving the first coin out of every cost from the
start leaves every comparison the walk makes the same.

## Verification

Every arm prints the same output as `coin_path.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` for the debug build and `abbdbaf131` for the release build
that runs `check` and `__mir-run`, with runtime archives newer than the
last `runtime/src` change.

The frozen legacy backends refuse every arm and the differential at type
checking. The harness reads `*p` from `path.iter()` over a `Vec[i64]`,
which legacy types by value; the forward arm, which the differential
copies, hands `best[i]` to `smaller`, whose parameters legacy still
takes owned, so that moves an element out of a `Vec`. Legacy is frozen,
so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes eight random rows of
100,000 coins from 0 to 100 once, about one in ten blocked; then
40 rounds each find the cheapest path through one, picked by the round,
with jumps of up to 100, and put its length, cost and indices into a
checksum. Every implementation prints `8 rows of 100000, 40 rounds:
57445 steps, checksum 457010577`, the Kāra program under `karac
__mir-run` included (in 121 s).

Each implementation is the same backward sweep over the same rows. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine), each including making the
rows:

| | time |
|---|---|
| C (`clang -O3`) | 0.68 to 0.73 s |
| Rust (`rustc -O`) | 0.71 to 0.76 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.84 to 0.94 s |
| Go | 0.78 to 0.85 s |
| Python | 22 to 23 s |
| Kāra (`karac build --mir`) | 0.77 to 0.80 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program: it reads `*p` from `path.iter()` over a `Vec[i64]`, which
legacy types by value, and its parameters are still owned rather than
borrowed, so `cheapest_jump` cannot take the row borrowed from `rows`.
That edit is by hand, on top of the `scripts/new-bench.sh` output. A
copy outside the kata with `p` for `*p` and a `ref Vec[i64]` parameter
builds under legacy and takes 0.71 to 0.75 s. Under `karac
__mir-llvm-run` the program prints the same line in 3.6 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

So the v2 build is within 10 percent of legacy and of Rust. The
comparison with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The legacy refusals
above are not filed because legacy is frozen.
