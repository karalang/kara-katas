# 998. Maximum Binary Tree II

A **maximum tree** is a tree where every node has a value greater than
any other value in its subtree.

You are given the `root` of a maximum binary tree and an integer `val`.

Just as in the previous problem, the given tree was constructed from a
list `a` (`root = Construct(a)`) recursively with the following
`Construct(a)` routine:

- If `a` is empty, return `null`.
- Otherwise, let `a[i]` be the largest element of `a`. Create a `root`
  node with the value `a[i]`.
- The left child of `root` will be
  `Construct([a[0], a[1], ..., a[i - 1]])`.
- The right child of `root` will be
  `Construct([a[i + 1], a[i + 2], ..., a[a.length - 1]])`.
- Return `root`.

Note that we were not given `a` directly, only a root node
`root = Construct(a)`.

Suppose `b` is a copy of `a` with the value `val` appended to it. It is
guaranteed that `b` has unique values.

Return `Construct(b)`.

```
root = [4,1,3,null,null,2], val = 5  ->  [5,4,null,1,3,null,null,2]
root = [5,2,4,null,1], val = 3       ->  [5,2,4,null,1,null,3]
root = [5,2,3,null,1], val = 4       ->  [5,2,4,null,1,3]
```

**Constraints:** the number of nodes is in the range `[1, 100]`;
`1 <= Node.val <= 100`; all the values of the tree are unique;
`1 <= val <= 100`.

## Approaches

A value appended to `a` comes after every value already there, so in
`Construct(b)` it can only sit on the right spine, the chain of right
children from the root, whose values fall as it goes down. It takes
the place of the first node there smaller than itself, with that node
and all below it as its left subtree. Three arms find that place; two
read `a` back out of the tree, in order, and build `Construct(b)` anew.

| file | mechanism |
|---|---|
| `insert_into_max_tree.kara` ★ | recursion down the right spine: a value larger than the root becomes the new root with the whole tree on its left, and otherwise goes into the root's right subtree. O(h) for the spine's length h |
| `insert_into_max_tree_walk.kara` | a loop down the right spine, keeping the last node larger than the value, then a splice: the value takes that node's right child as its left subtree and becomes its right child. O(h) |
| `insert_into_max_tree_rebuild.kara` | `a` read back by an in-order walk, the value appended, and the tree built again by the definition, the largest value of each stretch at its root, over index ranges. O(n²) at worst |
| `insert_into_max_tree_stack.kara` | `a` read back by an in-order walk with an explicit stack, the value appended, and the tree built again in one pass with a stack of falling values: each value takes the smaller ones it pops as its left subtree and becomes the right child of the larger one left on top. O(n) |
| `insert_into_max_tree_spine.kara` | the right spine gathered into a list, and a binary search for the first node on it smaller than the value, which the value then replaces. O(h) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 18 lines, each tree in LeetCode's level
order. The first ten are LeetCode's three examples and seven more: one
node and a larger value, and a smaller one; a chain of left children
and a value above them all; a chain of left children and a value below
them all, which goes to the root's right; a value landing in the
middle of the right spine, and one landing under a spine node with a
left subtree of its own; and a value below every node of a chain of
right children. Then five trees of 99 values, as large as `b` leaves
room for: values rising from 1, inserting 100; rising from 2,
inserting 1; falling from 100, inserting 1; falling from 99, inserting
100; and falling from 100 without 50, inserting 50. Then totals over
random lists of different values from 1 to 100, each with another
value to insert: 300 of up to 5 values, 3,000 of up to 30 and 300 of
up to 99. `insert_into_max_tree.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: `Construct(b)` on the list `b` itself, with new lists
made for the values before the largest and those after it. The arms
get only the tree, built from `a`; the statement gets `a`. It checks
3,200 random lists of different values from 1 to 100, each with two
more values not in it: 3,000 of up to 7 values against the statement,
and 200 of up to 98 against the other properties.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 lists |
| P2 | read in order, the tree gives back `a` with `val` after it |
| P3 | every node is larger than its children, and the tree has one node more than before |
| P4 | the second value inserted into the result gives `Construct` of `a` with both values appended |
| P5 | every value `v` turned into `3v + 7`, which keeps their order, gives the same tree with its values turned |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 trees of 25426 nodes: heights 13081, checksum
772736546, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (14.1 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-five edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the test turned round | P1 3000, P3 3200, P4 3200, P6 3200 |
| M2 | ★: the old tree hung on the new root's right | P1 1507, P2 1616, P4 2666, P6 1616 |
| M3 | ★: down the left, not the right | P1 2313, P2 2503, P4 3033, P6 2503 |
| M4 | walk: the rest of the spine dropped | P1 820, P2 919, P3 919, P4 1707, P6 919 |
| M5 | walk: the walk goes on past smaller nodes | P1 1596, P3 1774, P4 2367, P6 1774 |
| M6 | walk: the old tree hung on the new root's right | P1 687, P2 697, P4 1077, P6 697 |
| M7 | rebuild: the tree read in preorder | P1 2317, P2 2513, P4 2916, P6 2513 |
| M8 | rebuild: the value put first | P1 3000, P2 3200, P4 3200, P6 3200 |
| M9 | rebuild: each left stretch loses its first value | P1 2718, P2 2916, P3 2916, P4 3116, P6 2916 |
| M10 | stack: never a right child | P1 2703, P2 2903, P3 2903, P4 3102, P6 2903 |
| M11 | stack: the top of the stack returned | P1 2313, P2 2503, P3 2503, P4 3033, P6 2503 |
| M12 | stack: the value never appended | P1 3000, P2 3200, P3 3200, P4 3200, P6 3200 |
| M13 | spine: the spine below dropped | P1 1507, P2 1616, P3 1616, P4 2666, P6 1616 |
| M14 | spine: a new largest value dropped | P1 687, P2 697, P3 697, P4 1077, P6 697 |
| M15 | spine: the value spliced in on the left | P1 2313, P2 2503, P3 1680, P4 3033, P6 2503 |

P1, P4 and P6 kill all fifteen, P2 thirteen, P3 ten and P5 none.
Every arm, and every edit, only compares values with each other,
never with a fixed number, and `3v + 7` keeps every comparison, so P5
stays a check on the arms, not on these edits. The checks draw no
random number that depends on an answer, so every mutant sees the same
lists, and their counts can be compared: of the 3,000 small lists,
`val` is the largest in 687, where it becomes the new root. M6 and M14
go wrong only there; M3, M11 and M15, which only get the new root
right, go wrong on the other 2,313. `val` lands at the bottom of the
spine, with nothing below it, in 1,493, and M2 and M13, which mishandle
what lies below it, go wrong on the other 1,507. P2 misses M1 and M5,
which put the value somewhere on the right spine with what was below
it on its left, as the right answer does, only in the wrong place: the
order read back is right, but a smaller node then sits above a larger
one, which P3 sees. P3 misses the five that build a proper maximum
tree with one node more from the values in a wrong order: M2 and M6,
which hang the old tree on the new root's right; M3, which goes down
the left; M7, which reads the tree in preorder; and M8, which puts the
value first. P2 sees all five.

Ten other edits were tried and set aside. Four failed exactly the same
checks as a kept one: rebuild putting the smallest value of each
stretch at its root, stack popping the larger values and spine's
binary search turned round, as M1; and stack not keeping the values it
pops on the left, which loses them, as M9. Five were sound but beyond
three an arm: ★ dropping the old tree under a new root; walk splicing
the value in on the left, and dropping a new largest value; rebuild
never making the last value of a stretch its root; and spine's search
never reaching the end of the spine. One survived and is equivalent: ★
making an equal value the new root, since the values of `b` are all
different and an equal one never comes. None crashed.

## Verification

Every arm prints the same output as `insert_into_max_tree.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error;
the differential prints its line under all three. `karac check` passes
all five arms, the differential and the bench program. `karac run` and
a `karac build --mir` binary print the same output for every arm and
the differential. The release build is at kara `395f71ae05`, the
runtime archives rebuilt at `d867340a02`, whose runtime sources are
the same. Under `karac __mir-run` the arms take 2.4 s (★) to 3.4 s
(stack, which reads the whole tree out and builds it again for every
list), and the differential 14.1 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. The program builds 20
maximum trees of 99 values once, each from the values 1 to 100 but a
random one, which is its `val`: ten from those values in a random
order, and ten from them in falling order, which makes a chain of 99
right children, LeetCode's worst case. In each of 100,000 rounds it
inserts every tree's `val` into it, each round starting from a
different tree, then takes the value out again, walking the spine the
same way, so that every call starts from the same tree, and folds how
deep the value sat into a checksum. Every implementation prints
`100000 rounds over 20 trees of 99 values: depth total 36700000,
checksum 873065628`. Each call allocates one node and frees one, and
walks 18 nodes down on average each way; C frees with `free`, Rust's
tree is LeetCode's `Option<Rc<RefCell<TreeNode>>>`, reference counted
as Kāra's `shared struct` is, and Go's is collected.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `395f71ae05`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.233 to 0.323 s | 0.257 s |
| Rust (`rustc -O`) | 0.422 to 0.531 s | 0.462 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.448 to 0.578 s | 0.474 s |
| Go | 0.401 to 0.465 s | 0.418 s |
| Python | 5.1 s | |
| Kāra (`karac build --mir`) | 0.448 to 0.524 s | 0.495 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 10 times
Kāra's.

v2 took 1.04 times Rust's median time under overflow checks and 1.93
times C's. Under valgrind's cachegrind v2 ran 2,431 million
instructions and 484 million branches with 4.9 million mispredicted,
Rust with overflow checks 3,009 million, 569 million and 4.5 million,
and C 1,246 million, 158 million and 4.2 million. All three spend the
same 255 million instructions in glibc's allocator, one `malloc` and
one `free` a call. The insert itself takes v2 1,145 million
instructions, Rust 1,397 million and C 701 million, and the rest of
`main`, mostly taking the value out again, v2 1,024 million, Rust
1,282 million and C 280 million; the counting and reference checks a
shared node carries fit the gap to C (inferred). v2 runs fewer
instructions than Rust and is still a little slower; that was not
traced.
