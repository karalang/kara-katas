# 133. Clone Graph

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Graph, Hash Table, DFS, BFS &nbsp;·&nbsp; **Source:** [leetcode.com/problems/clone-graph](https://leetcode.com/problems/clone-graph/)

Given a reference to a node in a connected undirected graph, return a deep copy of the graph. Each `Node` has an integer `val` (unique, `1..n`) and a list of `neighbors`.

**Constraints:** `0 ≤ n ≤ 100`, `1 ≤ Node.val ≤ 100`, undirected, no self-loops, no duplicate edges, connected when non-empty.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| DFS recursive: clone-on-visit, memoize by val | O(N + M) time, O(N) space | [`dfs.kara`](dfs.kara) ✓ | [`dfs.py`](dfs.py) ✓ |
| BFS iterative: queue + visited map | O(N + M) time, O(N) space | [`bfs.kara`](bfs.kara) ✓ | [`bfs.py`](bfs.py) ✓ |

`✓` marks agreement with the Python mirror under **interpreter, JIT, and codegen** (output). Both variants ship the same per-node work (clone-once, link-once) and the same complexity; BFS just iterates a queue instead of the call stack.

> **A compiler bug this kata surfaced — now fixed.** Originally both variants diverged under `karac build`/JIT (BFS `unwrap()` panic, DFS garbage) while the interpreter was correct. Root cause: [kara `B-2026-07-21-13`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) — pushing a **bare `shared struct` element** aliased from a pool `Vec` into another node's `Vec[Node]` (`nodes[i].neighbors.push(nodes[j])` — the canonical adjacency-list build) was **not RC-retained**, so when the local pool `Vec` dropped (the function returns one node) the still-referenced neighbor was freed → use-after-free. **Fixed** (`share_shared_struct_ref_for_arg`, the bare-`shared` sibling of the existing `Option[shared]` push-retain): `karac build`/JIT now match the interpreter and the Python mirror on **all** cases. Not worked around in the kata — the natural adjacency-list construction correctly exposed the missing retain.
>
> **Residual — inherent RC limitation (not a bug).** The cloned graph's `neighbors` are **strong** `Vec[Node]` edges, so a graph with a cycle (e.g. the default 4-cycle) forms a strong reference cycle that reference counting cannot reclaim — it leaks by construction, the graph analog of the [#141](../141-linked-list-cycle/) linked-list cycle. Output is correct on every case; only the memory of the cyclic clones is not freed at exit. The leak-free variant is a **`Vec`-owned pool + `weak` neighbors** (the #141–143 model), tracked as a possible follow-up; acyclic graphs are already fully reclaimed.

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
| [`bench/clone_bfs_par.kara`](bench/clone_bfs_par.kara) | Same per-clone BFS as `clone_bfs.kara`, but the K=500 outer loop is split into **18 par-block branches** (28 × 14 + 27 × 4 = 500) sharing ONE graph through a `frozen` handle — a non-counting borrow, so the 18 readers emit no refcount traffic on the shared structure. Did not compile until 7 Aug 2026 (kara `B-2026-08-01-33`); the gate that refused it is unchanged, and what closed the gap is the `frozen` mode rather than a relaxation. Two deliberate differences from the seq file — an index-cursor `Vec` worklist (what the C mirror does) and graph construction in a helper — both explained in § Runtime — par lane. |
| [`bench/clone_bfs.py`](bench/clone_bfs.py) | Algorithmic mirror — same N, K, graph generator (gated behind `KARA_BENCH_INCLUDE_PY=1`) |
| [`bench/clone_bfs.rs`](bench/clone_bfs.rs) | Algorithmic mirror; uses `Rc<RefCell<Node>>` to mirror Kāra's `shared struct` reference semantics; compiled with `rustc -O`; `black_box(&nodes[0])` keeps LLVM from hoisting the K loop |
| [`bench/clone_bfs.c`](bench/clone_bfs.c) | Algorithmic mirror, hand-rolled manual-memory baseline; compiled with `clang -O3` |
| [`bench/go-seq/clone_bfs/main.go`](bench/go-seq/clone_bfs/main.go) | Algorithmic mirror (GC-managed pointer nodes); compiled with `go build` |

All compiled mirrors print `500` (sum of K root vals = 500 × 1); bench.sh fails loudly on mismatch.

### Runtime — seq lane

Three codegen gaps surfaced while writing this kata blocked the bench path. All landed in karac (details in § Caveats below).

Snapshot — M5 Pro (6 performance + 12 efficiency = 18 cores), 2026-08-08, hyperfine `--warmup 5 --runs 30 --shell=none`. All five single-threaded (95–99% CPU, and 118% for Go's GC); per BENCH.md's two-lane discipline the 18-way par row is reported separately below, not against the single-threaded comparators.

| Run | Mean ± σ | CPU |
|---|---|---|
| c    clone_bfs (manual memory) | **44.7 ± 1.3 ms** | 94.9% |
| **kāra clone_bfs (codegen)** | **182.1 ± 4.0 ms** | 98.8% |
| rust clone_bfs (Rc&lt;RefCell&gt;) | 232.2 ± 3.5 ms | 98.9% |
| rust clone_bfs (overflow-checks=on) | 236.1 ± 8.2 ms | 98.6% |
| go   clone_bfs | 242.8 ± 10.6 ms | 118.3% |

> **Retraction (2026-07-28).** Every figure and claim previously in this section
> was wrong, and wrong in Kāra's favour. It read `kāra 25.1 ms`, "**leads Rust by
> 8.83×**", "leads Go by 9.26×", and "**Kāra also leads C's manual-memory
> mirror**". That 25.1 ms was **not a sequential measurement**: this kata is one
> of the six worst-hit by the harness bug fixed in `8a48c21`, where the
> compile-cost lane rebuilt the kāra binary *without* `KARAC_AUTO_PAR=0` and
> `mv`'d it over the artifact the seq lane times. The seq row was silently
> timing an **auto-parallelised** binary at 1306% CPU. Corrected, it is 185.1 ms
> at 99.0% — a **7.3×** inflation. See [`BENCHMARKS.md`](../../../BENCHMARKS.md)
> § Retracted.

**Kāra leads both Rust builds by 1.27×** (1.30× against the equal-safety twin) — an allocator/hashtable-bound shape where Kāra's open-addressing `Map` with FxHash for `i64` keys and `shared struct` lowering (RC without RefCell borrow checks) beat `HashMap<_, _>` + `Rc<RefCell<_>>`. Rust's overflow-checked twin costs it almost nothing here (232.2 → 236.1 ms), which is the expected result on a pointer-chasing workload with almost no arithmetic to check. Kāra also leads Go by 1.33×.

**Against C, Kāra is 4.07× behind** (44.7 vs 182.1 ms) — the reverse of what this file used to claim. C's manual-memory mirror never refcounts, while Kāra pays RC traffic plus per-node heap bookkeeping on ~5.5M `Map` operations per run. That makes this kata a peer of [#71](../../1-100/71-simplify-path/) rather than an inversion of it: the hand-managed C baseline wins the allocator-bound shapes, and the interesting comparison is Kāra vs the *safe* languages, where it leads both.

> **Two corrections to the paragraph above.**
>
> *Mechanism.* It said C "allocates nodes from a flat bump array." It does not,
> and did not when that was written: [`bench/clone_bfs.c`](bench/clone_bfs.c)'s
> `make_node` takes **two `malloc`s per node** (the `Node` and its neighbour
> array), grows neighbours with `realloc`, and frees each node individually.
> There is no arena. C's advantage here is that it **never refcounts** — the
> real half of the claim — not that it skips the allocator.
>
> *Ratio (history — the table above has since caught up).* The 3.55× this
> paragraph originally quoted came from the 28 Jul 2026 feed. On the 4 Aug 2026
> M5 feed the seq lane read c 43.9 ms, kāra 178.8 ms, rust 230.1 ms, rust
> equal-safety 230.6 ms, go 235.6 ms — **4.07×** behind C, and still leading
> both safe languages. The live feed above reproduces that: the C multiple
> moved, the standing conclusion never did. C's `visited` map was also made
> heap-allocated and growing in `d702247` (31 Jul 2026), which is a separate
> parity correction on the map rather than on node allocation.

### Runtime — par lane (explicit 18-way `par {}`) — **kāra row RESTORED**

| Run | Mean ± σ | CPU | vs kāra |
|---|---|---|---|
| c    clone_bfs (pthreads) | **10.1 ± 0.4 ms** | 981% | 3.56× faster |
| **kāra clone_bfs (`par {}` over `frozen`)** | **35.9 ± 2.1 ms** | 1341% | — |
| rust clone_bfs (rayon) | 36.9 ± 2.4 ms | 1202% | tie |
| go   clone_bfs (goroutines) | 97.2 ± 1.6 ms | 731% | 2.71× slower |

Same snapshot as the seq table above (M5 Pro, 18 cores, hyperfine `--warmup 5
--runs 30 --shell=none`, all four printing the sink `500`).

**Read the rayon row as a tie, not a win.** 35.9 vs 36.9 ms is a 1.0 ms gap
against σ of 2.1 and 2.4 — inside the noise on both sides. Kāra and rayon are
level here; the honest one-line summary of this lane is *C is 3.6× ahead of
both, and both are ~2.7× ahead of Go*.

**Kāra's own seq → par speedup is 5.07×** (182.1 → 35.9 ms) on 18 branches over
18 cores. Note the CPU column: 1341% against C's 981%. Kāra burns ~2.7× the
sequential lane's CPU to buy 5.07× the wall-clock, where C burns ~1.7× to buy
4.4×. Some of that is the 6P/12E split — an efficiency core spends more
CPU-seconds on the same work, and Kāra's 18 branches saturate all of them —
but not obviously all of it, and per-branch allocator contention is the other
candidate. Not chased here; recorded because it is the visible gap between this
lane and C's.

#### What changed, and why the row exists again

This lane read **kāra row WITHDRAWN** from 28 Jul 2026 until 7 Aug 2026, and
[`bench/clone_bfs_par.kara`](bench/clone_bfs_par.kara) was kept in the tree
precisely *because* it did not compile:

```
error[ownership]: shared struct `Node` cannot be accessed from multiple
concurrent tasks (binding `root` reachable from two par-block branches)
```

**That gate is still there and still correct** — nothing about it was relaxed.
A `shared struct` reachable from more than one concurrent branch is a compile
error because `emit_rc_inc` is a plain load/add/store, so even pure **reads**
race on the refcount. What changed is that there is now a way to hand a branch
a handle that *does no counting at all*, which leaves nothing to race:

* **`frozen T`** — a non-owning, **non-counting** parameter mode for a
  deeply-immutable `shared` value. It lowers to a borrow, so the callee emits
  no retain/release; an escape check (`E0511`) pays for that by refusing to let
  the handle outlive its owner.
* **`let g = freeze root;`** — the freeze site, which requires the source to be
  **uniquely bound**. That is why the kata builds its graph inside
  `build_graph`: with `nodes` still live there genuinely *are* other handles to
  the root, and the checker is right to refuse.
* **a local `Vec[Node]` worklist may hold those non-counting handles**, which
  is what makes the traversal expressible iteratively at all.

Tracked as `B-2026-08-01-33` in the kara repo — nine stages from the first
diagnosis to a compiling kata, with the entry corrected several times along the
way (twice by the session that had written the claim being corrected).

#### The result that is not in the table

**Kāra shares one graph across all 18 branches. The Rust mirror cannot.**
`Rc<RefCell<Node>>` is not `Send`, so [`bench/rayon`](bench/rayon/src/main.rs)
has each worker **build its own private copy** of the ring — its header says so
— and the alternative, `Arc`, would put an atomic RMW on every handle clone in
an entirely read-only traversal. Those are the only two answers Rust has, and
they are exactly the Rc-vs-Arc decision Kāra exists to remove. This kata is now
the demonstration: one graph, eighteen readers, **zero** refcount traffic on the
shared structure.

That is an expressiveness result rather than a speed one, and the table is what
it costs: sharing the graph instead of rebuilding it 18× buys a tie, not a lead.
The rebuild rayon pays is small — O(N·deg) once per worker against 500 BFS
clones, order 3–4% of its work — so it does not explain the tie away in either
direction.

#### What is still missing

**C is 3.56× ahead** and that is the standing gap, the same one the sequential
lane has (4.07×). C never refcounts *and* never allocates a `visited` node per
clone through a general allocator; Kāra pays per-node heap bookkeeping on ~5.5M
`Map` operations per run. Closing it is an allocator/`Map` problem, not a
parallelism one — the par lane inherits the sequential gap almost exactly.

Two differences from [`bench/clone_bfs.kara`](bench/clone_bfs.kara) are worth
naming, because neither is a workaround for a compiler gap and both were
checked:

1. **An index-cursor `Vec` worklist instead of `VecDeque` + `pop_front`.** This
   is what the C mirror does (`Node **queue` with `q_head`/`q_tail`), so it
   moves the Kāra lane *toward* algorithm parity. It is also what `frozen`
   supports — `pop_front` returns a value rather than a place, so a
   non-counting handle coming back through it has nothing the escape checker
   can track. Measured on the **sequential** lane, where the queue form is the
   only variable: 181.4 ± 2.9 ms cursor vs 183.8 ± 2.1 ms deque, i.e. within
   noise. The par lane's number is not a queue-change artifact.
2. **Graph construction moved into `build_graph`,** purely so the freeze source
   is uniquely bound. Same generator, same shape.

The BFS itself, the `visited` map of clones, the `.iter()` walk and the sink are
`clone_bfs.kara` verbatim. `visited` holds **clones** — ordinary owned nodes the
branch mutates through — and is not frozen; conflating it with the queue is what
made a tracked reading of this kata's blocker wrong for a day.

The index-pool alternative (`Vec[Vec[i64]]`, indices instead of handles) still
sidesteps RC entirely and is still the corpus idiom for graph work — see
[#222](../../201-300/222-count-complete-tree-nodes/) and
[#234](../../201-300/234-palindrome-linked-list/). It remains a **different
program**, so it belongs as a new approach rather than an edit to this one.

<details>
<summary>History — the withdrawn row, and the wrong claims it rested on</summary>

The row published before the withdrawal read **37.7 ± 2.2 ms**, a dead heat
with rayon and a claimed 4.91× over kāra's own sequential baseline. It was
produced by a **stale pre-gate binary**: the gate landed 13 Jul 2026, and
`bench.sh` only rebuilds when the source or installed `karac` is newer than the
cached binary, so a pre-gate artifact survived. That binary is the one that
died in ~0.8% of runs with SIGSEGV/SIGTRAP — filed as `B-2026-07-28-13`, closed
as a stale-binary artifact rather than a codegen or runtime defect. It was
withdrawn, not re-measured; the number in the table above is a fresh
measurement of a program that compiles.

An earlier version of this section, and of the kata's own header comment,
claimed the two-phase Rc→Arc algorithm made `root` thread-safe across the par
boundary "with no source-level annotation". That was wrong, and the numbers
that rested on it are gone.

The withdrawal note also said, correctly at the time, that the `shared struct`
(RC) tier was shut out of parallelism on **both** surfaces — explicit `par {}`
hard-errored, and auto-par declined any loop body that *materialized* a
shared-typed value. Two later corrections to that: auto-par's decline is
**reported** (`karac query concurrency` names the gate and the reason; a plain
`karac build` prints nothing, but that is true of every auto-par decline), and
a bare field read *through* a handle — `ps[j].v` — always did parallelize,
lowering to a plain deref with no refcount traffic. The practical exclusion was
real; the "silently, on both surfaces" framing was too strong.

</details>

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `go   clone_bfs` | 9.3 MiB |
| `py   clone_bfs` | 33.8 MiB *(05-16 reading; gated)* |
| `c    clone_bfs` | 154.7 MiB |
| `kara clone_bfs (codegen)` | 173.6 MiB |
| `kara clone_bfs (par 18-way)` | 173.9 MiB |
| `rust clone_bfs` | 186.0 MiB |

Kāra's peak is 7% under Rust's — both are dominated by the K=500 leaked Rc cycles (the graph forms 2000-node cycles that Rc cannot collect; same shape between Kāra `shared struct` and Rust `Rc<RefCell>`). The C mirror deliberately reproduces the same leak shape (clones are never freed) and sits ~11% under kāra — the delta is the RC header + Map metadata per node. The par row's overhead vs serial is +0.3 MiB (the eighteen branch stacks + Arc-promoted handle metadata) — negligible. Go and Python land far smaller because their tracing GCs walk the cycles and reclaim them between iterations (Go: 9.3 MiB, CPython: 33.8) — the structural counterpoint to refcounting on cyclic graphs; a faithful Rust impl that wanted bounded RSS would use `Weak` references or an arena (`Vec<Node>` + indices), and the same option is available in Kāra. The Kāra-vs-Rust comparison here is like-for-like.

### Compile elapsed, binary size, compile memory

First measured 2026-06-05 (`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`):

| Compiler | Compile time | Binary size | Compile peak RSS |
|---|---|---|---|
| `clang -O3 clone_bfs.c` | 56.5 ± 0.4 ms | 33.0 KiB | 2.5 MiB |
| **`karac build clone_bfs.kara`** | **85.9 ± 0.7 ms** | **312.4 KiB** | **14.3 MiB** |
| **`karac build clone_bfs_par.kara`** | **105.9 ± 1.7 ms** | **313.7 KiB** | **17.2 MiB** |
| `rustc -O clone_bfs.rs` | 166.3 ± 1.3 ms | 475.7 KiB | 44.5 MiB |

Kāra compiles the seq kata **1.94× faster than `rustc -O`** at **~3.1× lower compile RAM**, with a binary 1.52× smaller. Unlike the ~33 KiB array katas, this binary carries real runtime surface — `Map` (open-addressing + FxHash), `VecDeque`, and the shared-struct RC machinery — which is what the ~279 KiB over the no-runtime floor pays for; the par binary adds the worker/par-block runtime on top (+1.3 KiB). (Vs the 06-05-morning snapshot: all four compile-elapsed rows moved up 4–6 ms together — rustc and clang on unchanged sources — an afternoon environment band, not a karac change. The karac compile-RSS rows moved +1.7 MiB while rustc/clang read flat: the karac binary was reinstalled between snapshots (`a3acedaf`, ~25 commits of SIMD/host-fn/spawn work), the same benign compiler-internal growth band tracked corpus-wide; emitted binaries are unaffected.)

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
