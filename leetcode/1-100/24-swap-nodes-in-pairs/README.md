# 24. Swap Nodes in Pairs

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Linked List, Recursion &nbsp;·&nbsp; **Source:** [leetcode.com/problems/swap-nodes-in-pairs](https://leetcode.com/problems/swap-nodes-in-pairs/)

Given the head of a singly linked list, swap every two adjacent nodes and return the new head. The problem requires swapping the **nodes themselves**, not their values — a structural re-link, with a trailing singleton left in place on odd-length input.

```
[1, 2, 3, 4]  → [2, 1, 4, 3]
[]            → []
[1]           → [1]
[1, 2, 3]     → [2, 1, 3]
```

**Constraints:** `0 ≤ list length ≤ 100`, `0 ≤ Node.val ≤ 100`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Iterative dummy-anchored pair re-link: walk a `prev` cursor; re-link each `first → second` pair to `second → first` via three pointer stores | O(n) time, O(1) extra | [`iterative.kara`](iterative.kara) ✓ via `karac run` / `karac build` | [`iterative.py`](iterative.py) ✓ |
| Recursive two-at-a-time: `swap(first → second → rest) = second → first → swap(rest)` | O(n) time, O(n/2) stack | [`recursive.kara`](recursive.kara) ✓ via `karac run` / `karac build` | [`recursive.py`](recursive.py) ✓ |

`✓` runs end-to-end today. Both forms produce identical output under the interpreter and codegen across all nine test cases; the **iterative** form is the benchmarked one.

## Why iterative (and the three-store dance)

Where kata [#19](../19-remove-nth-node-from-end-of-list/) splices a node *out* and kata [#21](../21-merge-two-sorted-lists/) splices nodes *in* from two sources, this kata **re-orders nodes in place** — the first kata in the run whose re-link removes a node from the chain while a local still points at it. Each pair swap is three stores, in an order that never strands a node:

```
prev → first → second → rest      becomes      prev → second → first → rest

  1. first.next  = second.next   — `first` adopts the rest of the list.
  2. second.next = Some(first)   — `second` points back at `first`.
  3. prev.next   = Some(second)  — the pair is grafted in swapped order.
```

then `prev = first` (the back node of the swapped pair) anchors the next pair. Store 1 drops the chain's reference to `second` — between stores 1 and 3 that node is held **only** by the `if let` binding, which is exactly the shape that found this kata's compiler bug (below).

The **dummy node** is the same load-bearing trick as katas [#2](../2-add-two-numbers/), [#19](../19-remove-nth-node-from-end-of-list/) and [#21](../21-merge-two-sorted-lists/): a throwaway node before the head makes the first pair's graft uniform with every later pair, so swapping the head needs no special case and the new head falls out as `dummy.next`.

`i64` is *not* load-bearing — LeetCode bounds the list at 100 nodes and values to `[0, 100]`; the width is for uniformity with the rest of the corpus (contrast kata [#18](../18-4sum/), where the 10⁹ bound forces `i64`).

Kata [#25](../25-reverse-nodes-in-k-group/) generalizes this swap to arbitrary group size — at k = 2 its group reversal degenerates to exactly this three-store dance, and its trailing partial group generalizes the odd-length singleton.

## Kāra features exercised

- **`shared struct ListNode { val: i64, mut next: Option[ListNode] }`** — the same reference-semantics (RC-backed) linked-node model as katas 2/19/21/23, with niche `Option[shared]` layout (a single nullable pointer).
- **Pattern-bound aliases under displacement** — `if let Some(second) = first.next` binds an alias whose *source field is overwritten* one line later. Kata 21's cursors walk lists destructively but never invalidate a live binding; this kata does, on every pair.
- **In-place pair re-link from one source** — three field stores re-parent two existing nodes with no allocation; the suffix (`second.next`) grafts in one move.
- **`break` out of nested `if let` arms with live bindings** — both loop exits leave the arm while `first` (and its scope-exit refcount release) is in flight.
- **Bounded non-tail recursion (`recursive.kara`)** — one frame per *pair* (depth ≤ 50 at the 100-node bound), mixing `Some(<alias>)` returns (constructor retains) with bare-param returns (per-branch compensation) — the same two return flavors kata [#21](../21-merge-two-sorted-lists/)'s per-branch fix covers. Same TCO caveat as kata 21 (kara `docs/deferred.md § Tail-Call Optimization`).

> **This kata found two `karac` codegen bugs — both fixed on the spot (karac `cb33da55`).** Both forms were interpreter-clean and codegen-crashing (SIGSEGV/SIGBUS or garbage, scattering by allocator luck). (1) **`if let` shared pattern bindings were non-retained aliases**: the binding's payload pointer carried no refcount, so store 1 of the re-link (`first.next = second.next`) freed `second`'s node *under the live binding* — the one alias shape the June 2026 refcount-soundness overhaul (unwrap receive-inc, field-let alias acquire, let-path receive-inc) hadn't covered, because no earlier kata displaces a node while a pattern binding aliases it. Pattern bindings now take the same alias acquire as field-lets, exempting the analyzer's count-free walk families so read-only walks (katas 2/19/21) stay elided. (2) **`break`/`continue` skipped cleanup-frame drains**: early loop exits branched straight out, skipping every scope-exit release (and `defer`) registered between the jump and the loop boundary — a *pre-existing* leak gap (`return` was the only early exit with a parity drain) that fix 1 made observable in this kata's `break`-from-`if let` shape. Both forms are now `karac build`-correct and leak-free — a 500k-iteration × 100-node swap stress holds flat RSS (~1.0 MiB). See the compiler's `docs/implementation_checklist/phase-7-codegen.md` kata-24 entry.

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

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`iterative.{kara,rs,c,py}`, `go-seq/main.go`). Figures below are the 2026-10-31 re-bench (results.json `measured_at` 2026-11-01T01:39Z), measured with **karac 0.9.0-dev.14057+g6697158fa** — the v2/MIR backend (the legacy backend was deleted 2026-10-23).

**Workload.** A fresh N = 100-node list (`[1, 2, …, 100]`) is built every iteration — the swap consumes and re-links it, so each iter needs fresh input — then every adjacent pair is swapped in place and the list summed. K = 500,000 iterations. The swap moves no values, so the per-iter sum is the invariant `N·(N+1)/2 = 5050` and the sink is `K·5050 =` **2,525,000,000** — a swap that drops or duplicates a node breaks the sink, which all four compiled mirrors must agree on before timing.

**Seq lane** (BENCH.md two-lane discipline): per-call work is a linear build + a linear pair re-link + a linear sum — the kāra binary is built with `KARAC_AUTO_PAR=0` (dual-binary seq pattern) so the K-loop reduction stays single-threaded and directly comparable to `rustc -O` / `clang -O3` / `go build`. (The default build auto-parallelized the K-loop legitimately as of 2026-06-07 — see the note below the table.)

This is the **alloc/re-link/drop sibling of kata 19 (splice-out) and kata 21 (two-source splice-in)**: one list per iter instead of kata 21's two, and the re-link touches *every* node instead of removing one. Note these numbers **already include** the pattern-binding alias acquire this kata forced into karac — there is no pre-fix baseline, because pre-fix the program segfaults; the soundness cost is priced in.

### Runtime — seq lane

M5 Pro, 2026-10-31, karac g6697158fa (v2/MIR), `bench.sh` (hyperfine `--warmup 5 --runs 30 --shell=none`, structured-JSON emit). All single-threaded.

| Implementation | Wall time | vs Kāra |
|---|---|---|
| go   iterative                     | 0.589 ± 0.006 s | 0.64× |
| c    iterative (clang -O3)         | 0.790 ± 0.035 s | 0.85× |
| **kāra iterative**                 | **0.927 ± 0.036 s** | **1.00×** |
| rust iterative                     | 1.073 ± 0.031 s | 1.16× |
| rust iterative (`-C overflow-checks=on`) | 1.102 ± 0.058 s | 1.19× |

**Kāra leads Rust by 1.16×** (1.19× against Rust with overflow checks on) and trails C by 1.17× and Go by 1.57×. Same causes as katas [#19](../19-remove-nth-node-from-end-of-list/)/[#21](../21-merge-two-sorted-lists/): Rust's reference-semantics list is `Rc<RefCell<ListNode>>`, whose per-node `Rc` + `RefCell` borrow-flag traffic — paid on every one of the three re-link stores per pair — is heavier than Kāra's plain RC header; against the manual-memory floor the order flips because the workload is allocator-bound (build + drop 100 nodes per iter) and Kāra's RC bookkeeping sits behind C's bare `malloc`/`free`.

**MIR vs the previous feed (legacy karac 0.1.0, 2026-07-28), in language ratios:** Kāra/Rust 0.83× → 0.86×, Kāra/C 1.14× → 1.17×, Kāra/Go 1.74× → 1.57× — flat (each move under 10%).

**Go beats C here (1.34×)** — the most pronounced Go lead in the linked-list set (kata 21 reads Go 1.28× over C in the same session). Pure alloc-churn is Go's best case: its bump allocator hands out nodes from a contiguous arena and the GC reclaims each iteration's 100 dead nodes in batch, where C (and Kāra, and Rust) pay a `malloc`/`free` pair per node. The flip side is the 10.4 MiB GC arena in the memory table below — Kāra holds C-level RSS.

> **Default (non-`KARAC_AUTO_PAR=0`) build (2026-06-07 legacy build, not re-measured on MIR):** karac's reduction-recognition auto-parallelizes the K-loop — 155.0 ± 26.2 ms wall / 2.20 s user on 18 cores, a **~5.3× wall win over seq** for a +262.8 KiB binary (295.8 KiB — 302,856 B, the `karac_par_reduce` floor; an earlier revision of this line divided by 1000 and read "302.9 KiB" — see [kata 16 § Binary size](../16-3sum-closest/README.md)). Per BENCH.md lane discipline the table above stays seq-lane; the par lane would need same-lane comparators (rayon / goroutine mirrors) before it can headline.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py iterative` (K=100k) — last measured 2026-07-28, not re-run | 0.944 ± 0.008 s |

Not re-run on 2026-10-31 (the bench did not set `KARA_BENCH_INCLUDE_PY`). Python at K=100k read 0.94 s in the 2026-07-28 feed; projecting to the compiled mirrors' K=500k (~4.72 s) put it **~5.5× slower than that feed's kāra seq** (0.863 s; a cross-session projection, not re-derived against the current feed) — the narrowest Python gap in the linked-list set (kata 19/21 read ~10×), because the workload is almost pure object allocation and pointer stores, both of which CPython does in C; there is no arithmetic inner loop for the bytecode interpreter to lose on.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 iterative.c           | **46.7 ± 0.8 ms** |
| rustc -O iterative.rs           | 105.7 ± 1.1 ms |
| **karac build iterative.kara**  | **130.4 ± 1.1 ms** |

On the MIR backend karac compiles **1.23× slower than `rustc -O`** and sits at **2.79× of clang -O3** (kata 21: 1.17× / 2.85×). The 2026-06-07 legacy build was 1.27× faster than rustc (79.9 ms vs 110.2 ms).

### Binary size

| Implementation | Size |
|---|---|
| c    iterative                     | 32.7 KiB |
| **kāra iterative**                 | **295.8 KiB** |
| rust iterative                     | 456.1 KiB |
| go   iterative                     | 2434.1 KiB |

Every MIR Kāra binary is ~300–390 KB where the legacy backend's were ~34 KB (kara ledger [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md)); this one is **295.8 KiB** (302,872 B, was 34,136 B in the 2026-07-28 feed), 1.54× under Rust's 456.1 KiB and 9.0× over C's 32.7 KiB. Go's ~2.4 MiB is the Go runtime + GC.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    iterative                     | 1.05 MiB |
| **kāra iterative**                 | **1.08 MiB** |
| rust iterative                     | 1.09 MiB |
| go   iterative                     | 10.4 MiB |

Kāra's peak RSS sits **at C's level** — 1,130,832 vs 1,098,040 B in the 2026-10-31 run, two 16 KiB pages apart (single-shot `/usr/bin/time -l` readings, page-level noisy, so the honest claim is parity within a couple of pages). The per-iter list is allocated, re-linked, and fully freed inside the loop; steady state stays flat across all 500,000 iterations — the flat-RSS property is exactly what the `break`-drain fix this kata drove is about. Go's 10.4 MiB is the GC arena that buys its wall-time lead above.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 iterative.c          | 2.6 MiB |
| rustc -O iterative.rs          | 29.9 MiB |
| **karac build iterative.kara** | **58.8 MiB** |

On the MIR backend karac's compile-memory peak is **2.0× rustc's** and ~23× clang's (the 2026-06-07 legacy build peaked at 13.7 MiB, ~2.2× below rustc).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil. On this allocator-bound re-link kata **Kāra leads Rust by 1.16×** — the `Rc<RefCell>` tax is at its most visible when every pair costs three refcounted pointer stores — while holding C-level RSS; Go's GC buys a 1.57× wall lead over Kāra at 9.7× the memory.
