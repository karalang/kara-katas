# 1203. Sort Items by Groups Respecting Dependencies

There are `n` items each belonging to zero or one of `m` groups where
`group[i]` is the group that the `i`-th item belongs to and it's equal to
`-1` if the `i`-th item belongs to no group. The items and the groups are
zero indexed. A group can have no item belonging to it.

Return a sorted list of the items such that:

- The items that belong to the same group are next to each other in the
  sorted list.
- There are some relations between these items where `beforeItems[i]` is
  a list containing all the items that should come before the `i`-th item
  in the sorted array (to the left of the `i`-th item).

Return any solution if there is more than one solution and return an
empty list if there is no solution.

```
n = 8, m = 2, group = [-1,-1,1,0,0,1,0,-1],
beforeItems = [[],[6],[5],[6],[3,6],[],[],[]]    ->  [6,3,4,1,5,2,0,7]
n = 8, m = 2, group = [-1,-1,1,0,0,1,0,-1],
beforeItems = [[],[6],[5],[6],[3],[],[4],[]]     ->  []
```

**Constraints:** `1 <= m <= n <= 3 * 10^4`; `group.length ==
beforeItems.length == n`; `-1 <= group[i] <= m - 1`; `0 <=
beforeItems[i].length <= n - 1`; `0 <= beforeItems[i][j] <= n - 1`; `i !=
beforeItems[i][j]`; `beforeItems[i]` does not contain duplicates
elements.

The arms are `fn sort_items(n: i64, m: i64, group: Vec[i64],
before_items: Vec[Vec[i64]]) -> Vec[i64]`. The two Rust arms keep the
method LeetCode gives Rust users, on `i32`, inside `impl Solution`, and a
one-line `sort_items` calls it.

## Approaches

Any answer is accepted, so the arms give different orders, and the
harness prints, for each case, whether the arm found an order and
whether it is one: every item once, each group's items side by side, and
every item after the items it must follow. With each item in no group
given a group of its own, an answer exists exactly when both the items
and the groups (an edge from a dependency's group to the item's when the
two differ) can be sorted topologically.

| file | mechanism |
|---|---|
| `sort_items.kara` ★ | Kahn's algorithm twice, over the groups and over the items, each with a `Vec` and a head index for its queue; the items, in their sorted order, dealt into their groups, and the groups laid out in theirs. O(n + m + e) |
| `sort_items_dfs.kara` | both sorts a recursive depth-first search with three colours (unseen, on the path, done): a node met again while on the path closes a cycle, and the nodes in the reverse of the order they finish are sorted |
| `sort_items_lifo.kara` | one graph: each group a gate in and a gate out, each grouped item between its group's two, and a dependency across groups an edge from one group's gate out to the other's gate in; Kahn's algorithm with a stack, so once a gate in is taken everything it frees is of its group and comes out next |
| `sort_items_heap.kara` | Kahn's algorithm over a smallest-first `PriorityQueue` for both sorts, so each takes the least node it may: the least answer in that sense |
| `sort_items_solution.kara` | a Rust solution as LeetCode's Rust users write it (`group.iter_mut()` numbering the items in no group, `vec![vec![]; m]` graphs with in-degree counts, a nested `fn topo` over a `VecDeque` returning an `Option`, and the answer by `flat_map` over the group order with `std::mem::take`), carried to Kāra by `karac fix` |
| `sort_items_methods.kara` | another Rust solution (both graphs as `HashMap<i32, Vec<i32>>` filled with `entry(..).or_insert_with(Vec::new)`, a nested recursive `fn dfs` keeping each node's colour in a `HashMap<i32, u8>` and matching `state.get(&u)` against `Some(1)` and `Some(2)`, and each group's members taken out of a map with `remove`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six more properties |

Every arm prints the same 12 lines: LeetCode's two examples; one item;
two cases where an item in no group stands between two items of one
group, one with no answer; two where two groups each wait on the other;
a chain of five items in no group; two items that each wait on the
other; 1000 random cases of up to nine items (`1000 random cases: 618
ordered, 382 with none, 0 invalid`); and two at the constraints' top,
30000 items in 3000 groups and a third in none, each after up to three
earlier items (`an order of 30000`), and the same with the first and
last items each made to follow the other (`none`).
`sort_items.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac run` and `karac build`, and
under the AddressSanitizer build.

The Mend loop: the ★, dfs, lifo and heap arms check clean as written.
The solution arm takes one round of 70 fixes (among them `struct
Solution;` to `struct Solution {}`, the nested `fn topo` moved to the top
level, `&Vec<Vec<usize>>` to `Vec[Vec[i64]]` and `&mut Vec<i32>` to `mut
ref Vec[i32]`, `vec![vec![]; m]` to `Vec.filled(m, Vec.new())`, `for &b
in &before_items[i]` to `for b in ref before_items[i]`, `group: Vec<i32>`
to `own Vec[i32]` for the `let mut group = group;` that takes it, and
`std::mem::take(&mut buckets[g])` to `take(mut buckets[g]).into_iter()`),
and the methods arm one round of 75 (among them the `use` line dropped,
the nested `fn dfs` moved to the top level, `HashMap<i32, Vec<i32>>` to
`Map[i32, Vec[i32]]`, `or_insert_with(Vec::new)` to
`or_insert_with(Vec.new)`, `state.get(&u)` to `state.get(u)` with its
`Some(1)` and `Some(2)` patterns kept, `!dfs(..)` to `not dfs(..)`, and
`or_default()` to `or_insert(Vec.new())`). Both outputs match.

## Gaps

None found.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every order of the items tried, each checked against the two
rules, and an answer exists when one passes. 2000 random cases: 1 to 6
items in up to as many groups, each after up to two others; 1394 of them
have an answer.

| | property |
|---|---|
| P1 | the statement read literally: an answer exactly when one exists |
| P2 | every item once, each group's items side by side |
| P3 | every item after the items it must follow |
| P4 | the items numbered the other way round give an answer just when the items do |
| P5 | the groups numbered the other way round give an answer just when they do |
| P6 | one more dependency never makes an answer where there was none |
| P7 | the ★ arm gives an answer just when this arm does |

All 84,000 checks pass on every arm: `2000 cases: checksum 785219071,
84000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. The checksum folds
the ★ arm's order and the literal reading's verdict; a Python reading of
the same cases, trying every order with `itertools.permutations` and
sorting with the Python mirror, gives the same checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: no edge between groups | P1 115, P3 650, P7 575 |
| S2 | ★: a sort left short by a cycle still given | P1 310, P2 310, P3 310, P7 1550 |
| D1 | dfs: a node on the path taken for one done | P1 606, P3 606, P7 606 |
| D2 | dfs: the finished order never reversed | P3 906 |
| L1 | lifo: no item before its group's gate out | P1 450, P3 496, P7 450 |
| L2 | lifo: a dependency inside a group sent through its gates | P1 318, P7 318 |
| H1 | heap: a cycle among the groups unnoticed | P1 58, P2 58, P3 58, P7 58 |
| H2 | heap: an in-degree never brought down | P1 906, P7 906 |
| X1 | solution: an item's in-degree never counted | P1 68, P3 250, P7 68 |
| X2 | solution: every item in no group put in the first group | P1 76, P2 115, P5 97, P7 76 |
| M1 | methods: the items' finished order never reversed | P3 318 |
| M2 | methods: a node on the path taken for one done | P1 606, P3 606, P7 606 |

A mutation of the ★ arm fails P7 on all six arms, the ★ arm against the
other five. Of the 2000 cases, 906 have an answer and at least one
dependency, and 318 of those a dependency between two items of one group
(both counted by a Python reading of the cases). H2 never brings an
in-degree down, so only nodes nothing points at are ever taken, and it
finds no answer in exactly the 906. D2 leaves both of the dfs arm's
orders unreversed, so every dependency points the wrong way, and P3 fails
the same 906 while P1 holds: it answers exactly when an answer exists.
M1 leaves only the items' order unreversed in the methods arm; the
groups still come in order, so only a dependency inside a group is
broken, and P3 fails the 318. L2 sends a dependency inside a group
through the group's own gates, a loop from its gate out to its gate in,
and finds no answer in the same 318. S2 and H1 hand back an order cut
short by a cycle, which P2 and P3 refuse as well as P1. P5, the groups
renumbered, catches only X2, which puts the items in no group into group
0: renumbering the groups changes which group's items they must sit
beside.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (each item in no group given one of its own, then Kahn's algorithm
over the groups and over the items) on four instances at the
constraints' top, 30000 items, drawn once: every tenth in no group and
the nine after it in a group of their own (3000 groups), each item after
up to three of the items before it; the same with up to six; every item
in no group, up to three; and the first with the last item and the first
each made to follow the other, which has no answer. Then 10 rounds over
the four, each answer folded into a checksum. Every program prints `10
rounds over 4 instances of 30000 items: checksum 64501306`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.255 to 0.323 s | 0.268 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.258 to 0.341 s | 0.284 s |
| Rust (`rustc -O`) | 0.274 to 0.345 s | 0.289 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.272 to 0.349 s | 0.291 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.274 to 0.367 s | 0.301 s |
| C (`clang -O3`) | 0.149 to 0.192 s | 0.174 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.148 to 0.185 s | 0.154 s |
| Go | 0.366 to 0.479 s | 0.420 s |
| Python | 2.154 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (0.291 s
against 0.284 s), and the two ranges overlap. Kāra takes about 1.6x C's
time (0.284 s against 0.174 s); Kāra is about 32% ahead of Go (0.284 s
against 0.420 s). Python takes about 8x Kāra's time. No profile was
taken.
