# 1597. Build Binary Expression Tree From Infix Expression

A binary expression tree is a binary tree used to represent arithmetic
expressions. Each leaf holds an operand (a single digit) and each inner
node holds one of the operators `+`, `-`, `*` and `/`, with exactly two
children.

Given a string `s`, an infix expression of single digits, the four
operators and parentheses, return any valid binary expression tree whose
in-order traversal reproduces `s` without its parentheses. The usual
order of operations applies: parentheses first, then `*` and `/`, then
`+` and `-`, operators of one level taken from the left; the operands
appear in the tree in the order they appear in `s`.

```
s = "3*4-2*5"      ->  [-,*,*,3,4,2,5]
s = "2-3/(5*2)+1"  ->  [+,-,1,2,/,null,null,null,null,3,*,null,null,5,2]
s = "1+2+3+4+5"    ->  [+,+,5,+,4,null,null,+,3,null,null,1,2]
```

**Constraints:** `1 <= s.length <= 100`; `s` holds digits and the
characters `+`, `-`, `*`, `/`, `(` and `)`; every operand in `s` is one
digit; `s` is a valid expression.

## Approaches

The tree is LeetCode's node, a `shared struct Node` with a `char` and two
`Option[Node]` children, and every arm returns the tree that groups
operators of one level from the left, the one LeetCode's examples show.

| file | mechanism |
|---|---|
| `expression_tree.kara` ★ | two stacks, as the shunting-yard reads an expression: digits become leaves on a stack of trees, and an operator first joins every operator waiting of the same or higher precedence with the two trees below it; `(` waits for its `)`. O(n) |
| `expression_tree_descent.kara` | recursive descent: a `Parser` struct of characters and a place, with `expression`, `term` and `factor` methods that call one another, each loop joining from the left. O(n) |
| `expression_tree_split.kara` | by the last operator to apply: parentheses around the whole text taken off, then the rightmost `+` or `-` outside every parenthesis, or failing that the rightmost `*` or `/`, is the root, and each side is built the same way, as `Str` slices. O(n^2) |
| `expression_tree_solution.kara` | LeetCode's Rust template (a `Vec<char>` of operators, a `Vec<Option<Rc<RefCell<Node>>>>` of trees, nested `fn prec` and `fn combine`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and four
more (one digit, a digit in three pairs of parentheses, a chain nested to
the right, and a mix of all four operators) in LeetCode's answer form,
then the node count and a checksum of every answer for 3000 random
expressions of up to 4 digits, 300 of up to 12 and 30 of up to 25, a
quarter of their parts in parentheses. `expression_tree.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the order of operations applied by hand to a list of items.
The innermost parentheses first; inside them the leftmost `*` or `/` with
its two neighbours, or failing that the leftmost `+` or `-`, made one
tree; a pair of parentheses around one tree dropped; until one tree is
left. It checks 3000 expressions of up to 6 digits, every random choice
drawn before any arm answers.

| | property |
|---|---|
| P1 | the tree is the one the order of operations builds, read literally |
| P2 | the tree read in order is the expression without its parentheses |
| P3 | the expression in one more pair of parentheses leaves the tree |
| P4 | each digit `d` made `9 - d` makes the same change to the tree |
| P5 | `+` and `-` swapped, and `*` and `/`, make the same change to the tree |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 752074346, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

The first M2, `/` left out of the higher precedence, was killed only by
an `unwrap` panic: `/` then shared the precedence of `(`, so a `/`
joined a waiting `(` as if it were an operator.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: operators of one level grouped from the right | P1 743, P6 743 |
| M2 | ★: `*` and `/` given the precedence of `+` and `-` | P1 446, P6 446 |
| M3 | ★: a joined operator's children swapped | P1 1828, P2 1816, P6 1828 |
| M4 | descent: a term stops at `/` | P1 858, P2 858, P3 87, P5 1367, P6 858 |
| M5 | descent: a `+` or `-` puts the right side on the left | P1 1329, P2 1320, P6 1329 |
| M6 | split: the leftmost `+` or `-` taken as the root | P1 445, P6 445 |
| M7 | split: any text starting `(` taken as wrapped whole | P1 257, P2 257, P6 257 |
| M8 | split: `*` and `/` taken as the root before `+` and `-` | P1 696, P6 696 |
| M9 | template: `+` and `-` given the precedence of `*` and `/` | P1 446, P6 446 |
| M10 | template: operators of one level grouped from the right | P1 743, P6 743 |

## Benchmarks

The bench runs the ★ arm on 200000 expressions of up to 50 digits, all
drawn first, each tree folded to a hash, in all five languages. Every
implementation prints `200000 expressions, 3462496 characters: checksum
482433585`. The C mirror keeps two stacks, as the shunting-yard reads an
expression, each node a malloc freed with its tree, each tree folded to
a hash. Each expression is a malloc'd string, as Kāra's String is.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5dc4418bbd` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.164 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.267 s |
| Kāra (`karac build`) | 0.269 s |
| Go | 0.327 s |
| Rust (`rustc -O`) | 0.363 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.365 s |
| Python | 3.6 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is below its real time (0.260 s and 0.267 s on one run).

## Verification

All four arms print the same output as `expression_tree.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them but the descent arm and the differential, where it gives the
note design.md § Effect Inference asks for on a mutual recursion group
(`expression`, `term` and `factor`), which `karac run` also prints; and
`karac fix` has nothing left to change. Checked at kara `5dc4418bbd`.

## Writing it

The ★, descent and split arms were written in Kāra and checked as
written, but for two lines of the shared harness: it took a `String` out
of a list of literals by index, and `karac fix` wrote `.clone()`; and it
wrote `*c` in a `filter` over `chars()`, and `karac fix` dropped the `*`,
as a `char` is passed by value. The differential wrote `from.find(c)`
for a `char`, and `karac fix` made it `c.to_string()`, as `find` takes a
`Str`.

The Rust template took one run of `karac fix`, of 61 edits: the `use`
lines dropped, `struct Solution;` to `struct Solution {}`, the nested
`fn prec` and `fn combine` hoisted to the top level,
`Option<Rc<RefCell<Node>>>` to `Option[Node]` (a `shared struct` is
counted already), `Rc::new(RefCell::new(Node::new(c)))` to
`Node.new(c)`, each `borrow_mut()` dropped, `&mut Vec<..>` parameters to
`mut ref Vec[..]`, the calls' `&mut` to `mut`, `Vec::new()` to
`Vec.new()`, `!` to `not`, `&&` to `and`, and `Solution::` to
`Solution.`. It then checks and agrees with no hand edit.
