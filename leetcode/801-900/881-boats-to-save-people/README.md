# 881. Boats to Save People

You are given an array `people` where `people[i]` is the weight of the
`i`-th person, and an infinite number of boats where each boat can
carry a maximum weight of `limit`. Each boat carries at most two people
at the same time, provided the sum of the weight of those people is at
most `limit`. Return the minimum number of boats to carry every given
person.

```
people = [1,2], limit = 3  ->  1
people = [3,2,2,1], limit = 3  ->  3
people = [3,5,3,4], limit = 5  ->  4
```

**Constraints:** `1 <= people.length <= 5 * 10^4`,
`1 <= people[i] <= limit <= 3 * 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `num_rescue_boats.kara` ★ | sort, then two pointers: the heaviest person left takes the next boat, with the lightest one left if the two fit. If even the lightest cannot share with the heaviest, nobody can, and if the lightest can, pairing them leaves the rest no worse off. O(n log n) |
| `num_rescue_boats_counting.kara` | counting by weight: no one weighs more than `limit`, so the people are counted by weight and the same pairing runs over the weights from both ends. O(n + limit) |
| `num_rescue_boats_bestfit.kara` | the heaviest partner that fits: with the people sorted, the heaviest one left takes a boat with the heaviest other person they can carry, found by a binary search for the last weight that fits and a union-find step to the nearest person at or below it still waiting. O(n log n) |
| `num_rescue_boats_pairs.kara` | binary search on the pairs: the boats are n less the boats holding two, and p pairs can be formed exactly when the 2p lightest people can, lightest with heaviest, inward; that test only gets harder as p grows, so the largest p is found by binary search. O(n log n) |
| `num_rescue_boats_multiset.kara` | lightest first, from a multiset: a `SortedMap` from weight to how many weigh that; the lightest one left takes a boat with the heaviest other person who fits beside them, found with `floor`. O(n log n) as `SortedMap` is documented |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's three examples and seven
more (one person weighing the limit; five people of half the limit;
nine people who pair off to the limit but one; four who weigh more than
half of it; and 50,000 people, LeetCode's most, all of half the limit
30,000, all of the limit, and of every weight from 1 to 30,000 and then
1 to 20,000); the boats for 3,000 cases of 1 to 12 people, 13,619 in
all; and for 10 cases of 40,000 to 50,000 people with the limit up to
30,000, with a checksum. `num_rescue_boats.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way of putting the people into boats of one or two, the
first person without a boat going alone or with any other person without
one who fits beside them, and the fewest boats over all the ways. It
checks 3,040 cases: 3,000 of 1 to 10 people with the limit up to 20,
against the statement, and 40 of 1,000 to 2,000 people with the limit up
to 30,000, against the other properties. The ★ arm's boats sum to
44,110.

| | property |
|---|---|
| P1 | the statement's answer, on up to 10 people |
| P2 | at least half the people, rounded up, and at least one boat for each person heavier than half the limit; at most one boat each |
| P3 | the people in another order need the same boats |
| P4 | a higher limit never needs more boats, and with room for any two people the boats are half the people, rounded up |
| P5 | a person weighing the limit adds exactly one boat |
| P6 | each arm agrees with at least two of the other four |

P2, P3 and P6 are checked on every case, P4 and P5 on the first 3,000.
It prints `3040 cases, boats sum to 44110, 90600 checks over 5 arms: 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: two who fill the boat exactly kept apart | P1 748, P4 259, P6 756 |
| M2 | ★: the last person left when the pointers meet | P1 1947, P2 1146, P4 1530, P6 1969 |
| M3 | ★: the people left unsorted | P1 1110, P3 1039, P6 1150 |
| M4 | counting: two who fill the boat exactly kept apart | P1 748, P4 259, P6 756 |
| M5 | counting: the last person never taken as a partner | P1 1053, P4 1470, P6 1071 |
| M6 | counting: a pair one over the limit allowed | P1 974, P2 281, P5 350, P6 978 |
| M7 | best-fit: a partner exactly filling the boat passed over | P1 748, P4 259, P6 756 |
| M8 | best-fit: the partner left waiting | P1 2194, P4 2682, P6 2234 |
| M9 | best-fit: the first person in line taken as partner, fitting or not | P1 1908, P2 323, P4 2118, P5 318, P6 1948 |
| M10 | pairs: a pair exactly filling the boat refused | P1 748, P4 259, P6 756 |
| M11 | pairs: at most (n - 1) / 2 pairs searched for | P1 330, P4 1470, P5 330, P6 330 |
| M12 | pairs: only the outer pair checked | P1 435, P2 249, P6 474 |
| M13 | multiset: a partner exactly filling the boat passed over | P1 748, P4 259, P6 756 |
| M14 | multiset: everyone of a weight leaving at once | P1 1732, P2 1413, P4 1579, P5 1451, P6 1772 |
| M15 | multiset: a partner of the same weight passed over | P1 480, P4 640, P6 482 |

P1 and P6 kill all fifteen. M1, M4, M7, M10 and M13 are one fault in
all five arms, a pair whose weights add up to exactly the limit kept
apart, and fail the same cases, as the arms all compute the same count.
M5 and M11 fail P4 on the same 1,470 cases, the ones with an even
number of people: with room for any two, everyone can pair, and each
mutant loses the last pair. None of the
fifteen tried was equivalent or crashed, and none was replaced.

## Verification

Every arm prints the same output as `num_rescue_boats.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `89d76e3ff2` and the runtime
archives at `e903d5b111`, with no runtime change between them.

Under `karac __mir-run` four arms take 1 to 3 s each and the
differential 11 s. The multiset arm first took 378 s there: the MIR
interpreter copied and ordered every key of the map on each `floor` and
`ceiling` call, so the some 450,000 calls of the ten largest cases were
quadratic (kara `B-2026-10-23-1`, filed on kata 870; here 10,000 `floor`
calls on a map of 10,000 keys took 8.5 s under `__mir-run` against 0.4
s for as many `get` calls, and 20,000 took 36 s). Kara `35709d0045`
fixed that row, and on a release build at `fe44986b7e` the arm prints
the same output in 7 s. The differential keeps its large cases to 2,000
people so that it runs in seconds there.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends (its interpreter and JIT, and `karac build
--legacy` with and without auto-par) print the same output for the ★,
counting, best-fit and pairs arms. They refuse the multiset arm and the
differential at the `*` on the value a `SortedMap.get` match binds,
saying the value is not a reference, where v2 binds a reference. Legacy
is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 600 cases of
40,000 to 50,000 people with the limit up to 30,000, drawn from the same
generator in each language as they are solved, each sorting its own
copy of the weights. The sort is each language's own: Kāra's `sort` on a
`Vec` of integers, which `karac build --mir` lowers to Rust's
`sort_unstable`; Rust's `sort_unstable`, to match; Go's `slices.Sort`;
Python's `sorted`; and C's `qsort`. Every implementation prints `600
cases of up to 50000 people: 13442247 boats, checksum 417301215`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 2.81 to 2.97 s | 2.92 s |
| Rust (`rustc -O`) | 0.46 to 0.51 s | 0.49 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.45 to 0.49 s | 0.47 s |
| Go | 2.22 to 2.31 s | 2.26 s |
| Python | 18.9 s | |
| Kāra (`karac build --mir`) | 0.51 to 0.55 s | 0.52 s |
| Kāra legacy (`karac build --legacy`) | 0.47 to 0.52 s | 0.49 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 880's does.

The sort sets most of the time, so this compares sorts more than the
two-pointer walk. v2 takes 1.12 times Rust's median time under overflow
checks, 1.05 times legacy's, 0.18 times C's and 0.23 times Go's. Under
valgrind's cachegrind C runs 12.5 billion instructions, most of them
most likely in `qsort` and its comparison called through a function
pointer (inferred from the other counts, not profiled), Rust with
overflow checks 4.96 billion, legacy 4.63 billion and v2 5.01 billion.
Go's `slices.Sort` most likely accounts for its time the same way
(also inferred). The comparison with C and Rust waits until
after M4.
