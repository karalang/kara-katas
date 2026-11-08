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

- **`shared struct TreeNode` (RC), read-only crossed walk** — the ★ compares two subtrees in the crossed lockstep that defines mirroring, without mutating anything. Node type mirrors kata [#100](../../1-100/100-same-tree/).
- **Recursive deep clone with a swap** (`mirror`) — the test *trees* are constructed as `root { left: L, right: mirror(L) }`, where `mirror` deep-clones a subtree swapping left/right at every level (the RC-clone surface hardened by [#95](../../1-100/95-unique-binary-search-trees-ii/)'s fixes); a plain `copy_tree` builds the asymmetric cases.
- **Nested `match` on paired `Option[shared]`** — the four-way `None`/`Some` case analysis on the two crossed children.
- **`mut ref String` double serialization** — the second solver emits a normal and a mirror preorder through `mut ref String` accumulators and compares them.

**v1 note.** Trees stay within the `≤ 1000`-node constraint. The sink folds each tree's boolean verdict into a running polynomial hash (order-sensitive). Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the preorder-vs-mirror-preorder + fuzz ground truth.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`80745775`). Workload: build 8 trees once, then K=8000000 reps of recursive is_symmetric on a data-dependent-selected tree (idx=acc%8), folding each verdict into a rolling polynomial hash.

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-11-01, karac g6697158fa (v2/MIR backend) (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O -C overflow-checks=on` (equal-safety) | 117.6 ms | 0.90× |
| Rust `-O` | 118.1 ms | 0.90× |
| C `clang -O3` | 121.8 ms | 0.93× |
| **Kāra (codegen)** | 131.3 ms | 1.00× |
| Go | 222.0 ms | 1.69× |

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

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

> ✅ **M5 re-bench (2026-11-01).** The canonical numbers below are the corpus's **Apple M5 Pro** run (6P+12E, Darwin 25.6.0; **karac g6697158fa** (0.9.0-dev.14057, the v2/MIR backend; the legacy backend was deleted 2026-10-23), `rustc 1.95.0`, Apple clang 21.0.0, `go 1.26.3`, hyperfine 1.20) — [`bench/results.json`](bench/results.json). Against the 2026-07-27 legacy-backend snapshot kāra is flat against every comparator: kāra/Rust 1.12× → 1.11×, kāra/C 1.13× → 1.08×, kāra/Go 0.62× → 0.59×. A shared **x86-64 Linux cloud-container** reference run is kept alongside in [`bench/results.container-x86.json`](bench/results.container-x86.json); absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. History: on the **pre-fix** container run kāra trailed the seq leader by **3.01×** (Rust 2.87×); the **post-fix M5** run (2026-07-15, legacy backend) closed that to **1.14×** (Rust 1.13×) — default-ON RC-elision + a tail-call unblock roughly halved the walk (**256.1 → 123.0 ms**), so the former gap was the per-node refcount traffic, now elided.

**Workload.** Build 8 trees once (15-node subtrees; even index symmetric via a mirrored subtree, odd index asymmetric via a plain-copied subtree), then **K = 8,000,000** reps of recursive `is_symmetric` on a **data-dependent-selected** tree (`idx = acc%8`, seeded by the running hash, so nothing hoists), folding each verdict into a rolling polynomial hash. Each mirror uses its natural read-only tree node: Kāra `shared` (RC), C/Go raw pointer, **Rust `Box` + `&`-borrow**. All five compiled mirrors must agree on `80745775` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../../1-100/69-sqrtx/)'s discipline) — though on a pure-traversal loop the fold's `acc*131` is the only arithmetic, so it barely moves.

`--warmup 5 --runs 30 --shell=none`. All single-threaded, ~99 % CPU (the default build emits no call of `karac_mir_task_spawn`, verified in the emitted IR (`KARAC_MIR_LL`), same as its `KARAC_AUTO_PAR=0` twin). **Apple M5 Pro numbers, karac g6697158fa, 2026-11-01** (canonical; sink `80745775` agreed by all five mirrors before timing):

Note (2026-11-07, karac g97681763d, seq lane re-benched with `KARAC_AUTO_PAR=0`): Kāra now reads 1.83× equal-safety Rust, 1.79× `rustc -O`, 1.90× C and 1.03× Go. The 2026-11-01 standing above came from a build that left auto-par on. That gap was kara B-2026-11-07-55 (bf1ae02cf1), fixed at b5581f4232: re-benched on the M5 at karac gda99ff05d, Kāra reads 97.5 ms, 0.87× equal-safety Rust and `rustc -O`, 0.89× C and 0.49× Go.

| Implementation | Wall time |
|---|---|
| rust is_symmetric (rustc -O, overflow-checks=on)     | 117.6 ± 5.9 ms |
| rust is_symmetric (rustc -O, `Box` + borrow)        | 118.1 ± 5.2 ms |
| c    is_symmetric (clang -O3, `*Node`)              | 121.8 ± 2.2 ms |
| **kāra is_symmetric**                               | **131.3 ± 2.4 ms** |
| go   is_symmetric (`*Node`, GC)                     | 222.0 ± 3.5 ms |

kāra is **1.12×** the seq leader (equal-safety Rust), **1.11×** stock Rust, **1.08×** C, and **1.69× faster than Go** (it was 1.30× *slower* than Go pre-fix). This is the read-only crossed-traversal twin of [#100](../../1-100/100-same-tree/) (same-tree): a pointer-chase with `match` + field-access per node and nothing to amortize, so Kāra's per-node cost is the exposed one — and, as #100's note now documents from the object code, that cost was **dominated by refcount traffic** (per-node retains/releases), not the ~11% earlier believed. The [`B-2026-07-15-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) fix (default-ON RC-elision + a tail-call unblock) elides it, halving the walk **256.1 → 123.0 ms** (2026-07-15, legacy backend). On the M5, C, Rust, and overflow-checked Rust land in a near tie (117.6–121.8 ms, within ~1σ of each other) — the fold's lone `acc*131` makes the overflow check free, as expected on a pure-traversal loop. Compile-cold on the M5 is clang 51.6 ms < rustc 103.4 ms < **karac 126.5 ms** (2.5× clang, 1.22× rustc). Compile-cold, binary size, and peak-RSS records are in [`bench/results.json`](bench/results.json) (M5, canonical) and [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference). Binary size: c 32.9 KiB, **kāra 295.8 KiB**, rust 456.7 KiB, go 2.39 MiB; every MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (the legacy M5 kāra binary here was 33.5 KiB), tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). Peak RSS: kāra **1.08 MiB**, on par with Rust (1.08) and C (1.03), vs Go's 2.56 MiB.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched read-only tree traversal (`shared` handle walk vs `Box` + `&`-borrow). C's raw pointer chase is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
