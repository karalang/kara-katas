# 546. Remove Boxes

You are given several boxes with different colours represented by
different positive numbers. You may experience several rounds to remove
boxes until there is no box left. Each time you can choose some
continuous boxes with the same colour (i.e., composed of `k` boxes, `k
>= 1`), remove them and get `k * k` points. Return the maximum points
you can get.

```
boxes = [1,3,2,2,2,3,4,3,1]  ->  23
boxes = [1,1,1]              ->  9
boxes = [1]                  ->  1
```

**Constraints:** `1 <= boxes.length <= 100`; `1 <= boxes[i] <= 100`.

## Approaches

Every arm is `fn remove_boxes(boxes: Vec[i64]) -> i64`. Each one
carries, beside a span of boxes, how many boxes of its first box's
colour are already waiting to go with it; that count is what makes the
problem split into smaller ones.

| file | mechanism |
|---|---|
| `remove_boxes.kara` ★ | memoized recursion on (l, r, k) in an n * n * n `Vec`; box l first takes in the rest of its run, and only the first box of each later run of its colour is tried as the one it waits for |
| `remove_boxes_table.kara` | the same table bottom up, spans from the shortest, k over every count that can sit before box i |
| `remove_boxes_map.kara` | the plain recursion, every later box of l's colour tried, memoized in a `Map[(i64, i64, i64), i64]` holding only the states it reaches |
| `remove_boxes_runs.kara` | the row squeezed into runs of one colour first (a colour and a count each), and the recursion over runs |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 12 lines: the three examples, two colours
alternating, a nest, and a row where the best move is to wait, each with
its answer; then for 300 random rows of 1 to 20 boxes (from 3, 5 or
10 colours in turn) the number of boxes, the points and a checksum; and
last five rows of 100 boxes (the problem's most): from 3 colours, from
100 colours, of one colour, two colours alternating, and a palindrome of
50 colours. `remove_boxes.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: every run of one colour in the row is
tried as the next to go, and the rows left behind are memoized in a
`Map[Vec[i64], i64]`. Each arm is held to the properties below on
1,000 random rows of 1 to 8 boxes, from 2, 3 or 5 colours in turn.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the row reversed gives the same answer |
| P3 | the colours renamed (c to 11 - c) give the same answer |
| P4 | at least one point a box, and at most the sum over colours of the count squared |
| P5 | one more box of a new colour on the end adds exactly 1 |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a box waiting on a later one takes only the boxes before l, not l's run | P1 544 |
| M2 | ★: the first later box of l's colour skipped | P1 357 |
| M3 | table: the waiting count not grown when box i waits | P1 766 |
| M4 | table: k + 1 boxes scored 2k + 1, not squared | P1 766 |
| M5 | map: box l never waits for the box right after it | P1 616 |
| M6 | map: every state stored as if nothing waited | P1 260, P2 209, P4 180 |
| M7 | runs: the boxes waiting before run l left out of its score | P1 544 |
| M8 | runs: a run's count reset rather than grown | P1 616, P4 334 |
| E1 | ★: every later box of l's colour tried, not just the first of each run | 0 |
| E2 | table: k run up to n at every i | 0 |
| E3 | map: the memo never consulted | 0 |
| E4 | runs: the memo sized by boxes, not runs | 0 |

Almost every kill is the definition's (P1) alone. The other four
properties hold for any scoring that is symmetric and takes each run
whole, and most of these mistakes keep both: they only make an arm give
up points it could have had, which P4's bounds and P5's one extra point
are too loose to see. M6 is the exception, since a stored state with the
wrong count can also give back more points than the row holds (P4) and
depend on which end is read first (P2). M8 scores a run of three as
three runs of one, so a row of one colour falls under P4's floor. E1 to
E4 are safe: a box in the middle of a run is never a better box to wait
for than the run's first, k past i is never reached, and a memo that is
never hit, or is larger than it needs, changes only the time.

## Verification

Every arm prints the same output as `remove_boxes.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes on every arm, the differential and the bench program.

The frozen legacy backends: the map and runs arms and the differential
stop at type checking under `karac run --interp`, `karac run` and `karac
build`, on `*v` over a value that legacy reads as `i64` ("unary '*'
requires 'ref T' ... found 'i64'"). The ★ and table arms fail `karac
run` and `karac build` in codegen ("Call parameter type does not match
function signature" on `show("example 1", ...)`), and under `karac run
--interp` they do not finish within the 300 s budget. Legacy is frozen,
so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 40 random rows of 100 boxes
(the problem's most), row g from 2 + g % 8 colours, once, and answers
every row 5 times, summing the points and folding each answer into a
checksum. Every implementation prints `40 rows, 5 times each:
214170 points, checksum 417102104`, the Kāra program under `karac
__mir-run` included (80.4 s).

Every implementation is the same memoized recursion over a flat n * n *
n table of 64-bit integers, a fresh one per answer. Spot timings on a
shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.34 to 0.37 s |
| Rust (`rustc -O`) | 0.37 to 0.42 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.36 to 0.39 s |
| Go | 0.59 to 0.71 s |
| Python | 10.45 to 11.10 s |
| Kāra (`karac build --mir`) | 0.46 to 0.53 s |

The legacy `karac build` refuses this program: it moves `all[t]` out of
the index where v2 borrows it (`E_INDEX_MOVE_NON_COPY`). So `bench.sh`
builds the Kāra program with `karac build --mir`, the v2 compiled
backend; that edit is by hand, on top of the `scripts/new-bench.sh`
output. The `--mir` row is timed at kara `2b8238c108`. Under `karac
__mir-llvm-run` the program prints the same line in 2.1 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark. The Kāra row is about 1.3 times Rust's.

## Compiler findings

None new. Nothing was filed from this kata; the legacy failures above
are not filed because legacy is frozen.
