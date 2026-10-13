# 515. Find Largest Value in Each Tree Row

Given the `root` of a binary tree, return an array of the largest value
in each row of the tree (0-indexed).

```
root = [1,3,2,5,3,null,9]  ->  [1,3,9]
root = [1,2,3]             ->  [1,3]
```

**Constraints:** the number of nodes in the tree is in the range
`[0, 10^4]`; `-2^31 <= Node.val <= 2^31 - 1`.

## Approaches

Every arm is `fn largest_values(root: Option[TreeNode]) -> Vec[i64]`
over a `shared struct TreeNode`; the tree may be empty, so the root is
an `Option`.

| file | mechanism |
|---|---|
| `largest_values.kara` ★ | breadth-first with a `VecDeque`, one level at a time (`for _ in 0..queue.len()`), the largest of each level kept from `i64.MIN` up. O(n) time, O(width) space |
| `largest_values_depth.kara` | a preorder walk carrying the depth: the first node at a new depth opens that row's entry and later ones raise it, the list going down the recursion as `mut ref Vec[i64]`. O(n) time, O(height) stack |
| `largest_values_stack.kara` | the same walk on an explicit stack of `(TreeNode, i64)` popped with `while let`, each row's entry raised with `.max`. O(n) |
| `largest_values_rows.kara` | each row a whole `Vec[TreeNode]`, its largest found with `row.iter().map(\|n\| n.val).max()`, the next row built from the children and swapped in. O(n) time, O(width) space |
| `differential.kara` | the four arms on 1,500 random trees, five properties |

Every arm prints the same 8 lines: the two LeetCode examples, the empty
tree, one node, all values negative, a zigzag, the extremes -2^31 and
2^31 - 1, and for 300 random trees (0 to 60 nodes, the values from -2
to 2, from -1,000 to 1,000, or from the whole range in turn) the count
of rows and a checksum of the entries. The trees are given in
LeetCode's level order, built by the harness. `largest_values.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random trees of 0 to 40 nodes, the values from -2 to 2, from
-1,000 to 1,000, or from the whole range in turn, each new node hung
at the end of a random walk down from the root.

| | property |
|---|---|
| P1 | the entries are the reference's: every value gathered into its row's list, each list's largest found by a plain loop |
| P2 | there is one entry for each row, as many as the tree's height |
| P3 | the mirror image of the tree gives the same entries |
| P4 | k added to every value, k from -1,000 to 1,000, adds k to every entry |
| P5 | a new root over a copy of the tree on the left and its mirror image on the right puts its own value in front of the same entries |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each row's best starts at 0, not `i64.MIN` | P1 1188, P4 1313, P5 966 |
| M2 | ★: the smallest kept, `best.min` | killed at the first case (see below) |
| M3 | depth: a smaller value replaces the entry (`<` for `>`) | P1 1357 |
| M4 | depth: the right child counted in its parent's row | P1 1385, P2 1245, P3 1404, P5 1338 |
| M5 | stack: the last value seen replaces the entry | P1 1287, P3 1356, P5 1356 |
| M6 | stack: the right child pushed in place of the left | P1 1375, P2 1230, P3 1422, P5 1422 |
| M7 | rows: the smallest of each row, `.min()` | P1 1357 |
| M8 | rows: the left child pushed in place of the right | P1 1373, P2 1245, P3 1422 |
| E1 | ★: each row's best starts at -2^31 | 0 |
| E2 | depth: an equal value replaces the entry (`>=`) | 0 |
| E3 | stack: the two sides of `.max` swapped | 0 |
| E4 | rows: the next row built from the right, `row.iter().rev()` | 0 |

M2 starts each row at `i64.MIN` and keeps the smaller, so every entry
is `i64.MIN`. P1 reports the first case, and then P4's `got[i] + k`
overflows `i64` for a negative k: Kāra checks integer overflow, so the
run stops there with a runtime error, which is still a kill. E1 holds
because no value is below -2^31. E2 and E3 change nothing about which
value is largest. E4 holds because a row's largest does not depend on
the order its nodes are listed in.

M3 and M7 keep the smallest of each row and are seen only by the
reference: the smallest is as unmoved as the largest by the mirror
image, a shift and a new root. M1 is wrong only for rows whose values
are all below 0, so P4 sees it whenever the shift moves such a row.
M5 keeps whichever value of a row the stack reaches last, which the
mirror image changes but a shift does not. M4, M6 and M8 put nodes in
the wrong row or drop them, so P2 sees the count of rows change. M8
escapes P5: under the new root it drops the mirror image on the right
and keeps the copy on the left, whose rows it gets wrong in the same
way as the tree's.

## Verification

Every arm prints the same output as `largest_values.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `30000 checks, 0 failures` on the first two and runs clean
under the third. `karac check` passes on every arm, the differential
and the bench program.

The frozen legacy backends refuse every arm, the differential and the
bench program at type checking: legacy types the items of a `Vec`'s
`iter()` by value, so the harness's `*v` in `for v in row.iter()` is
"unary '*' requires 'ref T' ... found 'i64'". On copies that write `v`
there, the only change, `karac run --interp` prints the same output
for all four arms, and LLJIT and legacy `karac build` fail at codegen
with "Call parameter type does not match function signature!" at the
calls to `show`, whose first parameter is a `Str` given a string
literal (as in katas 501 to 503). Legacy is frozen, so these are
noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 random trees of 10,000
nodes (the problem's most), the values from the whole range, each tree
a random root over its list of values with those before it on the
left and those after it on the right, once. Then it solves each 50
times, folding every entry into a checksum. Every implementation
prints `100 trees of 10000 nodes, 50 times each: 155350 rows, checksum
312077034`, the Kāra program under `karac __mir-run` included (in
161 s).

Every mirror uses a fresh queue and a fresh answer list for every
call, as the ★ arm uses `VecDeque.new()` and `Vec.new()`: Rust a
`VecDeque` of `Rc<RefCell<TreeNode>>`, the closest match to a `shared
struct`, Go a slice read from the front, Python a `deque`, and C a
ring buffer it writes itself, grown by doubling. Spot timings on a
shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.90 to 0.93 s |
| Rust (`rustc -O`) | 1.34 to 1.50 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.27 to 1.39 s |
| Go | 1.37 to 1.42 s |
| Python | 14.1 to 14.3 s |
| Kāra (`karac build --mir`) | 2.42 to 2.43 s |

The legacy `karac build` refuses this program at the same `*v` (see
Verification). So `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`e85c10e377`. Under `karac __mir-llvm-run` the program prints the same
line in 7.3 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

None filed. Every arm, the differential and the bench program run
right on the v2 backends, and `karac check` passes on all of them as
first written.
