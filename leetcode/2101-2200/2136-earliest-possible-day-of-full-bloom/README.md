# 2136. Earliest Possible Day of Full Bloom

You have `n` flower seeds. Every seed must be planted first before it
can begin to grow, then bloom. Planting a seed takes time and so does
the growth of a seed. You are given two **0-indexed** integer arrays
`plantTime` and `growTime`, of length `n` each:

- `plantTime[i]` is the number of **full days** it takes you to
  **plant** the `i`th seed. Every day, you can work on planting exactly
  one seed. You **do not** have to work on planting the same seed on
  consecutive days, but the planting of a seed is not complete **until**
  you have worked `plantTime[i]` days on planting it in total.
- `growTime[i]` is the number of **full days** it takes the `i`th seed
  to grow after being completely planted. **After** the last day of its
  growth, the flower **blooms** and stays bloomed forever.

From the beginning of day `0`, you can plant the seeds in **any** order.

Return the **earliest** possible day where **all** seeds are blooming.

```
plantTime = [1,4,3], growTime = [2,3,1]        ->  9
plantTime = [1,2,3,2], growTime = [2,1,2,1]    ->  9
plantTime = [1], growTime = [1]                ->  2
```

**Constraints:** `n == plantTime.length == growTime.length`;
`1 <= n <= 10^5`; `1 <= plantTime[i], growTime[i] <= 10^4`.

Every order plants for the same days in all, and splitting a seed's
planting only delays it, so what an order decides is which grow time
follows which planting. The seed that grows longest is planted first:
two neighbours out of that order, swapped, never bloom later. So the
seeds are sorted by grow time, longest first, and the answer is the
latest of each one's planting done plus its grow time. O(n log n).

## Approaches

| file | mechanism |
|---|---|
| `bloom.kara` ★ | the indices sorted by `sort_by` on grow time, longest first, then one walk keeping the days planted and the latest bloom |
| `bloom_buckets.kara` | no sort: grow times are at most 10000, so each one's plant times are summed into a bucket of a `Vec.filled`, and the buckets walked from the longest grow down |
| `bloom_pairs.kara` | the seeds `zip`ped into `(grow, plant)` tuples, sorted, and `fold`ed from the back by `rev`, the closure taking two tuple patterns and carrying the pair (days planted, latest bloom) |
| `bloom_struct.kara` | a `struct Seed` with its own `PartialEq`, `Eq`, `PartialOrd` and `Ord`, the longer grow the smaller, so that a plain `sort` puts the seeds in planting order |
| `bloom_search.kara` | a search on the day: a day can be met when, taking the grow times longest first, the days planted never pass the deadline of the seed just done; the test is monotone, so the earliest day is found by halving, each test walking the buckets |
| `bloom_solution.kara` | LeetCode's Rust template: `usize` indices sorted by `sort_unstable_by` through `\|&a, &b\|`, in `i32`; carried by `karac fix` in four rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more (equal grow times, equal plant times, a long grow behind a long
plant, and the largest times), each with
its answer; then the total and a checksum over 2000 random gardens of 1
to 10 seeds, times of 1 to 3, 1 to 10 or 1 to 100 in turn; then the
constraints' largest, 100000 seeds: all of the largest times, plant
times rising as grow times fall, and at random. `bloom.py` mirrors the ★
arm and its output is byte-identical.

No compiler gap was met. `karac fix` carries the template in four
rounds of 23, 4, 1 and 2 edits: Rust's spellings (`<..>` to `[..]`, the
`|&a, &b|` and `|&v|` patterns to `|a, b|` and `|v|`, the `&` dropped
from `cmp(&..)`, `struct Solution;` to `struct Solution {}`, the
adapter's `&Vec` to `ref Vec`, `Solution::` to `.`); then the
`Vec[usize]` of indices to `Vec[i64]`, `sort_unstable_by` to `sort_by`,
`ans` typed `i32` to match the grow times it is compared with, and the
adapter's `as i64` dropped, since an `i32` widens on return; then `cur`
typed `i32` as well; then the `ref` dropped from the adapter's two
parameters, which borrow already.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: from each day on, every seed still to plant may be the one
worked on that day, its planting split across days as the statement
allows, and the search keeps the earliest day by which every seed has
bloomed, over a state of days still to plant per seed; no order is
assumed and no seed is assumed planted in one piece. It checks 300
random gardens of 1 to 5 seeds, times of 1 to 3; then 30 of 1 to 4
seeds with one grow time; then 30 of 1 to 3 seeds, plant times of 1 to
3 and grow times of 1 to 20. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the seeds in reverse order: the same answer |
| P3 | every grow time one more: one day more |
| P4 | a seed of one day's planting and one day's growth added: the later of the answer and every planting day plus 2 |
| P5 | every time doubled: twice the answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 gardens: checksum 54011955, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
gardens by the same search. On a failure it prints the first ten and
then the count by property.

## Mutation testing

Thirty edits to the differential, four to six to each arm, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: sorted by plant time | P1 145, P2 91, P6 145 |
| M3 | ★: the bloom read before the planting | P1 360, P2 84, P4 320, P6 360 |
| M4 | ★: the last seed's bloom alone | P1 28, P4 58, P6 28 |
| M5 | buckets: walked from the shortest grow | P1 249, P4 319, P6 249 |
| M6 | buckets: the longest grow's bucket skipped | P1 360, P3 111, P4 346, P6 360 |
| M8 | buckets: a bucket holding its last plant time alone | P1 213, P2 139, P4 264, P6 213 |
| M10 | pairs: the tuples as (plant, grow) | P1 228, P3 296, P4 254, P6 228 |
| M11 | pairs: the bloom without its own planting | P1 360, P4 317, P6 360 |
| M12 | pairs: the days planted never carried | P1 256, P4 278, P6 256 |
| M15 | struct: the seeds left unsorted | P1 138, P2 199, P6 138 |
| M26 | struct: the planting started a day late | P1 360, P4 205, P5 360, P6 360 |
| M27 | struct: the longest grow's seed skipped | P1 360, P2 82, P3 63, P4 340, P6 360 |
| M17 | search: the deadline one day late | P1 360, P4 299, P5 360, P6 360 |
| M18 | search: the search's top one short | P1 111, P4 80, P5 111, P6 111 |
| M28 | search: the shortest grow's deadline never asked | P1 164, P3 164, P4 205, P5 164, P6 164 |
| M25 | solution: the adapter dropping the last seed | P1 271, P2 211, P4 232, P6 271 |
| M30 | solution: the adapter dropping the first seed | P1 256, P2 211, P4 322, P6 256 |

P1 and P6 kill all seventeen, P4 fifteen, P2 seven, P3 four and P5
four. P4 adds a seed that plants in a day and grows in a day, which
goes last in any right order and so blooms the day after every planting
is done; an edit that gets the order or the sum of the plantings wrong
shows there, all but the order by plant time (M2) and the unsorted
seeds (M15), which leave the new seed where it falls. P2 reverses the
seeds, which every right answer ignores; it sees an edit that ties the
answer to where a seed is listed: an order that is not by grow time
(M2, M15), a bloom read off the wrong seed (M3, M27), a bucket that
keeps its last seed alone (M8), and a seed dropped by the adapter (M25,
M30). P3 lengthens every grow by a day, which moves the answer by one;
it sees an edit that treats grow times unlike plant times or a bound
fixed by them: the tuples' fields swapped (M10), the longest bucket
skipped (M6), the longest grow's seed skipped (M27), and the shortest
grow's deadline never asked (M28). P5 doubles every time; it sees an
edit off by a fixed day, which doubling does not double: a planting
started late (M26), a deadline a day late (M17), a search a day short
(M18), and the shortest deadline left out (M28).

Of the thirty, thirteen were not kept. Three are equivalent. An empty
bucket's grow counted in the buckets arm, and an empty bucket's
deadline asked in the search arm, add only a bloom or a deadline below
one already counted, since the days planted are unchanged from the
bucket before, whose grow is longer. The search's halving keeping mid
as its low, with a step to the top when one apart, still ends on the
earliest day. None fails by a crash. Nine fail as a kept one does: the
order by shortest grow first in the ★, pairs, struct and search arms
and in the template, as M5; the struct arm ordered by plant time, as
M2; its own plant time left out, as M3; the adapter's lists swapped, as
M10; and the template's days planted never carried, as M12. One is
killed with checks of its own but was left out because its arm keeps
its share: the search arm's deadline met exactly counted as missed (P1
249, P4 234, P5 249, P6 249).

## Verification

Every arm prints the same output as `bloom.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.9 s to 3.6 s and the
differential 0.7 s.

## Benchmarks

The bench builds 10 gardens of 100000 seeds once, times of 1 to 10000;
then solves every garden 10 times, one seed's plant and grow times
drawn anew before each solve so that no solve repeats one before, with
the ★ arm in all five languages. Every implementation prints `100
solves: 46929340693 days in all, checksum 735495539`.

BENCHTAB
