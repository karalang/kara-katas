# 652. Find Duplicate Subtrees

Given the root of a binary tree, return every duplicate subtree: for
each kind of subtree that appears two or more times, the root node of
any one of them. Two subtrees are duplicates when they have the same
structure and the same node values. The answer may be in any order.

```
root = [1,2,3,4,null,2,4,null,null,4]  ->  [[2,4],[4]]
root = [2,1,1]                          ->  [[1]]
root = [2,2,2,3,null,3,null]            ->  [[2,3],[3]]
```

**Constraints:** 1 to 5,000 nodes (about 2,000 in the LeetCode
statement's tests); values from -200 to 200.

## Approaches

Every arm is `fn find_duplicate_subtrees(root: Option[TreeNode]) ->
Vec[TreeNode]` over a `shared struct TreeNode`. The harness writes each
subtree found in preorder, `#` for an empty child, and sorts the texts,
so the order the arms find them in does not matter.

| file | mechanism |
|---|---|
| `find_duplicate_subtrees.kara` ★ | children first, each subtree numbered by a `Map` from its value and its children's numbers to a number; a number's subtree kept when its count reaches 2; O(nodes) |
| `find_duplicate_subtrees_strings.kara` | each subtree written as a `String` from its children's, counted in a `Map` through `entry(...).or_insert(0)`; O(nodes^2) in the worst case |
| `find_duplicate_subtrees_pairwise.kara` | the nodes listed in preorder and every pair compared node by node; a node kept when a later one matches and no earlier one does; O(nodes^2) comparisons |
| `find_duplicate_subtrees_hashed.kara` | a hash of each subtree from its children's, and a `Map` from hash to one example of each kind met and its count, through `entry(...).or_insert(Vec.new())`; a subtree compared node by node only with its hash's examples |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 11 lines: the three LeetCode examples; five
more trees (one node; a full tree of seven equal values; the same values
in mirrored shapes, which share only their leaves; a chain down the left
of one value, which has no duplicates; and the smallest and largest
values), each with its duplicates written out; the kinds and a checksum
of the texts over 300 random trees of 1 to 40 nodes of values 0 to
2; and two large trees, 1,500 nodes of values 0 and 1 and 2,000 over the
whole range. The pairwise arm takes 21 s under `karac __mir-run` on
these. `find_duplicate_subtrees.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which shares no step with them: every subtree written out in preorder,
the texts sorted, and each text met twice or more one kind of duplicate.
Each of 1,000 random trees has 1 to 30 nodes of 1 to 4 values, built
leaning left with chance 20, 50 or 80 in 100.

| | property |
|---|---|
| P1 | the kinds found are the definition's |
| P2 | each subtree found is met at least twice in the tree, and no two found are the same |
| P3 | the mirrored tree has as many kinds |
| P4 | two copies of the tree under a new root have one kind for every distinct subtree of the tree |
| P5 | the children of a subtree found are found too |

It prints `1000 trees (15361 nodes), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the empty tree numbered like the first shape | P1 656, P2 440, P3 228, P4 814, P5 380 |
| M2 | ★: a shape kept every time after its first | P1 654, P2 654, P4 822 |
| M3 | strings: the right child left out of the string | P1 697, P2 686, P3 652, P4 767, P5 552 |
| M4 | strings: a string kept at its third time | P1 620, P4 1000 |
| M5 | pairwise: the node just before not looked at | P1 181, P2 181, P3 285, P4 245 |
| M6 | pairwise: the values not compared | P1 573, P2 524, P4 622, P5 247 |
| M7 | hashed: the count tested for 1, which it has passed, so nothing kept | P1 822, P4 1000 |
| M8 | hashed: a new kind counted from 0 | P1 620, P4 1000 |
| E1 | ★: the empty tree numbered -1 | 0 |
| E2 | strings: an empty child written `x` | 0 |
| E3 | pairwise: the pair compared the other way round | 0 |
| E4 | hashed: the empty tree hashed to 0 | 0 |

P1 and P4 kill all eight. P2 sees the five that report a subtree met
once or a kind twice, and misses M4, M7 and M8, which only report too
few. P3 sees only M1, M3 and M5, which confuse shapes or kinds in a way
a mirror image changes; the others miscount the mirrored tree exactly as
they miscount the tree. P5 sees M1, M3 and M6, which make subtrees the
same that are not, so a parent is found without its children. The four
survivors cannot change an answer: the empty tree's number only has to
differ from every real number, and -1 does as 0 does; `x` writes an
empty child as unambiguously as `#`; the node-by-node comparison is
symmetric; and a hash only picks the bucket, so changing the empty
tree's hash changes which subtrees share a bucket but not which are
found the same.

## Verification

Every arm prints the same output as `find_duplicate_subtrees.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` for the debug build and `abbdbaf131` for the release build
that runs `check` and `__mir-run`, with runtime archives newer than the
last `runtime/src` change.

The frozen legacy backends refuse every arm and the differential at type
checking: the harness hands `seed`, already a `mut ref` parameter, on
with the `mut` marker design.md asks for, which legacy rejects; the ★
arm reads `*i` from `Map.get`, and the differential `*t` from `iter()`
over a `Vec[String]`, both typed by value under legacy. Legacy is
frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes four trees of 100,000 nodes
once, with 2, 3, 5 and 401 values, each node placed by walking down from
the root with even chances; then 40 rounds each find the duplicates of
one tree, picked by the round, adding up the kinds and putting the found
roots' values into a checksum. Every implementation prints `4 trees,
40 rounds: 78690 kinds, checksum 917118823`, the Kāra program under
`karac __mir-run` included (in 31 s).

The map from (value, left number, right number) to a number is Kāra's
`Map`, Rust's `HashMap` (both SipHash), Go's
`map[[3]int64]int64`, Python's `dict`, and in C an open-addressing table
sized for the tree and made for each call, with a multiply-xor hash.
Kāra's nodes are a `shared struct`, Rust's `Rc<RefCell<TreeNode>>`, and
C's and Go's plain pointers. Spot timings on a shared 4-core container,
three runs each (two for Python; `bench.sh` timings need a quiet
machine), each including making the trees:

| | time |
|---|---|
| C (`clang -O3`) | 0.25 to 0.27 s |
| Rust (`rustc -O`) | 0.99 to 1.05 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.95 to 1.03 s |
| Go | 0.68 to 0.89 s |
| Python | 3.79 to 4.77 s |
| Kāra (`karac build --mir`) | 0.87 to 0.93 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program for the `*i` and the `mut` markers above. That edit is by hand,
on top of the `scripts/new-bench.sh` output. A copy outside the kata
with `i` for `*i` and no forwarded markers builds under legacy and takes
0.97 to 1.02 s. Under `karac __mir-llvm-run` the program prints the same
line in 5.5 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

So the v2 build is level with legacy and slightly ahead of Rust, whose
`HashMap` uses the same SipHash and whose `Rc<RefCell>` nodes pay a
borrow flag check on each visit. C is three and a half times faster for
its cheaper hash, a table it never grows, and plain pointers. The
comparison with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The legacy refusals
above are not filed because legacy is frozen.
