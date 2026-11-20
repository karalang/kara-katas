# 2347. Best Poker Hand

You are given an integer array `ranks` and a character array `suits`.
You have `5` cards where the `i`th card has a rank of `ranks[i]` and a
suit of `suits[i]`.

The following are the types of **poker hands** you can make from best
to worst:

1. `"Flush"`: Five cards of the same suit.
2. `"Three of a Kind"`: Three cards of the same rank.
3. `"Pair"`: Two cards of the same rank.
4. `"High Card"`: Any single card.

Return *a string representing the **best** type of **poker hand** you
can make with the given cards.*

**Note** that the return values are **case-sensitive**.

```
ranks = [13,2,3,1,9],   suits = ["a","a","a","a","a"]  ->  "Flush"
ranks = [4,4,2,4,4],    suits = ["d","a","a","b","c"]  ->  "Three of a Kind"
ranks = [10,10,2,12,9], suits = ["a","b","c","a","d"]  ->  "Pair"
```

**Constraints:** `ranks.length == suits.length == 5`;
`1 <= ranks[i] <= 13`; `'a' <= suits[i] <= 'd'`; no two cards have the
same rank and suit.

A flush beats everything, so the suits are read first. Otherwise only
the most cards of one rank matters: three or four is three of a kind,
two is a pair, one a high card. Two pairs and a full house are pairs
and three of a kind here, as the list has no better name for them.

## Approaches

| file | mechanism |
|---|---|
| `poker.kara` ★ | a flush when every suit equals the first; otherwise the most cards of one rank, counted in a table of 14 as the ranks go by, names the hand |
| `poker_sorted.kara` | the suits sorted, a flush when the first equals the last; the ranks sorted, so equal ranks sit side by side and the longest run names the hand by `match` |
| `poker_map.kara` | the suits gathered in a `Set`, one suit a flush; the ranks counted in a `Map`, whose largest count names the hand, so the map's order never shows |
| `poker_naive.kara` | no table: every pair of suits compared, and each card's rank counted against all five, the largest count naming the hand |
| `poker_iter.kara` | iterators: a flush by `all` against the first suit; the most cards of one rank by `map` over the ranks to how many `filter` finds equal, and `max` |
| `poker_solution.kara` | LeetCode's Rust template: a flush by `all` with a `\|&s\|` pattern, the ranks counted in a `[0; 14]` array through `r as usize`, and the largest count matched against the range pattern `3..`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples; a high
card, a full house and two pairs; then 2000 random hands of five
different cards, their suits drawn from the first one to four letters
and their ranks from the first five to thirteen, with a checksum and
how many of each hand. Each arm returns a `String`; the harness reads
`suits` from a string literal through `chars().collect()`.
`poker.py` mirrors the ★ arm and its output is byte-identical, and the
mirror was checked against `collections.Counter` on 3000 random hands
dealt from the 52 cards.

`karac fix` carries the template in one call, reporting 11 edits.
`check` first reports 6 errors and offers 8 edits for them: the four
brackets of the two `Vec<..>`s; the `&` of the patterns `|&s|` and
`for &r` dropped; `in &ranks` to `in ref ranks`; and `String::from` to
`String.from`. The other three drop the `.to_string()` on the three
literals returned as a `String`, which a literal already is. The
`[0; 14]` array indexed by `r as usize`, `*cnt.iter().max().unwrap()`,
and the range pattern `3..` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a flush when all five suits are the same; otherwise three of
a kind when some three cards share a rank, tried over every three
places; otherwise a pair when some two do, over every two places;
otherwise a high card. No table and no sorting. It checks 300 random
hands drawn as the arms' harness draws them; then 30 of one suit; then
30 of two ranks. All 360 are drawn before any arm answers: 89 flushes,
35 three of a kind, 136 pairs and 100 high cards.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | one of the four names, and `"Flush"` exactly when no suit differs from the first |
| P3 | the cards reversed: the same answer |
| P4 | the second card's rank made the first card's, where their suits differ so the cards stay different: anything but `"High Card"` |
| P5 | the ranks made 1 to 5 and the suits kept: `"Flush"` when no suit differs from the first, and otherwise `"High Card"` |
| P6 | each arm agrees with at least three of the other five |

The first draft's P4 and P5 were relabellings, every rank `r` made
`14 - r` and every suit moved one letter on; every arm's answer is
blind to both, and so was every mutation, so neither killed any. They
were replaced by the two above, which change the answer in a known
direction.

The differential prints `360 cases: checksum 380155564, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same hands and tries every three and two places with
`itertools.combinations`. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: never a flush | P1 89, P2 89, P5 89, P6 89 |
| M4 | ★: the latest count kept, not the most | P1 72, P3 99, P4 129, P6 72 |
| M6 | ★: each card counted twice | P1 236, P5 271, P6 236 |
| M7 | sorted: the ranks left unsorted | P1 109, P6 109 |
| M8 | sorted: the suits left unsorted | P1 77, P2 77, P5 77, P6 77 |
| M11 | sorted: a pair named three of a kind | P1 136, P6 136 |
| M12 | map: a flush at two suits | P1 106, P2 106, P5 106, P6 106 |
| M14 | map: the least count read | P1 171, P4 169, P6 171 |
| M15 | map: a pair at one card | P1 100, P5 271, P6 100 |
| M18 | naive: a card not counted against itself | P1 167, P4 128, P6 167 |
| M19 | naive: the most kept as the least | P1 171, P4 185, P6 171 |
| M21 | naive: a pair read at one card | P1 236, P4 128, P5 271, P6 236 |
| M22 | iter: a flush when any suit is the first | P1 271, P2 271, P5 271, P6 271 |
| M23 | iter: the fifth suit never checked | P1 8, P2 8, P3 13, P5 8, P6 8 |
| M26 | iter: a pair named a high card | P1 136, P4 128, P6 136 |
| M27 | solution: three of a kind only from four | P1 31, P4 47, P6 31 |
| M31 | solution: the middle card's count read | P1 92, P4 139, P6 92 |

P1 and P6 kill all seventeen, P4 and P5 eight each, P2 five and P3
two. P2 fails only the edits to the flush: never one, the suits left
unsorted, a flush at two suits or whenever any suit is the first, the
fifth suit never checked. P5, five different ranks, fails all five
flush edits too, and the edits that name five different ranks something
other than a high card: each card counted twice, and a pair at one card
in the map and naive arms. P4, a pair made, fails the
edits that can lose a pair or a triple: the latest, least or middle
card's count read, a card not counted against itself, the most kept as
the least, a pair read at one card or named a high card, and three of
a kind only from four, which names a triple a high card. P3, the cards
reversed, fails only where an edit reads one end: the latest count kept
and the fifth suit never checked. A pair named three of a kind and the
ranks left unsorted are killed by P1 and P6 alone, since neither a made
pair nor five different ranks can tell them apart.

Of the thirty-one, fourteen were not kept. Never a flush in the ★ arm
(M1) fails as the template's flush when no suit is the first (M29); the
fifth suit never checked in the ★ (M2) and iter (M23) arms as the naive
arm's last suit never compared (M17); three of a kind only from four in
the ★ (M3), naive (M20) and template (M27) arms alike; a pair read as a
high card in the ★ arm (M5) as one named a high card in the iter arm
(M26) and the template (M30); each card counted twice in the ★ arm (M6)
as every count started at 1 in the map arm (M13) and every rank up to
it counted in the iter arm (M25); the longest run started at 2 in the
sorted arm (M10) as a pair at one card in the map arm (M15); the least
count read in the map arm (M14) as the fewest of a rank in the iter arm
(M24); and each rank counted once in the map arm (M16) and the template
(M28) as the most kept as the least in the naive arm (M19). Of each
group only one is kept, the one named in the table. The sorted arm's run
never reset (M9) fails apart from every kept one, and was left out to
keep three to the arm. The template's fifth edit was first every count
started at 1, which failed as M6, and was replaced by the middle card's
count read (M31).

## Verification

Every arm prints the same output as `poker.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.2 to 0.4 s, and the
differential 0.5 s there and 0.43 s under `karac __mir-llvm-run`.

## Benchmarks

The bench deals `10^5` hands once, five different cards of 52 each from
the harness's generator, any card already in the hand drawn again, and
then makes 30 passes, pass `p` folding each answer's length plus `p`
into the checksum, with the ★ arm in all five languages. About half the
hands are high cards, 47% pairs, 2.4% three of a kind and 0.2%
flushes. Every implementation prints `30 passes over 10^5 hands:
checksum 142111295`. Kāra and Rust return a `String` and count in a
heap table of 14 on every call; Go returns a `string` constant and
counts in a slice; C returns a static string and counts on the stack.

BENCHTAB
