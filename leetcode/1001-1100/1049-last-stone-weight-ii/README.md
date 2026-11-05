# 1049. Last Stone Weight II

You are given an array of integers `stones` where `stones[i]` is the weight
of the `i`th stone.

We are playing a game with the stones. On each turn, we choose any two
stones and smash them together. Suppose the stones have weights `x` and `y`
with `x <= y`. The result of this smash is:

- If `x == y`, both stones are destroyed, and
- If `x != y`, the stone of weight `x` is destroyed, and the stone of
  weight `y` has new weight `y - x`.

At the end of the game, there is **at most one** stone left.

Return the **smallest possible weight** of the left stone. If there are no
stones left, return `0`.

```
stones = [2,7,4,1,8,1]       ->  1
stones = [31,26,33,21,40]    ->  5
```

**Constraints:** `1 <= stones.length <= 30`; `1 <= stones[i] <= 100`.

## Approaches

However the stones are smashed, what is left is the stones split into two
piles, one counted plus and one minus, and any split can be smashed down to
its difference. So the answer is the total less twice the largest sum a set
of the stones makes without passing half the total.

| file | mechanism |
|---|---|
| `last_stone.kara` ★ | a `Vec[bool]` of the sums up to half the total, each stone walked downward so it is used once. O(n S) |
| `last_stone_diffs.kara` | a `Set[i64]` of every signed total, each stone added and subtracted; the smallest absolute value. O(n S) |
| `last_stone_memo.kara` | recursion down the stones, a `Map[(i64, i64), i64]` from (stone, signed total so far) to the best weight left. O(n S) |
| `last_stone_bits.kara` | the ★ table as a bitset of `u64` words, each stone or-ing in the set shifted up by its weight, across words. O(n S / 64) |
| `last_stone_iter.kara` | the ★ sums as a `SortedSet` folded over the stones with `flat_map` and `filter`, the answer from its `max` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: the answers for LeetCode's two examples
and eight more (`[1, 1]`, which leaves nothing, and twenty-nine 2s and a 99,
where no split of the 2s reaches the 99, among them); the total and a
checksum of the answers for 3000 random lists of 1 to 8 stones of 1 to 20
and for 500 lists of 1 to 30 stones of 1 to 100; and two lists at the size
limit, 29 stones of 100 and one of 99 (1) and the first 30 odd numbers (0).
`last_stone.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: from a list of stones, try every pair as the next smash, two
equal stones both going and two unequal leaving their difference, and take
the smallest weight any order leaves; the stones are kept sorted, so a set
reached two ways is worked out once. It checks 3000 random lists: 2000 of 1
to 6 stones of 1 to 10, where weights repeat and many splits tie, and 1000
of 1 to 7 stones of 1 to 100, where a stone moves the bits arm's sums a
whole word.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is between 0 and the heaviest stone, and odd exactly when the total is |
| P3 | the list reversed, and rotated by one, gives the same answer |
| P4 | a stone weighing the whole list added, or the list given twice, leaves 0 |
| P5 | every stone twice as heavy makes the answer twice as large |
| P6 | each arm agrees with at least two of the other four |

P2 holds because the heavier pile is never more than the heaviest stone
ahead of the lighter one in a best split (moving that stone across would
narrow the gap), and every smash keeps the total's parity. P4 holds because
the new stone, or the second copy of each stone, can take the minus side of
everything else.

The differential prints `3000 lists: checksum 242903153, 90000 checks over
5 arms: 0 failures` under `karac __mir-run` (32 s), `karac
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
| M1 | ★: walked upward, so a stone is used again | P1 959, P6 959 |
| M2 | ★: half rounded up | P1 699, P2 699, P5 699, P6 699 |
| M3 | ★: every other sum skipped | P1 1491, P2 769, P3 671, P4 1231, P5 1892, P6 1491 |
| M4 | diffs: the totals before a stone kept, so a stone may be left out | P1 2592, P2 1532, P6 2592 |
| M5 | diffs: no absolute value | P1 3000, P2 3000, P4 3000, P6 3000 |
| M6 | diffs: starting from 1 | P1 3000, P2 3000, P4 3000, P5 3000, P6 3000 |
| M7 | memo: looked up by the stone alone | P1 107, P3 286, P6 107 |
| M8 | memo: the worse sign | P1 2521, P2 2521, P4 3000, P6 2521 |
| M9 | memo: the first stone left out | P1 2695, P2 1470, P3 2403, P4 3000, P6 2695 |
| M10 | bits: no carry between words | P1 335, P2 51, P4 687, P5 321, P6 335 |
| M11 | bits: the whole-word shift ignored | P1 476, P2 209, P3 345, P4 717, P5 620, P6 476 |
| M12 | bits: the carry one bit short | P1 318, P4 313, P5 434, P6 318 |
| M13 | iter: 1 made from nothing | P1 1893, P5 2592, P6 1893 |
| M14 | iter: the best sum counted once | P1 2521, P2 2170, P4 3000, P6 2521 |
| M15 | iter: the last stone left out | P1 844, P2 278, P3 1443, P6 844 |

P1 and P6 kill all fifteen, P2 eleven, P4 eight, P5 seven and P3 five. M1
is seen only by P1 and P6: a stone used twice still gives a weight of the
right parity, in range, that moves with nothing the other properties
change, and the doubled list doubles it. P3 sees the edits whose answer
depends on which stone is first or last (M9, M15), the memo whose key
forgets the total (M7), and the two that drop sums by position (M3, M11).
P5 sees the edits that do not scale: a rounding (M2), every other sum
(M3), a constant 1 (M6, M13) and the bit edits, since doubling moves
the sums across words.

Fifteen other edits were set aside. Ten fail exactly as a kept one does.
Six answer the total, as M8 does: the ★ arm never making a stone's own
weight, diffs adding every stone or taking the largest, the memo adding
both signs, the bits arm never updating the lowest word, and the iter arm
taking the smallest sum. The memo with no absolute value and the bits arm
searched from the total fail as M5, the memo leaving any stone out as M4,
and the ★ arm counting the best sum once as M14. Two fail in ways of their
own: the ★ arm leaving the first stone out, and the bits arm xor-ing for or.
Two crash: the iter arm keeping only sums below half, or adding every stone,
empties the set on a one-stone list, and both backends stop with the same
"called unwrap() on None". One survives, and it is equivalent: diffs
writing `s - d` for `d - s` flips the sign of some totals, but every total
the arm reaches is the true one or its negative, and the answer takes the
absolute value.

## Verification

Every arm prints the same output as `last_stone.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file. The runs used a release build of kara `0152b193bc`.
Under `karac __mir-run` the arms take 0.3 s (bits) to 36 s (iter); the
iter arm builds two-element arrays and a sorted set for every sum.

The ★ and bits arms needed only `karac fix`, which turned a `!` into
`not` and a `&&` into `and`; diffs and memo passed as first written. The
iter arm, written the way Rust writes it, stopped short before kara
`0152b193bc`:
`SortedSet.from([0])`, Rust's `BTreeSet::from([0])`, was "no associated
function 'from'" with no fix, and the cascade from its unknown type offered
to delete the `*` from each `*t`. `SortedSet.from` and `SortedMap.from` now
build the sorted collections from a list as `Set.from` and `Map.from` do,
and `karac fix` carries the rest: the closure's array becomes
`[*t, *t + *s].into_iter()`, since `flat_map` takes a closure that returns
an iterator, and the comparison's `*t <= half` becomes `t <= half`.

## Benchmarks

The bench builds 1000 lists of 30 stones of 1 to 100 once in all five
languages, then runs the ★ arm on every list ten times, adding up the
answers and folding each into a checksum. Every implementation prints
`1000 lists of 30 stones, 10 rounds: total 4700, checksum 388451308`. A
list's half total is about 750, so each list fills a table of that many
sums 30 times.

Each implementation allocates the table afresh for each list: Kāra's
`Vec.filled(half + 1, false)`, Rust's `vec![false; n]`, Go's `make`, a list
in Python and `calloc` in C, and walks it downward with a bounds-checked
index where the language checks one.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `0152b193bc` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.179 to 0.194 s | 0.191 s |
| Rust (`rustc -O`) | 0.188 to 0.215 s | 0.200 s |
| Go | 0.193 to 0.246 s | 0.224 s |
| Kāra (`karac build`) | 0.252 to 0.324 s | 0.271 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.253 to 0.300 s | 0.276 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.253 to 0.349 s | 0.280 s |
| Python | 11.8 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.27 s) matches its real time.

Kāra took 1.01 times Rust's median time under overflow checks, and 1.47
times C's. The inner loop is a bounds-checked read and write and a checked
decrement for every sum below half; with overflow checks Rust pays the
same, and without them it is within 5% of C.
