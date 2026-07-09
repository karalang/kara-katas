# 98. Validate Binary Search Tree

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Tree · Depth-First Search · Binary Search Tree · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/validate-binary-search-tree](https://leetcode.com/problems/validate-binary-search-tree/)

Decide whether a binary tree is a valid **binary search tree**: for *every* node, its value must be strictly greater than **all** values in its left subtree and strictly less than **all** values in its right subtree.

```
    2               5                  5
   / \             / \                / \
  1   3   ✓       1   4     ✗        4   6      ✗
                     / \                / \
                    3   6              3   7
  valid BST     4's left child 3    3 is in 5's right subtree
                is < 5 (its         yet 3 < 5 — a distant
                grandparent)        ancestor violation
```

**Constraints:** `1 ≤ nodes ≤ 10⁴`; `−2³¹ ≤ Node.val ≤ 2³¹ − 1`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Recursive (lo, hi) bounds** ★ — a node must lie in the open interval inherited from its ancestors | O(n) time, O(h) stack | [`validate_bst.kara`](validate_bst.kara) ✓ via `karac run` / `karac build` | [`validate_bst.py`](validate_bst.py) ✓ |
| **Inorder is sorted** — collect the inorder traversal, check it strictly increases | O(n) time, O(n) space | [`validate_bst_inorder.kara`](validate_bst_inorder.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output across all ten test trees, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other and with the Python mirror.

## The trap: local rule ≠ BST

The mistake the problem is built to catch is checking only `left < node < right` at each node. That misses a value that is a valid immediate child but violates the invariant against a *distant* ancestor — `[5,4,6,null,null,3,7]`: the `3` is the left child of `6` (so `3 < 6`, locally fine) but it sits in `5`'s **right** subtree, where everything must exceed `5`. A correct check carries the full legal range, not just the parent.

**Recursive (lo, hi) bounds** ([`validate_bst.kara`](validate_bst.kara)) is the ★. Thread an open interval `(lo, hi)` down the tree: the value must land strictly inside it, the **left** child inherits `(lo, node.val)`, the **right** child inherits `(node.val, hi)`. The bounds are `Option[i64]` with `None` meaning "unbounded on that side," and the root starts `(None, None)` — so there is no sentinel `i64::MIN`/`MAX` that a legitimate node value (which can span the full i32 range) might equal. A node outside its interval short-circuits the whole tree to `false` via `and`.

**Inorder is sorted** ([`validate_bst_inorder.kara`](validate_bst_inorder.kara)) uses the defining property directly: an inorder walk (left, node, right) of a BST emits values in strictly increasing order. Collect the traversal into a `Vec[i64]` and verify every adjacent pair increases. It trades O(n) space for the most literal statement of the property, and cross-checks the ★.

## Kāra features exercised

- **`shared struct TreeNode` (RC) with `Option[TreeNode]` children** — the recursive reference type `shared struct TreeNode { val: i64, mut left: Option[TreeNode], mut right: Option[TreeNode] }`, and nested `Some(TreeNode { … })` construction (with a `leaf` helper), the tree idiom shared with kata [#226](../../201-300/226-invert-binary-tree/).
- **`match` on the node and on each `Option[i64]` bound** — `match node { None => …, Some(n) => … }` drives the recursion, and the ★ matches each bound (`match lo { Some(l) => …, None => {} }`) to apply it only when present; a mid-arm `return false` short-circuits.
- **Recursion carrying accumulators two different ways** — the ★ threads by-value `Option[i64]` bounds *down* and returns a `bool` (with short-circuiting `and`); the inorder solver threads a **`mut ref Vec[i64]`** accumulator *through* the recursion, forwarding the existing mutable borrow to the child calls without a call-site marker (`inorder(n.left, out)`) and marking only the fresh owned binding at the top (`inorder(root, mut vals)`). Two distinct codegen shapes over the same `shared struct`.
- **Bool-folding `report` harness** — one `valid=true`/`valid=false` per tree plus a `sums:` fold of `1`/`0`, the byte-for-byte diff anchor; both solvers and the Python mirror print it identically.

**v1 note.** Node values are i64 (the problem's i32 range fits with room to spare); no arithmetic here can overflow — the only operations are comparisons. Using `Option[i64]` bounds rather than sentinels means the validator is correct even for a node whose value equals `i64`'s extremes. Both solvers verified byte-identical under `karac run` and `karac build`, including the default auto-parallelizing build and `KARAC_AUTO_PAR=0` — the recursive `shared struct` traversal lowers consistently across all three surfaces.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   validate_bst.kara
karac build validate_bst.kara && ./validate_bst

# The inorder approach (identical output):
karac run validate_bst_inorder.kara

# Python
python3 validate_bst.py

# Verify they all agree
diff <(karac run validate_bst.kara) <(python3 validate_bst.py)             && echo OK
diff <(karac run validate_bst.kara) <(karac run validate_bst_inorder.kara) && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`validate_bst.{kara,rs,c,py}`, `validate_bst_rc.rs`, `go-seq/main.go`).

> ⚠️ **Machine caveat.** Like katas [#63](../63-unique-paths-ii/#benchmarks)–[#70](../70-climbing-stairs/#benchmarks)'s container passes (and unlike the M5 Pro tables elsewhere in the corpus), the numbers below were measured on a **shared x86-64 Linux cloud container** (Intel Xeon @ 2.10 GHz, 4 vCPU, Linux 6.18.5; karac rebuilt from current `main`). Don't compare absolute times/sizes/RSS against sibling katas' M5 tables; `bench/results.json` records the real host. This alloc-heavy run is **noisy** (hyperfine flagged outliers). Re-run `bench/bench.sh` on the M5 to fold comparable numbers in.

**Workload.** A validation is O(n), and validating a *fixed* tree K times would be hoisted (a loop-invariant tree gives a constant result). So the bench is **build-then-validate**: each of **K = 200,000** iterations builds a fresh **63-node balanced BST** (an RC `shared struct TreeNode` tree) and runs the ★'s recursive `(lo, hi)`-bounds validator, folding `shift + valid?1:0` into a rolling hash. A per-iteration `shift = k%1000` makes each tree different (non-hoistable). This is **allocation-inclusive by design** — it stresses the RC / `Option` / recursion surface end to end (per-node RC alloc + drop in `build`, `match`-driven recursion in `is_valid`), the closest analogue being the linked-list katas [#19](../19-remove-nth-node-from-end-of-list/)/[#61](../61-rotate-list/). All four compiled mirrors must agree on `584566580` before timing.

### The equal-memory-semantics comparison

Kāra's recursive `TreeNode` is a **`shared struct` — RC-backed** (reference-counted). The default Rust mirror uses **`Box<Node>`** (unique ownership, *no* refcount), which is cheaper. The faithful like-for-like is **`Rc<Node>`** — so, exactly as [#69](../69-sqrtx/) adds a `-C overflow-checks=on` row for equal *safety*, this harness adds an `Rc<Node>` row for equal *memory semantics*.

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **Cloud-container numbers.**

| Implementation | Wall time | Node memory |
|---|---|---|
| c    validate_bst (clang -O3)         | 362.5 ± 12.5 ms | `malloc`/`free` |
| rust validate_bst (`Box<Node>`)       | 390.6 ± 18.1 ms | unique owned |
| rust validate_bst (`Rc<Node>`)        | 417.5 ± 7.4 ms | **refcounted** |
| **kāra validate_bst (`shared struct`)** | **453.4 ± 13.5 ms** | **refcounted (RC)** |
| go   validate_bst                     | 527.5 ± 20.2 ms | GC |

**This is an honest "kāra trails" result on the RC surface** — and unlike [#69](../69-sqrtx/), the equal-semantics row does *not* bring parity. kāra's RC (453 ms) trails C's raw `malloc` (~1.25×), Rust's `Box` (~1.16×), and — the load-bearing comparison — even Rust's `Rc` (417 ms, ~1.09×). Adding the refcount to Rust (`Box` → `Rc`, +27 ms) closes only part of the gap: about half the kāra-vs-Box distance is "RC vs unique ownership" (which Rust would pay too for a shared type), but the remaining ~1.09× over `Rc` is **genuine kāra RC/allocation codegen overhead** on this build-heavy tree, not a semantics artifact. kāra still beats Go's GC (~1.16× ahead). This is a container-only measurement flagged for the M5 re-bench before it's treated as a tracked regression; it is the counterweight to [#61](../61-rotate-list/), where kāra *led* Rust because there the faithful Rust needed `Rc<RefCell>`.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py validate_bst` (K=20k) | 655.3 ± 31.8 ms |

Python at K=20k is ~0.66 s; projecting to the compiled mirrors' K=200k (~6.6 s) puts it **~14× slower than kāra seq** — a narrower gap than the pure-compute katas because this workload is dominated by allocation and pointer-chasing, which CPython does in C.

### Compile elapsed (cold)

| Compiler | Time |
|---|---|
| clang -O3 validate_bst.c          | **105.4 ± … ms** |
| rustc -O validate_bst.rs          | 120.3 ms |
| **karac build validate_bst.kara** | **156.8 ms** |

On this container karac compiles at ~1.49× clang and ~1.30× rustc.

### Binary size

| Implementation | Size |
|---|---|
| **kāra validate_bst**            | **15.4 KiB** |
| c    validate_bst                | 15.8 KiB |
| go   validate_bst                | 2.11 MiB |
| rust validate_bst                | 3.77 MiB |

Kāra's seq binary is **15.4 KiB — the smallest of the four**, a hair under C's 15.8 KiB (same as [#69](../69-sqrtx/)/[#70](../70-climbing-stairs/)), and orders of magnitude below Rust's 3.8 MiB and Go's 2.1 MiB. Even with the RC runtime, the shared-struct tree links no heavy floor here — the binary is essentially the code.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| **kāra validate_bst**            | **7.00 MiB** |
| c    validate_bst                | 7.00 MiB |
| rust validate_bst                | 7.00 MiB |
| go   validate_bst                | 7.45 MiB |

All the compiled mirrors sit at the same ~7.0 MiB floor — each tree is built and freed inside the iteration, so steady state is flat across all 200,000 builds (no leak); Go's is a touch higher for its GC arena.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| **karac build validate_bst.kara** | **85.1 MiB** |
| clang -O3 validate_bst.c          | 96.7 MiB |
| rustc -O validate_bst.rs          | 105.4 MiB |

On this container karac has the lowest compile-memory footprint of the three.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — and the *right* Rust row here is `Rc<Node>` (refcounted), matching Kāra's `shared struct`. Against it kāra trails ~1.09×, a genuine (if modest) RC-codegen gap this container run surfaces, to be confirmed on the M5. C calibrates the raw-`malloc` floor, Go is the GC data point, Python the ergonomic foil. The load-bearing facts are the five-language sink agreement, the equal-semantics `Rc` comparison, and that kāra allocates+frees 200,000 trees with a flat memory floor (no RC leak) in the smallest binary of the four.
