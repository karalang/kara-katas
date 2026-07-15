# 103. Binary Tree Zigzag Level Order Traversal

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Tree · Breadth-First Search · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/binary-tree-zigzag-level-order-traversal](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/)

Return the node values grouped by depth, but with the direction **alternating** each level: row 0 left-to-right, row 1 right-to-left, row 2 left-to-right, and so on — a boustrophedon ("as the ox ploughs") walk of the tree.

```
      3               zigzag:
     / \                [3],          (level 0, left→right)
    9  20                [20, 9],      (level 1, right→left)
       / \               [15, 7]       (level 2, left→right)
      15  7
```

**Constraints:** `0 ≤ #nodes ≤ 2000`, node values fit `-100 … 100`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **DFS carrying the depth, reverse odd rows** ★ | [`zigzag.kara`](zigzag.kara) ✓ | [`zigzag.py`](zigzag.py) ✓ |
| **BFS frontier, directional emit** | [`zigzag_bfs.kara`](zigzag_bfs.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for both approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the two Kāra approaches agree with **each other** and with the Python mirror. An independent **ground-truth check** confirms the traversal: the DFS-with-depth zigzag equals a genuinely different **BFS**-then-reverse-odd zigzag (a queue that dequeues a whole level per iteration, reversing every odd level) on a case battery **and 20,000 randomised fuzz trees**, zero mismatches. Both solvers compile with zero diagnostics and are valgrind-clean.

## Two ways to zigzag

Zigzag order is plain level order with the emission direction flipping each level — so both solvers reduce to "level order, then decide which end each row is read from."

**DFS carrying the depth** ([`zigzag.kara`](zigzag.kara), the ★): collect the levels exactly as kata [#102](../102-binary-tree-level-order-traversal/) does — one depth-indexed DFS that appends each node's value to the row for its depth, so every row fills left to right — then emit the rows, copying even rows as-is and **reversing** every odd one. O(n).

```
dfs(node, depth, rows):  append node.val to rows[depth]  (left→right)
zigzag(root):
    rows = dfs-collected levels
    for each depth d:  out.push( d even ? rows[d] : reverse(rows[d]) )
```

**BFS frontier, directional emit** ([`zigzag_bfs.kara`](zigzag_bfs.kara)): hold the current level as a `Vec[TreeNode]` frontier, read off its values, and emit that row left-to-right on even levels / reversed on odd — while building the next frontier left-to-right as usual and advancing `current = next`. The traversal is plain BFS; the zigzag is *only* which end each row is read from. A distinct mechanism (iterative queue vs recursive depth index) that must land on the identical grouping — and it exercises the `Vec[shared]` frontier + `current = next` reassignment that kata [#102](../102-binary-tree-level-order-traversal/)'s BFS first drove (leak-clean since kara `924cd05`).

## Kāra features exercised

- **`shared struct TreeNode` (RC), read-only traversal** — both solvers walk the shared-node tree without mutating it. Node type mirrors kata [#102](../102-binary-tree-level-order-traversal/) / [#100](../../1-100/100-same-tree/).
- **`mut ref Vec[Vec[i64]]` accumulator grown mid-recursion** — the DFS threads the nested rows through recursive calls as a `mut ref`, and because the two recursive calls both write it, the calls share a genuine dependency (which is also why auto-par correctly leaves this recursion sequential — see the benchmark note).
- **Reverse via reverse-order index walk** — odd rows are emitted by pushing `rows[d][len-1 .. 0]` into a fresh row, a nested-`Vec` reverse read.
- **`Vec[TreeNode]` frontier with `current = next`** — the BFS solver advances the shared-node frontier by whole-variable reassignment (the surface hardened by kara `924cd05` / [`B-2026-07-12-30`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl)); the frontier drains to empty, so its scope-exit drop is clean.

**v1 note.** Trees stay within the `≤ 2000`-node constraint. The sink folds each tree's zigzag structure — level count, each level's size, and every value in emitted order — into a running polynomial hash. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the BFS-reverse-odd fuzz ground truth, and are valgrind-clean.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   zigzag.kara
karac build zigzag.kara && ./zigzag

# The BFS-frontier variant (identical output):
karac run zigzag_bfs.kara

# Python
python3 zigzag.py

# Verify they all agree
diff <(karac run zigzag.kara) <(python3 zigzag.py)         && echo OK
diff <(karac run zigzag.kara) <(karac run zigzag_bfs.kara) && echo OK

# Ground truth: DFS-depth zigzag == BFS-then-reverse-odd zigzag (battery + 20k fuzz)
python3 ground_truth.py
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`zigzag.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** The canonical numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json). The corpus's canonical **Apple M5 Pro** numbers ([`bench/results.json`](bench/results.json)) are folded in separately; absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. Re-run `bench.sh` on the M5 to refresh the canonical table.

**Workload.** Build 8 distinct 15-node BSTs once, then **K = 600,000** reps of DFS-with-depth zigzag on a **data-dependent-selected** tree (`idx = acc%8`, seeded by the running hash, so nothing hoists), building a fresh `Vec[Vec[i64]]` output (odd rows reversed) and folding the whole result — level count, each level's size, and every value — into a rolling polynomial hash. Each rep allocates both the depth-indexed rows *and* the reversed-odd output, so the workload is **allocation-bound**. Each mirror uses its natural node: Kāra `shared` (RC), C/Go raw pointer, **Rust `Box` + `&`-borrow** (the tree is never mutated or shared during traversal). All five compiled mirrors must agree on `107317664` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../../1-100/69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **x86-64 container numbers** (canonical M5 pending; see the machine note):

| Implementation | Wall time | Node / result representation |
|---|---|---|
| c    zigzag (clang -O3)                             | 439.2 ± 10.1 ms | `malloc` pointer + `realloc` rows |
| rust zigzag (rustc -O)                              | 645.6 ± 22.5 ms | `Box` + `Vec<Vec>` |
| rust zigzag (rustc -O, overflow-checks=on)           | 653.7 ± 18.2 ms | `Box` + `Vec<Vec>` |
| **kāra zigzag**                                     | **656.9 ± 38.1 ms** | **`shared` (RC) + `Vec[Vec]`** |
| go   zigzag (GC)                                    | 855.5 ± 28.4 ms | `*Node` + `[][]int64` (GC) |

**On this allocation-bound nested-container workload Kāra effectively ties Rust — within 2% — and runs 30% ahead of Go.** Every rep builds two layers of fresh `Vec[Vec[i64]]` (the depth-indexed rows, then the reversed-odd output) and tears them down, so the per-rep cost is the nested-container churn. Against its semantic peer Rust — `Box` node walked by `&`-borrow, `Vec<Vec<i64>>` result — Kāra is a statistical **dead heat** (657 vs 646 ms plain, 657 vs 654 with overflow-checks on; the ±38 ms spread swamps the 11 ms gap): the two do the same allocate-outer-then-grow-inners-then-free work, and Kāra's `Vec` growth path keeps pace even with the per-node RC inc/decs the borrow-based Rust walk skips, because the *allocation* dominates. **C is the floor** at 439 ms (Kāra **1.50× behind**): raw `malloc`/`realloc`/`free`, no refcount, no GC. **Go trails at 856 ms** (Kāra **1.30× ahead**): its GC pays on the 600 k × (two nested-slice layers) allocation churn — deferred collection being the wrong trade for short-lived nested allocations, the same GC-under-churn regime where Go placed last in [#102](../102-binary-tree-level-order-traversal/). So the ordering is by allocator overhead on short-lived nested containers — raw malloc < `Box`/`Vec` ≈ **Kāra RC/`Vec`** < Go GC — with Kāra and Rust indistinguishable. Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`) over the run. Python is listed at **234 ms but ran K = 30,000 — 1/20 of the compiled iterations** (pure-Python recursion is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **2.4 MiB** peak RSS (parity with Rust's 2.2 MiB, above C's 1.5 MiB) vs Go's **7.5 MiB**. The kāra binary measures **336 KiB** here — a build-linkage artifact of this container run (heap-growing programs retain the backtrace-symbolizer tree `--gc-sections` should strip; a correct build is ~15 KiB), independent of the runtime numbers, flagged for the M5 — vs C's 16 KiB and Go's 2.2 MiB.

**Flagged for the M5 re-bench** — the Kāra≈Rust tie here is inside the noise, and the corpus has seen container tree orderings shift on the M5's wider core (see [#97](../../1-100/97-interleaving-string/), [#99](../../1-100/99-recover-binary-search-tree/)), so treat the *tie* as a data point, not a verdict; the C-floor and Go-last signs are robust.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference) and, once folded in, [`bench/results.json`](bench/results.json) (M5, canonical).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched nested-container allocation (`Vec[Vec[i64]]` vs `Vec<Vec<i64>>`, both over a by-reference tree walk), where Kāra and Rust come out indistinguishable. C's raw `malloc`/`realloc` is the metal floor, Go the GC data point (last, on nested-slice churn), Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
