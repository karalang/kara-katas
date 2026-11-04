# 1046. Last Stone Weight

You are given an array of integers `stones` where `stones[i]` is the
weight of the `i`th stone.

We are playing a game with the stones. On each turn, we choose the
**heaviest two stones** and smash them together. Suppose the heaviest
two stones have weights `x` and `y` with `x <= y`. The result of this
smash is:

- If `x == y`, both stones are destroyed, and
- If `x != y`, the stone of weight `x` is destroyed, and the stone of
  weight `y` has new weight `y - x`.

At the end of the game, there is **at most one** stone left.

Return the weight of the last remaining stone. If there are no stones
left, return `0`.

```
stones = [2,7,4,1,8,1]   ->  1   (8,7 -> 1; 4,2 -> 2; 2,1 -> 1; 1,1 -> 0; 1 is left)
stones = [1]             ->  1
```

**Constraints:** `1 <= stones.length <= 30`; `1 <= stones[i] <= 1000`.

## Approaches

Every arm plays the game as the statement says. They differ in how
they find the two heaviest stones each turn.

| file | mechanism |
|---|---|
| `last_stone.kara` ★ | a largest-first `PriorityQueue`, built from the pile in O(n): pop two, push their difference back if it is not zero. O(n log n) |
| `last_stone_sorted.kara` | the pile kept in ascending order, the two heaviest popped off the end, and the difference put back at its place, found by binary search, with `insert`. O(n) a turn |
| `last_stone_count.kara` | a count of the stones of each weight, which the bound of 1000 makes small, and a cursor walking down from the heaviest: an even count smashes to nothing, and a lone stone is smashed against the next weight down that has one. O(n + W) for weights up to W |
| `last_stone_resort.kara` | the pile sorted again every turn, the last two smashed and the difference pushed on the end. O(n^2 log n) |
| `last_stone_iter.kara` | the heaviest found with `.iter().enumerate().max_by_key(..)` and taken out with `swap_remove`, twice a turn. O(n) a turn |
| `differential.kara` | the five arms against the statement read literally, five properties |

Every arm prints the same 15 lines: the answers for ten piles,
LeetCode's two examples among them, with `[2,2]` (nothing left),
`[10,3,3]` (the heaviest outweighs the rest), `[5,5,5,5]` and a pile of
1000 with four 1s; for every pile of 1 to 6 stones of 1 to 4, the
number of cases, the sum of the answers and a checksum; the same for
1000 random piles of 1 to 30 stones of 1 to 1000; and three of the
largest, 30 stones of 1000, the weights 1 to 30, and 1, 2, 4 up to
512, where each stone outweighs all the lighter ones together.
`last_stone.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: look at every stone to find the heaviest, then at every
other stone for the heaviest of the rest, smash the two, and play on
with what is left, recursively. It checks 6960 piles: every pile of 1
to 6 stones of 1 to 4 (5460), 1000 random piles of 1 to 30 stones of 1
to 1000, and 500 random piles of 1 to 30 stones of 1 to 8, where equal
weights are common.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer lies between 0 and the heaviest stone, and has the parity of the total weight |
| P3 | the answer is at least twice the heaviest less the total, and equals it when the heaviest outweighs the rest together |
| P4 | the pile reversed, and rotated by one, gives the same answer |
| P5 | two stones heavier than any, of equal weight, added to the pile change nothing |
| P6 | each arm agrees with at least two of the other four |

P2 holds because a smash takes the same weight from two stones, so the
total's parity never changes. P3 holds because the heaviest stone can
lose at most what the others weigh, and when it outweighs them all it
stays the heaviest through every turn and meets each of them once. P5
holds because the two added stones are the heaviest and smash each
other first.

The differential prints `6960 piles: checksum 15166340, 208800 checks
over 5 arms: 0 failures` under `karac __mir-run` (13 s), `karac
__mir-llvm-run` and `karac __mir-llvm-asan` with no error, and the same
line under `karac run` and from a `karac build` binary. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Fifteen are kept, three to
each arm. All fifteen are killed, each fails the same way under both
backends, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a last lone stone counted as nothing | P1 4088, P2 3479, P3 173, P6 4088 |
| M2 | ★: the two stones fused, `y + x` for `y - x` | P1 6067, P2 5541, P3 161, P6 6067 |
| M3 | ★: the difference one short | P1 3774, P2 3600, P3 133, P6 3774 |
| M4 | sorted: the binary search turned round | P1 3312, P2 2278, P3 64, P6 3312 |
| M5 | sorted: the last stone one light | P1 4088, P2 4088, P3 173, P6 4088 |
| M6 | sorted: the pile never sorted | P1 4335, P2 2959, P3 94, P4 6176, P6 4335 |
| M7 | count: three of a weight smash to nothing | P1 4408, P2 4146, P3 53, P5 4066, P6 4408 |
| M8 | count: stones of 1 never reached | P1 922, P3 144, P6 922 |
| M9 | count: the cursor skips a weight | P1 1799, P2 1616, P3 35, P6 1799 |
| M10 | resort: sorted heaviest first | P1 4666, P2 3467, P3 144, P5 1825, P6 4666 |
| M11 | resort: sorted once only | P1 2805, P2 2136, P6 2805 |
| M12 | resort: each stone smashed against the lightest | P1 2368, P5 2591, P6 2368 |
| M13 | iter: the number of stones left returned | P1 922, P2 609, P3 144, P6 922 |
| M14 | iter: always the first stone taken | P1 4785, P2 2953, P3 107, P4 6307, P5 4452, P6 4785 |
| M15 | iter: stops with two stones | P1 4593, P2 323, P3 169, P6 4593 |

P1 and P6 kill all fifteen, P2 and P3 thirteen each, P5 four and P4
two. P2 misses M8 and M12. M12 smashes the heaviest stone against the
lightest, and any smash keeps the total's parity and leaves no stone
heavier than the heaviest, so its wrong answers stay in range. P3
misses M11 and M12: when the heaviest outweighs the rest, it is the
heaviest every turn and absorbs every other stone whichever order they
come in, so both edits give the right answer exactly where P3 pins one.
P5 sees the edits that pick the wrong stones (M10, M12, M14) and M7,
under which two stones of one weight no longer always smash each other,
so the two added stones change the game. P4 sees only the two edits
whose answer depends on the order the stones arrive in: M6, which never
sorts, and M14, which takes the first stone.

Fifteen other edits were set aside. Three are equivalent: the ★ arm
pushing back a zero after two equal stones (a zero changes no later
smash and is returned only when it is the last), and the resort arm
pushing a difference that could be negative, or putting it at the
front, since it sorts the pile again before the next turn. Four fail
exactly as a kept one does: the count arm's lone stone counted as
nothing (as M1), and the ★ arm smallest first and the iterator arm
taking the lightest (as M10), and the sorted arm putting the difference
last (as M11). Eight fail in ways of their own: the ★ arm and resort arm
counting an empty pile as 1 (which fail alike), the sorted arm putting
the difference first and stopping with two stones, the count arm
counting the difference twice and keeping the lighter stone, and the
iterator arm's difference the wrong way round and its two stones named
the wrong way round.

## Verification

Every arm prints the same output as `last_stone.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with
no error. `karac run` and a `karac build` binary print the same output
for every arm and the differential. `karac check --output=json` reports
nothing on any file. The runs used a release build of kara
`f55808f63d`. Under `karac __mir-run` the arms take 0.3 s (sorted,
resort) to 1.2 s (iterator).

The arms went through the Mend loop clean: `karac check` reported
nothing on any of them as first written. Writing the ★ arm the way Rust
does, with `use std::collections::BinaryHeap;` and `BinaryHeap::from(..)`,
led to two gaps that B-2026-11-04-5 tracked, which this kata widened:
the `use` became an `import` whose `::` path had no fix, and once
`BinaryHeap::from` was written `BinaryHeap.from` the resolver said only
"undefined name 'BinaryHeap'". Kāra's heap is `PriorityQueue`, and it
pops the smallest first where Rust's pops the largest, so the faithful
rewrite is `PriorityQueue.max_first_from(..)`; a rename alone would flip
the game. Since kara `75832f76f1`, `karac fix` deletes the `use` line
(the heap is in the prelude) and writes `PriorityQueue.max_first_from(..)`
for `BinaryHeap::from(..)`. The arm then stops at the next gap: the
borrowed parameter `stones` passed where `max_first_from` takes `own
Vec[T]` draws "expected 'Vec[T]', found 'ref Vec[i32]'" and a cascade,
with no fix (B-2026-11-04-78).

## Benchmarks

The bench builds 1000 piles of 3000 stones once in all five languages,
with weights up to `10^9`, past LeetCode's 1000, so that the heap does
the work rather than the count arm's table. It then plays the ★ arm on
every pile three times, adding up the answers and folding each into a
checksum. Every implementation prints `1000 piles of 3000 stones, 3
rounds: total 1563, checksum 142150343`. Doubling the rounds doubles
C's time (2.26 to 2.29 s against 1.11 to 1.20 s), so no compiler hoists
a game out of the round loop. A game is up to 2999 turns, each two
pops and, unless the stones are equal, a push.

Each implementation uses its standard heap: Kāra's `PriorityQueue`
largest first, Rust's `BinaryHeap`, Go's `container/heap`, and
Python's `heapq` on negated weights. C has none, so its mirror is a
binary heap in an array that sifts by swapping, as Kāra's
`PriorityQueue` does.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python:

| | time | median |
|---|---|---|
| Rust (`rustc -O -C overflow-checks=on`) | 0.572 to 0.672 s | 0.608 s |
| Rust (`rustc -O`) | 0.586 to 0.690 s | 0.624 s |
| C (`clang -O3`) | 0.898 to 1.257 s | 1.131 s |
| Kāra (`karac build`) | 1.478 to 1.754 s | 1.578 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.542 to 1.730 s | 1.618 s |
| Go | 2.598 to 3.207 s | 2.896 s |
| Python | 6.0 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
`KARAC_AUTO_PAR_DEBUG=1` reports every loop kept in order, and its user
time (1.54 s) matches its real time.

Kāra took 2.66 times Rust's median time under overflow checks, and 1.43
times C's. Most of the gap to Rust is the heap, not the compiler. Rust's
`BinaryHeap::pop` moves the last element into a hole at the root, sifts
the hole to the bottom moving one child up at each level, and then
sifts up, which takes one comparison a level on the way down and
moves elements rather than swapping them; Kāra's
`PriorityQueue` swaps its way down, as the C mirror does. The same
swapping heap written by hand in Rust, under overflow checks, takes
1.32 to 1.39 s, against 1.53 to 1.64 s for it in Kāra and 1.12 to 1.15 s
in C, so the compiler accounts for about 1.15 times and the heap
algorithm for the rest. Filed as B-2026-11-04-55.
