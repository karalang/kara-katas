# 547. Number of Provinces

There are `n` cities. Some of them are connected, while some are not. If
city `a` is connected directly with city `b`, and city `b` is connected
directly with city `c`, then city `a` is connected indirectly with city
`c`. A province is a group of directly or indirectly connected cities
and no other cities outside of the group. You are given an `n x n`
matrix `isConnected` where `isConnected[i][j] = 1` if the `i`th city and
the `j`th city are directly connected, and `isConnected[i][j] =
0` otherwise. Return the total number of provinces.

```
isConnected = [[1,1,0],[1,1,0],[0,0,1]]  ->  2
isConnected = [[1,0,0],[0,1,0],[0,0,1]]  ->  3
```

**Constraints:** `1 <= n <= 200`; `n == isConnected.length ==
isConnected[i].length`; `isConnected[i][j]` is `1` or
`0`; `isConnected[i][i] == 1`; `isConnected[i][j] == isConnected[j][i]`.

## Approaches

Every arm is `fn find_circle_num(is_connected: Vec[Vec[i64]]) -> i64`.

| file | mechanism |
|---|---|
| `number_of_provinces.kara` ★ | depth-first search: every city not yet seen starts a province, and a recursive walk marks every city it reaches |
| `number_of_provinces_uf.kara` | union-find over the connections above the diagonal, union by size and path halving; every join of two different sets leaves one province fewer |
| `number_of_provinces_bfs.kara` | breadth-first search from every city not yet seen, the queue one `Vec` read from a moving head, cities marked as they are queued |
| `number_of_provinces_closure.kara` | Warshall's transitive closure of the matrix, then each province counted at its lowest-numbered city; O(n^3) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 12 lines: both examples, one city, two cities
joined, a chain of four, and the first and last of five joined, each
with its answer; then for 300 random matrices of 1 to 40 cities (each
pair joined with chance 2, 20 or 80 in 1000 in turn) the number of
cities, the provinces and a checksum; and last five matrices of
200 cities (the problem's most): all alone, all joined, a chain, a hub
joined to the even cities, and a random one. `number_of_provinces.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: every city starts with its own label, and
every connection hands the smaller of its two labels to both ends until
a whole pass changes nothing, so the labels left are the provinces. Each
arm is held to the properties below on 1,000 random matrices of 1 to
12 cities, each pair joined with chance 50, 150 or 400 in 1000 in turn.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the cities renumbered by a random permutation give the same answer |
| P3 | at least 1, at most the number of cities, and at least the cities less the connections |
| P4 | one more city joined to none adds exactly 1 |
| P5 | one more city joined to every city leaves exactly 1 |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a walk looks only at higher-numbered cities | P1 338, P2 290, P5 861 |
| M2 | ★: a city's neighbours marked but not walked from | P1 439, P2 207, P5 890 |
| M3 | uf: a city never joined to the next one | P1 361, P2 333, P5 582 |
| M4 | uf: the second city's parent taken for its root | P1 42, P2 76, P3 30, P5 201 |
| M5 | bfs: the queue's head starts past the new city | P1 713, P5 1000 |
| M6 | bfs: a city's row read only from itself onwards | P1 338, P2 290, P5 861 |
| M7 | closure: the last city never used in between | P1 84, P2 145, P4 84, P5 706 |
| M8 | closure: the city just below not checked for lowest | P1 493, P2 210, P5 1000 |
| E1 | closure: `reach[k][i]` read for `reach[i][k]` | 0 |
| E2 | uf: the larger set put under the smaller | 0 |
| E3 | uf: no path halving | 0 |
| E4 | bfs: the queue read from its start for every province | 0 |

P5 is the strongest property here: a new city joined to everything makes
one province only if the arm can go from any city to any other through
it, so every mistake that loses a path shows there. M1 and M6 are the
same mistake in two arms and fail the same checks. M4 is the only mutant
P3 sees: comparing a root with a parent that is not a root can count one
join twice and give fewer provinces than the cities less the
connections. M5 never leaves the starting city, so it answers the number
of cities every time, which renumbering does not change and P3 and
P4 allow. M7 is the only one P4 sees: a city joined to none, added last,
becomes the one it never goes through, so the grown matrix is answered
right where the original was not. E1 is safe because the matrix is
symmetric and stays so, E2 and E3 change only the shape of the trees,
and E4 only rereads cities whose neighbours are all seen already.

## Verification

Every arm prints the same output as `number_of_provinces.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes on every arm, the differential and the bench program.

The frozen legacy backends: `karac run --interp` prints the same output
for every arm. `karac run` and `karac build` fail every arm in codegen
("Call parameter type does not match function signature" on
`show("example 1", ...)`), and stop the differential at type checking on
`*l` over `iter()` of a `Vec[i64]` ("unary '*' requires 'ref T' ...
found 'i64'"). Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 30 random matrices of
200 cities (the problem's most), matrix g joining each pair with chance
1 + g % 10 in 1000, once. Then 200 times over, one connection of every
matrix is flipped, picked by the round and the matrix, and the matrix is
answered; the provinces go into the checksum. Every implementation
prints `30 matrices, 200 rounds each: 222086 provinces, checksum
569798085`, the Kāra program under `karac __mir-run` included (45.9 s).

C keeps each matrix in one flat array; Rust, Go and Python use a vector
of rows as Kāra does. Spot timings on a shared 4-core container, three
runs each (two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.27 to 0.28 s |
| Rust (`rustc -O`) | 0.29 to 0.33 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.28 to 0.31 s |
| Go | 0.37 to 0.43 s |
| Python | 5.45 to 5.81 s |
| Kāra (`karac build --mir`) | 0.33 to 0.36 s |

The legacy `karac build` refuses this program: it moves `all[g]` out of
the index where v2 borrows it (`E_INDEX_MOVE_NON_COPY`). So `bench.sh`
builds the Kāra program with `karac build --mir`, the v2 compiled
backend; that edit is by hand, on top of the `scripts/new-bench.sh`
output. The `--mir` row is timed at kara `2d241d9b05`. Under `karac
__mir-llvm-run` the program prints the same line in 1.9 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark. The Kāra row is about 1.1 times Rust's.

Re-timed on 2026-10-14 at kara `2d241d9b05`. The row first published
here, 0.40 to 0.44 s, was taken with a runtime archive older than kara
`8969be0434`, which runs `main` on a second thread, and once a process
has two threads glibc's `malloc` and `free` take a lock on every call.
Linked against that older runtime and against the current one by the
same compiler, three runs each, the program takes 0.39 to 0.41 and
0.36 to 0.40 s: the older runtime alone costs this program about 10%.

## Compiler findings

None new. Nothing was filed from this kata; the legacy failures above
are not filed because legacy is frozen.
