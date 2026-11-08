# 1506. Find Root of N-Ary Tree

You are given all the nodes of an N-ary tree as a list of `Node` objects,
each with a unique value and the list of its children, in no particular
order. Return the root.

```
tree = [1,null,3,2,4,null,5,6]                      ->  root 1 (children 3, 2, 4)
tree = [1,null,2,3,4,5,null,null,6,7,null,8,null,9,10,null,null,11,null,12,null,13,null,null,14]
                                                    ->  root 1 (children 2, 3, 4, 5)
```

The tree is given in LeetCode's level-order form; the judge flattens it to
a list of nodes, shuffles it, and checks that the node returned serializes
back to the same tree.

**Constraints:** `1 <= n <= 5 * 10^4`; values are unique, `0 <= val <= 5 * 10^4`.
Follow-up: constant extra space, linear time.

## Approaches

| file | mechanism |
|---|---|
| `root.kara` ★ | every value but the root's appears once as a child, so the sum of all values less the sum of all children's values is the root's; then find the node with it. O(n) time, O(1) space |
| `root_xor.kara` | the same with XOR: each child's value meets itself twice and cancels. O(n), O(1) |
| `root_set.kara` | collect every child's value in a `Set`, return the node that is not in it. O(n), O(n) |
| `root_iter.kara` | the set arm with iterators: `flat_map` over the children into a `Set`, then `find` |
| `differential.kara` | the four arms against the statement read literally, six properties |

LeetCode offers no Rust template for this problem, so there is no
Rust arm.

Every arm prints the same 7 lines: the root of LeetCode's two examples
and two more, each listed leaves first, then a checksum of every root
value for 3000 trees of 1 to 10 nodes, 300 of 1 to 300, and 3 of 1 to
50000, each with distinct values up to 50000 and its nodes shuffled.
`root.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: for each node, look through every node's children for it, and
return the first that no one holds. It checks 3000 trees of 1 to 10 nodes
with values below 64. Every random choice of a problem is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the root is the statement read literally |
| P2 | the nodes listed in another order leave the root |
| P3 | every value mapped to `3 v + 7` maps the root's the same way |
| P4 | the root reaches every node |
| P5 | a new node holding the root as its only child, put anywhere in the list, is the new root |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 11980928, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Twenty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Twelve are kept, three to
each arm. Fifteen are killed, each the same way under both backends and
none by a crash; five survive, all equivalent.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each child subtracted as one more than its value | P1 2155, P2 1944, P3 220, P4 2155, P5 2380, P6 2155 |
| M2 | ★: each value added capped at 500 | P5 2380 |
| M3 | ★: the first node at least the total taken, not equal | P1 1468, P2 1461, P4 1468, P6 1468 |
| M4 | xor: only the even bits of each child cancelled | P1 1078, P2 936, P3 1192, P4 1078, P5 1185, P6 1078 |
| M5 | xor: each node or-ed in, not xor-ed | P1 2139, P2 2025, P3 519, P4 2139, P5 2306, P6 2139 |
| M6 | xor: the root matched on its low five bits | P1 110, P2 100, P4 110, P5 262, P6 110 |
| M7 | set: each parent's value inserted, not the child's | P1 2688, P2 1475, P4 2688, P5 3000, P6 2688 |
| M8 | set: the first node held as a child returned | P1 2688, P2 1840, P4 2688, P5 3000, P6 2688 |
| M9 | set: only each node's first child inserted | P1 1489, P2 1444, P4 1489, P5 1445, P6 1489 |
| M10 | iter: each child's value off by one | P1 2132, P2 2068, P3 171, P4 2132, P5 2347, P6 2132 |
| M11 | iter: each node's first child skipped | P1 1877, P2 1916, P4 1877, P5 2223, P6 1877 |
| M12 | iter: the first listed node's children skipped | P1 412, P2 685, P4 412, P5 633, P6 412 |

P5 kills eleven of the twelve, and M2 only P5: the values of the drawn
trees stay below 64, so capping at 500 changes nothing until the new root
of value 1000 arrives. P3 sees the edits whose damage depends on the
values themselves.

The other three that are killed (the ★ arm without the children's
subtraction, the xor arm skipping each first child, the xor arm also
xor-ing each child's child count) fail as M1 or with the same properties
and add nothing. Five survive and are equivalent: the ★ and set arms'
fallback after the loop (never reached, since a root always exists), the
set arm inserting grandchildren too (they are children of someone
already), the iterator arm's `contains(..) == (val < 0)` (values are never
negative), and the iterator arm searching from the back (only one node is
the root).

## Benchmarks

The bench builds 20 trees of up to 50000 nodes once and finds each root
10 times by the ★ arm in all five languages. Every implementation prints `200 roots over 20 trees of up to 50000
nodes: checksum 453798400`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `acb9d4c5b` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.100 s |
| Rust (`rustc -O`) | 0.181 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.189 s |
| Kāra (`karac build`) | 0.271 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.277 s |
| Go | 0.280 s |
| Python | 2.02 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.273 s) is below its real time (0.343 s).

Kāra is 1.47x Rust under overflow checks by median. The gap is the
run-time borrow flags, B-2026-11-08-14: `Node` is a `shared struct` and
`children` is not a `mut` field, yet each `node.children.iter()` takes a
flag through `karac_mir_flag_acquire` and gives it back through
`karac_mir_flag_release`. Under callgrind those two are 23% and 16% of the
bench's instructions; on a ten-line program that only walks
`node.children` they are 46% and 31%. The flag pass flags every non-`Copy`
field of a shared value because MIR does not record which fields are
`mut`, but a field that is not `mut` can never be written, so its flag
never catches anything.

## Verification

The four arms print the same output as `root.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them.
Under `karac __mir-run` the differential takes 2.5 s.

## Writing it

The arms were written in Kāra. `karac fix` turned each `ref Vec[i64]`
parameter into a bare one and dropped the `*` on `Copy` closure
parameters. The level-order harness first sliced `tokens[2..]`, which is
out of bounds on a tree of one node (Python's `tokens[2:]` is empty);
`tokens.iter().skip(2)` is the Kāra that means the same.
