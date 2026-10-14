# 568. Maximum Vacation Days

LeetCode would like to give one of its best employees the option to
travel among `n` cities to collect algorithm problems. But all work and
no play makes Jack a dull boy, so you can take vacations in some
particular cities and weeks. Your job is to schedule the traveling to
maximize the number of vacation days you could take, under these rules:
you start in city 0 on Monday; the cities are connected by flights,
where `flights[i][j] == 1` means there is a flight from city i to city j
(and `flights[i][i] == 0`); you have `k` weeks to travel, can take a
flight at most once a day, and only on each week's Monday morning; for
each city you can only have restricted vacation days in different weeks,
given as `days[i][j]`, the most days you can take in city i in week j;
and you may stay in a city beyond its vacation days but must work on the
extra days. Given `flights` and `days`, return the maximum vacation days
you could take during `k` weeks.

```
flights = [[0,1,1],[1,0,1],[1,1,0]], days = [[1,3,1],[6,0,3],[3,3,3]]  ->  12
flights = [[0,0,0],[0,0,0],[0,0,0]], days = [[1,1,1],[7,7,7],[7,7,7]]  ->  3
flights = [[0,1,1],[1,0,1],[1,1,0]], days = [[7,0,0],[0,7,0],[0,0,7]]  ->  21
```

**Constraints:** `n == flights.length == flights[i].length ==
days.length`; `k == days[i].length`; `1 <= n, k <= 100`; `flights[i][j]`
is 0 or 1; `0 <= days[i][j] <= 7`.

## Approaches

Every arm is `fn max_vacation_days(flights: Vec[Vec[i64]], days:
Vec[Vec[i64]]) -> i64`.

| file | mechanism |
|---|---|
| `max_vacation_days.kara` ★ | forward over the weeks: `best[c]`, the most days so far ending the last week in city c, or -1 while c cannot be reached; each week's `best[j]` is that week's days in j plus the largest last `best[i]` over the cities i that are j or fly to j; O(k * n^2) |
| `max_vacation_days_memo.kara` | recursion, most(c, w) the most days from week w on starting it in city c, each (city, week) kept in a `Map[(i64, i64), i64]` once worked out |
| `max_vacation_days_backward.kara` | a table filled from the last week back, `table[w][c]` the most days from week w on starting it in c, for every city, reachable or not; the answer is `table[0][0]` |
| `max_vacation_days_lists.kara` | each city's destinations listed once, and the weeks walked forward over a `Vec[Option[i64]]`, `None` while a city cannot be reached; each reached city offers its total to each of its destinations |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 12 lines: eight tables at the edges (the three
LeetCode examples, one city and one week, a one-way chain whose last
city is reachable only from week 1, a detour where the best first week
costs more later, two cities flown between every week, and no days
anywhere), a total and checksum over 300 random tables of 1 to 6 cities
and 1 to 6 weeks with any number of flights, and the problem's largest,
100 cities and 100 weeks, with every flight, then one flight in fifty,
then a ring where each city flies only to the next.
`max_vacation_days.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: every itinerary tried, one city a week,
each week's city the last week's or one with a flight from it (city
0 before week 0), its days added up and the most kept. Each arm is held
to the properties below on 1,000 random tables of 1 to 4 cities and 1 to
4 weeks, days 0 to 7, each flight there with a chance from 0 to 100 in
100 drawn for the table.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | at least staying in city 0 every week gives, and at most the best city of each week |
| P3 | one more flight never gives fewer days |
| P4 | renaming the cities other than 0 changes nothing |
| P5 | one more day in every city and week gives k more |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac
__mir-llvm-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: staying in a city not allowed | P1 827, P2 724, P5 595 |
| M2 | ★: the answer read from city 0 only | P1 272 |
| M3 | memo: the memo read with the key the wrong way round | P1 28, P2 1, P3 1, P4 31, P5 3 |
| M4 | memo: city 0 never chosen for a week, not even to stay | P1 783, P2 661, P5 513 |
| M5 | backward: next week's total read for the city left | P1 92 |
| M6 | backward: the last week left out | P1 927, P2 750, P5 1000 |
| M7 | lists: the last city's total taken, not the largest | P1 268, P2 144, P3 29, P4 131 |
| M8 | lists: the week's days of the city left | P1 228 |
| E1 | ★: reached tested with `> -1` | 0 |
| E2 | memo: the most started at -1 | 0 |
| E3 | backward: the loop tested with `> -1` | 0 |
| E4 | lists: the larger taken the other way round | 0 |

P2's floor, staying in city 0 throughout, is what M1, M4 and M6 break:
M1 and M4 cannot stay in city 0, and M6 leaves the last week's days out,
so it fails P5 on every case, since it adds one day too few. M3 reads
the memo at (w, c) where it wrote (c, w), so it goes wrong only when the
two are both in the memo and differ, which is rare on 4 cities and
4 weeks; P4 sees it about as often as P1, since a renaming changes which
entries collide. M7 depends on which city is listed last, which a
renaming changes, so P4 sees it too. M2, M5 and M8 keep every property
but the definition: their answers stay within P2's bounds and move the
same way under more flights, renamed cities and one more day. P5 does
not see M7 either, since the last city's total also grows by k. E1 to
E3 are the same tests written another way; E2 is safe because staying is
always a choice, so the most is never below 0.

## Verification

The four arms print the same output as `max_vacation_days.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes on every arm, the differential and the bench program.

The frozen legacy backends: `karac run --interp` prints the right output
for the backward arm, and stops the ★ arm at `Option.cloned` ("method
'cloned' not found on type 'Option'"). `karac run` and `karac build`
refuse the ★ arm on the same `cloned`, and the backward arm at module
verification on the harness's `show` call ("Call parameter type does not
match function signature"). All three refuse the memo and lists arms and
the differential at type checking, on `*known` and `*d`, where legacy
gives the element as an `i64` and v2 as a reference. Legacy is frozen,
so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 random tables once, each
of 100 cities and 100 weeks (the problem's most), days 0 to 7, each
flight there with a chance of 1, 2, 5, 10, 25, 50 or 100 in 100 in turn;
then 30 times over every table is answered. Every implementation prints
`20 cases of 100 cities and 100 weeks, 30 rounds: 379740 days, checksum
295153059`, the Kāra program under `karac __mir-run` included (228 s).

Every implementation makes a fresh array for each week's `next`, as the
Kāra arm does; C's tables are rows of `malloc`'d arrays. Spot timings on
a shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.31 to 1.45 s |
| Rust (`rustc -O`) | 0.99 to 1.07 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.97 to 1.09 s |
| Go | 1.15 to 1.24 s |
| Python | 42.9 to 47.5 s |
| Kāra (`karac build --mir`) | 1.40 to 1.63 s |

The legacy `karac build` refuses this program, at passing the `ref`
bindings from `let (flights, days) = ref cases[(round * 7 + g) %
count];` to the arm ("expected 'Vec[Vec[i64]]', found 'ref
Vec[Vec[i64]]'"), where v2 parameters borrow. So `bench.sh` builds the
Kāra program with `karac build --mir`, the v2 compiled backend; that
edit is by hand, on top of the `scripts/new-bench.sh` output. The
`--mir` row is timed at kara `680733538b`. Under `karac __mir-llvm-run`
the program prints the same line in 5.3 s, compile included; that JITs
the MIR's IR without optimization passes, so it is not a benchmark.

The Kāra row is about 1.4 times Rust's, with or without Rust's overflow
checks, which cost Rust nothing measurable here. The cause of the gap is
not measured, nor why C is slower than Rust on this program.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
