# 101. Symmetric Tree

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Tree · Depth-First Search · Breadth-First Search · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/symmetric-tree](https://leetcode.com/problems/symmetric-tree/)

Given the root of a binary tree, decide whether it is **a mirror of itself** — symmetric around its center.

```
      1              1
     / \            / \
    2   2          2   2
   / \ / \          \   \
  3  4 4  3          3   3

  symmetric  ->  true      not symmetric  ->  false
```

**Constraints:** `1 ≤ #nodes ≤ 1000`, node values fit a signed 32-bit int.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Recursive crossed-lockstep mirror check** ★ | [`is_symmetric.kara`](is_symmetric.kara) ✓ | [`is_symmetric.py`](is_symmetric.py) ✓ |
| **Preorder vs mirror-preorder serialization** | [`is_symmetric_serial.kara`](is_symmetric_serial.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for both approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the two Kāra approaches agree with **each other** and with the Python mirror. An independent **ground-truth check** confirms the test: `is_symmetric(root)` equals "normal preorder `==` mirror preorder" on the case battery **and on 20,000 randomised fuzz trees** (forced-symmetric and arbitrary), zero mismatches. Both solvers compile with zero diagnostics.

## Two ways to test symmetry

**Recursive crossed-lockstep** ([`is_symmetric.kara`](is_symmetric.kara), the ★): a tree is symmetric iff its left and right subtrees are mirror images, and two subtrees mirror when their roots share a value and — the crucial *cross* — the left's LEFT child mirrors the right's RIGHT child while the left's RIGHT child mirrors the right's LEFT child. Walk both in that crossed step, short-circuiting on the first mismatch:

```
is_mirror(a, b):
    both None         -> true
    exactly one None  -> false
    else              -> a.val == b.val
                         and is_mirror(a.left,  b.right)   # cross
                         and is_mirror(a.right, b.left)    # cross
```

**Preorder vs mirror-preorder** ([`is_symmetric_serial.kara`](is_symmetric_serial.kara)): a tree equals its own mirror iff a normal preorder serialization (root, LEFT, RIGHT) reads the same as a **mirror** preorder (root, RIGHT, LEFT). Both encode shape via `#` null-markers and every value, so the two strings are equal exactly when the tree is symmetric — a distinct mechanism (two full serialization passes plus a string compare) that must land on the identical verdict.

## Kāra features exercised

- **`shared struct TreeNode` (RC), read-only crossed walk** — the ★ compares two subtrees in the crossed lockstep that defines mirroring, without mutating anything. Node type mirrors kata [#100](../100-same-tree/).
- **Recursive deep clone with a swap** (`mirror`) — the test *trees* are constructed as `root { left: L, right: mirror(L) }`, where `mirror` deep-clones a subtree swapping left/right at every level (the RC-clone surface hardened by [#95](../95-unique-binary-search-trees-ii/)'s fixes); a plain `copy_tree` builds the asymmetric cases.
- **Nested `match` on paired `Option[shared]`** — the four-way `None`/`Some` case analysis on the two crossed children.
- **`mut ref String` double serialization** — the second solver emits a normal and a mirror preorder through `mut ref String` accumulators and compares them.

**v1 note.** Trees stay within the `≤ 1000`-node constraint. The sink folds each tree's boolean verdict into a running polynomial hash (order-sensitive). Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the preorder-vs-mirror-preorder + fuzz ground truth.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   is_symmetric.kara
karac build is_symmetric.kara && ./is_symmetric

# The serialize-vs-mirror-serialize variant (identical output):
karac run is_symmetric_serial.kara

# Python
python3 is_symmetric.py

# Verify they all agree
diff <(karac run is_symmetric.kara) <(python3 is_symmetric.py)              && echo OK
diff <(karac run is_symmetric.kara) <(karac run is_symmetric_serial.kara)   && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`is_symmetric.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** The canonical numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json). The corpus's canonical **Apple M5 Pro** numbers ([`bench/results.json`](bench/results.json)) are folded in separately; absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. Re-run `bench.sh` on the M5 to refresh the canonical table.

**Workload.** Build 8 trees once (15-node subtrees; even index symmetric via a mirrored subtree, odd index asymmetric via a plain-copied subtree), then **K = 8,000,000** reps of recursive `is_symmetric` on a **data-dependent-selected** tree (`idx = acc%8`, seeded by the running hash, so nothing hoists), folding each verdict into a rolling polynomial hash. Each mirror uses its natural read-only tree node: Kāra `shared` (RC), C/Go raw pointer, **Rust `Box` + `&`-borrow**. All five compiled mirrors must agree on `80745775` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline) — though on a pure-traversal loop the fold's `acc*131` is the only arithmetic, so it barely moves.

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **x86-64 container numbers** (canonical M5 pending; see the machine note):

| Implementation | Wall time |
|---|---|
| c    is_symmetric (clang -O3, `*Node`)              | 197.3 ± 5.2 ms |
| rust is_symmetric (rustc -O, overflow-checks=on)     | 201.6 ± 2.3 ms |
| rust is_symmetric (rustc -O, `Box` + borrow)        | 207.1 ± 11.2 ms |
| go   is_symmetric (`*Node`, GC)                     | 361.1 ± 4.7 ms |
| **kāra is_symmetric**                               | **594.8 ± 11.3 ms** |

This is the read-only crossed-traversal twin of [#100](../100-same-tree/) (same-tree): a pointer-chase with `match` + field-access per node and nothing to amortize, so Kāra's per-node RC/traversal overhead is again the exposed cost — see #100's benchmark note for the profiled RC-retain-vs-traversal-codegen split (~11 % / the rest). Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference) and, once folded in, [`bench/results.json`](bench/results.json) (M5, canonical). The kāra binary size there is a symbolizer-inflated build-linkage artifact (~15 KB on a correct build), independent of the runtime numbers.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched read-only tree traversal (`shared` handle walk vs `Box` + `&`-borrow). C's raw pointer chase is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
