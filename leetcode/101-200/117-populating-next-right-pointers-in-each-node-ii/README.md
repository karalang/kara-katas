# 117. Populating Next Right Pointers in Each Node II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Linked List · Tree · Depth-First Search · Breadth-First Search · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/populating-next-right-pointers-in-each-node-ii](https://leetcode.com/problems/populating-next-right-pointers-in-each-node-ii/)

The generalisation of [#116](../116-populating-next-right-pointers-in-each-node/): the tree is now **any** binary tree — a node may have zero, one, or two children — so the perfect-tree shortcut (`node.right.next = node.next.left`) is gone. Populate each node's `next` to point to the node immediately to its **right on the same level**; the rightmost node of each level gets `None`. Initially every `next` is `None`.

```
        1                          1 -> None
      /   \                       / \
     2     3      connect -->    2 - 3 -> None
    / \     \                   / \   \
   4  5      7                  4 - 5 - 7 -> None
```

**Constraints:** `0 ≤ #nodes ≤ 6000`, node values fit `-100 … 100`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **O(1) space — dummy-head + tail per level** ★ | [`connect.kara`](connect.kara) ✓ | [`connect.py`](connect.py) ✓ |
| **BFS level-order with a queue** | [`connect_bfs.kara`](connect_bfs.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for both approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the two Kāra approaches agree with **each other** and with the Python mirror. An independent **ground-truth check** confirms the wiring three ways: the O(1)-space dummy-head threading equals the BFS queue *and* the literal invariant — **each level's reachable `next` chain equals that level's nodes in BFS left-to-right order, rightmost `next` = None** — on a case battery **and 20,000 randomised trees of varied shape** (random BSTs, size 0…80), zero disagreements. Both solvers compile with zero diagnostics and are valgrind-clean.

## Two wiring mechanisms

**O(1) space, dummy-head + tail** ([`connect.kara`](connect.kara), the ★): with children possibly missing, you can't index across the gap the way #116 does. Instead, for each level keep a **dummy head** and a running **tail**; thread the current level via its (already-wired) `next` chain, and for every node append whichever children exist (left then right) to the next level's chain through `tail`. `dummy.next` is that level's head, so descending is `leftmost = dummy.next` — constant extra space, no queue, no recursion.

```
leftmost = root
while leftmost:
    dummy = Node(); tail = dummy          # anchor the next level's chain
    cur = leftmost
    while cur:
        if cur.left:  tail.next = cur.left;  tail = cur.left
        if cur.right: tail.next = cur.right; tail = cur.right
        cur = cur.next
    leftmost = dummy.next                  # head of the next level (or None)
```

**BFS level-order** ([`connect_bfs.kara`](connect_bfs.kara)): the textbook sweep — collect each level's nodes into a queue, link each to the next in that level (last gets `None`), enqueue whichever children exist. The arbitrary-tree case needs no special handling here. A distinct mechanism (explicit per-level queue vs the dummy-head reuse of the level-above chain) that must land on the identical wiring — same `next` pointers, hence the same `level_hash`.

## Kāra features exercised

- **Dummy-head sentinel as a `shared` node** — `let dummy = Node { .. }; let mut tail = dummy;` then `tail.next = Some(child); tail = child` walks the growing tail through RC handles. The canonical constant-space idiom; the sentinel is a heap `shared` node (RC), the honest cost `shared` and Rust's `Rc` both pay where C/Go get a stack local free.
- **In-place `mut next` mutation on `shared` nodes**, read right back to advance (`cur = cur.next`) — the mutating-tree surface of [#116](../116-populating-next-right-pointers-in-each-node/), now over sparse shapes.
- **Deep `Option[shared]` matching for missing children** — every `left`/`right` is matched before use, the natural expression of "whichever children exist".
- **Level-head recovery over a sparse tree** — the sink can't descend by `.left` (a level's leftmost node may have no left child); it scans each level via `next` for the first existing child, the arbitrary-tree analogue of #116's straight-down walk.

**v1 note.** Trees stay within the `≤ 6000`-node constraint. The sink folds each tree's level-order hash (walked via the freshly-wired `next` chains) into a running accumulator. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the BFS + literal-level-order ground truth, and are valgrind-clean.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   connect.kara
karac build connect.kara && ./connect

# The BFS variant (identical output):
karac run connect_bfs.kara

# Python
python3 connect.py

# Verify they all agree
diff <(karac run connect.kara) <(python3 connect.py)          && echo OK
diff <(karac run connect.kara) <(karac run connect_bfs.kara)  && echo OK

# Ground truth: O(1) == BFS == literal level-order (battery + 20k fuzz)
python3 ground_truth.py
```

## Benchmarks
Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`connect.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5 re-bench (2026-11-01).** The canonical numbers below are the corpus's **Apple M5 Pro** run (6P+12E, Darwin 25.6.0; **karac g6697158fa** (0.9.0-dev.14057, the v2/MIR backend; the legacy backend was deleted 2026-10-23), `rustc 1.95.0`, Apple clang 21.0.0, `go 1.26.3`, hyperfine 1.20) — [`bench/results.json`](bench/results.json). Against the 2026-07-28 legacy-backend M5 run kāra is flat against every comparator (each move under this session's ~10 % noise band): kāra/Rust 0.87× → 0.93×, kāra/equal-safety Rust 0.86× → 0.90×, kāra/C 1.20× → 1.28×, kāra/Go 1.51× → 1.45×. An earlier shared **x86-64 Linux cloud-container** run, which this section originally reported as canonical, is kept below as history ([`bench/results.container-x86.json`](bench/results.container-x86.json)); absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal.

**Workload.** Each rep builds a fresh **~500-node** pseudo-random BST (fixed insert sequence, so a fixed **shape**) whose values carry a **data-dependent** base (`base = acc%100`, shifting every value equally so the shape is unchanged and nothing hoists), wires every node's `next` with the O(1)-space dummy-head threading, and folds a level-order hash that reads the `next` chain back — **K = 16,000** reps. This is the **mutate regime**: shared-node allocation (~500 RC nodes built + freed) plus in-place `next` wiring per rep, the arbitrary-tree sibling of [#116](../116-populating-next-right-pointers-in-each-node/).

**Node representation & equal safety.** As in [#116](../116-populating-next-right-pointers-in-each-node/): **C** (`*Node`) and **Go** (`*Node`, GC) chase raw pointers (dummy head a stack local); **Rust** uses **`Rc<RefCell<Node>>`** — the *safe* interior-mutability peer to Kāra's `shared` (RC), the caveat being that an *unsafe* raw-pointer Rust would match C. Kāra's `shared` is RC too but **without** `RefCell`'s runtime borrow flag (the ownership pass discharges it statically). Kāra checks integer overflow by default; the `rustc -O -C overflow-checks=on` row is the like-for-like on the hash fold.

`--warmup 5 --runs 30 --shell=none`. Single-threaded mirrors, ~99.6 % CPU (the default build emits no call of `karac_mir_task_spawn`, verified in the emitted IR (`KARAC_MIR_LL`), same as its `KARAC_AUTO_PAR=0` twin; Go's runtime runs at 113 % CPU, 225.6 ms user). **Apple M5 Pro numbers, karac g6697158fa, 2026-11-01** (canonical; sink `483878699` agreed by all five mirrors):

| Implementation | Wall time | Node representation |
|---|---|---|
| go   connect (GC `*Node`)                           | 226.6 ± 2.3 ms | `*Node` |
| c    connect (clang -O3)                            | 257.9 ± 4.7 ms | `*Node` (raw) |
| **kāra connect**                                    | **329.3 ± 3.9 ms** | **`shared` (RC)** |
| rust connect (rustc -O)                             | 353.8 ± 2.9 ms | `Rc<RefCell>` |
| rust connect (rustc -O, overflow-checks=on)          | 364.1 ± 10.6 ms | `Rc<RefCell>` |

**On the M5 (2026-11-01, v2/MIR) Kāra is third of five, ahead of both safe-Rust rows** — **0.93× `rustc -O`** (1.07× ahead) and **0.90× the equal-safety Rust row** (1.11× ahead), **1.28× behind raw-pointer C** and **1.45× behind Go**, the same ordering as the 2026-07-28 legacy-backend M5 run in the box below. kāra holds **1.09 MiB** peak RSS (Rust 1.09, C 1.02; Go 9.8 MiB). Binary size: c 32.8 KiB, **kāra 295.8 KiB**, rust 456.3 KiB, go 2.38 MiB; every MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (the legacy M5 kāra binary here was 33.3 KiB), tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). Compile-cold on the M5 is clang 47.1 ms < rustc 125.5 ms < **karac 132.2 ms** (2.8× clang, 1.05× rustc).

**x86-64 container numbers** (history: the earlier, undated container run this section first reported):

| Implementation | Wall time | Node representation |
|---|---|---|
| c    connect (clang -O3)                            | 335.0 ± 8.5 ms | `*Node` (raw) |
| **kāra connect**                                    | **475.0 ± 12.3 ms** | **`shared` (RC)** |
| go   connect (GC `*Node`)                           | 493.3 ± 7.2 ms | `*Node` |
| rust connect (rustc -O, overflow-checks=on)          | 527.9 ± 15.3 ms | `Rc<RefCell>` |
| rust connect (rustc -O)                             | 530.3 ± 21.0 ms | `Rc<RefCell>` |

**On this container run Kāra sat between raw-pointer C and safe `Rc<RefCell>` Rust — ahead of both Go and safe Rust, behind C by a wider margin than [#116](../116-populating-next-right-pointers-in-each-node/) (1.42× vs 1.02×).** The extra gap to C is *construction*, not the wiring: the arbitrary-tree workload builds each ~500-node tree via **repeated root-down BST inserts** (≈500 inserts × ~log-depth traversal), which is RC-inc/dec-heavy in Kāra but a raw pointer-chase in C — a heavier build than #116's single-pass perfect-tree fill. On the `connect` itself Kāra still runs **1.04× ahead of Go** and **1.11× ahead of safe `rustc -O` Rust** (both the dummy-head sentinel and the node graph are RC/`Rc` in Kāra and Rust alike, so that comparison is clean; Kāra's edge is the absent `RefCell` borrow flag). A raw-pointer (unsafe) Rust would sit alongside C; the `Rc<RefCell>` row is the honest *safe*-Rust peer, and that is the one Kāra passes. Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`). Python is listed at **375 ms (earlier container run, not re-run 2026-11-01) but ran K = 800 — 1/20 of the compiled iterations** (pure-Python is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

On the container kāra held **1.7 MiB** peak RSS — **level with C** (1.7 MiB), below Rust's 2.1 MiB and a fraction of Go's 6.9 MiB. And because this workload nets **zero heap growth** (each rep builds, wires, and frees a fixed tree), the backtrace-symbolizer tree is stripped: the container kāra binary was **15.4 KiB, at parity with C's 15.8 KiB** — vs Rust's 3.8 MiB and Go's 2.1 MiB.

> **M5 result (2026-07-28, legacy backend; history) — half the predicted direction held, half inverted.** (2026-11-01 note: the v2/MIR re-bench keeps this ordering — see the M5 table above.)
> This section used to argue the direction "should hold, since it reflects the
> RC-model difference, not a microarchitectural quirk." On the canonical M5 host:
>
> | Implementation | M5 wall time | vs Kāra |
> |---|---|---|
> | go   connect | **195.7 ± 1.2 ms** | 0.66× |
> | c    connect (clang -O3) | 244.6 ± 3.9 ms | 0.83× |
> | **kāra connect** | **294.7 ± 5.8 ms** | **1.00×** |
> | rust connect (rustc -O) | 338.2 ± 6.9 ms | 1.15× |
> | rust connect (overflow-checks=on) | 342.3 ± 4.4 ms | 1.16× |
>
> **Ahead of safe Rust: held**, and by more than claimed — 1.15× rather than
> 1.11×, and the overflow-checked twin costs Rust nothing on this pointer-wiring
> workload (338.2 → 342.3 ms), so the RC-model argument survives intact.
> **Ahead of Go: inverted.** Go is 1.51× *faster* than Kāra here, not 1.04×
> slower. Behind C widened slightly, 1.42× → 1.20× measured differently but the
> sign is unchanged.
>
> The RC-model reasoning was sound where it was actually about RC — the Rust
> comparison, where both sides refcount. It over-reached when applied to Go,
> which refcounts nothing and whose GC handles this build-wire-free cycle far
> better than a container run suggested. The text below is the pre-M5 container
> analysis, retained for provenance.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.json`](bench/results.json) (M5, canonical) and [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched **in-place next-pointer wiring of an aliased shared-node tree of arbitrary shape**, where Kāra's compiler-managed `shared` (RC) is measured against Rust's `Rc<RefCell>` (the safe interior-mutability equivalent) and comes out ahead. C's raw pointer chase is the unsafe metal floor (further ahead here because the BST construction is RC-heavy for Kāra and Rust but not for C), Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
