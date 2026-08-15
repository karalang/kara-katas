# 261. Graph Valid Tree

`n` nodes labelled `0..n-1` and a list of undirected edges. Return whether they
form a **valid tree**.

```
n=5, [[0,1],[0,2],[0,3],[0,4]]      ->  true    star
n=5, [[0,1],[1,2],[2,3],[3,4]]      ->  true    path
n=4, [[0,1],[1,2],[2,3],[0,3]]      ->  false   cycle
n=4, [[0,1],[1,2],[0,2]]            ->  false   3 = n-1 edges, still not a tree
n=1, []                             ->  true
```

**Constraints:** `1 ≤ n ≤ 2000`; `0 ≤ edges.length ≤ 5000`; no self-loops and no
repeated edges.

## Approaches

| file | mechanism | establishes |
|---|---|---|
| `graph_valid_tree.kara` ★ | union-find, union by size + path compression | acyclic ∧ connected |
| `graph_valid_tree_bfs.kara` | edge count, then BFS reachability | \|E\| = n−1 ∧ connected |
| `graph_valid_tree_peel.kara` | erode leaves until nothing is a leaf | acyclic ∧ connected, from the residue |
| `differential.kara` | 4,000 randomized graphs, all three agree | — |

## The mechanism

A graph on `n` nodes is a tree iff it is **acyclic**, **connected**, and has
**exactly `n − 1` edges** — and *any two of those imply the third*.

That is the whole problem, and it is why a wrong answer here looks so complete.
Each of the three conditions is individually necessary and individually
insufficient, and each has a counterexample that is easy to miss:

| checking only | accepts, wrongly |
|---|---|
| `edges.len() == n - 1` | `n=4, [[0,1],[1,2],[0,2]]` — a triangle plus a stranded node 3 |
| acyclic | any forest: `n=5, [[0,1],[2,3],[3,4]]` |
| connected | anything with a cycle bolted on |

So a correct solution picks a **pair**. The three files here pick different
pairs, or reach the same pair by unrelated means.

## Why three, and what each one is really doing

**Union-find** merges the endpoints of each edge and rejects the first edge whose
endpoints already share a root — that edge closes a cycle. Surviving every edge
proves *acyclic*; a final component count of 1 proves *connected*. It never reads
`edges.len()`.

**BFS** does the reverse. It checks `edges.len() == n - 1` first, then walks from
node 0 and requires every node reached. It never looks for a cycle — and does not
need to, because (count ∧ connected) ⇒ acyclic. The order matters: the count test
is not a fast-path optimisation, it is half the proof. Delete that line and the
BFS reports true for *every connected graph*, cycles included.

**Leaf peeling** builds no spanning structure at all. Delete a degree-1 vertex
together with its edge, repeatedly:

- a tree erodes down to a single vertex;
- a cycle never erodes — every vertex on it holds degree ≥ 2 forever;
- a forest of `c` components erodes to exactly `c` vertices.

So *exactly one vertex survives* ⟺ valid tree, settling acyclic and connected
from the residue alone, with no edge count anywhere.

Two details in the peel are load-bearing. It must remove **one leaf at a time**,
not every current leaf per round: a two-node path has two leaves, and taking both
at once erodes to zero and reports false. And **degree 0 is not degree 1**, so an
isolated vertex never peels — which is exactly why `n=1` answers true and why the
triangle-plus-stranded-node case ends with four vertices standing rather than
one.

## A fourth approach, and why it is not here

The textbook undirected cycle check is a DFS that carries the parent and skips
the edge it arrived on. It is correct for this problem — but only because the
constraints forbid **repeated edges**. Given `n=2, [[0,1],[0,1]]` it walks 0 → 1,
sees 0 as a neighbour, dismisses it as the parent, and reports a valid tree on
two edges. The three forms here need no such assurance: union-find rejects the
second copy as a cycle, the count test rejects it outright, and the peel leaves
node degrees at 2 with nothing to erode.

## Generator design

A uniformly random edge set on `n` nodes is essentially never a tree, so a naive
generator answers false nearly always and exercises only the rejection path.
Worse, it almost never produces the case that actually separates these
algorithms: **a graph with exactly `n − 1` edges that is still not a tree**.

Five families are drawn deliberately instead:

| family | construction | answer |
|---|---|---|
| 0 | random tree by parent attachment | true |
| 1 | tree + one extra edge (`n` edges) | false — cycle |
| 2 | tree − one edge (`n−2` edges) | false — forest |
| 3 | ★ tree with one edge **rewired**, holding \|E\| = n−1 | either |
| 4 | uniform random edge set sized near `n−1` | mostly false |

Family 3 is the one that matters. It fixes the edge count and varies only the
shape, so `return edges.len() == n - 1` is wrong on exactly those cases and right
on every other. Family 0 keeps the accept path live; without it the harness would
agree trivially by rejecting everything.

Every family refuses self-loops and duplicate edges as they are drawn, matching
the constraints, and the edge list is shuffled before the deciders see it — the
parent-attachment families emit edges in topological order, which is a gift no
real input provides.

Over 4,000 cases: **1,711 valid trees** (43%, so both answers are well
represented) and **450 cases with exactly `n − 1` edges that are not trees**.

**All three failure modes were tested, not assumed:**

| injected bug | mismatches / 4,000 |
|---|---|
| `return edges.len() == n - 1` (count only) | **450** |
| union-find without the component check (acyclic only) | **858** |
| BFS without the edge-count guard (connected only) | **810** |

The first number is not a coincidence: it is exactly the count of generated
graphs with `n − 1` edges that are not trees, which is what a count-only decider
must get wrong and nothing else. The generator and the harness agree on their
own arithmetic.

## Benchmark

`bench/` builds **one random tree on 100,000 nodes once** — parent attachment,
then a Fisher–Yates shuffle of the edge list — and punches the ★ union-find
validator through it **240 times**. Sink `785843880`, reproduced by all four
compiled mirrors and by Python.

Two properties of the workload are deliberate:

- **The graph is a genuine tree**, so all `n − 1` edges are processed. There is
  no cycle to trigger the early `return false`, and the lane measures the full
  merge rather than a lucky exit on edge three.
- **The edges are shuffled.** Parent attachment emits them in topological order,
  and fed that way every union hangs a singleton off a growing root: one hop per
  find, nothing for path compression to compress, and the measurement collapses
  into a linear scan. Shuffled, the forest grows from the middle out and the
  finds walk real chains.

This is the corpus's **random dependent load** lane — the inner cost is chasing
`parent[parent[parent[…]]]` in an order no prefetcher can predict, which is a
different bottleneck from the sort-dominated ([#252](../252-meeting-rooms/),
[#253](../253-meeting-rooms-ii/)), allocation
([#254](../254-factor-combinations/)), string-building
([#257](../257-binary-tree-paths/)), integer-division
([#258](../258-add-digits/)) and branch-prediction ([#259](../259-3sum-smaller/))
lanes.

### n was set by measurement, not by taste

The first sizing, `n = 400,000`, produced a table that could not be ranked: σ of
8–21% across the lanes, and `c` at 554 ms against the same code at `-march=v3` at
437 ms, a 27% "ISA effect" on a pointer-chasing loop with nothing to vectorize.

Re-running **a single unchanged binary** by itself settled it — the spread is not
between languages, it is within one binary:

| n | working set | mean | σ | σ/mean | sys time |
|---|---|---:|---:|---:|---:|
| 30,000 | ~1 MB | 438.3 ms | 5.6 | **1.3%** | 0.4 ms |
| 100,000 | ~3 MB | 430.0 ms | 8.6 | **2.0%** | 1.6 ms |
| 400,000 | ~13 MB | 486.9 ms | 111.0 | **22.8%** | 31.0 ms |

Same total work at all three sizes — only the footprint changes. At 400,000 the
same binary scattered over 368–1126 ms, a 3× spread, with system time up 75×.
The container cannot hold a 13 MB randomly-accessed working set steady; it holds
3 MB fine.

So the lane runs at **n = 100,000** — the largest size that is measurable here,
and still large enough that `parent[]` alone is 800 KB and the chase is a real
L2-miss chain rather than an L1-resident one. Sizing down was not tuning for a
nicer number: at 400,000 there is no number, only noise.

### Runtime — sequential lane

Apple M5 Pro (6P+12E), 2026-08-15, `karac 0.1.0-dev.6106+g50267795a`, hyperfine
30 runs, `KARAC_AUTO_PAR=0`, every lane 99% CPU. This is the canonical host —
`bench/results.json`.

| Impl | Mean ± σ | vs Kāra |
|---|---|---|
| C `clang -O3` | 197.9 ± 2.6 ms | 0.88× |
| Rust `-O` | 201.1 ± 3.2 ms | 0.89× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 211.7 ± 5.9 ms | 0.94× |
| **Kāra (codegen)** | **224.7 ± 4.4 ms** | 1.00× |
| Go | 248.6 ± 2.1 ms | 1.11× |

**Kāra keeps its place between the two Rust builds' logic but not their times.**
On the container the six non-Go rows were a tie (7% spread, σ 2.6–4.6%); here σ
is 1.1–2.9% and the lane separates. Kāra is **1.14× behind C** and **1.06× behind
equal-safety Rust** — both gaps now clear the noise, where on the container
neither did. The 6% gap between the two Rust builds survives to this host almost
exactly (5.3% here), so the safety cost is stable and Kāra's remaining 6% over
the checked build is codegen, not contract.

**Go is 11% behind and remains the one clearly separable row**, down from 20% on
the container. This lane still does not identify its cause.

### The x86 corroboration run

| lang | mean (ms) | σ |
|---|---|---|
| C | 425.5 ± 17.0 | 4.0% |
| Rust | 429.5 ± 12.1 | 2.8% |
| C (`-march=x86-64-v3`) | 440.3 ± 20.2 | 4.6% |
| **Kāra** | **444.4 ± 11.7** | 2.6% |
| Rust (checked + `target-cpu=v3`) | 446.6 ± 18.3 | 4.1% |
| Rust (checked, equal-safety) | 455.1 ± 15.6 | 3.4% |
| Go | 512.0 ± 18.1 | 3.5% |

**C, Rust and Kāra are a six-way tie.** 425 to 455 ms is a 7% spread against σ of
2.6–4.6%; the ordering among those six is not resolvable, and neither the ISA
twins nor the safety twins separate from their siblings. Kāra sits between plain
Rust (429.5) and equal-safety Rust (455.1) — which is where a checked-arithmetic
implementation should sit, and the 6% gap between those two Rust builds is the
only intra-language effect this lane can see at all.

**Go is 20% behind and is the one separable row.** Its σ is no worse than the
others, so this is a real gap rather than a noise artifact — but this lane does
not identify its cause and I am not going to guess one.

Kāra's binary is 332.9 KiB against C's 15.7 KiB, Go's 2.16 MB and Rust's 3.86 MB;
peak RSS is 5.3 MiB against C's 4.5 MiB, within the array footprint the algorithm
requires.

`bench/results.container-x86.json` holds this run; it is corroboration only
(BENCHMARKS.md § Hosts). The σ-versus-n table above is a property of *this*
container and should be re-measured, not assumed, on any other host.

## Kāra features exercised

- **`Vec[Vec[i64]]` adjacency lists** and **`Vec[Vec[bool]]`** as an adjacency
  matrix for duplicate-edge rejection.
- **`mut ref Vec[i64]` parameters** — `find` compresses the path it walked, so
  the mutation has to travel back out of the call.
- **`continue`** inside a `while`, for the stale-queue-entry skip in the peel.
- **Index-pool FIFO** (`Vec` + head cursor) in two different algorithms.
- **Fisher–Yates over `Vec[Vec[i64]]`** — swapping whole rows, not scalars.

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`; the ★ solver
and the differential match their Python mirrors.

No compiler bugs found — adjacency lists, `mut ref` parameters and index-pool
queues are all well-trodden ground in this corpus.

## Running

```bash
karac run graph_valid_tree.kara
karac run graph_valid_tree_bfs.kara
karac run graph_valid_tree_peel.kara

diff <(karac run graph_valid_tree.kara) <(python3 graph_valid_tree.py) && echo OK
diff <(karac run graph_valid_tree.kara) <(karac run graph_valid_tree_bfs.kara) && echo OK
diff <(karac run graph_valid_tree.kara) <(karac run graph_valid_tree_peel.kara) && echo OK

# 4,000 randomized graphs, three deciders cross-checked
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in graph_valid_tree graph_valid_tree_bfs graph_valid_tree_peel differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```

```bash
# cross-language benchmark (needs hyperfine, rustc, clang, go)
BENCH_OUT=results.container-x86.json bash bench/bench.sh
```
