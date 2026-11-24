# 2462. Total Cost to Hire K Workers

You are given a **0-indexed** integer array `costs` where `costs[i]` is
the cost of hiring the `i`th worker.

You are also given two integers `k` and `candidates`. We want to hire
exactly `k` workers according to the following rules:

- You will run `k` sessions and hire exactly one worker in each session.
- In each hiring session, choose the worker with the lowest cost from
  either the first `candidates` workers or the last `candidates`
  workers. Break the tie by the smallest index.
  - For example, if `costs = [3,2,7,7,1,2]` and `candidates = 2`, then in
    the first hiring session, we will choose the `4`th worker because
    they have the lowest cost `[3,2,7,7,1,2]`.
  - In the second hiring session, we will choose `1`st worker because
    they have the same lowest cost as `4`th worker but they have the
    smallest index `[3,2,7,7,2]`. Please note that the indexing may be
    changed in the process.
- If there are fewer than `candidates` workers remaining, choose the
  worker with the lowest cost among them. Break the tie by the smallest
  index.
- A worker can only be chosen once.

Return *the total cost to hire exactly* `k` *workers.*

```
costs = [17,12,10,2,7,2,11,20,8], k = 3, candidates = 4  ->  11
costs = [1,2,4,1], k = 3, candidates = 3                 ->  4
```

**Constraints:** `1 <= costs.length <= 10^5`; `1 <= costs[i] <= 10^5`;
`1 <= k, candidates <= costs.length`.

Each session looks only at the two ends of the workers still waiting,
`candidates` from each, and hiring one moves the next waiting worker
from the middle onto that end. So two heaps of `(cost, index)` hold the
ends, and the untaken middle is a range between two pointers. A tie
between the two tops always goes to the front, whose indices are all
lower. Once the ends meet, every worker left is a candidate, and the
heaps simply drain.

## Approaches

| file | mechanism |
|---|---|
| `hire.kara` ★ | two heaps: the first `candidates` workers and the last `candidates` not already taken, each by `(cost, index)`; each session takes the cheaper top, the front's on a tie, and refills that heap from the middle while any is left. O((k + c) log c) |
| `hire_naive.kara` | the statement read directly: the workers not yet hired kept in order; each session looks at all of them when fewer than `2 candidates` are left and otherwise at the first and last `candidates`, takes the lowest `(cost, index)` and removes it. O(k n) |
| `hire_one.kara` | one heap of `(cost, index)` over both ends: a worker's index tells which end it came from, since the front's are below the middle and the back's above, so the refill comes from the same end; ties fall to the lower index by the tuple order. O((k + c) log c) |
| `hire_sorted.kara` | a `SortedSet` of `(cost, index)` as the pool, each session taking its least entry by `min` and removing it, and refilling from the end its index shows. O((k + c) log c) |
| `hire_iter.kara` | iterators: the two starting heaps collected from `enumerate` with `take`, and with `rev`, `take` and a `filter` past the front's; then the `k` sessions by `map` over `0..k`, each closure taking the cheaper top and refilling, and the costs added by `sum`. O((k + c) log c) |
| `hire_solution.kara` | LeetCode's Rust template: `Vec<i32>`, `k` and `candidates` as `i32`, two `BinaryHeap`s of `Reverse((cost, index))` filled over `usize` pointers `l` and `r`, the tops compared through `peek()` and matched as `Some(&Reverse(..))`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples; then five
more, one worker, the two ends overlapping from the start, a tie
between the ends, which the front wins, every worker hired with one
candidate a side, and the cheapest in the middle, out of reach until
the ends are used up; 2000 workers of the constraints' largest cost,
every one hired; 2000 random costs from 1 to `10^5` with `k` of 1000
and 2 candidates, and with `k` of 2000 and 1500 candidates; and 3000
random cases of 1 to 12 workers with costs from 1 to 6 and a random `k`
and `candidates`, as a checksum. The lists stop at 2000 workers, below
the constraints' `10^5`, since the naive arm is O(k n). `hire.py`
mirrors the ★ arm with `heapq` and its output is byte-identical, and
the mirror was checked on every list of 1 to 7 costs from 1 to 3, with
every `k` and `candidates`, against the sessions run by hand.

`check` first reports 10 errors on the template. `karac fix` carried
the two `use` lines, the brackets of `Vec<..>`, `BinaryHeap::new`'s
path, each `&&` and each `&` of `Some(&Reverse(..))`, and `struct
Solution;`; but until B-2026-11-24-28 it then stopped at the two heaps, named
`front` and `back`: it could not tell which way they pop, so it wrote
`import std.cmp.Reverse;` and left each `BinaryHeap` for the author.
The same template with the heaps named anything else was carried: the
heaps' evidence was read from the program with the Kāra library
appended, whose `collections.kara` pushes bare items with
`self.front.push(x)` and `self.back.push(x)`. Now
one call carries it, reporting 24 edits: both heaps become
`PriorityQueue.new()`, which pops the smallest first, and every
`Reverse(..)` is unwrapped, in the pushes, the `peek()` patterns and the
two `let Reverse((cost, _)) = ..`; `candidates as usize` is written
`as i64` and each `cost as i64` dropped. The `match` over the two
`peek()`s and `l < c and l < r` over the lengths stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the workers not yet hired kept as a list of indices; each
session builds its candidates as the list's first `candidates` and its
last `candidates`, all of it when those overlap, and hires the cheapest,
the lower index on a tie, each compared by hand. No heap or set is
kept. It checks 300 random lists of 1 to 12 costs from 1 to 6; then 30
of up to 200 costs from 1 to 1000, with up to 20 candidates; then 30 of
up to 200 costs from 1 to 5; each with a random `k`, and `candidates`
from 1 to the length unless said. All 360 are drawn before any arm
answers; each case's constant for P3 is drawn as the case is checked.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the costs made distinct, `1000 v + i`: the same answer for the list reversed |
| P3 | every cost raised by one constant below 1000: the answer plus `k` times it |
| P4 | the answer between the sums of the `k` cheapest and the `k` dearest |
| P5 | `candidates` the whole list: the sum of the `k` cheapest |
| P6 | each arm agrees with at least three of the other five |

P2 holds because with no two costs equal no tie is ever broken, and the
sessions on the reversed list are the same sessions mirrored, front for
back. P3 holds because raising every cost keeps their order, ties
included, and every hire pays the constant once. P4 holds because any
`k` distinct workers cost at least the cheapest `k` and at most the
dearest. P5 holds because with every worker a candidate each session
takes the cheapest left.

The differential prints `360 cases: checksum 912930231, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and runs the sessions over slices of the waiting list.
On a failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the front one short | P1 35, P2 63, P6 35 |
| M3 | ★: the back filled over the front | P1 7, P2 13, P6 7 |
| M6 | ★: the dearer top taken | P1 173, P2 84, P6 173 |
| M7 | naive: the last candidate at the back left out | P1 41, P2 63, P6 41 |
| M10 | naive: the first worker removed instead | P1 233, P2 245, P4 223, P5 240, P6 233 |
| M11 | naive: the dearest hired | P1 253, P5 261, P6 253 |
| M13 | one: the refill side reversed | P1 34, P6 34 |
| M15 | one: the cost counted with its index | P1 284, P2 124, P4 78, P5 287, P6 284 |
| M16 | one: every refill from the back | P1 36, P2 40, P6 36 |
| M17 | sorted: the first worker paid twice | P1 262, P2 286, P3 262, P4 123, P5 245, P6 262 |
| M19 | sorted: the hired worker left in the pool | P1 157, P3 157, P4 155, P5 163, P6 157 |
| M20 | sorted: the refill priced one place along | P1 98, P2 112, P4 43, P6 98 |
| M23 | iter: the back left empty | P1 96, P2 172, P5 67, P6 96 |
| M24 | iter: a tie to the back | P1 11, P6 11 |
| M25 | iter: the front never refilled | P1 44, P2 54, P6 44 |
| M29 | solution: the back never refilled | P1 35, P2 54, P6 35 |
| M30 | solution: the cost taken from the back top too | P1 182, P2 284, P4 63, P6 182 |

P1 and P6 kill all seventeen, P2 thirteen, P4 and P5 six and P3 two.

Fourteen are not kept. Eight fail exactly as a kept one: the ★ arm's
tie to the back, the naive arm's tie to the later worker and the
template's tie to the back (M1, M9, M28) as the iter arm's (M24), each
comparing the two tops by cost alone; the ★ arm's front never refilled
(M4) as the iter arm's (M25); the ★ arm's front refilled from the back
(M5) as the one-heap arm's every refill from the back (M16); the naive
arm's front's last candidate left out (M8) as the ★ arm's front one
short (M2); the sorted arm's dearest entry taken (M18) as the naive
arm's dearest hired (M11); and the template's back started one short
(M27) as the naive arm's last candidate at the back left out (M7). Six
fail apart from every kept one and were left out because those arms
keep their share already: the one-heap arm's refill always from the
front (M12), which fails exactly as the iter arm's back refilled from
the front (M26); the one-heap arm's back one long (M14), which fails
exactly as the iter arm's (M22); the sorted arm's back end never moved
in (M21); and the template's one session fewer (M31).

Eleven edits of the first run were replaced: five ended in a runtime
error, a pool run dry or an index past the end, and six could not be
killed by any check. Comparing the two tops as whole `(cost, index)` tuples
with `<` instead of `<=`, in the ★, iter and template arms, changes
nothing, since the two tops never share an index and on a tie of costs
the front's index is the lower. The naive arm's `<=` against `<` over
the same tuples, its test for fewer than `2 candidates` left, which the
two ends already cover, and the iter arm's front capped at `n / 2`
rather than `(n + 1) / 2`, which only moves a worker between two heaps
that are both in play, are equivalent too. P2 was first `k` the whole
list, every cost added, which only a lost or doubled hire breaks; it
was replaced by the reversal of distinct costs, which every edit that
treats the two ends differently breaks.

## Verification

Every arm prints the same output as `hire.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.4 to 0.7 s but the naive arm,
1.4 s, and the differential 2.9 s; under `karac __mir-llvm-asan` the
differential takes 1.1 s and under `karac run` 0.7 s.

## Benchmarks

The bench builds 10 lists of `10^5` costs from 1 to `10^5`, the
constraints' longest, once from its own generator, then makes 32
passes; each sets one cost of every list from the checksum so far, so
no answer carries over, then answers every list with `k` of `5 * 10^4`
and `1 + 97p` candidates, folding the answer plus the pass into the
checksum. The bench uses the ★ arm, two heaps of `(cost, index)`, in
all five languages. Every implementation prints `32 passes over 10
lists of 10^5: checksum 708394102`. The heaps are the language's own:
`PriorityQueue` in Kāra, `BinaryHeap` of `Reverse` in Rust,
`container/heap` in Go and `heapq` in Python; C has none, and uses two
binary heaps of `(cost, index)` pairs in arrays allocated once.

BENCHTAB
