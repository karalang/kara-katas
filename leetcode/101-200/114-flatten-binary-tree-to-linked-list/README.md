# 114. Flatten Binary Tree to Linked List

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Stack · Tree · Depth-First Search · Binary Tree · Linked List &nbsp;·&nbsp; **Source:** [leetcode.com/problems/flatten-binary-tree-to-linked-list](https://leetcode.com/problems/flatten-binary-tree-to-linked-list/)

Flatten the tree **in place** into a "linked list": every node's `right` points to the next node in **pre-order**, and every `left` is null. The first mutating tree kata of this stretch — where [#112](../112-path-sum/) / [#113](../113-path-sum-ii/) only *read* the shared nodes, this one *rewrites* their `left`/`right` fields.

```
    1              pre-order 1,2,3,4,5,6         1
   / \                                           \
  2   5     flatten -->                           2
 / \   \                                           \
3   4   6                                           3
                                                     \
                                                      4
                                                       \
                                                        5
                                                         \
                                                          6
```

**Constraints:** `0 ≤ #nodes ≤ 2000`, node values fit `-100 … 100`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Iterative Morris rewiring, O(1) space** ★ | [`flatten.kara`](flatten.kara) ✓ | [`flatten.py`](flatten.py) ✓ |
| **Recursive, return the pre-order tail** | [`flatten_recursive.kara`](flatten_recursive.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for both approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the two Kāra approaches agree with **each other** and with the Python mirror. An independent **ground-truth check** confirms the flattening three ways: the iterative Morris rewiring equals the recursive tail-return *and* the literal invariant — **the flattened right-spine's values equal the original tree's pre-order traversal, with every `left` null** — on a case battery **and 20,000 randomised trees**, zero disagreements. Both solvers compile with zero diagnostics and are valgrind-clean.

## 🐛 This kata found (and fixed) a compiler bug

Writing the natural harness — `let root = if cond { build_balanced(..) } else { build_bst(..) }; flatten(root); spine_hash(root)` — **heap-corrupted under `karac build`/`karac run`** (glibc `malloc(): unaligned tcache chunk`) while `karac run --interp` was correct. Root-caused to [kara `B-2026-07-16-9`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl): an `Option[shared]` bound from an **`if`/`match`/block expression**, then used more than once by value, was freed after the first use — a use-after-free. The `let`-binding RC registration matched only single RHS shapes (a call, a `Some(..)`, a `v[i]`, …) and never looked inside a control-flow expression, so the binding was never entered into the caller-retains bookkeeping. Same class as two earlier fixes (`Some(..)` RHS / `v[i]` RHS), extended to control-flow-expression RHSs. Fixed in the compiler (not worked around here) — the kata now runs clean across all surfaces. This is the dogfood loop doing exactly its job: a natural mutating-tree program surfaced a memory-safety hole a read-only walk never would.

## Two rewiring mechanisms

**Iterative Morris** ([`flatten.kara`](flatten.kara), the ★): O(1) extra space. At each node with a left child, walk to the left subtree's **rightmost** node (the pre-order predecessor of the current right subtree), splice the right subtree onto it, move the left subtree over to `right`, null `left`, and advance to `right`.

```
curr = root
while curr:
    if curr.left:
        prev = rightmost(curr.left)
        prev.right = curr.right      # splice right subtree onto the left subtree's tail
        curr.right = curr.left       # move left subtree to right
        curr.left  = None
    curr = curr.right
```

**Recursive, return the tail** ([`flatten_recursive.kara`](flatten_recursive.kara)): post-order recursion. Flatten both children, then — if a left subtree exists — splice the right subtree onto the left subtree's returned tail, shift left→right, and return the subtree's overall pre-order tail (right's tail, else left's, else the node). A distinct mechanism (recursion returning a handle vs an iterative predecessor-find) that must produce the identical flattening.

## Kāra features exercised

- **In-place `mut` field mutation on `shared` nodes** — both solvers write `c.right = c.left`, `c.left = None`, `prev.right = c.right` through `shared struct TreeNode` handles; the RC layer keeps every still-reachable node alive as the pointers are rewired. Same in-place-mutation surface as [#226](../../201-300/226-invert-binary-tree/) (invert), the mutating counterpart to #112/#113's read-only walks.
- **`Option[shared]` cursor advance** (`curr = c.right`) and a nested predecessor-find loop (`prev = r`) — reassigning shared handles as the walk proceeds.
- **`Option[shared]` from a control-flow expression** — `let root = if .. { build(..) } else { build(..) }` used by value across `flatten` + `spine_hash`; the exact shape that surfaced and now regression-pins [kara `B-2026-07-16-9`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl).
- **Two construction shapes** — balanced trees (middle-pick) and pseudo-random BSTs (LCG insert), so flatten runs over both dense and skewed structures.

**v1 note.** Trees stay within the `≤ 2000`-node constraint. The sink folds each flattened tree's spine hash (values + an all-left-null assertion) into a running accumulator. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the recursive + pre-order ground truth, and are valgrind-clean.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   flatten.kara
karac build flatten.kara && ./flatten

# The recursive variant (identical output):
karac run flatten_recursive.kara

# Python
python3 flatten.py

# Verify they all agree
diff <(karac run flatten.kara) <(python3 flatten.py)            && echo OK
diff <(karac run flatten.kara) <(karac run flatten_recursive.kara) && echo OK

# Ground truth: Morris == recursive == original pre-order, all lefts null (battery + 20k fuzz)
python3 ground_truth.py
```

## Benchmarks
Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`flatten.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5 re-bench (2026-11-01).** The canonical numbers below are the corpus's **Apple M5 Pro** run (6P+12E, Darwin 25.6.0; **karac g6697158fa** (0.9.0-dev.14057, the v2/MIR backend; the legacy backend was deleted 2026-10-23), `rustc 1.95.0`, Apple clang 21.0.0, `go 1.26.3`, hyperfine 1.20) — [`bench/results.json`](bench/results.json). Against the 2026-07-27 legacy-backend M5 snapshot kāra is flat against every comparator (each move under this session's ~10 % noise band): kāra/Rust 0.93× → 0.90×, kāra/equal-safety Rust 0.93× → 0.91×, kāra/C 1.33× → 1.36×, kāra/Go 1.72× → 1.57×. An earlier shared **x86-64 Linux cloud-container** run, which this section originally reported as canonical, is kept below as history; absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal.

**Workload.** Flatten is *destructive* (it rewires the tree into a right-spine in place), so each rep builds a fresh **63-node** balanced tree over a **data-dependent** value range (`base = acc%100`, seeded by the running hash so nothing hoists), flattens it with the O(1)-space Morris rewiring, and folds the spine hash — **K = 200,000** reps. This is the **mutate regime**: shared-node allocation (63 RC nodes built + freed) plus in-place pointer rewiring per rep, distinct from #112's read-only walk and #113's collect-and-copy.

**Node representation & equal safety.** A cursor-driven in-place rewiring of an aliased linked structure is awkward in Rust's ownership model, so the mirrors span the safety spectrum: **C** (`*Node`) and **Go** (`*Node`, GC) chase raw pointers; **Rust** uses **`Rc<RefCell<Node>>`** — the *safe* interior-mutability peer to Kāra's `shared` (RC), with the caveat that an *unsafe* raw-pointer Rust would match C. Kāra's `shared` is RC too, but **without** `RefCell`'s runtime borrow flag (the compiler's ownership analysis discharges that statically). Kāra checks integer overflow by default; the `rustc -O -C overflow-checks=on` row is the like-for-like on the hash fold.

`--warmup 5 --runs 30 --shell=none`. Single-threaded mirrors, ~99.7 % CPU (the default kāra build emits no call of `karac_mir_task_spawn`, verified in the emitted IR (`KARAC_MIR_LL`), same as its `KARAC_AUTO_PAR=0` twin; Go's runtime runs at 114 % CPU, 230.5 ms user). **Apple M5 Pro numbers, karac g6697158fa, 2026-11-01** (canonical; sink `538693327` agreed by all five mirrors):

| Implementation | Wall time | Node representation |
|---|---|---|
| go   flatten (GC `*Node`)                           | 232.6 ± 4.9 ms | `*Node` |
| c    flatten (clang -O3)                            | 268.3 ± 13.0 ms | `*Node` (raw) |
| **kāra flatten**                                    | **364.9 ± 12.6 ms** | **`shared` (RC)** |
| rust flatten (rustc -O, overflow-checks=on)          | 399.8 ± 12.6 ms | `Rc<RefCell>` |
| rust flatten (rustc -O)                             | 404.6 ± 7.3 ms | `Rc<RefCell>` |

**On the M5 (2026-11-01, v2/MIR) Kāra still beats Rust's safe `Rc<RefCell>`, but Go and C both lead.** Kāra runs at **0.90× stock `rustc -O`** (404.6 ms) and **0.91× equal-safety Rust** (399.8 ms), **1.36× behind C** (268.3 ms), and **1.57× behind Go** (232.6 ms wall, 230.5 ms user) — on the M5, Go's GC handles the per-rep 63-node tree churn better than either RC model, the reverse of the container ordering below. kāra holds **1.03 MiB** peak RSS (C 1.02, Rust 1.06) vs Go's **9.84 MiB**. Binary size: c 32.8 KiB, **kāra 295.8 KiB**, rust 456.4 KiB, go 2.38 MiB; every MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (the legacy M5 kāra binary here was 33.3 KiB), tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). Compile-cold on the M5 is clang 45.6 ms < rustc 103.5 ms < **karac 122.0 ms** (2.7× clang, 1.18× rustc).

**x86-64 container numbers** (history: the earlier, undated container run this section first reported; [`bench/results.container-x86.json`](bench/results.container-x86.json) now holds a later 2026-10-30 container run, not reproduced here):

| Implementation | Wall time | Node representation |
|---|---|---|
| c    flatten (clang -O3)                            | 267.5 ± 6.3 ms | `*Node` (raw) |
| **kāra flatten**                                    | **320.8 ± 12.6 ms** | **`shared` (RC)** |
| rust flatten (rustc -O, overflow-checks=on)          | 401.8 ± 14.0 ms | `Rc<RefCell>` |
| rust flatten (rustc -O)                             | 407.2 ± 23.6 ms | `Rc<RefCell>` |
| go   flatten (GC `*Node`)                           | 460.2 ± 28.3 ms | `*Node` |

**On this container run: on a mutating linked-structure workload, Kāra's `shared` beats Rust's safe `Rc<RefCell>` — 1.27× faster — and trails only raw-pointer C.** Both `shared` and `Rc<RefCell>` provide *safe* reference-counted interior mutability, but Kāra's is compiler-managed: the ownership pass proves the aliasing statically, so the emitted code is plain RC inc/dec with no per-access `RefCell` borrow-flag check and no `Rc::clone` at every hop. That lands Kāra at **1.20× behind C** (the unsafe raw-pointer floor) while running **1.27× ahead of `rustc -O`** and **1.43× ahead of Go** (whose per-rep tree allocation feeds the GC — 7.1 MiB RSS, ~5× everyone else). A raw-pointer (unsafe) Rust would sit alongside C; the `Rc<RefCell>` row is the honest *safe*-Rust peer, and that is the one Kāra passes. Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`) over the run. Python is listed at **207 ms (earlier container run, not re-run 2026-11-01) but ran K = 10,000 — 1/20 of the compiled iterations** (pure-Python is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **1.5 MiB** peak RSS — **level with C**, below Rust's 2.2 MiB and a fraction of Go's 7.1 MiB. And because this workload nets **zero heap growth** (each rep builds, flattens, and frees a fixed 63-node tree), the backtrace-symbolizer tree is stripped: the kāra binary is **15.4 KiB, at parity with C's 15.8 KiB** (contrast the heap-growing traversal katas, whose container binaries carried the ~324 KiB symbolizer artifact) — vs Rust's 3.8 MiB and Go's 2.1 MiB.

**Flagged for the M5 re-bench** — container orderings can shift on the M5's wider core (see [#97](../../1-100/97-interleaving-string/)); treat the *margins* as data points. The direction — Kāra ahead of safe `Rc<RefCell>` Rust, behind raw C — should hold, since it reflects the RC-model difference, not a microarchitectural quirk. (2026-11-01 note: on the M5 v2/MIR run that direction holds — 0.90× Rust, 1.36× C — but Go now leads every mirror, Kāra 1.57× behind it; see the M5 table above.)

Compile-cold, binary size, and peak-RSS records are in [`bench/results.json`](bench/results.json) (M5, canonical) and [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched **in-place mutation of an aliased shared-node tree**, where Kāra's compiler-managed `shared` (RC) is measured against Rust's `Rc<RefCell>` (the safe interior-mutability equivalent) and comes out ahead. C's raw pointer chase is the unsafe metal floor, Go the GC data point (the outlier on the container on per-rep tree churn, but the fastest mirror on the 2026-11-01 M5 run), Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
