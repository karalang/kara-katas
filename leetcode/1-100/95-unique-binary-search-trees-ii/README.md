# 95. Unique Binary Search Trees II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Dynamic Programming · Tree · Binary Search Tree · Backtracking · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/unique-binary-search-trees-ii](https://leetcode.com/problems/unique-binary-search-trees-ii/)

Given an integer `n`, return **every structurally unique BST** (binary *search* tree) that stores exactly the integers `1..n`. The number of them is the *n*th **Catalan number** — `1, 2, 5, 14, 42, 132, 429, 1430` for `n = 1..8`.

```
n = 3  ->  five BSTs over {1,2,3}:

   1         1       2        3       3
    \         \     / \      /       /
     2         3   1   3    1       2
      \       /            \       /
       3     2              2     1
```

**Constraints:** `1 ≤ n ≤ 8`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Recursive divide & conquer** ★ | [`generate_trees.kara`](generate_trees.kara) ✓ | [`generate_trees.py`](generate_trees.py) ✓ |
| **Bottom-up shape DP + value offset** | [`generate_trees_dp.kara`](generate_trees_dp.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for both approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the two Kāra approaches agree with **each other** and with the Python mirror, and every `n`'s tree count is the *n*th **Catalan number** (an independent ground-truth check: `1, 2, 5, 14, 42, 132, 429`). Both solvers compile with zero diagnostics.

## Two ways to enumerate every BST

Both solvers exploit the BST invariant: pick a root value `r`, and *everything smaller* must sit in its left subtree, *everything larger* in its right. They differ in **how the subtrees are reused**.

**Recursive divide & conquer** ([`generate_trees.kara`](generate_trees.kara), the ★) is the textbook shape — to build every BST over the value range `[lo, hi]`, try each value as the root and take the full cross product of all left subtrees with all right subtrees:

```
build_all(lo, hi):
    if lo > hi: return [None]                 # the empty range: one empty subtree
    for r in lo..hi:
        for l in build_all(lo, r-1):          # every left subtree
            for right in build_all(r+1, hi):  # every right subtree
                emit TreeNode(r, l, right)
```

Subtrees are `shared struct TreeNode` (RC) handles, so the **same** left/right subtree instance is *shared* across every root that pairs with it — the structural sharing this problem is famous for, expressed naturally because RC makes the aliasing safe: `TreeNode { val: r, left: lefts[li], right: rights[ri] }` stores a second reference to an existing subtree, never a copy.

**Bottom-up shape DP** ([`generate_trees_dp.kara`](generate_trees_dp.kara)) reaches the identical trees without recursion, by observing that the *shape* of a BST over a contiguous range depends only on the range's **size**, not its actual values — the BSTs over `[1..k]` and over `[r+1..r+k]` are the same shapes, one relabelled by `+r`. So it builds a table `shapes[k]` = every BST over the canonical values `1..k`, bottom-up:

```
shapes[0] = [None]
shapes[k] = for root position r in 1..k:
                for L in shapes[r-1]:            # left subtree, values 1..r-1
                    for R in shapes[k-r]:        # right subtree, values 1..k-r
                        TreeNode(r, clone(L), clone(R) offset by r)
```

Here the right subtree's values must shift into `r+1..k`, so it is **deep-cloned with a `+r` value offset** (`clone_offset`) — a genuinely distinct mechanism from the ★'s instance sharing. It walks the identical candidate order as the ★'s recursion (root value `r` ascending, left cross right), so the two serialize **byte-identically**.

The two approaches are a deliberate contrast in how a language of RC values handles subtree reuse: the ★ **aliases** shared subtrees (many roots point at one instance), the DP **deep-clones** them (each root owns fresh nodes). Both are natural Kāra; exercising both is the point.

## Kāra features exercised

- **`shared struct TreeNode` (RC) with `Option[TreeNode]` children** — the tree node type shared with kata [#94](../94-binary-tree-inorder-traversal/) / [#98](../98-validate-binary-search-tree/); `match` on `Option` children drives the serialization and the `clone_offset` recursion.
- **RC structural sharing** — the ★ stores the *same* `Vec[Option[TreeNode]]` element (`lefts[li]`, `rights[ri]`) into many roots, aliasing one subtree across the whole Catalan-sized forest; the refcount keeps every alias live and frees each node exactly once.
- **`Vec[Vec[Option[TreeNode]]]` shape table** — the DP holds a growing table of per-size BST lists, indexing `shapes[r-1]` / `shapes[k-r]` and pushing a fresh `shapes[k]` row each lap (a nested collection of RC handles, grown in place).
- **Recursive deep clone with a value transform** (`clone_offset`) — the DP rebuilds a subtree node-for-node while adding `delta` to every value, the deep-copy counterpart to the ★'s sharing.
- **`mut ref String` serialization** — both approaches fold each tree into a canonical preorder string (`#,` for null, `val,` for a node) threaded through a `mut ref String` accumulator, then hash its bytes into an order-sensitive sink.

**v1 note.** `n ≤ 8` keeps the forest inside the Catalan bound (≤ 1430 trees). The per-`n` sink folds the tree count and every tree's serialized bytes (in `build_all` order, with a separator) into a running polynomial hash — count-, content-, and order-sensitive. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other and the Python mirror, and every tree count matches the Catalan ground truth.

The DP variant was also the surface that surfaced and drove [`B-2026-07-11-29`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) — a cluster of five RC-accounting gaps in `Vec[Option[shared]]` clone + consume + share + grow, now fixed in the compiler (it is clean under LeakSanitizer/valgrind across every surface).

The same variant surfaced two further **high-severity double-frees**, both codegen-only (the tree-walk interpreter was correct throughout) and both now fixed:

- [`B-2026-07-11-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) — reusing an owned `Option[shared struct]` value across two by-value consuming calls whose callee *clones* the matched subtree double-freed under both JIT and AOT, silently and with no diagnostic.
- [`B-2026-07-11-24`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) — passing a `Vec[Vec[Option[shared]]]` **element** by value to that same consuming callee corrupted the heap once the outer `Vec` grew in a loop: a wrong answer at small `n`, a double-free crash at larger.

Together with `B-2026-07-11-29` these make the DP variant the corpus's densest RC-ownership bug-finder — which is why it is kept alongside the ★ rather than folded into it.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   generate_trees.kara
karac build generate_trees.kara && ./generate_trees

# The bottom-up shape-DP variant (identical output):
karac run generate_trees_dp.kara

# Python
python3 generate_trees.py

# Verify they all agree
diff <(karac run generate_trees.kara) <(python3 generate_trees.py)          && echo OK
diff <(karac run generate_trees.kara) <(karac run generate_trees_dp.kara)   && echo OK
```

## Benchmarks
Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`generate_trees.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** Canonical numbers measured on the corpus's **Apple M5 Pro** (6P+12E, Darwin 25.6.0; karac g6697158fa (0.9.0-dev.14057, v2/MIR backend), `rustc 1.95.0`, Apple clang 21.0.0, `go 1.26.3`, hyperfine 1.20; measured 2026-11-01) — [`bench/results.json`](bench/results.json). A shared x86-64 Linux cloud-container reference run is kept alongside in [`bench/results.container-x86.json`](bench/results.container-x86.json); absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. This is the corpus's most allocation-dominated kata, so its ordering shifts more than any other between the two hosts — see the note below the table. (The M5 compiler carries the `Vec[Option[shared]]` RC-accounting fix `B-2026-07-11-29`; the kāra output is verified correct **and** memory-clean here — the earlier container run predates that fix and was correct only by allocator luck.)

**Workload.** Building all BSTs for a *fixed* `n` once is instant, so this is a **build-once + fold** workload with no vectorizable refill loop: each of **K = 250** passes builds **every** structurally-unique BST over the values `1..8` (recursive divide & conquer, `1+2+5+14+42+132+429+1430 = 2055` trees per pass) and folds each tree's canonical preorder serialization (`#,` null / `val,` node) into a rolling polynomial hash. Folding the serialization rather than materializing all strings keeps the loop-carried hash the only cross-iteration state; it is **not** a reduction the auto-par pass can split, so the default `karac build` stays single-threaded (its emitted IR, `KARAC_MIR_LL`, carries no call of `@karac_mir_task_spawn`, same as its `KARAC_AUTO_PAR=0` twin — checked 2026-11-01). All five compiled mirrors must agree on `569418406` before timing.

**Equal data structure.** Matched to each language's natural idiom for this build-then-serialize-then-drop shape: Kāra `shared struct TreeNode` (RC, so equal subtrees are **shared** across roots), **Rust single-owner `Box<Node>`** (each pair cloned into its root, same choice as sibling tree kata [#98](../98-validate-binary-search-tree/)), **C a `malloc`/`free` raw-pointer tree** (deep-copied), Go a GC-managed `*Node` (deep-copied). The RC-sharing-vs-deep-copy split is the honest cross-language memory story, **not** a workload mismatch — every mirror emits the identical set of trees and the identical serialization, so the sink agrees byte-for-byte.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **Apple M5 Pro numbers, 2026-11-01.**

| Implementation | Wall time |
|---|---|
| go   generate_trees (`*Node`, GC)                    | 333.5 ± 2.0 ms |
| c    generate_trees (clang -O3, malloc tree)        | 507.9 ± 17.4 ms |
| rust generate_trees (rustc -O, Box)                 | 542.1 ± 14.7 ms |
| rust generate_trees (rustc -O, overflow-checks=on)   | 551.4 ± 22.7 ms |
| **kāra generate_trees**                             | **553.0 ± 27.1 ms** |

**Kāra still trails on the same-work deep-copy table — the honest cost of RC allocation on the corpus's most allocation-dominated kata.** Each pass deep-copies `2055` trees node-by-node, ≈ **1.3 M node allocations/pass × 250 = ~330 M allocations/run**, and the fold does almost nothing else. On the M5 kāra is **1.66× behind Go**, **1.09× behind C**, **1.02× behind unchecked Rust**, and in a dead heat with checked Rust (553.0 vs 551.4 ms, within σ). Against the previous feed (2026-09-07) the ratios are flat within this session's noise band — Kāra/Rust 0.93× → 1.02×, Kāra/C 1.02× → 1.09×, Kāra/Go 1.53× → 1.66× — and against the 2026-07-11 snapshot this table used to show (Kāra/Rust 1.10×, Kāra/C 1.19×, Kāra/Go 1.89×) kāra is closer on every comparator. Compared with the container the gaps moved in opposite directions, and the reason is instructive:

- **The C gap narrowed (1.30× → 1.09×), and it is no longer the header *width*.** macOS's allocator rounds **both** C's 24 B node and kāra's 32 B `{rc,val,left,right}` node into the **same 32-byte slot** (measured via `malloc_size`, see [#94](../94-binary-tree-inorder-traversal/)) — so the 8-byte refcount header is *free* here. The residual 1.09× is the per-node **rc-init store** (writing the header on every node) plus the **rc-dec on the drop walk** — real instructions C skips — not memory-bandwidth from a wider node. On Linux, where the 24 B node packs tighter, the width cost was also live and the gap was larger.
- **The Go gap widened (1.42× → 1.66×).** 330 M allocations/run is exactly Go's sweet spot; its bump-allocator + concurrent GC (118 % CPU — 395 ms user+system CPU, still under kāra's 552 ms) pulls *further* ahead on the M5's fast cores. The trade stays memory: Go holds **9.8 MiB** peak RSS against kāra's **2.0 MiB** (C 1.7 MiB, Rust 1.8 MiB) and ships a **2.4 MiB** binary against kāra's **295.8 KiB** (302,896 B; C 33.1 KiB) — ~5.0× the RSS and ~8.3× the binary for its speed. Every v2/MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (this kata's was 33.4 KiB, ~73× under Go's), tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md).

The equal-safety `rustc -O -C overflow-checks=on` row lands within σ of unchecked `rustc -O` (1.02×; the checks are nearly free here — the bottleneck is `malloc`, not arithmetic), and kāra ties the checked row and trails the unchecked one by 1.02×. This is the RC-alloc-tax regime flagged for [#92](../92-reverse-linked-list-ii/) and [#98](../98-validate-binary-search-tree/), at its most exposed. (The container recorded a ~329 KB kāra binary — a build-linkage artifact that retained the backtrace-symbolizer tree; the legacy M5 build stripped it correctly, so the real legacy size was **33.4 KiB**, C parity. On v2/MIR, 2026-11-01, the binary is 295.8 KiB per `B-2026-10-28-36` above.)

**The idiomatic solver tells the other half of the story.** The table forces every language onto **deep-copy** so the work is identical (kata rule: same workload). But the *natural* Kāra solution — the ★ [`generate_trees.kara`](generate_trees.kara) — doesn't copy at all: it **RC-shares** each subtree across every root that reuses it, which is the whole point of this problem. Benched in that idiomatic form ([`bench/generate_trees_share.kara`](bench/generate_trees_share.kara) — same K, same sink `569418406`, MallocScribble-clean) Kāra runs the workload in **359 ± 8 ms** (last measured 2026-07-11, not re-run; the share form is not in `bench/results.json`, and the ratios here are against that day's table) — **1.51× faster than its own deep-copy row**, and faster than **C (1.27×)** and **both Rust builds** — because it simply doesn't do the allocation the copy-only languages must. On the M5 only **Go's concurrent-GC allocator (289 ms that day) still edged it** (1.24×), where on the container the sharing form was outright fastest; the ordering flip is the same alloc-bound Go-on-M5 effect as [#94](../94-binary-tree-inorder-traversal/). Still a real language advantage — RC sharing does asymptotically less allocation, and Kāra has it cheaply — so it is noted here rather than folded into the same-work table: the fair *CPU* comparison has Kāra behind, the fair *solution* comparison has it 2nd and ahead of every single-threaded-allocator language.

Python (K = 40, a fraction of the compiled iterations, timed separately at **219 ms** — last measured 2026-07-11, not re-run; not cross-checked) is the ergonomic foil.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.json`](bench/results.json) (M5, canonical) and [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at matched single-owner node representation (`shared struct` vs `Box`), the same direct comparison as the tree sibling [#98](../98-validate-binary-search-tree/). C's raw-pointer tree is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
