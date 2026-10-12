# 449. Serialize and Deserialize BST

Design an algorithm to serialize a binary search tree to a string and
deserialize the string back to the original tree. There is no
restriction on how it works; the encoded string should be as compact as
possible.

```
root = [2,1,3]  ->  [2,1,3]
root = []       ->  []
```

**Constraints:** the tree has `0` to `10^4` nodes; `0 <= Node.val <=
10^4`; the input tree is guaranteed to be a binary search tree.

## Approaches

Every arm is `fn serialize(root: Option[TreeNode]) -> String` and
`fn deserialize(data: Str) -> Option[TreeNode]`, over the same
`shared struct TreeNode`. A search tree is fixed by its preorder or its
postorder alone, so no arm writes markers for missing children.

| file | mechanism |
|---|---|
| `codec.kara` ★ | preorder, comma-separated; rebuilt by reading the values in turn, each call taking values while they fit the range its subtree allows. O(n) both ways |
| `codec_postorder.kara` | postorder, comma-separated; rebuilt by reading backwards, root first, then the right subtree, then the left, with the same ranges. O(n) both ways |
| `codec_insert.kara` | preorder, comma-separated; rebuilt by inserting the values one by one into an empty search tree, which puts each where it was. O(n · height) |
| `codec_compact.kara` | one character per node: the value plus 256, which keeps every code point clear of the ASCII control characters and below the surrogates. Rebuilt with a stack of the path to the last node: a smaller value is its left child, a larger one the right child of the last node on the path smaller than it. O(n) both ways |
| `differential.kara` | the four codecs on 1,500 random trees, five properties |

Every arm prints the same 8 lines: for each of seven trees (the LeetCode
example, the empty tree, one node, the two ends of the value range, an
ascending and a descending chain, and a ten-node tree), its preorder,
node count and height, and whether the tree and its text came back the
same after a round trip; then, for 300 random trees of 0 to 200 values
(inserted in random order, or one time in five in ascending order,
which makes a chain), the totals and a checksum of the preorders.
`codec.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four codecs and runs them on
1,500 random search trees of distinct values from 0 to 10,000: up to 2,
19 or 119 values, inserted in random order or one time in five in
ascending order.

| | property |
|---|---|
| P1 | deserializing the text gives back the same tree |
| P2 | serializing that tree again gives the same text |
| P3 | the rebuilt tree's inorder is the values, sorted |
| P4 | the same values inserted in another order give the same text exactly when they give the same tree |
| P5 | a tree of up to 30 consecutive values, at an end of the range two times in three, comes back the same |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | preorder: a right child one above its parent is lost | P1 98, P2 98, P3 98, P5 1417 |
| M2 | preorder: the value 0 is out of range | P1 6, P2 6, P3 6, P5 485 |
| M3 | postorder: reading starts one before the root | P1 1336, P2 1336, P3 1336, P5 1500 |
| M4 | postorder: a left child one below its parent is lost | P1 70, P2 70, P3 70, P5 1417 |
| M5 | insert: a new node is hung on the wrong side | P1 1146, P2 945, P3 1146, P5 1448 |
| M6 | insert: right subtrees are never written | P1 1061, P3 1061, P4 21, P5 1417 |
| M7 | compact: the root is never popped off the path | P1 681, P3 681, P5 1236 |
| M8 | compact: a value one below the top of the path is not its left child | P1 47, P3 47, P5 1371 |

P5 does most of the work: M1, M2 and M4 go wrong only on neighbouring
values (or on 0), which random trees over 10,001 values seldom hold and
runs of consecutive values always do. P4 compares only texts, so it sees
only M6, the one mutant in a serializer: dropping the right subtrees
makes some different trees write the same text. P2 misses M6, M7 and
M8, because a tree rebuilt wrongly from a text can still write that
text again: M6's text never held the right subtrees, and M7 and M8 keep
the preorder while hanging nodes in the wrong places.

The first M6 tried, writing the right subtree in place of the left,
writes each right subtree twice, so on an ascending chain of up to 119
nodes the text doubles at every level; it never finished and was
replaced.

## Verification

All four arms print the same output as `codec.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends every arm matches under
`karac run --interp`. LLJIT and `karac build` stop in the legacy code
generator on the `Str` parameter of `deserialize`: the three
comma-separated arms on `data.len()` ("no handler for method 'len' on
variable 'data'"), and the compact arm on `for c in data.chars()`, a
panic at `src/codegen/control_flow_for.rs:582`. The differential
prints `0 failures` under `karac run --interp`, and `karac build` stops
on the same `len`, as does the bench program. Legacy is frozen, so these are noted,
not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 10 random search trees of
50,000 values once (each a shuffle of every third number, heights 35 to
43), then serializes and deserializes each 20 times.
Every implementation prints `20 rounds on 10 trees of 50000: 62593600
characters, checksum 862159862`, the Kāra program under
`karac __mir-run` included (in 152 s).

The mirrors keep the ★ arm's structure: a recursive preorder writer
into one growing string, the text split on commas into a list of
numbers, and the recursive rebuild with bounds. Rust's tree is
`Rc<RefCell<TreeNode>>`, the closest match to a `shared struct`; C
frees each rebuilt tree, Go leaves it to the collector. Spot timings on
a shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.8 to 2.0 s |
| Rust (`rustc -O`) | 2.2 to 2.5 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.2 to 2.4 s |
| Go | 1.8 to 1.9 s |
| Python | 16.5 to 18.0 s |

The legacy `karac build` cannot build the bench program (the `len`
above), so there is no compiled Kāra time. The Kāra program prints the
same line under `karac __mir-llvm-run` in 14 s, compile included; that
JITs the MIR's IR without optimization passes, so it is not a
benchmark.

The time goes to formatting and parsing 3,000,000 numbers and
allocating as many nodes, which every language pays alike. Rust runs a
little behind C and Go; its reference-counted `RefCell` nodes are the
likely cost, though that is not measured here.

## Compiler findings

No new findings.
