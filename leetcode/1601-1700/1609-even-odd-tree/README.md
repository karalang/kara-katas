# 1609. Even Odd Tree

A binary tree is named **Even-Odd** if it meets the following
conditions:

- The root of the binary tree is at level index `0`, its children are at
  level index `1`, their children are at level index `2`, etc.
- For every **even-indexed** level, all nodes at the level have **odd**
  integer values in **strictly increasing** order (from left to right).
- For every **odd-indexed** level, all nodes at the level have **even**
  integer values in **strictly decreasing** order (from left to right).

Given the `root` of a binary tree, *return* `true` *if the binary tree is*
***Even-Odd****, otherwise return* `false`*.*

```
root = [1,10,4,3,null,7,9,12,8,6,null,null,2]  ->  true
root = [5,4,2,3,3,7]                           ->  false
root = [5,9,1,3,5,7]                           ->  false
```

**Constraints:** the number of nodes in the tree is in the range
`[1, 10^5]`; `1 <= Node.val <= 10^6`.

## Approaches

| file | mechanism |
|---|---|
| `even_odd.kara` ★ | breadth first over a `VecDeque`, a level at a time (`for _ in 0..queue.len()`); the value before on the level an `Option[i32]`, each value checked with `prev.is_none_or(\|p\| v > p)`. O(n) time, O(width) space |
| `even_odd_dfs.kara` | a preorder walk, left before right, which meets each level left to right, keeping the last value seen at each depth in a `Vec[i32]` passed `mut`. O(n) time, O(height) space |
| `even_odd_levels.kara` | whole levels: each a `Vec[TreeNode]` built from the one above by `flat_map`, its values checked all at once with `all` and `windows(2)`. O(n) time, O(width) space |
| `even_odd_solution.kara` | LeetCode's Rust template (`Rc<RefCell<TreeNode>>`, `i32::MIN` / `i32::MAX` as the value before a level's first, `node.borrow()`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and four
more (one odd node, one even node, a level of equal values, and a level
rising where it should fall), then the count even-odd and a checksum of
the answers for 3000 random trees of up to 8 nodes, 300 of up to 1000,
and 10 of up to 100000. Each random tree is made even-odd, then half are
spoiled: one value moved by one, or two values swapped (which may be one
node with itself, or leave the tree even-odd). `even_odd.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: one recursive walk files every value under its level, left to
right, and each level is then checked against the rule for its index. It
checks 3000 trees of 1 to 8 nodes, made and spoiled as above with values
from 1 to 1000, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the tree mirrored, each value `v` made `2000 - v`, leaves the answer |
| P3 | every value raised by 2 leaves the answer |
| P4 | the tree hung under a new root of 1, each value `v` made `1001 - v`, leaves the answer |
| P5 | the root's value made even gives `false` |
| P6 | each arm agrees with at least two of the other three |

P2 holds because mirroring reverses every level and `2000 - v` reverses
it again without changing a parity; P4 because the new root moves every
level to the other parity, and `1001 - v` both flips each value's parity
and reverses its order.

The differential prints `3000 problems: checksum 839770412, 72000 checks over 4 arms: 0 failures` under every lane in Verification. On
a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to four to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M1, M6 and M8 are killed the fewest
times: they matter only where two values on a level are equal, or where
a level's last value is forgotten, and a tree of eight nodes seldom
shows either.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an even level's values allowed to repeat | P1 5, P4 9, P6 5 |
| M2 | ★: an odd level's first value refused | P1 806, P4 210, P6 806 |
| M3 | ★: every level taken as even | P1 841, P4 990, P6 841 |
| M4 | ★: a right child queued at the front | P1 543, P2 2, P6 543 |
| M5 | dfs: each level's parity rule turned round | P1 1278, P4 262, P5 497, P6 1278 |
| M6 | dfs: the last value at a depth never updated | P1 2, P2 1, P6 2 |
| M7 | dfs: a right child walked at its parent's depth | P1 747, P2 227, P6 747 |
| M8 | levels: an odd level's values allowed to repeat | P1 4, P4 9, P6 4 |
| M9 | levels: the next level built right child first | P1 543, P6 543 |
| M10 | template: an odd level's first value bounded by 1000 | P1 345, P2 461, P3 284, P4 354, P6 345 |

## Benchmarks

The bench makes 20 even-odd trees of 100000 nodes and 20 pairs of nodes each, all of it first. Then: each tree checked as made and with each pair of values swapped, breadth first over a VecDeque. Every implementation prints `20 trees of 100000 nodes: 420 checks, 20 even-odd, checksum 999274249`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5bb1708545` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.321 s |
| Kāra (`karac build`) | 0.462 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.497 s |
| Rust (`rustc -O`) | 0.517 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.523 s |
| Go | 1.085 s |
| Python | 11 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its user time is not above its real time (0.418 s and 0.470 s on one run).

## Verification

All four arms print the same output as `even_odd.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5bb1708545`.

## Writing it

The ★ arm wrote `prev.is_none_or(|p| v > p)`, Rust's dual of
`is_some_and`, and `Option` had no `is_none_or`: it was refused with a
bare "no method", and it is now a library method (B-2026-11-18-8).

The levels arm wrote three Rust habits. `values.windows(2).all(..)` is
an iterator method on the `Vec` `windows` returns, and `karac fix` added
`.into_iter()`. `flat_map(|node| [node.left, node.right]).flatten()`
hands `flat_map` an array and `flatten` items that are `Option`s, and
`karac fix` made it `flat_map(|node| [node.left, node.right].into_iter())`
then `filter_map(|v| v)`. `root.into_iter().collect()`, the root as a
level of zero or one node, was refused: an `Option` has no `iter` or
`into_iter` (B-2026-11-18-11), and that line is a `match` instead. The dfs
arm was written in Kāra and checked as written. The bench's harness wrote `tree[*a]` for an index `a` bound by
`for (a, b) in pairs.iter()`, and `karac fix` took the four `*` off: a
tuple pattern over `iter()` binds the copied `i64`s themselves.

The Rust template took one `karac fix` of 18 edits: the `use` lines
dropped, `struct Solution;` to `struct Solution {}`, the `<..>` types to
`[..]`, `Option<Rc<RefCell<TreeNode>>>` to `Option[TreeNode]`,
`VecDeque::new()` to `VecDeque.new()`, `let node = node.borrow();`
dropped, `i32::MIN` and `i32::MAX` to `i32.MIN` and `i32.MAX`, `!` to
`not`, `||` to `or`, and `Solution::` to `Solution.`. It then checks and
agrees with no hand edit.
