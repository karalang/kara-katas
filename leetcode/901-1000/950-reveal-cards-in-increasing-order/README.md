# 950. Reveal Cards In Increasing Order

You are given an integer array `deck`. There is a deck of cards where
every card has a unique integer. The integer on the `i`-th card is
`deck[i]`.

You can order the deck in any order you want. Initially, all the cards
start face down (unrevealed) in one deck.

You will do the following steps repeatedly until all cards are revealed:

1. Take the top card of the deck, reveal it, and take it out of the deck.
2. If there are still cards in the deck then put the next top card of the
   deck at the bottom of the deck.
3. If there are still unrevealed cards, go back to step 1. Otherwise,
   stop.

Return *an ordering of the deck that would reveal the cards in
increasing order*.

**Note** that the first entry in the answer is considered to be the top
of the deck.

```
deck = [17,13,11,2,3,5,7]  ->  [2,13,3,11,5,17,7]
deck = [1,1000]            ->  [1,1000]
```

**Constraints:** `1 <= deck.length <= 1000`; `1 <= deck[i] <= 10^6`;
all the values of `deck` are unique.

## Approaches

| file | mechanism |
|---|---|
| `deck_revealed_increasing.kara` ★ | the reveals played on the deck's places rather than its cards: a queue holds the places 0 to `n - 1` from the top, and each step takes the top place, the next card revealed, and moves the place after it to the bottom. The `k`-th place taken is where the `k`-th smallest card goes. O(n log n) for the sort |
| `deck_revealed_increasing_backward.kara` | the reveals undone from the last: the largest card is the last one left, and before each card was revealed the card now at the bottom was on top of what remained. So, from the largest card down, the bottom card is moved to the top and the card put on top, in a double-ended queue. O(n log n) for the sort |
| `deck_revealed_increasing_walk.kara` | the places walked round again and again with the cards in increasing order: the next card goes in the next empty place, and the empty place after it is passed over, since its card is the one sent to the bottom. Each lap fills half the places still empty. O(n log n) |
| `deck_revealed_increasing_links.kara` | the empty places kept in a ring, each linked to the next: the next card goes in the current place, which is unlinked, and the place after it is passed over, the current place's predecessor carried along so that unlinking takes one step. O(n) after the sort |
| `deck_revealed_increasing_halves.kara` | the first pass down the deck reveals the places 0, 2, 4, ..., so they take the smallest half of the cards in order; what is left is a deck of its own, the odd places, with place 1 moved to the bottom when the deck is odd, since it was sent down just after the last even place was revealed. That deck is filled with the larger half the same way, recursively. O(n log n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's two examples and six more
(one card, two in falling order, 1 to 4, 1 to 5, 8 down to 1, and three
cards up to the largest value); for 300 random decks of 1 to 40 cards
from 1 to 100, 6,151 cards, a checksum of the answers; and four of
LeetCode's largest decks, 1,000 cards: random cards up to 1,000,000, 1
to 1,000 in order, 1,000,000 down to 999,001, and the multiples of 1,000
plus 1 in a scattered order, each with its first eight cards, its last
card and a checksum. `deck_revealed_increasing.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every ordering of the deck, made by swapping each card in
turn into each place, revealed by the statement's three steps, and the
orderings that reveal the cards in increasing order, with how many there
are. It checks 3,200 random decks of distinct cards: 3,000 of 1 to 6
cards from 1 to between the deck's size and 9 more, so that the cards
are close together, against the statement, and
200 of 1 to 1,000 cards from 1 to 1,000,000, against the other
properties; 111,338 cards.

| | property |
|---|---|
| P1 | the one ordering the statement's search finds, on the small decks |
| P2 | the deck's own cards, which the statement's steps reveal in increasing order |
| P3 | the deck shuffled gives the same answer |
| P4 | every card renamed, the new names in the same order as the old, gives the answer renamed |
| P5 | the even places hold the smallest half of the cards, in increasing order |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 decks of 111338 cards, checksum 253583299, 95000 checks
over 5 arms: 0 failures` under `karac __mir-run` (11 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the cards never sorted | P1 2101, P2 2301, P3 2316, P5 2274, P6 2301 |
| M2 | ★: each card placed one higher | P1 3000, P2 3200, P4 3200, P5 3200, P6 3200 |
| M3 | ★: no place sent down once two remain | P1 1986, P2 2185, P5 520, P6 2185 |
| M4 | backward: the top card moved to the bottom | P1 1466, P2 1665, P5 1665, P6 1665 |
| M5 | backward: the largest card left out | P1 3000, P2 3200, P5 3200, P6 3200 |
| M6 | backward: the moved card raised by one | P1 2474, P2 2674, P4 2674, P6 2674 |
| M7 | walk: a filled place passed over | P1 960, P2 1159, P6 1159 |
| M8 | walk: the walk going backwards | P1 1986, P2 2185, P5 1679, P6 2185 |
| M9 | walk: the last card never placed | P1 3000, P2 3200, P4 3200, P5 526, P6 3200 |
| M10 | links: the ring entered at the last place | P1 2474, P2 2674, P4 2154, P5 2674, P6 2674 |
| M11 | links: each place linked two on | P1 2474, P2 2674, P4 2674, P5 2674, P6 2674 |
| M12 | links: the first place its own predecessor | P1 1954, P2 2154, P4 2154, P5 2154, P6 2154 |
| M13 | halves: the rest turned when the deck is even | P1 1466, P2 1665, P6 1665 |
| M14 | halves: the rest never turned | P1 504, P2 701, P6 701 |
| M15 | halves: the last place copied to the bottom | P1 504, P2 701, P4 701, P6 701 |

P1, P2 and P6 kill all fifteen, P5 ten, P4 seven and P3 one.

P2 replays the statement's steps on the answer, so it fails exactly the
answers that are wrong, and kills everything P1 does, on the large decks
as well.

P3 kills only M1. Every arm sorts the cards first, so a mistake made
after the sort sees only the cards' ranks, and a shuffled deck has the
same ranks; M1 alone skips the sort.

P4 kills the seven that can put a card in the answer that the deck does
not hold, which has no new name, or a card changed in a way renaming does
not carry over: M2 and M6 add 1 to cards, M9 leaves
the last place at 0, and M15 writes one place twice and leaves another
at 0. M10, M11 and M12 start the ring with a predecessor that is not the
place before the first (M10 and M12 the first place itself, M11 the
wrong place in a ring linked two on), so a place can stay in the ring
after it is filled and be written again, leaving another at 0. The
other eight put the deck's own cards in the wrong places, the same wrong
places whatever the cards are called, so renaming carries their mistake
over unchanged.

P5 checks only the first pass. It misses M7, M13, M14 and M15, which go
wrong only after the first pass: M7's walk lets a filled place stand
for the place passed over, and filled places come only after the first
lap, and M13 to M15 change only the deck of odd places. M6 raises the
cards the backward arm moves, and the cards at the even places are
revealed in the first pass without ever going to the bottom, so they
are never moved. M3 fails P5 only for decks of three cards, the one
size where two places remain before the first pass is over, and M9 only for a
single card, whose last place is place 0.

Twenty-four other edits were tried and set aside. Twenty-one failed
exactly the same checks as each other, in four groups, so none of them
was kept. Eight fail every deck of three cards or more and no other
(★ putting the next place back on top and sending two places down,
backward leaving the bottom card at the bottom and moving it twice,
walk passing no place over, and links passing none, passing two and
never moving the predecessor on): one or two cards are revealed in the
order given whatever happens to the place after, and from three cards
each of these puts a wrong card at an even place. Nine fail every deck of two
cards or more (★ taking each place from the bottom, numbering the
places one on, sending a place down before the card is placed and
queueing the places from the last; backward moving after each card,
reading the deck from the bottom and putting each card at the bottom;
walk starting at place 1 and passing over the first place): each puts
a card other than the smallest on top. Two are the same edit in two
arms, ★ and walk passing a place over only after an even card, and two
the same mistake in two arms, walk never marking a filled place and
links never unlinking one. Two were sound but beyond three an arm: ★
passing a place over only after an even place, and halves dealing the
rest the same cards again. One crashed: halves filling the odd places
first, which for a single card hands the same one place on forever,
until the stack overflows.

## Verification

Every arm prints the same output as `deck_revealed_increasing.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are at kara
`086f304909`. Under `karac __mir-run` the arms take 0.2 s each
and the differential 11 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program builds 20 decks of 1,000 distinct random cards from 1
to 1,000,000 once, LeetCode's largest; in each of 1,000 rounds it runs
the ★ arm on every deck, each round starting from a different one, and
folds the last card of each answer into a total and one card of it,
chosen by the round, into a checksum. Every implementation prints `1000
rounds over 20 decks of 1000 cards: last cards adding to 18828800000,
checksum 399532663`. Each call copies and sorts the deck and queues the
places: C with `qsort` and a ring buffer, Rust with `sort` (stable) and
a `VecDeque`, Go with `slices.Sort` and a slice taken from the front and
appended to, Python with `sorted` and a `deque`, and Kāra with
`Vec.sort` and a `VecDeque`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 1.58 to 1.69 s | 1.63 s |
| Rust (`rustc -O`) | 0.30 to 0.37 s | 0.32 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.30 to 0.37 s | 0.33 s |
| Go | 1.19 to 1.35 s | 1.22 s |
| Python | 3.16 s | |
| Kāra (`karac build --mir`) | 0.32 to 0.36 s | 0.35 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 1.9 times
C's: its `sorted` is written in C and needs no comparison function
called through a pointer.

v2 takes 1.05 times Rust's median time under overflow checks and 0.21
times C's. Under valgrind's cachegrind v2 runs 4.26 billion
instructions and 0.61 billion branches with 12 million mispredicted,
Rust with overflow checks 3.55 billion, 0.49 billion and 23 million,
and C 6.67 billion, 0.99 billion and 111 million, 204 million of its
branches indirect: `qsort` calling its comparison function for every
comparison, as in kata 945. That the sort is most of each program's
time is inferred from those counts, not profiled.
