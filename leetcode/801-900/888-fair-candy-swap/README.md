# 888. Fair Candy Swap

Alice and Bob have a different total number of candies. You are given
two integer arrays `aliceSizes` and `bobSizes` where `aliceSizes[i]` is
the number of candies of the `i`th box of candy that Alice has and
`bobSizes[j]` is the number of candies of the `j`th box of candy that
Bob has. Since they are friends, they would like to exchange one candy
box each so that after the exchange, they both have the same total
amount of candy. The total amount of candy a person has is the sum of
the number of candies in each box they have. Return an integer array
`answer` where `answer[0]` is the number of candies in the box that
Alice must exchange, and `answer[1]` is the number of candies in the box
that Bob must exchange. If there are multiple answers, you may return
any one of them. It is guaranteed that at least one answer exists.

```
aliceSizes = [1,1], bobSizes = [2,2]  ->  [1,2]
aliceSizes = [1,2], bobSizes = [2,3]  ->  [1,2]
aliceSizes = [2], bobSizes = [1,3]  ->  [2,3]
```

**Constraints:** `1 <= aliceSizes.length, bobSizes.length <= 10^4`,
`1 <= aliceSizes[i], bobSizes[j] <= 10^5`, Alice and Bob have a
different total number of candies, and there will be at least one valid
answer for the given input.

## Approaches

Swapping Alice's box x for Bob's box y evens the totals exactly when y -
x = d, half of Bob's total less Alice's. LeetCode accepts any such swap;
every arm returns the one in which Alice gives her smallest box, so that
all five print the same, which is also what LeetCode's second example
shows.

| file | mechanism |
|---|---|
| `fair_candy_swap.kara` ★ | a set of Bob's boxes: Bob's boxes go in a `Set`, and each of Alice's boxes x is looked up as x + d, the smallest x found kept. O(n + m) |
| `fair_candy_swap_sorted.kara` | two pointers over the sorted boxes: both lists sorted, a gap from Alice's box to Bob's below d moves Bob's pointer up and one above d moves Alice's, and the first gap of exactly d is the swap. O(n log n + m log m) |
| `fair_candy_swap_search.kara` | a binary search in Bob's sorted boxes: both lists sorted, and for each of Alice's boxes from the smallest up, x + d looked for among Bob's by binary search. O((n + m) log m) |
| `fair_candy_swap_counting.kara` | a table of the box sizes: which sizes Alice has and which Bob has marked in two tables up to the largest box, and the sizes walked from 1 up. O(n + m + the largest box) |
| `fair_candy_swap_ordered.kara` | ordered sets of the boxes: Alice's boxes in a `SortedSet`, walked from the smallest up with each size once, and each looked up as x + d in a `SortedSet` of Bob's. O((n + m) log(n + m)) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more (Alice giving her largest box; two lists where Alice could give
either box, and the larger is first; boxes of 10^5 candies with two
swaps that work; and boxes repeated on both sides); the sizes of the
boxes swapped in 3,000 cases of up to 6 boxes of up to 12 candies each;
and in 30 cases of up to 10^4 boxes of up to 10^5 candies, with a
checksum. Each case is built with a swap that evens it: Alice's box i
and Bob's box j are picked, Bob's box j given a size at random, and
then Bob's other boxes and Alice's other boxes nudged, within 1 to the
largest size, until the totals differ by twice the gap.
`fair_candy_swap.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every box of Alice's swapped with every box of Bob's, the
totals compared after each swap, and of the swaps that even them the
one in which Alice gives her smallest box. It checks 3,040 cases: 3,000
of up to 6 boxes of up to 12 candies against the statement, and 40 of
up to 2,000 boxes of up to 10^5 candies against the other properties,
with Alice and Bob given as many boxes each in a third of all cases. In
848 of the cases more than one size of Alice's box would do.

| | property |
|---|---|
| P1 | the statement's swap, on up to 6 boxes |
| P2 | one of Alice's boxes and one of Bob's, the swap evening the totals; and the same with Alice and Bob exchanged |
| P3 | the same boxes in another order |
| P4 | none of Alice's smaller boxes would do |
| P5 | every box doubled doubles the swap, and with as many boxes each, every box a candy more adds a candy to both sides of it |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every case. It prints `3040 cases, 848 with a
choice of swaps, Alice gives 1294609 candies and Bob 1452742, 91000
checks over 5 arms: 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the whole difference taken, not half | P1 3000, P2 3040, P4 311, P5 2362, P6 3040 |
| M2 | ★: Alice's largest box kept, not her smallest | P1 823, P4 848, P6 848 |
| M3 | ★: Bob's box read the wrong way from Alice's | P1 3000, P2 3040, P6 3040 |
| M4 | sorted: the pointers moved the wrong way | P1 2522, P2 2562, P5 2562, P6 2562 |
| M5 | sorted: Alice's boxes left unsorted | P1 987, P2 993, P3 863, P4 409, P5 614, P6 1023 |
| M6 | sorted: Alice's last box never tried | P1 1128, P2 1274, P5 1128, P6 1128 |
| M7 | search: the search landing past the box it looks for | P1 3000, P2 3040, P5 3040, P6 3040 |
| M8 | search: the box looked for d below Alice's | P1 3000, P2 3040, P4 348, P5 2207, P6 3040 |
| M9 | search: Bob's largest box never matched | P1 1072, P2 1274, P5 1072, P6 1072 |
| M10 | counting: the largest size never tried | P1 614, P2 1347, P5 614, P6 614 |
| M11 | counting: Bob's box of the largest size never matched | P1 733, P2 1347, P5 733, P6 733 |
| M12 | counting: Alice's sizes marked in Bob's table | P1 3000, P2 3040, P5 3040, P6 3040 |
| M13 | ordered: Alice's total added, not taken away | P1 3000, P2 3040, P5 3040, P6 3040 |
| M14 | ordered: Bob's boxes put in Alice's set | P1 3000, P2 3040, P5 3040, P6 3040 |
| M15 | ordered: the two boxes returned the wrong way round | P1 3000, P2 3040, P4 1603, P6 3040 |

P1 and P6 kill all fifteen. M2 fails 848 cases under P4 and P6, as many
as give Alice a choice of box; it is the only
mutant that still returns a swap that evens the totals, which is why P2
misses it. P3 kills only M5, as only an arm that depends on the order of
the lists can change with it. One mutant was replaced: in the search
arm, a search never reaching past Bob's second-largest box still finds
the largest, since a search that ends there checks that box anyway, so
it is equivalent; it was replaced by M9, which never accepts a match on
the largest box.

## Verification

Every arm prints the same output as `fair_candy_swap.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 0.8 to 1.2 s
each and the differential 7 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends refuse every arm, the differential and the
bench program. For the ★, sorted, search and counting arms and the bench
it is the harness passing `boxes[0]`, a list held in a `Vec`, to a
parameter that only borrows it: legacy predates borrowed parameters and
reports `cannot move boxes[0] out of an index`. For the ordered arm and
the differential it is `*size`, reading a `SortedSet`'s element through
the reference its iterator gives, where legacy yields the value itself.
Legacy is frozen, so neither is filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 2,000 cases of
5,000 to 10^4 boxes each for Alice and for Bob, up to 10^5 candies a
box, built as the arms' harness builds its cases. Bob's boxes go in a
`Set` in Kāra (SipHash-1-3), a `HashSet` in Rust (SipHash-1-3), a map
in Go and a set in Python; C has no set, so it uses an open-addressing
table of 32,768 slots with linear probing and a multiplicative hash,
cleared for each case. Every implementation prints `2000 cases of 5000
to 10000 boxes: Alice gives 32708381 candies, Bob 36155536, checksum
901861687`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.23 to 0.26 s | 0.25 s |
| Rust (`rustc -O`) | 0.71 to 0.80 s | 0.75 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.71 to 0.84 s | 0.76 s |
| Go | 1.66 to 2.08 s | 1.87 s |
| Python | 18.9 s | |
| Kāra (`karac build --mir`) | 0.76 to 0.86 s | 0.82 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 887's does. Legacy refuses the bench program
(above), so it has no row.

v2 takes 1.08 times Rust's median time under overflow checks and 3.31
times C's. Under valgrind's cachegrind C runs 1.98 billion
instructions, Rust with overflow checks 6.80 billion and v2 8.14
billion. Kāra and Rust both hash every box with SipHash, keyed per
process, where C multiplies once; that most likely accounts for most of
C's lead (inferred from the hashes used and the counts, not profiled).
The comparison with C and Rust waits until after M4.
