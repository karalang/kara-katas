# 109. Convert Sorted List to Binary Search Tree

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Linked List · Divide and Conquer · Tree · Binary Search Tree · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/convert-sorted-list-to-binary-search-tree](https://leetcode.com/problems/convert-sorted-list-to-binary-search-tree/)

Given the head of a singly linked list sorted in ascending order, build a **height-balanced** binary search tree. The linked-list sibling of [#108](../108-convert-sorted-array-to-binary-search-tree/) — same balanced-BST goal, reached from a list instead of an array.

```
head: -10 -> -3 -> 0 -> 5 -> 9         0            the middle node is the root;
                                      / \           the nodes before it form the
                                   -3    9          left subtree, those after the
                                   /     /          right — recursively, which
                                -10     5           keeps the tree balanced.
```

**Constraints:** `0 ≤ #nodes ≤ 2·10^4`, values strictly ascending, fit `-10^5 … 10^5`. Any valid height-balanced BST is accepted.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Walk to array + middle-pick** ★ | [`sorted_list_to_bst.kara`](sorted_list_to_bst.kara) ✓ | [`sorted_list_to_bst.py`](sorted_list_to_bst.py) ✓ |
| **Inorder simulation with a list cursor** | [`sorted_list_to_bst_inorder.kara`](sorted_list_to_bst_inorder.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for both approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the two Kāra approaches (both fixing `mid = (lo+hi)/2`) build the **byte-identical** tree and agree with the Python mirror. An independent **ground-truth check** confirms both defining properties: for every list, (a) an inorder walk of the built tree reproduces the list's values in order (a valid BST), *and* (b) the tree is **height-balanced** (`|height(left) − height(right)| ≤ 1` at every node) — verified on a case battery **and 20,000 randomised sorted lists**, zero violations, plus an array-vs-inorder-simulation structural cross-check.  Both solvers compile with zero diagnostics and are valgrind-clean.

## Two ways to convert

**Walk to array + middle-pick** ([`sorted_list_to_bst.kara`](sorted_list_to_bst.kara), the ★): a sorted list holds the same values in the same order as a sorted array, so walk the list once into a `Vec[i64]` and hand it to [#108](../108-convert-sorted-array-to-binary-search-tree/)'s middle-pick recursion — the middle element is the root, the halves are the subtrees. O(n) time, O(n) extra space. The simplest, most readable route.

```
sorted_list_to_bst(head):
    arr = [ every node's value, walking head→next ]
    return build_middle_pick(arr, 0, len-1)     # the #108 recursion
```

**Inorder simulation with a list cursor** ([`sorted_list_to_bst_inorder.kara`](sorted_list_to_bst_inorder.kara)): the clever route that never materializes an array. First count the list length, then build the tree by an **inorder simulation** — a subtree over list positions `[lo, hi]` builds its *left* subtree first (consuming the first half of the list), so that when it is the current node's turn a shared list cursor is sitting exactly on this subtree's root value; read it, advance the cursor one node, then build the right subtree from the rest. Because the list is sorted (= the BST's inorder), consuming it left to right hands each node to the right place. O(n) time, O(1) extra space beyond the recursion. The cursor threads through the recursion as a `mut ref Option[ListNode]`, advanced in place — a genuinely different mechanism that, with the same middle choice, lands on the byte-identical tree.

## Kāra features exercised

- **A `shared struct ListNode` alongside `shared struct TreeNode`** — the first corpus kata in this tree run to consume a **linked list** input and produce a tree output, both RC. The list is walked read-only; the tree is built fresh.
- **`mut ref Option[ListNode]` cursor advanced in place** — the inorder-simulation solver threads a single list cursor through the recursion and advances it with `cur = n.next`, the writeback-through-a-shared-`mut ref` surface hardened by kara [`B-2026-07-12-3`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) (`89fd514`); building the left subtree before reading the root is what lines the cursor up.
- **`ref Option[ListNode]` recursive length count** — the inorder solver counts the list by recursion over a borrowed head (`count(n.next)`), so the head stays owned for the build cursor.
- **`shared` list walked read-only into a `Vec[i64]`** — the ★ moves a cursor down the list (`cur = n.next`) collecting values; because the list nodes are shared, the walk drops only cursor handles, never the nodes.

**v1 note.** Lists stay within the `≤ 2·10^4`-node constraint. The sink folds each built tree's preorder serialization (a `#` sentinel per empty child, so shape *and* values are captured) into a running polynomial hash — and it is the **same sink as [#108](../108-convert-sorted-array-to-binary-search-tree/)** on the same values, since both build the identical balanced tree. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the BST + height-balanced fuzz ground truth, and are valgrind-clean.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   sorted_list_to_bst.kara
karac build sorted_list_to_bst.kara && ./sorted_list_to_bst

# The inorder-simulation variant (identical output):
karac run sorted_list_to_bst_inorder.kara

# Python
python3 sorted_list_to_bst.py

# Verify they all agree
diff <(karac run sorted_list_to_bst.kara) <(python3 sorted_list_to_bst.py)              && echo OK
diff <(karac run sorted_list_to_bst.kara) <(karac run sorted_list_to_bst_inorder.kara) && echo OK

# Ground truth: valid BST (inorder == list values) AND height-balanced (battery + 20k fuzz)
python3 ground_truth.py
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`sorted_list_to_bst.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** The canonical numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json). The corpus's canonical **Apple M5 Pro** numbers ([`bench/results.json`](bench/results.json)) are folded in separately; absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. Re-run `bench.sh` on the M5 to refresh the canonical table.

**Workload.** Build 8 sorted linked lists once (15 nodes each, distinct value ranges) and keep them alive across reps, then **K = 1,000,000** reps of the array-conversion `sorted_list_to_bst` on a **data-dependent-selected** list (`idx = acc%8`, seeded by the running hash, so nothing hoists): walk the list into a fresh array, build a fresh 15-node balanced tree by middle-pick, fold its serialization into a rolling polynomial hash. The workload is **allocation-bound** (the intermediate array + the tree). Each mirror uses its natural nodes: Kāra `shared` list + `shared` tree (RC); **Rust `Rc<ListNode>` list** (shared, read many times) **+ `Box` tree** (single-owner); C/Go raw pointers. All five compiled mirrors must agree on `940439984` before timing.

**Auto-par note.** The middle-pick recursion's two calls are independent, so auto-par *considers* parallelizing them — but the granularity cost model ([`B-2026-07-15-4`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl), fixed) correctly leaves the ~15-node subtree builds sequential, so the default `karac build` runs single-threaded here (byte-equal to `KARAC_AUTO_PAR=0`) — the table below is the ordinary default build.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../../1-100/69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **x86-64 container numbers** (canonical M5 pending; see the machine note):

| Implementation | Wall time | List / tree representation |
|---|---|---|
| c    sorted_list_to_bst (clang -O3)                  | 379.9 ± 26.4 ms | raw `*LNode` / `*TNode` |
| **kāra sorted_list_to_bst**                          | **495.1 ± 18.6 ms** | **`shared` list / `shared` tree (RC)** |
| rust sorted_list_to_bst (rustc -O, overflow-checks=on)| 539.9 ± 31.2 ms | `Rc` list / `Box` tree |
| rust sorted_list_to_bst (rustc -O)                   | 554.9 ± 14.3 ms | `Rc` list / `Box` tree |
| go   sorted_list_to_bst (GC)                         | 601.2 ± 25.5 ms | GC `*LNode` / `*TNode` |

**Kāra lands second — ahead of Rust by 12% and Go by 21% — on this walk-a-shared-list-and-build-a-tree workload.** Each rep walks the shared list into a fresh array (a per-node reference-count bump on the shared handle) and then builds and frees a 15-node balanced tree, so the cost is refcount traffic on the walk plus tree allocation. Against its semantic peer Rust — `Rc<ListNode>` list (matched to Kāra's `shared`) walked by `.clone()`, `Box` tree — Kāra is **1.12× ahead** (495 vs 555 ms; 495 vs 540 with overflow-checks on): both pay a per-node refcount on the list walk *and* allocate the tree, and Kāra's combined `shared`-handle-walk plus `Vec`/RC allocation path comes out leaner than Rust's `Rc::clone` chain plus `Box` build. **C's raw pointers** are the metal floor at 380 ms (**1.30× ahead**) — a pointer chase with no refcount and no GC on either structure. **Go trails at 601 ms** (Kāra **1.21× ahead**): the GC pays on the 1 M × 15-node tree churn, the same GC-under-churn regime where Go placed last across the tree-build siblings [#105](../105-construct-binary-tree-from-preorder-and-inorder-traversal/) / [#106](../106-construct-binary-tree-from-inorder-and-postorder-traversal/) / [#108](../108-convert-sorted-array-to-binary-search-tree/). So the ordering is raw pointer < **Kāra RC** < Rust `Rc`/`Box` < Go GC — the added shared-list walk (absent from the pure array-build [#108](../108-convert-sorted-array-to-binary-search-tree/), where Kāra and Rust tied) tips this one to Kāra, since the `Rc::clone`-per-node walk costs Rust more than Kāra's shared-handle walk. Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`) over the run. Python is listed at **393 ms but ran K = 60,000 — 1/17 of the compiled iterations** (pure-Python recursion is ~17× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **2.5 MiB** peak RSS (parity with Rust's 2.4 MiB, above C's 1.5 MiB) vs Go's **7.5 MiB**. The kāra binary measures **336 KiB** here — a build-linkage artifact of this container run (heap-growing programs retain the backtrace-symbolizer tree `--gc-sections` should strip; a correct build is ~15 KiB), independent of the runtime numbers, flagged for the M5 — vs C's 16 KiB and Go's 2.2 MiB.

**Flagged for the M5 re-bench** — the Kāra-ahead-of-Rust margin here (1.12×) rests on the `Rc::clone`-per-node list walk, and the corpus has seen container tree orderings shift on the M5's wider core (see [#99](../../1-100/99-recover-binary-search-tree/)), so treat the *margin* as a data point; the C-floor and Go-last signs are robust.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference) and, once folded in, [`bench/results.json`](bench/results.json) (M5, canonical).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched representations on both sides (`Rc` shared list + `Box` tree vs Kāra's `shared` list + `shared` tree), the honest comparison for a walk-a-shared-list-and-build-a-tree workload. C's raw pointers are the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
