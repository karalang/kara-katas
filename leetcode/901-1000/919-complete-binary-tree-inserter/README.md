# 919. Complete Binary Tree Inserter

A complete binary tree is a binary tree in which every level, except
possibly the last, is completely filled, and all nodes are as far left
as possible.

Design an algorithm to insert a new node to a complete binary tree,
keeping it complete after the insertion.

Implement the `CBTInserter` class:

- `CBTInserter(TreeNode root)` initializes the data structure with the
  `root` of the complete binary tree.
- `int insert(int v)` inserts a `TreeNode` into the tree with value
  `Node.val == val` so that the tree remains complete, and returns the
  value of the parent of the inserted `TreeNode`.
- `TreeNode get_root()` returns the root node of the tree.

```
["CBTInserter", "insert", "insert", "get_root"]
[[[1, 2]], [3], [4], []]
->  [null, 1, 2, [1, 2, 3, 4]]
```

**Constraints:** the number of nodes in the tree is in the range
`[1, 1000]`; `0 <= Node.val <= 5000`; `root` is a complete binary tree;
`0 <= val <= 5000`; at most `10^4` calls are made to `insert` and
`get_root`.

## Approaches

In a complete tree the nodes fill level order without a gap, so the new
node always takes the first free child slot in level order.

| file | mechanism |
|---|---|
| `cbt_inserter.kara` ★ | a `VecDeque` of the nodes missing a child, in level order, found by one walk at the start: `insert` gives the front node a left child, or else a right child and drops it from the queue, and queues the new node. O(n) to build, O(1) an insert |
| `cbt_inserter_array.kara` | every node in a `Vec` in level order, the heap layout: the node at index `i` hangs under index `(i - 1) / 2`, on the left when `i` is odd. O(n) to build, O(1) an insert |
| `cbt_inserter_bits.kara` | only the root and the count: the new node's number, from 1 in level order, spells its path in binary after the leading 1 (0 left, 1 right), so `insert` follows every digit but the last from the root. O(n) to count once, O(log n) an insert, O(1) extra space |
| `cbt_inserter_levels.kara` | two `Vec`s, the deepest full level and the level being filled below it: the k-th new child goes under node `k / 2` of the full level, and a filling level twice as long as the full one becomes the full one. O(1) amortised an insert |
| `cbt_inserter_map.kara` | a `Map[i64, TreeNode]` from each node's number to the node, filled by a recursive walk: node `k`'s parent is node `k / 2`. O(1) expected an insert |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: six small cases (LeetCode's example,
a single node given seven children in turn, a full tree of three, a
tree one node short of full, a full tree of seven, and zeros beside a 5,000), each
with the parents returned, the tree in level order and whether it is
complete; for 200 random trees of 1 to 1,000 nodes with up to 1,000
inserts, the parents' sum (250,912,990), a checksum and that every tree
stayed complete; and LeetCode's largest, 1,000 nodes and 10,000 inserts.
`cbt_inserter.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: to insert, try the new node in every free child slot of the
tree, keep the slots where a level-order walk finds no node after a gap
(the tree is complete), and require exactly one such slot; the starting
tree is grown from its first value the same way. It checks 3,200 random
cases: 3,000 trees of 1 to 12 nodes with 0 to 8 inserts of values below
4 against the statement, and 200 trees of 1 to 200 nodes with up to 200
inserts of values up to 5,000 against the other properties; 69,504
nodes in all.

| | property |
|---|---|
| P1 | the statement's parents and final tree, on the small cases |
| P2 | `get_root` before any insert is the tree given, and after them its level order is the starting values followed by the inserted ones |
| P3 | the tree stays complete, with one more node for each insert and one parent returned for each |
| P4 | the j-th insert's parent is the node at `(n + j - 1) / 2` in the final level order |
| P5 | starting from the tree with the first m inserts already in (m random) gives the same parents for the rest, and the same tree |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 cases, 69504 nodes, parents summing to 44645194, 95000
checks over 5 arms: 0 failures` under `karac __mir-run` (31 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a node never leaves the queue once full | P1 2166, P2 2365, P3 2365, P4 2156, P5 1835, P6 2365 |
| M2 | ★: only nodes missing both children queued at the start | P1 1336, P3 1444, P4 1325, P5 704, P6 1444 |
| M3 | ★: a new node queued at the front | P1 2360, P3 2560, P4 2448, P5 1259, P6 2560 |
| M4 | array: the parent taken as node `i / 2` | P1 2520, P2 2154, P3 2720, P4 2495, P5 1222, P6 2720 |
| M5 | array: left and right children swapped | P1 2638, P2 2612, P3 2311, P5 1835, P6 2838 |
| M6 | array: right children left out of the starting walk | P1 2255, P2 2452, P3 2452, P4 2277, P5 2123, P6 2452 |
| M7 | bits: the count leaving out the right subtree | P1 2255, P2 2452, P3 2452, P4 2298, P5 2123, P6 2452 |
| M8 | bits: the new node numbered before the count goes up | P1 2691, P2 2861, P3 2869, P4 2470, P5 2242, P6 2891 |
| M9 | bits: the top bit found one too low for a power of two | P1 1749, P2 1904, P3 1904, P4 1743, P5 1180, P6 1904 |
| M10 | levels: the filling level not emptied when it becomes the full one | P1 1393, P3 1547, P4 1370, P5 624, P6 1547 |
| M11 | levels: the parent wrapping round the full level | P1 2444, P2 2146, P3 2644, P4 2429, P5 1237, P6 2644 |
| M12 | levels: left children first across the whole level | P1 2405, P2 2512, P3 2605, P5 1669, P6 2605 |
| M13 | map: the parent taken as the node numbered just before | P1 2666, P3 2866, P4 2757, P6 2866 |
| M14 | map: the new node's own value returned | P1 2582, P4 2782, P6 2782 |
| M15 | map: the parent recorded under the new number | P1 597, P2 689, P3 689, P4 601, P5 538, P6 689 |

P1 and P6 kill all fifteen; P3 fourteen, P4 and P5 thirteen, and P2
ten. P2 compares only the values in level order, which skip the gaps, so
it misses the mutants that put each new node in a wrong but later place
(M2, M3, M10, M13) and the one that returns a wrong value into a right
tree (M14); P3 sees all of those but M14. P4 misses the two that swap
left and right (M5, M12), since the parent is still right. P5 misses
M13 and M14, which make the same mistake whether the first inserts were
made before or after the start.

Four mutants were replaced. The first M13 (map: the parent numbered
`(k + 1) / 2`) failed exactly the same checks as M4, as it is the same
mistake: the node at index `i` is number `i + 1`. The first M8 (bits:
the new node on the wrong side) and the first M14 (map: the count one
short) stopped at runtime on `unwrap()` of a missing node, and the first
M10 (levels: the filling level promoted when half full) on an index out
of bounds, so none of the three reached the properties.

## Verification

Every arm prints the same output as `cbt_inserter.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 3.3 to 6.4 s each (the bits arm,
which counts the starting tree recursively, the longest) and the
differential 31 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy compiler refuses every arm, the differential and the
bench program at the first `*` on an element of a `Vec[i64]`'s
`.iter()`, in the harness's `complete_tree` ("unary '*' requires 'ref
T', ... found 'i64'"), legacy's older rule; under v2 the element is a
reference and the `*` is required. Legacy is frozen, so none of this is
filed.

## Benchmarks

The bench program uses the ★ arm. Each of 200 rounds builds a fresh
complete tree of 1,000 random values below 100,000, makes an inserter
over it and inserts 50,000 more, so the tree reaches 51,000 nodes and
the round ends by freeing it. Every implementation prints `200 rounds of
50000 inserts into trees of 1000: parents summing to 163793529947,
checksum 608440678`. Rust uses LeetCode's `Rc<RefCell<TreeNode>>` nodes,
Go pointers under its collector, and C `malloc` and `free` with a ring
buffer for the queue.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.35 to 0.42 s | 0.37 s |
| Rust (`rustc -O`) | 0.48 to 0.57 s | 0.51 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.49 to 0.63 s | 0.53 s |
| Go | 0.46 to 0.53 s | 0.48 s |
| Python | 6.5 s | |
| Kāra (`karac build --mir`) | 0.46 to 0.58 s | 0.51 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about eighteen times C's.

v2 takes 0.96 times Rust's median time under overflow checks and 1.38
times C's. Under valgrind's cachegrind v2 runs 6.18 billion instructions
and 0.99 billion branches, against 4.88 billion and 0.88 billion for
Rust with overflow checks and 4.37 billion and 0.69 billion for C; v2
and Rust both mispredict about 11 million, C 16 million (2.3%). v2's
extra instructions do not show in its time, which suggests that the
allocation and the memory traffic of 10 million new nodes dominate all
three; that is inferred, not profiled.
