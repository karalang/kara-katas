# 133. Clone Graph

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Graph, Hash Table, DFS, BFS &nbsp;·&nbsp; **Source:** [leetcode.com/problems/clone-graph](https://leetcode.com/problems/clone-graph/)

Given a reference to a node in a connected undirected graph, return a deep copy of the graph. Each `Node` has an integer `val` (unique, `1..n`) and a list of `neighbors`.

**Constraints:** `0 ≤ n ≤ 100`, `1 ≤ Node.val ≤ 100`, undirected, no self-loops, no duplicate edges, connected when non-empty.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| DFS recursive: clone-on-visit, memoize by val | O(N + M) time, O(N) space | [`dfs.kara`](dfs.kara) ✓ via `karac run` | [`dfs.py`](dfs.py) ✓ |
| BFS iterative: queue + visited map | O(N + M) time, O(N) space | [`bfs.kara`](bfs.kara) ✓ via `karac run` | [`bfs.py`](bfs.py) ✓ |

`✓` runs end-to-end today.

### Why a visited map breaks cycles

The graph is undirected so every edge appears twice, and any cycle hits a back-reference on its second visit. Without memoization the recursive clone would unfold forever. Keying the visited map by `val` is cheap and unambiguous (LeetCode guarantees unique vals); a more general implementation would key by node identity, but Kāra's shared-struct equality is opt-in and the val key is sufficient for this problem.

```
clone_graph(root):
    if root is None: return None
    visited = {}             # val → cloned-node
    dfs(root, visited)

dfs(node, visited):
    if node.val in visited:
        return visited[node.val]
    copy = Node(node.val, neighbors=[])
    visited[node.val] = copy
    for nb in node.neighbors:
        copy.neighbors.push(dfs(nb, visited))
    return copy
```

The BFS variant is structurally the same — it just iterates a queue instead of the call stack. Both ship the same per-node work (clone-once, link-once) and the same complexity.

## Kāra features exercised

- **`shared struct Node { val: i64, mut neighbors: Vec[Node] }`** — self-referential RC-backed graph node with a mutable adjacency list. Mutability on the field is what lets the cloned node's neighbors be appended to *after* the node has been inserted into the visited map.
- **`Map[i64, Node]` for memoization** — keys the clone-cache by val. The shared-struct value semantics mean re-fetching `visited.get(node.val).unwrap()` returns another RC handle to the same heap object, so mutations through the re-fetched handle are visible to every other handle.
- **`VecDeque[Node]`** (BFS variant) — `push_back` / `pop_front` for level-order traversal.
- **`Option[Node]` return shape** — the LeetCode signature already returns a nullable handle; the empty-graph case threads through cleanly.
- **`for` over `Vec.iter()`, `match` on `Option`, `if let` destructuring** — standard traversal idioms.

## API shape

Each solution exposes `clone_graph(root: Option[Node]) -> Option[Node]` plus a small test harness (`build_graph`, `print_graph`, `report`). `main` calls `report` per test case. The Python files mirror the same names so the files diff line-for-line.

## Output format

Each `report` BFS-walks the *cloned* graph and emits `val: [neighbor_vals]` per line, with `---` between test cases. The BFS order is deterministic (push neighbors in stored order, mark visited by val), so DFS-clone and BFS-clone produce identical output for every input.

```
1: [2, 4]
2: [1, 3]
4: [1, 3]
3: [2, 4]
---
1: []
---
(empty)
---
1: [2]
2: [1]
---
1: [2]
2: [1, 3]
3: [2, 4]
4: [3]
---
```

## Running

```bash
# Kāra
karac run dfs.kara
karac run bfs.kara

# Python
python3 dfs.py
python3 bfs.py
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup)
./bench/bench.sh
```

`bench/bench.sh` builds the Rust file with `rustc -O` (cached in `bench/target/`, gitignored) and runs `hyperfine --warmup 5 --runs 30` against a 10-regular ring graph of `N = 2_000` nodes (val 1..N, neighbors at `i±1..i±5 mod N`), cloning the graph `K = 500` times per process. Sink is `sum of cloned root.val` across the K iterations so the optimizer cannot elide the call.

| File | What it does |
|---|---|
| [`bench/clone_bfs.kara`](bench/clone_bfs.kara) | N=2000, K=500. Serial baseline mirroring `clone_bfs.rs` line-for-line — `curr_clone` hoisted out of the inner for-nb loop to match Rust's shape. |
| [`bench/clone_bfs_par.kara`](bench/clone_bfs_par.kara) | Same per-clone BFS as `clone_bfs.kara`, but the K=500 outer loop is split into **8 par-block branches** (62 × 7 + 66 = 500). M1 has 4 perf + 4 efficiency cores; the two-phase Rc→Arc algorithm promotes shared-struct handles when they escape across the par barrier. |
| [`bench/clone_bfs.py`](bench/clone_bfs.py) | Algorithmic mirror — same N, K, graph generator |
| [`bench/clone_bfs.rs`](bench/clone_bfs.rs) | Algorithmic mirror; uses `Rc<RefCell<Node>>` to mirror Kāra's `shared struct` reference semantics; compiled with `rustc -O`; `black_box(&nodes[0])` keeps LLVM from hoisting the K loop |

Both Rust and Python print `500` (sum of K root vals = 500 × 1).

### Codegen vs Rust — **landed**

Three codegen gaps surfaced while writing this kata blocked the bench path. All three landed in karac; the headline `kara codegen` row now sits at the top of the table (details in § Caveats below).

Snapshot — M1, 2026-05-16, hyperfine `--warmup 5 --runs 30 --shell=none`:

| Workload | Kāra (par 8-way) | Kāra (codegen) | Rust (Rc&lt;RefCell&gt;) | Python (CPython) | Kāra par : Rust |
|---|---|---|---|---|---|
| `clone_bfs` (N=2000, K=500) | **35.0 ± 1.3 ms** | 155.0 ± 2.2 ms | 230.1 ± 1.8 ms | 599.0 ± 5.2 ms | **6.58× faster** |

The serial codegen row is 48% faster than Rust on its own — allocator/hashtable-bound shape where Kāra's open-addressing `Map` with FxHash for `i64` keys and `shared struct` lowering (RC without RefCell borrow checks) win against `HashMap<_, _>` + `Rc<RefCell<_>>`. The 8-way par row then folds in the K=500 outer loop's iteration-level parallelism: K clones are independent (each builds its own `visited` Map and `queue` VecDeque), so an explicit `par {}` fork-join with 8 branches lets all eight M1 cores work. The two-phase Rc→Arc algorithm promotes `shared struct Node` handles to Arc automatically when they escape across the par boundary — no source-level annotation. Effective parallel speedup is ~4.4× (8-branch fork-join, not 8× linear because of branch-startup cost, Arc atomics, and the perf/efficiency-core split).

`karac run clone_bfs.kara` (tree-walk interpreter) completes the same workload in ~527 s on the same hardware — ~2400× slower than Rust. That row is dropped from the table for the same reason 1-two-sum drops `kara brute_force (interp)`: it measures interpreter dispatch, not algorithm cost.

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara clone_bfs (par 8-way)` | 172.3 MiB |
| `kara clone_bfs (codegen)` | 171.0 MiB |
| `py   clone_bfs` | 33.8 MiB |
| `rust clone_bfs` | 185.8 MiB |

Kāra's peak is 8% under Rust's — both are dominated by the K=500 leaked Rc cycles (the graph forms 2000-node cycles that Rc cannot collect; same shape between Kāra `shared struct` and Rust `Rc<RefCell>`). The par row's overhead vs serial is +1.3 MiB (the eight branch stacks + Arc-promoted handle metadata) — negligible. Python's number is much smaller because CPython's tracing GC walks the cycles and reclaims them between iterations; a faithful Rust impl that wanted bounded RSS would use `Weak` references or an arena (`Vec<Node>` + indices), and the same option is available in Kāra. The Kāra-vs-Rust comparison here is like-for-like.

## Caveats surfaced while writing this kata

Two parser bugs were uncovered and fixed in `karac` (`src/parser.rs`) as part of this slice:

1. **`break` / `return` as a non-block match arm body.** `parse_break_args` / the `Return` arm only treated `;` and `}` as "no value" terminators, so `None => break,` parsed as `break` followed by an unexpected comma. Now `,` is also a terminator.
2. **Block-bodied match arm followed by another arm.** `parse_match_expr` broke out of the arm loop after any arm whose body didn't end with a comma — but Rust-style match grammar makes the trailing comma *optional* after a `{}` block body. Now the loop only breaks when the previous arm was non-block.

The two fixes unblock multiple existing examples that were stuck on the same shape (`course_schedule.kara`, `max_depth_binary_tree.kara`, `lru_cache.kara`, `merge_sorted_lists.kara` all parse again afterwards).

Three pre-existing typechecker warnings remain (orthogonal to this kata; flagged here so they're not silently absorbed):

- `expected 'mut ref Map<i64, Node>', found 'Map<i64, Node>'` at the call-site for a `dfs(n, mut visited)` pass — the call-site `mut` marker doesn't currently propagate the parameter mode for `mut ref T` (it works for `mut Slice[T]`). Same warning fires in `course_schedule.kara`.
- `expected 'Vec<i64>', found 'Vec<?T1>'` on the empty-graph test case's outer `Vec.new()` annotation — the constructor inference issue noted in the v62 brainstorm where empty-Vec element typevars don't propagate from the annotation back to the constructor call.
- `Option is implicitly #[must_use]` on `Map.insert(...)` returns when the prior value isn't needed — silenced in this kata with `let _ = visited.insert(...)`.

Codegen blockers and enablers (see § Codegen vs Rust — landed above). Bugs 1–4 blocked the kata from compiling or running at all; 5–6 unblocked the **par 8-way** bench row by closing receiver-dispatch and par-block branch-binding gaps.

- **Landed** in [`6b44c54`](../../../../karac-rust/src/codegen/calls.rs) — `compile_method_call` FieldAccess-receiver arm (FR slice, sibling to MR). `obj.field.method(...)` now dispatches for both shared and plain structs via a synth-identifier route through the existing identifier-receiver flow.
- **Landed** in [`0439a5f`](../../../../karac-rust/src/codegen/calls.rs) — `Option`/`Result` `unwrap` / `expect` / `is_some` / `is_none` / `is_ok` / `is_err` codegen surface (new receiver-shape-agnostic arm + Index→FieldAccess→method dispatch chains). The `visited.get(curr.val).unwrap()` shape now compiles end-to-end.
- **Landed** in [`9e2a71c`](../../../../karac-rust/src/codegen/types_lowering.rs) — `VecDeque[T]` type-lowering registered with the right `{ptr, len, cap}` shape (was hitting i64's default, overflowing 16 bytes into adjacent `Map` handle's alloca) plus effect-seeds for VecDeque mutating methods so auto-par captures them by reference. The "let-bound `SharedStruct{...}` + `Map.insert(k, x)` followed by additional inserts hangs at runtime" symptom resolved as a side-effect of the layout fix.
- **Landed** in [`394cd64`](../../../../karac-rust/src/codegen/control_flow_for.rs) — for-loop struct-binding registration (struct-typed `x` in `for x in xs.iter() { ... x.val ... }` was folding to constant 0 because `var_type_names` wasn't populated for for-bindings) plus `obj.field.iter()` for-receiver dispatch (the inner `for nb in curr.neighbors.iter()` body was silently never emitted). Both gaps prevented the BFS body from actually executing once the queue advanced past iter 1.
- **Landed** in [`3c69c5c`](../../../../karac-rust/src/codegen/functions.rs) — `ref T` / `mut ref T` collection parameter receiver method dispatch. Unified the per-shape ad-hoc param registration cascade through `register_var_from_type_expr`; made Map/Set handle loads ref-aware via a `get_data_ptr` helper; routed the typechecker's stdlib named-type checks through a derefed view. Incidentally unblocks `mut ref Set[T]`, `mut ref VecDeque[T]`, `mut ref String` as parameter types — broader receiver-dispatch coverage. Surfaced while attempting a recursive DFS variant of this kata.
- **Landed** in [`f9ff988`](../../../../karac-rust/src/codegen/par_blocks.rs) — explicit `par {}` block-result + branch-binding propagation. `compile_par_block` was passing an empty `return_slots` list and unconditionally returning `i64 0` regardless of the block's final expression; branches' `let` bindings stayed branch-local and the join expression's identifier reads found nothing. The slot mechanism already existed for the auto-par dispatch path — the explicit-par path just hadn't engaged it. With this in, `bench/clone_bfs_par.kara` builds, runs, and shows the 4.43× iteration-parallelism speedup over serial.

One adjacent bug (#7) noted but not yet fixed: a Map+shared-struct refcount/ownership interaction where returning an owned `Node` from a helper while discarding the local `Map` (which holds the only other RC reference) hangs at runtime. Independent of bugs 1–6; not blocking any existing bench row. Minimal repros saved alongside the bug-5 work; intended for a follow-up slice.
