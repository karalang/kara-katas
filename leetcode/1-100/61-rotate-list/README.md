# 61. Rotate List

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Linked List · Two Pointers &nbsp;·&nbsp; **Source:** [leetcode.com/problems/rotate-list](https://leetcode.com/problems/rotate-list/)

Given the head of a singly linked list, rotate it to the **right** by `k` places — the last `k` nodes wrap around to the front, keeping their order.

```
[1, 2, 3, 4, 5], k = 2   →   [4, 5, 1, 2, 3]   (the tail pair 4,5 moves to the head)
[0, 1, 2],       k = 4   →   [2, 0, 1]         (4 % 3 == 1, so one place)
```

**Constraints:** `0 ≤ list length ≤ 500`; `-100 ≤ Node.val ≤ 100`; `0 ≤ k ≤ 2·10⁹`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Close the ring, then cut** — join `tail → head` into a ring, walk `L - k%L - 1` steps to the new tail, sever right after it | O(L) time, O(1) space | [`rotate_list.kara`](rotate_list.kara) ✓ via `karac run` / `karac build` | [`rotate_list.py`](rotate_list.py) ✓ |
| **Two-segment splice** — cut into front/back segments first, then re-join front behind back with `tail.next = head` | O(L) time, O(1) space | [`rotate_list_splice.kara`](rotate_list_splice.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output across all ten test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other and with the Python mirror.

## Why reduce `k` first, and why a ring?

Two observations do all the work:

1. **`k` and `k % L` land on the same list.** `L` rotations return a list of length `L` to itself, so only `k mod L` matters. LeetCode lets `k` reach **2·10⁹** against a list of at most 500 nodes — the naive "shift one node, `k` times" loop would spin two billion times for a list you could rotate in ≤ 500 steps. Reducing modulo `L` is not an optimization here, it is what makes the problem O(L). Case 8 (`[1,2,3]`, `k = 2·10⁹`) is the one that would hang without it.
2. **After reduction, the new head is the node at index `L - k%L`.** Its predecessor, index `L - k%L - 1`, is the new tail.

**Close the ring** ([`rotate_list.kara`](rotate_list.kara)) realizes the cut with the fewest branches: point the old tail back at the old head to form a cycle, walk `L - s - 1` steps (`s = k % L`) to the new tail, then `result = new_tail.next; new_tail.next = None`. Whether the split lands deep in the list or right at the head, the cut is the same two lines — the same "spend one structural move to erase the special cases" idea as the dummy node in kata [#19](../19-remove-nth-node-from-end-of-list/). The transient cycle is severed before returning, and every node stays reachable from the result, so nothing leaks or is freed early.

**Two-segment splice** ([`rotate_list_splice.kara`](rotate_list_splice.kara)) makes the cut *first* — splitting `[.. new_tail]` from `[new_head .. tail]` — then stitches the front segment behind the back with `tail.next = head`. Because `s` is in `1 .. L-1` once the no-op case is handled, the new tail is strictly before the old tail, so the two field writes never touch the same node. It is the same arithmetic and the same early return, expressed as two independent splices instead of ring-plus-cut — a useful independent cross-check that the modulo/index math, not the ring trick, is what's correct.

Both share the ownership discipline the linked-list corpus turns on: **read before you null.** `result = new_tail.next` (or `new_head = nt.next`) retains the back segment into a local *before* `new_tail.next = None` clears that edge, so nulling the field never frees the node the local now names. `tail.next = head` then stores an *alias* — the same retain-on-store flavor as kata [#24](../24-swap-nodes-in-pairs/)'s `second.next = Some(first)`.

## Kāra features exercised

- **`shared struct ListNode { val, mut next: Option[ListNode] }`** — the corpus's Rc-like linked-node model from kata [#2](../2-add-two-numbers/): reassigning a cursor (`cur = node.next`) re-points without copying, and a field store through the shared reference (`tail.next = head`, `nt.next = None`) mutates the graph in place. Reassigning a `next` drops the previous edge's reference automatically.
- **Transient reference cycle, then severed** — `tail.next = head` deliberately forms a ring, which is broken again by `new_tail.next = None` before the function returns; the result chain keeps every node reachable, so the Rc refcounts settle with no leak and no early free. This is the sharpest ownership case in the kata — read-into-a-local before the cut is what keeps the retained node alive.
- **`Option[ListNode]` cursor walk via `match` / `if let Some(node) = …`** — the measure loop (`match cur { Some(node) => { … cur = node.next; } None => break }`) and the fixed-step advance (`while i < steps { if let Some(node) = new_tail { new_tail = node.next; } }`) are the same cursor idioms as katas [#19](../19-remove-nth-node-from-end-of-list/) and [#24](../24-swap-nodes-in-pairs/).
- **`k % len` modular reduction** — the whole reason the 2·10⁹ bound is harmless; `%` on `i64`, reduced once against the measured length.
- **`Slice[i64]` param + `Array[i64, N]` literals** — `from_array(arr: Slice[i64])` fed by sized array literals (including the empty `Array[i64, 0] = []`), same harness shape as the other list katas.

**v1 note.** `k` reaches 2·10⁹, which still fits `i32` (max 2.147·10⁹); the arithmetic is `i64` for uniformity with the rest of the corpus, not because the width is forced. The load-bearing part is the modulo, not the range — contrast kata [#18](../18-4sum/), where the 10⁹ *sum* bound genuinely requires `i64`.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   rotate_list.kara
karac build rotate_list.kara && ./rotate_list

# The alternative approach (identical output):
karac run rotate_list_splice.kara

# Python
python3 rotate_list.py

# Verify they all agree
diff <(karac run rotate_list.kara) <(python3 rotate_list.py)                  && echo OK
diff <(karac run rotate_list.kara) <(karac run rotate_list_splice.kara)       && echo OK
diff <(karac run rotate_list.kara) <(./rotate_list)                           && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`rotate_list.{kara,rs,c,py}`, `go-seq/main.go`).

**Workload.** A fresh N = 100-node list (values `1..N`) is built every iteration — the rotation re-links the chain in place, so each iter needs a fresh list — then it is rotated right and the result head is read. K = 500,000 iterations. The rotation amount sweeps `r = k % 2N` over `0..2N-1`, so **half the iters have `r ≥ N` and fire a real `k % L` reduction** (the modulo path this kata turns on) while `r` still visits every distinct final rotation, keeping the branch predictor off a single cut trajectory. The sink is the running sum of the result head's value — rotating `[1..N]` right by `s = r % N` puts value `101 − s` at the head (`1` when `s == 0`), summing to a fixed `(K / 2N)·N(N+1)` = **25,250,000**; all four compiled mirrors must agree before timing.

**Seq-only kata** (BENCH.md two-lane discipline): per-call work is a linear build + a linear measure/walk + an in-place re-link — small enough that a parallel lane would mostly measure worker-pool dispatch, so this stays single-threaded and measures pure codegen quality, the same call kata [#19](../19-remove-nth-node-from-end-of-list/) makes. The sink reads the result head under an `if let` guard, which was meant to keep the K-loop off karac's auto-par-on-reduction allow-list — but current karac parallelises it anyway (verified in the emitted IR, `KARAC_MIR_LL`: the default build carries a call of `karac_mir_task_spawn`, the `KARAC_AUTO_PAR=0` build does not), so the bench builds the kāra row with `KARAC_AUTO_PAR=0`, single-threaded and directly comparable to `rustc -O` / `clang -O3` / `go build`.

This is the **structural-mutation peer to kata [#19](../19-remove-nth-node-from-end-of-list/)**: where #19 builds an input list per iter and splices one node *out*, this builds one and *re-links* it (close the ring, walk, cut) — the same per-node RC allocator traffic, plus an in-place pointer rewrite instead of a deletion.

### Runtime — seq lane

Measured 2026-10-31 (`measured_at` 2026-11-01T02:22Z) — Apple M5 Pro (6P+12E), Darwin 25.6.0, hyperfine, 30 runs, karac `g6697158fa` (0.9.0-dev.14057, v2/MIR backend), kāra built `KARAC_AUTO_PAR=0`. All single-threaded (kāra CPU 99.9%). Numbers from the committed [`results.json`](bench/results.json) unless marked otherwise.

| Implementation | Wall time |
|---|---|
| go   rotate_list                   | 529.3 ± 8.7 ms |
| c    rotate_list (clang -O3)       | 677.7 ± 13.4 ms |
| **kāra rotate_list**               | **820.8 ± 13.4 ms** |
| rust rotate_list                   | 1114.8 ± 28.5 ms |
| rust rotate_list (`overflow-checks=on`) | 1118.2 ± 26.2 ms |

**Kāra leads Rust by 1.36×** (Kāra/Rust 0.74×) and trails C by ~1.21× and Go by ~1.55× — the same profile as its sibling linked-list kata [#19](../19-remove-nth-node-from-end-of-list/) (there, at the 2026-07-04 snapshot: Rust +1.29×, C −1.27×, Go −1.54×). Against the previous run (2026-07-28, legacy backend) the ratios are flat to Rust and C (Kāra/Rust 0.76× → 0.74×, Kāra/C 1.24× → 1.21×) and better against Go (1.89× → 1.55×), mostly because Go itself ran slower this session. The headline gap to Rust, Kāra's semantic peer, is wide because Rust's reference-semantics linked list is `Rc<RefCell<ListNode>>`, whose per-node refcount + `RefCell` borrow-flag traffic is heavier than Kāra's plain RC header. Against the no-refcount mirrors the order flips: this kata is allocator-bound (build + drop ~100 nodes per iter, plus the re-link), and Kāra's per-node RC inc/dec bookkeeping sits behind C's plain `malloc`/`free` (~1.21×) and Go's GC-managed pointer nodes (~1.55×) — there is no sort here for Kāra's inlined-comparator edge (kata 15/18) to show through, so on pure RC-node churn Kāra lands behind the no-refcount mirrors. The Rust gap is the load-bearing number.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py rotate_list` (K=100k) | 886.4 ± 30.9 ms (last measured 2026-07-04, not re-run) |

Python at K=100k was 886 ms; projecting to the compiled mirrors' K=500k (~4.43 s) puts it **~5.4× slower than this run's kāra seq** (a cross-session ratio) — a narrow Python gap (cf. #19's ~7.0×), because this workload is dominated by allocation (which CPython does in C) and pointer-chasing rather than arithmetic the interpreter would run bytecode-by-bytecode.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 rotate_list.c           | **48.2 ± 0.8 ms** |
| rustc -O rotate_list.rs           | 110.4 ± 2.4 ms |
| **karac build rotate_list.kara**  | **137.6 ± 3.2 ms** |

Kāra compiles at **2.85× clang -O3** and **1.25× slower than `rustc -O`** on this kata — the bands no longer overlap (the 2026-07-04 snapshot had the two level within rustc's ±17.7 ms noise). Compile favouring rustc is the corpus-wide MIR-backend pattern (tracked as [`B-2026-10-31-41`](../../../../kara/docs/bugs-v2.md)).

### Binary size

| Implementation | Size |
|---|---|
| c    rotate_list                   | 32.7 KiB |
| **kāra rotate_list**               | **295.8 KiB** |
| rust rotate_list                   | 456.1 KiB |
| go   rotate_list                   | 2434.2 KiB |

Kāra's seq binary is **295.8 KiB** — 1.5× under Rust's 456.1 KiB but 9× C's 32.7 KiB; every MIR-backend Kāra binary is ~300–390 KB where the legacy backend's were ~34 KB (tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md)). Under the legacy backend this binary was 33.1 KiB, essentially C's size: the kata calls no `sort_by`, so it never linked the runtime's libstd floor (panic infrastructure + DWARF symbolizer) that dominates the sort-using katas — see [kata 16 § Binary size](../16-3sum-closest/README.md).

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    rotate_list                   | 1.03 MiB |
| rust rotate_list                   | 1.06 MiB |
| **kāra rotate_list**               | **1.06 MiB** |
| go   rotate_list                   | 10.1 MiB |

Kāra's peak RSS (1,114,448 B) ties Rust's (1,114,424 B, 24 bytes apart) and sits two 16 KiB pages above C's (1,081,656 B); the 2026-07-04 snapshot had Kāra lowest of the three. The per-iter list is allocated, rotated, and fully freed inside the loop, so steady state stays flat across all 500,000 iterations with no growth — direct evidence that the transient ring (`tail.next = head`) leaves **no surviving reference cycle** once `new_tail.next = None` severs it, so the Rc refcounts settle to zero every iteration. A cycle-leak would show as unbounded RSS growth here; it does not. Go's 10.1 MiB carries its GC arena + scheduler.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 rotate_list.c          | 2.6 MiB |
| rustc -O rotate_list.rs          | 30.3 MiB |
| **karac build rotate_list.kara** | **60.2 MiB** |

Kāra's compile-memory footprint is ~23× clang's and ~2.0× rustc's on this kata (the 2026-07-04 snapshot had it ~1.5× *under* rustc).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil. On this allocator-bound linked-list kata **Kāra leads Rust by ~1.36×** — the same cause kata [#19](../19-remove-nth-node-from-end-of-list/) identifies: a reference-semantics linked list is `Rc<RefCell<>>` in Rust, whose per-node refcount + borrow-flag overhead is heavier than Kāra's RC header. Against the no-refcount mirrors (C, Go) Kāra trails (~1.21× / ~1.55×) because pure RC-node churn — with no sort to amortize — is the whole workload. The Rust gap is the load-bearing number.
