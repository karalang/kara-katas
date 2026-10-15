# 653. Two Sum IV - Input is a BST

Given the root of a binary search tree and an integer `k`, return `true`
if two different nodes of the tree have values that add up to `k`, and
`false` otherwise.

```
root = [5,3,6,2,4,null,7], k = 9   ->  true     2 + 7, 3 + 6, 4 + 5
root = [5,3,6,2,4,null,7], k = 28  ->  false
```

**Constraints:** 1 to 10,000 nodes; values from -10,000 to 10,000; the
tree is a valid binary search tree, so its values are distinct; `k` from
-100,000 to 100,000.

## Approaches

Every arm is `fn find_target(root: Option[TreeNode], k: i64) -> bool`
over a `shared struct TreeNode`.

| file | mechanism |
|---|---|
| `two_sum_bst.kara` ★ | an in-order walk lists the values in rising order, then two indices move in from the ends; O(nodes) time and space |
| `two_sum_bst_seen.kara` | any walk, each value checked against a `Set` of those met before for `k - value`; ignores the order; O(nodes) |
| `two_sum_bst_search.kara` | for each node, a search down the tree from the root for `k - value`, skipping the node itself; O(nodes * height) time, O(height) space |
| `two_sum_bst_stacks.kara` | the two ends without the list: one stack walks in rising order and one in falling order, each yielding its next value on demand; O(nodes) time, O(height) space |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 12 lines: the two LeetCode examples; eight
more (one node, which cannot pair with itself; a sum of two leaves; a
target that would need a value twice; 0 with the smallest and largest
values; and a chain of ten rising values), each with its answer; the
count found and a checksum of the answers for 200 random trees of 1 to
60 values from -100 to 100, each asked 20 targets; and a tree of the
problem's largest size, 10,000 values, asked 40 targets from -30,000 to
30,000. `two_sum_bst.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which ignores the tree: every pair of different values in the list the
tree was built from, checked for the sum. Each of 2,000 random trees
holds 1 to 40 distinct values from `-r` to `r`, `r` being 5, 50 or
1,000, inserted in random order, and is asked a target from `-2r - 2` to
`2r + 2`.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the values and the target negated, the answer is the same |
| P3 | the sum of two different values of the tree is found |
| P4 | a target above the two largest values' sum, or below the two smallest values' sum, is not found |
| P5 | the same values inserted in rising order, a chain down the right, give the same answer |

It prints `2000 trees (31708 nodes), 4 arms, 40000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the two ends allowed to meet on one value | P1 109, P4 709 |
| M2 | ★: a small sum moving the high end down | P1 422, P2 314, P3 1209 |
| M3 | seen: the right subtree never walked | P1 553, P2 130, P3 1502, P5 62 |
| M4 | seen: the partner taken as `value - k` | P1 405, P2 408, P3 995, P4 640, P5 197 |
| M5 | search: a node allowed to pair with itself | P1 111, P4 709 |
| M6 | search: the search turning the wrong way | P1 431, P3 1152, P5 219 |
| M7 | stacks: a small sum moving the falling walk | P1 422, P2 314, P3 1209 |
| M8 | stacks: the falling walk going down the left child's left side | P1 246, P2 310, P3 694, P5 246 |
| E1 | ★: a single value walked by the two ends | 0 |
| E2 | seen: the right subtree walked first | 0 |
| E3 | search: an equal value sent left | 0 |
| E4 | stacks: the empty tree told by the falling stack | 0 |

P1 kills all eight. M1 and M5 let a value pair with itself, so they
answer `true` wrongly only for an even target twice a value; P4 sees
them, through its target just past the two largest or below the two
smallest, which a value doubled reaches, and P2 and P3 cannot. M2 and
M7, a small sum moving the wrong end, and M8, a falling walk that skips
values, miss pairs, as do M3 and M6; P3 sees all five. P5 sees the
mutants whose fault depends on the tree's shape, M3, M4, M6 and M8: a
chain has no left subtrees, so M3's lost right subtree is everything but
the root. P2 sees the asymmetric ones. The four survivors cannot change
an answer: with one value the ends start equal and the loop never runs;
the order of the walk does not matter to a set; values are distinct, so
sending an equal value left never happens after the equality test; and
an empty tree leaves both stacks empty.

## Verification

Every arm prints the same output as `two_sum_bst.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` for the debug build and `abbdbaf131` for the release build
that runs `check` and `__mir-run`, with runtime archives newer than the
last `runtime/src` change.

The frozen legacy backends refuse every arm and the differential at type
checking: the harness reads `*v` from `values.iter()` over a `Vec[i64]`,
which legacy types by value. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm. It makes a search tree of
200,000 distinct values from 0 to 999,999, inserted in random order,
once; then asks 300 targets from 0 to 2,999,999, counting those found
and putting each answer into a checksum. A target the tree cannot make
walks the whole list from both ends. Every implementation prints
`200000 values, 300 targets: 193 found, checksum 304305694`, the Kāra
program under `karac __mir-run` included (in 163 s).

Each implementation walks the tree recursively into a growable array and
moves two indices in from its ends. Kāra's nodes are a `shared struct`,
Rust's `Rc<RefCell<TreeNode>>`, and C's and Go's plain pointers; the set
of values already inserted is Kāra's `Set`, Rust's `HashSet`, Go's
`map`, Python's `set`, and in C a byte per value. Spot timings on a
shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine), each including making the tree:

| | time |
|---|---|
| C (`clang -O3`) | 1.60 to 1.74 s |
| Rust (`rustc -O`) | 3.05 to 3.27 s |
| Rust (`rustc -O -C overflow-checks=on`) | 3.06 to 3.13 s |
| Go | 4.10 to 4.61 s |
| Python | 22.3 to 22.4 s |
| Kāra (`karac build --mir`) | 2.96 to 2.97 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The legacy `karac build` builds the bench
program unchanged and takes 2.87 to 3.03 s over six runs. Under `karac
__mir-llvm-run` the program prints the same line in 4.4 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

So the v2 build is level with legacy and with Rust. The walk is the
cost: 60 million visits to nodes scattered over the heap, and C, with
plain pointers and nothing to count, takes a little over half the time.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The legacy refusals
above are not filed because legacy is frozen.
