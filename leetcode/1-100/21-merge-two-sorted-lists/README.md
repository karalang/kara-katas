# 21. Merge Two Sorted Lists

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Linked List, Recursion &nbsp;·&nbsp; **Source:** [leetcode.com/problems/merge-two-sorted-lists](https://leetcode.com/problems/merge-two-sorted-lists/)

Given the heads of two singly linked lists sorted in non-decreasing order, splice their nodes together into one sorted list and return its head. The merged list reuses the input nodes — no new node is allocated.

```
([1, 2, 4], [1, 3, 4])  → [1, 1, 2, 3, 4, 4]
([],        [])         → []
([],        [0])        → [0]
```

**Constraints:** `0 ≤ each list length ≤ 50`, `-100 ≤ Node.val ≤ 100`, both inputs sorted non-decreasing.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Iterative dummy-anchored splice: walk both lists, splice the smaller front onto a growing tail, graft the surviving suffix when one runs dry | O(m + n) time, O(1) extra | [`iterative.kara`](iterative.kara) ✓ via `karac run` / `karac build` | [`iterative.py`](iterative.py) ✓ |
| Recursive structural merge: pick the smaller front, set its `next` to the merge of the rest | O(m + n) time, O(m + n) stack | [`recursive.kara`](recursive.kara) ✓ via `karac run` / `karac build` | [`recursive.py`](recursive.py) ✓ |

`✓` runs end-to-end today. Both forms produce identical output under the interpreter and codegen across all nine test cases; the **iterative** form is the benchmarked one.

## Why iterative (and the dummy)

This is the merge step of a merge sort in linked-list form. Walk both lists with a cursor each (`a`, `b`); at every step compare the two front nodes and splice the smaller onto the growing output tail, advancing only that list's cursor. When one list runs dry, the other's remaining suffix is already sorted and already linked, so it attaches in one move — `tail.next = a` (or `b`) — with no per-node copying.

The **dummy node** is the same load-bearing trick as kata [#2](../2-add-two-numbers/) and kata [#19](../19-remove-nth-node-from-end-of-list/): a throwaway node before the output head so the first spliced node is not a special case. `tail` starts on the dummy; every iteration does `tail.next = <node>; tail = <node>;` uniformly, and the real head falls out as `dummy.next`.

`<=` (not `<`) on the tie makes the merge **stable**: when both fronts are equal, `a`'s node is taken first, so equal keys keep their list-1-before-list-2 order. Stability is invisible on bare `i64` values but is the property that makes this merge reusable as the combine step of a stable sort.

`i64` is *not* load-bearing — LeetCode bounds each list by 50 nodes and values to `[-100, 100]`, so `i32` would suffice; the width is for uniformity with the rest of the corpus (contrast kata [#18](../18-4sum/), where the 10⁹ bound forces `i64`).

## Kāra features exercised

- **`shared struct ListNode { val: i64, mut next: Option[ListNode] }`** — the same reference-semantics (RC-backed) linked-node model kata [#2](../2-add-two-numbers/) introduced. `Option[shared Self]` `next` fields use karac's niche layout (a single nullable pointer, not a 4-i64 tagged enum).
- **Cursor reassignment over a consumed list** — `let mut a = l1; … a = na.next;` walks a cursor that *destructively consumes* an existing list, distinct from kata 2/19's append-only builders where the cursor advances over freshly-allocated nodes. This is the first kata in the run to mutate two pre-existing shared-struct lists via interleaved cursors.
- **In-place structural splice from two sources** — `tail.next = Some(na)` then `tail = na`, alternating between the two input lists, re-links existing nodes into a new order with no allocation.
- **`if let` Option destructuring + suffix graft** — the lockstep walk uses nested `if let Some(na) = a { if let Some(nb) = b { … } else { tail.next = a; break } }`, and the surviving suffix attaches with a single `tail.next = a` (or `b`).
- **Bounded non-tail recursion (`recursive.kara`)** — one frame per node consumed, fine at LeetCode's ≤ 50-per-list bound. The source header (lines 21–24) notes Kāra does not yet guarantee TCO; guaranteed tail calls (`#[tailrec]` / the reserved `become` keyword) are designed and deferred in kara `docs/deferred.md § Tail-Call Optimization`, which names this file as its standing corpus citation. Honest caveat recorded there too: this merge shape is *not* tail-recursive as written (the call's result feeds a field store before the return), so a TCO rewrite would be accumulator-style.

> **This kata drove a round of `karac` shared-struct refcount hardening.** It is the first to walk a *destructive cursor* over a shared-struct list (`let mut a = l1; a = na.next;`) and to splice from two sources, which surfaced four distinct use-after-free bugs in codegen — all fixed: (1) an un-annotated `let mut a = l1` over an `Option[shared]` binding wasn't registered for refcount management, so the cursor advance freed the aliased node; (2) a branch-buried `Option[shared]` parameter return (`fn pick(l1,l2){ if let Some(_)=l1 {l1} else {l2} }`) freed the returned chain; (3) passing a niche `Option[shared]` field (`merge(n1.next, l2)`) under-counted vs the callee; (4) the recursive form mixes `Some(<alias>)` returns (which the constructor already retains) with bare-arg `l1`/`l2` returns (which need a compensating inc) in one function — fixed with *per-branch, flow-sensitive* compensation that inc's a bare-arg leaf only in the specific arm that returns it. Both forms are now `karac build`-correct and leak-free — the iterative and recursive merge both hold flat RSS (1.8 MB) across 500k merges. See the compiler's `docs/implementation_checklist/phase-7-codegen.md` for the per-branch fix.

## Running

```bash
# Kāra — interpreter and codegen agree on both forms.
karac run   iterative.kara
karac build iterative.kara && ./iterative
karac run   recursive.kara
karac build recursive.kara && ./recursive

# Python
python3 iterative.py
python3 recursive.py

# Verify they agree
diff <(./iterative)                <(python3 iterative.py)  && echo OK
diff <(karac run iterative.kara)   <(python3 recursive.py)  && echo OK
diff <(karac run recursive.kara)   <(python3 recursive.py)  && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`iterative.{kara,rs,c,py}`, `go-seq/main.go`).

**Workload.** Two fresh fully-interleaving N = 100-node lists are built every iteration (`a` = evens `[0, 2, …, 198]`, `b` = odds `[1, 3, …, 199]`) — the merge consumes and re-links them, so each iter needs fresh inputs — then merged and the 200-node result summed. K = 500,000 iterations. Evens-vs-odds is the worst case for the splice: it alternates between the two lists on *every* node, so no run of same-side nodes lets the branch predictor settle. The merged list is `[0, 1, …, 199]`, whose sum is `199·200/2 = 19900`; the sink is the running total `K·19900 =` **9,950,000,000**, and all four compiled mirrors must agree before timing.

**Seq lane** (BENCH.md two-lane discipline): per-call work is a linear build ×2 + a linear two-pointer merge + a linear sum — small enough that a parallel lane would mostly measure worker-pool dispatch, so this stays single-threaded and measures pure codegen quality, same call kata [#2](../2-add-two-numbers/) and [#19](../19-remove-nth-node-from-end-of-list/) make. The kāra binary is built with `KARAC_AUTO_PAR=0` (dual-binary seq pattern) so the K-loop reduction stays single-threaded and directly comparable to `rustc -O` / `clang -O3` / `go build`.

This is the **alloc/merge/drop peer to kata 19's alloc/splice/drop**: where kata 19 builds one input list per iter and splices one node out, this builds *two* input lists per iter and re-links all 2N nodes into a merged order — the same RC-node allocator traffic, plus a two-source interleaved structural splice.

### Runtime — seq lane

Snapshot — M5 Pro, 2026-06-06, `bench.sh` (hyperfine `--warmup 5 --runs 30 --shell=none`, structured-JSON emit). All four single-threaded.

| Implementation | Wall time |
|---|---|
| go   iterative                     | 1.001 ± 0.012 s |
| c    iterative (clang -O3)         | 1.083 ± 0.030 s |
| **kāra iterative**                 | **1.245 ± 0.074 s** |
| rust iterative                     | 1.510 ± 0.096 s |

**Kāra leads Rust by 1.21×** and trails C by 1.15× and Go by 1.24×. Same cause as kata [#19](../19-remove-nth-node-from-end-of-list/): Rust's reference-semantics linked list is `Rc<RefCell<ListNode>>`, whose per-node `Rc` refcount + `RefCell` borrow-flag traffic is heavier than Kāra's plain RC header. Against the manual-memory floor the order flips — this kata is allocator-bound (build + drop ~200 nodes per iter, plus the re-link), and Kāra's per-node RC inc/dec bookkeeping sits just behind C's plain `malloc`/`free` and Go's GC-managed pointer nodes; with no sort here, pure RC-node churn is the whole workload, so Kāra lands a hair behind the no-refcount mirrors. The Rust gap is the load-bearing number, driven by `Rc<RefCell>`.

(History: the 2026-05-30 snapshot read kāra 1.212 ± 0.036 / C 1.085; 06-05 read kāra 1.109 / C 1.065 with byte-identical binaries — batch conditions. The **06-06 batch is the first with a changed kāra binary**: the 2026-06-05/06 karac refcount-soundness overhaul (unwrap receive-inc, field-let alias acquire, explicit-return compensation, tail-zeroing retirement — four UAF classes closed, several surfaced by THIS kata's splice shapes) costs this alias-heaviest kata **~5% in a controlled same-load old-vs-new A/B (1.05 ± 0.02×, 1.125 → 1.184 s, 40 runs)** — a real regression, accepted as the soundness price; binary size unchanged (33 624 B). The table above is the canonical `bench.sh`/results.json run (wider σ, ~6% load drift vs the controlled A/B — read the A/B for the codegen attribution and the table for cross-language position). Splice/re-parenting shapes are outside the current RC-elision phases (B1/B2 are append-only) — recovering the 5% would need splice-aware elision, tracked in the karac wip doc. **Separately, the DEFAULT (non-`KARAC_AUTO_PAR=0`) build now auto-parallelizes the K-loop** (karac auto-par engages where it previously fell back; 90.2 ms wall / 1.45 s user, ~12.7× over seq on 18 cores) — per BENCH.md lane discipline the table above stays seq-lane; the par lane needs its own same-lane comparators before it can headline.)

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py iterative` (K=100k) | 2.163 ± 0.010 s |

Python at K=100k is 2.16 s; projecting to the compiled mirrors' K=500k (~10.8 s) puts it **~9.8× slower than kāra seq** — a narrow Python gap (as in kata 19), because the workload is dominated by allocation (which CPython does in C) and pointer-chasing rather than arithmetic the interpreter would run bytecode-by-bytecode.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 iterative.c           | **41.6 ± 0.8 ms** |
| **karac build iterative.kara**  | **79.0 ± 1.1 ms** |
| rustc -O iterative.rs           | 100.4 ± 1.0 ms |

Kāra compiles **1.27× faster than `rustc -O`** and sits at **1.90× of clang -O3** — same shape as the rest of the corpus. (06-06 batch: karac 79.0, rustc 100.4, clang 41.6 — karac is +2.3 ms vs 06-05 despite the compiler having grown the June elision/niche analysis passes; within the corpus-wide compile-cost band.)

### Binary size

| Implementation | Size |
|---|---|
| c    iterative                     | 32.8 KiB |
| **kāra iterative**                 | **32.8 KiB** |
| rust iterative                     | 456.2 KiB |
| go   iterative                     | 2434.1 KiB |

Kāra's seq binary is **32.8 KiB — byte-for-byte 64 bytes off C's 32.8 KiB** (33,624 vs 33,560 B), and far below Rust's 456 KiB. This kata calls no `sort_by` and triggers no auto-par dispatch, so it never links the ~262 KiB libstd panic/backtrace floor that dominates the sort-using katas (15 / 16 / 18) and every auto-par binary (~295 KiB) — see [kata 16 § Binary size](../16-3sum-closest/README.md) for that breakdown. With no sort, a `shared struct` linked-list program is as small as the C mirror. The 06-05 rebuild reproduced all four binary sizes from the 05-30 table exactly.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| **kāra iterative**                 | **1.0 MiB** |
| c    iterative                     | 1.1 MiB |
| rust iterative                     | 1.1 MiB |
| go   iterative                     | 9.7 MiB |

Kāra's peak RSS sits **at C's level** — the 2026-05-30 sample read the two byte-identical (1,179,984 B each); the 06-05 sample read kāra a shade *below* C (1,098,016 vs 1,130,784 B). These are single-shot `/usr/bin/time -l` readings, page-level noisy, so the honest claim is parity within a couple of 16 KiB pages, not a stable byte match. Either way the structural point holds: the two per-iter lists are allocated, merged, and fully freed inside the loop, so steady state stays flat across all 500,000 iterations with no growth. Rust's `Rc<RefCell>` adds a hair; Go's 9.7 MiB carries its GC arena + scheduler. Reaching flat RSS here is what the shared-struct refcount fixes this kata drove are about — a stress run of 500k merges holds flat at ~1 MiB, confirming the destructive-cursor splice is leak-free (see § Kāra features).

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 iterative.c          | 2.5 MiB |
| **karac build iterative.kara** | **11.3 MiB** |
| rustc -O iterative.rs          | 30.9 MiB |

Kāra's compile-memory footprint is ~4× clang's and ~3× lower than rustc's on this kata — same shape as the rest of the corpus.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil. On this allocator-bound linked-list kata **Kāra leads Rust by 1.21×**, the same `Rc<RefCell>` cause kata 2 / 19 identify; against the no-refcount mirrors (C, Go) Kāra trails (1.15× / 1.24×) because pure RC-node churn — with no sort to amortize — is the whole workload, plus the ~5% June soundness-fix cost noted above.
