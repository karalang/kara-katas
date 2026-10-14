# 563. Binary Tree Tilt

Given the `root` of a binary tree, return the sum of every tree node's
tilt. The tilt of a tree node is the absolute difference between the sum
of all left subtree node values and all right subtree node values. If a
node does not have a left child, then the sum of the left subtree node
values is treated as `0`. The rule is similar if the node does not have
a right child.

```
root = [1,2,3]                ->  1
root = [4,2,9,3,5,null,7]     ->  15
root = [21,7,14,1,1,2,2,3,3]  ->  9
```

**Constraints:** the number of nodes is in `[0, 10^4]`; `-1000 <=
Node.val <= 1000`.

## Approaches

Every arm is `fn find_tilt(root: Option[TreeNode]) -> i64` over `shared
struct TreeNode { val: i64, mut left: Option[TreeNode], mut right:
Option[TreeNode] }`, the shape kata 543 uses.

| file | mechanism |
|---|---|
| `find_tilt.kara` ★ | one recursive walk returning each subtree's sum and adding each node's tilt to a `mut ref` total; O(n) time, O(h) stack |
| `find_tilt_pair.kara` | the same walk with no running total: each subtree returns its sum and its tilt as a tuple; O(n) time, O(h) stack |
| `find_tilt_stack.kara` | post-order with an explicit stack of `(TreeNode, bool)`: each node visited twice, the second time taking its children's sums off a second stack; O(n) |
| `find_tilt_naive.kara` | the statement as written: every node's two subtrees summed from scratch; O(n h) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 13 lines: eight trees at the edges (the three
examples, no nodes, one node, a left chain, negative values and the
problem's extreme values), a count and checksum over 300 random trees of
1 to 80 nodes, and four trees of 10,000 nodes, the problem's most: a
random one, a chain down the left, two chains from the root and a
complete tree. `find_tilt.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: for every node, the values of its left
subtree and of its right subtree listed out breadth first and added up,
and the differences' sizes summed. Each arm is held to the properties
below on 1,000 random trees of 0 to 30 nodes, leaning left with chance
20 to 80 in 100, with values in -3 to 3 or in -1000 to 1000, in turn.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the answer is at least 0, at most the node count times the sum of the values' sizes, and 0 for a tree of one node or none |
| P3 | the tree mirrored, every node's children swapped, gives the same answer |
| P4 | the values negated give the same answer |
| P5 | the values tripled give three times the answer |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the difference's sign kept, not its size | P1 855, P2 460, P3 901, P4 901 |
| M2 | ★: a subtree's sum without its root | P1 919 |
| M3 | pair: the children's tilts dropped, only each node's own kept | P1 873 |
| M4 | pair: a subtree's sum without its right side | P1 827, P3 842 |
| M5 | stack: the two sums added, not subtracted | P1 832 |
| M6 | stack: a missing right child counted as the node's value | P1 962, P2 51, P3 831 |
| M7 | naive: the left subtree's tilts skipped | P1 833, P3 846 |
| M8 | naive: every value's size summed, not the value | P1 815 |
| E1 | ★: the difference taken the other way round | 0 |
| E2 | pair: the tilt taken by destructuring the tuple | 0 |
| E3 | stack: the sums stack given room for 64 up front | 0 |
| E4 | naive: a subtree's sum added in another order | 0 |

P5 sees none of them: every mutant still adds up values and their
differences, which scale with the values. Mirroring swaps left and
right, so the mutants that treat the two sides differently, M4, M6 and
M7, fail P3; M1 keeps signs, which mirroring and negating both flip.
M8 sums the sizes of the values, which negating leaves alone, so
P4 cannot see it. E3 is safe because a `Vec` grows past its first room
as it needs to.

## Verification

Every arm prints the same output as `find_tilt.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes on every arm, the differential and the bench program.

The frozen legacy backends, as for kata 543, whose harness this one
shares: `karac run --interp` prints the right output for the ★ and stack
arms, and the pair and naive arms print the first 11 and 10 lines and
are still on the 10,000-node trees when a 60 s limit stops them. `karac
run` and `karac build` fail on every arm in code generation, the
harness's `show` called with a string literal and a `vec!` ("Call
parameter type does not match function signature"). The differential
stops at type checking on `*v` over `values.iter()` of a `Vec[i64]`
("unary '*' requires 'ref T' ... found 'i64'"). The bench program builds
under the legacy `karac build`, but the binary aborts before it prints
with `malloc_consolidate(): unaligned fastbin chunk detected`, a
corrupted heap. Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm, on kata 543's workload with this
kata's values. It makes 20 random trees of 10,000 nodes (the problem's
most) once, values from -1000 to 1000, each new node walking down from
the root and going left with chance 50 to 88 in 100, keeping the nodes
in the order they were added. Then 1,000 times over every tree the
subtree at one of its first 16 nodes, picked by the round and the tree,
is answered; the picked node changes with the round, so the call cannot
be lifted out of the loop. Every implementation prints `20 trees,
1000 times each: tilts 47807589674, checksum 248363470`, the Kāra
program under `karac __mir-run` included (147 s).

Rust uses LeetCode's `Option<Rc<RefCell<TreeNode>>>`, reference counted
as Kāra's `shared struct` is; C and Go use plain pointers, Python a
class with `__slots__`. Spot timings on a shared 4-core container, three
runs each (two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.04 to 1.16 s |
| Rust (`rustc -O`) | 1.56 to 1.59 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.20 to 2.34 s |
| Go | 1.25 to 1.34 s |
| Python | 15.8 to 17.0 s |
| Kāra (`karac build --mir`) | 2.14 to 2.28 s |

The legacy `karac build` binary aborts (see Verification). So `bench.sh`
builds the Kāra program with `karac build --mir`, the v2 compiled
backend; that edit is by hand, on top of the `scripts/new-bench.sh`
output. The `--mir` row is timed at kara `e17ae2b58d`. Under `karac
__mir-llvm-run` the program prints the same line in 3.2 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark. The Kāra row is about level with Rust's with overflow
checks on, the equal-safety comparison, and about 1.4 times plain `rustc
-O`.

## Compiler findings

None new. Nothing was filed from this kata; the legacy failures above
are not filed because legacy is frozen.
