# 323. Number of Connected Components in an Undirected Graph

There are `n` nodes, labelled `0..n-1`, and a list of undirected edges. Return
how many connected components the graph has.

```
n = 5  edges = [(0, 1), (1, 2), (3, 4)]          ->  2
n = 5  edges = [(0, 1), (1, 2), (2, 3), (3, 4)]  ->  1
```

Every node starts as a component on its own, so the answer starts at `n`. An
edge either joins two different components, which lowers the count by one, or
lands inside a component that already exists, which changes nothing. The
problem is telling those two cases apart. The statement does not promise a
simple graph, so self-loops and repeated edges are allowed here, and both have
to change nothing.

## Approaches

| file | mechanism | cost |
|---|---|---|
| `count_components.kara` ★ | disjoint-set forest, union by size, path compression | `O((n + edges) · α(n))` |
| `count_components_dfs.kara` | adjacency lists, flood from every unseen node with a stack | `O(n + edges)` |
| `count_components_bfs.kara` | the same sweep with a queue, over a packed CSR adjacency array | `O(n + edges)` |
| `count_components_labels.kara` | push the smaller label across every edge until nothing moves | `O(edges · longest path)` |
| `differential.kara` | four arms, a transitive-closure oracle, thirteen properties | — |
| `bench/count_components.kara` | 16 passes, each up to 1,000,000 random edges over 1,000,000 nodes | — |

All four arms print the same eleven fixed cases and three small random ones.
The ★, DFS and BFS arms also print three large random cases (up to 100,000
nodes). The labels arm skips those, because a sweep per step of the longest
path is too slow at that size. `count_components.py` mirrors the ★ arm and
prints all seventeen lines.

## Four ways to count components

**★ Union-find.** Each component is a tree, and its root names it. Two nodes
are in the same component when `find` gives them the same root, and `merge`
joins two trees by hanging one root under the other. The count starts at `n`
and drops by one on every `merge` that finds two different roots. Two
standard tricks keep the trees shallow. Union by size hangs the smaller tree
under the larger, so a tree of height `h` holds at least `2^h` nodes. Path
compression points every node that `find` walks past straight at the root.
This arm never builds a graph. It looks at one edge at a time and asks only
whether that edge joins two groups.

**Depth-first search.** Build the adjacency lists, then sweep the nodes in
order. A node that has not been seen yet starts a new component: count it and
flood out from it with an explicit stack. This arm never looks at an edge on
its own. It asks what one node can reach, which is the definition of a
component read literally.

**Breadth-first search over CSR.** The same sweep with different machinery.
The adjacency lists are packed into one flat array: `start[v]..start[v + 1]`
is the slice of `nbr` that holds v's neighbours. A counting pass sizes each
slice and a prefix sum places it, so the graph is two flat Vecs instead of `n`
small ones. The flood uses a queue, so nodes are reached in a different order
from the DFS arm on every graph with a branch. The count does not depend on
that order, and running both arms is how that gets checked.

**Label propagation.** Every node starts with its own index as a label. Then
sweep the edges again and again, setting both ends of every edge to the
smaller of their two labels, until a sweep changes nothing. A label only ever
moves to one a neighbour already holds, so it never crosses between
components. Inside a component the smallest index spreads one edge further on
every sweep. At the fixed point, the components are the nodes that still hold
their own index. There is no forest, no adjacency list and no traversal order,
only "take the minimum across an edge" repeated until it stops changing.

## Differential

`karac run differential.kara` has three tiers:

- Every simple graph on 0 to 5 nodes, 1100 graphs in all.
- 240 random multigraphs on up to 12 nodes, with self-loops and repeats.
- 24 larger sparse graphs on 20 to 219 nodes, where the closure is too slow.

```
cases 1364 closure-cases 1340 edge-removal-cases 1343
DIFFERENTIAL OK
```

The oracle is a boolean transitive closure (Warshall). It computes
reachability from its definition and says a node starts a component when no
smaller node reaches it. It has no forest, no traversal and no fixed point.

| # | property |
|---|---|
| P1 | the DFS arm agrees with the ★ arm |
| P2 | the BFS arm agrees with the ★ arm |
| P3 | the labels arm agrees with the ★ arm |
| P4 | the transitive closure agrees with the ★ arm (up to 12 nodes) |
| P5 | `max(1, n - edges) <= answer <= n` |
| P6 | reversing or shuffling the edge list changes nothing |
| P7 | swapping the two ends of every edge changes nothing |
| P8 | relabelling the nodes by a random permutation changes nothing |
| P9 | doubling every edge and adding a self-loop at every node changes nothing |
| P10 | adding an edge lowers the answer by at most one, and by exactly one when the closure says its ends were apart; removing an edge raises it by at most one |
| P11 | the answer adds over the disjoint union of two graphs |
| P12 | one extra node joined to every node leaves exactly one component |
| P13 | keeping each edge only if it lowers the count keeps exactly `n - answer` edges, and leaves the count at the answer |

P4 and P13 check the answer rather than an arm. P4 is reachability computed
from nothing but its definition. P13 ties the count to the other thing it
determines, the size of a spanning forest. A count that is off by one somewhere
cannot also have exactly `n - answer` edges doing the connecting.

The sizes are set by the tree-walk interpreter, not by the JIT. The whole
harness takes 0.5 s under `karac run` and about 55 s under `karac run --interp`.

## Mutation testing

Sixteen content-anchored edits to `differential.kara`, each run through the
full harness under `karac run`. A panic or a hang counts as a kill alongside
`DIFFERENTIAL FAILED`.

| # | mutation | predicted | outcome | properties that fired |
|---|---|---|---|---|
| M1 | the ★ `merge` counts a merge of two nodes already together | kill | **killed** (overflow panic) | — |
| M2 | the ★ `find` skips path compression | *silent* | silent | — |
| M3 | union by size hangs the larger tree under the smaller | *silent* | silent | — |
| M4 | the ★ arm starts with one set too few | kill | **killed** | P1, P2, P3, P4, P5, P11, P12, P13 |
| M5 | the DFS adjacency is directed (drops `b -> a`) | kill | **killed** | P1 |
| M6 | the BFS CSR is directed (drops `b -> a`) | kill | **killed** | P2 |
| M7 | labels spread the largest index instead of the smallest | *silent* | silent | — |
| M8 | labels stop after one sweep | kill | **killed** | P3 |
| M9 | the closure seeds only one direction per edge | kill | **killed** | P4, P10 |
| M10 | the closure loop puts `k` innermost (not Warshall) | kill | **killed** | P4, P10 |
| M11 | P5's lower bound is one too high | kill | **killed** | P5 |
| M12 | the "flipped" transformation does not flip | *silent* | silent | — |
| M13 | the relabelling forgets the second end of each edge | kill | **killed** | P8 |
| M14 | the self-loops all point at node 0 | kill | **killed** | P9 |
| M15 | the hub node skips node 0 | kill | **killed** | P12 |
| M16 | P13 keeps an edge that does not lower the count | kill | **killed** | P13 |

**12 killed, 4 silent, and every prediction held.** The four silent mutants
are equivalent, and each for a reason that can be stated. M2 and M3 remove the
two tricks that make union-find fast, and neither changes an answer. M7 is
correct too: the largest index names a component as well as the smallest does,
and "the node still holds its own index" is true once per component either
way. M12 turns P7 into an identity check, and nothing else uses the flipped
graph.

M1 was predicted to fail P1–P4 and did not get that far. Without the early
return, a merge of a root with itself still doubles that root's size, and
a run of self-loops overflowed it within a few dozen merges. Kāra's default
overflow checking stopped the harness there, with `integer overflow` in
`DisjointSet.merge`. In a language that wraps, this
mutant would have carried on and been caught by the count instead. M4 was
predicted to fire P1–P5 and P12, and it also fired P11 and P13, since an answer
one too small breaks the disjoint-union sum and the spanning-forest size as
well.

## Verification

All four arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build`. `scripts/surface-sweep.py --filter
323- --timeout 400` reports `5 programs · 5 clean · 0 DIVERGENCES`. The ★ arm's
full output, including the three large cases, is byte-identical to
`count_components.py`. The other three arms match its first fourteen lines.

The benchmark kernel is verified on JIT, AOT-sequential and AOT-auto-par, and
its sink matches all four language twins (`sink 164091388 components 161628`).
It is not run under `--interp`, because at this size the tree-walk backend
would take far too long. The kata's semantics are covered by the arms and the
differential, which do run on every backend.

## Benchmarks

`bench/count_components.kara` and its four mirrors allocate one disjoint-set
forest over 1,000,000 nodes and run 16 passes over it. Each pass resets the
forest to singletons and feeds it `M` random edges from an LCG, with `M`
cycling through 250,000, 500,000, 750,000 and 1,000,000. That covers a random
graph from below its giant-component threshold (`M = n/2`) to well above it,
about 10 million merges and 20 million `find`s per run. After each pass the
component count and a stride-9973 sample of roots are folded into a rolling
hash, so the forest's shape stays observable as well as the count.

The edges are never stored. What is timed is the forest's random walks over
two 8 MB arrays, which are cache misses more than arithmetic. The reset at the
start of each pass is a refill loop that an optimizer can vectorise, but it is
one sequential write per node against two random-access `find`s per edge, so
it is a small share of the run.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`, the file
> `scripts/consolidate-bench.sh` feeds into the top-level chart) is not
> measured yet, and `bench-lib.sh` refuses to write it from Linux. Absolute
> milliseconds are NOT comparable between hosts. Only the **within-file
> cross-language ratios** are.

30 runs each, 5 warmups, on a 4-core x86-64 Linux container, karac
`0.1.0-dev.9486+ged4df8e22`, measured 2026-09-23. Python is its own lane at
3 runs.

| implementation | mean | vs fastest |
|---|---|---|
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 391.3 ms ± 13.2 | 1.00× |
| rust `-O -C overflow-checks=on` (equal-safety) | 402.8 ms ± 13.8 | 1.03× |
| c `-march=x86-64-v3` (matched-ISA) | 408.5 ms ± 14.7 | 1.04× |
| rust `-O` | 410.2 ms ± 14.5 | 1.05× |
| c `clang -O3` | 412.3 ms ± 13.3 | 1.05× |
| **kāra `karac build`** | **414.2 ms ± 13.8** | **1.06×** |
| go `go build` | 668.0 ms ± 20.1 | 1.71× |
| python 3 | 23866 ms ± 197 | 61.0× |

**Kāra, C and Rust are tied.** The six compiled C, Rust and Kāra builds span
391 to 414 ms, and every pair is within one standard deviation of every other,
whether overflow checks are on or off and whatever the ISA. That is what a
memory-bound kernel looks like: a random `find` is a chain of dependent loads
into two 8 MB arrays, and the time goes to cache misses that no compiler can
remove. Overflow checks cost nothing measurable here, unlike kata 322, whose
inner loop was pure arithmetic. Go is 1.71× behind. That gap was not
profiled; Go bounds-checks every slice access, as Kāra does, so the checks
alone do not explain it.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 85.7 ms ± 1.9 | 15.8 KiB | 16.8 MiB |
| rust | 149.0 ms ± 4.3 | 3863.5 KiB | 17.2 MiB |
| kāra | 320.6 ms ± 11.8 | 341.6 KiB | 17.8 MiB |
| go | — | 2179.1 KiB | 17.4 MiB |
| python | — | — | 53.7 MiB |

Peak RSS is dominated by the two 8 MB arrays, which every mirror allocates
once. `karac build` is 3.7× clang's cold compile and 2.2× rustc's. Its binary
is 22× clang's and 11× smaller than rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

**Six found, all fixed.** Three were fixed in kara `a4ce83d04`, and three more in `a8ad4239a` and `c7b9cbdbf`. The first one hit
the ★ arm as written: its `for (a, b) in edges` loop did not type-check. The
rest came from probing other ways to write the same problem, fourteen
spellings in all, each run on all four surfaces. Nothing in this directory had
to be changed to dodge one.

- **[`B-2026-09-23-28`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) (high): a tuple pattern over a borrowed tuple was
  refused.** `edges: ref Vec[(i64, i64)]` makes every element a
  `ref (i64, i64)`, and `for (a, b) in edges` failed with `tuple pattern used
  but type is ref (i64, i64)` on every surface. So did design.md's own
  `for (key, value) in map` over a `ref Map` parameter. Each field now binds the
  way a bare `for` binds a borrowed element: a `Copy` scalar by value, anything
  else as a borrow. Accepting the pattern then exposed two more gaps behind it:
  `let (a, b) = ref v[i]` bound nothing under `--interp` and had no lowering in
  compiled code.
- **[`B-2026-09-23-29`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl): iterator terminals refused destructuring closure
  params and `enumerate()` sources.** `label.iter().enumerate().filter(|(i, l)|
  i == l).count()` failed on every compiled surface with `no handler for
  method 'count'`, and so did `any`, `all`, `position`, `find_map`,
  `partition` and `for_each` in the same shapes. Widening them turned up a
  double free that was already there: `fold`, `collect` and `count` over a
  `Vec[(String, i64)]` with a destructuring param freed each `String` twice,
  because the desugar projected every field into a second owner.
- **[`B-2026-09-23-30`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl): a `for` over a call that returns a `Slice` did
  not build.** A CSR graph's `fn neighbours(ref self, v: i64) -> Slice[i64]`
  used as `for w in g.neighbours(v)` ran under `--interp` and reached the
  unlowered-source error on every compiled surface, as did its `.iter()` and
  `.iter().enumerate()` forms and `v[a..b].iter().enumerate()`.

Fixed next, in kara `a8ad4239a` and `c7b9cbdbf`:

- **[`B-2026-09-23-31`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) (high): a heap field copied out of a borrowed tuple
  or `ref v[i]` binding was freed twice.** `let p = ref ps[1]; let name =
  p.0;` over `Vec[(String, i64)]`, the same through `for p in ps.iter()`, and
  `let q = ref qs[0]; let m = q.name;` over a struct all aborted with a double
  free on every compiled surface. `--interp` printed the right output. Those
  roots now get the copy that a `ref P` parameter already got. They still do
  not warn `borrow_projection_copy` the way the parameter does.
- **[`B-2026-09-23-32`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl): `enumerate().map(..).collect()` over heap tuples
  double-freed.** `names.iter().enumerate().map(|q| q.0 + q.1.1).collect()`
  over `Vec[(String, i64)]` reads only an index and an integer, and still
  aborted with a double free on every compiled surface. `enumerate()` put the
  loop element whole into a tuple that then owned it too.
- **[`B-2026-09-23-33`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) (test infra): an ASAN fixture with a parse error passed.**
  Found while writing the fixtures for this kata's fixes. One used `&&`, which
  Kāra spells `and`, and the harness printed `setup failed — skipping` and
  reported `ok`. A parse failure now fails the fixture. That exposed six
  existing fixtures that had never parsed. Five were repaired. The sixth was
  hiding a real double free when a `String` is moved out of a `Map.get` enum
  payload (`B-2026-09-23-40`), which was fixed in the same commit.

Two older faults turned up along the way, and both are now fixed:

- **[`B-2026-09-23-38`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl): a nested tuple member read leaked.**
  `println(v[0].1.0)` over `Vec[(i64, (String, i64))]` leaked one copy of the
  `String` per read. The read now copies only the leaf and frees it.
- **[`B-2026-09-23-39`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl): a borrowed payload field bound
  without a type.** In `match v.get(0) { Some(B.S(w)) => ... }`, `w` had no
  type, so a moved `w` read back empty and `w.len()` did not compile. `w` is now
  a borrow, like the bare `Some(w)`: reads and `len` work everywhere, and moving
  it out is a type error (`.clone()` it instead).

Two more gaps found next to those are fixed too:
[`B-2026-09-24-1`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) (`let t = r;` over a borrowed `String`
lost its type, so `t.len()` did not build) and
[`B-2026-09-24-2`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) (`v[0].1.0.s`, a field on a struct
nested in a tuple in a `Vec` element, did not build; making it build also
fixed a double free when a `match` moves an enum field out of `v[0].1.k`).
Their three neighbours `B-2026-09-24-6`, `-7` and `-8` were fixed in kara `889202e1c`; two narrower remainders stay open as `B-2026-09-24-17` (a nested enum pattern or `Option[Map]` payload over an element field) and `-18` (a spurious `borrow_projection_copy` warning).

No `KARAC_AUTO_PAR=0`-only pass, and nothing contorted.
