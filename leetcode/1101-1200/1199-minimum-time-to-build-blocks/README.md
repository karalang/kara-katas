# 1199. Minimum Time to Build Blocks

You are given a list of blocks, where `blocks[i] = t` means that the
`i`-th block needs `t` units of time to be built. A block can only be
built by exactly one worker.

A worker can either split into two workers (the number of workers
increases by one) or build a block and then go home. Both decisions
cost some time. The time cost of splitting one worker into two workers
is given as an integer `split`. Note that if two workers split at the
same time, they split in parallel, so the cost would be `split`.

Output the minimum time needed to build all blocks. Initially, there is
only one worker.

```
blocks = [1],       split = 1  ->  1
blocks = [1, 2],    split = 5  ->  7     split, then each builds one: 5 + max(1, 2)
blocks = [1, 2, 3], split = 1  ->  4
```

**Constraints:** `1 <= blocks.length <= 1000`; `1 <= blocks[i] <=
10^5`; `1 <= split <= 100`.

The arms are `fn min_build_time(blocks: own Vec[i64], split: i64) ->
i64`, or `blocks: Vec[i64]` for an arm that only reads them. The two
Rust arms keep the method LeetCode gives Rust users, on `Vec<i32>` and
`i32`, inside `impl Solution`, and a one-line `min_build_time` calls
it.

## Approaches

The splits form a binary tree with a block at each leaf, and a block at
depth `d` is done at `d * split` plus its own time.

| file | mechanism |
|---|---|
| `min_build_time.kara` ★ | Huffman's merge: the two quickest blocks merged into one that takes `split` more than the slower of them, on a smallest-first `PriorityQueue`, until one block, the answer, is left. O(n log n) |
| `min_build_time_queues.kara` | Huffman's merge with two queues and no heap: the blocks sorted, and the merged blocks in a `VecDeque` that fills in rising order, each merge taking the quicker of the two fronts twice. O(n log n) for the sort, O(n) after |
| `min_build_time_search.kara` | a binary search on the answer: within a time `t`, a block of time `b` may sit `(t - b) / split` splits deep, and the blocks fit when, counting up from the deepest level, each level's own blocks and the parents of the level below, two children to a parent, come to one worker at the top (Kraft's inequality) |
| `min_build_time_table.kara` | a table over the blocks sorted slowest first, `best[i][w]` the time to build blocks `i..` with `w` workers on hand: every worker splits at once, or one builds block `i` and the rest carry on. O(n^2) |
| `min_build_time_heap.kara` | a Rust solution as LeetCode's Rust users write it (Huffman's merge on a `BinaryHeap<Reverse<i32>>`, collected from `blocks.into_iter().map(Reverse)`), carried to Kāra by `karac fix` |
| `min_build_time_memo.kara` | another Rust solution, the table as a recursion with a memo (the blocks sorted by `sort_unstable_by(|a, b| b.cmp(a))`, a nested `fn dp(i, w, blocks: &[i32], split, memo: &mut Vec<Vec<i32>>)`, and `i32::MAX` for no worker on hand), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six more properties |

Every arm prints the same 16 lines: LeetCode's three examples; four
equal blocks (`[5, 5, 5, 5], split 2: 9`); one slow block among quick
ones, built by a worker that splits off first (`[1, 1, 1, 100], split
10: 110`, and `[10, 1, 1, 1, 1], split 3: 13`); 1000 blocks of 1 and of
100000 with a split of 100 (`1001`, `101000`); 512, 1000 and 513 blocks
of 7 with a split of 1 (`16`, `17`, `17`: nine splits make 512 workers,
and the 513th block needs a tenth); 1000 random block sets of up to 12
blocks (`1000 random block sets: total 62277, checksum 44952850`); and
1000 random blocks up to 10^5 with a split of 100 and of 1 (`100090`,
`99891`). `min_build_time.py` mirrors the ★ arm with `heapq`, and its
output is byte-identical. Every arm gives the same output under `karac
run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, queues and table arms check clean as written. The
search arm, which only reads its blocks, takes two fixes, the harness's
two `.clone()`s on its arguments dropped. The heap arm takes one round
of 19 fixes (among them both `use`s dropped, `BinaryHeap<Reverse<i32>>`
to `PriorityQueue[Reverse[i32]]` built by `max_first_from`, the tuple
struct `Reverse(b)` to `Reverse { value: b }` in the pattern, the push
and the `.0`), and the memo arm one round of 25 (among them the nested
`fn dp` moved out to the top level, `&[i32]` to `Slice[i32]`, `&mut
Vec<Vec<i32>>` to `mut ref Vec[Vec[i32]]`, `usize` to `i64`, `i32::MAX`
to `i32.MAX`, `vec![vec![-1; n + 1]; n + 1]` to `Vec.filled(n + 1,
Vec.filled(n + 1, -1))`, and `mut blocks: Vec<i32>` to `blocks: own
Vec[i32]` with a `let mut blocks = blocks;`). Both outputs match.

## Gaps

The heap arm found one, filed. In Rust, `blocks: Vec<i32>` is owned and
`blocks.into_iter()` consumes it for free. `karac fix` turns the type
into `Vec[i32]`, a bare parameter, which borrows, and then answers the
move out of it with `blocks.clone().into_iter()`: the right answer, and
a copy of every block on every call that the Rust never made. The hint
names `.clone()` and a borrowing method but not `own`, which keeps the
Rust's meaning, and which `karac fix` already writes for Rust's `mut
weight: Vec<i32>` (kata 1196) and for `arr: Vec<i32>` rebound by `let
mut arr = arr` (kata 1200). kara B-2026-11-18-31.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: one worker with a set of blocks builds a single block at
once, and with two or more must split, each new worker taking a part,
the split costing `split` and the slower part setting the rest; every
way to part every set is tried, memoized over the sets as bitmasks. 2000
random sets of 1 to 7 blocks of 1 to 5, 20 or 100, with a split of 1 to
20.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | at least the slowest block, and at most that and a split for each level of a balanced tree, `ceil(log2 n)` |
| P3 | the blocks reversed take as long |
| P4 | a split one dearer takes as long or longer |
| P5 | one more block takes as long or longer |
| P6 | every block one longer takes exactly one longer |
| P7 | the ★ arm's answer |

All 84,000 checks pass on every arm: `2000 block sets: checksum
964807038, 84000 checks over 6 arms: 0 failures`, under `karac
__mir-run`, `karac run`, `karac build` and the AddressSanitizer build.
A Python reading of the same sets, trying every parting, gives the same
checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the quicker of the two kept | P1 1675, P2 523, P5 125, P7 8375 |
| S2 | ★: the slowest merged first | P1 1680, P2 896, P5 319, P7 8400 |
| Q1 | queues: the slower front taken | P1 1368, P2 211, P4 31, P5 169, P7 1368 |
| Q2 | queues: a merge takes split more than the quicker | P1 1675, P2 523, P5 125, P7 1675 |
| B1 | search: two workers at the top allowed | P1 1704, P7 1704 |
| B2 | search: an odd level's parents rounded down | P1 1675, P7 1675 |
| T1 | table: a split adds one worker | P1 782, P2 638, P7 782 |
| T2 | table: the quicker of a block and the rest sets the time | P1 1704, P2 485, P5 181, P7 1704 |
| H1 | heap: the slowest merged first | P1 1680, P2 896, P5 319, P7 1680 |
| H2 | heap: a split one cheaper | P1 1704, P7 1704 |
| M1 | memo: the quickest block left sets the time | P1 1597, P2 637, P5 241, P7 1597 |
| M2 | memo: the builder still on hand | P1 1704, P7 1704 |

1704 of the 2000 sets have two blocks or more, and B1, H2 and M2 fail on
every one of them: each saves a split somewhere it cannot be saved. A
mutation of the ★ arm fails P7 on all six arms, the ★ arm against the
other five. S1 and Q2 are one fault in two arms, a merge charged on the
quicker block, and fail alike; so are S2 and H1, the slowest merged
first. P3, the blocks reversed, catches none, since every arm sorts or
queues the blocks first, and P6, every block one longer, none either:
each mutation still adds the same one to every leaf.

## Benchmarks

`bench/` times the ★ arm against the same algorithm in C, Rust, Go and
Python: 200 sets of 1000 blocks, the constraints' most, built once, with
times up to 10, 1000 and 100000 and splits of 1 to 100 in turn; then 50
rounds over the sets, each answer folded into a checksum. Every program
prints `50 rounds of 200 sets of 1000 blocks: checksum 107433778`. Each
call builds a smallest-first queue from a copy of the blocks: Kāra a
`PriorityQueue`, Rust a `BinaryHeap` of `Reverse`d times, C a binary
heap in an array, built bottom up, Go `container/heap`, and Python
`heapq`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac `e8dc4f7aa2`
plus the typechecker fix pushed as `ab7613763c`, on LLVM 22. A plain
`karac build` targets x86-64-v2, so the C and overflow-checked Rust
programs are also built at x86-64-v3 for comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.644 to 0.734 s | 0.722 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.641 to 0.776 s | 0.714 s |
| Rust (`rustc -O`) | 0.519 to 0.673 s | 0.649 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.622 to 0.684 s | 0.644 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.572 to 0.679 s | 0.649 s |
| C (`clang -O3`) | 0.990 to 1.129 s | 1.075 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.986 to 1.145 s | 1.087 s |
| Go | 2.498 to 2.644 s | 2.591 s |
| Python | 3.899 to 3.922 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on is about 10% ahead of Kāra (0.644 s
against 0.714 s), at the edge of the spread. C's hand-written heap takes
about 1.5x Kāra's time and Go's `container/heap`, which moves every time
through an `interface{}`, about 3.6x; no profile was taken. Python takes
only about 5.5x Kāra's time, since `heapq` runs in C.
