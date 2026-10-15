# 502. IPO

Suppose LeetCode will start its IPO soon. In order to sell a good price
of its shares to Venture Capital, LeetCode would like to work on some
projects to increase its capital before the IPO. Since it has limited
resources, it can only finish at most `k` distinct projects before the
IPO. Help LeetCode design the best way to maximize its total capital
after finishing at most `k` distinct projects.

You are given `n` projects where the `i`th project has a pure profit
`profits[i]` and a minimum capital of `capital[i]` is needed to start
it. Initially, you have `w` capital. When you finish a project, you
will obtain its pure profit and the profit will be added to your total
capital.

Pick a list of at most `k` distinct projects from given projects to
maximize your final capital, and return the final maximized capital.

```
k = 2, w = 0, profits = [1,2,3], capital = [0,1,1]  ->  4
k = 3, w = 0, profits = [1,2,3], capital = [0,1,2]  ->  6
```

**Constraints:** `1 <= k <= 10^5`; `0 <= w <= 10^9`; `n == profits.length
== capital.length`; `1 <= n <= 10^5`; `0 <= profits[i] <= 10^4`;
`0 <= capital[i] <= 10^9`.

## Approaches

Every arm is `fn find_maximized_capital(k: i64, w: i64, profits:
Vec[i64], capital: Vec[i64]) -> i64`. All four are the same greedy:
capital only grows, so a project once affordable stays affordable, and
of the affordable ones the most profitable is always the right next
project.

| file | mechanism |
|---|---|
| `ipo.kara` ★ | the project indices sorted by capital (`sort_by_key`); each round every newly affordable profit goes into a `PriorityQueue.max_first()` and the top is taken |
| `ipo_heaps.kara` | no sort: the projects wait as `(capital, profit)` pairs in a smallest-first `PriorityQueue.from(...)`, and each round moves the affordable ones, read with `peek`, into the largest-first heap of profits |
| `ipo_scan.kara` | no heap: each round scans every project not yet done for the most profitable affordable one; O(k n) |
| `ipo_sorted.kara` | the projects sorted as `(capital, profit)` pairs, the affordable profits counted in a `SortedMap[i64, i64]`; the last entry, read with `iter().rev().next()`, is the next project |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 8 lines: the two LeetCode examples, nothing
affordable, `k` beyond `n`, a small project that must come first, no
profit, the largest numbers the problem allows, and for 300 random
cases of 1 to 20 projects the total final capital and a checksum.
`ipo.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases of 1 to 6 projects of profit 0 to 20 needing 0 to
30, `k` from 1 to 7 and `w` from 0 to 10.

| | property |
|---|---|
| P1 | the capital is the reference's, which tries every order of up to `k` affordable projects and keeps the best; no greedy |
| P2 | `d` more capital to start with ends with at least `d` more |
| P3 | allowing one more project never ends with less, and once `k >= n` allowing more changes nothing |
| P4 | the projects in the reverse order give the same capital |
| P5 | one more project that needs more than all the profits together could bring changes nothing |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Ten edits to `differential.kara`, two to each arm and two equivalent
ones, each run under `karac __mir-run`. All eight non-equivalent ones
are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the heap is smallest-first (`PriorityQueue.new()`) | P1 171, P2 54 |
| M2 | ★: a project needing exactly the capital is not affordable (`<` for `<=`) | P1 133 |
| M3 | heaps: the first project out of reach is made ready too | P1 1049, P5 1171 |
| M4 | heaps: `k + 1` rounds (`0..=k`) | P1 199 |
| M5 | scan: a project already done can be done again | P1 537, P3 322, P5 326 |
| M6 | scan: the least profitable affordable project is taken (`<=` for `>`) | P1 171, P2 54 |
| M7 | sorted: the first entry, the smallest profit, is taken (`iter().next()`) | P1 171, P2 54 |
| M8 | sorted: a count that reaches 1 is never removed (`count == 0`) | P1 537, P2 3, P3 219, P5 304 |
| E1 | scan: ties go to the last affordable project (`>=` for `>`) | 0 |
| E2 | ★: the order is sorted by `(capital[i], i)` | 0 |

E1 is equivalent because two projects of the same profit leave the
same capital, whichever is taken. E2 is equivalent because
`sort_by_key` is stable: the indices start in order, so equal
capitals stay in index order, which is what the pair key spells out.

M1, M6 and M7 are the same wrong greedy, the least profitable project
first, written three ways, and fail the same cases. It is the only
mutation that breaks P2: with the smallest profits taken first, more
starting capital can unlock a project worth less than the one it
displaces, so the final capital can grow by less than the extra. M5 and
M8 both let a project be done again, so rounds beyond the number of
projects keep adding capital, which the second half of P3 sees. P4 kills none of the
eight; no mutation depends on the order the projects are given in.

## Verification

All four arms print the same output as `ipo.py` under `karac __mir-run`
(the v2 MIR interpreter) and `karac __mir-llvm-run`, and run clean
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer):
output identical, no error, no leak. The differential prints `30000
checks, 0 failures` on both and runs clean under the third.

`karac check` passes on the ★ and scan arms and the bench program. On
the heaps and sorted arms and the differential it passes with
`KARAC_CHECK_LIBRARY=1`, and default `karac check` refuses them (see
Compiler findings).

On the frozen legacy backends, `karac run --interp` prints the same
output for the ★ and scan arms, but LLJIT and legacy `karac build` fail
on both at codegen: "Module verification failed: Call parameter type
does not match function signature!", at the harness's calls to `show`,
whose first parameter is a `Str` given a string literal (as in kata
501). The heaps and sorted arms and the differential are refused on
legacy as by default `karac check`. Legacy is frozen, so this is noted,
not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 60 cases of 100,000
projects (the problem's most) with `k` = 100,000 (the most), profits
from 0 to 10,000 (the most) and capital needs from 0 to 10^5, 10^7 or
10^9 (the most) in turn, `w` from 0 to 1,000, once. Then it solves each
case once, folding the final capitals into a total and a checksum.
Every implementation prints `60 cases of 100000 projects: total capital
17833039386, checksum 726210963`, the Kāra program under `karac
__mir-run` included (in 157 s).

Every mirror sorts a fresh index array by capital and pushes onto a
fresh largest-first heap for each case, as the ★ arm does: Rust
`sort_by_key` and `BinaryHeap`, Go `slices.SortStableFunc` and
`container/heap`, Python `sorted` and `heapq` (negated profits), and C
`qsort` and a hand-written binary heap. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.47 to 1.57 s |
| Rust (`rustc -O`) | 0.73 to 0.77 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.63 to 0.69 s |
| Go | 3.73 to 4.07 s |
| Python | 8.6 to 9.4 s |
| Kāra (`karac build --mir`) | 1.98 to 2.15 s |

The sort is most of the difference: C's `qsort` and Kāra's sort both
call their comparison through a function pointer for every comparison,
where Rust inlines the key (kara B-2026-10-13-18, below). Go's
`container/heap` boxes every pushed profit in an interface.

The legacy `karac build` refuses this program: "cannot move out of an
index expression", on `all_profits[c]` and `all_capital[c]` in the call
to `find_maximized_capital`, which v2 reads as borrows. So `bench.sh`
builds the Kāra program with `karac build --mir`, the v2 compiled
backend. That edit is by hand, on top of the `scripts/new-bench.sh`
output. The `--mir` row is timed at kara `486f47f97d`. Under `karac
__mir-llvm-run` the program prints the same line in 7.5 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

## Compiler findings

kara B-2026-10-13-18 (perf, open): `sort_by_key` on the v2 compiled
backend runs about 3.5 to 4 times slower than Rust's. The runtime's
merge sort calls the comparison through a function pointer for every
comparison, and the comparison calls the key closure for each side. In
this kata's bench the sort is 63% of the instructions; sorting 1,000,000
indices by an `i64` key 10 times takes 2.7 s on `karac build --mir`
(2.6 s on legacy `karac build`) against 0.7 s for `rustc -O`.

Three existing rows show up here too.

kara B-2026-10-13-11 (open): `PriorityQueue.peek` is typed `Option[T]`
by value in default `karac check`, where the spec gives `Option[ref T]`.
The heaps arm reads the root as `while let Some((need, _)) =
waiting.peek()` and compares `*need`, the spec's form. Both v2 backends
run it (kara `28c51bf033` made `peek` a view in the MIR), and `karac
check` passes it with `KARAC_CHECK_LIBRARY=1`, but default `karac check`
refuses it: "unary '*' requires 'ref T' ... found 'i64'".

The sorted arm's `ready.iter().rev().next()` gives `(ref K, ref V)`, so
the arm reads `*p` and `*count`. That runs on both v2 backends and
passes `karac check` with `KARAC_CHECK_LIBRARY=1`; default `karac check`
types the items by value and refuses the `*`. As for kata 495, default
`karac check` does not see the Kāra library's iterator types. Kara
B-2026-10-12-23 was closed in `7609de871d` for serde programs only,
which now check with the library; default check still refuses this arm
at that commit.

kara B-2026-10-06-68 (open, from kata 352; narrowed on 2026-10-15 to the
`Vec` that `range` returns and the methods below): `SortedMap.entry`,
`min` and `max` are implemented but not in the spec's `SortedMap` table
(docs/library/collections.md). The sorted arm counts profits with
`*ready.entry(p).or_insert(0) += 1`, which the implementation accepts
and the table does not list. It takes the largest entry from the back of
`iter()`, which is in the spec, rather than `max()`; the
implementation's `max()` gives the entry by value, where the spec's
`floor` and `ceiling` give `(ref K, ref V)`.
