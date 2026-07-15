# 107. Binary Tree Level Order Traversal II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Tree · Breadth-First Search · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/binary-tree-level-order-traversal-ii](https://leetcode.com/problems/binary-tree-level-order-traversal-ii/)

Return the node values grouped by depth, **bottom-up** — the deepest level first, the root level last. It is [#102](../102-binary-tree-level-order-traversal/) with the *rows* emitted in reverse order; the values within each row still read left to right.

```
      3            bottom-up:
     / \             [15, 7],      (deepest level first)
    9  20            [9, 20],
       / \           [3]           (root level last)
      15  7
```

**Constraints:** `0 ≤ #nodes ≤ 2000`, node values fit `-1000 … 1000`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **DFS carrying the depth, reverse the row order** ★ | [`level_order_bottom.kara`](level_order_bottom.kara) ✓ | [`level_order_bottom.py`](level_order_bottom.py) ✓ |
| **BFS frontier, reverse the row order** | [`level_order_bottom_bfs.kara`](level_order_bottom_bfs.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for both approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the two Kāra approaches agree with **each other** and with the Python mirror. An independent **ground-truth check** confirms the traversal: the DFS-with-depth bottom-up order equals a genuinely different **BFS**-then-reverse order (a queue that dequeues a whole level per iteration, rows reversed) on a case battery **and 20,000 randomised fuzz trees**, zero mismatches. Both solvers compile with zero diagnostics and are valgrind-clean.

## Two ways to go bottom-up

Bottom-up order is plain level order with the *row list* reversed — so both solvers reduce to "collect the levels top-down, then emit them deepest-first."

**DFS carrying the depth** ([`level_order_bottom.kara`](level_order_bottom.kara), the ★): collect the levels exactly as kata [#102](../102-binary-tree-level-order-traversal/) does — one depth-indexed DFS that appends each node's value to the row for its depth, so every row fills left to right — then emit the rows in reverse depth order (deepest first). O(n).

```
dfs(node, depth, rows):  append node.val to rows[depth]  (left→right)
level_order_bottom(root):
    rows = dfs-collected levels
    for d from last depth down to 0:  out.push(rows[d])
```

**BFS frontier** ([`level_order_bottom_bfs.kara`](level_order_bottom_bfs.kara)): hold the current level as a `Vec[TreeNode]` frontier, collect its values top-down into a row list (advancing `current = next` each level), then reverse the row order. A distinct mechanism (iterative queue vs recursive depth index) that must land on the identical bottom-up grouping — and it exercises the `Vec[shared]` frontier + `current = next` reassignment the tree katas [#102](../102-binary-tree-level-order-traversal/)/[#103](../103-binary-tree-zigzag-level-order-traversal/) share.

## Kāra features exercised

- **`shared struct TreeNode` (RC), read-only traversal** — both solvers walk the shared-node tree without mutating it. Node type mirrors kata [#102](../102-binary-tree-level-order-traversal/) / [#103](../103-binary-tree-zigzag-level-order-traversal/).
- **`mut ref Vec[Vec[i64]]` accumulator grown mid-recursion** — the DFS threads the nested rows through recursive calls as a `mut ref`; the two recursive calls both write it, a genuine dependency (also why auto-par correctly leaves this recursion sequential — see the benchmark note).
- **Reverse the outer list via a descending index walk** — the output rows are built by walking `rows` from the last depth down to 0, the row-order flip at the heart of the problem (the outer-list analogue of [#103](../103-binary-tree-zigzag-level-order-traversal/)'s inner-row reverse).
- **`Vec[TreeNode]` frontier with `current = next`** — the BFS solver advances the shared-node frontier by whole-variable reassignment; the frontier drains to empty, so its scope-exit drop is clean (the surface hardened by kara `924cd05`).

**v1 note.** Trees stay within the `≤ 2000`-node constraint. The sink folds each tree's bottom-up level structure — level count, each level's size, and every value in emitted order — into a running polynomial hash. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the BFS-reverse fuzz ground truth, and are valgrind-clean.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   level_order_bottom.kara
karac build level_order_bottom.kara && ./level_order_bottom

# The BFS-frontier variant (identical output):
karac run level_order_bottom_bfs.kara

# Python
python3 level_order_bottom.py

# Verify they all agree
diff <(karac run level_order_bottom.kara) <(python3 level_order_bottom.py)             && echo OK
diff <(karac run level_order_bottom.kara) <(karac run level_order_bottom_bfs.kara)     && echo OK

# Ground truth: DFS-depth bottom-up == BFS-then-reverse bottom-up (battery + 20k fuzz)
python3 ground_truth.py
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`level_order_bottom.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** The canonical numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json). The corpus's canonical **Apple M5 Pro** numbers ([`bench/results.json`](bench/results.json)) are folded in separately; absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. Re-run `bench.sh` on the M5 to refresh the canonical table.

**Workload.** Build 8 distinct 15-node BSTs once, then **K = 1,000,000** reps of DFS-with-depth bottom-up level order on a **data-dependent-selected** tree (`idx = acc%8`, seeded by the running hash, so nothing hoists), building a fresh `Vec[Vec[i64]]` output (rows emitted deepest-first) and folding the whole result — level count, each level's size, and every value — into a rolling polynomial hash. Each rep allocates both the depth-indexed rows *and* the reversed-order output, so the workload is **allocation-bound**. Each mirror uses its natural node: Kāra `shared` (RC), C/Go raw pointer, **Rust `Box` + `&`-borrow** (the tree is never mutated or shared during traversal). All five compiled mirrors must agree on `59640307` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../../1-100/69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **x86-64 container numbers** (canonical M5 pending; see the machine note):

| Implementation | Wall time | Node / result representation |
|---|---|---|
| c    level_order_bottom (clang -O3)                 | 463.5 ± 14.0 ms | `malloc` pointer + `realloc` rows |
| **kāra level_order_bottom**                         | **562.9 ± 9.9 ms** | **`shared` (RC) + `Vec[Vec]`** |
| rust level_order_bottom (rustc -O)                  | 728.8 ± 20.8 ms | `Box` + `Vec<Vec>` |
| rust level_order_bottom (rustc -O, overflow-checks=on)| 740.4 ± 21.3 ms | `Box` + `Vec<Vec>` |
| go   level_order_bottom (GC)                        | 978.9 ± 15.0 ms | `*Node` + `[][]int64` (GC) |

**On this allocation-bound nested-container workload Kāra lands second — ahead of Rust by 30% and Go by 74%.** Every rep builds two layers of fresh `Vec[Vec[i64]]` (the depth-indexed rows, then the deepest-first output) and tears them down, so the per-rep cost is the nested-container churn. Against its semantic peer Rust — `Box` node walked by `&`-borrow, `Vec<Vec<i64>>` result — Kāra is **1.29× ahead** (563 vs 729 ms; 563 vs 740 with overflow-checks on): building an outer vector of freshly-grown inner vectors and freeing the lot is exactly the shape Kāra's `Vec` growth handles leanest, and it stays ahead even with the per-node RC inc/decs the borrow-based Rust walk skips, because the *allocation* dominates. **C is the floor** at 464 ms (Kāra **1.21× behind**): raw `malloc`/`realloc`/`free`, no refcount, no GC. **Go trails at 979 ms** (Kāra **1.74× ahead**): its GC pays hardest on the 1 M × (two nested-slice layers) allocation churn — deferred collection being the wrong trade for short-lived nested allocations, the same GC-under-churn regime where Go placed last in [#102](../102-binary-tree-level-order-traversal/) and [#103](../103-binary-tree-zigzag-level-order-traversal/). So the ordering is by allocator overhead on short-lived nested containers — raw malloc < **Kāra RC/`Vec`** < `Box`/`Vec` < Go GC — the same nested-Vec regime where Kāra beat Rust in [#102](../102-binary-tree-level-order-traversal/) (the alloc-heavy tree siblings consistently favor Kāra's `Vec` growth over Rust's `Vec<Vec>`). Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`) over the run. Python is listed at **207 ms but ran K = 50,000 — 1/20 of the compiled iterations** (pure-Python recursion is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **2.5 MiB** peak RSS (parity with Rust's 2.4 MiB, above C's 1.5 MiB) vs Go's **7.7 MiB**. The kāra binary measures **336 KiB** here — a build-linkage artifact of this container run (heap-growing programs retain the backtrace-symbolizer tree `--gc-sections` should strip; a correct build is ~15 KiB), independent of the runtime numbers, flagged for the M5 — vs C's 16 KiB and Go's 2.2 MiB.

**Flagged for the M5 re-bench** — the corpus has seen container tree orderings shift on the M5's wider core (see [#97](../../1-100/97-interleaving-string/), [#99](../../1-100/99-recover-binary-search-tree/)), so treat the *margin* as a data point; the Kāra-ahead-of-Rust sign is robust across the nested-Vec siblings ([#102](../102-binary-tree-level-order-traversal/)), but the size may compress.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference) and, once folded in, [`bench/results.json`](bench/results.json) (M5, canonical).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched nested-container allocation (`Vec[Vec[i64]]` vs `Vec<Vec<i64>>`, both over a by-reference tree walk), the honest comparison for a collect-and-reverse-levels workload. C's raw `malloc`/`realloc` is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
