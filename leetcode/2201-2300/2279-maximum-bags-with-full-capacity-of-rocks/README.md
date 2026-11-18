# 2279. Maximum Bags With Full Capacity of Rocks

You have `n` bags numbered from `0` to `n - 1`. You are given two
**0-indexed** integer arrays `capacity` and `rocks`. The `i`th bag can
hold a maximum of `capacity[i]` rocks and currently contains `rocks[i]`
rocks. You are also given an integer `additionalRocks`, the number of
additional rocks you can place in **any** of the bags.

Return *the **maximum** number of bags that could have full capacity
after placing the additional rocks in some bags.*

```
capacity = [2,3,4,5], rocks = [1,2,4,4], additionalRocks = 2    ->  3
capacity = [10,2,2], rocks = [2,2,0], additionalRocks = 100     ->  3
```

**Constraints:** `n == capacity.length == rocks.length`; `1 <= n <= 5 *
10^4`; `1 <= capacity[i] <= 10^9`; `0 <= rocks[i] <= capacity[i]`; `1
<= additionalRocks <= 10^9`.

Filling a bag costs what it lacks, `capacity[i] - rocks[i]`, and every
full bag counts the same, so the cheapest go first: any set of `k` bags
the rocks can fill costs at least the `k` cheapest. With what the bags
lack sorted, spend the rocks in that order until the next bag costs too
much. O(n log n).

## Approaches

| file | mechanism |
|---|---|
| `bags.kara` ★ | what each bag lacks pushed into a `Vec` and sorted; the spare rocks spent in that order until a bag costs more than is left |
| `bags_heap.kara` | what each bag lacks into a `PriorityQueue.new()`, which pops the smallest first; the cheapest taken off and filled while the rocks cover it |
| `bags_binary.kara` | the sorted needs' prefix costs from `[0]`, and `partition_point(\|c\| c <= additional_rocks) - 1` for the most bags the rocks pay for |
| `bags_struct.kara` | `struct Pile` of the rocks left and the bags filled; `fill` (`mut ref self`) takes a need and answers whether it filled the bag, and the bags are offered cheapest first until one is refused |
| `bags_iter.kara` | one chain: the needs by `zip` and `map`, sorted, the running cost by `scan`, the bags within the rocks by `take_while`, then `count` |
| `bags_solution.kara` | LeetCode's Rust template: `Vec<i32>` twice and `i32` in, `i32` out; the needs by `zip`, `sort_unstable`, and `for d in need` while the rocks last; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and five
more (one full bag, 1; one bag a rock short, 0; three bags with rocks
for two, 2; nothing to spare, 0; every bag full already, 2), each with
its count; then 2000 random sets of 1 to 40 bags of capacity up to 10,
1000 or 10^9, half of them a fifth full or less, with spare rocks up to
what they all lack, with a checksum; then three of the constraints'
largest, 5 * 10^4 bags: capacities up to 10^9 (368), up to 100
(22000), and every bag empty with capacity 1 and 10^9 to spare (50000).
`bags.py` mirrors the ★ arm and its output is byte-identical.

`PriorityQueue.min_first()`, the name the heap arm was first written
with, does not exist: `PriorityQueue.new()` is already smallest first,
and `max_first()` the other way. `karac check` reports the unknown
method with no hint toward `new()`.

`karac fix` carries the template in one round, reporting 20 edits:
`Vec<i32>` to `Vec[i32]` three times, `sort_unstable` to `sort`,
`struct Solution;` to `struct Solution {}`, and in the adapter
`&Vec<i64>` to a bare `Vec[i64]` twice, `|&x|` to `|x|`, `Solution::`
to `Solution.` and the `as i64` dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every set of bags, as a mask, costed by what its bags lack,
and the largest set the spare rocks pay for. No sort and no greed. It
checks 300 random sets of 1 to 10 bags of capacity up to 3, 10 or 1000,
with spare rocks up to what they all lack; then 30 sets of equal bags;
then 30 with every bag full but one. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the count is the literal reading's |
| P2 | the bags in reverse order: the same count |
| P3 | every capacity, every bag's rocks and the spare rocks times 3: the same count |
| P4 | at least the bags already full and at most all of them, and all exactly when the spare rocks cover what every bag lacks |
| P5 | one spare rock more: the same count or one more |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 491323333, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that tries
every `itertools.combinations` of the needs. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: never sorted | P1 164, P2 186, P4 50, P5 28, P6 164 |
| M3 | ★: the dearest first | P1 235, P4 87, P5 24, P6 235 |
| M5 | ★: the capacity for the need | P1 288, P4 122, P6 288 |
| M7 | heap: the rocks spent twice | P1 155, P4 22, P6 155 |
| M9 | heap: the cheapest bag thrown away | P1 285, P4 100, P6 285 |
| M10 | heap: each need doubled | P1 228, P4 44, P6 228 |
| M12 | binary: the empty prefix counted | P1 360, P4 218, P6 360 |
| M13 | binary: a cost equal to the rocks refused | P1 148, P4 94, P5 39, P6 148 |
| M15 | binary: the costs never summed | P1 184, P4 153, P5 18, P6 184 |
| M17 | struct: every bag filled | P1 299, P4 299, P6 299 |
| M19 | struct: a bag that takes the last rock refused | P1 137, P4 83, P5 25, P6 137 |
| M20 | struct: each bag counted twice | P1 317, P4 275, P5 87, P6 317 |
| M22 | iter: equal needs taken once | P1 170, P4 85, P6 170 |
| M23 | iter: each bag one rock dearer | P1 212, P3 125, P4 110, P6 212 |
| M25 | iter: the first need free | P1 75, P4 42, P6 75 |
| M27 | solution: each bag half price | P1 164, P3 36, P4 92, P5 12, P6 164 |
| M29 | solution: each bag one rock cheaper | P1 146, P3 112, P4 102, P5 2, P6 146 |

P1, P4 and P6 kill all seventeen, P5 eight, P3 three, and P2 one. P4
alone needs no literal reading and still catches every edit: each one
either fills a bag the rocks cannot pay for, misses all of them when
the rocks cover all, or answers below the bags already full. P3 catches
the edits that move a cost by a fixed amount, a rock more or less or
half the price rounded, which tripling every count does not scale with
it. P5 catches the edits whose count jumps or stalls by the wrong amount
as one rock is added: a bag refused at its exact cost, a need not
summed, two bags counted for one. Every arm sorts or heaps the needs,
so reversing the bags moves only an arm that never sorts.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. All fourteen fail as a kept one does: the ★ and
heap arms' bag that takes the last rock refused and the struct arm's
pile one rock short (M2, M8, M21) as the struct arm's (M19); the ★ and heap arms' rocks
never spent and the struct arm's pile never drawn (M4, M11, M18) as the
binary arm's costs never summed (M15); the ★ arm's count from 1 (M6) as
the binary arm's empty prefix counted (M12); the binary, iter and
template arms' never sorted (M14, M24, M28) as the ★ arm's (M1); the
binary arm's costs from 1 (M16) as its cost equal to the rocks refused
(M13); the iter arm's need turned negative (M26) as the struct arm's
every bag filled (M17); the template's cheapest bag skipped (M30) as the
heap arm's thrown away (M9); and the template's half the rocks (M31) as
the heap arm's each need doubled (M10).

Six edits of the first draft were replaced because each failed as
another did: the heap arm's largest first, as the ★ arm's M3; the struct
arm's never sorted, as M1; the iter arm's cost equal to the rocks
refused and its costs from 1, as M19; the iter arm's need against the
rocks alone, as M15; and the template's bag that takes the last rock
refused, as M19. They are now M7, M20, M22, M23, M25 and M27. One
candidate for the struct arm, a refused bag passed over rather than
stopping at, was equivalent and not used: with the needs sorted, no bag
after a refused one is cheaper.

## Verification

Every arm prints the same output as `bags.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★ arm takes 0.6 s, the differential 0.7 s,
the binary arm 0.8 s, the struct arm 1.2 s, the iter arm 1.4 s, the
template 1.6 s, and the heap arm 3.2 s, the 1.5 * 10^5 pushes of the long
cases into the `PriorityQueue` taking most of it.

## Benchmarks

The bench answers 50 sets of the constraints' largest, 5 * 10^4 bags of
capacity up to 10^9, each filled to a random level, with up to 10^9
spare rocks, with the ★ arm in all five languages. Every implementation
prints `50 sets of 5 * 10^4: checksum 595266871`. Each builds its bags
from the same generator and sorts a fresh list of needs per call: C by
`qsort`, Go by `sort.Slice`.

BENCHTAB
