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

> ✅ **M5 re-bench (2026-11-01).** Measured on the corpus's **Apple M5 Pro reference machine** (arm64, 6P+12E = 18 logical cores; clang 21 / rustc 1.95 / go 1.26) with **karac g6697158fa** (0.9.0-dev.14057, the v2/MIR backend; the legacy backend was deleted 2026-10-23). The first M5 snapshot (2026-08-05) replaced an earlier x86-64 cloud-container one. Seq lane: kāra **ties both Rust builds** within noise (behind C/Go on this allocation-bound list); flat against every comparator since 2026-08-05. The par lane is the standout and improved against all three comparators — kāra's zero-parallel-code auto-par **beats hand-tuned rayon 1.55×** and goroutines 2.49×, lands within 1.05× of the C-pthreads floor, for a **7.19× self-speedup** over its own seq lane. `bench/results.json` records the M5 host.
>
> ⚠️ **Provenance — this kata's par lane regressed and was repaired between snapshots.** The 2026-07-28 corpus run recorded kāra's par row at **683.7 ms @ 99.8 % CPU** — auto-par had silently stopped firing, so a *sequential* binary was published against parallel rayon, reading as "0.25× / ~4× slower than rayon" in the public feed. Cause: auto-par's cross-task-safety gate was TYPE-based and declined a reduction whose body allocates an iteration-local `shared` value (karac **B-2026-07-30-1**, fixed 2026-07-30 in `05b1fe66`). This README was *not* wrong during that window — it still carried the pre-regression 2026-07-11 numbers, which is why it disagreed with `results.json`. Both agreed on the 2026-08-05 re-bench, and again on the 2026-11-01 one, sink-verified across all five binaries (`84997457408934`).

**Two lanes over one workload.** A batch of **K = 170,000 independent** partitions: each iteration builds a **fresh M = 200-node linked list** whose values depend on the iteration index (`val = (j·7 + iter) % 100`, so no call hoists), stably partitions it around `x = 50`, and the per-iteration fold is combined through an **associative sum** (order-independent, so parallel and sequential produce the same total). This is an **allocation-bound** workload — a fresh M-node list is built and torn down every iteration — so *no* implementation scales linearly; the point is auto-par vs hand-tuned parallelism on equal, malloc-heavy footing. All nine seq + par mirrors must agree on `84997457408934` before timing.

- **Seq lane** — single-threaded: kāra (`KARAC_AUTO_PAR=0`) vs `rustc -O` / `clang -O3` / `go build` per-core.
- **Par lane** — the *same* batch, parallel: the default `karac build` **auto-parallelises the `for k in 0..K` sum reduction with no hand-written parallel code** (verified in the emitted IR (`KARAC_MIR_LL`): the default build calls `karac_mir_task_spawn`, the `KARAC_AUTO_PAR=0` twin does not), raced against hand-tuned C-pthreads, rayon, and goroutines.

**Equal reference semantics.** Kāra uses a `shared struct` (Rc-like) list; **Rust mirrors it with `Rc<RefCell<ListNode>>`** (same per-node reference-count overhead; each rayon task builds its own thread-local `Rc` lists), Go a GC-managed `*ListNode`, and **C a plain `malloc`/`free` raw-pointer list** (single-owner, the metal floor). **Equal safety:** the seq lane includes a `rustc -O -C overflow-checks=on` row (kata [#69](../69-sqrtx/)'s discipline).

#### Seq lane — single-threaded (`--warmup 3 --runs 20`; M5 Pro, karac g6697158fa, 2026-11-01)

| Implementation | Wall time |
|---|---|
| c    partition_list (clang -O3, malloc list)          | **491.7 ± 22.0 ms** |
| go   partition_list (`*Node`, GC)                     | 531.2 ± 5.2 ms |
| rust partition_list (rustc -O, `Rc<RefCell>`)         | 724.2 ± 22.6 ms |
| rust partition_list (rustc -O, overflow-checks=on)    | 736.8 ± 37.3 ms |
| **kāra partition_list (`KARAC_AUTO_PAR=0`)**          | **746.0 ± 32.0 ms** |

Single-threaded and at **matched reference semantics**, kāra's `shared struct` **ties both Rust builds** (746.0 vs `Rc<RefCell>` 724.2 / 736.8 ms — 1.03× / 1.01×, inside every row's σ; Kāra/Rust was 0.99× on 2026-08-05, so flat). On the M5 the native front pulls away on this allocation-bound partition: C's unchecked pointer list at 1.52× under kāra and Go's GC list at 1.40× (both flat since 2026-08-05: 1.43× and 1.40×). Overflow checks are free here. Python is timed separately.

#### Par lane — auto-par vs hand-tuned, NOT comparable to seq (`--warmup 5 --runs 30`; M5 Pro, karac g6697158fa, 2026-11-01)

| Implementation | Wall time |
|---|---|
| c    partition_list (pthreads — metal floor)            | **99.2 ± 15.6 ms** |
| **kāra partition_list (auto-par, NO parallel code)**    | **103.7 ± 8.2 ms** |
| rust partition_list (rayon `into_par_iter`)             | 161.3 ± 17.1 ms |
| rust partition_list (rayon, overflow-checks=on)         | 170.1 ± 21.5 ms |
| go   partition_list (goroutines + WaitGroup)            | 258.8 ± 3.1 ms |

The standout: kāra's **zero-parallel-code auto-par beats hand-tuned rayon** (103.7 vs 161.3 ms, **1.55×**; 1.64× against the equal-safety rayon build) and the goroutine version (258.8 ms, 2.49×), and sits within 1.05× of the raw-pthreads floor (99.2 ms, inside C's ±15.6 ms). That is an improvement against all three since 2026-08-05: Kāra/rayon 0.79× → 0.64×, Kāra/C 1.55× → 1.05×, Kāra/Go 0.67× → 0.40×. It also spends less total CPU than rayon (1.38 s of user time vs rayon's 2.72 s; C-pthreads 1.25 s). rayon's per-task overhead on this build-a-fresh-list-per-iteration batch is higher than the compiler's leaner reduction split — the inverse of sibling [#84](../84-largest-rectangle-in-histogram/), where rayon edged kāra. Against its own single-threaded seq lane (746.0 ms) that is a **7.19× self-speedup** on the M5's 18 cores, for free — no threads or annotations written. Note the wide σ on the sub-200 ms par rows (C ±15.6, rayon ±17.1, kāra ±8.2) — at this duration the lane is dispatch-noise-dominated; the ordering against rayon and Go is stable across runs, but treat the exact ratios as ±0.1 and kāra-vs-C as a tie. See [`bench/results.json`](bench/results.json).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — at **matched reference semantics** (`shared struct` vs `Rc<RefCell>`) single-threaded, and in the par lane kāra's zero-code auto-par vs hand-tuned rayon. C's raw-pointer list is the metal floor in both lanes, Go the GC data point, Python (a fraction of the iteration count, timed separately) the ergonomic foil.
