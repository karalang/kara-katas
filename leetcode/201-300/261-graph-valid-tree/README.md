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
