# 1029. Two City Scheduling

A company is planning to interview `2n` people. Given the array `costs`
where `costs[i] = [aCost, bCost]`, the cost of flying the `i`th person
to city a is `aCost` and to city b is `bCost`. Return the minimum cost
to fly every person to a city such that exactly `n` people arrive in
each city.

```
costs = [[10,20],[30,200],[400,50],[30,20]]                                  ->  110
costs = [[259,770],[448,54],[926,667],[184,139],[840,118],[577,469]]          -> 1859
costs = [[515,563],[451,713],[537,709],[343,819],[855,779],[457,60],[650,359],[631,42]]  -> 3086
```

**Constraints:** `costs.length` is even, from 2 to 100; every cost is
from 1 to 1,000.

## Approaches

Everyone pays the fare to b and the people sent to a pay `a - b` on top,
so the cheapest choice sends to a the `n` people with the smallest
`a - b`.

| file | mechanism |
|---|---|
| `two_city.kara` ★ | sorted by the saving: clone the list, `sort_by_key` on `a - b`, send the first half to a and the rest to b. O(n log n) |
| `two_city_dp.kara` | a table of the cheapest: `cheapest[i][j]` is the least cost of the first `i` people with `j` of them in a, the `i`th going to a after `j - 1` others did or to b after `j` did, with `i64.MAX` for a count no choice reaches. O(n^2) |
| `two_city_memo.kara` | recursion with a memo: from person `i` on, with so many places left in a and the rest in b, the cheaper of the person's fare to a city with room plus the least cost of the rest, each state kept in a `Map` keyed by a tuple. O(n^2) |
| `two_city_buckets.kara` | counting the savings: costs run from 1 to 1,000, so `a - b` lies in -999 to 999; count the people at each difference, charge everyone the fare to b, and hand out the `n` places in a from the smallest difference up. No sort. O(n + 1999) |
| `two_city_swaps.kara` | swapping until nothing helps: start with the first half in a, and swap a person in a with one in b whenever that costs less, until no swap does; then everyone in a saves at least as much as anyone in b, which is the sorted answer. O(n^3) at worst |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 15 lines: the answers for seven lists,
LeetCode's three examples among them; for six groups of random lists
(2,000 of 2 people down to 20 of 100, with costs up to 3 to 1,000), the
sum of the answers and a checksum; and the answers for 100 people for
whom a is always cheaper by 499, and for 100 people whose every cost is
1,000. `two_city.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: of every way to send exactly half the people to a, picked
out by the bits of a mask, the cheapest. It checks 1,352 lists: every
list of 2 people with costs from 1 to 4 (256) and of 4 people with costs
1 or 2 (256), then 800 random lists of 2 to 10 people and 40 of 12 to
100, with costs up to 3, 20 or 950. The 1,312 lists of at most 10
people are searched in full. Each list is also asked in the opposite
order, with every person's two costs swapped, with every cost raised by
a random amount from 1 to 50, and with one random cost of one random
person raised by such an amount.

| | property |
|---|---|
| P1 | the statement read literally, on the lists of at most 10 people |
| P2 | the order of the people does not matter |
| P3 | with every person's two costs swapped, the answer does not change, since half go to each city |
| P4 | with every cost raised by `k`, the answer rises by `k` for every person |
| P5 | with one cost raised by `k`, the answer rises by 0 to `k` |
| P6 | each arm agrees with at least two of the other four |

The differential prints `1352 cases (1312 searched in full): checksum
762017811, 40360 checks over 5 arms: 0 failures` under `karac __mir-run`
(9.7 s) and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Thirty edits to the differential, each run under `karac __mir-run` and
`karac __mir-llvm-run`; fifteen are kept, three to each arm, all fifteen
are killed, each fails the same checks under both, and no two kept ones
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: sorted by the fare to a alone | P1 531, P2 287, P3 845, P5 47, P6 571 |
| M2 | ★: never sorted | P1 933, P2 1203, P3 1203, P6 973 |
| M3 | ★: the last person never paid for | P1 1312, P2 110, P3 901, P4 1352, P5 129, P6 1352 |
| M4 | dp: going to a charged the fare to b | P1 1142, P3 1187, P6 1182 |
| M5 | dp: the answer read with one fewer in a | P1 929, P3 1043, P6 947 |
| M6 | dp: nobody in a never filled | P1 561, P2 967, P3 1115, P6 572 |
| M7 | memo: one more kept than found | P1 658, P2 439, P3 632, P6 698 |
| M8 | memo: one place too many in b | P1 243, P3 491, P6 252 |
| M9 | memo: a place in a never used up | P1 866, P2 985, P3 1122, P6 906 |
| M10 | buckets: the saving counted the wrong way | P1 1150, P3 1187, P5 863, P6 1187 |
| M11 | buckets: the saving added, not taken off | P1 1142, P3 1187, P5 868, P6 1182 |
| M12 | buckets: a whole bucket taken | P1 120, P3 127, P5 54, P6 127 |
| M13 | swaps: one pass only | P1 196, P2 345, P3 346, P5 9, P6 233 |
| M14 | swaps: the person from b never moved | P1 828, P2 1070, P3 1095, P5 152, P6 868 |
| M15 | swaps: only later people swapped in | P1 271, P2 422, P3 411, P5 21, P6 307 |

P1, P3 and P6 kill all fifteen, P2 nine, P5 eight and P4 one. P3, which
swaps the cities, sees every edit, since each treats a and b
differently. P2 sees the nine whose answer changes with the
order the people come in, among them the unsorted list (M2), the sort
whose ties fall in the order given (M1), the person left unpaid
being whoever sorts last, which among ties is set by the order given
(M3), and swaps that stop early (M13). P4 sees only M3: raising every cost by `k` raises any choice
of one fare per person by `k` for each person, so every other edit,
which still pays one fare per person, moves with it, while M3 pays for
one person fewer. The checks draw random numbers for every list whatever
the answers, so every mutant sees the same lists and their counts can be
compared.

Fifteen other edits were tried and set aside. One changes no answer
here, and it is a gap in the cases rather than an equivalent edit:
buckets starting its walk at a difference of -998, skipping -999, which
needs a fare of 1 to a and 1,000 to b, a pair no list checked holds.
Three dp edits stop on an integer overflow panic (exit 101): keeping
the dearer way and never placing the last person both answer
`i64.MAX`, and P4's check overflows adding to it; adding to an entry no
choice reaches overflows in the arm itself. The other eleven were killed
too, beyond three per arm. Four answer the dearest choice and fail
exactly alike: ★ sorting by what going to a costs extra, ★ and swaps
charging the fares the wrong way round, and swaps making a swap that
costs more. ★ sending one person too many to a, memo starting with one
place too many in a and swaps starting with one person too many in a
fail alike; buckets using one place per difference fails as M4; and
memo letting a full city a take people, memo charging the fare to a for
going to b and buckets charging everyone the fare to a first fail on
their own.

## Verification

Every arm prints the same output as `two_city.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error; the differential prints its line under all three. `karac check
--output=json` reports no diagnostic for the five arms, the differential
and the bench program, so `karac fix` had nothing to do. `karac run` and
a `karac build` binary print the same output for every arm and the
differential. The release build is kara `56c60bdf7c`, with runtime
archives rebuilt at `ce706dd131`, the last commit before it to change
the runtime. Under `karac __mir-run` the arms take 0.4 s (★) to 2.5 s (buckets). No
compiler gap turned up.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench builds 1,000 random lists of 100 people (LeetCode's largest),
with costs from 1 to 1,000, once in all five languages, and answers
each list 100 times with the ★ arm, folding the answers into a sum and
a checksum. Every call copies the list before sorting it, as Kāra's
`costs.clone()` does: a deep copy of a `Vec` of `Vec`s in Kāra and Rust
(`to_vec`) and in Python, a copy of the outer slice in Go, and one
`malloc`'d array of pairs in C. Rust and Python sort stably with their
own sorts, Go with `sort.SliceStable` and C with `qsort`; the answer does
not depend on how ties fall. Every implementation prints `1000 cases of
100 people, 100 rounds: sum 3328740100, checksum 240874372`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.661 to 0.837 s | 0.700 s |
| Rust (`rustc -O`) | 0.719 to 1.040 s | 0.820 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.743 to 1.047 s | 0.837 s |
| Go | 2.443 to 2.943 s | 2.603 s |
| Python | 3.0 s | |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.863 to 1.052 s | 0.964 s |
| Kāra (`karac build`) | 0.911 to 1.089 s | 1.022 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(its user time stays below its real time) and runs as fast as the
sequential one.

v2 took 1.15 times Rust's median time under overflow checks and 1.38
times C's. Go took 3.7 times C's, nearly as long as Python, whose sort
runs in C; Go's `sort.SliceStable` calls a closure for every comparison
and swaps through a function it builds by reflection, but we did not
measure how much of Go's time that is, nor where Kāra's gap to C goes.
