# 133. Clone Graph

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Graph, Hash Table, DFS, BFS &nbsp;·&nbsp; **Source:** [leetcode.com/problems/clone-graph](https://leetcode.com/problems/clone-graph/)

Given a reference to a node in a connected undirected graph, return a deep copy of the graph. Each `Node` has an integer `val` (unique, `1..n`) and a list of `neighbors`.

**Constraints:** `0 ≤ n ≤ 100`, `1 ≤ Node.val ≤ 100`, undirected, no self-loops, no duplicate edges, connected when non-empty.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| DFS recursive: clone-on-visit, memoize by val | O(N + M) time, O(N) space | [`dfs.kara`](dfs.kara) ✓ via `karac run` | [`dfs.py`](dfs.py) ✓ |
| BFS iterative: queue + visited map | O(N + M) time, O(N) space | [`bfs.kara`](bfs.kara) ✓ via `karac run` | [`bfs.py`](bfs.py) ✓ |

`✓` runs end-to-end today. Both variants ship the same per-node work (clone-once, link-once) and the same complexity; BFS just iterates a queue instead of the call stack.

## Kāra features exercised

- **`shared struct Node { val: i64, mut neighbors: Vec[Node] }`** — self-referential RC-backed node; mutable adjacency lets neighbors be appended *after* insertion into the visited map.
- **`Map[i64, Node]` memoization** — re-fetching a stored handle returns another RC alias to the same heap object, so mutations are visible across handles. Since the 2026-06 refcount fixes the sources use the *natural* alias discipline: insert a handle, keep using the original binding, return it while the map is discarded (this exact shape was bug #7's runtime hang — see § Caveats).
- **`VecDeque[Node]`** (BFS variant) — `push_back` / `pop_front` for level-order traversal.
- **`Option[Node]` return shape** — LeetCode's nullable handle threads the empty-graph case cleanly.

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

`bench/bench.sh` builds the Rust file with `rustc -O`, the C file with `clang -O3`, the Go mirror with `go build`, and both Kāra files with `karac build` (all cached in `bench/target/`, gitignored), then runs `hyperfine --warmup 5 --runs 30` against a 10-regular ring graph of `N = 2_000` nodes (val 1..N, neighbors at `i±1..i±5 mod N`), cloning the graph `K = 500` times per process. Sink is `sum of cloned root.val` across the K iterations so the optimizer cannot elide the call.

| File | What it does |
|---|---|
| [`bench/clone_bfs.kara`](bench/clone_bfs.kara) | N=2000, K=500. Serial baseline mirroring `clone_bfs.rs` line-for-line — `curr_clone` hoisted out of the inner for-nb loop to match Rust's shape; returns the held `root_clone` alias directly (natural post-bug-7 shape, see § Caveats). |
| [`bench/clone_bfs_par.kara`](bench/clone_bfs_par.kara) | Same per-clone BFS as `clone_bfs.kara`, but the K=500 outer loop is split into **18 par-block branches** (28 × 14 + 27 × 4 = 500), one per core on M5 Pro. The two-phase Rc→Arc algorithm promotes shared-struct handles when they escape across the par barrier. |
| [`bench/clone_bfs.py`](bench/clone_bfs.py) | Algorithmic mirror — same N, K, graph generator (gated behind `KARA_BENCH_INCLUDE_PY=1`) |
| [`bench/clone_bfs.rs`](bench/clone_bfs.rs) | Algorithmic mirror; uses `Rc<RefCell<Node>>` to mirror Kāra's `shared struct` reference semantics; compiled with `rustc -O`; `black_box(&nodes[0])` keeps LLVM from hoisting the K loop |
| [`bench/clone_bfs.c`](bench/clone_bfs.c) | Algorithmic mirror, hand-rolled manual-memory baseline; compiled with `clang -O3` |
| [`bench/go-seq/clone_bfs/main.go`](bench/go-seq/clone_bfs/main.go) | Algorithmic mirror (GC-managed pointer nodes); compiled with `go build` |

All compiled mirrors print `500` (sum of K root vals = 500 × 1); bench.sh fails loudly on mismatch.

### Runtime — seq lane

Three codegen gaps surfaced while writing this kata blocked the bench path. All landed in karac (details in § Caveats below).

Snapshot — M5 Pro (6 performance + 12 efficiency = 18 cores), 2026-06-05, hyperfine `--warmup 5 --runs 30 --shell=none`. All four single-threaded; per BENCH.md's two-lane discipline the 18-way par row is reported separately below, not against the single-threaded comparators.

| Run | Mean ± σ |
|---|---|
| c    clone_bfs (manual memory) | 44.6 ± 1.0 ms |
| **kāra clone_bfs (codegen)** | **147.3 ± 2.8 ms** |
| rust clone_bfs (Rc&lt;RefCell&gt;) | 217.6 ± 1.5 ms |
| go   clone_bfs | 241.7 ± 4.3 ms |

> **Post-rewrite re-bench (same day).** This snapshot is the first since the kāra sources were rewritten to the natural shared-struct shape (return the held `root_clone` alias instead of a final `visited.get` re-fetch — see § Caveats, bug #7 resolved). Kāra's −2.7% vs the morning reading is mostly batch: rust and C moved −1.2%/−1.1% on **byte-identical, not-even-rebuilt binaries**, and the residual is within σ. The natural shape costs nothing — it removes only K=500 Map lookups out of ~5.5 M per run.

**Kāra leads Rust by 1.48×** — allocator/hashtable-bound shape where Kāra's open-addressing `Map` with FxHash for `i64` keys and `shared struct` lowering (RC without RefCell borrow checks) win against `HashMap<_, _>` + `Rc<RefCell<_>>` — and leads Go by 1.64×. C's manual-memory mirror (no RC, no per-node heap bookkeeping) is 3.30× ahead of kāra — the algorithmic floor for this shape, same role as kata [#71](../../1-100/71-simplify-path/)'s stack-buffer C mirror. (The 2026-05-16 snapshot read kāra 155.6 ± 7.5 / rust 230.2 ± 2.5; the 06-05-morning one 151.4 ± 2.5 / 220.3 ± 1.5 — all reproduce within ~3–4%. Python's 588.3 ms reading is from 05-16 — the py mirror is gated off by default at today's K.)

### Runtime — par lane (explicit 18-way `par {}`)

| Run | Mean ± σ | User | User / wall |
|---|---|---|---|
| `kara clone_bfs` (par 18-way) | 23.1 ± 0.7 ms | 258.6 ms | 11.2× |

**6.4× faster than kāra's own seq baseline** (147.3 → 23.1 ms) — the intra-Kāra seq→par speedup, reported within-lane per BENCH.md (the 05-16 snapshot's headline "10.16× faster than Rust" was a cross-lane ratio and is retired; the honest decomposition is 1.46× codegen × ~6.6× parallelism). K clones are independent (each builds its own `visited` Map and `queue` VecDeque), so an explicit `par {}` fork-join with 18 branches lets every core on M5 Pro work. The two-phase Rc→Arc algorithm promotes `shared struct Node` handles to Arc automatically when they escape across the par boundary — no source-level annotation. Not 18× linear: branch-startup cost, Arc atomics, hash-table contention on shared input, and the 6-perf-vs-12-efficiency core asymmetry each take a slice. A sweep at K=500 / N ∈ {6, 8, 12, 18, 24} on the same hardware identified N=18 as the optimum; N=24 regresses ~5% from oversubscription. (05-16 read 22.7 ± 1.4 — reproduces within σ; this allocator-contention-bound shape sees no June-scheduler-archive win, same as kata [#71](../../1-100/71-simplify-path/)'s malloc-bound auto-par lane.)

`karac run clone_bfs.kara` (tree-walk interpreter) completes the same workload in hundreds of seconds on the same hardware — orders of magnitude slower than Rust. That row is dropped from the table for the same reason 1-two-sum drops `kara brute_force (interp)`: it measures interpreter dispatch, not algorithm cost.

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `go   clone_bfs` | 9.4 MiB |
| `py   clone_bfs` | 33.8 MiB *(05-16 reading; gated)* |
| `c    clone_bfs` | 154.7 MiB |
| `kara clone_bfs (codegen)` | 170.5 MiB |
| `kara clone_bfs (par 18-way)` | 173.5 MiB |
| `rust clone_bfs` | 185.8 MiB |

Kāra's peak is 8% under Rust's — both are dominated by the K=500 leaked Rc cycles (the graph forms 2000-node cycles that Rc cannot collect; same shape between Kāra `shared struct` and Rust `Rc<RefCell>`). The C mirror deliberately reproduces the same leak shape (clones are never freed) and sits ~9% under kāra — the delta is the RC header + Map metadata per node. The par row's overhead vs serial is +3.3 MiB (the eighteen branch stacks + Arc-promoted handle metadata) — negligible. Go and Python land far smaller because their tracing GCs walk the cycles and reclaim them between iterations (Go: 9.4 MiB, CPython: 33.8) — the structural counterpoint to refcounting on cyclic graphs; a faithful Rust impl that wanted bounded RSS would use `Weak` references or an arena (`Vec<Node>` + indices), and the same option is available in Kāra. The Kāra-vs-Rust comparison here is like-for-like.

### Compile elapsed, binary size, compile memory

First measured 2026-06-05 (`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`):

| Compiler | Compile time | Binary size | Compile peak RSS |
|---|---|---|---|
| `clang -O3 clone_bfs.c` | 59.4 ± 3.1 ms | 33.0 KiB | 2.5 MiB |
| **`karac build clone_bfs.kara`** | **84.0 ± 0.8 ms** | **278.8 KiB** | **12.7 MiB** |
| **`karac build clone_bfs_par.kara`** | **93.3 ± 2.2 ms** | **313.1 KiB** | **14.1 MiB** |
| `rustc -O clone_bfs.rs` | 158.4 ± 2.0 ms | 475.7 KiB | 44.1 MiB |

Kāra compiles the seq kata **1.89× faster than `rustc -O`** at **~3.5× lower compile RAM**, with a binary 1.71× smaller. Unlike the ~33 KiB array katas, this binary carries real runtime surface — `Map` (open-addressing + FxHash), `VecDeque`, and the shared-struct RC machinery — which is what the ~246 KiB over the no-runtime floor pays for; the par binary adds the worker/par-block runtime on top (+34 KiB). (Vs the 06-05-morning snapshot: all four compile-elapsed rows moved up 4–6 ms together — rustc and clang on unchanged sources — an afternoon environment band, not a karac change. The karac compile-RSS rows moved +1.7 MiB while rustc/clang read flat: the karac binary was reinstalled between snapshots (`a3acedaf`, ~25 commits of SIMD/host-fn/spawn work), the same benign compiler-internal growth band tracked corpus-wide; emitted binaries are unaffected.)

On byte-identity: rust and C were not rebuilt (sources untouched — same artifacts, hashes verified identical); Go rebuilt same-size/different-bytes (embedded build IDs, as everywhere in the corpus). The kāra binaries rebuilt at +32 B (seq) / +192 B (par) vs the morning artifacts — the natural-shape source rewrite (§ Caveats) plus the karac reinstall; both deltas are noise-scale against the 278.8/313.1 KiB totals.

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

**Bug #7 — RESOLVED (2026-06-05).** The adjacent Map+shared-struct refcount/ownership interaction — returning an owned `Node` from a helper while discarding the local `Map` (which held the only other RC reference) hung at runtime — no longer reproduces: the 2026-06 shared-struct refcount fixes (karac `a98149b9` + `fca1e3ea`, driven by kata [#21](../../1-100/21-merge-two-sorted-lists/)) killed it incidentally. Verified two ways: a minimal repro (insert handle into a local Map, mutate through the original binding, return it, discard the Map) builds and runs clean under both `karac run` and `karac build`; and all four kāra sources in this kata were **rewritten to the natural shape** the bug used to forbid — `dfs.kara` pushes through and returns its held `copy` binding, `bfs.kara` / both bench mirrors return the held `root_clone` alias, and `bfs.kara` hoists `curr_clone` out of the neighbor loop — with outputs identical, all sinks agreeing at 500, and wall time within batch noise (the natural shape costs nothing; see § Runtime).

One new gap surfaced *by the bug-7 verification probe* (2026-06-05, filed in karac's bug tracker): **indexing a `Vec` field through a shared-struct handle fails codegen** — `n.neighbors[0]` errors `Index operator applied to non-array type` under `karac build` while `karac run` evaluates it fine. Iteration and method calls through the same place work, so this kata never hits it (the BFS/DFS bodies iterate, never index); a `let first = n.neighbors[0]` shape would. Not blocking any bench row.
