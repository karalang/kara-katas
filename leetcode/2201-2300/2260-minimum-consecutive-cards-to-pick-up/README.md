# 2260. Minimum Consecutive Cards to Pick Up

You are given an integer array `cards` where `cards[i]` represents the
**value** of the `i`th card. A pair of cards are **matching** if the
cards have the **same** value.

Return *the **minimum** number of **consecutive** cards you have to
pick up to have a pair of **matching** cards among the picked cards.*
If it is impossible to have matching cards, return `-1`.

```
cards = [3,4,2,3,4,7]  ->  4
cards = [1,0,5,3]      ->  -1
```

**Constraints:** `1 <= cards.length <= 10^5`; `0 <= cards[i] <= 10^6`.

The shortest run holding a matching pair has the pair at its two ends,
or it could lose a card from an end, and two cards of one value with no
third of that value between them are neighbouring occurrences. So the
answer is the smallest gap between neighbouring occurrences of a value,
plus one, and one pass that remembers where each value was last seen
finds it. O(n).

## Approaches

| file | mechanism |
|---|---|
| `cards.kara` ★ | a `Map[i64, i64]` from each value to where it was last seen, read by `if let Some(j) = last.get(..)` at every card, each repeat's run `i - j + 1` a candidate |
| `cards_array.kara` | no map: last positions in a `Vec.filled(top + 1, -1)` indexed by the card itself, `top` the largest card; the shortest run folded in by `min` from `i64.MAX` |
| `cards_window.kara` | a sliding window of distinct cards: a `Set` of the cards in `[lo, hi)`, and a repeat at `hi` gives up cards from the left until the earlier copy, whose run is the candidate, is gone |
| `cards_sort.kara` | the pairs `(card, position)` sorted, so each value's positions sit together in order; `windows(2)`, `into_iter`, `filter` to one value, `map` to the run, `min`, `unwrap_or(-1)` |
| `cards_struct.kara` | `struct Table` with the last positions in a `Map` and the shortest run in an `Option[i64]`; `deal` (`mut ref self`) uses the old value `Map.insert` returns, and a guarded `match` keeps the shorter run |
| `cards_solution.kara` | LeetCode's Rust template: `Vec<i32>` in, `i32` out; a `HashMap<i32, usize>`, `usize::MAX` for no pair yet, `Some(&j)` out of `last.get(&c)`, the run folded in by `min`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four
more (one card; a pair side by side; the pair at the two ends; two
pairs, the later one shorter), each with its answer; then 5000 hands of
1 to 30 cards with values below 5, 20, 100 or 1000 in turn, with how
many have no pair and a checksum; then four hands of the constraints'
most cards, 10^5: all different (-1); values to 10^6 at random (2);
every value of 0 to 49999 twice, 50000 apart (50001); and the first
card again at the very end (10^5). `cards.py` mirrors the ★ arm and its
output is byte-identical.

The array arm's `Vec` is as long as the largest card plus one. The
random hands keep their values below 1000 so that its 5000 hands do not
each fill a `Vec` of 10^6; the four long hands reach 10^6.

`karac fix` carries the template in one round of 18 edits: the `use
std::collections::HashMap;` line deleted, `Map` being in the prelude;
`Vec<i32>` to `Vec[i32]`, `HashMap<i32, usize>` to `Map[i32, i64]`,
`HashMap::new()` to `Map.new()`, both `usize::MAX` to `i64.MAX`, the
`&` dropped from `(i, &c)`, `Some(&j)` and `&c`, with `.cloned()` put on
the `get`, and `struct Solution;` to `struct Solution {}`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: runs of 2 cards, then 3, and so on, each run tried at every
start and every two cards in it compared, the first length with a
matching pair the answer. No map, no last positions. It checks 300
random hands of 1 to 30 cards with values below 2 to 40; then 30 of all
different cards; then 30 of all different cards but one pair. All 360
are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the hand reversed: the same answer |
| P3 | every card relabelled `7c + 3`: the same answer |
| P4 | the hand followed by itself: n + 1 if there was no pair, else no more than the answer and at least 2 |
| P5 | the first card dropped: still no pair if there was none, else no pair or no shorter a run |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 966913569, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that takes
the smallest gap over every two positions of equal cards. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the run counted without its ends | P1 271, P4 289, P6 271 |
| M5 | ★: the last card never dealt | P1 31, P2 53, P4 32, P6 31 |
| M6 | ★: the run one card short | P1 271, P4 245, P6 271 |
| M7 | array: no pair at position 0 | P1 30, P2 53, P4 33, P6 30 |
| M8 | array: cards paired with the next value | P1 78, P3 78, P6 78 |
| M9 | array: the run measured to the start | P1 222, P2 232, P5 186, P6 222 |
| M12 | window: the window not shrunk | P1 222, P2 187, P4 108, P5 88, P6 222 |
| M13 | window: the run measured from lo before it | P1 271, P4 89, P6 271 |
| M15 | window: a card added only when new | P1 94, P2 132, P5 13, P6 94 |
| M17 | sort: sorted by card only | P1 271, P4 360, P5 229, P6 271 |
| M19 | sort: neighbours of any value | P1 334, P2 307, P4 345, P5 301, P6 334 |
| M21 | sort: windows of three | P1 22, P2 5, P4 23, P6 22 |
| M23 | struct: the old position kept | P1 271, P4 360, P6 271 |
| M25 | struct: the first run kept | P1 105, P2 152, P5 22, P6 105 |
| M26 | struct: no answer reported as 0 | P1 89, P4 89, P5 20, P6 89 |
| M30 | solution: the cards cut to one byte | P1 150, P6 150 |
| M31 | solution: no pair reported as n | P1 89, P4 89, P5 80, P6 89 |

P1 and P6 kill all seventeen, P4 twelve, P2 and P5 eight each, and P3
one. P2 catches the edits that lean on one end of the hand: the
first position kept rather than the last, the last card never dealt, a
run measured from the start, a window that forgets cards. P3 fails only
the edit that files cards under their even neighbour (M8): relabelling
by `7c + 3` turns even into odd and changes which values share a slot.
P4 and P5 catch the edits that miscount a run or report no pair as a
number, since doubling the hand or dropping its first card moves the
answer in a known direction.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Twelve fail as a kept one does or as a group:
the longest run kept in the ★, sort, struct and template arms (M3, M20,
M22, M28) all alike; the first position kept in the ★, array and
template arms (M2, M10, M29) all alike; the ★ arm's first pair taken
(M4) as the struct arm's first run kept (M25); the array arm's no pair
reported as 0 (M11) as the struct arm's (M26); the sort arm's run
without its ends (M18) as the ★ arm's (M1); the struct arm's run
without its later end (M24) as the ★ arm's run one short (M6); and the
template's run counted from the start (M27) as the array arm's (M9).
Two fail in ways of their own and are left out because their arm keeps
enough: the window arm's one card given up per repeat (M14) and its
window dropping two at a time (M16). Two edits first written were
equivalent and replaced: an array-arm edit that still updated the last
position on every path, now M10, and the window arm's run checked at
every step of the shrink, now M14, which only adds longer runs than
the one it reaches.

## Verification

Every arm prints the same output as `cards.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, array and struct arms take 1.2 s, the
window arm 1.4 s, the template 2.0 s, the sort arm 4.2 s, and the
differential 1.1 s.

## Benchmarks

The bench answers 300 hands of 10^5 cards, their values below 10^6,
10^5 or 10^4 in turn, with the ★ arm in all five languages. Every
implementation prints `300 hands of 10^5 cards: checksum 61490925`.
The Rust, Go and Python mirrors use their standard hash maps; C has
none, so its mirror is an open-addressing table with linear probing,
sized to the next power of two above twice the hand and allocated per
hand.

BENCHTAB
