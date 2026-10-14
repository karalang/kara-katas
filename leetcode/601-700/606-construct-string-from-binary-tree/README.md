# 606. Construct String from Binary Tree

Given the root of a binary tree, return a string of its values in
preorder, each child in parentheses after its parent's value. Leave out
every empty pair of parentheses that the tree can be read back without:
a missing child writes nothing, except a missing left child beside a
right one, which writes `()` so that the right child is not read as the
left.

```
[1, 2, 3, 4]           ->  1(2(4))(3)
[1, 2, 3, null, 4]     ->  1(2()(4))(3)
```

**Constraints:** 1 to 10^4 nodes, each value from -1,000 to 1,000.

## Approaches

Every arm is `fn tree2str(root: Option[TreeNode]) -> String` over
LeetCode's tree, a `shared struct TreeNode` with a value and two
optional children.

| file | mechanism |
|---|---|
| `tree2str.kara` ★ | preorder recursion appending to one `String`: the value, the left child in parentheses when there is any child, the right child in parentheses when there is one; O(n) |
| `tree2str_concat.kara` | each node's string built from its children's and joined by an f-string, so each level copies the strings below it again; O(n * h) |
| `tree2str_stack.kara` | preorder on a stack of nodes with a flag, opening a node's parenthesis the first time it is popped and closing it the second, with the whole string's extra outer pair taken off at the end; O(n) |
| `tree2str_trim.kara` | every node first written as `value(left)(right)`, an empty child as `()`, then read backwards keeping a `()` only when the next character kept is an opening one; O(n) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 14 lines: the two examples above; seven more
(one node, a lone left child, a lone right child, chains down the right
and the left, negative values, and the problem's extremes); a total
length and checksum over 300 random trees of 1 to 80 nodes; and the
length and checksum of four trees of 10,000 nodes, the problem's most:
one at random, chains down the left and the right, and a complete tree.
`tree2str.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: the tree written with every child in
parentheses, an empty one as `()`, and then every empty pair left out
that can be, tried from the right until none can, where a pair can be
left out when the string still reads back as the same tree. Reading back
is a small parser of the problem's form, which takes a missing group or
an empty one as no child. Each of 1,000 random cases is a tree of 1 to
30 nodes leaning left with chance 20, 50 or 80 in 100, with values up to
9 or up to 1,000 either way.

| | property |
|---|---|
| P1 | the string is the definition's |
| P2 | read back, it stands for the tree |
| P3 | the numbers in it, in order, are the tree's values in preorder |
| P4 | under a new root as its left child, the tree's string is wrapped in one pair after the root's value |
| P5 | as the right child, it follows an empty pair |

It prints `1000 cases (15686 nodes), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no empty pair for a missing left child | P1 729, P2 729, P5 1000 |
| M2 | ★: a pair for the left child of every node | P1 1000 |
| M3 | concat: the two children swapped | P1 933, P2 933, P3 896, P5 1000 |
| M4 | concat: an empty pair after a lone left child | P1 724, P4 1000 |
| M5 | stack: an empty pair for every missing left child | P1 1000 |
| M6 | stack: the outer closing parenthesis kept | P1 1000 |
| M7 | trim: an empty pair dropped only at the very end | P1 961, P4 97, P5 97 |
| M8 | trim: every empty pair dropped | P1 729, P2 729, P5 1000 |
| E1 | ★: the test for a pair written as a negation | 0 |
| E2 | concat: the left child tested by its string | 0 |
| E3 | stack: the opening parenthesis pushed as a string | 0 |
| E4 | trim: the backward walk stopped by `> 0` | 0 |

Two pairs of mutants make the same mistake in different arms and fail
the same cases. M1 and M8 drop the `()` before a right child, so the
right child reads back as a left one (P2), and P5, which always puts the
tree under a missing left child, sees them on every case. M2 and
M5 write `()` after every leaf, which only P1 can see: the parser takes
an empty pair as no child, the numbers are unchanged, and the wrapping
of P4 and P5 carries the extra pairs through. M6's extra parenthesis at
the very end is invisible to every property but P1 for the same reasons.
M3 is the only mutant P3 sees, since it alone changes the order of the
values; P4 misses it because a lone left child does not take the swapped
branch. M4 puts its extra pair after the lone left child that P4 always
makes, so P4 sees it on every case. M7 drops only the empty pairs at the
very end of the string and keeps the rest, which the parser and the
numbers read the same way, and which the wrapping of P4 and P5 changes
on only 97 cases. E2 is safe because a child's string is empty only when
there is no child, every value writing at least one digit.

## Verification

Every arm prints the same output as `tree2str.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes every arm, the differential and the bench program. All at kara
`8579c4f0d7`.

The frozen legacy backends do not get through. Under `karac run
--interp` the stack arm prints the same output, and the other three
print the same first lines and run past 60 seconds on the trees of
10,000 nodes. `karac run` and `karac build` stop every arm at module
verification on the harness's `show` call ("Call parameter type does not
match function signature"). `karac run --interp` and `karac build`
refuse the differential at type checking: legacy types the elements of
`shorter.iter()` as `char`, so the `*c` that reads one is an error.
`karac build` refuses the bench program in codegen, which does not lower
its `for (i, c) in s.chars().enumerate()`. Legacy is frozen, so these
are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 random trees of
10,000 nodes, each new node walking down from the root and going left
with chance 50 to 88 in 100, once, keeping the nodes in the order they
were added; then 200 times over writes out every tree's subtree at one
of its first 16 nodes, picked by the round and the tree, adding up the
lengths and putting every 101st character into a checksum. Every
implementation prints `20 trees, 200 times each: 61492825 characters,
checksum 478357407`, the Kāra program under `karac __mir-run` included
(224 s).

Each implementation appends to one growing string, as the ★ arm does: a
`String` in Rust, a `strings.Builder` in Go, a buffer that doubles in C,
and in Python a list of parts joined at the end. Rust and Go format each
value into a string of its own before appending it, as the arm's
`f"{node.val}"` does; C formats it into a buffer on the stack. The Rust
tree is LeetCode's `Option<Rc<RefCell<TreeNode>>>`. Spot timings on a
shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.89 to 1.10 s |
| Rust (`rustc -O`) | 0.95 to 1.12 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.16 to 1.29 s |
| Go | 0.99 to 1.04 s |
| Python | 7.06 to 7.10 s |
| Kāra (`karac build --mir`) | 1.97 to 2.33 s |

So `bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` does not build it;
that edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 12.1 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

The Kāra row is about twice Rust's, Go's and C's, which are level with
each other. In callgrind profiles at 20 rounds, the v2 program runs
1.52 billion instructions to Rust's 0.69 billion, and valgrind counts
3.47 million heap allocations in the writing to Rust's 1.16 million, the
difference between runs at 0 and at 20 rounds: about three a node where
Rust's `to_string` makes one. `malloc` and `free` alone take
0.46 billion of the v2 program's instructions. That the formatting of
each value is where the extra allocations come from is read from the
profile, where `karac_mir_fmt_i64` and `karac_mir_fmt_end_string` take
0.12 billion instructions between them; it is not measured by changing
the program.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
