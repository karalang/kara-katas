# 19. Remove Nth Node From End of List

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Linked List, Two Pointers &nbsp;·&nbsp; **Source:** [leetcode.com/problems/remove-nth-node-from-end-of-list](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)

Given the head of a singly linked list and an integer `n`, remove the `n`-th node counting from the **end** (1-indexed: `n == 1` is the tail) and return the head of the modified list.

```
([1, 2, 3, 4, 5], n=2)  → [1, 2, 3, 5]
([1],             n=1)  → []
([1, 2],          n=1)  → [1]
```

**Constraints:** `1 ≤ list length ≤ 30`, `0 ≤ Node.val ≤ 100`, `1 ≤ n ≤ length`. LeetCode's follow-up: do it in one pass.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| One-pass gap two-pointer: lead `fast` n nodes, then walk `fast`/`slow` in lockstep until `fast` falls off the end; splice `slow.next` | O(L) time, O(1) extra | [`remove_nth.kara`](remove_nth.kara) ✓ via `karac run` / `karac build` | [`remove_nth.py`](remove_nth.py) ✓ |

`✓` runs end-to-end today. Interpreter and codegen produce identical output to the Python mirror across all eight test cases.

## Why one-pass two-pointer (and the dummy)

The naive route is two passes: walk once to measure the length `L`, then walk again to the `(L - n)`-th node and splice. The follow-up asks for one pass — the **gap two-pointer**, the same fast/slow index-cursor idea as kata [#2](../2-add-two-numbers/)'s lockstep walk, but with a fixed *lead* between the cursors rather than stepping them together from the start:

1. Advance `fast` `n` nodes into the list from the head. There are now exactly `L - n` nodes still ahead of it.
2. Walk `fast` and `slow` in lockstep until `fast` runs off the end (`None`). `slow` starts at a **dummy** node placed before the head, so when `fast` is `None`, `slow` rests on the node *just before* the target.
3. Splice: `slow.next = slow.next.next`.

The **dummy node** is the load-bearing trick. Without it, deleting the head (`n == L`) is a special case needing its own branch; with a dummy sitting before the head, the node to remove is *always* `slow.next`, head or not, so the splice is uniform. This is the same role the dummy plays in kata [#2](../2-add-two-numbers/), where it anchors the output tail so the first real node isn't a special case.

`i64` is *not* load-bearing here — LeetCode bounds the list by 30 nodes and values by 100, so i32 would suffice; the width is chosen for uniformity with the rest of the corpus (contrast kata [#18](../18-4sum/), where the 10⁹ bound forces i64).

## Kāra features exercised

- **`shared struct ListNode { val: i64, mut next: Option[ListNode] }`** — the same reference-semantics (RC-backed) linked-node model kata [#2](../2-add-two-numbers/) introduced. `Option[shared Self]` `next` fields use karac's niche layout (a single nullable pointer, not a 4-i64 tagged enum).
- **In-place structural splice** — `slow.next = slow.next.next` re-points an existing `.next` to drop a mid-chain node. This is the first kata in the run to *splice* (kata 2 only appends), and it is the load-bearing operation: reassigning `slow.next` drops the spliced-out node's last reference, freeing it with no manual bookkeeping.
- **Cursor reassignment over a shared chain** — `let mut slow = dummy; … slow = snode;` re-points the cursor without copying nodes; `let mut fast = head;` and the `if let Some(node) = fast { fast = node.next; }` advance are the `Option[shared]` walk pattern.
- **`loop { match … }` + `if let` Option control flow** — the lockstep crawl uses `loop`/`match` on `fast`, and the lead/splice use `if let Some(_)`, exercising Option destructuring and reassignment across a `shared struct` chain.

> This kata drove a round of `karac` shared-struct refcount hardening: it is the first to splice a node out of a list *and* to return a chain that aliases its `head` parameter, which surfaced (and fixed) several RC inc/dec discipline bugs in codegen. Both `karac run` and `karac build` now produce identical, leak-free output.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   remove_nth.kara
karac build remove_nth.kara && ./remove_nth

# Python
python3 remove_nth.py

# Verify they agree
diff <(./remove_nth)              <(python3 remove_nth.py) && echo OK
diff <(karac run remove_nth.kara) <(python3 remove_nth.py) && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`remove_nth.{kara,rs,c,py}`, `go-seq/main.go`).

**Workload.** A fresh N = 100-node list (values `1..N`) is built every iteration — the removal mutates the chain in place, so each iter needs a fresh list — then one node is removed and the result head is read. K = 500,000 iterations. The removal position rotates `n = (k % N) + 1` over the full range `[1, N]`, so across any N consecutive iters every position is removed once — tail (`n=1`), head (`n=N`), and every interior node — which keeps the branch predictor from learning a single splice trajectory and exercises the dummy's head-removal path on 1/N of the iters. The sink is the running sum of the result head's value (1 on the iters that keep the head, 2 on the 1/N that remove it) = `(K − K/N)·1 + (K/N)·2` = **505,000**; all four compiled mirrors must agree before timing.

**Seq-only kata** (BENCH.md two-lane discipline): per-call work is a linear build + a single linear two-pointer pass — small enough that a parallel lane would mostly measure worker-pool dispatch, so this stays single-threaded and measures pure codegen quality, same call kata [#2](../2-add-two-numbers/) makes. The sink reads the result head under an `if let` guard, which keeps the K-loop off karac's auto-par-on-reduction allow-list, so the default `karac build` is single-threaded and directly comparable to `rustc -O` / `clang -O3` / `go build`.

This is the **alloc/splice/drop peer to kata 2's alloc-per-digit**: where kata 2 builds an output list per iter, this builds an input list per iter and splices one node out of it — the same RC-node allocator traffic, plus an in-place structural mutation.

### Runtime — seq lane

Snapshot — M5 Pro, 2026-06-05, hyperfine `--warmup 5 --runs 30 --shell=none`. All four single-threaded. This kata's bench is the longest sustained load in the 1–100 tranche (~2.4 s of CPU per iteration set), and back-to-back batches drift ±5% together thermally — three same-day runs put kāra at 533–576 ms with every comparator moving in step, while the *ratios* held to ±2% across all three. Quote the ratios, not the walls. (The 2026-05-30 snapshot read kāra 530.7 / c 509.2 — kāra reproduces to 0.5% on a cool run; the old C reading was ~1.1× of today's, consistent with that batch's documented load inflation on other katas.)

| Implementation | Wall time |
|---|---|
| go   remove_nth                    | 471.5 ± 14.7 ms |
| c    remove_nth (clang -O3)        | 503.2 ± 25.7 ms |
| **kāra remove_nth**                | **566.1 ± 20.0 ms** |
| rust remove_nth                    | 853.1 ± 12.3 ms |

**Kāra leads Rust by 1.51×** and trails C by ~1.12× and Go by ~1.20×. The headline number — the gap to Rust, Kāra's semantic peer — is wide because Rust's reference-semantics linked list is `Rc<RefCell<ListNode>>`, whose per-node `Rc` refcount + `RefCell` borrow-flag traffic is heavier than Kāra's plain RC header (this is the same effect kata 2 shows, where Rust's `Rc<RefCell<>>` is the slowest mirror). Against the manual-memory floor the order flips: this kata is allocator-bound (build + drop ~100 nodes per iter, plus the splice), and Kāra's per-node RC inc/dec bookkeeping sits just behind C's plain `malloc`/`free` (~1.12×) and Go's GC-managed pointer nodes (~1.20×) — there is no sort here for Kāra's inlined-comparator edge (kata 15/18) to show through, so on pure RC-node churn Kāra lands behind the no-refcount mirrors. The Rust gap is the load-bearing number and it is the widest in the corpus, driven by `Rc<RefCell>`.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py remove_nth` (K=100k) | 796.0 ± 4.8 ms |

Python at K=100k is 796 ms; projecting to the compiled mirrors' K=500k (~3.98 s) puts it **~7.0× slower than kāra seq** — the narrowest Python gap in the corpus, because this workload is dominated by allocation (which CPython does in C) and pointer-chasing rather than arithmetic the interpreter would run bytecode-by-bytecode.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 remove_nth.c           | **43.9 ± 1.2 ms** |
| **karac build remove_nth.kara**  | **75.0 ± 2.7 ms** |
| rustc -O remove_nth.rs           | 98.3 ± 1.8 ms |

Kāra compiles **1.31× faster than `rustc -O`** and sits at **1.71× of clang -O3** — same shape as the rest of the corpus. (05-30 read 67.6 for karac; the corpus-wide karac compile band has sat at ~75–85 ms in the 06-05 sweep — single-digit-ms drift on an identical compiler binary, environmental.)

### Binary size

| Implementation | Size |
|---|---|
| c    remove_nth                    | 32.7 KiB |
| **kāra remove_nth**                | **32.8 KiB** |
| rust remove_nth                    | 456.1 KiB |
| go   remove_nth                    | 2434.1 KiB |

Kāra's seq binary is **32.8 KiB — essentially identical to C's 32.7 KiB**, and far below Rust's 456 KiB. This kata calls no `sort_by` and triggers no auto-par dispatch, so it never links the runtime's libstd floor (panic infrastructure + DWARF symbolizer) that dominates the sort-using katas (15 / 16 / 18, ~295 KiB) — see [kata 16 § Binary size](../16-3sum-closest/README.md) for that breakdown. With no sort, a `shared struct` linked-list program is as small as the C mirror.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    remove_nth                    | 1.0 MiB |
| **kāra remove_nth**                | **1.1 MiB** |
| rust remove_nth                    | 1.1 MiB |
| go   remove_nth                    | 9.5 MiB |

Kāra's peak RSS (1,130,784 B) sits two pages above C (1,098,016 B) and one below Rust (1,147,168 B) — the per-iter list is allocated, spliced, and fully freed inside the loop, so steady state stays flat across all 500,000 iterations with no growth. (The trio shifted down ~48 KiB vs the 05-30 readings — the same environment-wide dyld/OS page shift seen across the #12–#18 re-benches; byte-level ordering within the trio is page noise.) Go's 9.5 MiB carries its GC arena + scheduler. (Reaching flat RSS here required fixing a `shared struct` refcount leak in karac's codegen that this kata surfaced — see the note under § Kāra features.)

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 remove_nth.c          | 2.5 MiB |
| **karac build remove_nth.kara** | **10.3 MiB** |
| rustc -O remove_nth.rs          | 30.4 MiB |

Kāra's compile-memory footprint is ~4× clang's and ~3× lower than rustc's on this kata — same shape as the rest of the corpus. (Flat vs the 05-30 reading.)

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil. On this allocator-bound linked-list kata **Kāra leads Rust by ~1.5×** — the widest Rust gap in the corpus, and the same cause kata 2 identifies: a reference-semantics linked list is `Rc<RefCell<>>` in Rust, whose per-node refcount + borrow-flag overhead is heavier than Kāra's RC header. Against the no-refcount mirrors (C, Go) Kāra trails (~1.12× / ~1.20×) because pure RC-node churn — with no sort to amortize — is the whole workload. The Rust gap is the load-bearing number.
