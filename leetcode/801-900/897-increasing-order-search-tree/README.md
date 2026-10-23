# 897. Increasing Order Search Tree

Given the `root` of a binary search tree, rearrange the tree in
in-order so that the leftmost node in the tree is now the root of the
tree, and every node has no left child and only one right child.

```
root = [5,3,6,2,4,null,8,1,null,null,null,7,9]
    ->  [1,null,2,null,3,null,4,null,5,null,6,null,7,null,8,null,9]
root = [5,1,7]  ->  [1,null,5,null,7]
```

**Constraints:** the number of nodes in the given tree is in the range
`[1, 100]`, and `0 <= Node.val <= 1000`.

## Approaches

The chain holds the nodes in the order an in-order walk meets them,
which for a search tree is increasing order. The arms differ in how they
walk and in whether they reuse the nodes.

| file | mechanism |
|---|---|
| `increasing_bst.kara` ★ | an in-order walk that relinks as it goes: keeping the tail of the chain so far, starting from a placeholder head, each node reached loses its left child and becomes the tail's right child and the new tail. O(n) time, O(height) stack |
| `increasing_bst_values.kara` | the values in order, a new chain: the values read in order into a list, and a fresh chain built from the last value back. O(n) time and n new nodes |
| `increasing_bst_stack.kara` | the ★ arm's walk with a stack of its own: left as far as possible, stacking the nodes passed, then the top node relinked onto the tail and the walk going on from its right child. O(n) time, O(height) stack |
| `increasing_bst_vine.kara` | right rotations into a vine: below a placeholder head, rotate right at the top of the rest until it has no left child, then step down one, the first half of the Day-Stout-Warren balancing. O(n) time, O(1) space |
| `increasing_bst_pairs.kara` | each subtree flattened to a chain, head and tail: the left subtree's chain, the node and the right subtree's chain joined by pointing the left chain's last node at the node and the node at the right chain's first. O(n) time, O(height) stack |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples and five
more (one node, a tree that is already a chain, a chain of left
children, a balanced tree of three, and a tree whose root's left child
has only a right subtree), each in LeetCode's level order before and
after; three of LeetCode's largest trees, 100 nodes put in at random, in
increasing order and in decreasing order, each with the length of its
chain and a checksum of its values and shape; and 300 random trees of 1
to 100 nodes, 15,818 nodes in all, with a checksum. `increasing_bst.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the values of the given tree in order, the left subtree, the
node, the right, and the answer walked from its root down its right
children, each node holding the next value, none with a left child,
every one but the last with a right child, and the root holding the
smallest value. The arms rebuild the tree they are given, so every call
gets a fresh copy. It checks 3,200 random search trees: 3,000 of up to
12 nodes against the statement and 200 of up to 100 against the other
properties, their distinct values from 0 to 1,000 put in at random, in
increasing order or in decreasing order, 29,520 nodes in all.

| | property |
|---|---|
| P1 | the statement's chain, on the small cases |
| P2 | a chain with no left children holding all `n` values, each larger than the one before, from the smallest to the largest |
| P3 | the same values put in in increasing order give the same chain; and the chains of the root's left and right subtrees with the root between them make the whole chain |
| P4 | the chain rearranged again is itself |
| P5 | the tree mirrored with every value negated, itself a search tree, gives the chain backwards with every value negated |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every case. It prints `3200 cases, 29520 nodes,
95000 checks over 5 arms: 0 failures` under `karac __mir-run` and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the right subtrees never walked | P1 737, P2 809, P3 809, P4 547, P5 809, P6 809 |
| M2 | ★: the tail never moved on | P1 2741, P2 2938, P3 2938, P5 2938, P6 2938 |
| M3 | ★: each node hung on the left of the tail | P1 3000, P2 3200, P3 3200, P5 3200, P6 3200 |
| M4 | values: each value put at the front | P1 2741, P2 2938, P3 2938, P4 2938, P6 2938 |
| M5 | values: the first value left out | P1 3000, P2 3200, P3 2069, P4 2938, P5 3200, P6 3200 |
| M6 | values: the left subtrees never read | P1 1747, P2 1880, P3 1880, P5 2938, P6 1880 |
| M7 | stack: never going left | P1 1747, P2 1880, P3 1880, P5 2938, P6 1880 |
| M8 | stack: never going right | P1 737, P2 809, P3 809, P4 547, P5 809, P6 809 |
| M9 | stack: the tail never moved on | P1 2741, P2 2938, P3 2938, P5 2938, P6 2938 |
| M10 | vine: the left child's right subtree dropped | P1 619, P2 691, P3 691, P5 809, P6 691 |
| M11 | vine: the rotated child never lifted | P1 1747, P2 1880, P3 1880, P5 2938, P6 1880 |
| M12 | vine: the node dropped below its left child | P1 1747, P2 1880, P3 1880, P5 2938, P6 1880 |
| M13 | pairs: the left chain never joined to the node | P1 1747, P2 1880, P3 1880, P5 2938, P6 1880 |
| M14 | pairs: the head left at the node | P1 1747, P2 1880, P3 1880, P5 2938, P6 1880 |
| M15 | pairs: the tail left at the node | P1 619, P2 691, P3 691, P5 809, P6 691 |

P1, P2, P3 and P6 kill all fifteen, and P5 all but M4, which reverses
the order on the mirrored tree just as on the original, so the two
chains still match backwards. Mutants in different arms fail exactly the
same cases when they go wrong on the same trees: any tree with a left
child (M6, M7, M11 to M14), any with a right child (M1, M8), any with a
left child that has a right child (M10, M15), and any of two nodes or
more (M2, M9, which leave each node hanging off the head, so the chain
is the last node alone). P5 fails such a mutant more often than the
others do, because it fails when either the tree or its mirror has the
shape the mutant trips on. P4 kills only the mutants whose chain, given
back to the arm, comes out different: reversed again (M4), one value
shorter again (M5), or cut down to its root (M1, M8), since a chain is
nothing but right children.

The first M1 removed `relink(n.right, mut tail);`, which also matched
inside the arm's renamed `star_relink(...)` call and left the name
`star_` behind, so the program did not compile; it now names the whole
call. Seven mutants first stopped the differential with an index out of
bounds in P5, which compared the mirrored chain with the arm's own
without checking the arm's had `n` values; P5 now checks both lengths.

## Verification

Every arm prints the same output as `increasing_bst.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 0.5 to 0.6 s
each and the differential 10 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy lanes split. The values, stack, vine and pairs arms
print the same output under all of them, the interpreter, the JIT and
`karac build --legacy` with and without auto-par. The ★ arm prints it
under the legacy interpreter, but its JIT and both builds abort with
`free(): double free detected`; the ★ arm is the one that moves its
tail through a `mut ref TreeNode` (`*tail = n`). The legacy build of the
bench program, which uses the ★ arm, runs to the end but prints a wrong
checksum, a different one on each run. Every legacy lane refuses the
differential: `*v` on an element of `.iter()` is rejected, because
legacy's iterator gives the value itself. Legacy is frozen, so none of
this is filed.

## Benchmarks

The bench program uses the ★ arm on 200,000 search trees of 100 nodes,
LeetCode's largest, each made by putting in 100 random values from 0 to
1,000 (a value equal to one already in goes right), and each chain
walked into a checksum. The work is the trees' building as well as
their relinking. Kāra's nodes are a reference-counted `shared struct`,
Rust's LeetCode's `Rc<RefCell<TreeNode>>`, Go's pointers left to its
collector, and C's `malloc`'d nodes freed as the chain is walked. Every
implementation prints `200000 trees of 100 nodes: 20000000 in the
chains, checksum 728076515`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 1.19 to 1.32 s | 1.25 s |
| Rust (`rustc -O`) | 1.58 to 1.69 s | 1.64 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.60 to 1.83 s | 1.69 s |
| Go | 1.66 to 1.93 s | 1.79 s |
| Python | 19.2 s | |
| Kāra (`karac build --mir`) | 1.48 to 1.61 s | 1.53 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 896's does. Legacy's build prints a wrong
checksum (above), so it has no row.

v2 takes 0.90 times Rust's median time under overflow checks and 1.22
times C's. Under valgrind's cachegrind C runs 5.56 billion instructions
and mispredicts 96 million branches, Rust with overflow checks 10.08
billion and 112 million, and v2 7.71 billion and 103 million. Each
insertion's walk down the tree turns left or right on a random value,
so all three mispredict at about the same rate; the difference between
them is mostly instructions, of which Rust's `RefCell` borrow flags and
`Rc` counts are a part, though how large a part was not measured. The
comparison with C and Rust waits until after M4.
