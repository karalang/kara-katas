# 99. Recover Binary Search Tree

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Tree · Depth-First Search · Binary Search Tree · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/recover-binary-search-tree](https://leetcode.com/problems/recover-binary-search-tree/)

Exactly two nodes of a binary *search* tree had their values swapped by mistake. **Recover the tree without changing its structure** — only the two misplaced values move back.

The key fact both solvers lean on: an inorder walk of a *correct* BST visits values in strictly ascending order. The mistake shows up as (at most two) places where a value is followed by a smaller one.

```
    3               2
   / \             / \
  1   4    ->     1   4     (3 and 2 were swapped; recover puts them back)
     /               /
    2               3
```

**Constraints:** `1 ≤ #nodes ≤ 1000`, node values fit a signed 32-bit int.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Inorder scan + swap the descent pair** ★ | [`recover.kara`](recover.kara) ✓ | [`recover.py`](recover.py) ✓ |
| **Sort inorder values + write back mismatches** | [`recover_sort.kara`](recover_sort.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for both approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the two Kāra approaches agree with **each other** and with the Python mirror. An independent **ground-truth check** confirms the recovery: for every test tree, the corruption genuinely changes the tree, and after recovery the tree is (a) a valid BST — its inorder is sorted — and (b) **byte-identical to the pre-corruption original**. Both solvers compile with zero diagnostics.

## Two ways to find the two nodes

Both collect the nodes in inorder (a `Vec[TreeNode]` of shared handles) and then fix the values in place; they differ in how they locate the pair.

**Inorder descent scan** ([`recover.kara`](recover.kara), the ★): sweep the inorder list once, watching for a value followed by a smaller one — a "descent". With one descent (the swapped nodes are adjacent) the pair is that neighbour; with two descents (non-adjacent) the culprits are the *earlier* descent's left node and the *later* descent's right node. Swap those two values. O(n) after the walk.

**Sort + positional compare** ([`recover_sort.kara`](recover_sort.kara)): take a sorted copy of the inorder values — that is exactly what each position *should* hold — and write the sorted value back into any node whose current value disagrees. Only the two swapped nodes differ from sorted order, so only their values move. A distinct mechanism (a full `Vec.sort()` + compare, rather than descent-spotting) that must land on the identical result.

### A codegen bug this kata surfaced

The most textbook third approach — a **recursive** inorder that threads the running `prev` / `first` / `second` node handles through the recursion as `mut ref Option[TreeNode]` parameters — is **correct on the interpreter but miscompiles** (SIGSEGV on `karac build`, wrong result on `karac run`). Assignment through a `mut ref Option[shared]` parameter doesn't write back to the caller under codegen; the store lands in a callee-local copy. Per the repo's "never route around — fix or file it" rule, that gap is filed as [`B-2026-07-12-3`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) with a minimal repro, and this kata ships the two solvers above, which keep the running state **local** (a collected `Vec` + local indices) and are byte-identical across every surface.

## Kāra features exercised

- **`shared struct TreeNode` (RC) with mutable fields** — `mut val` / `mut left` / `mut right`; the recovery *mutates node values in place* through shared `Vec[TreeNode]` handles collected from the tree, so a value written via one handle is seen through the tree — the reference semantics `shared` exists for. Node type mirrors kata [#94](../94-binary-tree-inorder-traversal/) / [#95](../95-unique-binary-search-trees-ii/) / [#98](../98-validate-binary-search-tree/).
- **`Vec[TreeNode]` of shared nodes + index-assign** — `nodes[i].val = x` writes a field of a shared node reached by Vec index (the same `Vec`-of-shared surface the [#95](../95-unique-binary-search-trees-ii/) RC fixes hardened).
- **`Vec.sort()`** — the sort-based variant sorts a `Vec[i64]` copy of the values.
- **Reused shared tree (RC)** — `root` is threaded through `corrupt` → `recover` → `serialize`; because a `shared` tree is reference-counted, the reuse is an RC handle (the compiler notes the RC fallback, which is exactly correct here).

**v1 note.** Trees stay within the `≤ 1000`-node constraint. The sink folds each recovered tree's preorder serialization into a running polynomial hash. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the recover-to-original ground truth.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   recover.kara
karac build recover.kara && ./recover

# The sort-based variant (identical output):
karac run recover_sort.kara

# Python
python3 recover.py

# Verify they all agree
diff <(karac run recover.kara) <(python3 recover.py)        && echo OK
diff <(karac run recover.kara) <(karac run recover_sort.kara) && echo OK
```

## Benchmarks
Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`recover.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5 re-bench (2026-11-01).** Canonical numbers measured on the corpus's **Apple M5 Pro** (6P+12E, Darwin 25.6.0; **karac g6697158fa** (0.9.0-dev.14057, the v2/MIR backend; the legacy backend was deleted 2026-10-23), `rustc 1.95.0`, Apple clang 21.0.0, `go 1.26.3`, hyperfine 1.20) — [`bench/results.json`](bench/results.json). Against the 2026-07-12 legacy-backend snapshot kāra gained on every comparator: kāra/Rust 0.96× → 0.78×, kāra/C 2.59× → 2.12×, kāra/Go 1.51× → 1.20× (the comparators ran 13–16 % slower this session, so the ratios, not the milliseconds, carry the comparison). A shared x86-64 Linux cloud-container reference run is kept alongside in [`bench/results.container-x86.json`](bench/results.container-x86.json); absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. Unlike its alloc-heavy siblings, this kata's cross-language *ordering* is **identical** on both hosts — see the note below the table.

**Workload.** Build a 31-node BST once, then **K = 700,000** reps of: **corrupt** (swap two node values at inorder indices `a = acc%n`, `b = (acc*7+3)%n`), **fold** the corrupted tree's inorder into the running hash, **recover** (the ★ descent scan). The indices are **data-dependent** (seeded by the hash), so nothing hoists — and because `recover` must correctly restore the tree for the *next* rep's corruption to match, the sink verifies the recovery, not just the corruption. Each mirror uses its natural shared-mutable node and allocates the collect buffer per call (Kāra `Vec.new`, C `malloc`/`free`, Rust `Vec`, Go `make`); **Rust uses `Rc<RefCell<Node>>`** to match Kāra's `shared struct` — reference-counted + interior-mutable — the honest representation for collecting node handles and mutating their values. All five compiled mirrors must agree on `331731322` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded, ~99.8 % CPU (the default build emits no call of `karac_mir_task_spawn`, verified in the emitted IR (`KARAC_MIR_LL`), same as its `KARAC_AUTO_PAR=0` twin). **Apple M5 Pro numbers, karac g6697158fa, 2026-11-01.**

| Implementation | Wall time | Node representation |
|---|---|---|
| c    recover (clang -O3)                            | 145.2 ± 4.2 ms | raw `malloc` pointer |
| go   recover (GC)                                   | 256.4 ± 1.5 ms | GC `*Node` |
| **kāra recover**                                    | **307.6 ± 11.4 ms** | **`shared` (RC)** |
| rust recover (rustc -O, overflow-checks=on)          | 392.9 ± 10.8 ms | `Rc<RefCell>` |
| rust recover (rustc -O)                             | 393.1 ± 13.3 ms | `Rc<RefCell>` |

**Kāra beats its closest semantic peer — and the M5 keeps the ordering identical.** The honest match for Kāra's `shared struct TreeNode` — reference-counted *and* interior-mutable — is Rust's `Rc<RefCell<Node>>`, and against it Kāra is ahead on the M5 (**1.28×**, 308 vs 393 ms; the two Rust builds tie, so equal safety changes nothing): collecting node handles bumps a refcount on every `clone`, and `Rc<RefCell>` layers a runtime borrow-flag check on top of that count on every `borrow()`/`borrow_mut()`, which Kāra's leaner RC handle avoids. On the legacy backend the margin had narrowed from the container's 1.13× to 1.04× (2026-07-12) — on the M5's wide core the extra borrow-flag branch is cheaper to predict, so it costs Rust less; the v2/MIR backend widened it to 1.28×. The gap runs the other way against the representations that carry *no* per-access ownership bookkeeping: **C's raw `malloc` pointer tree** (145 ms, **2.12×**) is the metal floor with zero refcount, and **Go's GC `*Node`** (256 ms, **1.20×**) chases pointers with the count deferred to the collector. So the ordering is exactly by per-node-access overhead — raw pointer < GC pointer < **Kāra RC** < `Rc<RefCell>` — and it is **byte-for-byte the same on both hosts**: where the alloc-heavy siblings inverted on the M5 (#94's Go flipped last→first, #96's C flipped slowest→fastest), this per-node-*access*-bound kata is stable, because there is no per-rep allocation churn for the M5's allocator to speed up — the 31-node tree is built once and only the collect buffer (43 M `Vec[shared]` push/drop pairs over the run) turns over. Those RC inc/decs are exactly why C and Go pull *further* ahead here on fast cores (their no-per-access-count advantage compounds) while kāra holds its place against Rust. Verified correct **and** MallocScribble-clean over the run. Python is listed at **166 ms (last measured 2026-07-12, not re-run) but ran K = 30,000 — 1/23 of the compiled iterations** (pure-Python recursion is ~23× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **1.08 MiB** peak RSS (parity with C's 1.05 and Rust's 1.09 MiB) vs Go's **9.5 MiB**. Binary size: c 32.8 KiB, **kāra 295.8 KiB**, rust 457.0 KiB, go 2.39 MiB; every MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB, tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). This is the RC-vs-`Rc<RefCell>` regime of the tree siblings ([#92](../92-reverse-linked-list-ii/), [#95](../95-unique-binary-search-trees-ii/), [#98](../98-validate-binary-search-tree/)), landing kāra ahead of Rust because the workload's shared-mutable-node shape forces Rust into `Rc<RefCell>` rather than a bare `Box`.

Compile-cold on the M5 is clang 49.2 ms < rustc 114.9 ms < **karac 125.7 ms** (2.6× clang, 1.09× rustc). Compile-cold, binary size, and peak-RSS records are in [`bench/results.json`](bench/results.json) (M5, canonical) and [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched **reference-counted interior-mutable** node representation (`shared struct` vs `Rc<RefCell>`), the honest comparison for a collect-shared-nodes-and-mutate workload. C's raw `malloc` pointer tree is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
