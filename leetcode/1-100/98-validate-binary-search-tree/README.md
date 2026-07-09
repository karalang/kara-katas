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

> **Machine.** The numbers below are the corpus-canonical **Apple M5 Pro** (arm64; 6P+12E, Darwin 25.5.0) — directly comparable with the sibling M5 tables. The kata was originally measured on a shared x86-64 Linux cloud container; that run is **preserved verbatim in [`bench/results.container-x86.json`](bench/results.container-x86.json)** so a regression can be re-run on that host without re-deriving the baseline (its absolute times/sizes/RSS are *not* comparable here — different ISA and toolchains). `bench/results.json` records the M5 host and toolchain versions. The container's [flagged RC gap did not survive the M5 re-bench](#the-equal-memory-semantics-comparison) — see below.

**Workload.** A validation is O(n), and validating a *fixed* tree K times would be hoisted (a loop-invariant tree gives a constant result). So the bench is **build-then-validate**: each of **K = 200,000** iterations builds a fresh **63-node balanced BST** (an RC `shared struct TreeNode` tree) and runs the ★'s recursive `(lo, hi)`-bounds validator, folding `shift + valid?1:0` into a rolling hash. A per-iteration `shift = k%1000` makes each tree different (non-hoistable). This is **allocation-inclusive by design** — it stresses the RC / `Option` / recursion surface end to end (per-node RC alloc + drop in `build`, `match`-driven recursion in `is_valid`), the closest analogue being the linked-list katas [#19](../19-remove-nth-node-from-end-of-list/)/[#61](../61-rotate-list/). All four compiled mirrors must agree on `584566580` before timing.

### The equal-memory-semantics comparison

Kāra's recursive `TreeNode` is a **`shared struct` — RC-backed** (reference-counted). The default Rust mirror uses **`Box<Node>`** (unique ownership, *no* refcount), which is cheaper. The faithful like-for-like is **`Rc<Node>`** — so, exactly as [#69](../69-sqrtx/) adds a `-C overflow-checks=on` row for equal *safety*, this harness adds an `Rc<Node>` row for equal *memory semantics*.

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **Apple M5 Pro.**

| Implementation | Wall time | Node memory |
|---|---|---|
| go   validate_bst                       | 163.2 ± 2.6 ms | GC |
| c    validate_bst (clang -O3)           | 218.0 ± 3.5 ms | `malloc`/`free` |
| rust validate_bst (`Box<Node>`)         | 222.2 ± 4.1 ms | unique owned |
| rust validate_bst (`Rc<Node>`)          | 235.7 ± 4.6 ms | **refcounted** |
| **kāra validate_bst (`shared struct`)** | **237.8 ± 4.7 ms** | **refcounted (RC)** |

**On the M5, the equal-semantics comparison lands at parity** — the resolution the container run asked for. kāra's RC (237.8 ms) is a statistical tie with the faithful **Rust `Rc<Node>`** (235.7 ms) — **1.009×**, with the two error bars overlapping almost completely. The container had measured kāra ~1.09× *behind* `Rc` and flagged it "genuine RC/allocation codegen overhead… before it's treated as a tracked regression": on the canonical machine that gap **does not reproduce**. kāra's remaining +7% over Rust's `Box<Node>` (222.2 ms) is fully accounted for by the refcount itself — Rust pays +6% going `Box` → `Rc` (222.2 → 235.7 ms), and kāra's `shared struct` sits right on top of Rust's `Rc`. So the honest reading is: **kāra's RC codegen matches Rust's `Rc`; the only distance to `Box`/`malloc` is the cost of shared reference semantics, which any language pays.** This is the counterweight to [#61](../61-rotate-list/), where kāra *led* Rust because there the faithful Rust needed `Rc<RefCell>`.

One machine-dependent flip worth calling out honestly: **Go went from slowest to fastest.** On the slow container its GC dominated (527 ms, last of five); on the M5's fast cores its bump allocator + concurrent GC win this build-heavy tree workload outright (163.2 ms, ahead of raw C `malloc`). The five-language sink agreement on `584566580` holds on both hosts; only the ranking below C moved.

> **Container reference (x86-64 Linux, [`bench/results.container-x86.json`](bench/results.container-x86.json)).** For regression runs on that host, the original numbers were: c 362.5, rust `Box` 390.6, rust `Rc` 417.5, **kāra 453.4**, go 527.5 ms — i.e. kāra 1.09× behind `Rc` there. Absolute times are not comparable with the M5 table above; re-run `bench/bench.sh` on that container to reproduce the baseline.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py validate_bst` (K=20k) | 191.4 ± 1.1 ms |

Python at K=20k is ~0.19 s; projecting to the compiled mirrors' K=200k (~1.9 s) puts it **~8× slower than kāra seq** — a much narrower gap than the pure-compute katas because this workload is dominated by allocation and pointer-chasing, which CPython does in C.

### Compile elapsed (cold)

| Compiler | Time |
|---|---|
| clang -O3 validate_bst.c          | **40.0 ± 1.1 ms** |
| rustc -O validate_bst.rs          | 74.8 ± 3.7 ms |
| **karac build validate_bst.kara** | **76.7 ± 1.4 ms** |

On the M5 karac compiles at ~1.92× clang and ~1.03× rustc — a dead heat with rustc, both ~1.9× the bare-C floor.

### Binary size

| Implementation | Size |
|---|---|
| c    validate_bst                | 32.8 KiB |
| **kāra validate_bst**            | **33.1 KiB** |
| rust validate_bst                | 455.9 KiB |
| go   validate_bst                | 2.38 MiB |

Kāra's seq binary is **33.1 KiB — a hair over C's 32.8 KiB** and effectively tied with it (arm64 code runs larger than the container's x86-64 build), and it stays orders of magnitude below Rust's 456 KiB and Go's 2.38 MiB. Even with the RC runtime, the shared-struct tree links no heavy floor here — the binary is essentially the code.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    validate_bst                | 1.02 MiB |
| **kāra validate_bst**            | **1.03 MiB** |
| rust validate_bst                | 1.05 MiB |
| go   validate_bst                | 9.31 MiB |

The three non-GC mirrors sit at the same ~1.0 MiB floor — each tree is built and freed inside the iteration, so steady state is flat across all 200,000 builds (**no RC leak**); Go's 9.3 MiB is its GC arena, the same allocator that buys it the runtime lead above.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 validate_bst.c          | 2.5 MiB |
| **karac build validate_bst.kara** | **19.8 MiB** |
| rustc -O validate_bst.rs          | 26.8 MiB |

On the M5 karac's compile-memory footprint (19.8 MiB) sits below rustc's (26.8 MiB) and above bare clang's (2.5 MiB) — the prelude typecheck is the bulk of it.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — and the *right* Rust row here is `Rc<Node>` (refcounted), matching Kāra's `shared struct`. Against it kāra lands at **parity on the M5** (1.009×, a statistical tie); the container's ~1.09× was a slow-host artifact, not a codegen gap. C calibrates the raw-`malloc` floor, Go is the GC data point (which, on fast cores, wins outright here), Python the ergonomic foil. The load-bearing facts are the five-language sink agreement, the equal-semantics `Rc` parity, and that kāra allocates+frees 200,000 trees with a flat ~1.0 MiB memory floor (no RC leak) in a binary tied with C for smallest.
