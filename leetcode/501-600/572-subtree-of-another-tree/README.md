# 572. Subtree of Another Tree

Given the roots of two binary trees `root` and `subRoot`, return `true`
if there is a subtree of `root` with the same structure and node values
of `subRoot` and `false` otherwise. A subtree of a binary tree `tree` is
a tree that consists of a node in `tree` and all of this node's
descendants. The tree `tree` could also be considered as a subtree of
itself.

```
root = [3,4,5,1,2], subRoot = [4,1,2]                            ->  true
root = [3,4,5,1,2,null,null,null,null,0], subRoot = [4,1,2]      ->  false
```

**Constraints:** the number of nodes in `root` is in `[1, 2000]`; the
number of nodes in `subRoot` is in `[1, 1000]`; `-10^4 <= root.val <=
10^4`; `-10^4 <= subRoot.val <= 10^4`.

## Approaches

Every arm is `fn is_subtree(root: Option[TreeNode], sub_root:
Option[TreeNode]) -> bool` over a `shared struct TreeNode` with `mut`
fields.

| file | mechanism |
|---|---|
| `is_subtree.kara` ★ | recursion: sub_root is a subtree when the two trees are the same, or it is a subtree of root's left or right subtree; two trees are the same when both are empty, or their roots' values match and so do their left and their right subtrees; O(m * n) |
| `is_subtree_text.kara` | both trees written in preorder, each node as `^` and its value and each missing child as `#`; sub_root is a subtree when root's text contains its text, since a run starting at a `^` that reads as one whole tree is one of root's subtrees |
| `is_subtree_hash.kara` | every subtree given a number made from its root's value and its children's numbers, bottom up; where a subtree of root has sub_root's number, the two are compared node by node, since different trees can share a number |
| `is_subtree_stack.kara` | no recursion: one stack walks root, and at each node with sub_root's value a second stack of node pairs compares the two trees |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 18 lines: ten pairs at the edges (the two
examples, the whole tree, a leaf, a node that is there but has children,
the same values in another shape, sub_root larger than root, 12 against
2 and -2 against 2, whose digits run together when written out, and the
problem's extreme values), a count and checksum over 300 random pairs,
and the problem's largest: a random root of 2,000 nodes against a copy
of its largest subtree of at most 1,000, then a chain of 2,000 ones down
the left against a chain of 1,000 that ends in a 2, and against one of
1,000 ones. Each random root has 1 to 60 nodes valued 0 to 2, and
sub_root is in turn a copy of one of its subtrees, that copy with one
value changed, that copy with a leaf added, or a random tree of 1 to
5 nodes. `is_subtree.py` mirrors the ★ arm and its output is
byte-identical.

The test harness keeps one of a tree's nodes while walking them with
`for n in nodes.iter()`, and writes `best = *n` and `Some(*n)`. `karac
check` refused `*n` on a reference to a `shared` handle when the kata
was written (kara B-2026-10-14-22), so the harness first wrote `n`; that
row is fixed (kara `5391da32d4`) and the harness is back to `*n`. The
fields are `mut` because the harness changes a value in a copied tree.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: each node of root with all its descendants
written out in full, `(value left right)` with `()` for a missing child,
and sub_root written the same way; it is a subtree when its text is one
of root's. Each arm is held to the properties below on 1,000 random
pairs: root of 1 to 20 nodes valued 0 or 1, and sub_root in turn a copy
of one of root's subtrees, that copy with one value changed, or a random
tree of 1 to 4 nodes. Every other pair is valued 2 and 12 in place of
0 and 1, so that one value's digits end another's.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | when it is true, sub_root has no more nodes and no more depth than root |
| P3 | mirroring both trees changes nothing |
| P4 | moving every value in both trees by the same amount changes nothing |
| P5 | a copy of sub_root hung beside root under a new root is found |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac
__mir-llvm-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the right subtrees never compared | P1 232, P2 4, P3 220 |
| M2 | ★: the right subtree never searched | P1 317, P3 258, P5 756 |
| M3 | text: missing children not written | P1 217, P3 65 |
| M4 | text: no mark before a value | P1 29, P4 28 |
| M5 | hash: a missing child numbered differently while searching | P1 561, P5 1000 |
| M6 | hash: the left subtree's subtrees never searched | P1 341, P3 258 |
| M7 | stack: the left child never pushed, the right twice | P1 341, P3 258 |
| M8 | stack: a match accepted at the first pair of leaves | P1 188, P2 3, P3 267 |
| E1 | ★: the values compared the other way round | 0 |
| E2 | text: the value written with `to_string` | 0 |
| E3 | hash: left and right children weighted alike | 0 |
| E4 | stack: the values not compared before `matches_at` | 0 |

P3 sees every mutant that treats the left and right sides differently,
since mirroring swaps them: M1, M2, M6, M7 and M8, and M3, whose text
without `#` cannot tell a left child from a right one. M6 and M7 fail
identically: each misses every match inside a left subtree. P5 hangs the
copy on the right, which M2 never searches. M5 gives sub_root's missing
children one number and root's another, so no number ever matches and it
answers false whenever the answer is true, P5 on all 1,000. M4 fails
only on the pairs valued 2 and 12, where a leaf 2 is found inside
`12##`; without those pairs it survived every property, and they were
added for it. P4 sees it there too, since moving the values changes
their digits. E3 makes mirrored trees share a number, but a match on the
number is always confirmed node by node, so only the speed changes;
E4 is safe because `matches_at` compares the values first itself.

## Verification

The four arms print the same output as `is_subtree.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and run
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes on every arm, the differential and the bench program.

The frozen legacy backends refuse every arm under `karac run --interp`,
`karac run` and `karac build`, at type checking: legacy gives the
elements of `iter()` as values, so the harness's `*n` does not check
("unary '*' requires 'ref T' ... found 'TreeNode'"). Before the harness
went back to `*n`, `karac run --interp` printed the right output for the
text and hash arms, and `karac run` and `karac build` stopped every arm
at module verification on the harness's `show` call. `karac run
--interp` did not finish the differential within a 60-second limit;
`karac build` builds the differential, which prints the same line, and
the bench program. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 random pairs once: root a
random tree of 2,000 nodes (the problem's most) valued 0 or 1, and
sub_root a copy of one of its subtrees of at least 20 nodes, every other
copy with one value changed. Then 1,000 times over every pair is
answered. Every implementation prints `20 pairs, 1000 rounds:
10000 found, checksum 595957116`, the Kāra program under `karac
__mir-run` included (242 s).

Rust's nodes are `Rc<RefCell<TreeNode>>`, LeetCode's Rust tree, counted
as the Kāra `shared struct` is; C's are `malloc`'d and Go's and Python's
are plain references, none of them counted. Spot timings on a shared
4-core container, three runs each (two for Python; `bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.58 s |
| Rust (`rustc -O`) | 0.73 to 0.77 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.75 to 0.83 s |
| Go | 0.64 to 0.65 s |
| Python | 6.97 to 7.07 s |
| Kāra (`karac build`, legacy) | 0.99 to 1.05 s |
| Kāra (`karac build --mir`) | 1.21 to 1.30 s |

The legacy `karac build` builds this program, so `bench.sh` is the
`scripts/new-bench.sh` output as it stands; the `--mir` row is the
v2 compiled backend, timed by hand. The `--mir` row is timed at kara
`680733538b`. Under `karac __mir-llvm-run` the program prints the same
line in 3.0 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

The `--mir` row is about 1.7 times Rust's and 1.2 times the legacy
backend's on the same program. The cause is not measured.

## Compiler findings

One filed: **B-2026-10-14-22**, now fixed (kara `5391da32d4`). `karac
check` refused `*n` where `n` is a `ref` to a `shared struct` handle, as
in `for n in nodes.iter() { best = *n; }`, with `borrow_projection_copy`
("cannot move a non-`Copy` value out of a borrow with `*`"), though the
spec copies a handle on every use and both MIR backends ran it. The
harness wrote `n` until the fix and writes `*n` again: the four arms
pass `karac check` at kara `a7d3ce0b8e`, where the compiler before the
fix still refuses them, and print the same output under `karac
__mir-run`, `karac __mir-llvm-run` and `karac __mir-llvm-asan`. The
legacy failures above are not filed because legacy is frozen.
