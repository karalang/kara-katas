# 39. Combination Sum

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array, Backtracking &nbsp;·&nbsp; **Source:** [leetcode.com/problems/combination-sum](https://leetcode.com/problems/combination-sum/)

Given **distinct** positive integers `candidates` and a `target`, return every unique
combination of candidates that sums to `target`. The **same** candidate may be chosen any
number of times, and a combination is a *multiset* of choices — order does not matter, so
`[2,2,3]` and `[2,3,2]` are one combination, not two.

```
candidates = [2,3,6,7], target = 7   →  [[2,2,3], [7]]
candidates = [2,3,5],   target = 8   →  [[2,2,2,2], [2,3,3], [3,5]]
candidates = [2],       target = 1   →  []
```

**Constraints:** `1 ≤ candidates.length ≤ 30`, `2 ≤ candidates[i] ≤ 40` (all distinct),
`1 ≤ target ≤ 40`. The number of combinations can be large, but each is a list of chosen
candidates in non-decreasing index order.

## Why this kata — backtracking that *builds a set of paths*, three ways

After [#38](../38-count-and-say/) (pure `String` growth) and the allocation-free fixed
grids of [#36](../36-valid-sudoku/)/[#37](../37-sudoku-solver/), #39 is the **nested-
collection** counterpart: the answer is a `Vec[Vec[i64]]`, grown by **snapshotting a
backtracking path** at every solution leaf. The work is recursion + per-node push/pop + a
**path copy** at each hit + nested-Vec heap growth — so this kata is about *how you carry
the current branch's choices* and *how you record a finished combination*.

Uniqueness is free from an **index-bounded DFS**: each call may pick `candidates[start..]`,
and picking `candidates[i]` recurses with `start = i` (**not** `i+1`, so the value can be
reused) while never looking left of `i`. That monotone walk visits each multiset of
choices exactly once — the index discipline *is* the dedup, no HashSet of seen combinations
needed. Two axes vary across the three styles — **how the path is carried** (one mutable
buffer with undo, vs. an immutable snapshot per descent) and **how the candidate axis is
pruned** (a per-candidate `c <= remaining` test, vs. a sorted-array `break`):

| Lens | Idea |
|---|---|
| **Mutable-path DFS** ★ | carry one `mut ref Vec[i64]` path; `push` / recurse-at-`i` / `pop` brackets each choice; snapshot `path.clone()` at `remaining == 0`; descend a candidate only when `c <= remaining` |
| **Immutable-snapshot DFS** | carry the path as an owned `Vec[i64]`; each descent builds a fresh child (`path.clone()` + `push`) and never undoes — the functional shape, like [#22](../22-generate-parentheses/)'s string snapshots |
| **Sorted + early-break** | sort the candidates first, turning the per-candidate filter into a suffix cut: once `candidates[i] > remaining`, every later one overshoots too, so `break` |

## Approaches

Three styles, all agreeing with the Python oracle for the LeetCode examples under `karac run`
**and** `karac build`.

| Approach | File | Shape |
|---|---|---|
| **Mutable-path DFS** ★ | [`combination_sum.kara`](combination_sum.kara) | `path: mut ref Vec[i64]`, `push`/recurse-at-`i`/`pop`, `out.push(path.clone())` at the leaf |
| Immutable-snapshot DFS | [`combination_sum_snapshot.kara`](combination_sum_snapshot.kara) | owned `path: Vec[i64]`, `let next = path.clone(); next.push(c)` per descent, move the leaf snapshot into `out` |
| Sorted + early-break | [`combination_sum_sorted.kara`](combination_sum_sorted.kara) | `cands.sort_by(\|a, b\| a.cmp(b))`, then `if c > remaining { break }` |

The mutable-path form is the tightest (one buffer, the clone only at the leaf); the snapshot
form trades a per-descent copy for zero pop bookkeeping and no shared mutable state; the
sorted form makes the candidate-axis prune a single suffix cut at the cost of an up-front
sort. All three are O(answer size) to emit and agree on every combination.

## What this kata surfaced

Both findings are **run/build divergences** in the `out.push(path.clone())` shape every
solver here uses — the kata's backtracking idiom drove the compiler straight into them.

**`<expr>.clone()` on a borrowed (`ref` / `mut ref`) collection receiver shallow-aliased
instead of deep-copying** ([`B-2026-06-18-9`](../../../../kara/docs/bug-ledger.jsonl),
`kata:39`, codegen, **fixed [`c0432862`](../../../../kara/docs/bug-ledger.jsonl)**). The
backtracking leaf does `out.push(path.clone())` where `path` is a `mut ref Vec[i64]`. Under
`karac build` the snapshot came out **empty**: the build emitted the right *count* of
combinations but every inner list was `[]`. `try_compile_clone` passed the variable's raw
alloca pointer to the per-type clone fn — but for a borrowed parameter the alloca holds a
pointer *to* the value (`**Vec`), so the clone copied the `{data,len,cap}` header out of the
pointer's own bits, yielding a Vec whose data pointer **aliased the source buffer**. The
subsequent `path.pop()` on the way back up then drained the "snapshot" to length 0. The
interpreter always deep-copied, so it was a pure run/build split. **The fix** routes the
receiver through `get_data_ptr`, which load-throughs one ref-level for `ref`/`mut ref`
params (and unboxes RC-promoted bindings past their refcount header) while leaving owned
bindings — the common case — at `slot.ptr` unchanged. So all three solvers' leaf snapshots
now deep-copy under `karac build`, exactly as under `karac run`.

**An auto-parallelized `sort_by(|a, b| a.cmp(b))` emitted a stray cancel-flag load and
failed module verification** ([`B-2026-06-18-10`](../../../../kara/docs/bug-ledger.jsonl),
`kata:39`, codegen, **fixed [`c0432862`](../../../../kara/docs/bug-ledger.jsonl)**). The
sorted solver sorts the candidates; a `path.clone()` later in the same function tipped the
auto-par analyzer into parallelizing the (resource-disjoint) sort and clone, so the sort
helpers were emitted **inside a `par {}` branch's cancel context**. With `branch_cancel_ptr`
pointing at the par-branch fn's `cancel_flag` argument, the comparator thunk's `a.cmp(b)`
ran the cooperative-cancel check and emitted `load i8, ptr %1` — but `%1` in the comparator
/ mono-sort helpers is an element pointer / the `i64` length, not a cancel flag, so LLVM
rejected the module (*"Referring to an argument in another function"* + a `ret void`/`i64`
type mismatch). `karac run` and the `KARAC_AUTO_PAR=0` build were both fine; only the
auto-par default build failed. **The fix** clears `branch_cancel_ptr` for the duration of
each separate-function body emission — `compile_closure` and the three sort emitters
(`emit_sort_by_inline_thunk`, `emit_sort_by_key_inline_thunk`, `emit_sort_by_mono`) — the
same `take()`/restore the par/reduce/task-group emitters already do, since a closure or sort
helper is a distinct function whose body must not inherit the caller's cancel argument.

Both fixes ship with E2E regression tests (`test_e2e_vec_clone_borrowed_receiver_is_deep`,
`test_auto_par_sort_by_comparator_no_stray_cancel_flag_e2e`) and benefit **all** Vec-clone /
sorted / closure code, not just this kata. Full codegen (1618) + par_codegen (122) +
memory_sanitizer ASAN (264) + Linux LSan (264) green; fmt + clippy clean.

## Benchmarks

Workload: enumerate combinations for a per-iteration target. **`TOTAL = 30000`** times, with
candidates `[2,3,5,7]`, set `target = 18 + (k % 13)` (a per-iteration target, so nothing
hoists), solve with the ★ mutable-path backtracker, and fold a **position-weighted**
signature of every combination — `sum element*(i+1)` per combo, combos folded by a rolling
`*31`, plus the combination count — into a rolling checksum (sink `503333481`). The target
varies with the loop index (no comparator can hoist the work out) and the checksum carries a
loop-borne dependency, so this is a single-lane (seq) bench by construction. Unlike #36/#37
this is a **heap-allocating** workload — each solve grows a fresh `Vec[Vec[i64]]` and clones
a path at every leaf — so it isolates nested-collection allocation + the backtracking
codegen, the counterpart to #38's `String` growth. Apple M5 Pro; `bench/bench.sh`
(`hyperfine`).

### Seq lane — runtime (single-threaded mutable-path backtracking)

| | Rust (`-O`) | Rust (`overflow-checks=on`) | C | Go | **Kāra** | Python |
|---|---|---|---|---|---|---|
| time | 40.3 ms | 40.8 ms | 43.1 ms | 48.2 ms | **59.0 ms** | 759 ms |
| vs Kāra | 1.46× faster | **1.45× faster (= safety)** | 1.37× faster | 1.22× faster | — | 12.9× slower |

**Kāra trails the C-class here, and the gap is allocation, not the algorithm.** Where the
stack-integer compute of #36/#37 put Kāra *ahead* of C, #39 is dominated by `Vec[Vec[i64]]`
growth and a path `clone()` at every solution leaf — `malloc`/`realloc`/`free` churn that
C/Rust/Go drive through the same allocator but with tighter per-object overhead. The headline
costs are structural, not a miscompile:

- **The residual is allocation churn.** Each `solve` allocates a fresh result vector and one
  fresh heap buffer per combination snapshot, all freed at the end of the iteration — the
  same per-step allocate-and-grow that #38's "residual 1.58× to C is now purely allocation"
  note identified. Closing it is the same deeper move (builder-buffer / arena reuse across
  iterations) and is left as identified headroom — **not** claimed until implemented and
  measured. This pass fixed the two **correctness** bugs above; no perf change was made or is
  claimed.
- **The overflow tax is ~zero.** `rustc -O` (40.3 ms) and `-C overflow-checks=on` (40.8 ms)
  are within ~1% — the hot path is pointer-chasing and `i64` adds well inside range, no
  arithmetic to check — so **equal-safety** Rust is 1.45× ahead, the same as unchecked. Rust
  (40.3 ms) edges C (43.1 ms) here on `Vec` ergonomics; Go (48.2 ms) sits between C and Kāra.

**No par lane — by construction.** The per-iteration solve is pure, but the checksum
reduction carries a loop-borne dependency, so karac's auto-par-on-reduction pass does not
fire: the default and `KARAC_AUTO_PAR=0` binaries are **byte-identical** and both run
single-threaded. (Fixing B-2026-06-18-10 was about the auto-par pass *mis-compiling* the
sorted solver's comparator, not about this bench parallelizing — it doesn't.)

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | **1.14 MiB** | 1.22 MiB | 1.20 MiB | 9.66 MiB |
| binary size (seq) | 33.3 KiB | 456.0 KiB | **32.8 KiB** | 2434.1 KiB |
| compile elapsed | 74.4 ms | 90.4 ms | **45.8 ms** |
| compile peak RSS | 13.7 MiB | 29.0 MiB | **2.5 MiB** |

The result vectors are freed each iteration, so steady-state RSS is allocator-bound and
tight: Kāra (**1.14 MiB**) is actually the lowest, with Rust (1.22) and C (1.20) within
rounding, while Go's runtime pays 9.66 MiB and Python's interpreter 6.8 MiB. The seq compute
binary references no par-scheduler runtime, so LTO + `-dead_strip` carve it to **33.3 KiB** —
13.7× under Rust and within a rounding of C's 32.8 KiB (Go's static runtime is 2.4 MiB).
Compile favours Kāra over `rustc -O` on both elapsed (74.4 vs 90.4 ms) and peak compiler RSS
(13.7 vs 29.0 MiB); clang's 45.8 ms / 2.5 MiB is the toolchain floor.

## Kāra features exercised

- **`Vec[Vec[i64]]` built by path snapshots** — the result is a nested Vec grown with
  `out.push(path.clone())` at each solution leaf; the `clone()` of a `mut ref Vec` receiver
  is the exact form surfaced (and fixed) as [`B-2026-06-18-9`](../../../../kara/docs/bug-ledger.jsonl).
- **`mut ref` accumulator + path threaded through recursion** — both `path` and `out` thread
  as `mut ref Vec[…]`; the root call writes the call-site markers (`mut path`, `mut out`)
  because they are fresh owned bindings there, and interior calls forward the already-mut-ref
  bindings unmarked, per the call-site-marker rule.
- **`Vec.push` / `Vec.pop` backtracking** — the ★ solver brackets every choice with
  `path.push(c)` / `path.pop()` so the parent's path is exactly restored on unwind.
- **`Vec.clone()` across owned and borrowed receivers** — the snapshot solver clones an owned
  `path`, the ★ and sorted solvers clone a `mut ref` one, exercising both clone-receiver
  codegen paths now that the borrowed path deep-copies.
- **`sort_by(|a, b| a.cmp(b))` + closure under auto-par** — the sorted solver's comparator,
  whose codegen under an auto-parallelized caller surfaced (and fixed)
  [`B-2026-06-18-10`](../../../../kara/docs/bug-ledger.jsonl).
- **Three factorings of one backtracker** — mutable-path, immutable-snapshot, and sorted
  early-break, all agreeing across the LeetCode examples under both `karac run` and
  `karac build`.

---

**Bug ledger:** [`B-2026-06-18-9`](../../../../kara/docs/bug-ledger.jsonl) (`kata:39`,
codegen, **fixed `c0432862`**) — `<expr>.clone()` on a `ref`/`mut ref` Vec receiver
shallow-aliased the source buffer instead of deep-copying (right combination count, empty
inner lists), though it ran correctly under the interpreter; the fix routes the receiver
through `get_data_ptr` to unwrap the borrow level.
[`B-2026-06-18-10`](../../../../kara/docs/bug-ledger.jsonl) (`kata:39`, codegen, **fixed
`c0432862`**) — an auto-parallelized `sort_by` comparator emitted a stray cancel-flag load
and failed module verification; the fix clears `branch_cancel_ptr` across each closure /
sort-helper body emission. See the [`karac` bug ledger](../../../../kara/docs/bug-ledger.jsonl).
