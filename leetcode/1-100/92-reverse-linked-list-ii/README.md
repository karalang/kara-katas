# 92. Reverse Linked List II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Linked List &nbsp;·&nbsp; **Source:** [leetcode.com/problems/reverse-linked-list-ii](https://leetcode.com/problems/reverse-linked-list-ii/)

Given the head of a singly linked list and two **1-indexed** positions `left ≤ right`, reverse the nodes from position `left` to `right` (inclusive) and return the head. Do it in **one pass**.

```
1 → 2 → 3 → 4 → 5,  left = 2, right = 4   ->   1 → 4 → 3 → 2 → 5
5,                  left = 1, right = 1   ->   5
```

**Constraints:** `1 ≤ nodes ≤ 500`; `-500 ≤ Node.val ≤ 500`; `1 ≤ left ≤ right ≤ nodes`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **One-pass head insertion** ★ | [`reverse_between.kara`](reverse_between.kara) ✓ via `karac run` / `karac build` | [`reverse_between.py`](reverse_between.py) ✓ |
| **Three-pointer reversal, then reconnect** | [`reverse_between_threeptr.kara`](reverse_between_threeptr.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output across all nine test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other, with the Python mirror, **and with a slice-reversal ground truth** (`nums[:l-1] + nums[l-1:r][::-1] + nums[r:]`).

## Two ways to reverse a sublist

Both solvers use Kāra's reference-semantics node — a `shared struct` (Rc-like handle), the model of katas [#82](../82-remove-duplicates-from-sorted-list-ii/)/[#83](../83-remove-duplicates-from-sorted-list/)/[#86](../86-partition-list/):

```
shared struct ListNode { val: i64, mut next: Option[ListNode] }
```

A dummy before the head means `left == 1` needs no special case. Both start by walking a `prev` cursor to the node **just before** position `left`; `cur = prev.next` is the section's first node (which becomes its last).

**One-pass head insertion** ([`reverse_between.kara`](reverse_between.kara), the ★) then repeatedly lifts the node right after `cur` and splices it to the **front** of the section (just after `prev`), `right - left` times:

```
nxt = cur.next
cur.next = nxt.next        # cut nxt out
nxt.next = prev.next       # nxt jumps to the front of the reversed part
prev.next = nxt
```

`cur` never moves — it drifts to the section's tail as everything after it gets pulled to the front. One pass, O(1) extra.

**Three-pointer reversal, then reconnect** ([`reverse_between_threeptr.kara`](reverse_between_threeptr.kara)) does it in two clear phases: run the classic `prev`/`cur`/`next` list reversal over exactly `right - left + 1` nodes (flipping each `node.next` backward), then stitch the two seams — `prev.next` to the section's new head (`pr`, the old `right` node) and `cur.next` to the continuation (`c`, the node that followed `right`). A distinct surface — an explicit reversal loop over `Option[ListNode]` with a `pr`/`c` pointer pair — that must land byte-identical to the head-insertion ★.

## Kāra features exercised

- **`shared struct` (Rc) sublist re-linking** — the ★'s three-line head-insertion splice and the variant's `node.next = pr` reversal both re-link by aliasing the Rc handle, no copying; RC / ownership machinery under real pointer-mutation load, verified byte-identical under codegen *and* auto-par.
- **`Option` pattern matching for pointer moves** — `match prev.next { Some(n) => … }` walks the cursor, and the ★'s `match cur.next { Some(nxt) => … }` drives the splice; the variant's `match c { Some(node) => … None => break }` is the reversal loop.
- **`Option[ListNode]` `pr`/`c` pointer pair** — the three-pointer variant threads two `Option[ListNode]` handles through the reversal and rebinds them each step.
- **Cursor that stays put while the list mutates around it** — the ★'s `cur` is fixed while `prev.next` is re-pointed repeatedly, the shared semantics letting the alias and the re-link coexist.

**v1 note.** Lists are short (`≤ 500` nodes) and values fit i64; the per-case sink folds each result's length and values into a running polynomial hash. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`, and both match the slice-reversal ground truth on every case. (The three-pointer variant compiles with one `note`-level RC-fallback on the reversal pointer juggling — the compiler working as designed, not an error.)

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   reverse_between.kara
karac build reverse_between.kara && ./reverse_between

# The three-pointer variant (identical output):
karac run reverse_between_threeptr.kara

# Python
python3 reverse_between.py

# Verify they all agree
diff <(karac run reverse_between.kara) <(python3 reverse_between.py)                  && echo OK
diff <(karac run reverse_between.kara) <(karac run reverse_between_threeptr.kara)     && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`reverse_between.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** Canonical numbers measured on the corpus's **Apple M5 Pro** (6P+12E, Darwin 25.5.0; `karac 0.1.0`, `rustc 1.95.0`, Apple clang 21.0.0, `go 1.26.3`, hyperfine 1.20) — [`bench/results.json`](bench/results.json). A shared x86-64 Linux cloud-container reference run is kept alongside in [`bench/results.container-x86.json`](bench/results.container-x86.json); absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. The cross-language *ordering* itself differs between the two — see the note below the table.

**Workload.** The reverse mutates/re-links the list, so — like kata [#82](../82-remove-duplicates-from-sorted-list-ii/)/[#83](../83-remove-duplicates-from-sorted-list/)/[#86](../86-partition-list/) — each iteration builds a **fresh M = 200-node** list and reverses a **~100-node window** whose start shifts per iteration (`left = 1 + iter%50`, `right = left+100`, so no call hoists). For **K = 178,000** iterations (seeded by the loop index) it builds, reverses, and folds the result through a **rolling polynomial hash**. Per-iteration node allocation is part of the measured work — fair, since every mirror allocates its nodes — alongside the RC-node pointer-chase reversal. All five compiled mirrors must agree on `147795689` before timing.

**Equal data structure.** Kāra uses a `shared struct` (Rc-like) list; **Rust mirrors it with `Rc<RefCell<ListNode>>`** (same per-node reference-count overhead), Go uses a GC-managed `*ListNode`, and **C a plain `malloc`/`free` raw-pointer list** (single-owner, the metal floor).

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded (the loop-carried sum is not a reduction the auto-par pass can split; the default build is verified equal to `KARAC_AUTO_PAR=0`). **Apple M5 Pro numbers.**

| Implementation | Wall time |
|---|---|
| c    reverse_between (clang -O3, malloc list)          | 453.3 ± 12.7 ms |
| go   reverse_between (`*Node`, GC)                     | 458.5 ± 5.5 ms |
| **kāra reverse_between**                               | **637.5 ± 17.0 ms** |
| rust reverse_between (rustc -O)                        | 677.8 ± 15.1 ms |
| rust reverse_between (rustc -O, overflow-checks=on)    | 684.8 ± 10.7 ms |

**The headline holds: at matched reference semantics kāra beats both Rust builds** — `shared struct` vs `Rc<RefCell<ListNode>>`, kāra ~1.06–1.07× faster (the `RefCell` borrow-flag check on every node access is the gap, the same pattern as [#82](../82-remove-duplicates-from-sorted-list-ii/)/[#83](../83-remove-duplicates-from-sorted-list/)/[#86](../86-partition-list/)). Raw-pointer C is the floor at ~1.41× under kāra.

**What changed from the container:** Go — the *slowest* mirror on the shared x86 container (1155 ms, last place) — is nearly tied with C on the M5, landing kāra in **3rd** here rather than 2nd. This is the alloc-bound container→M5 inversion: each iteration allocates a fresh 200-node list, and Go's GC allocator runs far better on fast native cores than on the noisy shared container (its 107 % CPU is a sliver of concurrent-GC help, not a multicore-wall-clock artifact — it wins on total CPU too, 491 vs kāra's 636 ms). But the trade is memory: kāra holds **1.0 MiB** peak RSS and a **33.9 KiB** binary against Go's **9.2 MiB** and **2.43 MiB** — ~9× less RSS and a ~74× smaller binary for a 1.39× wall-time gap. Python (K=6000, a fraction of the native iterations) is timed separately.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.json`](bench/results.json) (M5, canonical) and [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — at **matched reference semantics** (`shared struct` vs `Rc<RefCell>`), the same direct comparison as the linked-list siblings. C's raw-pointer list is the metal floor, Go the GC data point, Python (a fraction of the iteration count, timed separately) the ergonomic foil.
