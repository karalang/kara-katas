# 545. Boundary of Binary Tree

The boundary of a binary tree is the concatenation of the root, the left
boundary, the leaves ordered from left to right, and the reverse order
of the right boundary. The left boundary is the set of nodes defined by
the following: the root node's left child is in the left boundary (if
the root does not have a left child, the left boundary is empty); if a
node is in the left boundary and has a left child, then the left child
is in the left boundary; if a node is in the left boundary, has no left
child, but has a right child, then the right child is in the left
boundary; the leftmost leaf is not in the left boundary. The right
boundary is similar to the left boundary, except it is the right side of
the root's right subtree, and the rightmost leaf is not in the right
boundary. The leaves are nodes that do not have any children; for this
problem, the root is not a leaf. Given the `root` of a binary tree,
return the values of its boundary.

```
root = [1,null,2,3,4]                    ->  [1,3,4,2]
root = [1,2,3,4,5,6,null,null,null,7,8,9,10]  ->  [1,2,4,7,8,9,10,6,3]
```

**Constraints:** the number of nodes in the tree is in the range
`[1, 10^4]`; `-1000 <= Node.val <= 1000`.

## Approaches

Every arm is `fn boundary_of_binary_tree(root: Option[TreeNode]) ->
Vec[i64]` over a `shared struct TreeNode` with `val`, `left` and
`right`.

| file | mechanism |
|---|---|
| `boundary_of_binary_tree.kara` ★ | three walks: a loop down the left boundary, a recursive walk for the leaves, and a loop down the right boundary, collected and then read backwards |
| `boundary_of_binary_tree_flags.kara` | one pre-order walk below the root carrying whether a node is on the left and on the right boundary; left-boundary nodes and leaves are written on the way down, right-boundary nodes on the way back up |
| `boundary_of_binary_tree_stack.kara` | no recursion: the boundaries as loops and the leaves from a pre-order walk on an explicit stack; the right boundary is popped off a stack onto the answer |
| `boundary_of_binary_tree_mirror.kara` | one function reads the left side (the left boundary and the leaves); run on the tree and on a mirrored copy, the copy's left boundary read backwards is the tree's right boundary |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 14 lines: both examples, one node, a root with
only a left or only a right child, a chain down the left, a zigzag on
each side, and a full tree of three levels, each with its answer; then
for 300 random trees of 1 to 80 nodes (each new node walking down from
the root and going left with chance 50, 80 or 95 in 100 in turn) the
total length and a checksum; and last four trees of 10,000 nodes (the
problem's most): a random one, a chain down the left, a chain down the
right and a complete tree, each by its length, first and last value and
a checksum. `boundary_of_binary_tree.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: both boundary paths walked in full and
their leaf dropped, the leaves gathered by a separate survey of the
tree. Each arm is held to the properties below on 1,000 random trees of
1 to 40 nodes holding 1 to n once each, so a value names its node,
leaning left with chance 50, 80 or 95 in 100 in turn.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the tree mirrored left to right gives the root and then the rest of the answer backwards |
| P3 | no node twice, and every leaf there |
| P4 | after the root, the nodes before the first leaf go down one level a step from depth 1, and those after the last leaf come back up one level a step to depth 1 |
| P5 | between them come exactly the leaves, left to right |

The survey records each node's depth by its value, `depths[n.val] =
depth`. `karac check` refused that line on every backend until kara
B-2026-10-14-1 was fixed (`56b330ae8b`, below); the mutation results in
the next section are from a copy that read the value into a local first,
`let v = n.val; depths[v] = depth;`, the only change. Rechecked at kara
`a87257d083`, the file here runs as written and prints `1000 cases,
4 arms, 20000 checks, 0 failures` under `karac __mir-run`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the left boundary only ever goes left | P1 64, P2 221 |
| M2 | ★: the right boundary read top down | P1 433, P2 901, P4 433 |
| M3 | flags: a right child kept on the left boundary beside a left one | P1 711, P2 738, P5 711 |
| M4 | flags: a left child kept on the right boundary beside a right one | P1 373, P2 738, P5 373 |
| M5 | stack: a node with no left child taken as a leaf | P1 501, P2 943, P3 290, P4 196, P5 434 |
| M6 | stack: a root with one child returned alone | P1 189, P3 189, P5 189 |
| M7 | mirror: the right side read from the tree, not its mirror | P1 951, P2 951, P3 940 |
| M8 | mirror: the left boundary not stopped at its leaf | P1 979, P3 979, P5 979 |
| E1 | ★: no early return for a lone root | 0 |
| E2 | flags: the right boundary's check without `not on_left` | 0 |
| E3 | stack: no early return for a lone root | 0 |
| E4 | mirror: the left boundary copied in, not moved | 0 |

M1 passes P3 to P5: stopping the left boundary where it should turn
right leaves a shorter path that still goes down a level a step, and
every leaf is still there. Only the definition and the mirror (P2) see
the nodes it drops. M7 writes the left boundary again where the right
one belongs; read backwards it climbs one level a step to depth 1, so
P4 passes it, and P3 sees the repeated nodes. P2 is the strongest
property here, since mirroring swaps the two boundaries and reverses the
leaves, so any asymmetric mistake shows on one side or the other; it
misses M6 and M8, which treat both sides alike. E2 is safe because no
node below the root is on both boundaries: the root's left subtree
starts on the left one and its right subtree on the right one.

## Verification

Every arm prints the same output as `boundary_of_binary_tree.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes on every arm, the differential and the bench program. The
differential prints `20000 checks, 0 failures` under `__mir-run` and
`__mir-llvm-run` and runs clean under `__mir-llvm-asan` (rechecked at
kara `a87257d083`, after B-2026-10-14-1 was fixed).

The frozen legacy backends: `karac run --interp`, `karac run` and `karac
build` stop every arm, the differential and the bench program at type
checking, on `*v` over `iter()` of a `Vec[i64]` ("unary '*' requires
'ref T' ... found 'i64'"). Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 random trees of
10,000 nodes (the problem's most) with values from -1,000 to 1,000, each
new node walking down from the root and going left with chance 50 to
88 in 100, once, keeping the nodes in the order they were added. Then
200 times over every tree the subtree at one of its first 16 nodes,
picked by the round and the tree, is answered, and every value on the
boundary goes into the checksum. Every implementation prints `20 trees,
200 times each: 4021456 on the boundary, checksum 167516461`, the Kāra
program under `karac __mir-run` included (37.9 s).

Rust uses LeetCode's `Option<Rc<RefCell<TreeNode>>>`, reference counted
as Kāra's `shared struct` is; C and Go use plain pointers, C with a
growable array for the answer, Python a class with `__slots__`. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.27 to 0.28 s |
| Rust (`rustc -O`) | 0.37 to 0.41 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.38 to 0.40 s |
| Go | 0.30 to 0.33 s |
| Python | 3.57 to 3.59 s |
| Kāra (`karac build --mir`) | 0.40 to 0.41 s |

The legacy `karac build` refuses this program (see Verification). So
`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`2b8238c108`. Under `karac __mir-llvm-run` the program prints the same
line in 1.6 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark. The Kāra row is level
with Rust's.

## Compiler findings

kara B-2026-10-14-1, filed from this kata and fixed in kara
`56b330ae8b`: `v[n.val] = x` was refused with "shared struct field
'Node.val' is not declared mut" when the index reads a non-`mut` field
of a `shared struct`. The flag that marks the target of an assignment
reached the index expression, so a read of `n.val` was checked as a
write to it. `v[n.val] += x`, `let i = n.val; v[i] = x` and a plain
struct's field as the index all passed. Met here in the differential's
`depths[n.val] = depth`, which now runs as written.
