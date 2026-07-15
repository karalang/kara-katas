# 106. Construct Binary Tree from Inorder and Postorder Traversal

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Hash Table · Divide and Conquer · Tree · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal](https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/)

Given `inorder` and `postorder` traversals of a binary tree with **distinct** values, reconstruct the tree. The end-of-array sibling of [#105](../105-construct-binary-tree-from-preorder-and-inorder-traversal/): postorder is `left, right, root`, so its **last** element is the root.

```
inorder   = [9, 3, 15, 20, 7]         3
postorder = [9, 15, 7, 20, 3]        / \
                                     9  20
   postorder[last]=3 is the root;      / \
   3 splits inorder into [9] (left)   15  7
   and [15,20,7] (right).
```

**Constraints:** `1 ≤ #nodes ≤ 3000`, node values are distinct and fit `-3000 … 3000`, and the two arrays are genuine inorder/postorder traversals of the *same* tree.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Recursive index-bounds split** ★ | [`build_tree.kara`](build_tree.kara) ✓ | [`build_tree.py`](build_tree.py) ✓ |
| **Recursive with a single postorder cursor (from the end)** | [`build_tree_cursor.kara`](build_tree_cursor.kara) ✓ | — |
| **Iterative stack (O(n), no search)** | [`build_tree_iter.kara`](build_tree_iter.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for all three approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the three Kāra approaches agree with **each other** and with the Python mirror. An independent **ground-truth check** confirms the reconstruction: for every test tree, (a) the rebuilt tree's own inorder and postorder traversals reproduce the exact input arrays (the defining round-trip), *and* (b) the rebuilt tree is byte-identical to the original tree the `(inorder, postorder)` pair was read off — verified on a case battery **and 20,000 randomised fuzz trees**, zero mismatches. All three solvers compile with zero diagnostics and are valgrind-clean.

## Three ways to place the postorder position

Every approach rests on the same split: `postorder[last]` is the subtree's **root**, and the root's position in the inorder slice divides it into the left subtree's inorder (everything before) and the right subtree's (everything after); the left slice's *length* is how the postorder run divides into `[left…][right…][root]`. They differ only in how they track "where we are in postorder." This is the mirror of [#105](../105-construct-binary-tree-from-preorder-and-inorder-traversal/), reading the root from the **end** rather than the front.

**Index-bounds split** ([`build_tree.kara`](build_tree.kara), the ★): pass explicit postorder *and* inorder windows `(post_lo..post_hi, in_lo..in_hi)` down each call and derive the two child ranges from the left subtree's size (`mid - in_lo`). Pure divide-and-conquer — each call is a self-contained window, no shared state.

```
build(post_lo, post_hi, in_lo, in_hi):
    post_lo > post_hi -> None
    root = postorder[post_hi]
    mid  = index of root in inorder[in_lo..in_hi]
    left_size = mid - in_lo
    node.left  = build(post_lo,            post_lo+left_size-1, in_lo,  mid-1)
    node.right = build(post_lo+left_size,  post_hi-1,           mid+1,  in_hi)
```

**Single postorder cursor from the end** ([`build_tree_cursor.kara`](build_tree_cursor.kara)): thread *one* cursor into postorder as a `mut ref i64`, starting at the last index and **decreasing**. Reversed postorder is `root, right, left`, so each call consumes the next value (`postorder[cur]`) as its root and recurses **right before left** — the exact order the reversed walk lays nodes out, so the shared cursor visits them in sequence with no per-call postorder arithmetic. The inorder window alone bounds the recursion.

**Iterative stack** ([`build_tree_iter.kara`](build_tree_iter.kara)): the linear-time form. Walk postorder right to left, keeping a `Vec[TreeNode]` stack of ancestors whose left subtree is not yet built. If the stack top's value isn't the current inorder value (scanned from the end), the new node is the top's **right** child; otherwise pop while the top matches the retreating inorder cursor and the new node is the **left** child of the last node popped. Each value is pushed and popped once — O(n), no inorder search. The end-walking mirror of [#105](../105-construct-binary-tree-from-preorder-and-inorder-traversal/)'s iterative form (right↔left swapped, indices reversed).

## Kāra features exercised

- **`shared struct TreeNode` (RC), built then read** — all three solvers construct a fresh shared-node tree per call, then a preorder serialization walks it. Node type mirrors kata [#105](../105-construct-binary-tree-from-preorder-and-inorder-traversal/) / [#102](../102-binary-tree-level-order-traversal/).
- **`ref Vec[i64]` read-only inputs threaded through recursion** — the inorder/postorder arrays pass as `ref` borrows down every recursive call (never moved), the natural shape for shared read-only inputs.
- **`mut ref i64` cursor walked backward** — the cursor solver threads a single mutable index, decreasing it and reading `postorder[cur]` directly (indexing a `mut ref` scalar; hardened by kara [`B-2026-07-15-3`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl)).
- **`Vec[TreeNode]` stack: peek, `push`, and `node = stack.pop()`** — the iterative solver reads the top by index, pushes shared child handles, and advances by reassigning a shared-struct local from a popped value (hardened by kara [`B-2026-07-15-1`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl)).

**On the shoulders of [#105](../105-construct-binary-tree-from-preorder-and-inorder-traversal/).** That kata (the preorder+inorder sibling) surfaced four `karac` gaps while probing exactly these three forms — a `Vec[shared].pop()`-reassign leak (`B-2026-07-15-1`), a dead single-element-vec leak (`B-2026-07-15-2`), a `mut ref` scalar-read papercut (`B-2026-07-15-3`), and an auto-par granularity pathology (`B-2026-07-15-4`) — **all now fixed**. So #106 ships all three canonical forms clean from the start, no withholding: the iterative `node = stack.pop()` advance and the backward `mut ref` cursor both compile and run leak-clean, and the ★'s independent recursion stays sequential under the default build (the granularity cutoff correctly skips the 15-node subtree builds).

**v1 note.** Trees stay within the `≤ 3000`-node constraint. The sink folds each rebuilt tree's preorder serialization (a `#` sentinel per empty child, so shape *and* values are captured) into a running polynomial hash. All three solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the round-trip + structural-identity fuzz ground truth, and are valgrind-clean.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   build_tree.kara
karac build build_tree.kara && ./build_tree

# The cursor and iterative-stack variants (identical output):
karac run build_tree_cursor.kara
karac run build_tree_iter.kara

# Python
python3 build_tree.py

# Verify they all agree
diff <(karac run build_tree.kara) <(python3 build_tree.py)            && echo OK
diff <(karac run build_tree.kara) <(karac run build_tree_cursor.kara) && echo OK
diff <(karac run build_tree.kara) <(karac run build_tree_iter.kara)   && echo OK

# Ground truth: round-trip + structural identity vs the original tree (battery + 20k fuzz)
python3 ground_truth.py
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`build_tree.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** The canonical numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json). The corpus's canonical **Apple M5 Pro** numbers ([`bench/results.json`](bench/results.json)) are folded in separately; absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. Re-run `bench.sh` on the M5 to refresh the canonical table.

**Workload.** Build 8 `(inorder, postorder)` input pairs once (15-node trees, distinct shapes), then **K = 800,000** reps of the recursive index-bounds reconstruction on a **data-dependent-selected** pair (`idx = acc%8`, seeded by the running hash, so nothing hoists), folding the rebuilt tree's shape+value serialization into a rolling polynomial hash. Each rep allocates a fresh 15-node tree and frees it, so the workload is **allocation-bound**. Each mirror uses its natural node: Kāra `shared` (RC), C/Go raw pointer, **Rust `Box`** (single-owner — built then dropped). Linear inorder scan (O(n²)) in every mirror for parity. All five compiled mirrors must agree on `99155409` before timing.

**Auto-par note.** The ★'s two recursive calls are independent, so auto-par *considers* parallelizing them — but the granularity cost model ([`B-2026-07-15-4`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl), fixed) correctly leaves the ~15-node subtree builds sequential, so the default `karac build` runs single-threaded here (byte-equal to `KARAC_AUTO_PAR=0`) — the table below is the ordinary default build.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../../1-100/69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **x86-64 container numbers** (canonical M5 pending; see the machine note):

| Implementation | Wall time | Node representation |
|---|---|---|
| c    build_tree (clang -O3)                         | 315.6 ± 3.2 ms | `malloc` pointer |
| **kāra build_tree**                                 | **380.2 ± 9.8 ms** | **`shared` (RC)** |
| rust build_tree (rustc -O, overflow-checks=on)       | 381.7 ± 5.8 ms | `Box` |
| rust build_tree (rustc -O)                          | 403.8 ± 18.4 ms | `Box` |
| go   build_tree (GC)                                | 500.5 ± 17.5 ms | `*Node` (GC) |

**Kāra lands second — in a dead heat with Rust and 32% ahead of Go — on this allocation-bound tree-build.** Each rep constructs a fresh 15-node tree and tears it down, so the per-rep cost is node allocation. Against its semantic peer Rust — `Box` node, same divide-and-conquer, same linear scan — Kāra is a **statistical tie** (380 vs 382 ms against the overflow-checked build; 380 vs 404 against plain `rustc -O`, whose ±18 ms spread covers the difference): the shared (RC) node carries a refcount word the single-owner `Box` skips, but on a build-and-drop-immediately workload the allocation dominates and the refcount traffic disappears into the noise. **C's raw `malloc`** is the metal floor at 316 ms (**1.20× ahead of Kāra**) — allocation with no refcount and no GC. **Go trails at 500 ms** (Kāra **1.32× ahead**): the GC pays on the 800 k × 15-node allocation churn, deferred collection being the wrong trade when every tree is short-lived — the same GC-under-churn regime as [#102](../102-binary-tree-level-order-traversal/) and [#105](../105-construct-binary-tree-from-preorder-and-inorder-traversal/), where Go was likewise last. So the ordering is by allocator overhead on short-lived nodes — raw malloc < **Kāra RC ≈ `Box`** < Go GC. (This is the same regime and workload as the preorder+inorder sibling [#105](../105-construct-binary-tree-from-preorder-and-inorder-traversal/), where Kāra landed a hair *behind* Rust rather than a hair ahead — the two are indistinguishable across the shared host's noise; only the within-file ratios are the signal, and both put Kāra shoulder-to-shoulder with `Box`.) Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`) over the run. Python is listed at **367 ms but ran K = 40,000 — 1/20 of the compiled iterations** (pure-Python recursion is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **2.5 MiB** peak RSS (parity with Rust's 2.3 MiB, above C's 1.5 MiB) vs Go's **7.7 MiB**. The kāra binary measures **336 KiB** here — a build-linkage artifact of this container run (heap-growing programs retain the backtrace-symbolizer tree `--gc-sections` should strip; a correct build is ~15 KiB), independent of the runtime numbers, flagged for the M5 — vs C's 16 KiB and Go's 2.2 MiB.

**Flagged for the M5 re-bench** — Kāra and Rust are inside each other's noise here (and the sibling [#105](../105-construct-binary-tree-from-preorder-and-inorder-traversal/) ordered them the other way by the same margin), so treat the Kāra≈Rust *tie* as the finding, not the sign; the C-floor and Go-last signs are robust.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference) and, once folded in, [`bench/results.json`](bench/results.json) (M5, canonical).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched divide-and-conquer tree construction (`shared` RC node vs single-owner `Box`), the honest comparison for a build-a-fresh-tree-per-rep workload, isolating the RC-refcount tax. C's raw `malloc` is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
