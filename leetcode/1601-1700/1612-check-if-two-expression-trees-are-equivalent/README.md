# 1612. Check If Two Expression Trees are Equivalent

A **binary expression tree** is a kind of binary tree used to represent
arithmetic expressions. Each node of a binary expression tree has either
zero or two children. Leaf nodes (nodes with 0 children) correspond to
operands (variables), and internal nodes (nodes with two children)
correspond to the operators. In this problem, we only consider the `'+'`
operator (i.e. addition).

You are given the roots of two binary expression trees, `root1` and
`root2`. Return `true` *if the two binary expression trees are
equivalent*. Otherwise, return `false`.

Two binary expression trees are equivalent if they **evaluate to the same
value** regardless of what the variables are set to.

```
root1 = [x],                      root2 = [x]                      ->  true
root1 = [+,a,+,null,null,b,c],    root2 = [+,+,a,b,c]              ->  true
root1 = [+,a,+,null,null,b,c],    root2 = [+,+,a,b,d]              ->  false
```

**Constraints:** the number of nodes in both trees is equal, odd and in
the range `[1, 4999]`; `Node.val` is `'+'` or a lower-case English
letter; it is guaranteed that the trees given are valid binary
expression trees.

## Approaches

With `+` the only operator, an expression's value is the sum of its
leaves, whatever their grouping or order, so two trees are equivalent
exactly when they hold each letter the same number of times. (The
follow-up's `-` is not taken up here.) The node is a `shared struct`
with a `char` value, as LeetCode's `Node` with `val: char`.

| file | mechanism |
|---|---|
| `equivalent.kara` ★ | one recursive walk counts the first tree's leaves up and the second's down, into one `Array[i32, 26]` passed `mut ref`; equivalent when every count ends at zero. O(n) time, O(height) stack |
| `equivalent_map.kara` | each tree's leaves counted into a `Map[char, i64]` by a walk with an explicit stack, a `match` on `(n.left, n.right)` telling leaves from `+`, and the two maps compared with `==`. O(n) |
| `equivalent_sorted.kara` | each tree's leaves listed by a recursive walk into a `Vec[char]`, sorted, and the two lists compared. O(n log n) |
| `equivalent_solution.kara` | LeetCode-style Rust (`Option<Rc<RefCell<Node>>>`, a nested `fn dfs` taking `&Option<..>` and `&mut [i32; 26]`, `n.borrow()`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and three
more (a leaf against a sum, one letter twice against two letters, and the
same letters regrouped), then the leaves, the count equivalent and a
checksum for 3000 pairs of up to 6 leaves from 3 letters, 300 of up to
1000 leaves from 26 letters, and 3 of up to 100000 leaves from 26 letters,
past LeetCode's bound. Each pair's second expression is built over the
first's leaves shuffled, and in half the pairs one of its leaves is
changed (which may change it to itself); each expression joins two
random loose subtrees under a `+` until one is left. `equivalent.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: both trees evaluated under three settings of the 26 variables
drawn at random, the sums taken mod 10^9 + 7, and equivalent when every
setting gives one value. It checks 3000 pairs of expressions over 1 to 6
leaves from 1 to 4 letters, made as above, an eighth also with a leaf
added to the second, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the two trees swapped leave the answer |
| P3 | a tree is equivalent to itself |
| P4 | a `z` added to both trees, on different sides of a `+`, leaves the answer |
| P5 | a tree is not equivalent to itself plus `b` |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 339393951, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M3 is the one only P2 kills: with
counts allowed to end above zero, a second tree whose leaves are some of
the first's passes, and only swapping the trees shows it, since no pair
is made that way.

The first M7, a leaf taken as any node with a child missing, is
equivalent in a valid expression tree, where a node has both children or
neither, and was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the second tree counted up, not down | P1 2014, P3 3000, P6 2014 |
| M2 | ★: right subtrees not walked | P1 934, P4 1952, P5 3000, P6 934 |
| M3 | ★: counts allowed to end above zero | P2 272 |
| M4 | map: a letter seen once however often | P1 454, P5 1588, P6 454 |
| M5 | map: left children skipped while the stack is short | P1 954, P4 1976, P5 779, P6 954 |
| M6 | sorted: the leaves not sorted | P1 795, P4 1219, P6 795 |
| M7 | sorted: only the first three leaves kept | P1 601, P4 1125, P5 2007, P6 601 |
| M8 | template: left subtrees always counted up | P1 1661, P3 2504, P4 353, P6 1661 |
| M9 | template: only `a` and `b` compared | P1 57, P6 57 |
| M10 | map: only the number of letters compared | P1 637, P5 1588, P6 637 |

## Benchmarks

The bench makes 10 pairs of expressions over 50000 leaves from 26 letters, all of it first. Then: each pair checked 10 times by one counting walk. Every implementation prints `10 pairs of 50000 leaves from 26 letters, 100 checks: 40 equivalent, checksum 870381383`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5bb1708545` on LLVM 22:

| | median |
|---|---|
| Go | 0.379 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.562 s |
| C (`clang -O3`) | 0.576 s |
| Kāra (`karac build`) | 0.611 s |
| Rust (`rustc -O`) | 0.611 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.786 s |
| Python | 5.6 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its user time is not above its real time (0.465 s and 0.503 s on one run).

## Verification

All four arms print the same output as `equivalent.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5bb1708545`.

## Writing it

The ★ arm wrote Rust's `[i32; 26]` as a parameter type, and `karac fix`
made it `Array[i32, 26]`; it indexed with `(n.val as u8 - b'a') as i64`,
and `karac fix` made the `char` a `u32` before the `u8`
(`n.val as u32 as u8 - b'a'`) and dropped the `as i64`. The shared
harness wrote `'a' as u8 + ..`, refused because a `char` does not fit a
`u8`, and `karac fix` made it the byte literal `b'a'`. The map and sorted
arms were written in Kāra and checked as written.

The Rust template took one `karac fix` of 41 edits, the harness's two
`b'a'` among them: the `use` lines dropped, `struct Solution;` to
`struct Solution {}`, `Option<Rc<RefCell<Node>>>` to `Option[Node]`, the
nested `fn dfs` hoisted out of the method, `&Option<..>` and
`&mut [i32; 26]` to `Option[Node]` and `mut ref Array[i32, 26]`,
`let n = n.borrow();` dropped, each `&` and `&mut` at a call dropped or
made `mut`, `n.val as u8` made `n.val as u32 as u8`, `|&c|` to `|c|`, and
`Solution::` to `Solution.`. It then checks and agrees with no hand edit.
