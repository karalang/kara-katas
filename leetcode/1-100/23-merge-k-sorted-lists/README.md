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

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`divide_and_conquer.{kara,rs,c,py}`, `go-seq/main.go`).

**Workload.** Every iteration builds k = 8 fresh 128-node lists (1024 nodes malloc'd per iter), where list j holds values `j, j+8, j+16, …` — stride-k interleaving, so at *every* pairwise merge level the two operands fully interleave (the k-way generalization of kata [#21](../21-merge-two-sorted-lists/)'s evens/odds worst case, which defeats the branch predictor at all log k = 3 rounds). The merged 1024-node list is summed and freed. K = 100,000 iterations; the merged list is `[0..1023]`, sum `1023·1024/2 = 523,776`, sink `K · 523,776 =` **52,377,600,000** — all four compiled mirrors must agree before timing. This is kata #21's alloc/merge/drop workload scaled ~5× per iteration and given a merge *tree* instead of a single merge: same RC-node allocator churn, plus the interval walk's Vec element read/write traffic.

**Two-lane kata** (BENCH.md § Implicit auto-par): the default `karac build` links the par-dispatch surface (the K-loop fold is reduction-shaped), so the bench builds the dual binaries and reports them separately. The merge itself is inherently sequential pointer-chasing, so the default lane mostly measures what the linked surface costs.

### Runtime — seq lane

Snapshot — M5 Pro, 2026-06-07, `bench.sh` (hyperfine `--warmup 5 --runs 30 --shell=none`, structured-JSON emit). All four compiled rows single-threaded; the kāra row is `KARAC_AUTO_PAR=0`.

| Implementation | Wall time |
|---|---|
| go   divide_and_conquer            | 1.116 ± 0.010 s |
| c    divide_and_conquer (clang -O3) | 1.328 ± 0.060 s |
| **kāra divide_and_conquer**        | **1.967 ± 0.057 s** |
| rust divide_and_conquer            | 2.385 ± 0.059 s |

**Kāra leads Rust by 1.44×** and trails C by 1.10× and Go by 1.44×. Same cause as katas [#19](../19-remove-nth-node-from-end-of-list/) / [#21](../21-merge-two-sorted-lists/), amplified: Rust's reference-semantics mirror is `Rc<RefCell<ListNode>>`, and the merge *tree* multiplies the per-node `Rc` clone + `RefCell` borrow-flag traffic — every node is re-spliced at every one of the log k = 3 rounds, so the Rust gap widens from kata 21's 1.21× to 1.44× while Kāra's plain RC headers shrug the extra rounds off. Against the no-refcount mirrors the order is kata 21's: allocator-bound RC-node churn lands Kāra just behind C's plain malloc/free and Go's GC arena (whose bump-allocated nodes and absent per-iter free win this workload outright).

**Separately, the DEFAULT (non-`KARAC_AUTO_PAR=0`) build auto-parallelizes the K-loop**: 213.1 ± 5.7 ms wall / 3.68 s user — **~8.7× over seq** on 18 cores. Per BENCH.md lane discipline the table above stays seq-lane; the par number is reported on its own row of `results.json` and has no same-lane comparator here.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py divide_and_conquer` (K=10k) | 1.752 ± 0.033 s |

Python at K=10k is 1.77 s; projecting to the compiled mirrors' K=100k (~17.7 s) puts it **~10.4× slower than kāra seq** — the same narrow Python gap as katas 19/21, because node allocation happens in CPython's C internals and the workload has no arithmetic inner loop for the interpreter to lose on.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 divide_and_conquer.c           | **52.5 ± 0.3 ms** |
| **karac build divide_and_conquer.kara**  | **96.2 ± 0.6 ms** |
| rustc -O divide_and_conquer.rs           | 138.8 ± 1.3 ms |

Kāra compiles **1.41× faster than `rustc -O`** and sits at **1.80× of clang -O3** — same shape as the rest of the corpus (kata 21: 1.27× / 1.90×).

### Binary size

| Implementation | Size |
|---|---|
| c    divide_and_conquer            | 32.8 KiB |
| **kāra divide_and_conquer (seq)**  | **33.3 KiB** |
| kāra divide_and_conquer (par)      | 296.1 KiB |
| rust divide_and_conquer            | 456.6 KiB |
| go   divide_and_conquer            | 2434.2 KiB |

Kāra's seq binary is **32.9 KiB — 136 bytes off C's 32.8 KiB** (33,712 vs 33,576 B), the kata-21 story verbatim: no sort, no auto-par dispatch in the seq build, so the ~262 KiB libstd floor never links and a `shared struct` linked-list program lands at C size. The default build's 295.8 KiB is the standard auto-par floor (see [kata 16 § Binary size](../16-3sum-closest/README.md)).

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    divide_and_conquer            | 1.1 MiB |
| **kāra divide_and_conquer (seq)**  | **1.2 MiB** |
| rust divide_and_conquer            | 1.2 MiB |
| kāra divide_and_conquer (par)      | 3.0 MiB |
| go   divide_and_conquer            | 9.4 MiB |

Kāra's seq peak RSS reads byte-identical to Rust's in this sample (1,245,472 B each — single-shot `/usr/bin/time -l`, page-noisy, so read it as parity) and a hair over C. The 1024 nodes per iteration are allocated, merged, and fully freed inside the loop — steady state stays flat across all 100,000 iterations, the same leak-free splice story the kata-21 refcount fixes established, now over a merge tree. The par build's 3.0 MiB carries the worker pool; Go's 9.4 MiB its GC arena + scheduler.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 divide_and_conquer.c          | 2.5 MiB |
| **karac build divide_and_conquer.kara** | **15.3 MiB** |
| rustc -O divide_and_conquer.rs          | 33.1 MiB |

Kāra's compile-memory footprint is ~5.5× clang's and ~2.4× below rustc's — corpus shape (kata 21 read 11.3 MiB on a slightly smaller program).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap — and on linked-list katas the Rust mirror's `Rc<RefCell<ListNode>>` reference semantics is the apples-to-apples comparator for Kāra's `shared struct` (katas 2 / 19 / 21 precedent). C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil.
