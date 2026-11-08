# 473. Matchsticks to Square

You are given an integer array `matchsticks` where `matchsticks[i]` is
the length of the `i`th matchstick. You want to use all the matchsticks
to make one square. You should not break any stick, but you can link
them up, and each matchstick must be used exactly one time.

Return `true` if you can make this square and `false` otherwise.

```
matchsticks = [1,1,2,2,2]  ->  true    (sides 2, 2, 2 and 1+1)
matchsticks = [3,3,3,3,4]  ->  false
```

**Constraints:** `1 <= matchsticks.length <= 15`; `1 <= matchsticks[i]
<= 10^8`.

## Approaches

Every arm is `fn makesquare(matchsticks: Vec[i64]) -> bool`, and
borrows the list. Each side is a quarter of the total, so a total that
is not a multiple of 4 is `false` at once.

| file | mechanism |
|---|---|
| `matchsticks.kara` ★ | backtracking: the sticks from longest to shortest, each tried on every side with room left, skipping a side as long as one already tried. Worst case O(4^n), far less in practice |
| `matchsticks_table.kara` | a table over the 2^n sets of sticks: for each set, how far along the side being filled a valid order of those sticks gets (the set's total modulo the side), or -1 when no order keeps every stick inside its side. O(2^n × n) |
| `matchsticks_sides.kara` | one side at a time, each new side started by the lowest unused stick, with the sets of used sticks from which nothing works remembered in a `Set[i64]`. O(2^n × n) |
| `matchsticks_subsets.kara` | every set of sticks that makes exactly one side, listed by bitmask, then three of them that do not overlap, each holding the lowest stick not yet used; the sticks left over are the fourth side |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 15 lines: the two LeetCode examples, four
ones, three sticks, two 12-stick squares, four sticks of 10^8, two that
have a multiple-of-4 total but no square (`6, 6, 6, 6, 4, 2, 2` and a
stick longer than a side), 15 sticks in five shapes (fourteen 5s and a
4, twelve 1s and three 2s, fourteen 4s and an 8, fifteen 12s, and 1 to
10 then 5 down to 1), and for 400 random cases of 1 to 12 sticks the
number of sticks, how many are squares, and a checksum of the answers
in order. A random case is a square cut into pieces (each side gets at
least one, cut at distinct random points), the same with one unit moved
from one stick to another, or lengths from 1 to 8, a third each.
`matchsticks.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases of 1 to 8 sticks, made the same three ways as in the
harness (random lengths from 1 to 6).

| | property |
|---|---|
| P1 | the arm says a square exactly when some way of giving the sticks to four sides makes the sides equal, every way tried (4^(n-1), the first stick on the first side) |
| P2 | the same sticks in another order give the same answer |
| P3 | every stick 2 to 5 times as long gives the same answer |
| P4 | a square stays a square with four more sticks of one length; a non-square stays one with two of its sticks glued into one |
| P5 | a square cut into 10 to 12 sticks is found |

P4 holds both ways round: the four new sticks go one to a side, and two
glued sticks that end up on one side could have lain there apart. P5
reaches past the sizes P1 can try; the sizes stop at 12 so the run fits
the corpus runner's time limit (the table and subset arms are 2^n).

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, in 23 to 26 s, and a count for each property when
anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a stick that exactly finishes a side does not fit | P1 522, P4 522, P5 1500 |
| M2 | ★: the last (shortest) stick is never placed | P1 28, P3 7, P4 6 |
| M3 | table: a full side does not start the next one | P1 522, P4 522, P5 1500 |
| M4 | table: a stick may run one unit past the end of its side | P1 182, P3 188, P4 41 |
| M5 | sides: only the lowest unused stick is ever tried | P1 364, P2 117, P4 477, P5 1365 |
| M6 | sides: the set without the second stick is remembered as dead | P1 1, P2 3, P4 12, P5 4 |
| M7 | subsets: two disjoint sides are enough | P1 56, P2 65, P4 5 |
| M8 | subsets: one stick alone is never a side | P1 431, P2 71, P5 244 |

M1 and M3 find no square at all, so they fail every square, and fail
them identically. M2 calls a case a square when everything but its
shortest stick fits, M4 when a side may run over by a unit; the near
misses of the harness, a square with one unit moved, are what catch M4,
and scaling the sticks (P3) turns a one-unit overrun into a k-unit one
it no longer allows. M5 only ever extends a side with the lowest unused
stick. M6 is the weakest kill: a wrong set marked dead matters only
when the search would have come back to it. Two first drafts were
equivalent and were replaced: "the set one higher is remembered as dead"
(every set the search reaches holds stick 0, so one higher never holds
it and is never reached) and "the table may use the first stick twice"
(killed by P2 alone, twice in 30,000 checks).

## Verification

All four arms print the same output as `matchsticks.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file, the bench program included. The
differential prints `30000 checks, 0 failures` on both. The four arms
and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

The frozen legacy backends get the harness wrong: `karac run --interp`,
LLJIT and legacy `karac build` all stop with an index out of bounds in
`random_case`, on every arm and on the differential. The cause is in
`square_sticks`: legacy evaluates the index of
`count[next_random(seed) % 4] += 1` twice, drawing two random numbers,
so the side counts no longer add up to `n` (12 sticks asked for, 8
made, on the first case that goes wrong) and a later `sticks[to]` runs
past the end. MIR draws once, which is what the Python mirror does.
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm on 2,000 sets of 15 sticks (the
problem's most), each from 50 to 99 long, the last made longer by up to
4 so the total is a multiple of 4. Sticks this close in length leave
many near fits to rule out before the backtracking can say no, and 292
of the sets are squares. Every implementation prints `2000 sets of 15
sticks: 292 squares, checksum 250458079`, the Kāra program under
`karac __mir-run` included (in 287 s).

Every mirror sorts a copy of the sticks longest first and backtracks
over four side lengths in the same order, skipping a side as long as
one tried before it.

The bench keeps the four sides in a fixed `Array[i64, 4]` (`[0; 4]`), as
Rust, C and Go keep theirs; the ★ arm uses a `Vec`. The M5 parity pass
of 2026-11-08 moved the bench to the array: with the `Vec` every
`sides[s]` reloaded the header and checked the length, 9.94G
instructions against 8.69G (callgrind, x86), and checked Rust 7.66G. The M5 tables below measured the bench
before this change.

### Apple M5 Pro, 2026-11-07

30 runs each, 5 warmups, on the Apple M5 Pro, karac `0.8.1-dev.14833+gfa3eab9b4`
(gfa3eab9b4, the v2/MIR backend), measured 2026-11-07, with the Kāra binary built
`KARAC_AUTO_PAR=0`. This is the kata's first M5 measurement; Python was not run.
The last column is Kāra's mean over that row's mean.

| implementation | mean | Kāra / this |
|---|---|---|
| rust `-O` | 203.4 ms ± 0.8 | 1.37× |
| rust `-O -C overflow-checks=on` (equal-safety) | 209.9 ms ± 0.9 | 1.33× |
| c `clang -O3` | 214.6 ms ± 0.8 | 1.30× |
| **kāra `karac build`, seq** | **278.5 ms ± 0.6** | **—** |
| go `go build` | 440.4 ms ± 4.2 | 0.63× |

Kāra is 1.37× `rustc -O`, 1.33× equal-safety Rust, 1.30× C and 0.63× Go. The 1.33× gap to equal-safety Rust was not investigated and has gone to the compiler's review. Against the legacy backend (exact counts, dd86e3955, `KARAC_AUTO_PAR=0`) Kāra executes 1.19× the instructions in 1.18× the cycles.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 50.3 ms ± 0.6 | 49.1 KiB | 1.0 MiB |
| rust | 123.0 ms ± 0.7 | 455.7 KiB | 1.1 MiB |
| kāra | 135.6 ms ± 1.8 | 83.1 KiB | 1.1 MiB |
| go | — | 2468.5 KiB | 3.2 MiB |

`karac build` is 2.7× clang's cold compile and 1.1× rustc's. Kāra's
85,112-byte binary is 1.7× clang's and 5.5× smaller than rustc's. Raw numbers are in
[`bench/results.json`](bench/results.json). The sink matches across the Kāra,
Rust, C and Go builds (`2000 sets of 15 sticks: 292 squares, checksum 250458079`).

### Container x86-64 history

Spot timings on a shared 4-core container, three
runs each (two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.48 to 0.51 s |
| Rust (`rustc -O`) | 0.51 to 0.59 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.57 to 0.77 s |
| Go | 0.98 to 1.13 s |
| Python | 51.0 to 54.6 s |
| Kāra (`karac build`) | 0.75 to 0.77 s |
| Kāra (`karac build --mir`) | 1.07 to 1.50 s |

The legacy `karac build` gets this program right (it has no compound
assignment with a random index), so `bench.sh` is the
`scripts/new-bench.sh` output unchanged and times that build. The
`--mir` row is the v2 compiled backend, timed for comparison. Both Kāra
rows are timed at kara `b0b1557b39`. Under `karac __mir-llvm-run` the
program prints the same line in 3.7 s, compile included; that JITs the
MIR's IR without optimization passes, so it is not a benchmark.

## Compiler findings

- **B-2026-10-13-7** (MIR and `karac check`, open): the MIR backends
  have no `Iterator.min` / `max` / `min_by` / `max_by` / `min_by_key` /
  `max_by_key` and no `Vec.min` / `max`, all in the library spec;
  `m.iter().max()` is refused with "no method 'max' on type 'VecIter'",
  and `m.max()` fails at run time ("call of unknown function
  Vec[i64].max"). `karac check` accepts `min` and `max` but types the
  result by value, so the spec's `*m.iter().max().unwrap()` is refused,
  and it has no `min_by` or `max_by_key`. Found probing the ways to
  write the longest-stick test; the arms sort instead, which is what
  the backtracking needs anyway.
