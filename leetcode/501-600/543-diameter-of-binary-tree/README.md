# 543. Diameter of Binary Tree

Given the `root` of a binary tree, return the length of the diameter of
the tree. The diameter of a binary tree is the length of the longest
path between any two nodes in a tree. This path may or may not pass
through the `root`. The length of a path between two nodes is
represented by the number of edges between them.

```
root = [1,2,3,4,5]  ->  3   (the path 4 -> 2 -> 1 -> 3 or 5 -> 2 -> 1 -> 3)
root = [1,2]        ->  1
```

**Constraints:** the number of nodes in the tree is in the range
`[1, 10^4]`; `-100 <= Node.val <= 100`.

## Approaches

Every arm is `fn diameter_of_binary_tree(root: Option[TreeNode]) ->
i64` over a `shared struct TreeNode` with `val`, `left` and `right`.

| file | mechanism |
|---|---|
| `diameter_of_binary_tree.kara` ★ | one recursive walk returning each subtree's height in nodes and raising a `mut ref` best to the path bending at each node, the two children's heights added |
| `diameter_of_binary_tree_pair.kara` | the same walk returning a pair, the subtree's height and its longest path, with nothing kept outside it |
| `diameter_of_binary_tree_stack.kara` | the walk in post-order with an explicit stack, each node pushed once to open and once to finish, the heights on a second stack |
| `diameter_of_binary_tree_bfs.kara` | the tree as an undirected graph, nodes numbered in level order; a breadth-first search from the root finds one end of a longest path and a second from there its length |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 12 lines: both examples, one node, a chain
down the left, a zigzag, a tree whose longest path misses the root, and
a full tree of three levels, each with its answer; then for 300 random
trees of 1 to 80 nodes (each new node walking down from the root and
going left with chance 50, 80 or 95 in 100 in turn) the total and a
checksum; and last four trees of 10,000 nodes (the problem's most): a
random one, a chain down the left, two chains from the root, and a
complete tree. `diameter_of_binary_tree.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every node numbered with its parent and depth, and for every pair of
nodes the deeper one climbs until the two meet, one edge a step; the
answer is the most steps. Each arm is held to the properties below on
1,000 random trees of 1 to 40 nodes, leaning left with chance 50, 80 or
95 in 100 in turn, with a second random tree for P5.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the tree mirrored left to right has the same answer |
| P3 | the answer is at most nodes - 1, and from height - 1 to 2 (height - 1), the height counted in nodes |
| P4 | under a new root, as its left child, the answer is the larger of the old one and the old height |
| P5 | joined with a second tree under a new root, the answer is the largest of the two answers and the two heights added |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the path through a node counted in nodes, not edges | P1 768, P3 204, P4 74, P5 753 |
| M2 | ★: a node's height taken from its shorter child | P1 931, P3 715, P4 898, P5 1000 |
| M3 | pair: only the path through the root | P1 75, P4 628, P5 83 |
| M4 | pair: the right subtree's own path left out | P2 75, P5 44 |
| M5 | stack: an empty child given height 1 | P1 1000, P3 463, P4 173, P5 855 |
| M6 | stack: the last node finished, not the best one | P1 75, P4 628, P5 83 |
| M7 | bfs: the second search from the root again | P1 827, P5 1000 |
| M8 | bfs: a farther node taken only when two farther | P1 703, P3 155, P4 543, P5 757 |
| E1 | ★: best raised on a tie too | 0 |
| E2 | pair: the three candidates in another order | 0 |
| E3 | stack: the height's max taken the other way round | 0 |
| E4 | bfs: the last farthest node kept on a tie | 0 |

M4 is the one P1 misses. It goes wrong only at a node whose longest path
lies wholly in its right subtree and beats both its left subtree's and
the one bending at the node. The trees lean left, so that is rare, and
none of the 1,000 has one; mirroring the tree (P2) moves those paths to
the left, where M4 does look, and catches it 75 times. P4 is what
catches a walk that keeps only the root's path (M3, and M6, the same
mistake in the stack arm): a new root above the tree makes the old
root's path an inner one. Only M4 is asymmetric, so P2 kills nothing
else. A first M8, the bfs arm taking the left child twice and the right
one never, made a graph that doubled at every level; its run was stopped
after seven minutes and the edit replaced.

## Verification

Every arm prints the same output as `diameter_of_binary_tree.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `20000 checks, 0 failures` on the first two and runs clean under
the third. `karac check` passes on every arm, the differential and the
bench program.

The frozen legacy backends: `karac run --interp` prints the right output
for the ★, pair and stack arms. `karac run` and `karac build` fail on
those three in code generation, the harness's `show` called with a
string literal and a `vec!` ("Call parameter type does not match
function signature"). The bfs arm and the differential stop at type
checking on `*v` over `adj[u].iter()` of a `Vec[i64]` ("unary '*'
requires 'ref T' ... found 'i64'"). The bench program builds under
legacy `karac build`, but the binary aborts before it prints with
`malloc_consolidate(): unaligned fastbin chunk detected`, a corrupted
heap. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 random trees of
10,000 nodes (the problem's most), each new node walking down from the
root and going left with chance 50 to 88 in 100, once, keeping the nodes
in the order they were added. Then 200 times over every tree the subtree
at one of its first 16 nodes, picked by the round and the tree, is
answered; the picked node changes with the round, so the call cannot be
lifted out of the loop. Every implementation prints `20 trees, 200 times
each: diameters 152698, checksum 134803681`, the Kāra program under
`karac __mir-run` included (29.1 s).

Rust uses LeetCode's `Option<Rc<RefCell<TreeNode>>>`, reference counted
as Kāra's `shared struct` is; C and Go use plain pointers, Python a
class with `__slots__`. Spot timings on a shared 4-core container,
three runs each (two for Python; `bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.23 to 0.27 s |
| Rust (`rustc -O`) | 0.35 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.37 to 0.39 s |
| Go | 0.25 to 0.26 s |
| Python | 3.83 to 4.07 s |
| Kāra (`karac build --mir`) | 0.43 to 0.45 s |

The legacy `karac build` binary aborts (see Verification). So
`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`2b8238c108`. Under `karac __mir-llvm-run` the program prints the same
line in 1.5 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

The Kāra row is about 1.25 times Rust's. Under callgrind the walk
itself, `height`, runs 864 million instructions against Rust's
494 million and C's 314 million. Read off the compiled code: each visit
adds one to the node's count and takes it off again, as Rust's `RefCell`
borrow does, and passes the child, the result and the `mut ref` through
stack slots, the v2 backend's by-pointer calling convention. Nothing
here is filed; the calling convention is the M2 backend's chosen shape.

## Compiler findings

None filed from this kata.
