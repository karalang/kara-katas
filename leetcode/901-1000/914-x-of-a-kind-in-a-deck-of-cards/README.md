# 914. X of a Kind in a Deck of Cards

You are given an integer array `deck` where `deck[i]` is the number
written on the `i`th card.

Partition the cards into one or more groups such that each group has
exactly `x` cards where `x > 1`, and all the cards in one group have the
same integer written on them. Return `true` if such a partition is
possible, or `false` otherwise.

```
deck = [1,2,3,4,4,3,2,1]  ->  true   ([1,1],[2,2],[3,3],[4,4])
deck = [1,1,1,2,2,2,3,3]  ->  false
```

**Constraints:** `1 <= deck.length <= 10^4` and `0 <= deck[i] < 10^4`.

## Approaches

Groups of `x` exist exactly when `x` divides every value's count, so the
question is whether the counts have a common divisor of at least 2.

| file | mechanism |
|---|---|
| `has_groups_size_x.kara` ★ | each value counted in a table as long as the largest value, the counts folded with Euclid's algorithm (recursive), and the result compared with 2. O(n + m) for the largest value m |
| `has_groups_size_x_sort.kara` | the deck sorted so each value's cards form one run, the run lengths folded with an iterative Euclid as each run ends. O(n log n), no table |
| `has_groups_size_x_tries.kara` | every group size x from 2 to n that divides n tried in turn against every count, the first that divides them all a partition |
| `has_groups_size_x_map.kara` | the counts in a `Map`, which holds only the values that occur, folded with Euclid in whatever order the map gives them |
| `has_groups_size_x_primes.kara` | the smallest count factored by trial division, and each of its primes tested against every count: a common divisor of at least 2 exists exactly when one of those primes divides them all |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples and five
more (one card, a pair, counts 3 and 6, the values 0 and 9,999, counts 5
and 3); for 600 random decks of up to 40 values in groups of 2 to 13,
half spoilt by one card, the number partitioned (317) and a checksum;
and three of LeetCode's largest, 10,000 cards in pairs, 9,991 cards as
97 values of 103 each, and 9,999 cards of which one differs.
`has_groups_size_x.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for each `x` from 2 to the deck's size, deal the cards into
groups by taking the first card left and looking for `x - 1` more of
the same value among the rest; `x` partitions the deck when every card
lands in a full group. It checks 3,200 random decks: 3,000 of up to 12
cards against the statement (half drawn at random over at most 4 values,
half built from groups of 2 to 4 over at most 5, some spoilt by one
card), and 200 of up to 3,333 cards, up to 40 values below 3, 100 or
1,000 in groups of 2 to 13, half spoilt, against the other properties;
153,493 cards in all, 1,388 decks partitioned.

| | property |
|---|---|
| P1 | some x > 1 deals the deck into groups as the statement says, on the small decks |
| P2 | the same answer for the deck shuffled again |
| P3 | the same answer with the values turned around, v renamed smallest + largest - v |
| P4 | the deck repeated two or three times can always be partitioned |
| P5 | when the deck can be partitioned, so can what is left after every card of one value is taken out |
| P6 | each arm agrees with at least two of the other four |

P5 holds because a common divisor of all the counts divides the counts
that remain. The large decks stop at 3,333 cards so that P4's three
copies stay within LeetCode's 10^4, and at values below 1,000 so that
the arms' tables stay small: with the values up to 10^4 and every arm's
table 10^4 long, the differential took more than 7 minutes under
`karac __mir-run` before it was stopped. It prints `3200 decks, 153493
cards, 1388 partitioned, 95000 checks over 5 arms: 0 failures` under
`karac __mir-run` (18 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a divisor of 1 accepted | P1 1721, P6 1812 |
| M2 | ★: each count rounded down to even | P1 1416, P5 204, P6 1507 |
| M3 | ★: groups of 2 refused | P1 390, P4 914, P6 405 |
| M4 | sort: a run ended only by a smaller card | P1 1558, P5 214, P6 1649 |
| M5 | sort: each run measured one card short | P1 787, P4 1951, P5 106, P6 883 |
| M6 | sort: a first run of one card never ended | P1 165, P3 153, P5 128, P6 165 |
| M7 | tries: the whole deck as one group never tried | P1 474, P4 163, P5 171, P6 476 |
| M8 | tries: only even group sizes tried | P1 454, P4 1157, P6 504 |
| M9 | tries: a count one past a multiple let through | P1 694, P5 383, P6 713 |
| M10 | map: neighbouring values counted together | P1 422, P3 150, P5 238, P6 426 |
| M11 | map: a value's first card counted twice | P1 808, P4 1752, P6 902 |
| M12 | map: Euclid's remainder halved | P1 669, P2 654, P4 529, P5 162, P6 768 |
| M13 | primes: the square of a prime taken for a prime | P1 16, P4 287, P5 1, P6 20 |
| M14 | primes: only even trial divisors | P4 165, P6 16 |
| M15 | primes: a last factor of 2 never tried | P1 374, P4 578, P6 380 |

P6 kills all fifteen and P1 fourteen; P4 and P5 nine each, P3 two and
P2 one. P1 misses M14 because a small deck's smallest count is at most
12, and trial division by 2, 4, 6, ... with the remainder taken as prime
once `p * p` passes it goes wrong only for a count like 9, whose 3 is
skipped and 9 itself tested: P4's tripled decks reach such counts. P3
sees the two mutants that care which values are neighbours (M6's first
run in sorted order, M10's pairing of v with v + 1), since turning the
values around changes both. P2 sees only M12: the halved remainder makes
the fold depend on the order of the counts, and a reshuffled deck
reaches the map in another order (inferred; M12's counts were the same
in two runs).

Two mutants were replaced, each because it failed exactly the same
checks as another and so told nothing new. The first M10 counted every
card twice, so every count was even and every deck partitioned, which
is M1's answer; the first M12 stopped Euclid at a remainder of 1, which
failed the same checks as M2.

## Verification

Every arm prints the same output as `has_groups_size_x.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 1.1 to 8.7 s
each (the primes arm the longest) and the differential 18 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The sort arm prints the same output under the frozen legacy interpreter,
the legacy JIT and both legacy builds, with and without auto-par. Legacy
refuses the other four arms, the differential and the bench program at
the first `*card` or `*c` on an element of a `Vec[i64]`'s `.iter()`:
"unary '*' requires 'ref T', 'mut ref T', or a raw pointer ..., found
'i64'". That is legacy's older rule; under v2 the element is a reference
and the `*` is required. Legacy is frozen, so none of this is filed.

## Benchmarks

The bench program uses the ★ arm on a deck of 9,996 cards, 1,666 values
six times each, built once. Each round rewrites one card to its own
value or one of the next two values used, asks the question, and puts
the card back; 20,000 rounds. Every implementation prints `20000 rounds
over 9996 cards: 6738 partitioned, checksum 312362102`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.51 to 0.58 s | 0.54 s |
| Rust (`rustc -O`) | 0.55 to 0.66 s | 0.61 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.56 to 0.69 s | 0.60 s |
| Go | 0.84 to 0.92 s | 0.89 s |
| Python | 23.2 s | |
| Kāra (`karac build --mir`) | 0.48 to 0.64 s | 0.56 s |

Legacy cannot build the bench program (above), so it has no row.
`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does.

v2 takes 0.93 times Rust's median time under overflow checks and 1.03
times C's. Under valgrind's cachegrind v2 runs 5.87 billion
instructions, against 7.19 billion for Rust with overflow checks and
5.52 billion for C. Nearly all the work is Euclid on a zero count, one
compare and return per value; C mispredicts 0.2 million branches, Rust
and v2 about 33 million each, which was not profiled.
