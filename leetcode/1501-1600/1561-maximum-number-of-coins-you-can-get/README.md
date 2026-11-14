# 1561. Maximum Number of Coins You Can Get

There are `3n` piles of coins of varying size, and you and your friends
take piles as follows: in each step you choose any 3 piles; of them,
Alice picks the pile with the most coins, you pick the next one, and Bob
picks the last. This repeats until there are no more piles. Given an
array of integers `piles` where `piles[i]` is the number of coins in the
`i`th pile, return the maximum number of coins you can have.

```
piles = [2,4,1,2,7,8]          ->  9
piles = [2,4,5]                ->  4
piles = [9,8,7,6,5,1,2,3,4]    ->  18
```

**Constraints:** `3 <= piles.length <= 10^5`; `piles.length % 3 == 0`;
`1 <= piles[i] <= 10^4`.

## Approaches

Bob takes one pile of every triple and gives nothing back, so he can be
handed the `n` smallest; of the `2n` left, sorted, each pile you take
needs one above it for Alice, so the best you can do is every other pile
from the bottom.

| file | mechanism |
|---|---|
| `coins.kara` ★ | the piles sorted, and `sorted[n..].iter().step_by(2).sum()`. O(n log n) |
| `coins_rounds.kara` | the rounds played out: the sorted piles collected into a `VecDeque`, and each round Alice takes `pop_back`, you the next `pop_back`, Bob `pop_front`. O(n log n) |
| `coins_count.kara` | a counting sort: a count per size from 1 to 10^4, walked from the top, laying out the `2n` largest piles largest first; you take the second, fourth and so on. O(n + 10^4) |
| `coins_solution.kara` | LeetCode's Rust template (`max_coins(mut piles: Vec<i32>) -> i32`, `sort_unstable`, then `skip(n).step_by(2).sum()`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples, then
`[1, 1, 1]`, six piles of 5, `[1, 2, 3, 4, 5, 6]`, three piles of 10^4,
and three of 1 with three of 10^4; then the total and a checksum of the
answers for 3000 random lists of up to 9 piles of up to 10, 300 of up to
3000 piles and 30 of up to 99999, both of up to 10^4. `coins.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every way to split the piles into triples (the first pile with
each pair of the others, the rest split the same way), you taking the
middle of each, and the most you can end with. It checks 3000 lists of 3,
6 or 9 piles of 1 to at most 20 coins, every random choice drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer lies between `n` times the smallest pile and `n` times the largest |
| P3 | the piles in reverse order leave the answer |
| P4 | every pile doubled doubles the answer, and every pile raised by `c` raises it by `n c` |
| P5 | a pile of 1 and two piles of `v`, above every other, put after the piles add `v` |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 938392694, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` (the interpreter takes about
30 s on the differential, so the timeout here was 150 s). All ten are
killed, each the same way under both backends. A first M5, Bob taking
nothing, was killed only by the next round's `unwrap` on an empty
`VecDeque`, and was replaced by one that answers wrong.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every other pile from one past the `n` smallest | P1 2460, P6 2460 |
| M2 | ★: Bob handed one triple's pile too few | P1 3000, P2 1817, P4 2962, P6 3000 |
| M3 | ★: the piles not sorted | P1 2091, P3 1668, P5 2990, P6 2091 |
| M4 | rounds: you take the largest, Alice the next | P1 2460, P6 2460 |
| M5 | rounds: Bob takes from the back | P1 1509, P5 2454, P6 1509 |
| M6 | rounds: you take the smallest, Bob the next largest | P1 2659, P5 2996, P6 2659 |
| M7 | count: the first, third and so on taken | P1 2460, P6 2460 |
| M8 | count: one pile fewer laid out | P1 3000, P2 1186, P4 2962, P6 3000 |
| M9 | template: every third pile past the `n` smallest | P1 1644, P2 69, P4 1031, P5 941, P6 1644 |
| M10 | template: the piles not sorted | P1 2091, P3 1668, P5 2990, P6 2091 |

## Benchmarks

The bench draws 20 lists of 99999 piles of 1 to 10^4 coins once, and
asks each 10 times by the ★ arm, in all five languages. Every call copies
the list and sorts the copy: Kāra with its `sort`, Rust with `sort`, Go
with `slices.Sort` and C with `qsort`. Every implementation prints `10
passes over 20 lists of 99999 piles: 42386445390 coins, checksum
337167400`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.344 s |
| Kāra (`karac build`) | 0.353 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.531 s |
| Rust (`rustc -O`) | 0.536 s |
| Go | 1.552 s |
| C (`clang -O3`) | 2.545 s |
| Python | 4.3 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.31 s and 0.33 s on one run).

Kāra is 0.65x Rust under overflow checks by median, and the sort is the
whole of it: Kāra's `sort` on a `Vec[i64]` calls the runtime's
`karac_vec_sort_i64_8`, which is Rust's `sort_unstable`, since a stable
and an unstable sort of plain integers give the same result; the Rust
mirror's `sort` is the stable one, which is slower on this data. C pays
a call through `qsort`'s comparison function for every comparison. Not
traced further.

## Verification

All four arms print the same output as `coins.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The ★, rounds and counting arms were written in Kāra and checked as
written.

The Rust template took 3 changed lines and 1 added, then 1 added, then 2
changed, over three rounds of `karac fix`: Rust's `mut piles: Vec<i32>`
parameter to `piles: own Vec[i32]` with `let mut piles = piles;` added
at the body's start, as the refusal spells out, the `Vec<..>` types to
`Vec[..]`, the wrapper's `|&p|` to `|p|` and `Solution::` to
`Solution.`; then `struct Solution {}` added; then `sort_unstable` to
`sort` (the library has only the stable sort) and the wrapper's closing
`as i64` dropped. It checks and agrees with no hand edit.
