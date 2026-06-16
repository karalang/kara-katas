# 25. Reverse Nodes in k-Group

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Linked List, Recursion &nbsp;·&nbsp; **Source:** [leetcode.com/problems/reverse-nodes-in-k-group](https://leetcode.com/problems/reverse-nodes-in-k-group/)

Given the head of a singly linked list, reverse the nodes of the list k at a time and return the modified list. Nodes must be re-linked, not have their values rewritten, and a trailing group of fewer than k nodes stays in its original order.

```
[1, 2, 3, 4, 5], k = 2  → [2, 1, 4, 3, 5]
[1, 2, 3, 4, 5], k = 3  → [3, 2, 1, 4, 5]
[1, 2, 3, 4, 5], k = 5  → [5, 4, 3, 2, 1]
[1, 2, 3, 4, 5], k = 1  → [1, 2, 3, 4, 5]
```

**Constraints:** `1 ≤ k ≤ n ≤ 5000`, `0 ≤ Node.val ≤ 1000`.

This is the Hard generalization of kata [#24](../24-swap-nodes-in-pairs/): at k = 2 the group reversal degenerates to exactly that kata's three-store pair swap, and the trailing partial group generalizes its odd-length singleton. It is also the corpus's first **full in-segment pointer reversal** — the classic reverse-a-linked-list loop, run k nodes at a time.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Iterative dummy-anchored group walk: probe k ahead, reverse the group in place (`prev`/`cur` pointer loop seeded on the suffix), graft via `group_prev` | O(n) time, O(1) extra | [`iterative.kara`](iterative.kara) ✓ via `karac run` / `karac build` | [`iterative.py`](iterative.py) ✓ |
| Recursive one group per frame: probe k ahead, recurse on the rest *first*, reverse the local k nodes onto the already-reversed tail | O(n) time, O(n/k) stack | [`recursive.kara`](recursive.kara) ✓ via `karac run` / `karac build` | [`recursive.py`](recursive.py) ✓ |

`✓` runs end-to-end today. Both forms produce identical output under the interpreter and codegen across all nine test cases; the **iterative** form is the benchmarked one.

## Why iterative (and the seeded reversal)

Each round handles one group, anchored by a `group_prev` cursor (initially a dummy before the head — the same load-bearing trick as katas [#2](../2-add-two-numbers/)/[#19](../19-remove-nth-node-from-end-of-list/)/[#21](../21-merge-two-sorted-lists/)/[#24](../24-swap-nodes-in-pairs/), so reversing the head group needs no special case):

```
group_prev → n1 → n2 → … → nk → rest      becomes      group_prev → nk → … → n2 → n1 → rest

  1. Probe   — walk k nodes from group_prev.next; if the list runs out, the
               partial suffix stays as-is and the walk ends. The probe rests
               on `rest`, the first node after the group.
  2. Reverse — the standard three-local pointer reversal (prev/cur/saved
               next), run exactly k steps, with `prev` seeded to `rest`
               rather than None — the old group head (which becomes the
               group *tail*) links straight to the suffix, no fix-up pass.
  3. Graft   — group_prev.next = prev (the old k-th node, the new group
               head); group_prev advances to the old group head (now the
               tail), anchoring the next group.
```

Where kata [#24](../24-swap-nodes-in-pairs/)'s pair swap is a fixed three-store dance, the reversal loop here displaces a node on **every step**: `cur = node.next` then `node.next = prev` rewrites the field a live pattern binding was just unwrapped from, k times per group — the alias-under-displacement shape that found kata #24's refcount bug, now in a loop instead of a straight line. The probe's `break` out of a `match` arm inside `while` exercises the other kata-#24 fix (early-exit cleanup drains) every round.

`i64` is *not* load-bearing — values are bounded by 1000; the width is for uniformity with the rest of the corpus (contrast kata [#18](../18-4sum/), where the 10⁹ bound forces `i64`).

## Kāra features exercised

- **`shared struct ListNode { val: i64, mut next: Option[ListNode] }`** — the same reference-semantics (RC-backed) linked-node model as katas 2/19/21/23/24, with niche `Option[shared]` layout (a single nullable pointer).
- **Pattern-bound aliases under displacement, in a loop** — every reversal step unwraps `cur` into `node`, then overwrites `node.next` while the binding is live. Kata [#24](../24-swap-nodes-in-pairs/) did this three times per pair in straight-line code; here it's the loop body itself.
- **`break` from a `match` arm inside `while`** — the probe's fewer-than-k exit drains cleanup frames mid-walk every round (the kata-#24 `break`-drain fix, `cb33da55`, re-exercised at every group boundary).
- **Early `return` from inside a `while` + `match` nest (`recursive.kara`)** — the probe's None arm returns the partial suffix through two live nesting levels.
- **Deepest recursion in the corpus (`recursive.kara`)** — one frame per *group*: depth n/k, degenerating to one frame per *node* at k = 1. At LeetCode's n = 5000 bound that's 5000 frames — the depth stress that found this kata's compiler bug (below). Not tail-recursive (the call's result seeds the local reversal); same TCO caveat as katas #21/#24 (kara `docs/deferred.md § Tail-Call Optimization`).

> **This kata found one `karac` bug — fixed on the spot (karac `e7bd9387`).** Both forms were correct under interpreter *and* codegen across all nine cases on the first build — the pattern-binding alias acquire + early-exit drain machinery kata #24 forced into karac (`cb33da55`) held for the looped generalization with no further refcount fixes, and a 500k-iteration × 100-node reversal stress holds flat RSS (~1.0 MiB) on both forms. The finding came from the **depth stress** instead: at LeetCode's own bound (k = 1 over a 5000-node list — one recursion frame per node), `karac run` aborted with a hard stack overflow while the AOT binary ran fine. The tree-walk interpreter bills ~8 Rust frames per Kāra call, so its fixed 16 MB thread stack cliffed at a depth a conforming program can reach. karac now grows the interpreter stack onto heap segments at every Kāra call boundary (`stacker::maybe_grow`, 2 MiB red zone / 32 MiB segments) — recursion depth is heap-bounded, `karac run` matches the AOT binary on the full 5000-frame stress, and `par { }` worker threads are covered at whatever stack size they spawn with. See the compiler's `docs/implementation_checklist/phase-4-interpreter.md` entry.

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

**Workload.** A fresh N = 100-node list (`[1, 2, …, 100]`) is built every iteration — the reversal consumes and re-links it, so each iter needs fresh input — then the list is reversed in groups of **k = 5** in place and summed. K = 500,000 iterations. The reversal moves no values, so the per-iter sum is the invariant `N·(N+1)/2 = 5050` and the sink is `K·5050 =` **2,525,000,000** — a reversal that drops or duplicates a node breaks the sink, which all four compiled mirrors must agree on before timing.

**Seq lane** (BENCH.md two-lane discipline): per-call work is a linear build + a probe walk + a linear group reversal + a linear sum — the kāra binary is built with `KARAC_AUTO_PAR=0` (dual-binary seq pattern) so the K-loop reduction stays single-threaded and directly comparable to `rustc -O` / `clang -O3` / `go build`.

This is the **heavier sibling of kata [#24](../24-swap-nodes-in-pairs/)'s workload**: same fresh-list-per-iter alloc/drop churn, but each node is visited twice per pass (once by the probe, once by the reversal store) instead of kata 24's single pair-walk, and every node's `next` is rewritten rather than half of them.

### Runtime — seq lane

Snapshot — M5 Pro, 2026-06-07, `bench.sh` (hyperfine `--warmup 5 --runs 30 --shell=none`, structured-JSON emit). All four single-threaded.

| Implementation | Wall time |
|---|---|
| go   iterative                     | 0.497 ± 0.006 s |
| c    iterative (clang -O3)         | 0.562 ± 0.015 s |
| **kāra iterative**                 | **0.798 ± 0.028 s** |
| rust iterative                     | 0.855 ± 0.043 s |

**Kāra leads Rust by 1.12×** and trails C by 1.31× and Go by 1.74×. Same cause structure as kata [#24](../24-swap-nodes-in-pairs/) (which read 1.23× / 1.12× / 1.56×), with the C gap widened by what this kata adds: the reversal unwraps-and-rewraps **every node** — a refcount acquire/release pair per step where kata 24's pair dance paid per-pair — and the probe pre-walk traverses each group a second time. Rust's `Rc<RefCell<ListNode>>` mirror pays the same per-step shape (an `Rc` clone plus `RefCell` borrow-flag traffic per reversal store), which is why Kāra still leads it; against C's bare pointer stores the soundness bookkeeping is pure overhead, and the gap grows with the per-node store count.

**Go beats C again (1.32×, vs 1.39× in kata 24)** — pure alloc-churn is Go's best case: bump-allocated nodes from a contiguous arena, batch GC reclaim of each iteration's 100 dead nodes, where C/Kāra/Rust pay a `malloc`/`free` pair per node. The flip side is the 9.6 MiB GC arena in the memory table below — Kāra holds C-level RSS at a C-adjacent pace.

> **Default (non-`KARAC_AUTO_PAR=0`) build:** karac's reduction-recognition auto-parallelizes the K-loop — 164.3 ± 24.6 ms wall / 2.52 s user on 18 cores, a **~5.3× wall win over seq** for a +262.8 KiB binary (295.8 KiB — the `karac_par_reduce` floor, same 302,856-byte binary as kata [#24](../24-swap-nodes-in-pairs/)'s default build). Per BENCH.md lane discipline the table above stays seq-lane; the par lane would need same-lane comparators (rayon / goroutine mirrors) before it can headline.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py iterative` (K=100k) | 1.106 ± 0.009 s |

Python at K=100k is 1.12 s; projecting to the compiled mirrors' K=500k (~5.6 s) puts it **~6.4× slower than kāra seq** — same neighborhood as kata 24's 5.9×, for the same reason: the workload is almost pure object allocation and pointer stores, both of which CPython does in C, so there's no arithmetic inner loop for the bytecode interpreter to lose on.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 iterative.c           | **45.7 ± 0.5 ms** |
| **karac build iterative.kara**  | **85.3 ± 0.7 ms** |
| rustc -O iterative.rs           | 121.5 ± 1.6 ms |

Kāra compiles **1.34× faster than `rustc -O`** and sits at **1.91× of clang -O3** — same shape as the rest of the corpus (kata 24: 1.27× / 1.84×).

### Binary size

| Implementation | Size |
|---|---|
| c    iterative                     | 32.7 KiB |
| **kāra iterative**                 | **33.1 KiB** |
| rust iterative                     | 456.1 KiB |
| go   iterative                     | 2434.2 KiB |

Kāra's seq binary is **32.9 KiB — 208 bytes off C's** (33,720 vs 33,512 B), byte-identical to kata [#24](../24-swap-nodes-in-pairs/)'s reading: a `shared struct` linked-list program stays at the C-mirror floor regardless of how much re-linking the loop does.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| **kāra iterative**                 | **1.2 MiB** |
| c    iterative                     | 1.1 MiB |
| rust iterative                     | 1.1 MiB |
| go   iterative                     | 9.6 MiB |

Kāra's single-shot reading (1,065,248 B) lands a page below C's (1,081,632 B) this batch — `/usr/bin/time -l` readings are page-level noisy, so the honest claim is parity. The per-iter list is allocated, group-reversed, and fully freed inside the loop; steady state stays flat across all 500,000 iterations — the same flat-RSS property the kata-24 fixes established, now under per-step alias churn. Go's 9.6 MiB is the GC arena that buys its wall-time lead above.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 iterative.c          | 2.5 MiB |
| **karac build iterative.kara** | **14.5 MiB** |
| rustc -O iterative.rs          | 31.4 MiB |

Kāra's compile-memory footprint is ~5× clang's and ~2.3× below rustc's — corpus shape. The reading is ~0.8 MiB above kata 24's same-shape workload (13.7 MiB): karac itself grew between the two measurements (this kata's interpreter fix links `stacker` into the compiler binary), consistent with the known fixed-floor compile-mem drift — the emitted binary is unaffected (see Binary size above).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil.
