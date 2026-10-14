# 637. Average of Levels in Binary Tree

Given the root of a binary tree, return the average value of the nodes
on each level, top level first. Answers within 10^-5 of the actual
answer are accepted.

```
root = [3,9,20,null,null,15,7]  ->  [3.00000, 14.50000, 11.00000]
root = [3,9,20,15,7]            ->  [3.00000, 14.50000, 11.00000]
```

**Constraints:** 1 to 10^4 nodes; every value from -2^31 to 2^31 - 1.

## Approaches

Every arm is `fn average_of_levels(root: Option[TreeNode]) -> Vec[f64]`
over a `shared struct TreeNode`. Each adds a level's values up as an
`i64`, which cannot overflow, since 10^4 values of at most 2^31 in size
sum to less than 2^45, and divides once, so every arm computes each
average as the same `f64` division and their outputs agree exactly.

| file | mechanism |
|---|---|
| `average_of_levels.kara` ★ | breadth first with a `VecDeque`: the queue's length at the start of a level is the level's size, and taking that many off the front while adding their children to the back leaves the next level; O(nodes) time, O(widest level) space |
| `average_of_levels_depths.kara` | a recursive depth-first walk carrying the depth, adding each value to that depth's sum and count and growing the two lists on reaching a new depth; O(nodes) time, O(height) stack |
| `average_of_levels_stack.kara` | the same sums and counts with an explicit stack of (node, depth) pairs instead of recursion; O(nodes) |
| `average_of_levels_frontier.kara` | the current level as a `Vec` of nodes, replaced by the `Vec` of their children in order once it is averaged; O(nodes) time, O(two widest levels) space |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 10 lines: the two LeetCode examples; six more
(one node; a chain down the left; a level averaging to -0.5; levels
holding the largest and smallest values, together and alone; and an
empty tree, which has no levels); the number of levels and the sum of
the averages over 300 random trees of 1 to 40 nodes; and the same over a
tree of 10,000 nodes with values over the whole range, with its lowest
average. Averages print to five places. `average_of_levels.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every node's value listed with its path from the root, one letter a
step, and each level averaged over the nodes whose paths have the same
length. Each of 1,000 cases makes a tree of 0 to 30 nodes with values
from -100 to 100, each new node walking down from the root, left with a
chance from 10 to 90 in 100, to the first empty place, so the shapes run
from chains to bushy trees.

| | property |
|---|---|
| P1 | the averages are the definition's, exactly |
| P2 | there is one average a level |
| P3 | the mirror image has the same averages |
| P4 | adding a number from -10 to 10 to every value adds it to every average, to within 10^-9 |
| P5 | two copies of the tree under a new root average to the root's value and then the tree's averages |

It prints `1000 cases (5886 levels), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac
__mir-llvm-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a left child put at the front of the queue | P1 752, P2 593, P3 840, P5 920 |
| M2 | ★: the sum replaced by each value, not added to | P1 878, P3 877, P4 820, P5 964 |
| M3 | depths: a left child counted at its parent's depth | P1 920, P2 691, P3 944, P5 963 |
| M4 | depths: a level's count set to 1, not added to | P1 878, P4 820, P5 964 |
| M5 | stack: a right child pushed two levels down | P1 910, P2 805, P3 944, P5 964 |
| M6 | stack: each node counted twice | P1 964, P4 901, P5 998 |
| M7 | frontier: a level divided by the next level's size | P1 964, P3 8, P4 821, P5 998 |
| M8 | frontier: the values added without their signs | P1 941, P4 881, P5 481 |
| E1 | ★: twice the sum over twice the count | 0 |
| E2 | depths: the lists grown while too short, not when one short | 0 |
| E3 | stack: the lists grown only when one short | 0 |
| E4 | frontier: the next level copied, not moved | 0 |

P1 kills all eight. P2 sees the three that put a node on the wrong
level, M1, M3 and M5, which can change how many levels there are.
P3 sees those three and M2, whose answer is each level's last value and
so depends on the order within a level; it also sees M7 in 8 cases,
where the deepest level is divided by an empty next level and a sum of
0 gives NaN, which is not equal to itself. P4 misses M1, M3 and
M5, because adding a number to every value adds it to the average of any
group of values, however wrongly grouped. P5 sees all eight. The four
survivors cannot change an answer: doubling both the sum and the count
is exact in floating point and leaves the quotient alone; a recursive
walk goes at most one level deeper than any it has reached, and so does
a preorder walk with a stack, since a node's parent is always visited
first, which makes growing the lists while short and growing them when
one short the same; and copying a `Vec` of `shared` nodes copies only
the handles.

## Verification

Every arm prints the same output as `average_of_levels.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes every arm, the
differential and the bench program. All at kara `ea2a2da2be` for the
debug build and `0bebe7947a` for the release build that runs `check` and
`__mir-run`.

The frozen legacy backends refuse every file at type checking. They
still hold the old rule that an argument which is already a `mut ref`,
as `seed` is inside the harness's `random_value`, drops its call-site
`mut` marker, and they type the items of a `Vec`'s `iter()` by value, so
`*a` and `*val` are errors. Legacy is frozen, so these are noted, not
filed.

## Benchmarks

The bench program uses the ★ arm. It makes 10 random trees of
10,000 nodes, the problem's most, with values over the whole range,
once; then 4,000 rounds each average the levels of one of them, picked
by the round, counting the levels and adding up the averages. Every
implementation prints `10 trees of 10000 nodes, 4000 rounds:
68000 levels, sum of averages -68822219969222.977`, the Kāra program
under `karac __mir-run` included (in 126 s).

Each implementation walks the trees breadth first, one level at a time:
Rust with `VecDeque` over LeetCode's `Option<Rc<RefCell<TreeNode>>>`, C
with a ring buffer of node pointers that grows by doubling, Go with a
slice taken from the front, and Python with `collections.deque` over a
class with `__slots__`. Spot timings on a shared 4-core container, three
runs each (two for Python; `bench.sh` timings need a quiet machine),
each including making the trees:

| | time |
|---|---|
| C (`clang -O3`) | 0.51 to 0.56 s |
| Rust (`rustc -O`) | 0.48 to 0.50 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.44 to 0.49 s |
| Go | 1.20 to 1.25 s |
| Python | 4.97 to 5.02 s |
| Kāra (`karac build --mir`) | 1.06 to 1.12 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program as above; that edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside the kata that drops the
forwarded `mut` markers and the `*` builds under legacy and takes
4.87 to 4.98 s, so the v2 build takes under a quarter of legacy's time.
Under `karac __mir-llvm-run` the program prints the same line in 4.8 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

The Kāra build takes about twice as long as C and Rust and a little less
than Go. In the built binary, every `push_back` and `pop_front` on the
`VecDeque` is a call into the runtime (`karac_mir_deque_push`,
`karac_mir_deque_pop`), so each node visited costs at least two calls,
where Rust's `VecDeque` is inlined; that this is the gap is inferred
from the disassembly, not profiled. It is not filed: the comparison with
Rust and C waits until after M4.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
