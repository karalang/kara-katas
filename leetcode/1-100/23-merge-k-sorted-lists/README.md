# 23. Merge k Sorted Lists

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Linked List, Divide and Conquer, Heap (Priority Queue), Merge Sort &nbsp;·&nbsp; **Source:** [leetcode.com/problems/merge-k-sorted-lists](https://leetcode.com/problems/merge-k-sorted-lists/)

Given an array of `k` linked lists, each sorted in non-decreasing order, splice all of them into one sorted list and return its head. Like kata [#21](../21-merge-two-sorted-lists/) — whose two-list merge is the inner kernel here — the result reuses the input nodes; no node is allocated.

```
[[1,4,5],[1,3,4],[2,6]]  → [1, 1, 2, 3, 4, 4, 5, 6]
[]                       → []
[[]]                     → []
```

**Constraints:** `0 ≤ k ≤ 10⁴` lists, each `0 ≤ length ≤ 500`, total nodes ≤ 10⁴, `-10⁴ ≤ Node.val ≤ 10⁴`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Divide and conquer: pairwise interval merging in place over the input Vec — round with interval d merges slot i with slot i+d, log k rounds, answer in slot 0 | O(N log k) time, O(1) extra | [`divide_and_conquer.kara`](divide_and_conquer.kara) ✓ via `karac run` / `karac build` | [`divide_and_conquer.py`](divide_and_conquer.py) ✓ |
| Binary min-heap of cursors: one frontier node per non-exhausted list, pop the global minimum, splice it, push its successor | O(N log k) time, O(k) extra | [`heap.kara`](heap.kara) ✓ via `karac run` / `karac build` | [`heap.py`](heap.py) ✓ |

`✓` runs end-to-end today. Both forms produce identical output under the interpreter and codegen against their Python mirrors across all ten test cases; the **divide-and-conquer** form is the benchmarked one.

## Why divide and conquer (and what the heap buys instead)

The naive fold — merge list 0 with list 1, that result with list 2, and so on — re-walks the growing accumulator on every step: O(kN). Pairwise divide-and-conquer fixes the imbalance by always merging lists of *equal pedigree*: round 1 merges neighbors at distance 1 (k → k/2 lists), round 2 at distance 2, … — log k rounds, each touching every live node once, so O(N log k) total. It is mergesort's combine tree applied to pre-sorted runs, and kata #21's two-list merge — dummy anchor, `<=` tie-break, one-move suffix graft — drops in unchanged as the kernel.

The in-place interval walk keeps the round bookkeeping at O(1) extra: after the round with interval d, slot i (i a multiple of 2d) holds the merge of old slots i and i+d; source slots at odd multiples of d are consumed exactly once and never read again, their stale handles simply sitting in the Vec until it drops. The answer ends in slot 0.

The heap form replaces the merge tree with a k-way frontier: a binary min-heap holds at most one cursor per non-exhausted list, keyed on the cursor's value; each step pops the global minimum, splices it onto the output tail, and pushes its successor. Same O(N log k), different constant profile — d&c does log k linear passes of branchy two-way compares; the heap does one pass with a log k sift per node. Kāra has no standard-library heap yet, so `heap.kara` hand-rolls one over a `Vec[ListNode]` — which is precisely why the style exists in this kata (see below).

**Stability:** `<=` in the kernel plus the interval pairing (lower-indexed list always the left operand) makes the d&c merge stable overall — equal keys come out in input-list order, the k-way extension of kata #21's tie rule. The heap form is *not* stable: equal keys pop in heap-shape order. Only values are printed, so the two styles still diff identical.

## Kāra features exercised

- **`Vec[Option[ListNode]]` — the corpus's first Vec of shared-struct handles.** The input is a Vec whose elements are RC-backed `Option[shared]` niche pointers (kata [#2](../2-add-two-numbers/)'s node model, now as *collection elements*). Vec slots are refcount-transparent — element reads alias without retaining, element writes overwrite without releasing, the buffer free walks no elements — so every consume/own decision sits at the call/return/store boundaries instead.
- **Owned Vec param moved into a mut local** — `let mut work = lists;` then in-place mutation: the param itself is immutable, so in-place interval merging requires the move. This is the shape that surfaced this kata's compiler bug (below).
- **Element read → consume → element write-back** — `work[i] = merge_two_lists(work[i], work[i + interval])` reads two slots as owned args, structurally consumes both chains, and writes the merged head back over slot i in one statement.
- **Hand-rolled binary heap over RC handles (`heap.kara`)** — `heap_push`/`heap_pop` with sift-up/sift-down: `heap[i].val` comparisons through two handles and slot swaps via element read + element write (`let tmp = heap[i]; heap[i] = heap[parent]; heap[parent] = tmp;`) — pure aliasing traffic on the heap array, plus `mut ref Vec[ListNode]` params with call-site `mut` markers (`heap_push(mut heap, node)`) per design.md Feature 4 Part 1½.
- **Splice-then-overwrite chain repair** — the heap form appends each popped node while its `next` still points at its source-list suffix; the next pop's `tail.next = Some(node)` overwrites the stale link, and the loop's termination (a node with no successor pushes nothing) guarantees the final node's `next` is `None`.

> **This kata found one karac codegen bug — an owned-param double-free whose symptoms scattered so widely it initially looked like three bugs.** `let mut work = lists;` where `lists` is a bare by-value `Vec` param: the let-move's move-suppression was written for local-to-local moves — applied to a *param* it armed the new binding as a second owner of a buffer the **caller** already frees (the kata-22 owned-param ABI). The double free's manifestation was pure allocator luck: of this kata's ten cases, five trapped (exit 133/134), three passed silently, and the split *changed* between default and `KARAC_AUTO_PAR=0` builds because the par runtime's startup allocations re-shuffle the heap — mimicking an auto-par race that didn't exist. Fixed on the spot (karac `9e261565`, 2026-06-07): the let-move (and assign-move) from an owned param now routes through the kata-22 defensive-copy machinery (`maybe_defensive_copy_param_arg`) — the binding owns a deep copy, the caller frees the original, and the param header stays intact for later consume sites. The heap form was never affected — it indexes the param Vec directly without a move. Regression pins: 4 E2E + 3 ASAN tests (the interval-merge ASAN pin fails pre-fix deterministically). Full record in the compiler's `docs/implementation_checklist/phase-7-codegen.md` § kata-23.

## Running

```bash
# Kāra — interpreter and codegen agree on both forms.
karac run   divide_and_conquer.kara
karac build divide_and_conquer.kara && ./divide_and_conquer
karac run   heap.kara
karac build heap.kara && ./heap

# Python
python3 divide_and_conquer.py
python3 heap.py

# Verify they agree (the two styles emit identical lines)
diff <(./divide_and_conquer)              <(python3 divide_and_conquer.py) && echo OK
diff <(karac run divide_and_conquer.kara) <(python3 divide_and_conquer.py) && echo OK
diff <(./heap)                            <(python3 heap.py)               && echo OK
diff <(karac run heap.kara)               <(python3 heap.py)               && echo OK
diff <(python3 divide_and_conquer.py)     <(python3 heap.py)               && echo STYLES-OK
```

## Benchmarks
Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`divide_and_conquer.{kara,rs,c,py}`, `go-seq/main.go`). Figures below are the 2026-10-31 re-bench (results.json `measured_at` 2026-11-01T01:26Z), measured with **karac 0.9.0-dev.14057+g6697158fa** — the v2/MIR backend (the legacy backend was deleted 2026-10-23).

**Workload.** Every iteration builds k = 8 fresh 128-node lists (1024 nodes malloc'd per iter), where list j holds values `j, j+8, j+16, …` — stride-k interleaving, so at *every* pairwise merge level the two operands fully interleave (the k-way generalization of kata [#21](../21-merge-two-sorted-lists/)'s evens/odds worst case, which defeats the branch predictor at all log k = 3 rounds). The merged 1024-node list is summed and freed. K = 100,000 iterations; the merged list is `[0..1023]`, sum `1023·1024/2 = 523,776`, sink `K · 523,776 =` **52,377,600,000** — all four compiled mirrors must agree before timing. This is kata #21's alloc/merge/drop workload scaled ~5× per iteration and given a merge *tree* instead of a single merge: same RC-node allocator churn, plus the interval walk's Vec element read/write traffic.

**Two-lane kata** (BENCH.md § Implicit auto-par): the default `karac build` links the par-dispatch surface (the K-loop fold is reduction-shaped), so the bench builds the dual binaries and reports them separately. Each *merge* is inherently sequential pointer-chasing, but the K-loop over independent iterations is not — auto-par parallelized across iterations through the 2026-08-05 feed, and the par lane below carries the full four-way comparator set. **On the 2026-10-31 MIR build auto-par does not fire** — see § Runtime — par lane.

### Runtime — seq lane

M5 Pro, 2026-10-31, karac g6697158fa (v2/MIR), `bench.sh` (hyperfine `--warmup 5 --runs 30 --shell=none`, structured-JSON emit). All compiled rows single-threaded; the kāra row is `KARAC_AUTO_PAR=0`.

| Implementation | Wall time | vs Kāra |
|---|---|---|
| go   divide_and_conquer            | 1.339 ± 0.013 s | 0.52× |
| c    divide_and_conquer (clang -O3) | 1.638 ± 0.078 s | 0.64× |
| **kāra divide_and_conquer**        | **2.578 ± 0.037 s** | **1.00×** |
| rust divide_and_conquer (`-C overflow-checks=on`) | 2.909 ± 0.066 s | 1.13× |
| rust divide_and_conquer            | 2.926 ± 0.070 s | 1.13× |

**Kāra leads Rust by 1.13×** and trails C by 1.57× and Go by 1.92×. Same cause as katas [#19](../19-remove-nth-node-from-end-of-list/) / [#21](../21-merge-two-sorted-lists/), amplified: Rust's reference-semantics mirror is `Rc<RefCell<ListNode>>`, and the merge *tree* multiplies the per-node `Rc` clone + `RefCell` borrow-flag traffic — every node is re-spliced at every one of the log k = 3 rounds, so Kāra stays ahead of Rust while its plain RC headers shrug the extra rounds off. Against the no-refcount mirrors the order is kata 21's: allocator-bound RC-node churn lands Kāra behind C's plain malloc/free and Go's GC arena (whose bump-allocated nodes and absent per-iter free win this workload outright). Note the equal-safety Rust row (`-C overflow-checks=on`) is indistinguishable from release here — this workload is allocator-bound, not arithmetic-bound, so the overflow-check tax that dominates katas like [#171](../../101-200/171-excel-sheet-column-number/) has nothing to bite on.

**MIR vs the previous feed (karac g4044152df, 2026-08-05), in language ratios:** Kāra/Rust 0.89× → 0.88×, Kāra/C 1.62× → 1.57×, Kāra/Go 1.99× → 1.92× — flat.

> **Provenance — the seq table moved between 2026-06-07 and 2026-08-05.** Earlier: go 1.116 / c 1.328 / kāra 1.967 / rust 2.385 s, quoted as "Kāra leads Rust by 1.44×." All four mirrors drifted up on the current toolchain (go +2.7 %, c +6.0 %, rust +7.4 %, kāra +16.2 %), narrowing the Rust lead to 1.12×. **Kāra's larger drift is not specific to this kata** — comparing `bench-baseline.json` (2026-06-06) against the current feed across 36 katas with a seq lane, kāra's median is **1.18× slower** while c (0.99×), go (0.98×) and rust (1.01×) are flat. That is a corpus-wide Kāra seq-lane regression over June, not a property of this workload, and it is unattributed to a specific commit.

### Runtime — par lane (auto-par, cross-lane — NOT comparable to the seq rows above)

M5 Pro, 2026-10-31, karac g6697158fa (v2/MIR). Kāra's row is the **default** `karac build` with **no parallel code in the source**; the other three are hand-written parallelism over the same K-loop.

| Implementation | Wall time | CPU | user |
|---|---|---|---|
| c    divide_and_conquer + pthreads (metal floor) | 0.323 ± 0.050 s | 1508 % | 4.87 s |
| rust divide_and_conquer + rayon                  | 0.501 ± 0.026 s | 1613 % | 8.05 s |
| rust + rayon (`-C overflow-checks=on`)           | 0.514 ± 0.026 s | 1632 % | 8.37 s |
| go   divide_and_conquer + goroutines             | 0.837 ± 0.006 s | 612 %  | 3.29 s |
| **kāra divide_and_conquer (default build) — auto-par does not fire (sequential program)** | **2.579 ± 0.046 s** | 100 % | 2.58 s |

**The kāra row is not a parallel result.** The default build's emitted IR (`KARAC_MIR_LL`) contains no `karac_mir_task_spawn` call, and the binary runs the sequential program: 2579 ms at 100 % CPU against the `KARAC_AUTO_PAR=0` twin's 2578 ms, with the same 302,880-byte binary. Read as a ratio it is 5.15× rayon, 7.98× the C pthreads floor and 3.08× Go — where the 2026-08-05 feed had Kāra at 1.49× rayon, 1.56× C and 1.13× Go with auto-par delivering 3.15× over its own seq lane. Filed as [`B-2026-10-31-43`](../../../../kara/docs/bugs-v2.md) (see § Bug ledger).

(History, 2026-08-05 legacy build: the auto-par row read 0.726 ± 0.177 s at 1759 % CPU / 12.76 s user, against C pthreads 0.466 s, rayon 0.487 s and Go 0.643 s — a correct parallel decomposition that trailed the hand-written mirrors because each worker carried the seq lane's RC/allocator tax; contrast [#394](../../301-400/394-decode-string/), where the same auto-par machinery beat both rayon and the C floor on fine-grained tasks.)

> **⚠️ Provenance — an earlier par figure here is unreproducible and has been removed.** This section previously claimed **213.1 ± 5.7 ms wall / 3.68 s user, "~8.7× over seq"** (dated 2026-06-07). The 2026-08-05 sink-verified measurement was 726.0 ms. The old figure is not merely stale, it is **internally implausible**: 213 ms would put Kāra 2.2× *faster* than hand-written parallel C (466 ms) on a workload where C beats it 1.62× in the seq lane. It also dates to the same day as the double-free fix this kata surfaced (karac `9e261565`), a bug whose manifestation explicitly "changed between default and `KARAC_AUTO_PAR=0` builds" — so the most likely reading is that it was measured on a binary that was not doing all the work. The 2026-08-05 number had sink agreement across all five binaries (`52377600000`). **Do not reinstate the 8.7× claim without a reproducible run.**

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py divide_and_conquer` (K=10k) — last measured by 2026-06-15, not re-run | 1.752 ± 0.033 s |

Not re-run on 2026-10-31 (the bench did not set `KARA_BENCH_INCLUDE_PY`). Python at K=10k was 1.75 s; projecting to the compiled mirrors' K=100k (~17.5 s) put it **~7.7× slower than the 2026-08-05 kāra seq figure** (17.5 / 2.285 s; a cross-session projection, not re-derived against the current feed) — the same narrow Python gap as katas 19/21, because node allocation happens in CPython's C internals and the workload has no arithmetic inner loop for the interpreter to lose on.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 divide_and_conquer.c           | **55.1 ± 1.0 ms** |
| rustc -O divide_and_conquer.rs           | 137.1 ± 2.0 ms |
| **karac build divide_and_conquer.kara**  | **152.2 ± 3.1 ms** |

On the MIR backend karac compiles **1.11× slower than `rustc -O`** and sits at **2.76× of clang -O3** (kata 21: 1.17× / 2.85×). The 2026-08-05 legacy build was 1.41× faster than rustc (96.2 ms vs 138.8 ms).

### Binary size

| Implementation | Size |
|---|---|
| c    divide_and_conquer            | 32.8 KiB |
| **kāra divide_and_conquer (seq)**  | **295.8 KiB** |
| kāra divide_and_conquer (par)      | 295.8 KiB |
| rust divide_and_conquer            | 456.6 KiB |
| go   divide_and_conquer            | 2434.2 KiB |

Every MIR Kāra binary is ~300–390 KB where the legacy backend's were ~34 KB (kara ledger [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md)); the seq binary is **295.8 KiB** (302,880 B, was 34,368 B in the 2026-08-05 feed), 1.54× under Rust's 456.6 KiB and 9.0× over C's 32.8 KiB. The default build is **byte-identical in size** (302,880 B; was 319,952 B with the auto-par machinery) — consistent with no task-spawn code being emitted ([`B-2026-10-31-43`](../../../../kara/docs/bugs-v2.md)). Both Kāra binaries undercut Rust's (456.6 KiB seq / 454.7 KiB rayon) and are ~8× smaller than Go's 2.4 MiB.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    divide_and_conquer            | 1.08 MiB |
| **kāra divide_and_conquer (seq)**  | **1.13 MiB** |
| rust divide_and_conquer            | 1.14 MiB |
| kāra divide_and_conquer (par)      | 1.11 MiB |
| go   divide_and_conquer            | 9.88 MiB |

Kāra's seq peak RSS sits within a page or so of Rust's (1,179,984 vs 1,196,344 B — single-shot `/usr/bin/time -l`, page-noisy, so read it as parity) and a hair over C (1,130,808 B). The 1024 nodes per iteration are allocated, merged, and fully freed inside the loop — steady state stays flat across all 100,000 iterations, the same leak-free splice story the kata-21 refcount fixes established, now over a merge tree. The par build's 1.11 MiB carries no worker pool this time (it was 3.0 MiB on 2026-08-05) — it runs sequentially; the hand-written par mirrors read C pthreads 2.45 MiB, rayon 3.52 MiB, Go 14.25 MiB. Go's seq 9.9 MiB is its GC arena + scheduler.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 divide_and_conquer.c          | 2.6 MiB |
| rustc -O divide_and_conquer.rs          | 33.1 MiB |
| **karac build divide_and_conquer.kara** | **58.9 MiB** |

On the MIR backend karac's compile-memory peak is **1.78× rustc's** and ~23× clang's (kata 21: 58.1 MiB). The 2026-08-05 legacy build peaked at 15.3 MiB, ~2.2× below rustc.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap — and on linked-list katas the Rust mirror's `Rc<RefCell<ListNode>>` reference semantics is the apples-to-apples comparator for Kāra's `shared struct` (katas 2 / 19 / 21 precedent). C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil.

## Calibration re-probe (2026-10-06)

Re-probed with new phrasings, on all four surfaces plus valgrind, as part of a ten-kata calibration batch (katas 1-49, against kata 352's probing). Gaps found, in the kara bug ledger:

- **B-2026-10-06-87** — comparing an indexed tuple element is refused by `karac build`, and `PriorityQueue[(..)]` cannot be built through the stdlib's `outranks`.
- The kata-2 tuple-literal `match` leak (B-2026-10-06-78) was hit again by the merge-two-lists step.

## Bug ledger

**Surfaced [`B-2026-10-31-43`](../../../../kara/docs/bugs-v2.md)** (perf, open). The default (auto-par) build no longer parallelizes the K-loop: its emitted IR (`KARAC_MIR_LL`) has no `karac_mir_task_spawn` call, and it runs the sequential program (2579 ms at 100 % CPU vs the `KARAC_AUTO_PAR=0` twin's 2578 ms, same binary size), so the par lane went 1.49× → 5.15× rayon. Measured 31 Oct 2026 with karac g6697158fa.
