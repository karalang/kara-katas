# 82. Remove Duplicates from Sorted List II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Linked List · Two Pointers &nbsp;·&nbsp; **Source:** [leetcode.com/problems/remove-duplicates-from-sorted-list-ii](https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/)

Given the head of a **sorted** linked list, delete **all** nodes that have duplicate numbers, leaving only numbers that were **distinct** in the original list. Return the resulting sorted list. Unlike kata #83 (its `m = 1` sibling, which keeps one copy of each value), a value that repeats is removed **entirely**.

```
1 → 2 → 3 → 3 → 4 → 4 → 5   ->   1 → 2 → 5
1 → 1 → 1 → 2 → 3           ->   2 → 3
```

**Constraints:** `0 ≤ nodes ≤ 300`; `-100 ≤ Node.val ≤ 100`; list sorted non-decreasing.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Iterative, dummy + `prev` cursor** ★ | [`remove_duplicates_ii_list.kara`](remove_duplicates_ii_list.kara) ✓ via `karac run` / `karac build` | [`remove_duplicates_ii_list.py`](remove_duplicates_ii_list.py) ✓ |
| **Structural recursion** | [`remove_duplicates_ii_list_recursive.kara`](remove_duplicates_ii_list_recursive.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output across all ten test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other and with the Python mirror. Both compile with **zero diagnostics**.

## The list model, and two ways to drop whole runs

Both solvers model the list with Kāra's reference-semantics node — a `shared struct` (Rc-like handle), the same one katas [#2](../2-add-two-numbers/) and [#21](../21-merge-two-sorted-lists/) use:

```
shared struct ListNode { val: i64, mut next: Option[ListNode] }
```

`Option[ListNode]` is the `Some(node) | None` link, and `node.next = …` re-links by aliasing the shared handle — no node copying. The whole kata is about splicing *entire runs* out of that chain.

**Iterative, dummy + `prev`** ([`remove_duplicates_ii_list.kara`](remove_duplicates_ii_list.kara), the ★) is the canonical single pass. A dummy node before the head means the first node can be dropped without a special case, and a `prev` cursor holds the last node **known to be kept**:

```
dummy.next = head; prev = dummy; cur = head
while cur:
    if cur.next and cur.val == cur.next.val:     # cur starts a duplicate run
        v = cur.val
        while cur and cur.val == v: cur = cur.next   # skip the whole run
        prev.next = cur                              # splice it out; prev does NOT move
    else:
        prev = cur; cur = cur.next                   # unique so far — keep it
return dummy.next
```

The load-bearing subtlety is that `prev` **does not advance** when a run is dropped: the node after the run might itself start another run (`[1,1,2,3,3,4]` → `[2,4]` — the `2` that briefly looks safe is fine, but adjacent runs like `[1,1,2,2]` must all splice onto the same `prev`). Only the *keep* branch moves `prev`.

**Structural recursion** ([`remove_duplicates_ii_list_recursive.kara`](remove_duplicates_ii_list_recursive.kara)) expresses the same rule without a dummy or a `prev` cursor — each call decides the fate of the front node:

```
delete_duplicates(head):
    if head is None: return None
    if head.val == head.next.val:            # front starts a run — drop the whole run
        skip every node equal to head.val
        return delete_duplicates(rest)       # front never appears
    else:                                    # front is unique — keep it
        head.next = delete_duplicates(head.next)
        return head
```

"Keep this node, recurse on the tail" is written directly as `node.next = delete_duplicates(node.next); Some(node)`, mutating the kept node's `next` through its shared handle — the same shape kata #21's recursive merge uses. O(n) recursion depth, one frame per front node.

## Kāra features exercised

- **`shared struct` (Rc) linked list** — reference-semantics nodes threaded as `Option[ListNode]`; `prev.next = runner` and `node.next = delete_duplicates(...)` re-link by aliasing the Rc handle, with no per-node copy. This is the RC-fallback / ownership machinery under real pointer-mutation load, verified byte-identical under codegen *and* auto-par.
- **`Option` pattern matching** — `match cur { Some(node) => … None => break }` and nested `match node.next { Some(nxt) => … None => {} }` drive both the outer scan and the run-skip; the recursive solver's whole body is a `match head { Some(node) => … None => None }`.
- **`loop { … break }` with an inner run-skip loop** — the ★ nests a runner loop inside the scan loop to consume a whole equal-valued run before splicing.
- **`shared struct` handle reassignment across a mutation** — `prev`, `cur`, and `runner` are re-pointed (`cur = node.next`) while `prev.next` is simultaneously mutated; the shared semantics make aliasing and re-linking coexist.
- **`f"{s}{node.val}"` string building in `to_string`** — the list renderer accumulates the `[...]` output by interpolation (shared with kata #21's harness).

**v1 note.** Lists are short (`≤ 300` nodes) and values fit i64; the per-case sink folds each result's length and surviving values into a running polynomial hash so it is both length- and content-sensitive across the ten cases. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   remove_duplicates_ii_list.kara
karac build remove_duplicates_ii_list.kara && ./remove_duplicates_ii_list

# The recursive variant (identical output):
karac run remove_duplicates_ii_list_recursive.kara

# Python
python3 remove_duplicates_ii_list.py

# Verify they all agree
diff <(karac run remove_duplicates_ii_list.kara) <(python3 remove_duplicates_ii_list.py)                        && echo OK
diff <(karac run remove_duplicates_ii_list.kara) <(karac run remove_duplicates_ii_list_recursive.kara)          && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`remove_duplicates_ii_list.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5-confirmed (2026-07-11).** Re-measured on the corpus's **Apple M5 Pro reference machine** (arm64, 6P+12E; clang 21 / rustc 1.95 / go 1.26; karac from current `main`), replacing the earlier x86-64 cloud-container snapshot. **The load-bearing result holds; the ordering shifts:** kāra's `shared struct` still beats Rust's `Rc<RefCell>` at equal reference semantics (1.10×), but Go's GC-managed pointer list — 4th on the container — leapfrogs to *fastest* on the M5, so kāra lands 3rd of five. `bench/results.json` records the M5 host.

**Workload.** The dedup pass mutates/re-links the list, so — like kata [#21](../21-merge-two-sorted-lists/)'s merge bench — each iteration builds a **fresh** sorted linked list and runs `delete_duplicates` on it. The list is an **M = 300** sorted run where every **even** value is duplicated (removed by #82) and every **odd** value is single (kept): `[0,0,1,2,2,3,…]`. For **K = 61,000** iterations (seeded by the loop index so nothing hoists) it builds, dedups, and folds the surviving values through a **rolling polynomial hash**. Per-iteration node allocation is part of the measured work — fair, since every mirror allocates its nodes — alongside the RC-node pointer chase and the run-detection logic. All five compiled mirrors must agree on `494436670` before timing.

**Equal data structure.** Kāra uses a `shared struct` (Rc-like) list; **Rust mirrors it with `Rc<RefCell<ListNode>>`** (the same per-node reference-count overhead — a mutable shared node needs interior mutability), Go uses a GC-managed `*ListNode`, and **C a plain `malloc`/`free` raw-pointer list** (single-owner in this workload, the honest metal floor). This keeps the comparison codegen-vs-codegen at matched reference semantics rather than handing anyone a cheaper node.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded, ~99 % CPU (verified equal to `KARAC_AUTO_PAR=0`; `karac build --concurrency-report` finds no parallelizable region). **M5 Pro numbers.**

| Implementation | Wall time |
|---|---|
| go   remove_duplicates_ii_list                               | **296.1 ± 4.5 ms** |
| c    remove_duplicates_ii_list (clang -O3)                    | 350.0 ± 5.0 ms |
| **kāra remove_duplicates_ii_list**                           | **463.6 ± 8.3 ms** |
| rust remove_duplicates_ii_list (rustc -O, overflow-checks=on)| 510.1 ± 10.0 ms |
| rust remove_duplicates_ii_list (rustc -O)                    | 510.9 ± 10.8 ms |

**The load-bearing result survives the reordering:** at **matched reference semantics** kāra's `shared struct` still beats Rust's `Rc<RefCell<ListNode>>` — **1.10×** ahead of both `rustc -O` (510.9 ms) and overflow-checked Rust (510.1 ms). `RefCell` pays a runtime borrow-flag check on every `.borrow()`/`.borrow_mut()` (several per step) where kāra's RC handle reads the value directly; that tax is most of the gap, and it survives on the reference machine. What *changed* from the container is the top: **Go's GC-managed pointer list jumps from 4th to fastest** (296.1 ms — arm64's allocator loves this build-a-fresh-list-per-iteration churn), and unchecked raw-pointer C sits 2nd, so kāra lands **3rd of five** — 1.32× behind C, 1.57× behind Go, still ahead of both Rusts. Overflow checks are free here (the loop is allocation/pointer-bound). Python (K=3000, ~0.43 s at 1/20 the native iteration count) is timed separately.

**Binary size & RSS.** The kāra binary is **33.1 KiB** (C parity, 32.7 KiB) and peak RSS **1.05 MiB** — tied with C, lowest of the five — versus Go's **9.4 MiB** GC heap. See [`bench/results.json`](bench/results.json).

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — and here, at **matched reference semantics** (`shared struct` vs `Rc<RefCell>`), the comparison is especially direct. C's raw-pointer list calibrates the metal floor, Go is the GC data point, Python (run at a fraction of the iteration count, timed separately) the ergonomic foil.
