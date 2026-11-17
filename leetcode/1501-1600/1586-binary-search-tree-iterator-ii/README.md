# 1586. Binary Search Tree Iterator II

Implement the `BSTIterator` class that represents an iterator over the
in-order traversal of a binary search tree (BST):

- `BSTIterator(TreeNode root)` initializes an object of the class. The
  root of the BST is given as part of the constructor. The pointer is
  initialized to a non-existent number smaller than any element in the
  BST.
- `boolean hasNext()` returns `true` if there exists a number in the
  traversal to the right of the pointer, otherwise returns `false`.
- `int next()` moves the pointer to the right, then returns the number at
  the pointer.
- `boolean hasPrev()` returns `true` if there exists a number in the
  traversal to the left of the pointer, otherwise returns `false`.
- `int prev()` moves the pointer to the left, then returns the number at
  the pointer.

You may assume that `next()` and `prev()` calls will always be valid.

```
root = [7,3,15,null,null,9,20]
next, next, prev, next, hasNext, next, next, next, hasNext, hasPrev, prev, prev
  ->  3, 7, 3, 7, true, 9, 15, 20, false, true, 15, 9
```

**Constraints:** the number of nodes is in `[1, 10^5]`;
`0 <= Node.val <= 10^6`; at most `10^5` calls to `hasNext`, `next`,
`hasPrev` and `prev`.

## Approaches

| file | mechanism |
|---|---|
| `bst_iterator.kara` ★ | the in-order walk made lazily: a stack of the left spine still to visit, and every value given out kept in a `Vec` with the iterator's place in it; `next` reads the list, or pops the stack once the list runs out, and `prev` steps back in the list. O(1) amortized a call, O(n) space for the values met |
| `bst_iterator_flat.kara` | every value up front, by a recursive in-order walk into one `Vec`; the iterator is a place in it. O(n) to build, O(1) a call |
| `bst_iterator_search.kara` | no state but the value it stands on (`Option[i32]`), each call a search from the root for the smallest value above it or the largest below. O(h) a call, O(1) space |
| `bst_iterator_solution.kara` | LeetCode's Rust template (a stack of `Rc<RefCell<TreeNode>>`, `n.borrow().left.clone()`, a `usize` count of the values given out), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

The tree is a `shared struct TreeNode`, LeetCode's node, built by
inserting values in order (a repeat is dropped); LeetCode's example tree
is the insertion order `[7, 3, 15, 9, 20]`. Every arm prints the same 8
lines: LeetCode's example and four more (one value, a chain to the right,
a chain to the left, a full tree of seven) in LeetCode's answer form, then
the node count, call count and a checksum of every answer for 3000 random
trees of up to 8 values below 20 with 20 calls each, 300 of up to 1000
values with 2000 calls, and 3 of up to 100000 with 100000 calls. Every
call is valid where it is drawn: a `next` only while a value is left, a
`prev` only past the first. `bst_iterator.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms, each struct renamed
and driven by its own copy of the harness's `drive`, and the statement
read literally: the tree's values from a walk in any order, sorted, and a
pointer that starts before the first and moves one place a `next` or
`prev`. It checks 3000 trees of 1 to 7 values from 0 to 14, each driven
by 1 to 25 calls, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | the same values inserted in reverse order (another tree) leave the answers |
| P3 | every value raised by 1000 raises each `next` and `prev` by 1000 |
| P4 | every value doubled doubles each `next` and `prev` |
| P5 | a `next` and a `prev` put in where both are valid leave every other answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 33796032, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

Three first choices were replaced: in the search arm, moving the value
to a wrong neighbour (`>=` for `>`, or descending the wrong way) was
killed only by an `unwrap` panic, since the arm keeps no state but the
value, and a lost value in the ★ arm's spine likewise; the search arm's
mutants are its `has_` calls instead.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `has_next` ignores the list of values met | P1 410, P5 113, P6 410 |
| M2 | ★: `has_prev` true at the first value | P1 1606, P6 1606 |
| M3 | ★: `has_next` ignores the stack | P1 1595, P5 317, P6 1595 |
| M4 | flat: the walk visits a node before its left subtree | P1 2010, P2 2334, P6 2010 |
| M5 | flat: `has_next` true at the last value | P1 1821, P6 1821 |
| M6 | search: `has_next` searches from no value at all | P1 1821, P6 1821 |
| M7 | search: `has_prev` asks for a larger value | P1 1794, P6 1794 |
| M8 | search: `has_prev` true before the first `next` | P1 1212, P6 1212 |
| M9 | template: `has_prev` true at the first value | P1 1606, P6 1606 |
| M10 | template: `prev` returns the value it leaves | P1 1587, P6 1587 |

## Benchmarks

The bench runs the ★ arm on 20 trees of 100000 random values, each
driven by 300000 calls, all drawn first, in all five languages. Every
implementation prints `20 trees of 100000 values: 1903285 nodes, 6000000
calls, checksum 376631251`. The C mirror keeps the lazy in-order stack
and the list of values met. Each node is its own malloc; the stack, the
list and the answers are growable arrays allocated per call.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5dc4418bbd` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.660 s |
| Go | 0.997 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.045 s |
| Kāra (`karac build`) | 1.053 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.073 s |
| Rust (`rustc -O`) | 1.079 s |
| Python | 12.4 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is below its real time (0.970 s and 1.069 s on one run).

## Verification

All four arms print the same output as `bst_iterator.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5dc4418bbd`.

## Writing it

The ★, flat and search arms were written in Kāra and checked as written,
but for one line of the shared harness: it wrote `["null".to_string()]`
and `"true".to_string()`, and `karac fix` dropped the `to_string()`s, as
a list of `String`s takes the literals.

The Rust template took four rounds of `karac fix`:

1. the `Vec<..>` and `Option<Rc<RefCell<TreeNode>>>` types to `[..]`
   form, `use std::rc::Rc` dropped, `Vec::new()` to `Vec.new()`, `&self`
   and `&mut self` to `self` and `mut ref self`, the `mut node` parameter
   to `own` and a `let mut`, `||` to `or` and `!` to `not`;
2. `Rc[RefCell[TreeNode]]` to `TreeNode` (a `shared struct` is counted
   already), `use std::cell::RefCell` dropped, and each `n.borrow()`
   dropped;
3. the `usize` count to `i64`;
4. the harness line above.

It then checks and agrees with no hand edit. The `.clone()` on
`n.left` is left: it copies a counted reference, as in Rust.

The class is `BstIterator` in every Kāra file, not LeetCode's
`BSTIterator`: a later `karac` (the `acronym_case` lint, design.md §3
CN-4) writes an acronym in a type name as a word, and `karac fix`
renamed it in each arm and the bench. The C, Rust and Go mirrors keep
LeetCode's name.
