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

> ✅ **M5 re-bench (2026-11-01).** The numbers below are the corpus-canonical **Apple M5 Pro** (arm64; 6P+12E, Darwin 25.6.0), measured with **karac g6697158fa** (0.9.0-dev.14057, the v2/MIR backend; the legacy backend was deleted 2026-10-23), rustc 1.95, clang 21, go 1.26 — directly comparable with the sibling M5 tables. kāra's ratio to every comparator is flat against the 2026-07-28 legacy-backend snapshot (kāra/Rust `Box` 1.06× → 1.09×, kāra/C 1.08× → 1.12×, kāra/Go 1.52× → 1.44×; every move under 10 %). The kata was originally measured on a shared x86-64 Linux cloud container; that run is **preserved verbatim in [`bench/results.container-x86.json`](bench/results.container-x86.json)** so a regression can be re-run on that host without re-deriving the baseline (its absolute times/sizes/RSS are *not* comparable here — different ISA and toolchains). `bench/results.json` records the M5 host and toolchain versions. The container's [flagged RC gap did not survive the M5 re-bench](#the-equal-memory-semantics-comparison) — see below.

**Workload.** A validation is O(n), and validating a *fixed* tree K times would be hoisted (a loop-invariant tree gives a constant result). So the bench is **build-then-validate**: each of **K = 200,000** iterations builds a fresh **63-node balanced BST** (an RC `shared struct TreeNode` tree) and runs the ★'s recursive `(lo, hi)`-bounds validator, folding `shift + valid?1:0` into a rolling hash. A per-iteration `shift = k%1000` makes each tree different (non-hoistable). This is **allocation-inclusive by design** — it stresses the RC / `Option` / recursion surface end to end (per-node RC alloc + drop in `build`, `match`-driven recursion in `is_valid`), the closest analogue being the linked-list katas [#19](../19-remove-nth-node-from-end-of-list/)/[#61](../61-rotate-list/). All four compiled mirrors must agree on `584566580` before timing.

### The equal-memory-semantics comparison

Kāra's recursive `TreeNode` is a **`shared struct` — RC-backed** (reference-counted). The default Rust mirror uses **`Box<Node>`** (unique ownership, *no* refcount), which is cheaper. The faithful like-for-like is **`Rc<Node>`** — so, exactly as [#69](../69-sqrtx/) adds a `-C overflow-checks=on` row for equal *safety*, this harness adds an `Rc<Node>` row for equal *memory semantics*.

`--warmup 5 --runs 30 --shell=none`. All single-threaded, ~99.8 % CPU (the default build emits no call of `karac_mir_task_spawn`, verified in the emitted IR (`KARAC_MIR_LL`), same as its `KARAC_AUTO_PAR=0` twin). **Apple M5 Pro, karac g6697158fa, 2026-11-01.**

| Implementation | Wall time | Node memory |
|---|---|---|
| go   validate_bst                       | 189.4 ± 3.6 ms | GC |
| c    validate_bst (clang -O3)           | 245.2 ± 11.6 ms | `malloc`/`free` |
| rust validate_bst (`Box<Node>`, overflow-checks=on) | 249.1 ± 14.6 ms | unique owned |
| rust validate_bst (`Box<Node>`)         | 251.4 ± 12.1 ms | unique owned |
| rust validate_bst (`Rc<Node>`)          | 255.0 ± 6.8 ms | **refcounted** |
| **kāra validate_bst (`shared struct`)** | **273.4 ± 11.9 ms** | **refcounted (RC)** |

**On the M5 the equal-semantics comparison is close but no longer a tie.** kāra's RC (273.4 ms) is **1.07× behind** the faithful **Rust `Rc<Node>`** (255.0 ms), 1.09× behind `Box<Node>` and 1.10× behind equal-safety `Box` with `-C overflow-checks=on`. Earlier M5 snapshots had kāra at 1.01× (the first M5 table) and 1.02× (2026-07-28) of `Rc`; the move to 1.07× is under this session's 10 % noise floor (four of the six rows carry σ of 5–6 %), so it is read as flat, not filed. The container had measured kāra ~1.09× *behind* `Rc` and flagged it "genuine RC/allocation codegen overhead… before it's treated as a tracked regression". What changed in the explanation: Rust now pays only **+1.4 %** going `Box` → `Rc` (251.4 → 255.0 ms), so the refcount alone no longer accounts for kāra's distance to `Box`/`malloc` — about 7 points of it sit on kāra's side of the `Rc` row. This is the counterweight to [#61](../61-rotate-list/), where kāra *led* Rust because there the faithful Rust needed `Rc<RefCell>`.

One machine-dependent flip worth calling out honestly: **Go went from slowest to fastest.** On the slow container its GC dominated (527 ms, last of five); on the M5's fast cores its bump allocator + concurrent GC win this build-heavy tree workload outright (189.4 ms, 1.29× ahead of raw C `malloc`; 119 % CPU). The five-language sink agreement on `584566580` holds on both hosts; only the ranking below C moved.

> **Container reference (x86-64 Linux, [`bench/results.container-x86.json`](bench/results.container-x86.json)).** For regression runs on that host, the original numbers were: c 362.5, rust `Box` 390.6, rust `Rc` 417.5, **kāra 453.4**, go 527.5 ms — i.e. kāra 1.09× behind `Rc` there. Absolute times are not comparable with the M5 table above; re-run `bench/bench.sh` on that container to reproduce the baseline.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py validate_bst` (K=20k) | 191.4 ± 1.1 ms (earlier run, not re-run 2026-11-01) |

Python at K=20k is ~0.19 s; projecting to the compiled mirrors' K=200k (~1.9 s) puts it **~7× slower than kāra seq** (273.4 ms) — a much narrower gap than the pure-compute katas because this workload is dominated by allocation and pointer-chasing, which CPython does in C.

### Compile elapsed (cold)

| Compiler | Time |
|---|---|
| clang -O3 validate_bst.c          | **46.1 ± 0.9 ms** |
| rustc -O validate_bst.rs          | 81.6 ± 1.1 ms |
| **karac build validate_bst.kara** | **115.4 ± 1.7 ms** |

On the M5 karac compiles at ~2.50× clang and ~1.41× rustc (2026-11-01; the legacy backend had been a dead heat with rustc).

### Binary size

| Implementation | Size |
|---|---|
| c    validate_bst                | 32.8 KiB |
| **kāra validate_bst**            | **295.8 KiB** |
| rust validate_bst                | 455.9 KiB |
| go   validate_bst                | 2.38 MiB |

Kāra's seq binary is **295.8 KiB** — 9× C's 32.8 KiB, still below Rust's 456 KiB and Go's 2.38 MiB. Every MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (this kata's legacy build was 33.1 KiB, tied with C), tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md).

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    validate_bst                | 1.00 MiB |
| **kāra validate_bst**            | **1.05 MiB** |
| rust validate_bst                | 1.08 MiB |
| go   validate_bst                | 9.88 MiB |

The three non-GC mirrors sit at the same ~1.0 MiB floor — each tree is built and freed inside the iteration, so steady state is flat across all 200,000 builds (**no RC leak**); Go's 9.9 MiB is its GC arena, the same allocator that buys it the runtime lead above.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 validate_bst.c          | 2.6 MiB |
| rustc -O validate_bst.rs          | 26.7 MiB |
| **karac build validate_bst.kara** | **59.0 MiB** |

On the M5 karac's compile-memory footprint (59.0 MiB, 2026-11-01) now sits above rustc's (26.7 MiB; 2.2×) and far above bare clang's (2.6 MiB); the legacy backend's was 19.8 MiB, below rustc.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — and the *right* Rust row here is `Rc<Node>` (refcounted), matching Kāra's `shared struct`. Against it kāra lands **1.07× behind on the M5** (2026-11-01; earlier M5 snapshots 1.01–1.02×), inside this session's noise floor; the container measured ~1.09×. C calibrates the raw-`malloc` floor, Go is the GC data point (which, on fast cores, wins outright here), Python the ergonomic foil. The load-bearing facts are the five-language sink agreement, the equal-semantics `Rc` parity, and that kāra allocates+frees 200,000 trees with a flat ~1.0 MiB memory floor (no RC leak).
