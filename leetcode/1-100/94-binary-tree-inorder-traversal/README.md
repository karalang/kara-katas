# 94. Binary Tree Inorder Traversal

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Stack · Tree · Depth-First Search · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/binary-tree-inorder-traversal](https://leetcode.com/problems/binary-tree-inorder-traversal/)

Given the `root` of a binary tree, return the **inorder** traversal of its nodes' values — visit the **left** subtree, then the **node**, then the **right** subtree.

```
root = [1,null,2,3]  ->  [1,3,2]
root = []            ->  []
root = [1]           ->  [1]
```

Inorder is defined for **any** binary tree (not just BSTs) — it is simply the left-node-right visiting discipline. For a binary *search* tree it happens to emit the values in sorted order, which the benchmark's balanced-tree cases exercise.

**Constraints:** number of nodes in `0..100`; `-100 ≤ Node.val ≤ 100`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Recursive DFS** ★ | [`inorder.kara`](inorder.kara) ✓ via `karac run` / `karac build` | [`inorder.py`](inorder.py) ✓ |
| **Explicit stack (no recursion)** | [`inorder_iter.kara`](inorder_iter.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output across all nine test trees, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other **and** with the Python mirror. The five BST-shaped test trees additionally pass an independent **ground-truth check** — their inorder must come out strictly sorted, and does. Both solvers compile with **zero diagnostics**.

## Left, node, right — two ways to sequence it

The traversal *order* is fixed (left subtree → this node → right subtree); the two solvers differ only in how they hold the "where to resume" state.

**Recursive DFS** ([`inorder.kara`](inorder.kara), the ★) is the textbook three lines — the call stack *is* the resume state:

```
inorder(node):
    if node is None: return
    inorder(node.left)      # drain the left subtree first
    emit(node.val)          # then this node
    inorder(node.right)     # then the right subtree
```

Values are pushed into a `mut ref Vec[i64]` threaded down the calls — the call-site-marker rule fires once at the root (`mut out`, a fresh owned binding) and the inner forwards are unmarked, the same shape as the backtracking siblings [#77](../77-combinations/)/[#78](../78-subsets/).

**Explicit stack** ([`inorder_iter.kara`](inorder_iter.kara)) makes that resume state a concrete `Vec[TreeNode]`. The invariant: push every node down the left spine, and when the walk runs off the left edge, pop the most recent node, emit it, and pivot to its right subtree (whose own left spine is pushed next lap). A node is emitted exactly when its whole left subtree has drained — precisely inorder:

```
cur = root
loop:
    while cur is Some: push(cur); cur = cur.left    # descend the left spine
    if stack empty: break
    node = pop(); emit(node.val); cur = node.right  # visit, pivot right
```

It walks the **identical sequence** as the ★'s DFS — a distinct surface (an explicit `Vec[TreeNode]` stack + `Option` walker instead of recursion) proving the same order two ways.

## Kāra features exercised

- **`shared struct TreeNode` (RC) with `Option[TreeNode]` children** — the tree node type shared with [#98](../98-validate-binary-search-tree/) / [#226](../../201-300/226-invert-binary-tree/); `match` on `Option` children drives both the recursion base case and the iterative walker.
- **Recursion threading `mut ref Vec[i64]`** — the ★ carries the output accumulator down the DFS (`mut out` at the root, unmarked forwarding inside — the call-site-marker rule).
- **`Vec[TreeNode]` as an explicit stack** — the iterative variant pushes/pops node *handles* (RC references) on a growing `Vec`, with `if let Some(node) = stack.pop()` consuming the `Option[TreeNode]` that `pop` returns.
- **`Option` walker with `loop`/`break`** — the iterative left-spine descent is a nested `loop` over a `cur: Option[TreeNode]` that `break`s when it hits `None`.
- **Negative `i64` node values** — a test tree with `-10..9` exercises signed values through the traversal and the (value-shifted) sink fold.

**v1 note.** Node count ≤ 100 so the trees stay small; the per-case sink folds the traversal length and every visited value (shifted past the `-100..100` range) into a running hash, both count- and content- and *order*-sensitive. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`, both agree with each other and the Python mirror, and every BST-shaped case matches the sorted-order ground truth.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   inorder.kara
karac build inorder.kara && ./inorder

# The explicit-stack variant (identical output):
karac run inorder_iter.kara

# Python
python3 inorder.py

# Verify they all agree
diff <(karac run inorder.kara) <(python3 inorder.py)            && echo OK
diff <(karac run inorder.kara) <(karac run inorder_iter.kara)   && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`inorder.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** Numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json) (Intel Xeon @ 2.80 GHz, 4 vCPU; karac from current `main` 7de42d3, rustc 1.94, clang 18, go 1.24). The corpus's canonical **Apple M5 Pro** `results.json` is added on the reference machine; absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal.

**Workload.** A traversal of a *fixed* tree would be hoisted (a loop-invariant tree gives a constant fold), so this is a **build-then-traverse** workload (the [#98](../98-validate-binary-search-tree/) shape): each of **K = 320,000** iterations builds a fresh **63-node balanced tree** (`shared struct TreeNode`, RC-allocated) and folds the ★'s recursive inorder walk into a rolling polynomial hash **in visit order** — so the sink is order-sensitive and a wrong traversal order changes the number. Folding *during* the walk (a threaded accumulator) rather than collecting a `Vec[i64]` keeps this a **pure traversal bench**, not an allocation bench; the only allocation is `build`'s per-iteration tree, which every mirror also pays. All five compiled mirrors must agree on `85325436` before timing.

**Equal data structure.** Matched to actual usage — the tree is built once, traversed read-only, then dropped (no aliasing, no mutation) — so the honest node is single-owner: Kāra `shared struct` (RC), **Rust `Box<Node>`** (same choice as sibling tree kata [#98](../98-validate-binary-search-tree/)), **C a plain `malloc`/`free` raw-pointer tree** (the metal floor), Go a GC-managed `*Node`.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded (the loop-carried hash is not a reduction the auto-par pass can split; the default build is verified equal to `KARAC_AUTO_PAR=0`). **x86 container numbers.**

| Implementation | Wall time |
|---|---|
| c    inorder (clang -O3, malloc tree)            | 658.6 ± 17.6 ms |
| **kāra inorder**                                 | **709.3 ± 20.7 ms** |
| rust inorder (rustc -O, Box)                      | 732.6 ± 31.6 ms |
| rust inorder (rustc -O, overflow-checks=on)       | 746.5 ± 26.8 ms |
| go   inorder (`*Node`, GC)                        | 937.7 ± 44.4 ms |

Kāra is **2nd of five and beats both Rust builds** — 1.03× ahead of plain `rustc -O` and 1.05× ahead of equal-safety `rustc -O -C overflow-checks=on`, both on `Box` trees — trailing only the **raw-pointer C floor by 1.08×** and ahead of Go by **1.32×**. This is the same favourable tree/RC regime as the sibling [#98](../98-validate-binary-search-tree/): the recursion is **pointer-chase latency-bound** (each node dereferences two child links before it can recurse), so kāra's higher IPC covers its extra bounds/overflow-check instructions, and the traversal itself carries **no refcount traffic** (the ownership pass elides the count ops to scope boundaries — the tree is single-owner).

**The gap to C is the 8-byte RC header**, not the traversal: kāra allocates 32 B/node (`{rc, val, left, right}`) against C's 24 B (`{val, left, right}`), and on 63 × 320,000 ≈ 20 M allocations/run that width is the memory-bandwidth cost separating kāra from the raw-`malloc` floor — the same header ceiling documented for the linked-list sibling [#92](../92-reverse-linked-list-ii/). Even so, kāra's **binary is 15.4 KiB** (smaller than C's 15.8 KiB, ~140× smaller than Go's 2.2 MiB) and peak RSS **1.6 MiB** (tied with C, vs Go's 7.9 MiB). Python (K = 40,000, a fraction of the native iterations) is timed separately at 1471 ms.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — at matched single-owner node representation (`shared struct` vs `Box`), the same direct comparison as the tree sibling [#98](../98-validate-binary-search-tree/). C's raw-pointer tree is the metal floor, Go the GC data point, Python (a fraction of the iteration count, timed separately) the ergonomic foil.
