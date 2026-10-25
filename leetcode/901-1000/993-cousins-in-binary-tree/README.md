# 993. Cousins in Binary Tree

Given the `root` of a binary tree with unique values and the values of
two different nodes of the tree `x` and `y`, return `true` *if the
nodes corresponding to the values* `x` *and* `y` *in the tree are
**cousins**, or* `false` *otherwise*.

Two nodes of a binary tree are **cousins** if they have the same depth
with different parents.

Note that in a binary tree, the root node is at the depth `0`, and
children of each depth `k` node are at the depth `k + 1`.

```
root = [1,2,3,4], x = 4, y = 3                ->  false
root = [1,2,3,null,4,null,5], x = 5, y = 4    ->  true
root = [1,2,3,null,4], x = 2, y = 3           ->  false
```

**Constraints:** the number of nodes is in the range `[2, 100]`;
`1 <= Node.val <= 100`; each node has a unique value; `x != y`; `x`
and `y` exist in the tree.

## Approaches

Two questions settle it, how deep each node is and whose child it is.
Three arms find both for each of `x` and `y` and compare them; two
read the tree a level at a time and stop at the first level that holds
either value.

| file | mechanism |
|---|---|
| `is_cousins.kara` ★ | breadth-first, a level at a time, each node kept with its parent's value: the first level holding `x` or `y` decides, cousins when it holds both and their parents differ, not when it holds only one. O(n) |
| `is_cousins_dfs.kara` | one depth-first walk records the depth and the parent of `x` and of `y` in a list of four; cousins when the depths match and the parents do not. O(n) |
| `is_cousins_search.kara` | separate searches: `depth_of` returns a value's depth, or -1 when it is not below the node, and `parent_of` its parent's value, -1 for the root and -2 when not found; four walks in all. O(n) |
| `is_cousins_maps.kara` | an explicit stack walks the whole tree, filling one `Map` from value to depth and one from value to parent, and then reads `x` and `y` in both. O(n) |
| `is_cousins_siblings.kara` | levels without parents: the first level holding either value decides, false when it holds only one, and otherwise true unless, while that level was built, one node had `x` and `y` as its two children. O(n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 17 lines. The first ten are LeetCode's three
examples and seven more: two cousins in the complete tree of seven
nodes, two siblings there, and the root against its child; two nodes at
depth 3 with different parents, asked both ways round; two nodes at
different depths; and the smallest tree, two nodes. Then every pair
in the complete tree of 100 nodes, LeetCode's largest, and in a path of
100 that turns left and right in turn, where no two nodes share a
depth. Then totals over random trees, 20 random pairs in each: 300 of
up to 10 nodes and 3,000 of up to 100; and every pair in three random
trees of 100 nodes. `is_cousins.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every node is listed with the place of its parent, a
node's depth is the number of steps up the parents to the root, and
two nodes are cousins when their depths match and their parents do
not. It checks 3,200 random trees, each with a random pair of
different values: 3,000 of up to 10 nodes against the statement, and
200 of up to 100 against the other properties.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 trees |
| P2 | the question asked the other way round, `y` before `x`, gives the same answer |
| P3 | the mirror image of the tree gives the same answer |
| P4 | a new root above the tree, with the tree as its left child, gives the same answer |
| P5 | `x` is not a cousin of its parent, nor of its sibling |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 trees of 28099 nodes: 179 cousin pairs, checksum
228971449, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (3.3 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Thirty-two edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: cousins when the parents match | P1 453, P5 1517, P6 492 |
| M2 | ★: the right child given the root as its parent | P1 110, P3 81, P6 139 |
| M3 | ★: `x` found by the value of `y` | P1 147, P6 179 |
| M4 | dfs: the right child at its parent's depth | P1 1050, P3 1949, P5 1232, P6 1121 |
| M5 | dfs: the parent test left out | P1 306, P5 1517, P6 313 |
| M6 | dfs: the depth test left out | P1 2547, P5 2548, P6 2708 |
| M7 | search: the left subtree never searched for a depth | P1 673, P3 1011, P4 2050, P5 931, P6 782 |
| M8 | search: `parent_of` answers from the first subtree | P1 296, P3 170, P5 1110, P6 329 |
| M9 | search: `parent_of` searches the left child alone | P1 314, P3 177, P5 1069, P6 349 |
| M10 | maps: the right child one level deeper still | P1 235, P3 251, P6 272 |
| M11 | maps: the left child at its parent's depth | P1 1035, P3 1949, P5 1316, P6 1092 |
| M12 | maps: the right child one level up | P1 362, P6 406 |
| M13 | siblings: any two children of a node with `x` | P1 73, P2 81, P6 97 |
| M14 | siblings: a lone right child dropped | P1 66, P3 93, P6 79 |
| M15 | siblings: only one order of the pair checked | P1 145, P2 313, P3 313, P5 728, P6 146 |

P1 and P6 kill all fifteen, P3 and P5 nine each, P2 two and P4 one. Of
the 3,000 small pairs 147 are cousins and 306 siblings, and three
mutants show those counts plainly: M3 answers false every time and
fails the 147, M5 calls siblings cousins and fails the 306, and M1 has
both wrong, 453. Every arm but siblings treats `x`
and `y` alike, so P2 sees only M13 and M15, which look for the pair in
one order. A new root above the tree adds one to every depth and gives
the old root a parent, which no arm minds; only M7 does, since with the
whole tree hung on the left it finds no depth at all and calls every
pair whose parents differ cousins. P5 sees the mutants that let a
sibling or a parent through: those that drop or upset the parent test
(M1, M5) or the depth test (M6), those that misjudge where a child
sits (M4, M7 to M9, M11), and M15, which misses siblings that come in
the other order.

Seventeen other edits were tried and set aside. Thirteen failed
exactly the same checks as a kept one. Five more answer false every
time, as M3: dfs recording `y` into `x`'s places; search's `parent_of`
reporting the root as every child's parent; maps storing each parent
as the depth, the depth as the parent, and comparing `x`'s parent with
itself. Five more drop the parent test, as M5: dfs giving the right
child its grandparent as parent; maps storing each node as its own
parent, giving the left child its grandparent, and leaving the parent
test out; siblings never marking two siblings. Search comparing the
parents equal, and siblings answering as siblings, fail M1's checks,
and search counting the right subtree one level shallower fails M4's.
Three were sound but beyond three an arm: ★ deciding once either value
is found, which fails the checks M6 does; search comparing the depths
with at most, and passing over a left child at depth 0. One survived
and is equivalent: ★ without its early `return false` when only one
value is found. The next level starts its parents afresh, so the value
found is forgotten, the other is then found alone further down, and the
loop runs out with the same false. None crashed.

## Verification

Every arm prints the same output as `is_cousins.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `395f71ae05`, the runtime
archives rebuilt at `d867340a02`, whose runtime sources are the same.
Under `karac __mir-run` the arms take 11.3 s (dfs) to 27.0 s (maps,
which fills two maps for every pair), and the differential 3.3 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. The program grows 20
random trees of LeetCode's largest size, 100 nodes holding 1 to 100,
once. In each of 500 rounds it asks every tree about 100 pairs, each
value from 1 to 100 against the value a fixed step on, the step
changing with the round and the tree, and folds every answer into a
checksum. Every implementation prints `500 rounds over 20 trees of 100
nodes: 187663 cousin pairs, checksum 641208188`. Each call builds a
fresh, growing list for every level it reaches, so the work is mostly
allocation. The Rust tree is LeetCode's `Option<Rc<RefCell<TreeNode>>>`,
reference counted as Kāra's `shared struct` is; C grows its lists with
`realloc`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `395f71ae05`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.446 to 0.615 s | 0.526 s |
| Rust (`rustc -O`) | 0.649 to 0.798 s | 0.714 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.675 to 0.805 s | 0.726 s |
| Go | 1.858 to 2.204 s | 2.048 s |
| Python | 6.7 s | |
| Kāra (`karac build --mir`) | 0.376 to 0.455 s | 0.416 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 16 times
Kāra's.

v2 was the fastest: 0.57 times Rust's median time under overflow
checks and 0.79 times C's. Under valgrind's cachegrind v2 ran 4,675
million instructions and 753 million branches with 45.4 million
mispredicted, Rust with overflow checks 7,531 million, 1,312 million
and 84.7 million, and C 5,681 million, 1,041 million and 82.9 million.
C spends 71% of its instructions in glibc's allocator, most of them in
`realloc` and in `_int_malloc`, the allocator's slow path, with 38
million of its misses. Kāra's runtime grows a small buffer by
allocating, copying and freeing (`small_realloc` in
`runtime/src/alloc.rs`) instead of calling `realloc`, and its 1,294
million instructions in glibc go to `malloc`, `free` and
`malloc_usable_size`, with almost no misses; no `_int_malloc` shows,
which fits glibc serving them from its per-thread cache (inferred).
Go's time fits the same churn landing on its garbage collector
(inferred, not profiled).
