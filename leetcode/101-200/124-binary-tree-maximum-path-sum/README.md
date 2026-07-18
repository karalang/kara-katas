# 124. Binary Tree Maximum Path Sum

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Tree · DFS · Dynamic Programming &nbsp;·&nbsp; **Source:** [leetcode.com/problems/binary-tree-maximum-path-sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/)

A **path** is any sequence of nodes where each consecutive pair is joined by an edge; it visits each node at most once and **need not pass through the root**. Given the tree, return the maximum sum of node values along any path. Node values can be negative, so a subtree may only ever subtract — the whole difficulty is knowing when to *not* extend into it.

```
      1                -10                     2
     / \               /  \                   / \
    2   3             9   20                -1  -2      single node: [-3]
                         /  \
       -> 6            15    7   -> 42          -> 2         -> -3
                    (15+20+7)
```

**Constraints:** `1 ≤ nodes ≤ 3·10⁴`, `-1000 ≤ Node.val ≤ 1000` — every path sum fits a signed 64-bit integer.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Post-order clamp-DP** ★ | O(n) time, O(h) stack | [`max_path_sum.kara`](max_path_sum.kara) ✓ | [`max_path_sum.py`](max_path_sum.py) ✓ |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the Kāra solver agrees with the Python mirror. An independent **ground-truth check** ([`ground_truth.py`](ground_truth.py)) confirms the clamp-DP equals a brute-force maximum over every path on **20,000 random trees** — zero disagreements. The solver compiles with zero diagnostics and is valgrind-clean.

## The mechanism

**Post-order clamp-DP** ([`max_path_sum.kara`](max_path_sum.kara), the ★): one bottom-up pass. Every path has a unique **top** node — the highest node on it — where the path may bend to use *both* children, or continue straight up using *one*. So for each node compute two things from its children's upward gains:

- `gain(c) = max(0, up(c))` — the most child `c` can add to a path that continues **upward** through this node. The `max(0, …)` is the key clamp: a child whose best downward chain is negative contributes **nothing** (you simply don't walk into it).
- `through = val + gain(left) + gain(right)` — the best path that **bends** at this node, using both sides. This is a candidate for the global answer but **cannot** be handed to the parent (a bent path has no free end to extend).
- `up = val + max(gain(left), gain(right))` — the best path that continues **upward**, using at most one side. This is what the function returns.

The global maximum is the maximum `through` over all nodes, threaded through the recursion in a **`mut ref i64`** accumulator (`best`). Because at least one node exists, the first `through` relax seeds a real value; `best` starts below the achievable floor (`-10⁹`) so an all-negative tree still returns its least-negative node.

## Kāra features exercised

- **`shared struct TreeNode` (RC)** — `{ val, mut left: Option[TreeNode], mut right: Option[TreeNode] }`, the same reference-counted node the #104/#112/#113 tree katas use; the post-order recursion borrows each `Option[TreeNode]` child without consuming it.
- **`mut ref i64` accumulator threaded through recursion** — `max_gain(node, best: mut ref i64)` carries the running maximum. The recursive calls `max_gain(n.left, best)` / `max_gain(n.right, best)` forward the in-scope `mut ref` binding **without** a call-site `mut` marker (per the call-site-marker rule); only `main`'s fresh `let mut best` needs `mut best` at the top-level call. The accumulator is read (`through > best`) and written (`best = through`) with transparent auto-deref — no explicit dereference operator.
- **`match` on `Option[TreeNode]`** — the `None => 0` / `Some(n) => …` post-order split; a missing child contributes a zero gain and never allocates.
- **Clamp via `if`-expression** — `if lg > 0 { lg } else { 0 }` lowers to a branchless conditional-move; the two per-node clamps plus the `max` branch are the whole hot body.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   max_path_sum.kara
karac build max_path_sum.kara && ./max_path_sum

# Python
python3 max_path_sum.py

# Verify they agree
diff <(karac run max_path_sum.kara) <(python3 max_path_sum.py) && echo OK

# Ground truth: clamp-DP == brute force over all paths, 20,000 random trees
python3 ground_truth.py
```

## Benchmarks

Wall-clock comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`max_path_sum.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** Canonical numbers are a shared **x86-64 Linux cloud-container** reference run (`bench/results.container-x86.json`). Absolute times/sizes/RSS are **not** comparable across hosts; only within-file cross-language ratios are the signal.

**Workload.** A forest of `T = 2048` balanced trees of `N = 511` mixed-sign nodes each, built **once** into a `Vec` before the timed loop, then `max_path_sum` run over the whole forest **K = 60** times, folding a sum-of-results sink (sink = `15576480`). Pointer-chasing post-order recursion over RC nodes dominates — the build-once + punch shape keeps the optimizer from erasing the traversal.

**Single-threaded, by design.** The per-tree recursion is a data-dependent pointer chase and the K-loop folds a serial sink, so every mirror stays on one core — the numbers measure the *traversal*, not a harness. `KARAC_AUTO_PAR=0` and the default build are byte-identical here (no auto-par-eligible reduction shape in the hot loop).

**Equal safety.** Kāra checks integer overflow (and the `Option[TreeNode]` unwrap) by default; the `rustc -O -C overflow-checks=on` row is the like-for-like on overflow.

> **Canonical numbers pending a quiet host.** All five mirrors are written and **cross-verified to produce the identical sink** (`15576480`), and [`bench.sh`](bench/bench.sh) runs them all. A preliminary container run was attempted but the shared host was **too noisy to publish** — a trivial `clang -O3` C binary spanned **429 ms … 3152 ms** across a single 12-run batch (a 7× spread from neighbour-tenant interference), which contaminates every cross-language ratio. Rather than commit numbers measured on a demonstrably unreliable host, `results.container-x86.json` is deferred to a clean reference run (`bash bench/bench.sh` on a quiet host). This kata's value as a dogfood — a correct, valgrind-clean RC-tree traversal verified on every surface — does not depend on the timing table.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at a matched RC-tree post-order traversal (`Option[TreeNode]`/`Rc<RefCell<…>>` vs `shared struct TreeNode`). C's raw-pointer tree is the metal floor, Go the GC data point, Python (timed separately, not cross-checked) the ergonomic foil.
