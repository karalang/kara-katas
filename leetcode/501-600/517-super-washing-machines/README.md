# 517. Super Washing Machines

You have `n` super washing machines on a line. Initially, each washing
machine has some dresses or is empty.

For each move, you could choose any `m` (`1 <= m <= n`) washing
machines, and pass one dress of each washing machine to one of its
adjacent washing machines at the same time.

Given an integer array `machines` representing the number of dresses
in each washing machine from left to right on the line, return the
minimum number of moves to make all the washing machines have the same
number of dresses. If it is not possible to do it, return `-1`.

```
machines = [1,0,5]  ->  3
machines = [0,3,0]  ->  2
machines = [0,2,0]  ->  -1
```

**Constraints:** `1 <= n <= 10^4`; `0 <= machines[i] <= 10^5`.

## Approaches

Every arm is `fn find_min_moves(machines: Vec[i64]) -> i64`. Each first
returns -1 when the dresses do not share out evenly, then works with
the average.

| file | mechanism |
|---|---|
| `find_min_moves.kara` ★ | two lower bounds, which together are also enough: the running surplus left of each gap is how many dresses must cross it, at most one per move, and a machine above the average can send only one per move. The answer is the largest of all of them, in one pass. O(n) |
| `find_min_moves_sides.kara` | for each machine, how many dresses the machines left of it and right of it need, from a running prefix sum and the total (`iter().sum()`): when both sides need dresses they all leave this machine, so it takes their sum, otherwise the larger flow. O(n) |
| `find_min_moves_search.kara` | binary search on the answer between 0 and the total, with `fits(k)` checking in one pass that no gap carries more than k and no machine gives away more than k. O(n log total) |
| `find_min_moves_fold.kara` | the ★ arm's pass as one `iter().fold((0, 0), \|(surplus, most), m\| ...)`, the closure destructuring its tuple accumulator. O(n) |
| `differential.kara` | the four arms on 1,500 cases, five properties |

Every arm prints the same 8 lines: the three LeetCode examples, one
machine, a pile in the middle, two piles at the ends, one full machine
and nine empty ones, and for 300 random rows of 1 to 40 machines
holding up to 3, 100 or 100,000 dresses in turn, every other row
topped up so it shares out evenly, the count that can be evened out
and a checksum. `find_min_moves.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 cases. Each has a small row of 1 to 4 machines, holding 0 to 3
dresses each or, every other case, 0 or 1 each with up to 8 more piled
on one, and a larger row of 1 to 30 machines holding up to 1,000,
topped up to share out evenly every other case.

| | property |
|---|---|
| P1 | the small row's answer is the reference's: a breadth-first search over every row of dresses, where one move has each machine holding a dress pass one left, pass one right or do nothing, all at once |
| P2 | the larger row read from the other end has the same answer |
| P3 | the same number more in every machine changes nothing |
| P4 | twice the dresses in every machine takes twice the moves (a row that cannot be evened out stays so, unless twice its dresses share out) |
| P5 | the row written out twice, end to end, has the same answer |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a machine's own excess not counted | P1 32 |
| M2 | ★: only flows to the right counted, `surplus` for `surplus.abs()` | P1 4, P2 673 |
| M3 | sides: both sides needing dresses takes the larger, not the sum | P1 32 |
| M4 | sides: the right side's sum keeps machine i | P1 585, P2 811, P3 670 |
| M5 | search: `fits` never checks a machine's excess | P1 32 |
| M6 | search: the range stops at half the total | P1 51 |
| M7 | fold: the surplus starts at 1 | P1 604, P2 756, P4 755 |
| M8 | sides: one side needing dresses is enough to add the two (`or` for `and`) | P1 3 |
| E1 | ★: the two bounds taken in the other order | 0 |
| E2 | search: the range runs to the total plus 5 | 0 |
| E3 | fold: the flow read before this machine is added | 0 |
| E4 | sides: `>= 0` for `> 0` on both sides | 0 |

E1 and E2 change nothing the answer depends on. E3 reads the surplus
before each machine instead of after it: that is the same set of gaps
shifted by one, the first (before any machine) and the last (after all
of them) both 0. E4 differs only when a side needs nothing, where the
sum and the larger flow agree.

Only the reference sees M1, M3, M5, M6 and M8, and on few cases. Each
gets one of the two bounds wrong in the same way on every row, so a
row reversed, raised, doubled or written twice gives the same wrong
answer each time; the four other properties hold for any rule built
from the flows and the excesses. The reference sees them only where
the bound they break is the one that sets the answer, which in random
rows is rare: a machine's excess (M1, M5) or the sum of both sides
(M3) beats the largest flow when one machine holds most of the
dresses, which is why half the small rows pile up to 8 more on one
machine; with only uniform small rows, M1, M3 and M5 failed 13 times
each and M8 5 times. M8 changes only machines with one side short of
dresses and the other over, where it adds the two flows and so answers
too little; that the overall answer is then usually set elsewhere is
inferred from the three cases, not measured. M6 matters only when the
answer is more than half the total, a pile again.

## Verification

Every arm prints the same output as `find_min_moves.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `30000 checks, 0 failures` on the first two and runs clean
under the third. `karac check` passes on every arm, the differential
and the bench program.

On the frozen legacy backends the sides arm agrees: `karac run
--interp`, LLJIT, legacy `karac build` and a `KARAC_AUTO_PAR=1` build
print the same output. The other three arms, the differential and the
bench program are refused by all of them at type checking: legacy
types the items of a `Vec`'s `iter()` by value, so it refuses `*m`,
"unary '*' requires 'ref T' ... found 'i64'". Legacy is frozen, so
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 random rows of 10,000
machines (the problem's most) holding up to 100,000 dresses each,
every other row topped up so it shares out evenly, once. Then it
solves each 300 times. Every implementation prints `100 rows of 10000
machines, 300 times each: checksum 436689043`, the Kāra program under
`karac __mir-run` included (in 702 s).

Spot timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.23 s |
| Rust (`rustc -O`) | 0.22 to 0.28 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.36 to 0.44 s |
| Go | 0.44 to 0.45 s |
| Python | 27.1 to 27.3 s |
| Kāra (`karac build --mir`) | 0.34 to 0.39 s |

The legacy `karac build` refuses this program at the same `*m` (see
Verification). So `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`0736eef763`. Under `karac __mir-llvm-run` the program prints the same
line in 3.6 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

None filed. Every arm, the differential and the bench program run
right on the v2 backends, and `karac check` passes on all of them as
first written.
