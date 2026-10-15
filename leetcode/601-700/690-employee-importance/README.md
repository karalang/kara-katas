# 690. Employee Importance

Each employee has a unique id, an importance value, and the ids of their
direct subordinates. Given the employees and an id, return the total
importance of that employee and of everyone under them, directly or not.

```
employees = [[1,5,[2,3]],[2,3,[]],[3,3,[]]], id = 1  ->  11
employees = [[1,2,[5]],[5,-3,[]]],           id = 5  ->  -3
```

**Constraints:** 1 <= `employees.length` <= 2000; 1 <= `id` <= 2000; ids
are unique; -100 <= importance <= 100; an employee has at most one
direct leader and any number of direct subordinates; `id` is an
employee's.

## Approaches

Every arm is `fn get_importance(employees: Vec[Employee], id: i64) ->
i64`, over `struct Employee { id: i64, importance: i64, subordinates:
Vec[i64] }`.

| file | mechanism |
|---|---|
| `employee_importance.kara` ★ | a map from id to place in the list, then a recursive sum of the employee and everyone under them; each person has at most one direct leader, so nobody is reached twice; O(n) |
| `employee_importance_bfs.kara` | ids run from 1 to 2000, so a `Vec` of 2,001 slots indexed by id finds each employee without hashing; a `VecDeque` from the given id, adding each one's importance and queueing their subordinates; O(n + 2000) |
| `employee_importance_stack.kara` | the recursive walk with an explicit stack of ids and a map, so a chain of 2,000 needs no deep recursion; O(n) |
| `employee_importance_leaders.kara` | each employee's direct leader recorded, then a climb from every employee through their leaders, counting them if it passes the given id; no list of subordinates is followed downward; O(n x depth) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 7 lines: the two LeetCode examples; one
employee alone; five employees with ids out of order and far apart, a
leader listed after the people under them and negative totals, asked
about four of them; a chain of 2,000, each the leader of the next, asked
about from its top, middle and bottom; one leader over 1,999 others; and
2,000 questions about 100 random companies of up to 300 people, ids
drawn from 1 to 2000 in random order, with a checksum.
`employee_importance.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: mark the given id,
then go over the whole list again and again, marking the subordinates of
everyone marked, until a pass marks no one new; the sum over everyone
marked. 1,200 random companies of 1 to 60 people are checked, ids drawn
from 1 to 2000 in random order, each person under one of the last one to
five people before them or, one time in eight, under no one, so the
trees run from flat to deep. One random person is asked about in each.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the same company listed in another order answers the same |
| P3 | the answer is the person's own importance plus each direct subordinate's answer |
| P4 | every importance negated negates the answer |

It prints `1200 companies, 4 arms, 19200 checks, 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each subordinate's total replacing those before it | P1 342, P3 196 |
| M2 | ★: a person's own importance left out | P1 1195, P3 1194 |
| M3 | bfs: importance counted without its sign | P1 904, P3 577, P4 1197 |
| M4 | bfs: direct subordinates only, not theirs | P1 575, P3 574 |
| M5 | stack: importance taken away, not added | P1 1195, P3 1194 |
| M6 | stack: only positive importance counted | P1 904, P3 577, P4 1197 |
| M7 | leaders: the climb stopping one leader short | P1 1195, P3 1194 |
| M8 | leaders: the given person's own importance left out | P1 1194, P3 1190 |
| E1 | ★: the map filled from the end of the list | 0 |
| E2 | bfs: unused slots 0, not -1 | 0 |
| E3 | stack: subordinates put at the bottom, not the top | 0 |
| E4 | leaders: the two tests of the climb swapped | 0 |

P1 and P3 kill all eight. P2 sees none: no arm reads the list by
position, only through ids, so its order changes nothing, a mutant's
included. P4 sees only M3 and M6, the two that treat negative and
positive importance unlike; the others stay linear in the importances,
so negating them negates their wrong answers too. M2 and M7 answer
0 whatever the company, M2 because it drops everyone's own importance
and M7 because its climb never lands on the given id, and M5 answers the
right total negated, so those three fail the same companies, the ones
whose answer is not 0. M3 and M6 also fail the same companies, the ones
whose tree holds a negative importance. The four survivors change no
answer: ids are unique, so the order the map is filled in does not
matter; every id asked about is in the list, so no slot is read before
it is set; a sum does not depend on the order people are visited in; and
`and` gives the same answer with its two tests either way round, since
neither has a side effect.

## Verification

Every arm prints the same output as `employee_importance.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`968707afd3` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives rebuilt after the last
`runtime/src` change.

The frozen legacy backends refuse all four arms, the differential and
the bench program at type checking, at the first `*s`, since legacy
gives the items of `e.subordinates.iter()` by value where v2 gives
references. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the breadth-first arm, the one that is the same
algorithm in all five languages; C has no map. It builds 30 companies of
2,000 people once, ids 1 to 2000 in random order, each person under a
random earlier one, with 100 random people to ask about in each, then
asks about all of them in each of 80 rounds, putting each answer into a
checksum. Every implementation prints `240000 questions answered,
checksum 852582164`, the Kāra program under `karac __mir-run` included
(in 110 s).

Each implementation is the same search: a freshly allocated table of
2,001 slots from id to place in the list, and a queue, which in C is a
ring buffer that doubles when full and in Go a slice taken from the
front. Spot timings on a shared 4-core container, six runs each, three
of them interleaved (two for Python; `bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.35 to 0.42 s |
| Rust (`rustc -O`) | 0.48 to 0.68 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.43 to 0.56 s |
| Go | 0.68 to 0.88 s |
| Python | 14.1 to 14.2 s |
| Kāra (`karac build --mir`) | 0.57 to 0.70 s |
| Kāra, legacy (`karac build`, a copy) | 0.51 to 0.68 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program at type checking, at `*s` as above and at
`get_importance(companies[c], ...)`, which moves an element out of
`companies` under legacy, where a bare parameter is owned, but
v2 borrows it. That edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside the kata that takes `ref
Vec[Employee]` and reads `push_back(s)` builds under legacy, and its row
is above. Under `karac __mir-llvm-run` the program prints the same line
in 3.7 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So the v2 build is level with legacy here, a little behind C and Rust,
and ahead of Go. The comparison with C and Rust waits until after M4.

## Compiler findings

None new. `karac check` first refused two lines, and both were changed
as its diagnostics said. `let e = employees[at[id]];` would move an
`Employee` out of the list, so it became `let e = ref
employees[at[id]];`; and the harness's `emp` helper gave away a bare, so
borrowed, `Vec[i64]` parameter, so it takes `subordinates: own
Vec[i64]`. Both are the programs' own mistakes, not the compiler's.
