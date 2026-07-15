# 108. Convert Sorted Array to Binary Search Tree

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Array · Divide and Conquer · Tree · Binary Search Tree · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/convert-sorted-array-to-binary-search-tree](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/)

Given an integer array sorted in ascending order, build a **height-balanced** binary search tree.

```
[-10, -3, 0, 5, 9]           0            pick the middle as root; the
                            / \           left half is the left subtree,
                         -3    9          the right half the right subtree,
                         /     /          recursively — which keeps the
                      -10     5           two sides balanced.
```

**Constraints:** `1 ≤ #elements ≤ 10^4`, values strictly ascending, fit `-10^4 … 10^4`. Any valid height-balanced BST is accepted.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Recursive middle-pick** ★ | [`sorted_to_bst.kara`](sorted_to_bst.kara) ✓ | [`sorted_to_bst.py`](sorted_to_bst.py) ✓ |
| **Iterative stack (range worklist)** | [`sorted_to_bst_iter.kara`](sorted_to_bst_iter.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for both approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the two Kāra approaches (both fixing `mid = (lo+hi)/2`) build the **byte-identical** tree and agree with the Python mirror. An independent **ground-truth check** confirms both defining properties: for every array, (a) an inorder walk of the built tree reproduces the sorted input (a valid BST placing every value), *and* (b) the tree is **height-balanced** (`|height(left) − height(right)| ≤ 1` at every node) — verified on a case battery **and 20,000 randomised sorted arrays**, zero violations, plus a recursive-vs-iterative structural cross-check. Both solvers compile with zero diagnostics and are valgrind-clean.

## Two ways to build the balanced tree

Both rest on the same idea: the **middle** element (`(lo + hi) / 2`) is the subtree's root — everything left of it is smaller (the left subtree), everything right is larger (the right subtree) — and choosing the middle keeps the two halves within one of each other, so the tree stays balanced. They differ only in how they drive the divide-and-conquer.

**Recursive middle-pick** ([`sorted_to_bst.kara`](sorted_to_bst.kara), the ★): the textbook form. Take the middle as the root, recurse on the left half for the left child and the right half for the right. O(n), each call a self-contained `(lo, hi)` window.

```
build(lo, hi):
    lo > hi -> None
    mid = (lo + hi) / 2
    node.val   = arr[mid]
    node.left  = build(lo,      mid-1)
    node.right = build(mid+1,   hi)
```

**Iterative stack** ([`sorted_to_bst_iter.kara`](sorted_to_bst_iter.kara)): drive the same recursion with an explicit worklist of `(node, lo, hi)` frames. Create a placeholder root over the whole array, then repeatedly pop a frame, set that node's value to `arr[mid]`, and for each non-empty half attach a fresh placeholder child and push its frame. When the worklist empties, every node is filled. A genuinely different mechanism (explicit range stack vs the call stack) that — with the same middle choice — produces the byte-identical tree.

## Kāra features exercised

- **`shared struct TreeNode` (RC), built then read** — both solvers construct a fresh shared-node tree, then a preorder serialization walks it. Node type mirrors kata [#105](../105-construct-binary-tree-from-preorder-and-inorder-traversal/) / [#106](../106-construct-binary-tree-from-inorder-and-postorder-traversal/).
- **`ref Vec[i64]` read-only input** — the sorted array passes as a `ref` borrow down every recursive call (never moved).
- **`mut val` placeholder-then-fill** — the iterative solver creates each node before it knows its value (`val: 0`), then sets `node.val = arr[mid]` on pop; this needs the node's `val` field declared `mut` (the recursive ★ constructs with the value inline and leaves `val` immutable).
- **Three parallel worklist stacks + `stack.pop()`** — the iterative frames live in a `Vec[TreeNode]` of shared handles alongside two `Vec[i64]` range bounds, popped in sync each step (the `Vec[shared]` push/pop surface hardened by kara [`B-2026-07-15-1`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl)).

**v1 note.** Arrays stay within the `≤ 10^4`-element constraint. The sink folds each built tree's preorder serialization (a `#` sentinel per empty child, so shape *and* values are captured) into a running polynomial hash. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the BST + height-balanced fuzz ground truth, and are valgrind-clean.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   sorted_to_bst.kara
karac build sorted_to_bst.kara && ./sorted_to_bst

# The iterative-stack variant (identical output):
karac run sorted_to_bst_iter.kara

# Python
python3 sorted_to_bst.py

# Verify they all agree
diff <(karac run sorted_to_bst.kara) <(python3 sorted_to_bst.py)          && echo OK
diff <(karac run sorted_to_bst.kara) <(karac run sorted_to_bst_iter.kara) && echo OK

# Ground truth: valid BST (inorder == input) AND height-balanced (battery + 20k fuzz)
python3 ground_truth.py
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`sorted_to_bst.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** The canonical numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json). The corpus's canonical **Apple M5 Pro** numbers ([`bench/results.json`](bench/results.json)) are folded in separately; absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. Re-run `bench.sh` on the M5 to refresh the canonical table.

**Workload.** Build 8 sorted arrays once (15 elements each, distinct value ranges), then **K = 1,200,000** reps of the recursive middle-pick `sorted_to_bst` on a **data-dependent-selected** array (`idx = acc%8`, seeded by the running hash, so nothing hoists), folding the built tree's shape+value serialization into a rolling polynomial hash. Each rep allocates a fresh 15-node balanced tree and frees it, so the workload is **allocation-bound**. Each mirror uses its natural node: Kāra `shared` (RC), C/Go raw pointer, **Rust `Box`** (single-owner — built then dropped). All five compiled mirrors must agree on `296311190` before timing.

**Auto-par note.** The middle-pick recursion's two calls are independent, so auto-par *considers* parallelizing them — but the granularity cost model ([`B-2026-07-15-4`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl), fixed) correctly leaves the ~15-node subtree builds sequential, so the default `karac build` runs single-threaded here (byte-equal to `KARAC_AUTO_PAR=0`) — the table below is the ordinary default build.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../../1-100/69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **x86-64 container numbers** (canonical M5 pending; see the machine note):

| Implementation | Wall time | Node representation |
|---|---|---|
| c    sorted_to_bst (clang -O3)                       | 472.7 ± 12.1 ms | `malloc` pointer |
| **kāra sorted_to_bst**                               | **523.5 ± 11.6 ms** | **`shared` (RC)** |
| rust sorted_to_bst (rustc -O)                        | 534.2 ± 14.0 ms | `Box` |
| rust sorted_to_bst (rustc -O, overflow-checks=on)     | 553.8 ± 49.9 ms | `Box` |
| go   sorted_to_bst (GC)                              | 769.6 ± 19.7 ms | `*Node` (GC) |

**Kāra lands second — a dead heat with Rust and 47% ahead of Go — on this allocation-bound balanced-tree build.** Each rep constructs a fresh 15-node balanced tree and tears it down, so the per-rep cost is node allocation (no search here — the middle is pure index arithmetic). Against its semantic peer Rust — `Box` node, same divide-and-conquer — Kāra is a **statistical tie** (523 vs 534 ms plain, 523 vs 554 with overflow-checks on): the shared (RC) node carries a refcount word the single-owner `Box` skips, but on a build-and-drop-immediately workload the allocation dominates and the refcount traffic disappears into the noise. **C's raw `malloc`** is the metal floor at 473 ms (**1.11× ahead**) — allocation with no refcount and no GC. **Go trails at 770 ms** (Kāra **1.47× ahead**): the GC pays on the 1.2 M × 15-node allocation churn, deferred collection being the wrong trade when every tree is short-lived — the same GC-under-churn regime as the tree-build siblings [#105](../105-construct-binary-tree-from-preorder-and-inorder-traversal/) / [#106](../106-construct-binary-tree-from-inorder-and-postorder-traversal/), where Go was likewise last. So the ordering is by allocator overhead on short-lived nodes — raw malloc < **Kāra RC ≈ `Box`** < Go GC — Kāra and Rust shoulder-to-shoulder, exactly as in [#105](../105-construct-binary-tree-from-preorder-and-inorder-traversal/) / [#106](../106-construct-binary-tree-from-inorder-and-postorder-traversal/) (the three tree-build katas put them within noise of each other, ordering either way by a hair). Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`) over the run. Python is listed at **455 ms but ran K = 60,000 — 1/20 of the compiled iterations** (pure-Python recursion is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **2.4 MiB** peak RSS (parity with Rust's 2.2 MiB, above C's 1.5 MiB) vs Go's **7.7 MiB**. The kāra binary measures **324 KiB** here — a build-linkage artifact of this container run (heap-growing programs retain the backtrace-symbolizer tree `--gc-sections` should strip; a correct build is ~15 KiB), independent of the runtime numbers, flagged for the M5 — vs C's 16 KiB and Go's 2.2 MiB.

**Flagged for the M5 re-bench** — Kāra and Rust are inside each other's noise here (as across all three tree-build katas), so treat the Kāra≈Rust *tie* as the finding, not the sign; the C-floor and Go-last signs are robust.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference) and, once folded in, [`bench/results.json`](bench/results.json) (M5, canonical).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched divide-and-conquer tree construction (`shared` RC node vs single-owner `Box`), the honest comparison for a build-a-fresh-balanced-tree-per-rep workload, isolating the RC-refcount tax. C's raw `malloc` is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
