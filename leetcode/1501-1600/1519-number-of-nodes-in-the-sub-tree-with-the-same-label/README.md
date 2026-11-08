# 1519. Number of Nodes in the Sub-Tree With the Same Label

You are given a tree (a connected, undirected graph with no cycles) of `n`
nodes numbered from `0` to `n - 1` and exactly `n - 1` edges. The root of
the tree is node `0`, and each node has a label, a lower-case letter given
in the string `labels` (node `i` has the label `labels[i]`). The `edges`
array is given as `edges[i] = [ai, bi]`, an edge between `ai` and `bi`.

Return an array of size `n` where `ans[i]` is the number of nodes in the
subtree of the `i`th node which have the same label as node `i`. A subtree
of a tree `T` is the tree made of a node in `T` and all its descendant
nodes.

```
n = 7, edges = [[0,1],[0,2],[1,4],[1,5],[2,3],[2,6]], labels = "abaedcd"  ->  [2,1,1,1,1,1,1]
n = 4, edges = [[0,1],[1,2],[0,3]], labels = "bbbb"                        ->  [4,2,1,1]
n = 5, edges = [[0,1],[0,2],[1,3],[0,4]], labels = "aabab"                 ->  [3,2,1,1,1]
```

**Constraints:** `1 <= n <= 10^5`; `edges.length == n - 1`;
`0 <= ai, bi < n`, `ai != bi`; `labels.length == n`; `labels` is lower-case
English letters.

## Approaches

| file | mechanism |
|---|---|
| `labels.kara` ★ | a depth-first walk from node 0 returns each subtree's count of every letter, the children's summed into the parent's; a node's answer is its own letter's count. O(26 n) |
| `labels_stack.kara` | no recursion: an explicit stack gives a preorder with parents, and walking it backwards adds each node's counts into its parent's. O(26 n) |
| `labels_euler.kara` | an Euler tour: a subtree is a contiguous run of entry times, so a node's answer is how many of its letter entered between its entry and its exit; one count per letter, read at entry and again at exit. O(n) |
| `labels_iter.kara` | the ★ arm with iterator adapters: adjacency lists built by `fold`, the children's counts summed by `filter`, `map` and `fold`. Ran wrong until B-2026-11-08-36 was fixed: see Writing it |
| `labels_solution.kara` | LeetCode's Rust template (`Vec<Vec<i32>>` edges, a nested `fn dfs` returning `[i32; 26]`, `usize::MAX` for no parent), carried by `karac fix`. Does not check (B-2026-11-08-57): see Rust template |
| `differential.kara` | the four arms that run against the statement read literally, six properties |

Every arm that runs prints the same 6 lines: LeetCode's three examples
and a one-node tree, then a checksum of the answers for 2000 trees of 1
to 12 nodes over 3 letters and 20 of 1 to 20000 nodes over 26. Node `i`
hangs under a random earlier node, each edge is written either way round,
and the edges are shuffled. `labels.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: node 0's parent links found by sweeping the edges until
nothing changes, then every node counted once for each node on its path to
node 0 that has its letter. It checks 2000 trees of 1 to 10 nodes over 3
letters, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the letters renamed (a to b, b to c, c to a) leave the answer |
| P3 | every edge turned round and the edges listed backwards leave the answer |
| P4 | node 0's answer is how often its letter appears in the whole tree |
| P5 | with every node labelled `a`, the answers are the subtree sizes, which add up to the sum over nodes of (depth + 1) |
| P6 | each arm agrees with at least two of the other three |

The differential prints `2000 problems: checksum 93640531, 48000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Fifteen edits to the differential, three or four to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run`. Twelve are killed,
each the same way under both backends where both finish; three survive.
M1 to M9 were run when the differential held three arms (P6 then asked
each arm to agree with both others); M10 to M12 with all four.

| # | mutation | killed by |
|---|---|---|
| M1 | ★: each edge added one way only | P1 1586, P3 1794, P4 1138, P5 1586, P6 4758 |
| M2 | ★: a child skipped when it is the node itself, not the parent | stack overflow (walks back up forever) |
| M3 | ★: the answer read before the node counts itself | P1, P4, P5 2000 each, P6 6000 |
| M4 | stack: a node not marked seen when pushed | the interpreter runs out of memory; compiled, exit 101 |
| M5 | stack: the preorder walked forwards | P1 1569, P4 1438, P5 1794, P6 4707 |
| M6 | stack: node 0's counts never passed up (`up > 0`) | P1 1438, P4 1438, P5 1794, P6 4314 |
| M7 | stack: a child's counts replace the parent's | P1 1157, P3 1046, P4 1059, P5 1453, P6 3471 |
| M8 | Euler: the count read after the node's own entry | P1, P4, P5 2000 each, P6 6000 |
| M9 | Euler: the count reset at exit | P1 614, P4 483, P5 1439, P6 1842 |
| M10 | iter: each edge added one way only | P1 1586, P3 1794, P4 1138, P5 1586, P6 1586 |
| M11 | iter: a child's counts dropped in the sum (`a` for `a + b`) | P1 1569, P4 1438, P5 1794, P6 1569 |
| M12 | iter: the answer read before the node counts itself | P1, P4, P5, P6 2000 each |

Two survivors are equivalent: the Euler arm starting every letter's count
at 1 (an offset that cancels in exit less entry) and never descending
into node 0 (node 0 is only ever a node's parent). The third is a blind
spot of this differential: the ★ arm adding only the first 25 letters'
counts up the tree. The differential's trees use three letters, so `z`
never appears; the harness's 26-letter tier does catch it.

## Rust template

LeetCode's Rust template nests `fn dfs(u: usize, p: usize, adj:
&Vec<Vec<usize>>, labels: &[u8], ans: &mut Vec<i32>) -> [i32; 26]` inside
the method and starts it with `dfs(0, usize::MAX, &adj, labels, &mut
ans)`. `karac fix` made 29, 2, 5 and 6 edits over four passes: it lifted
`dfs` out of the method, turned `&Vec<..>` into `ref Vec[..]`, `vec![]`
into `Vec.filled`, and `usize` into `i64` in `dfs`'s parameters and in
`let n = n as i64`. Six errors were left. Its callers still pushed
`e[1] as usize` into the lists and passed `usize.MAX`, which no longer
matched `dfs`'s rewritten `i64` parameters (B-2026-11-08-49); and `[0; 26]`
and `Vec.filled(n, 0)` stayed `i64` where `Array[i32, 26]` and `Vec[i32]`
are wanted.

B-2026-11-08-49 is fixed (kara `0600aebf3`): run again from the `usize`
spelling, `karac fix` writes `e[1] as i64` in the pushes and `i64.MAX` for
the missing parent. Four errors are left, all the collection literals'
type: `cnt[c] += 1; ans[u] = cnt[c]; cnt` with `let mut cnt = [0; 26]` in a
function returning `Array[i32, 26]`, and `let mut ans = Vec.filled(n, 0)`
handed to `ans: mut ref Vec[i32]`. That is B-2026-11-08-57; the message
names the binding annotation but carries no fix. With
`let mut cnt: Array[i32, 26]` and `let mut ans: Vec[i32]` written by hand,
the arm checks and prints the other arms' output.

## Benchmarks

The bench builds a random tree of 200000 nodes over 26 letters once and
answers it 5 times by the ★ arm in all five languages; each answer builds
its adjacency lists afresh, as the signature asks, and every walk returns
a fresh 26-count list (`calloc` and `free` in C). Every implementation
prints `5 passes over a tree of 200000 nodes: checksum 980281928`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `fd68cca28` on LLVM 22:

| | median |
|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.205 s |
| C (`clang -O3`) | 0.213 s |
| Kāra (`karac build`) | 0.219 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.232 s |
| Rust (`rustc -O`) | 0.235 s |
| Go | 0.360 s |
| Python | 1.65 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.349 s and 0.361 s on one run).

Kāra is 0.88x Rust under overflow checks by median; the runs spread by a
third or more in every compiled language, so the order of the first five
is not settled. Not traced.

## Verification

The four running arms print the same output as `labels.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them.
Under `karac __mir-run` the arms take 1.0 to 2.4 s and the differential
5.6 s.

## Writing it

The ★, stack and Euler arms were written in Kāra and `karac fix` had
nothing to change. The differential's letter renaming wrote
`(c as u8) + 1`, which is refused (`char` to `u8` would truncate) with a
help line but no fix; it is written `c as u32 as u8`, as the help says.

The iterator arm's adjacency fold was written `|mut lists:
Vec[Vec[i64]], (a, b)|`, which is a parse error naming Rust syntax.
`karac fix` rewrote it to a rebinding `let mut lists = lists;`, which is
refused again (a bare parameter borrows), and a second pass made the
parameter `own`. It then checks. But the counting fold, `.fold(
Vec.filled(26, 0), |total: Vec[i64], below: Vec[i64]| ..)`, checks and
fails on both backends: the interpreter stops with `deref of non-reference
Box` in the closure, `karac __mir-llvm-run` exits 101 with no message,
and `karac run` ends on a segmentation fault. That was B-2026-11-08-36:
the typechecker recorded the fold's slot type for the closure, turning
its borrowed parameters owned, while MIR built the body with borrowed
ones. Fixed in kara `1740abdd1`; the file, as `karac fix` left it, now
prints the same output as the other arms on every lane and joins the
differential.
