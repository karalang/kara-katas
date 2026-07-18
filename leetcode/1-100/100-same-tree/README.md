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

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **Apple M5 Pro numbers, post-fix** — measured on the fixed [kara `B-2026-07-15-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) compiler (default-ON RC-elision + a tail-call unblock). The awaited M5 re-bench confirmed the container reference's prediction: the fix roughly **halved** the Kāra row — **190.0 ms → 97.1 ms (−49%)** — while every other mirror held within noise (C/Rust/Go all ±<2%), moving Kāra from 2.44× behind C to just off the C/Rust cluster:

| Implementation | Wall time |
|---|---|
| c    same_tree (clang -O3, `*Node`)                 | 77.7 ± 0.7 ms |
| rust same_tree (rustc -O, overflow-checks=on)        | 77.9 ± 0.5 ms |
| rust same_tree (rustc -O, `Box` + borrow)           | 78.6 ± 2.4 ms |
| go   same_tree (`*Node`, GC)                        | 129.2 ± 2.8 ms |
| **kāra same_tree**                                  | **97.1 ± 0.8 ms** |

**This kata is where the corpus's read-only-traversal RC gap was root-caused and fixed.** Each rep is *only* `match` + field-access per node: no allocation, so any per-node overhead *is* the entire cost — which made this the corpus's most-exposed traversal and the one that surfaced [kara `B-2026-07-15-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl). At **97.1 ms** the fixed Kāra walk is **1.25× C** and **1.24× the equal-safety Rust** row; the pre-fix compiler had been 2.44× behind C (190.0 ms), and this kata is where that gap was root-caused.

**The earlier "the gap is *not* refcounting" conclusion was wrong — and this kata is why we know.** That claim rested on a `ref`-borrow variant ([`bench/same_tree_ref.kara`](bench/same_tree_ref.kara)) timing *slower* than the by-value mirror on the M5, read as "RC is free." But `ref` slower than by-value only shows `ref`'s per-node pointer indirection is expensive — it says nothing about whether the by-value walk's refcount traffic is free, because *both* variants carried the same RC (neither elided it). The decisive test is by-value-**with**-RC vs by-value-**without**, which the fix now provides: on the container the by-value `is_same` walk goes **0.454 s → 0.206 s (2.2×)** once the per-node retains/releases are elided. So RC was a *major* cost here, not a free one — the object code showed **two retains + two releases per visited node**. The fix makes RC-elision default-ON and, because `is_same`'s `and` short-circuit puts the last recursion in tail position, additionally unblocks LLVM's tail-call→loop conversion (`B-2026-07-15-21` Part B).

The M5 **residual** (1.25× C / 1.24× Rust) is the per-node `Option[shared]` decode plus the deliberate overflow check; leaner niche/match lowering is the remaining headroom, but the dominant tax (RC + a blocked tail-call) is gone. The x86 **container reference** corroborates cross-platform: kāra **210.0 ± 5.4 ms**, **1.17× the equal-safety Rust row (180 ms)** and 1.23× behind C (170.8 ms) — the same "just off the C/Rust cluster" verdict on a different bottleneck mix. This is the read-only-walk analogue of [#95](../95-unique-binary-search-trees-ii/)'s pure-allocation regime; the compute/check-bound siblings ([#96](../96-unique-binary-search-trees/) fastest, [#99](../99-recover-binary-search-tree/) ahead of `Rc<RefCell>`) bracket it from the other side. kāra holds **1.0 MiB** RSS and a **33.6 KiB** binary (both C parity; the container's ~332 KB was the backtrace-symbolizer build-linkage artifact, stripped correctly here) vs Go's 2.7 MiB / 2.4 MB. Python is listed at **153 ms but ran K = 300,000 — 1/20 of the compiled iterations** (timed separately, not cross-checked), so its wall-clock is not comparable.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.json`](bench/results.json) (M5, canonical) and [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched read-only tree traversal (`shared` handle walk vs `Box` + `&`-borrow). This is the kata that root-caused the per-node refcount-traffic gap now fixed in [kara `B-2026-07-15-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) (default-ON RC-elision + a tail-call unblock), after which the `shared`-handle walk runs at 1.24× the equal-safety `Box`+`&`-borrow on the M5 (1.17× on the x86 container reference). C's raw pointer chase is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
