# 501. Find Mode in Binary Search Tree

Given the `root` of a binary search tree (BST) with duplicates, return
all the mode(s) (i.e., the most frequently occurred element) in it. If
the tree has more than one mode, return them in any order.

Assume a BST is defined as follows: the left subtree of a node contains
only nodes with keys less than or equal to the node's key; the right
subtree of a node contains only nodes with keys greater than or equal
to the node's key; both the left and right subtrees must also be binary
search trees.

```
root = [1,null,2,2]  ->  [2]
root = [0]           ->  [0]
```

**Constraints:** the number of nodes in the tree is in the range
`[1, 10^4]`; `-10^5 <= Node.val <= 10^5`.

**Follow up:** could you do that without using any extra space? (The
implicit stack space incurred due to recursion does not count.)

## Approaches

Every arm is `fn find_mode(root: Option[TreeNode]) -> Vec[i64]` over a
`shared struct TreeNode`, and returns the modes in ascending order.

| file | mechanism |
|---|---|
| `find_mode.kara` ★ | recursive in-order walk, which meets the values in ascending order, so equal values come one after another; a `Walk` struct carries the current run, the best run and the modes, and a run longer than the best replaces the modes, one as long joins them |
| `find_mode_map.kara` | ignore the order: count every value in a `Map[i64, i64]` (`entry(...).or_insert(0)`), take the largest count with `*counts.values().max().unwrap()`, keep the values that have it (`iter().filter(...).map(...).collect()`) and sort them |
| `find_mode_stack.kara` | the ★ arm's running count, with the in-order walk on an explicit `Vec[TreeNode]` stack |
| `find_mode_morris.kara` | Morris traversal, the follow-up's O(1) extra space: before going left, point the in-order predecessor's right link back at the node, and on meeting that thread again clear it, count the node and go right. Values repeat, so the thread is told from a real right child by identity, `r.ref_eq(n)` |
| `differential.kara` | the four arms on 1,500 random trees, five properties |

Every arm prints the same 9 lines: the two LeetCode examples, all
equal, all different, two modes, the extremes of the range, a mode at
the end and at the start of the order, and for 300 random trees of 1 to
40 values (from 1 to 5 values, 50 values, or the whole range, in turn)
the count of values and modes and a checksum of the modes.
`find_mode.py` mirrors the ★ arm and its output is byte-identical.

The harness builds each tree by inserting its values in the order
given: a smaller value goes left, a larger one right, and an equal one
either way by a coin flip from the random generator, so equal values
land on both sides as the problem allows. LeetCode's first example is
built from `[1, 2, 2]`, which gives another shape of the same values.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random trees of 1 to 30 values, from 1 to 4 values, 20 values, or
the whole range -100,000 to 100,000, in turn. Every arm gets the same
trees: their coin flips start from the same seed.

| | property |
|---|---|
| P1 | the modes are the reference's, which counts each distinct value in a list and keeps those with the largest count, sorted |
| P2 | the modes rise and are values of the tree |
| P3 | one more copy of the smallest mode makes it the only mode |
| P4 | the tree is as it was: the same values in the same shape, read in preorder |
| P5 | the same values inserted in the reverse order, another shape, have the same modes |

P4 is there for the Morris arm, which rewrites links as it goes and
must leave the tree as it found it.

As written, the map arm is refused by the v2 backends (see Compiler
findings), and so is the differential, which holds a copy of it. It
is run on a copy that writes the map arm's largest count as
`counts.iter().map(|(_, c)| *c).max().unwrap()`, the only change. That
copy prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`. The files here keep the spec's spelling, and should
pass as they stand once the row is fixed. When this kata was written
the Morris arm's `r.ref_eq(n)` ran on no v2 backend either, and the
copy also gave each node an `id` field to compare in its place; since
kara `32540012cd` the Morris arm runs as written.

## Mutation testing

Ten edits to the copy of `differential.kara`, two to each arm and two
equivalent ones, each run under `karac __mir-run`. All eight
non-equivalent ones are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every value after the first continues the run (`>=` for `==`) | P1 1209, P3 1209 |
| M2 | ★: a run as long as the best replaces the modes instead of joining them | P1 814 |
| M3 | map: the modes are not sorted | P1 689, P2 689, P5 745 |
| M4 | map: the right subtrees are not counted | P1 1146, P3 789, P5 1037 |
| M5 | stack: a new run starts at 0 | P1 885, P2 885, P3 1500 |
| M6 | stack: a longer run keeps the old modes (no `clear`) | P1 885, P2 885, P3 1500 |
| M7 | Morris: the thread is told by value, not identity (`r.val == n.val`) | P1 430, P3 409, P4 698, P5 390 |
| M8 | Morris: `prev` is never updated | P1 646, P2 339, P3 1156 |
| E1 | Morris: `cur = Some(l)` for `cur = n.left` | 0 |
| E2 | ★: no `walk.run > 0` test before comparing with `prev` | 0 |

E1 is equivalent because `l` is `n.left`, read one line before. E2 is
equivalent because the test only matters on the first node, where `run`
and `prev` are both 0: without it a first value of 0 matches `prev` and
`run` goes from 0 to 1, which is what the other branch sets.

M7 is the reason the Morris arm needs identity. With equal values on
both sides of a node, the right spine of its left subtree can hold a
real node of the same value before the thread; M7 takes that node for
the thread, cuts it off and counts the walk wrong, and P4 sees the
damaged tree in 698 cases. M2 changes only the answer when two runs tie
for the best, so only P1 sees it. M5 and M6 fail the same cases with
different answers. M5 lists every node, since each node starts its run
at 0, which ties the starting best of 0. M6 never clears, so a value is
listed again each time its run grows past the best. Both are right
exactly when no value occurs twice, and P3, which adds a second copy of
a value, fails all 1,500 under both. M3 shows the map's order: P2 and P5 see it because the order of
a `Map` walk is random, not sorted.

## Verification

The ★ and stack arms print the same output as `find_mode.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak, and so does the
Morris arm as written, at kara `32540012cd`. So does the map arm in
the copy described under Differential, and so does that copy of the
differential, run again at `32540012cd` with the Morris arm as written.
`karac check` passes on the ★, stack and Morris arms and the bench
program, and refuses the map arm and the differential (see Compiler
findings).

On the frozen legacy backends, `karac run --interp` prints the same
output for the ★ and stack arms, but LLJIT and legacy `karac build`
fail on both at codegen: "Module verification failed: Call parameter
type does not match function signature!", at the harness's calls to
`show`, whose first parameter is a `Str` given a string literal. The
map arm and the differential are refused on legacy as on v2. The
Morris arm passes the type checker since kara `32540012cd` and fails
later on legacy: `karac run --interp` at "method 'ref_eq' not found on
type 'TreeNode'", and legacy `karac build` at codegen, "no handler for
method 'ref_eq'". Legacy `karac build` builds the bench program, which has no such
call. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 random search trees of
10,000 values (the problem's most) once, drawn from 1 to 10 values,
1,000 values, or the whole range -100,000 to 100,000 in turn, an equal
value going left or right by a coin flip. Then it finds the modes of
each tree 30 times, folding them into a checksum. Every implementation
prints `100 trees of 10000 values, 30 times each: 9570 modes, checksum
204168509`, the Kāra program under `karac __mir-run` included
(in 109 s).

Every mirror recurses in order and collects the modes into a fresh
growable array for each traversal, as the ★ arm pushes onto
`Vec.new()`. Rust's tree is `Rc<RefCell<TreeNode>>`, the closest match
to a `shared struct`; C mallocs each node and Go leaves them to the
collector. Spot timings on a shared 4-core container, three runs each
(two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.82 to 1.12 s |
| Rust (`rustc -O`) | 2.09 to 2.15 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.06 to 2.21 s |
| Go | 0.84 to 1.07 s |
| Python | 10.2 to 10.6 s |
| Kāra (legacy `karac build`) | 1.83 to 2.11 s |
| Kāra (`karac build --mir`) | 1.93 to 1.99 s |

Legacy `karac build` builds this program, so `bench.sh` is the
`scripts/new-bench.sh` output unchanged and times the legacy build; the
`--mir` row is timed by hand at kara `22c7db1833`. Under `karac
__mir-llvm-run` the program prints the same line in 3.3 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

## Compiler findings

kara B-2026-10-13-17 (missing-feature, fixed in kara `32540012cd`):
`ref_eq` had no v2 form. The spec gives identity on a `shared` handle
as a method, `a.ref_eq(b)` (design.md § Equality), and `karac check`
refused it: "no method 'ref_eq' on type 'TreeNode'". The older free
function `ref_eq(a, b)` passed `karac check`, but `karac __mir-run`
stopped at "call of unknown function ref_eq" and `karac
__mir-llvm-run` at "native `ref_eq` is not lowered yet". So the Morris
arm, which must tell its thread from a real right child holding the
same value, ran on no v2 backend. Since the fix it runs as written on
all three.

kara B-2026-10-13-1 (open; this kata adds a second data point to it):
`Map.values()` returns an eager `Vec` where the spec gives an
`Iterator[Item = ref V]`. The map arm's `*counts.values().max().unwrap()`
is the spec's form, and `karac check` refuses it ("unary '*' requires
'ref T' ... found 'i64'"). Without the `*` it passes `karac check` and
then fails on both v2 backends ("call of unknown function
Vec[i64].max"), and the implementation's own advice,
`counts.values().iter().max()`, passes `karac check` and fails the MIR
borrow check ("drop of _8 while it is borrowed").
