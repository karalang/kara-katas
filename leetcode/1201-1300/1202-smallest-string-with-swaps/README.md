# 1202. Smallest String With Swaps

You are given a string `s`, and an array of pairs of indices in the
string `pairs` where `pairs[i] = [a, b]` indicates 2 indices (0-indexed)
of the string. You can swap the characters at any pair of indices in the
given `pairs` any number of times. Return the lexicographically smallest
string that `s` can be changed to after using the swaps.

```
s = "dcab", pairs = [[0,3],[1,2]]          ->  "bacd"
s = "dcab", pairs = [[0,3],[1,2],[0,2]]    ->  "abcd"
s = "cba",  pairs = [[0,1],[1,2]]          ->  "abc"
```

**Constraints:** `1 <= s.length <= 10^5`; `0 <= pairs.length <= 10^5`;
`0 <= pairs[i][0], pairs[i][1] < s.length`; `s` only contains lower
case English letters.

The arms are `fn smallest_string_with_swaps(s: String, pairs:
Vec[Vec[i64]]) -> String`. The two Rust arms keep the method LeetCode
gives Rust users, on `Vec<Vec<i32>>`, inside `impl Solution`, and a
one-line `smallest_string_with_swaps` calls it.

## Approaches

The pairs join the indices into groups, the connected parts of the graph
whose edges are the pairs. Swaps along a group's edges reach every order
of its letters, and no swap moves a letter out of its group, so the
answer gives each group its letters in rising order, at its indices in
rising order.

| file | mechanism |
|---|---|
| `smallest_string_with_swaps.kara` ★ | a union-find over the indices (path halving, union by size); the indices gathered by root, in rising order, each group's letters sorted and laid back on them. O((n + m) α(n) + n log n) |
| `smallest_string_with_swaps_dfs.kara` | the pairs as an undirected graph in adjacency lists, each group found by a depth-first search on an explicit stack; the group's indices sorted, its letters sorted, and the one laid on the other |
| `smallest_string_with_swaps_bfs.kara` | each group found by a breadth-first search over a `VecDeque` and numbered; its letters counted into 26 buckets, and each index, in order, handed the least letter its group has left. O(n + m + 26 · groups) |
| `smallest_string_with_swaps_rank.kara` | the union-find as plain recursion (`find` compresses the whole path on the way back); the indices sorted once by (root, letter) and once by (root, index), and the `k`-th of a group in the first order the letter for the `k`-th in the second |
| `smallest_string_with_swaps_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `DSU` struct with a recursive `find(&mut self, x: usize)`, the groups in a `HashMap<usize, Vec<usize>>`, the answer built in a `Vec<u8>` from `s.as_bytes()`), carried to Kāra by `karac fix` |
| `smallest_string_with_swaps_heap.kara` | another Rust solution (a nested iterative `fn find` over a `Vec<usize>`, each root's letters in a `BinaryHeap<Reverse<char>>` filled through `entry(r).or_default()`, and each index, in order, given the least letter its root's heap still holds), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six more properties |

Every arm prints the same 11 lines: LeetCode's three examples; no pairs
(`zyx`); a pair of one index with itself (`q`); two cases with repeated
and self pairs (`udyyek` to `deykuy`, `pwqlmqm` to `lpqqmwm`); one pair
given twice, both ways round (`abcd`); 1000 random strings of up to 12
letters from the first five with up to 8 pairs (`1000 random strings:
583 changed, checksum 254473058`); and two at the constraints' top,
100000 random letters with 100000 random pairs (`digest 698942582,
starts hpalaqaaaaaa`), and with each index joined to the one two on, two
groups by parity (`digest 653480645, starts aaaaaaaaaaaa`).
`smallest_string_with_swaps.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, dfs, bfs and rank arms check clean as written. The
solution arm takes one round of 51 fixes (among them the `use` line
dropped, `DSU` renamed `Dsu`, `&mut self` to `mut ref self`, `usize` to
`i64` and the `as usize` casts on `p[0]` and `p[1]` dropped as widening,
`vec![]` to `Vec.new()`, `vec![0u8; n]` to `Vec.filled(n, 0u8)`,
`s.as_bytes()` to `s.bytes()`, and the `&i` patterns to `i`). The heap arm
takes one round of 57 (among them `use std::cmp::Reverse` to `import
std.cmp.Reverse`, the nested `fn find` moved to the top level with `mut
x: usize` to a `let mut x = x;`, `HashMap<usize,
BinaryHeap<Reverse<char>>>` to `Map[i64, PriorityQueue[Reverse[char]]]`,
`Reverse(c)` to `Reverse { value: c }` in both the push and the `let`,
and `entry(r).or_default()` to `entry(r).or_insert(PriorityQueue.max_first())`).
Both outputs match.

## Gaps

One, fixed. Before kara 275ab3ae7f, `karac fix` wrote the heap arm's
`entry(r).or_default()` as `or_insert(PriorityQueue.new())`. Kāra's
`PriorityQueue.new()` pops the smallest first and Rust's `BinaryHeap` the
largest, which is why every other `BinaryHeap` constructor becomes
`PriorityQueue.max_first()`; the fixed arm checked clean, ran, and gave
`dcab` for LeetCode's first example, every group's letters handed out
largest first, as `Reverse` over a smallest-first queue is largest-first.
The fix now reads the heap's kind from the map's declaration while the
source still names `BinaryHeap`, and writes `max_first()`, or `new()` for
a heap of `Reverse` items in a program whose fix drops `Reverse`. kara
B-2026-11-18-46.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a breadth-first search from `s` over every string the pairs'
swaps reach, and the least of them. 2000 random cases: 1 to 7 letters
from the first 2, 3 or 5, and 0 to 6 random pairs.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the same letters as `s`, and no greater than `s` |
| P3 | the pairs, each turned round and in reverse order, give the same |
| P4 | the answer, given again with the same pairs, comes back unchanged |
| P5 | the last pair left out gives an answer as small or greater |
| P6 | every letter of `s` one later gives every letter of the answer one later |
| P7 | the ★ arm's answer |

All 84,000 checks pass on every arm: `2000 cases: checksum 941053790,
84000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. A Python reading of
the same cases, searching the reachable strings, gives the same checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a group's letters never sorted | P1 792, P7 3960 |
| S2 | ★: a pair's second index never joined | P1 792, P7 3960 |
| D1 | dfs: a group's indices never sorted | P1 361, P2 77, P3 280, P5 106, P7 361 |
| D2 | dfs: each pair an edge one way only | P1 429, P3 628, P5 8, P7 429 |
| B1 | bfs: a letter handed out never used up | P1 1144, P2 1144, P7 1144 |
| B2 | bfs: a neighbour never queued | P1 295, P5 27, P7 295 |
| R1 | rank: the letters ordered by index | P1 792, P7 792 |
| R2 | rank: a pair joined at its index, not its root | P1 131, P3 222, P5 34, P7 131 |
| X1 | solution: a group's letters never sorted | P1 792, P7 792 |
| X2 | solution: a union joined at the index, not its root | P1 131, P3 222, P5 34, P7 131 |
| H1 | heap: each heap smallest-first, as `karac fix` wrote it | P1 1144, P2 823, P5 283, P7 1144 |
| H2 | heap: no pair ever joined | P1 792, P7 792 |

A mutation of the ★ arm fails P7 on all six arms, the ★ arm against the
other five. S1, S2, R1, X1 and H2 each give `s` back unchanged, and 792
of the 2000 cases have an answer other than `s`; `s` itself has its own
letters, is no greater than itself, comes back unchanged from every pair
set and shifts with its letters, so only the literal reading and the ★
arm catch them. B1 and H1 fail on exactly the 1144 cases where some group
holds two different letters (counted by a Python reading of the cases):
there, handing out the least letter for ever, or the greatest first,
differs from the answer, and B1's repeated letter changes the letters
too. H1 is the heap arm as `karac fix` wrote it before the fix in Gaps.
R2 and X2 are one fault in two arms, `parent[a] = b` on the indices
rather than their roots, and fail alike; turning the pairs round (P3)
catches more of them than the literal reading does, probably because a
union at an index that is not its root loses that index's earlier
joins, which depend on the order the pairs come in (inferred, not
traced).

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (a union-find over the indices, path halving and union by size; each
group's letters, sorted, go back to its indices in rising order) on one
string of 100000 random letters and four sets of pairs drawn once: 25000
random pairs, 100000 random pairs, each index joined to the one two on,
and each to the one 1000 on. Then 10 rounds over the four, each answer
folded into a checksum. Every program prints `10 rounds over 4 sets of
pairs on 100000 letters: checksum 406741769`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.266 to 0.334 s | 0.291 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.260 to 0.338 s | 0.304 s |
| Rust (`rustc -O`) | 0.218 to 0.261 s | 0.237 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.223 to 0.354 s | 0.244 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.222 to 0.280 s | 0.249 s |
| C (`clang -O3`) | 0.475 to 0.537 s | 0.515 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.478 to 0.605 s | 0.506 s |
| Go | 0.372 to 0.436 s | 0.398 s |
| Python | 5.746 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on is about 20% ahead of Kāra (0.244 s
against 0.304 s), and the two ranges overlap. C takes about 1.7x Kāra's
time; Kāra is about 24% ahead of Go (0.304 s against 0.398 s). Python
takes about 19x Kāra's time. No profile was taken.
