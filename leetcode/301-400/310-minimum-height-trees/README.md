# 310. Minimum Height Trees

Given a tree — `n` nodes, `n − 1` edges, connected and acyclic — find every
node that, used as the root, minimises the tree's height.

```
n = 6,  edges 3–0, 3–1, 3–2, 3–4, 5–4

      0   1   2                 rooted at 3: height 3
       \  |  /                  rooted at 4: height 3
         (3) — (4) — 5          rooted at anything else: more
                            ->  [3, 4]
```

The answer is always **one node or two adjacent ones** — the tree's *centre* —
and never more. That fact is what the whole problem turns on, and every arm
below either exploits it or measures around it. After a run of range-query and
DP katas, this is the corpus's first graph algorithm in the 301–400 block.

## Approaches

| file | mechanism | time |
|---|---|---|
| `minimum_height_trees.kara` ★ | peel whole layers of leaves until 1 or 2 remain | O(n) |
| `minimum_height_trees_diameter.kara` | two BFS, rebuild the longest path, take its midpoint | O(n) |
| `minimum_height_trees_ecc.kara` | `ecc(v) = max(dist to each diameter endpoint)`, argmin | O(n) |
| `minimum_height_trees_brute.kara` | root at every node, measure the height, keep the argmin | O(n²) |
| `differential.kara` | 4,800 trees, four arms, seven properties | — |
| `bench/peel.kara` | four 60,000-node trees × 950 peeling passes | — |

## The mechanism

Remove every degree-1 node **simultaneously** — that is one layer gone from
every branch at once — and repeat. Each round shortens the longest path by
exactly two, one from each end, so the process converges on the middle of the
diameter and stops when 1 or 2 nodes remain.

Why it stops at 1 or 2 and never 3: the centre is the midpoint of the diameter.
An even number of edges puts the midpoint on a single node; an odd number puts
it between two adjacent nodes and both qualify. There is no third case, so
`remaining > 2` is the exact loop condition — no separate termination test.

### The characteristic bug is peeling mid-layer

Removing leaves *individually* lets a node that became a leaf **during** this
round be peeled in the same round, which shortens one branch faster than
another and drifts the answer off-centre. The fix is to snapshot the current
leaf set before removing any of it — the same "snapshot before mutating"
discipline [#309](../309-best-time-to-buy-and-sell-stock-with-cooldown/)'s
rolling DP needed, in a different shape.

Mutating the ★ arm to push newly-made leaves into the *current* layer doesn't
just give wrong answers: the loop **never terminates**, because the layer it is
iterating keeps growing.

## Properties, not just agreement

| # | property | what it pins down |
|---|---|---|
| P1 | four arms, one answer | the algorithm, from four directions |
| P2 | the answer has size 1 or 2 | the centre theorem itself |
| P3 | when there are two, they are adjacent | ditto |
| P4 | the answer is exactly the set of eccentricity minimisers | ties it to the definition |
| P5 | min-height = `ceil(diameter / 2)` | ties it to the diameter, independently |
| P6 | relabelling the nodes permutes the answer identically | **no arm computes this** |
| P7 | a path's centre is its middle; a star's is its hub | shapes the statement fixes |

```
trees 4800
P1..P7 all 0
DIFFERENTIAL OK
```

**P6 is the one no arm computes.** The answer is a property of the tree's
*shape*, not its labels — permute every label, remap the edges, and the answer
must be the image of the original under that same permutation. Every arm is
label-sensitive internally: ★ seeds from the lowest-numbered leaves, the
diameter arm starts its BFS at node 0, the eccentricity arm breaks ties by
scanning in index order. So a label dependence is exactly the fault four-way
agreement is blind to — all four would inherit it from the input. Nothing in
any arm is trying to be isomorphism-invariant; the property asserts it from
outside.

**Arm C is the one that assumes nothing.** The other three all rest on the same
theorem — the answer is the diameter's midpoint, hence of size 1 or 2 — and
merely exploit it differently. If that theorem were misapplied they could be
wrong *together* and still agree. Arm C roots the tree at every node and
measures, which is what the statement actually asks.

## Mutation-tested, because a differential that cannot fail is decoration

| # | mutation | caught by |
|---|---|---|
| M1 | newly-made leaves peeled in the **same** round | **non-termination** |
| M2 | `remaining` decremented by 1 rather than by the layer size | P1 P2 · P4 · P7 |
| M3′ | diameter arm always emits **one** midpoint, ignoring parity | P1 |
| M4 | even-length midpoint pair shifted by one | P1 |
| M5 | eccentricity from **one** diameter endpoint, not both | P1 |
| M3 | **control** — `len/2` for `(len-1)/2` on the odd branch | *(correctly survives — identical expression)* |
| M6 | **control** — `>=` for `>` in an argmin scan | *(correctly survives)* |

### Two things the battery corrected

**M3 is an equivalent mutation, not a gap.** For odd `L`, `(L−1)/2` and `L/2`
are the same value under integer division — checked for every odd `L` up to 13.
Swapping them changes nothing, so it belongs in the table as a control. The
*real* parity bug is M3′: collapsing both branches to a single midpoint.

**And that one is wrong on 48.6% of trees** — measured over 20,000 random
trees, counting how many have a diameter path with an even node count. Arm B's
source comment originally said "about half"; it now says 48.6%, because the
number was cheap to get and a guess in a comment is a guess that ships.

## Benchmarks

Build four 60,000-node random trees once in flat CSR (an offsets array plus a
neighbours array); then punch 950 leaf-peeling passes, `build-once + punch`
([BENCHMARKS.md](../../../BENCHMARKS.md)). All five languages print
`checksum 56999050`.

**Each pass selects its tree from the previous pass's answer.** Peeling is a
pure function of its tree, so 950 identical peels of one unchanging tree are
exactly the shape an optimiser may hoist and run once; making the choice depend
on the last answer creates a serial dependency, so every pass must run.

Container x86-64, [`bench/results.container-x86.json`](bench/results.container-x86.json),
30 runs each.

| | mean | vs kara |
|---|---:|---:|
| rust (`-O`) | 592.6 ms | 0.98× |
| **kara** (codegen, seq) | **607.1 ms** | **1.00×** |
| go | 630.1 ms | 1.04× |
| rust (equal safety + matched ISA) | 647.2 ms | 1.07× |
| rust (`-O -C overflow-checks=on`, equal safety) | 651.1 ms | 1.07× |
| c (`-O3 -march=x86-64-v3`, matched ISA) | 704.1 ms | 1.16× |
| c (`-O3`) | 708.3 ms | 1.17× |
| python | 38.965 s | 64.2× |

**Kāra is faster than `clang -O3` here — the first time in this run.** Because
that is a result favourable to kāra, it was checked harder than an unfavourable
one would be: an independent back-to-back `hyperfine` session reproduced it
(kāra 605.0 ms ± 13.1 against C 723.3 ms ± 21.9), and the C mirror was rebuilt
at `-O2` (0.70 s) and `-O3 -march=native` (0.69 s) in case `-O3` was
pessimising. All five binaries print the same checksum, so they are doing the
same work.

**The cause is not established, and this README does not guess at one.** The
workload is dominated by two long strided passes per round — the O(n)
degree/alive re-initialisation and the O(n) final accumulate — around a
pointer-chasing peel, and which of those kāra's codegen handles better than
clang's is exactly the question a timing table cannot answer. Distinguishing
them would need per-loop instrumentation this lane does not carry. Recorded as
measured, on the same principle as
[#304](../304-range-sum-query-2d-immutable/)'s refuted stride-multiply
hypothesis and [#309](../309-best-time-to-buy-and-sell-stock-with-cooldown/)'s
unexplained loss to equal-safety Rust — the corpus is more useful with honest
gaps in it than with plausible stories.

Kāra also leads Go (1.04×) and both equal-safety Rust builds (1.07×), and
trails only plain `rustc -O` by 2%.

### One caveat on the layout

The lane uses **flat CSR**, not the nested `Vec[Vec[i64]]` adjacency the ★ arm
uses, because all five languages must index identically and C has no natural
nested form. [#308](../308-range-sum-query-2d-mutable/) measured what that
choice costs kāra on a different workload — nested beat flat by **1.59×** there,
because flat's `x * stride + y` is checked arithmetic on every access while
nested indexing hides the same computation inside a pointer load. The same
caveat applies here: this table is the flat number, and the kata's own arm is
written the other way.

## Compiler findings

The arms are clean — zero `karac check` diagnostics across all six sources, all
byte-identical under `karac run`, `karac build` and the default
auto-parallelising build, matching the Python oracle.

**No compiler defect surfaced.** Probed before shipping, targeting the graph
idioms these four arms happen not to use:

- **`Map[i64, Vec[i64]]` adjacency** — the natural spelling when node ids are
  sparse rather than dense `0..n`. Clean under keyed insert and lookup. (Never
  walked, so no iteration-order exposure — the repo rule about `Map`/`Set` order
  applies to walks, not lookups.)
- **`Set[i64]` as the visited frontier**, instead of a dense `Vec[i64]` marker
  array — clean; membership and `len` are both order-independent.
- **Recursive DFS with an explicit parent guard** — the shape a rerooting DP
  needs, and the one traversal style none of the four arms uses (all four are
  iterative). Clean.
- **Pushing into a `Vec` while iterating it by index** — the BFS-queue idiom
  every arm here relies on, where the loop bound must be re-read each iteration.
  Clean; the queue grows correctly mid-loop.

That last one is worth pinning explicitly rather than assuming, because the ★
arm's non-terminating mutation (M1) is precisely a *mis*use of it: appending to
the container being iterated is correct for a BFS queue and catastrophic for a
peeling layer, and the compiler cannot tell the two apart.

## Running it

```bash
karac run minimum_height_trees.kara           # ★ leaf peeling
karac run minimum_height_trees_diameter.kara  # diameter midpoint
karac run minimum_height_trees_ecc.kara       # eccentricity from endpoints
karac run minimum_height_trees_brute.kara     # the definition, O(n²)
karac run differential.kara                   # 4,800 trees, seven properties

bash bench/bench.sh                           # cross-language lane
```
