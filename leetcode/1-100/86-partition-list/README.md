# 86. Partition List

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Linked List · Two Pointers &nbsp;·&nbsp; **Source:** [leetcode.com/problems/partition-list](https://leetcode.com/problems/partition-list/)

Given the head of a linked list and a value `x`, rearrange it so that all nodes with value **< x** come before all nodes with value **≥ x**, **preserving** the original relative order within each group (a *stable* partition). Return the new head.

```
1 → 4 → 3 → 2 → 5 → 2,  x = 3   ->   1 → 2 → 2 → 4 → 3 → 5
2 → 1,                  x = 2   ->   1 → 2
```

**Constraints:** `0 ≤ nodes ≤ 200`; `-100 ≤ Node.val ≤ 100`; `-200 ≤ x ≤ 200`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Two-list split, splice** ★ | [`partition_list.kara`](partition_list.kara) ✓ via `karac run` / `karac build` | [`partition_list.py`](partition_list.py) ✓ |
| **Value-collect then rebuild** | [`partition_list_collect.kara`](partition_list_collect.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output across all ten test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other, with the Python mirror, **and with a stable-partition ground truth** (`[v for v in xs if v < x] + [v for v in xs if v >= x]`). Both compile with **zero diagnostics**.

## Two ways to keep it stable

Both solvers use Kāra's reference-semantics node (a `shared struct`, Rc-like handle), the model of katas [#82](../82-remove-duplicates-from-sorted-list-ii/)/[#83](../83-remove-duplicates-from-sorted-list/):

```
shared struct ListNode { val: i64, mut next: Option[ListNode] }
```

**Two-list split** ([`partition_list.kara`](partition_list.kara), the ★) is the canonical O(n) pass. As it walks the input, each node is appended to one of two dummy-headed sublists — `less` for `val < x`, `greater` for the rest — and at the end the `less` tail is spliced onto the `greater` head:

```
less_tail, greater_tail = less_dummy, greater_dummy
for node in list:
    nxt = node.next; node.next = None          # detach before re-appending
    if node.val < x: less_tail.next = node; less_tail = node
    else:            greater_tail.next = node; greater_tail = node
less_tail.next = greater_dummy.next
return less_dummy.next
```

Because nodes are visited in order and only ever **appended**, each sublist keeps the original order — that is the stability. The load-bearing detail is `node.next = None` **before** re-appending: without it the last `greater` node would still point into the middle of the old list and close a cycle. Every splice re-links by aliasing the `shared struct` handle, no copying.

**Value-collect then rebuild** ([`partition_list_collect.kara`](partition_list_collect.kara)) reaches the same result by decomposing to arrays: one pass pushes each node's value into a `less` or `greater` `Vec[i64]` (in list order, so stable), then a fresh list is built by draining `less` then `greater`. No in-place relinking of the input at all — just two `Vec` partitions and a tail-cursor rebuild. A distinct surface (`Vec` push + list construction) that must land byte-identical to the pointer-splicing ★.

## Kāra features exercised

- **`shared struct` (Rc) linked list, detach-and-splice** — `node.next = None` then `less_tail.next = Some(node)` re-links by aliasing the Rc handle; the RC / ownership machinery under real pointer-mutation load, verified byte-identical under codegen *and* auto-par.
- **Two independent tail cursors** — `less_tail` and `greater_tail` advance separately over the same walk, each an `Option[ListNode]` handle re-pointed as nodes attach.
- **`Option` pattern matching** — `match cur { Some(node) => … None => break }` drives the walk; the collect variant folds the same walk into two `Vec[i64]`.
- **`Vec[i64]` partition + rebuild** — the collect variant pushes into two vectors and rebuilds a list with a tail cursor, indexing `less[i]` / `greater[j]` in the reconstruction loops.
- **Auto-parallelised batch reduction** — the benchmark's `for k in 0..K { sum += fold(partition(build(k))) }` is an associative reduction the default build **auto-parallelises** with no parallel source (see Benchmarks).

**v1 note.** Lists are short (`≤ 200` nodes) and values fit i64; the per-case sink folds each result's length and values into a running polynomial hash. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`, and both agree with the stable-partition ground truth on every case.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   partition_list.kara
karac build partition_list.kara && ./partition_list

# The value-collect-rebuild variant (identical output):
karac run partition_list_collect.kara

# Python
python3 partition_list.py

# Verify they all agree
diff <(karac run partition_list.kara) <(python3 partition_list.py)                  && echo OK
diff <(karac run partition_list.kara) <(karac run partition_list_collect.kara)      && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`partition_list.{kara,rs,c,py}`, `go-seq/main.go`, plus the par-lane `partition_list_par.c`, `rayon/`, `go-par/`).

> ⚠️ **Machine caveat.** Measured on a **shared x86-64 Linux cloud container** (Intel Xeon @ 2.80 GHz, 4 vCPU, Linux 6.18.5; karac from current `main`). These are container numbers only — this kata has **no M5 `results.json` yet**; it will be re-benched on the corpus's Apple M5 Pro and the canonical table added then. Don't compare absolute times/sizes/RSS against sibling katas' M5 tables; [`bench/results.container-x86.json`](bench/results.container-x86.json) records the real host.

**Two lanes over one workload.** A batch of **K = 170,000 independent** partitions: each iteration builds a **fresh M = 200-node linked list** whose values depend on the iteration index (`val = (j·7 + iter) % 100`, so no call hoists), stably partitions it around `x = 50`, and the per-iteration fold is combined through an **associative sum** (order-independent, so parallel and sequential produce the same total). This is an **allocation-bound** workload — a fresh M-node list is built and torn down every iteration — so *no* implementation scales linearly; the point is auto-par vs hand-tuned parallelism on equal, malloc-heavy footing. All nine seq + par mirrors must agree on `84997457408934` before timing.

- **Seq lane** — single-threaded: kāra (`KARAC_AUTO_PAR=0`) vs `rustc -O` / `clang -O3` / `go build` per-core.
- **Par lane** — the *same* batch, parallel: the default `karac build` **auto-parallelises the `for k in 0..K` sum reduction with no hand-written parallel code**, raced against hand-tuned C-pthreads, rayon, and goroutines.

**Equal reference semantics.** Kāra uses a `shared struct` (Rc-like) list; **Rust mirrors it with `Rc<RefCell<ListNode>>`** (same per-node reference-count overhead; each rayon task builds its own thread-local `Rc` lists), Go a GC-managed `*ListNode`, and **C a plain `malloc`/`free` raw-pointer list** (single-owner, the metal floor). **Equal safety:** the seq lane includes a `rustc -O -C overflow-checks=on` row (kata [#69](../69-sqrtx/)'s discipline).

#### Seq lane — single-threaded (`--warmup 3 --runs 20`)

| Implementation | Wall time |
|---|---|
| c    partition_list (clang -O3, malloc list)          | 531.3 ± 31.0 ms |
| **kāra partition_list (`KARAC_AUTO_PAR=0`)**          | **758.9 ± 12.8 ms** |
| rust partition_list (rustc -O, `Rc<RefCell>`)         | 795.6 ± 12.9 ms |
| rust partition_list (rustc -O, overflow-checks=on)    | 826.6 ± 17.3 ms |
| go   partition_list (`*Node`, GC)                     | 1038.9 ± 19.3 ms |

Single-threaded and at **matched reference semantics**, kāra's `shared struct` is **ahead of both Rust builds** (`Rc<RefCell>`'s per-access borrow-flag check is the gap — the same pattern as [#82](../82-remove-duplicates-from-sorted-list-ii/)/[#83](../83-remove-duplicates-from-sorted-list/)), and ~1.37× Go. C's unchecked raw-pointer list is the floor at ~1.43× under kāra. Python (K=8000) is ~0.42 s, timed separately.

#### Par lane — auto-par vs hand-tuned, NOT comparable to seq (`--warmup 5 --runs 30`)

| Implementation | Wall time |
|---|---|
| c    partition_list (pthreads — metal floor)            | 304.3 ± 43.1 ms |
| rust partition_list (rayon `into_par_iter`)             | 359.9 ± 7.9 ms |
| **kāra partition_list (auto-par, NO parallel code)**    | **366.5 ± 11.6 ms** |
| go   partition_list (goroutines + WaitGroup)            | 376.4 ± 13.6 ms |

The interesting result: because the workload is **allocation-bound** (`malloc`/`free` of an M-node list every iteration, contending under parallelism), *nobody* scales linearly — even raw C-pthreads gets only ~1.75× over its own seq lane. On that footing kāra's **zero-code auto-par ties hand-tuned rayon** (366.5 vs 359.9 ms, ~1.02×), sits ~1.20× off the pthreads floor, and edges the goroutine version. Against its own single-threaded seq lane (758.9 ms) that is a **2.07× self-speedup** on 4 vCPU — the *best parallel scaling of the group* — for free, no threads or annotations written. (Binary note: the seq build links a **15.4 KiB** minimal runtime — `KARAC_AUTO_PAR=0` needs no scheduler — while the auto-par build is 374 KiB.) Records in [`results.container-x86.json`](bench/results.container-x86.json).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — at **matched reference semantics** (`shared struct` vs `Rc<RefCell>`) single-threaded, and in the par lane kāra's zero-code auto-par vs hand-tuned rayon. C's raw-pointer list is the metal floor in both lanes, Go the GC data point, Python (a fraction of the iteration count, timed separately) the ergonomic foil.
