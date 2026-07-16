# 116. Populating Next Right Pointers in Each Node

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Linked List · Tree · Depth-First Search · Breadth-First Search · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/populating-next-right-pointers-in-each-node](https://leetcode.com/problems/populating-next-right-pointers-in-each-node/)

You are given a **perfect** binary tree (every internal node has two children, all leaves on the same level). Populate each node's `next` pointer to point to the node immediately to its **right on the same level**; the rightmost node of each level gets `None`. Initially every `next` is `None`. A sibling of the mutating tree stretch — where [#114](../114-flatten-binary-tree-to-linked-list/) rewired `left`/`right`, this one adds a third `next` handle and stitches the tree sideways.

```
        1                          1 -> None
      /   \                       / \
     2     3      connect -->    2 - 3 -> None
    / \   / \                   / \ / \
   4  5  6  7                   4-5-6-7 -> None
```

**Constraints:** `0 ≤ #nodes ≤ 2¹² − 1` (a perfect tree), node values fit `-1000 … 1000`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **O(1) space — thread the wired level to stitch the next** ★ | [`connect.kara`](connect.kara) ✓ | [`connect.py`](connect.py) ✓ |
| **BFS level-order with a queue** | [`connect_bfs.kara`](connect_bfs.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for both approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the two Kāra approaches agree with **each other** and with the Python mirror. An independent **ground-truth check** confirms the wiring three ways: the O(1)-space level-threading equals the BFS queue *and* the literal invariant — **each level's `next` chain, starting at that level's leftmost node, equals that level's nodes in BFS left-to-right order, rightmost `next` = None** — on a case battery **and 20,000 randomised perfect trees** (depth 1…11), zero disagreements. Both solvers compile with zero diagnostics and are valgrind-clean.

## Two wiring mechanisms

**O(1) space** ([`connect.kara`](connect.kara), the ★): the perfect-tree shape lets each already-wired level stitch the one below with no queue. Walk straight down the left edge to reach each level's head; thread that level via its (established) `next` chain, and for every node set `node.left.next = node.right` and `node.right.next = node.next.left` (when a right neighbour exists). Constant extra space — the `next` pointers *are* the level's traversal.

```
leftmost = root
while leftmost and leftmost.left:
    head = leftmost
    while head:
        head.left.next = head.right                     # link the two children
        if head.next: head.right.next = head.next.left  # bridge across the sibling gap
        head = head.next
    leftmost = leftmost.left
```

**BFS level-order** ([`connect_bfs.kara`](connect_bfs.kara)): the textbook sweep — collect each level's nodes into a queue, link each to the next in that level (last gets `None`), enqueue the children. O(n) space. A distinct mechanism (an explicit per-level queue vs reusing the level-above chain) that must land on the identical wiring — same `next` pointers, hence the same `level_hash`.

## Kāra features exercised

- **In-place `mut next` mutation on `shared` nodes** — both solvers write `node.next` (and the O(1) form reads it right back to advance `head = head.next`) through `shared struct Node` handles; the RC layer keeps every node alive as the sideways links are added. The mutating-tree surface of [#114](../114-flatten-binary-tree-to-linked-list/), extended to a third handle.
- **Nested `Option[shared]` matching for the sideways bridge** — `head.right.next = head.next.left` is three chained `Option[Node]` matches (right child, next sibling, its left child), the natural shape of the constant-space trick.
- **`Vec[Node]` as a level queue** — the BFS variant collects each level into a `Vec[Node]` and rebuilds it per level (an RC-fallback on the re-used queue handle, which the ownership pass reports as a note — benign, and the run is valgrind-clean).
- **Perfect-tree construction by heap index** — `build_perfect(idx, max_idx)` with children `2·idx` / `2·idx+1`, so `max_idx = 2^depth − 1` gives a dense, exactly-full tree.

**v1 note.** Trees stay within the `≤ 4095`-node constraint. The sink folds each tree's level-order hash (walked via the freshly-wired `next` chains) into a running accumulator. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the BFS + literal-level-order ground truth, and are valgrind-clean.

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

> **Machine.** The canonical numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json). The corpus's canonical **Apple M5 Pro** numbers ([`bench/results.json`](bench/results.json)) are folded in separately; absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. Re-run `bench.sh` on the M5 to refresh the canonical table.

**Workload.** Each rep builds a fresh **511-node** (depth-9) perfect tree over a **data-dependent** value base (`base = acc%100`, seeded by the running hash so nothing hoists), wires every node's `next` with the O(1)-space level-threading, and folds a level-order hash that reads the `next` chain back — **K = 40,000** reps. This is the **mutate regime**: shared-node allocation (511 RC nodes built + freed) plus in-place `next` wiring per rep, the same family as [#114](../114-flatten-binary-tree-to-linked-list/)'s flatten.

**Node representation & equal safety.** As in [#114](../114-flatten-binary-tree-to-linked-list/): **C** (`*Node`) and **Go** (`*Node`, GC) chase raw pointers; **Rust** uses **`Rc<RefCell<Node>>`** — the *safe* interior-mutability peer to Kāra's `shared` (RC), the caveat being that an *unsafe* raw-pointer Rust would match C. Kāra's `shared` is RC too but **without** `RefCell`'s runtime borrow flag (the ownership pass discharges it statically). Kāra checks integer overflow by default; the `rustc -O -C overflow-checks=on` row is the like-for-like on the hash fold.

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **x86-64 container numbers** (canonical M5 pending; see the machine note):

| Implementation | Wall time | Node representation |
|---|---|---|
| c    connect (clang -O3)                            | 456.7 ± 6.4 ms | `*Node` (raw) |
| **kāra connect**                                    | **462.7 ± 7.1 ms** | **`shared` (RC)** |
| rust connect (rustc -O, overflow-checks=on)          | 687.9 ± 13.8 ms | `Rc<RefCell>` |
| rust connect (rustc -O)                             | 689.5 ± 16.8 ms | `Rc<RefCell>` |
| go   connect (GC `*Node`)                           | 687.5 ± 9.7 ms | `*Node` |

**On this mutating linked-structure workload, Kāra's `shared` runs neck-and-neck with raw-pointer C and comfortably ahead of safe `Rc<RefCell>` Rust.** Kāra lands **1.01× behind C** (the unsafe raw-pointer floor — within noise) while running **1.49× ahead of safe `rustc -O` Rust** and **1.49× ahead of Go**. Both `shared` and `Rc<RefCell>` provide *safe* reference-counted interior mutability, but Kāra's is compiler-managed: the ownership pass proves the aliasing statically, so the emitted code is plain RC inc/dec with no per-access `RefCell` borrow-flag check and no `Rc::clone` at every hop — which is what closes almost the entire gap to raw C here (tighter than #114's 1.20×, since the read-heavy level-threading and `next`-chain fold lean on cheap reads the RC-elision pass now skips). A raw-pointer (unsafe) Rust would sit alongside C; the `Rc<RefCell>` row is the honest *safe*-Rust peer, and that is the one Kāra passes. Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`). Python is listed at **294 ms but ran K = 2,000 — 1/20 of the compiled iterations** (pure-Python is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **1.6 MiB** peak RSS — **level with C** (1.7 MiB), below Rust's 2.1 MiB and a fraction of Go's 7.7 MiB. And because this workload nets **zero heap growth** (each rep builds, wires, and frees a fixed 511-node tree), the backtrace-symbolizer tree is stripped: the kāra binary is **15.4 KiB, at parity with C's 15.8 KiB** — vs Rust's 3.8 MiB and Go's 2.1 MiB.

**Flagged for the M5 re-bench** — container orderings can shift on the M5's wider core (see [#97](../../1-100/97-interleaving-string/)); treat the *margins* as data points. The direction — Kāra level with raw C, ahead of safe `Rc<RefCell>` Rust — should hold, since it reflects the RC-model difference, not a microarchitectural quirk.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference) and, once folded in, [`bench/results.json`](bench/results.json) (M5, canonical).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched **in-place mutation of an aliased shared-node tree** (adding `next` links), where Kāra's compiler-managed `shared` (RC) is measured against Rust's `Rc<RefCell>` (the safe interior-mutability equivalent) and comes out well ahead, right at the raw-pointer C floor. C's raw pointer chase is the unsafe metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
