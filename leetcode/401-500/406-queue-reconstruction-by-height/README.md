# 406. Queue Reconstruction by Height

People stand in a queue. Each is described by `(h, k)`: their height
`h`, and the number `k` of people in front of them whose height is `h`
or more. Given the people in any order, reconstruct the queue.

```
people = [[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]
      -> [[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]
```

**Constraints:** `1 <= people.length <= 2000`; `0 <= h <= 10^6`;
`0 <= k < people.length`. The input always describes a queue, and that
queue is unique.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `queue_reconstruction.kara` ★ | tallest first: sort by height descending, then `k` ascending, and insert each person at index `k`; everyone already placed is at least as tall, and the shorter people placed later do not count | O(n^2) | O(n) |
| `queue_reconstruction_slots.kara` | shortest first: sort by height ascending, then `k` descending, and put each person in the (k + 1)th empty slot; everyone placed later is at least as tall, so the empty slots in front are exactly the people they count | O(n^2) | O(n) |
| `queue_reconstruction_fenwick.kara` | the slots arm with the (k + 1)th empty slot found by descending a Fenwick tree of empty slots | O(n log n) | O(n) |
| `queue_reconstruction_front.kara` | build the queue from the front: the next person is the shortest whose `k` equals the number of people already placed who are at least as tall, kept per person and updated after each placement | O(n^2) | O(n) |
| `differential.kara` | the four arms on 3,000 random cases whose answers are known by construction, five properties | — | — |

Every arm prints the same 9 lines: the two LeetCode examples, six edge
cases (no people, one person, three of one height, rising and falling
queues, two pairs of equal heights), and for 2,000 random queues of 1
to 50 people with heights from 1 to 20, each person's `k` counted from
the queue and the people shuffled, how many are rebuilt exactly and a
checksum. `queue_reconstruction.py` mirrors the ★ arm and its output is
byte-identical.

The three sorting arms take `people: own Vec[(i64, i64)]` and rebind it
with `let mut people = people;` before sorting it in place, as
design.md shows for an owned parameter that is mutated.

## Differential

`differential.kara` holds copies of the four arms. Each of 3,000 random
cases makes a queue of 0 to 40 people with heights from 1 to 12, counts
each person's `k` from it, and shuffles it twice:

| | property |
|---|---|
| P1 | the people, shuffled, rebuild that queue exactly |
| P2 | the output holds the same people as the input |
| P3 | in the output, each person's `k` is the number of earlier people of their height or more |
| P4 | two shuffles of the same people give the same output |
| P5 | people of one height come out in order of `k`, and people with `k` = 0 and distinct heights come out shortest first |

It prints `3000 cases, 4 arms, 60000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
Seven are killed by a property and one stops the differential.

| # | mutation | failures by property |
|---|---|---|
| M1 | tallest: each person joins the back instead of index `k` | P1 2795, P3 2795, P5 2848 |
| M2 | slots: a person takes the `k`th empty slot, not the (k + 1)th | P1 2818, P3 2818, P5 2848 |
| M3 | slots: filled slots are counted with the empty ones | P1 2647, P3 2647 |
| M4 | fenwick: the descent stops short of a prefix holding exactly `k` empty slots | P1 2861, P2 2861, P3 2861, P5 2848 |
| M5 | fenwick: a filled slot stays counted as empty | P1 2795, P2 2795, P3 2795, P5 2848 |
| M6 | fenwick: the descent starts one power of two too low | P1 2535, P2 2535, P3 2535, P5 2212 |
| M7 | front: the tallest candidate is placed | panics: index out of bounds |
| M8 | tallest: each person goes in at half their `k` | P1 2818, P3 2818, P5 2848 |

No arm can fail P4: each sorts its input, or picks people by a rule
that does not depend on their order, so P4 is kept to guard the arms
against an order dependence a later change might add. The fenwick
mutants also fail P2, because a wrong slot overwrites a person who was
already placed. M7 stops the differential: every mistake in the front
arm makes some person's count pass their `k`, so no candidate is left
and the arm reads index -1. A second front mutant (people of equal
height not counted) stopped the same way, as did a first M3 (equal
heights placed smallest `k` first), a first M6 (the Fenwick tree built
without carrying counts upward) and a fenwick mutant that never reduced
`k`, which writes one past the end of the queue; each was replaced by a
mutation a property can see. M2 and M8 differ in mechanism and fail the
same checks.

## Verification

All four arms print the same output as `queue_reconstruction.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints `60000
checks, 0 failures` under both. The front arm also matches under
`karac run --interp`, LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac
build`. The frozen legacy typechecker refuses the other three and the
differential: it refuses `*p` on the items of `people.iter()`, as in
katas 382 to 403. Not filed.

## Benchmarks

The bench program uses the ★ arm on 1,000 random queues of 2,000
people (the problem's limit) with heights from 1 to 50, each person's
`k` counted from the queue, shuffled and rebuilt. It counts the queues
rebuilt exactly and folds them into a checksum. Every implementation
prints `1000 queues of 2000 people: 1000 rebuilt, checksum 882767420`;
a 5-queue cut of the Kāra program under `karac __mir-run` prints the
same as the C program cut the same way. C has no library stable sort,
so its mirror carries a merge sort; its inserts use `memmove`. Spot
timings on a shared 4-core container (`bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| Rust (`rustc -O`) | 0.27 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.30 s |
| C (`clang -O3`) | 0.43 s |
| Go | 1.6 s |
| Python | 4.5 s |

The Kāra program prints
the same line under `karac __mir-llvm-run` in 2.3 s, compile included;
that JITs the MIR's IR without optimization passes, so it is not a
benchmark. The legacy `karac build` refuses it, as above.

## Compiler findings

No new findings.
