# 2096. Step-By-Step Directions From a Binary Tree Node to Another

You are given the `root` of a binary tree with `n` nodes. Each node is
uniquely assigned a value from `1` to `n`. You are also given an integer
`startValue` representing the value of the start node `s`, and a
different integer `destValue` representing the value of the destination
node `t`.

Find the shortest path starting from node `s` and ending at node `t`.
Generate step-by-step directions of such path as a string consisting of
only the uppercase letters `'L'`, `'R'`, and `'U'`. Each letter
indicates a specific direction:

- `'L'` means to go from a node to its left child node.
- `'R'` means to go from a node to its right child node.
- `'U'` means to go from a node to its parent node.

Return the step-by-step directions of the shortest path from node `s` to
node `t`.

```
root = [5,1,2,3,null,6,4], startValue = 3, destValue = 6  ->  "UURL"
root = [2,1], startValue = 2, destValue = 1               ->  "L"
```

**Constraints:** the number of nodes in the tree is `n`; `2 <= n <=
10^5`; `1 <= Node.val <= n`; all the values in the tree are unique; `1
<= startValue, destValue <= n`; `startValue != destValue`.

A tree has one way between any two nodes: up from the start to their
lowest common ancestor, then down to the destination. The ways from the
root to the two nodes agree down to that ancestor, so dropping their
common start leaves the start's climb, all `U`, and the destination's
descent. The approaches differ in how they find the ancestor and the two
ways.

## Approaches

| file | mechanism |
|---|---|
| `directions.kara` ★ | the way from the root to each node by a recursive depth-first search that pushes a step onto a `String` through `mut ref` before going down and pops it on a miss; the common start counted, one `U` for each step the start has left, then the rest of the destination's way. O(n) |
| `directions_parents.kara` | one breadth-first walk from the root (a `VecDeque`) records each value's parent, depth and step in `Map`s; the deeper end climbs first, then both together until they meet, the destination's steps read back to front. O(n) |
| `directions_lca.kara` | a recursive `lca` returning the node under which both lie, `depth_of` the start below it and `steps_to` the destination's way down as an `Option[String]` built with `f"L{rest}"`. O(n) |
| `directions_stack.kara` | one walk with an explicit `Vec[(TreeNode, String)]` stack, each entry carrying its way, stopping once both are met; the shared start counted with `zip`, `take_while` and `count` |
| `directions_graph.kara` | a `struct Roads` of each value's neighbours as a `Map[i64, Vec[(i64, char)]]`, `L`/`R` down and `U` up, searched breadth first from the start and read back from the destination |
| `directions_solution.kara` | LeetCode's Rust template (`Option<Rc<RefCell<TreeNode>>>` with `i32` values, a `find` nested in the method over `&n.left` through `borrow()` into a `Vec<u8>`, the answer `"U".repeat(..)` and `std::str::from_utf8(&d[i..])`), carried by `karac fix` in five rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and five
more, each tree and question with its directions; then the steps and a
checksum of the directions for 2000 random trees of 2 to 60 nodes; then
the constraints' largest, 100000 nodes in a random tree, and in a chain
of left children walked down from the top and up from the bottom.
`directions.py` mirrors the ★ arm and its output is byte-identical; it
recurses as deep as the chain, so it runs in a thread with a large
stack.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the shortest string of `U`, `L` and `R` that, walked from the
start, reaches the destination, found by trying every string in order of
length. It checks 300 random trees of 2 to 8 nodes; then 20 chains of 6
to 8 nodes, each step down a random side; then 20 random trees of 9 or
10 nodes; each with a random start and destination. All 340 are drawn
before any arm answers. The Rust arm is given a copy of each tree in its
own `i32` nodes.

| | property |
|---|---|
| P1 | the directions are the statement read literally |
| P2 | the way back has the ups and downs counted the other way round: as many `U` as the way there has `L` and `R`, and as many `L` and `R` as it has `U` |
| P3 | every `U` comes before every `L` and `R` |
| P4 | the tree mirrored, every node's children swapped, gives the directions with `L` and `R` swapped |
| P5 | the directions, walked from the start, end at the destination |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 trees: checksum 636814649, 12240 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal directions was checked against a Python reading of the
same trees, which compares the ways from the root. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the right side's step written `L` | P1 178, P4 164, P5 178, P6 178 |
| M2 | ★: a failed right step left on the way | P1 152, P4 179, P5 152, P6 152 |
| M3 | ★: the ups counted from the destination | P1 311, P2 311, P5 311, P6 311 |
| M4 | parents: the steps down in climbing order | P1 58, P5 58, P6 58 |
| M5 | parents: the start's lone climbs not counted | P1 147, P2 311, P5 147, P6 147 |
| M6 | parents: each step recorded as the other side | P1 220, P5 220, P6 220 |
| M7 | lca: the start's depth one more each level | P1 208, P2 340, P5 208, P6 208 |
| M8 | lca: the left steps written after the rest | P1 35, P4 64, P5 35, P6 35 |
| M9 | lca: the left steps written `R` | P1 133, P4 220, P5 133, P6 133 |
| M10 | stack: the shared start counted to the shorter way's end | P1 88, P5 88, P6 88 |
| M11 | stack: the destination's whole way | P1 138, P2 138, P5 138, P6 138 |
| M12 | stack: the left child given its parent's way | P1 241, P4 321, P5 241, P6 241 |
| M13 | graph: the steps read in walking order | P1 123, P3 88, P5 123, P6 123 |
| M14 | graph: a down step written `U` | P1 220, P2 340, P5 220, P6 220 |
| M15 | graph: the last step dropped | P1 340, P2 88, P5 340, P6 340 |
| M16 | solution: the differing start counted as shared | P1 196, P5 58, P6 196 |
| M17 | solution: a failed left step left on the path | P1 254, P4 330, P5 254, P6 254 |

P1 and P6 kill all seventeen, P5 all seventeen too, P2 and P4 six each,
and P3 one. P5, the walk, misses only answers that still reach the
destination the long way round: M16 counts a differing first step as
shared, which climbs past the ancestor and comes down again, wrong 196
times and lost only 58. P4 sees an arm that treats the two sides
unalike (M1, M2, M9, M12, M17), or writes a step out of place (M8). P2
sees an arm whose count of ups or downs goes wrong (M3, M5, M7, M11,
M14, M15). P3 sees only M13, the one edit that can put an `L` or `R`
before a `U`: the graph arm's steps read from the start's end.

Of the thirty, thirteen were not kept, and none survives. Seven fail as
a kept one: the ★ arm's first steps taken as shared as M4; its
destination's whole way as M11; the ups counted from the destination,
in the stack and Rust arms, as M3; the right side's step written `L`,
in the stack and Rust arms, as M1; the graph arm's up step written as
the child's side as M7. Three fail the same way as each other and were
left out together: the right child's step written `L` in the parents,
lca and graph arms (P1 151, P4 220, P5 151). Two are killed with checks
of their own but were left out because their arm keeps its share: the
parents arm's two ups for each shared climb (P1 88, P2 88, P5 88) and
the Rust arm's adapter with its ends swapped (P1 340, P5 340). One
crashes and is not kept: the lca arm's ancestor taken as the left
side's find, whose destination is then not below it, so `steps_to`
finds nothing to unwrap.

## Verification

Every arm prints the same output as `directions.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 4.1 s to 9.6 s, and the
differential 1.2 s (timed while other work shared the machine).

The Rust arm met a gap in `karac fix`. The template ends with
`ans.push_str(std::str::from_utf8(&d[i..]).unwrap())`; the fix dropped
the `std::` and wrote `str.from_utf8`, and in the next round took the
resolver's nearest name for the undefined `str` and wrote
`ptr.from_utf8`, which cannot be typed. Rust's `str::from_utf8` is
Kāra's `String.from_utf8`: the path fix now writes that, and an
undefined `str` suggests `String`. Fixed in kara 81aca4606b, test
`tests/kata_2096_str_from_utf8_fix.rs`.

With that, `karac fix` carries the template in five rounds of 33, 6, 3,
4 and 1 edits: Rust's spellings (`Option<Rc<RefCell<TreeNode>>>` to
brackets, `&` to `ref` and `&mut` to `mut ref`, `&&` to `and`,
`std::str::from_utf8` to `String.from_utf8`, `Solution::` to `.`,
`struct Solution;` to `struct Solution {}`); then the `use` lines
dropped, `Rc[RefCell[TreeNode]]` to `TreeNode` and `.borrow()` dropped,
and the nested `find` moved out of the method; then `mut` on the
recursive calls' `path` and `vec![]` to `Vec.new()`; then the adapter's
`ref` parameter to a bare one, which borrows already. The fixed arm
reads as the template does, down to the `let n = n;` its `borrow()`
left. The parents arm was first written with Rust's `let (mut a, mut b)
= ..`, which `karac fix` made `let mut (a, b) = ..`.

## Benchmarks

The bench builds one random tree of 100000 nodes, the constraints'
largest, and asks it 1000 questions with the ★ arm in all five
languages: two recursive searches from the root per question, each way
in a growable buffer (a `String`, a `String`, a byte slice, a `list`, a
`malloc`'d buffer). The nodes are Kāra's `shared struct`, Rust's
`Rc<RefCell<TreeNode>>`, C's structs in one `malloc`'d array, Go's
`*TreeNode` and Python objects. Every implementation prints `1000
answers: 35693 steps, checksum 940925265`.

BENCHTAB
