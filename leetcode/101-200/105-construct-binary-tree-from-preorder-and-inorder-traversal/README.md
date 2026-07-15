# 105. Construct Binary Tree from Preorder and Inorder Traversal

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Hash Table · Divide and Conquer · Tree · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)

Given `preorder` and `inorder` traversals of a binary tree with **distinct** values, reconstruct the tree.

```
preorder = [3, 9, 20, 15, 7]          3
inorder  = [9, 3, 15, 20, 7]         / \
                                     9  20
   preorder[0]=3 is the root;          / \
   3 splits inorder into [9] (left)   15  7
   and [15,20,7] (right).
```

**Constraints:** `1 ≤ #nodes ≤ 2000`, node values are distinct and fit `-1000 … 1000`, and the two arrays are genuine preorder/inorder traversals of the *same* tree.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Recursive index-bounds split** ★ | [`build_tree.kara`](build_tree.kara) ✓ | [`build_tree.py`](build_tree.py) ✓ |
| **Recursive with a single preorder cursor** | [`build_tree_cursor.kara`](build_tree_cursor.kara) ✓ | — |
| **Iterative stack (O(n), no search)** | [`build_tree_iter.kara`](build_tree_iter.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for all three approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the three Kāra approaches agree with **each other** and with the Python mirror. An independent **ground-truth check** confirms the reconstruction: for every test tree, (a) the rebuilt tree's own preorder and inorder traversals reproduce the exact input arrays (the defining round-trip), *and* (b) the rebuilt tree is byte-identical to the original tree the `(preorder, inorder)` pair was read off — verified on a case battery **and 20,000 randomised fuzz trees**, zero mismatches. All three solvers compile with zero diagnostics and are valgrind-clean.

## Three ways to place the preorder position

Both rest on the same split: `preorder[first]` is the subtree's **root**, and the root's position in the inorder slice divides it into the left subtree's inorder (everything before) and the right subtree's (everything after); the left slice's *length* is exactly how much of the preorder run belongs to the left child. They differ only in how they track "where we are in preorder."

**Index-bounds split** ([`build_tree.kara`](build_tree.kara), the ★): pass explicit preorder *and* inorder windows `(pre_lo..pre_hi, in_lo..in_hi)` down each call and derive the left child's preorder range from the left subtree's size (`mid - in_lo`). Pure divide-and-conquer — each call is a self-contained window, no shared state, so left and right subtrees are wholly independent.

```
build(pre_lo, pre_hi, in_lo, in_hi):
    pre_lo > pre_hi -> None
    root = preorder[pre_lo]
    mid  = index of root in inorder[in_lo..in_hi]
    left_size = mid - in_lo
    node.left  = build(pre_lo+1,            pre_lo+left_size, in_lo,   mid-1)
    node.right = build(pre_lo+left_size+1,  pre_hi,           mid+1,   in_hi)
```

**Single preorder cursor** ([`build_tree_cursor.kara`](build_tree_cursor.kara)): thread *one* advancing cursor into preorder as a `mut ref i64`, consuming the next value (`preorder[cur]`) as each subtree's root and recursing **left before right** — the exact order preorder lays nodes out, so the shared cursor visits them in sequence with no per-call preorder arithmetic. The inorder window alone bounds the recursion. A genuinely different mechanism (stateful running index vs functional windows) that must land on the identical tree — and, unlike the ★, the shared cursor creates a real left-before-right *data dependency* between the two recursive calls.

**Iterative stack** ([`build_tree_iter.kara`](build_tree_iter.kara)): the linear-time form. Walk preorder left to right, keeping a `Vec[TreeNode]` stack of ancestors whose right subtree is not yet built. If the stack top's value isn't the current inorder value, the new node is the top's **left** child (still descending left); otherwise pop while the top matches the advancing inorder cursor (those left subtrees are done) and the new node is the **right** child of the last node popped. Each value is pushed and popped once — O(n), no inorder search. The `node = stack.pop()` frontier advance is the shape that surfaced [`B-2026-07-15-1`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) (below).

## Kāra features exercised

- **`shared struct TreeNode` (RC), built then read** — both solvers construct a fresh shared-node tree per call, then a preorder serialization walks it. Node type mirrors kata [#102](../102-binary-tree-level-order-traversal/) / [#100](../../1-100/100-same-tree/).
- **`ref Vec[i64]` read-only inputs threaded through recursion** — the preorder/inorder arrays pass as `ref` borrows down every recursive call (never moved), the natural shape for shared read-only inputs.
- **`mut ref i64` cursor through recursion** — the cursor solver threads a single mutable index and reads the root directly as `preorder[cur]` (indexing a `mut ref` scalar; the read-into-value coercion that once forced an arithmetic workaround is [`B-2026-07-15-3`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl), fixed `42a9f2c`).
- **`Vec[TreeNode]` stack: peek, `push`, and `node = stack.pop()`** — the iterative solver reads the top by index, pushes shared child handles, and advances by reassigning a shared-struct local from a popped value (the surface hardened by [`B-2026-07-15-1`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl), fixed `a384971`).
- **`Option[shared]` field construction** — `Some(TreeNode { val, left, right })` builds each node with its recursively-constructed subtrees as `Option[TreeNode]` fields.

### Compiler findings this kata surfaced (now all fixed)

Probing the **iterative stack** construction (walk preorder, keep a `Vec[TreeNode]` ancestor stack, advance with `node = stack.pop()`) — and the ★'s independent recursion at benchmark scale — turned up four `karac` gaps. Per the repo's "never route around — fix or file it" rule, all were filed with minimal repros; **all four are now fixed**, and this kata ships all three solvers above (the iterative form was withheld until [`B-2026-07-15-1`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) landed, exactly as [#102](../102-binary-tree-level-order-traversal/)'s BFS was withheld until `B-2026-07-12-30`):

- [`B-2026-07-15-1`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) (medium, fixed `a384971`) — reassigning a shared-struct local from a `Vec[shared].pop()` value (`node = popped`) skipped the old value's rc-dec, leaking the whole rebuilt tree on every iterative construction. Scalar-local sibling of `B-2026-07-12-30`.
- [`B-2026-07-15-2`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) (medium, fixed `a384971`) — a `Vec[shared]` with exactly one pushed element never read after the push leaked it at scope-exit drop (two+ elements, or any read, was clean); minimized out of the above.
- [`B-2026-07-15-3`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) (low, fixed `42a9f2c`) — no clean way to read a `mut ref i64` scalar into a plain `i64` for indexing; `preorder[cur]` now works directly.
- [`B-2026-07-15-4`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) (medium, fixed `67cc2db`/`a9f3f7f`) — auto-par parallelized the ★'s independent left/right recursion **with no granularity cutoff**, spawning threads for ~15-node subtrees: a **160× wall-time regression** (22.4 s vs 0.138 s at K=200 k), *same correct output*. The fix adds the size/cost cutoff, so small subtree builds now stay sequential and the default build matches `KARAC_AUTO_PAR=0`.

**v1 note.** Trees stay within the `≤ 2000`-node constraint. The sink folds each rebuilt tree's preorder serialization (a `#` sentinel per empty child, so shape *and* values are captured) into a running polynomial hash. All three solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the round-trip + structural-identity fuzz ground truth, and are valgrind-clean.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   build_tree.kara
karac build build_tree.kara && ./build_tree

# The single-cursor and iterative-stack variants (identical output):
karac run build_tree_cursor.kara
karac run build_tree_iter.kara

# Python
python3 build_tree.py

# Verify they all agree
diff <(karac run build_tree.kara) <(python3 build_tree.py)              && echo OK
diff <(karac run build_tree.kara) <(karac run build_tree_cursor.kara)  && echo OK
diff <(karac run build_tree.kara) <(karac run build_tree_iter.kara)    && echo OK

# Ground truth: round-trip + structural identity vs the original tree (battery + 20k fuzz)
python3 ground_truth.py
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`build_tree.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** The canonical numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json). The corpus's canonical **Apple M5 Pro** numbers ([`bench/results.json`](bench/results.json)) are folded in separately; absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. Re-run `bench.sh` on the M5 to refresh the canonical table.

**Workload.** Build 8 `(preorder, inorder)` input pairs once (15-node trees, distinct shapes), then **K = 800,000** reps of the recursive index-bounds reconstruction on a **data-dependent-selected** pair (`idx = acc%8`, seeded by the running hash, so nothing hoists), folding the rebuilt tree's shape+value serialization into a rolling polynomial hash. Each rep allocates a fresh 15-node tree and frees it, so the workload is **allocation-bound**. Each mirror uses its natural node: Kāra `shared` (RC), C/Go raw pointer, **Rust `Box`** (the tree is single-owner — built then dropped, never shared). Linear inorder scan (O(n²)) in every mirror for parity. All five compiled mirrors must agree on `99155409` before timing.

**Auto-par note.** The ★'s two recursive calls are independent, so auto-par *considers* parallelizing them — but with the granularity cost model ([`B-2026-07-15-4`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl), fixed `67cc2db`/`a9f3f7f`) it correctly leaves the ~15-node subtree builds sequential, so the default `karac build` runs single-threaded here (byte-equal to `KARAC_AUTO_PAR=0`) — the table below is the ordinary default build. (Before that fix this shape spawned threads for every tiny subtree, a ~160× wall-time regression at correct output; the numbers below are on the fixed compiler.)

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../../1-100/69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **x86-64 container numbers** (canonical M5 pending; see the machine note):

| Implementation | Wall time | Node representation |
|---|---|---|
| c    build_tree (clang -O3)                         | 465.3 ± 12.3 ms | `malloc` pointer |
| rust build_tree (rustc -O, overflow-checks=on)       | 506.4 ± 22.7 ms | `Box` |
| rust build_tree (rustc -O)                          | 507.2 ± 10.2 ms | `Box` |
| **kāra build_tree**                                 | **530.5 ± 19.5 ms** | **`shared` (RC)** |
| go   build_tree (GC)                                | 654.4 ± 25.2 ms | `*Node` (GC) |

**Kāra lands fourth by a hair — within ~5% of Rust, 14% behind C, and 23% ahead of Go — on an allocation-bound tree-build.** Each rep constructs a fresh 15-node tree and tears it down, so the per-rep cost is dominated by node allocation. Against its semantic peer Rust — `Box` node, same divide-and-conquer, same linear scan — Kāra is **1.05× behind** (530 vs 507 ms plain, 530 vs 506 with overflow-checks on): the shared (RC) node carries a refcount word and an inc/dec the single-owner `Box` skips, and on a build-and-drop-immediately workload that refcount traffic is the whole of the small gap. **C's raw `malloc`** is the metal floor at 465 ms (**1.14× ahead**) — allocation with no refcount and no GC. **Go trails at 654 ms** (Kāra **1.23× ahead**): the GC pays on the 800 k × 15-node allocation churn, deferred collection being the wrong trade when every tree is short-lived — the same GC-under-churn regime as [#102](../102-binary-tree-level-order-traversal/), where Go was likewise last. So the ordering is by allocator overhead on short-lived nodes — raw malloc < `Box` < **Kāra RC** < Go GC — with Kāra sitting one refcount-word behind Rust. Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`) over the run. Python is listed at **594 ms but ran K = 40,000 — 1/20 of the compiled iterations** (pure-Python recursion is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **2.3 MiB** peak RSS (parity with Rust's 2.3 MiB, above C's 1.5 MiB) vs Go's **7.6 MiB**. The kāra binary measures **336 KiB** here — a build-linkage artifact of this container run (heap-growing programs retain the backtrace-symbolizer tree `--gc-sections` should strip; a correct build is ~15 KiB), independent of the runtime numbers, flagged for the M5 — vs C's 16 KiB and Go's 2.2 MiB.

**Flagged for the M5 re-bench** — the Kāra-just-behind-Rust margin here is narrow (1.05×) and the corpus has seen container tree orderings shift on the M5's wider core (see [#99](../../1-100/99-recover-binary-search-tree/), where the RC node *passed* `Rc<RefCell>`), so treat the *margin* as a data point, not a verdict; the C-floor and Go-last signs are robust.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference) and, once folded in, [`bench/results.json`](bench/results.json) (M5, canonical).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched divide-and-conquer tree construction (`shared` RC node vs single-owner `Box`), the honest comparison for a build-a-fresh-tree-per-rep workload, isolating the RC-refcount tax (~3.5%). C's raw `malloc` is the metal floor, Go the GC data point (last, on allocation churn), Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
