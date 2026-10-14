# 544. Output Contest Matches

During the NBA playoffs, we always set the rather strong team to play
with the rather weak team, like making the rank 1 team play with the
rank nth team, which is a good strategy to make the contest more
interesting. Given `n` teams, return their final contest matches in the
form of a string. The `n` teams are labeled from `1` to `n`, which
represents their initial rank. We use parentheses `(` `)` and commas
`,` to represent the contest team pairing: parentheses for pairing and
commas for partition. During the pairing process in each round, you
always pair the rather strong one with the rather weak one.

```
n = 4  ->  "((1,4),(2,3))"
n = 8  ->  "(((1,8),(4,5)),((2,7),(3,6)))"
```

**Constraints:** `n == 2^x` where `x` is in the range `[1, 12]`.

## Approaches

Every arm is `fn find_contest_match(n: i64) -> String`.

| file | mechanism |
|---|---|
| `find_contest_match.kara` ★ | the teams as strings `"1"` to `"n"`; each round the i-th strongest and the i-th weakest are written as a pair over the i-th place, halving the list |
| `find_contest_match_deque.kara` | each round's teams in a `VecDeque[String]`, the strongest taken off the front and the weakest off the back, the pairs pushed into the next round's deque |
| `find_contest_match_seeds.kara` | recursive from the top: the group of m teams whose best is s joins the group of m / 2 whose best is s and the one whose best is 2n/m + 1 - s |
| `find_contest_match_order.kara` | the order the teams appear in first, by doubling from `[1]`, then the brackets from each place: one opened for every block of 2, 4, 8, ... teams starting there and one closed for every block ending there |
| `differential.kara` | the four arms against a reference, five properties |

Every arm prints the same 16 lines: the answers in full for 2, 4, 8 and
16 teams, then for every size the problem allows, 2 to 4,096 teams, the
answer's length (27,562 bytes at 4,096) and a checksum over its bytes.
`find_contest_match.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and a reference that
spells the statement out round by round, each round a fresh list. The
input is only `n`, and the problem allows twelve values of it, so the
differential runs every one, 2 to 4,096 teams, and parses each answer to
check its shape.

| | property |
|---|---|
| P1 | the answer is the reference's |
| P2 | it reads as nested pairs, every team from 1 to n exactly once, the two sides of every pair the same size |
| P3 | in a pair of groups of c teams, the two best teams add to n / c + 1: the strongest of the groups left met the weakest |
| P4 | in every pair the side with the better best team comes first |
| P5 | every group's teams average (n + 1) / 2 |

It prints `12 sizes, 4 arms, 240 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the strongest paired with the middle, not the weakest | P1 11, P3 11, P5 11 |
| M2 | ★: each pair written weaker side first | P1 12, P4 12 |
| M3 | deque: two teams off the front, so neighbours meet | P1 11, P3 11, P5 11 |
| M4 | deque: each match pushed at the front of the next round | P1 11, P4 11 |
| M5 | seeds: the other group's best team one too low | P1 12, P2 12, P3 12, P5 12 |
| M6 | seeds: the weaker group written first | P1 12, P4 12 |
| M7 | order: each team followed by the one l places on | P1 11, P3 11, P5 11 |
| M8 | order: the closing brackets counted from i, not i + 1 | P1 12, P2 12 |
| E1 | ★: each round's pairs made from the back | 0 |
| E2 | deque: the next round copied, not moved | 0 |
| E3 | seeds: a single team caught with `<` | 0 |
| E4 | order: the block search without its bound on b | 0 |

The counts are out of twelve sizes. The wrong pairings
(M1, M3, M7) still use every team once and keep every pair even, so
P2 passes them; P3 and P5 see that the wrong teams met, at every size
but 2, where there is only one way to pair. The edits that only change
which side is written first (M2, M4, M6) leave the pairing right and are
seen by P4 alone. M4 is the subtle one: pushing each match at the front
reverses the next round, so the following round still pairs best with
worst but writes the weaker group first; at 2 teams there is no next
round. E1 is safe because a round reads only places it has not yet
written: the i-th pair reads places i and m - 1 - i, and only the first
half is written.

## Verification

Every arm prints the same output as `find_contest_match.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `240 checks, 0 failures` on the first two and runs clean under
the third. `karac check` passes on every arm, the differential and the
bench program.

The frozen legacy backends: `karac run --interp`, `karac run` and `karac
build` stop every arm and the differential at type checking, on `*b`
over a string's `bytes().iter()` in the harness's checksum, and in the
order arm and the differential also on `*t` over `order.iter()` of a
`Vec[i64]` ("unary '*' requires 'ref T' ... found 'u8'" and "found
'i64'"). The bench program, which reads one byte by index instead,
builds under legacy `karac build` and prints the right line. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. 200 times over, it answers every size
the problem allows, 2 to 4,096 teams; the length of each answer is
summed, and one byte of it, picked by the round and the size, goes into
the checksum. Every implementation prints `200 rounds of 2 to
4096 teams: 10492000 bytes, checksum 290730140`, the Kāra program under
`karac __mir-run` included (10.1 s).

Every mirror writes each pair as a fresh string: Rust with `format!`, Go
by `+`, Python with an f-string, and C with `malloc` and two `memcpy`s,
freeing the two strings each pair replaces. Spot timings on a shared
4-core container, three runs each (two for Python; `bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.17 s |
| Rust (`rustc -O`) | 0.28 to 0.29 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.29 to 0.34 s |
| Go | 0.15 to 0.16 s |
| Python | 0.25 to 0.30 s |
| Kāra (`karac build`) | 0.18 to 0.22 s |
| Kāra (`karac build --mir`) | 0.49 to 0.54 s |

`bench.sh` is the `scripts/new-bench.sh` output as it stands: the legacy
`karac build` compiles this program. The `--mir` row is the v2 compiled
backend at kara `2b8238c108`, built by hand for comparison. Under `karac
__mir-llvm-run` the program prints the same line in 3.8 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

The bench is nearly all string building, and the v2 backend takes
2.5 times as long as legacy here. Under valgrind the `--mir` binary
makes 10.9 million allocations against Rust's 6.1 million and C's
3.3 million: an f-string is built in a buffer on a thread-local stack
and copied into a fresh `String` at the end, the lowering kara
B-2026-10-13-20 (open, filed from kata 504) describes for an integer
hole; here every hole is a string. Nothing new is filed.

## Compiler findings

None filed from this kata. The v2 f-string cost in the bench is kara
B-2026-10-13-20 (open), above.
