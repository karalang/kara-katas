# 100. Same Tree

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Tree · Depth-First Search · Breadth-First Search · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/same-tree](https://leetcode.com/problems/same-tree/)

Given the roots of two binary trees `p` and `q`, decide whether they are **the same** — structurally identical *and* holding equal values at every corresponding node.

```
p:  1     q:  1        same        p:  1     q:  1      different
   / \       / \                      / \       / \    (value at the
  2   3     2   3       ->  true      2   1     1   2    left/right leaf)  ->  false
```

**Constraints:** `0 ≤ #nodes ≤ 100`, node values fit a signed 32-bit int.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Recursive lockstep compare** ★ | [`same_tree.kara`](same_tree.kara) ✓ | [`same_tree.py`](same_tree.py) ✓ |
| **Serialize both + string-compare** | [`same_tree_serial.kara`](same_tree_serial.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for both approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the two Kāra approaches agree with **each other** and with the Python mirror. An independent **ground-truth check** confirms the comparison: `is_same(p, q)` equals `serialize(p) == serialize(q)` on the case battery **and on 20,000 randomised fuzz trees**, zero mismatches. Both solvers compile with zero diagnostics.

## Two ways to compare

**Recursive lockstep** ([`same_tree.kara`](same_tree.kara), the ★) walks both trees in step: two empty subtrees match; an empty paired with a non-empty does not; otherwise the roots must share a value and the two left subtrees *and* the two right subtrees must both match. The `and` short-circuits on the first mismatch — the textbook one-pass solution.

```
is_same(p, q):
    both None         -> true
    exactly one None  -> false
    else              -> p.val == q.val
                         and is_same(p.left,  q.left)
                         and is_same(p.right, q.right)
```

**Serialize + compare** ([`same_tree_serial.kara`](same_tree_serial.kara)) instead emits a canonical preorder string for each tree — `val,` at a node, `#,` at an empty child — which encodes both shape (where the `#` markers land) and every value, then tests the two strings for equality. A distinct mechanism: two full serialization passes plus a string compare, rather than an early-terminating paired walk.

### A codegen bug this kata surfaced

A natural third approach — an **iterative** compare with two parallel worklist stacks of node-pairs (`Vec[Option[TreeNode]]`) — **leaks** on `karac build`: pushing a field-read `Option[shared]` handle (`stack.push(pn.left)`) onto the worklist and then dropping the stack with residual pairs (on an early `false` return) does not release the pushed handles, while a fresh `Some(..)` push into the same `Vec` is clean. Per the repo's "never route around — fix or file it" rule, that gap is filed as [`B-2026-07-12-4`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) with a minimal repro and clean counterpart; the two solvers shipped here avoid the residual-worklist shape and are byte-identical across every surface, valgrind-clean.

## Kāra features exercised

- **`shared struct TreeNode` (RC), read-only traversal** — both solvers walk the shared-node tree without mutating it; the recursive form passes `Option[TreeNode]` by value (a cheap RC-handle pass), the serialize form reads each node's `val`. Node type mirrors kata [#98](../98-validate-binary-search-tree/) / [#99](../99-recover-binary-search-tree/).
- **Nested `match` on paired `Option[shared]`** — the lockstep compare matches `p` and `q` together (`None`/`None`, `Some`/`Some`, mismatched), the four-way case analysis at the heart of the problem.
- **`and` short-circuit** — the recursive conjunction stops at the first differing node.
- **`mut ref String` serialization** — the second solver folds each tree into a canonical preorder string through a `mut ref String` accumulator, then compares the two.

**v1 note.** Trees stay within the `≤ 100`-node constraint. The sink folds each pair's boolean verdict into a running polynomial hash (order-sensitive). Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the serialize-equality + fuzz ground truth.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   same_tree.kara
karac build same_tree.kara && ./same_tree

# The serialize-and-compare variant (identical output):
karac run same_tree_serial.kara

# Python
python3 same_tree.py

# Verify they all agree
diff <(karac run same_tree.kara) <(python3 same_tree.py)         && echo OK
diff <(karac run same_tree.kara) <(karac run same_tree_serial.kara) && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`same_tree.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** Canonical numbers measured on the corpus's **Apple M5 Pro** (6P+12E, Darwin 25.5.0; `karac 0.1.0` from `main` `3b7af61f`, `rustc 1.95.0`, Apple clang 21.0.0, `go 1.26.3`, hyperfine 1.20) — [`bench/results.json`](bench/results.json). A shared x86-64 Linux cloud-container reference run is kept alongside in [`bench/results.container-x86.json`](bench/results.container-x86.json); absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. The ordering carries to the M5 but the gap compresses — and the M5 *reverses* the container's `ref`-borrow finding, see the note below the table.

**Workload.** Build 8 tree pairs once (15-node BSTs; half identical → full traversal, half differing by one value → short-circuit), then **K = 6,000,000** reps of recursive `is_same` on a **data-dependent-selected** pair (`idx = acc%8`, seeded by the running hash, so nothing hoists), folding each verdict into a rolling polynomial hash. Each mirror uses its natural read-only tree node: Kāra `shared` (RC), C/Go raw pointer, **Rust `Box` + `&`-borrow** (the tree is never mutated or shared in `is_same`, so single-owner `Box` traversed by reference is the honest Rust). All five compiled mirrors must agree on `718339783` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline) — though on a pure-traversal loop the fold's `acc*131` is the only arithmetic, so the overflow-check row barely moves.

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **Apple M5 Pro numbers.**

| Implementation | Wall time |
|---|---|
| c    same_tree (clang -O3, `*Node`)                 | 78.0 ± 1.1 ms |
| rust same_tree (rustc -O, overflow-checks=on)        | 78.4 ± 0.5 ms |
| rust same_tree (rustc -O, `Box` + borrow)           | 79.0 ± 0.9 ms |
| go   same_tree (`*Node`, GC)                        | 127.6 ± 3.3 ms |
| **kāra same_tree**                                  | **190.0 ± 4.4 ms** |

**Kāra trails on the corpus's most-exposed traversal — a read-only pointer chase with nothing to amortize.** Each rep is *only* `match` + field-access per node: no allocation, no compute, no strings, so any per-node overhead *is* the entire cost. On the M5 kāra is **2.44× behind C**, **2.41× behind Rust**, and **1.49× behind Go** — the same last-place ordering as the container, but the gap **compressed** (from 3.0× / 2.65× / 1.94×) on the wider out-of-order core, the tree-traversal compression flagged for the re-bench (cf. [#97](../97-interleaving-string/)). C, `Box`-borrow Rust, and overflow-checked Rust are a three-way tie at ~78 ms (the fold's `acc*131` is the only arithmetic, so the overflow row barely moves); Go is a clean 2nd (no per-rep allocation, so its GC never runs — 99.5 % CPU, no concurrent-GC help).

**The M5 reverses the container's `ref`-borrow finding — the gap is *not* refcounting.** On the container a `ref Option[TreeNode]` borrow variant (matching the mirrors' `&`/pointer traversal, no per-node rc-inc/dec) ran *faster* (~530 vs 596 ms), pinning ~11 % of the gap on by-value RC traffic. On the M5 that inverts: the committed by-value mirror is **188.8 ms** but the borrow variant ([`bench/same_tree_ref.kara`](bench/same_tree_ref.kara), same sink) is **217.6 ms — 15 % *slower***. Passing a `ref` hands the callee a pointer it must load through on every access; on the M5's fast core that per-node indirection costs *more* than the rc-inc/dec it removes (the retain traffic being cheap here — predicted and pipelined). So borrow-elision is **not** the lever on the M5: the entire 2.44× gap to C is Kāra's per-node **`Option[shared]` traversal codegen** — niche-decode + `match` + GEP the shared field vs C/Rust's raw null-check-and-deref — with nothing in the loop to hide it behind. **Leaner `Option[shared]` match/field lowering** is the real headroom here, flagged as such. This is the read-only-walk analogue of [#95](../95-unique-binary-search-trees-ii/)'s pure-allocation regime; the compute/check-bound siblings ([#96](../96-unique-binary-search-trees/) fastest, [#99](../99-recover-binary-search-tree/) ahead of `Rc<RefCell>`) bracket it from the other side. kāra holds **1.0 MiB** RSS and a **33.3 KiB** binary (both C parity; the container's ~332 KB was the backtrace-symbolizer build-linkage artifact, stripped correctly here) vs Go's 2.7 MiB / 2.4 MB. Python is listed at **156 ms but ran K = 300,000 — 1/20 of the compiled iterations** (timed separately, not cross-checked), so its wall-clock is not comparable.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.json`](bench/results.json) (M5, canonical) and [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched read-only tree traversal (`shared` handle walk vs `Box` + `&`-borrow), where the per-node `Option[shared]` lowering is isolated as the gap (a later probe finds refcounting elided — by-value times identically to `ref`-borrow — so the earlier container "~11 %" RC split is superseded; see kara B-2026-07-15-21). C's raw pointer chase is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
