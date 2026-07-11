# 83. Remove Duplicates from Sorted List

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Linked List &nbsp;·&nbsp; **Source:** [leetcode.com/problems/remove-duplicates-from-sorted-list](https://leetcode.com/problems/remove-duplicates-from-sorted-list/)

Given the head of a **sorted** linked list, delete duplicates so that each value appears **exactly once**, and return the sorted list. Unlike kata [#82](../82-remove-duplicates-from-sorted-list-ii/) (which removes *every* node of a repeated value), #83 keeps the **first** copy of each value.

```
1 → 1 → 2           ->   1 → 2
1 → 1 → 2 → 3 → 3   ->   1 → 2 → 3
```

**Constraints:** `0 ≤ nodes ≤ 300`; `-100 ≤ Node.val ≤ 100`; list sorted non-decreasing.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Iterative, in-place skip** ★ | [`remove_duplicates_list.kara`](remove_duplicates_list.kara) ✓ via `karac run` / `karac build` | [`remove_duplicates_list.py`](remove_duplicates_list.py) ✓ |
| **Structural recursion** | [`remove_duplicates_list_recursive.kara`](remove_duplicates_list_recursive.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output across all ten test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other and with the Python mirror. Both compile with **zero diagnostics**.

## Keep the first copy — no dummy needed

Both solvers use Kāra's reference-semantics node (a `shared struct`, Rc-like handle), the same model katas [#82](../82-remove-duplicates-from-sorted-list-ii/) and [#21](../21-merge-two-sorted-lists/) use:

```
shared struct ListNode { val: i64, mut next: Option[ListNode] }
```

Because #83 keeps the first copy of each value, **the head is never deleted** — so, unlike #82, no dummy node is required.

**Iterative, in-place skip** ([`remove_duplicates_list.kara`](remove_duplicates_list.kara), the ★) walks a single cursor:

```
cur = head
while cur:
    if cur.next and cur.val == cur.next.val:
        cur.next = cur.next.next     # splice out the duplicate; STAY on cur
    else:
        cur = cur.next               # differs — advance
return head
```

The load-bearing detail is that the cursor **stays put** after a splice, so a run of three or more (`[1,1,1]`) collapses to a single node in place — only a differing successor advances the cursor. `cur.next = cur.next.next` re-links by aliasing the shared handle, no copying.

**Structural recursion** ([`remove_duplicates_list_recursive.kara`](remove_duplicates_list_recursive.kara)) dedups the tail first, then decides the front node:

```
head.next = delete_duplicates(head.next)     # dedup the suffix
return head.next if head.val == head.next.val else head
```

After the recursive call, `head.next` is the head of a fully-deduped suffix; if it carries `head`'s value, `head` is a redundant copy and is dropped by returning `head.next`, else `head` is kept with its rewired tail. It's the mirror of kata #82's recursive form (there the whole run is dropped; here only the redundant copy), O(n) frames deep.

## Kāra features exercised

- **`shared struct` (Rc) linked list, in-place re-link** — `cur.next = cur.next.next` (★) and `node.next = delete_duplicates(node.next)` (recursive) re-link by aliasing the Rc handle; the RC / ownership machinery under real pointer-mutation load, verified byte-identical under codegen *and* auto-par.
- **`Option` pattern matching** — the ★ nests `match cur { Some(node) => match node.next { … } }`; the recursive solver's body is a single `match head { Some(node) => … None => None }`.
- **Cursor-stays-put splice loop** — the ★'s `loop { … }` re-tests the same `cur` after a splice, so `[1,1,1,1]` folds without advancing.
- **`f"{s}{node.val}"` string building** — the `[...]` renderer accumulates via interpolation (shared with #82's harness).

**v1 note.** Lists are short (`≤ 300` nodes) and values fit i64; the per-case sink folds each result's length and surviving values into a running polynomial hash. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   remove_duplicates_list.kara
karac build remove_duplicates_list.kara && ./remove_duplicates_list

# The recursive variant (identical output):
karac run remove_duplicates_list_recursive.kara

# Python
python3 remove_duplicates_list.py

# Verify they all agree
diff <(karac run remove_duplicates_list.kara) <(python3 remove_duplicates_list.py)                  && echo OK
diff <(karac run remove_duplicates_list.kara) <(karac run remove_duplicates_list_recursive.kara)    && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`remove_duplicates_list.{kara,rs,c,py}`, `go-seq/main.go`).

> ⚠️ **Machine caveat.** Measured on a **shared x86-64 Linux cloud container** (Intel Xeon @ 2.80 GHz, 4 vCPU, Linux 6.18.5; karac from current `main`). These are container numbers only — this kata has **no M5 `results.json` yet**; it will be re-benched on the corpus's Apple M5 Pro and the canonical table added then. Don't compare absolute times/sizes/RSS against sibling katas' M5 tables; [`bench/results.container-x86.json`](bench/results.container-x86.json) records the real host.

**Workload.** The dedup mutates/re-links the list, so — like kata [#21](../21-merge-two-sorted-lists/)/[#82](../82-remove-duplicates-from-sorted-list-ii/) — each iteration builds a **fresh** sorted list and runs `delete_duplicates`. The list is an **M = 300** run with **every value duplicated** (`[0,0,1,1,2,2,…]`, so the keep-one dedup halves it uniformly). For **K = 70,000** iterations (seeded by the loop index so nothing hoists) it builds, dedups, and folds the survivors through a **rolling polynomial hash**. Per-iteration node allocation is part of the measured work — fair, since every mirror allocates its nodes. All five compiled mirrors must agree on `674382658` before timing.

**Equal data structure.** Kāra uses a `shared struct` (Rc-like) list; **Rust mirrors it with `Rc<RefCell<ListNode>>`** (same per-node reference-count overhead), Go uses a GC-managed `*ListNode`, and **C a plain `malloc`/`free` raw-pointer list** (single-owner here, the honest metal floor).

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded (the loop-carried sum is not a reduction the auto-par pass can split; the default build is verified equal to `KARAC_AUTO_PAR=0`). **Cloud-container numbers.**

| Implementation | Wall time |
|---|---|
| c    remove_duplicates_list (clang -O3)                    | 600.8 ± 12.8 ms |
| **kāra remove_duplicates_list**                           | **809.7 ± 32.3 ms** |
| rust remove_duplicates_list (rustc -O)                    | 999.8 ± 30.2 ms |
| rust remove_duplicates_list (rustc -O, overflow-checks=on)| 1034.4 ± 41.2 ms |
| go   remove_duplicates_list                               | 1294.5 ± 39.0 ms |

The same ordering as its `m = 2` sibling [#82](../82-remove-duplicates-from-sorted-list-ii/): kāra **2nd of five — ahead of both Rust builds and Go**, behind only raw-pointer C. At matched reference semantics kāra's `shared struct` beats Rust's `Rc<RefCell<ListNode>>` by ~1.24× (the `RefCell` borrow-flag check on every node access is the gap), and beats GC-managed Go by ~1.60×; overflow checks cost Rust another ~3%. C's unchecked raw-pointer list is the floor at ~1.35× under kāra. Python (K=3500, ~0.54 s at 1/20 the native iteration count) is timed separately.

**Binary size & RSS.** As with #82, the kāra binary is **15.4 KiB** — on par with C, ~20× smaller than compute siblings — because this RC-allocation loop is not an auto-parallelisation candidate, so no scheduler runtime links in; peak RSS is **1.54 MiB** (tied with C, lowest), versus Go's **7.43 MiB** GC heap. See [`results.container-x86.json`](bench/results.container-x86.json).

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — and here, at **matched reference semantics** (`shared struct` vs `Rc<RefCell>`), the comparison is especially direct. C's raw-pointer list calibrates the metal floor, Go is the GC data point, Python (run at a fraction of the iteration count, timed separately) the ergonomic foil.
