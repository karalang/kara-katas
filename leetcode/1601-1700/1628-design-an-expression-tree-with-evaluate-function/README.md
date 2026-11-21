# 1628. Design an Expression Tree With Evaluate Function

Given the `postfix` tokens of an arithmetic expression, build and return
*the binary expression tree that represents this expression.*

**Postfix** notation is a notation for writing arithmetic expressions in
which the operands (numbers) appear before their operators. For example,
the postfix tokens of the expression `4*(5-(7+2))` are represented in the
array `postfix = ["4","5","7","2","+","-","*"]`.

The class `Node` is an interface you should use to implement the binary
expression tree. The returned tree will be tested using the `evaluate`
function, which is supposed to evaluate the tree's value. You should not
remove the `Node` class; however, you can modify it as you wish, and you
can define other classes to implement it if needed.

A **binary expression tree** is a kind of binary tree used to represent
arithmetic expressions. Each node of a binary expression tree has either
zero or two children. Leaf nodes (nodes with 0 children) correspond to
operands (numbers), and internal nodes (nodes with two children)
correspond to the operators `'+'` (addition), `'-'` (subtraction), `'*'`
(multiplication), and `'/'` (division).

It's guaranteed that no subtree will yield a value that exceeds `10^9` in
absolute value, and all the operations are valid (i.e., no division by
zero).

**Follow up:** Could you design the expression tree such that it is more
modular? For example, is your design able to support additional
operators without making changes to your existing `evaluate`
implementation?

```
postfix = ["3","4","+","2","*","7","/"]  ->  2    ((3+4)*2)/7
postfix = ["4","5","2","7","+","-","*"]  ->  -16  4*(5-(2+7))
```

**Constraints:** `1 <= s.length < 100`; `s.length` is odd; `s` consists
of numbers and the characters `'+'`, `'-'`, `'*'`, and `'/'`; if `s[i]`
is a number, its integer representation is no more than `10^5`; it is
guaranteed that `s` is a valid expression; the absolute value of the
result and intermediate values will not exceed `10^9`; it is guaranteed
that no expression will include division by zero.

## Approaches

| file | mechanism |
|---|---|
| `expression.kara` ★ | the design asked for, made modular as the follow-up asks: a `Node` trait with `evaluate`, one struct per operator holding its operands as `dyn Node` fields, and a `TreeBuilder` whose `build_tree` reads the tokens onto a `Vec[dyn Node]`; a new operator is a new struct and one line in `operator`. O(n) |
| `expression_enum.kara` | the tree as a `shared enum Expr`, a variant per operator holding counted handles to its operands, and `evaluate` one `match`. O(n) |
| `expression_arena.kara` | the tree in one `Vec` of `Node` structs, children by index; postfix order puts every node after both its children, so one pass in arena order evaluates it with no recursion. O(n) |
| `differential.kara` | the three arms against the statement read literally, six properties |

LeetCode offers no Rust template for this problem, so there is no
Rust-template arm.

Every arm prints the same 6 lines: LeetCode's two examples, one operand
alone, and `(0 - 7) / 2`, which truncates toward zero to `-3`; then the
values summed and a checksum for 3000 random expressions of up to 8
operands below 10, so zeros are common, and 300 of up to 50 operands up
to `10^5`. The generator swaps an operator that would divide by zero or
leave `10^9` in absolute value for one that does not, as LeetCode
promises. `expression.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the three arms and the statement
read literally: the postfix evaluated on a stack of values, an operator
taking the top value as its right operand, with no tree at all. It
checks 3000 random expressions of 1 to 12 operands, every other one with
operands below 10 and the rest up to `10^5`. Every expression is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the value is the postfix evaluated on a stack, with no tree |
| P2 | adding 0 leaves the value |
| P3 | multiplying by 1 and dividing by 1 leave the value |
| P4 | 0 minus the expression is the value negated |
| P5 | the expression minus itself is 0 |
| P6 | each arm agrees with at least one of the other two |

The differential prints `3000 problems: checksum 318282619, 54000 checks
over 3 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, three or four to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Most kill by stopping the run: an
operand order or operator swapped makes some later division divide by
zero, which the generator ruled out only for the right tree, and Kāra
stops with `runtime error: division by zero` at the mutated arm's
division (exit 101), or with `integer overflow` at its multiplication.

| # | mutation | killed by |
|---|---|---|
| M1 | ★: `Subtract` takes right minus left | division by zero |
| M2 | ★: the builder pops the left operand first | division by zero |
| M3 | ★: `*` builds an `Add` | division by zero |
| M4 | ★: `Multiply` takes the right operand's absolute value | P1 130, P6 130 |
| M5 | enum: `-` builds its operands the other way round | division by zero |
| M6 | enum: `Multiply` adds | division by zero |
| M7 | arena: `-` takes right minus left | division by zero |
| M8 | arena: `*` squares its left operand | integer overflow |
| M9 | arena: the builder pops the left operand first | division by zero |
| M10 | arena: the value read off the first node, not the root | P1 2595, P4 2851, P5 2851, P6 2595 |

## Benchmarks

The bench draws 20000 random postfix expressions of 50 operands up to
`10^5`, all of them first, then builds each into a tree and evaluates it
by the ★ arm in all five languages: Rust with `Box<dyn Node>`, Go with
an interface, C with a pointer to a table of methods in each heap node,
as a trait object is. Every implementation prints `20000 expressions of
50 operands: values sum to 145832590487, checksum 63745765`. The C build
also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `21cdf88b69` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.245 s |
| C (`clang -O3`) | 0.255 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.257 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.328 s |
| Kāra (`karac build`) | 0.335 s |
| Go | 0.344 s |
| Python | 1.6 s |

The sequential Kāra build takes 1.34x Rust's time and 1.28x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md).
The time includes drawing the expressions, a recursive generator
building 2 million token strings, which every language does the same
way; how it splits between that and the trees was not measured.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.292 s and 0.343 s on one
run).

## Verification

All three arms print the same output as `expression.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`21cdf88b69`.

## Writing it

The first drafts took four edits from `karac fix`:

- The ★ arm's `token.parse::[i64]()`, a turbofish with Kāra's brackets,
  is refused with a pointer to `i64.parse(token)`, which the fix
  writes.
- `operator(token: Str, left: dyn Node, right: dyn Node)` moves both
  operands into the struct it builds, and the fix marks them
  `own dyn Node`.
- The harness's `["+", "-", "*", "/"][k]` takes a `String` out of a list
  by index, and the fix adds `.clone()`.
- The arena arm's `token.as_bytes()[0]` is Rust's spelling; the fix
  renames it `token.bytes()[0]`.

Each arm then checked clean and agreed with the mirror. The trait arm's
`dyn Node` fields, its `Vec[dyn Node]` stack, and the coercion of each
operator struct into the `dyn Node` return of `operator` all worked as
first written, as did the `shared enum` arm's recursion. No compiler gap
was met.
