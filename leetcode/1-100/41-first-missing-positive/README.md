# 41. First Missing Positive

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Array, Hash Table &nbsp;·&nbsp; **Source:** [leetcode.com/problems/first-missing-positive](https://leetcode.com/problems/first-missing-positive/)

Given an unsorted integer array, return the smallest **positive** integer that is **not**
present — in **O(n) time and O(1) auxiliary space**.

```
[1,2,0]        →  3
[3,4,-1,1]     →  2
[7,8,9,11,12]  →  1
```

**Constraints:** `1 ≤ nums.length ≤ 10⁵`, `-2³¹ ≤ nums[i] ≤ 2³¹-1`. The answer is always in
`[1, n+1]`: a length-`n` array holds at most `n` distinct positives `1..n`, so either some
value in `1..n` is missing (the smallest such gap) or all are present and the answer is
`n+1`. Values `≤ 0` and `> n` are irrelevant — they can never be the answer.

## Why this kata — the array *is* the hash table

After the heap-allocating backtrackers [#39](../39-combination-sum/)/[#40](../40-combination-sum-ii/)
(`Vec[Vec]` growth), #41 is the deliberate swing back to **allocation-free in-place integer
compute** — the [#36](../36-valid-sudoku/)/[#37](../37-sudoku-solver/) footing. The O(1)-space
constraint is the whole puzzle: with no room for a separate hash set, you must **use the
input array itself as the presence table**, keyed by value. Two canonical ways to do that —
permute values to their home slots, or overload each slot's *sign* as a present-bit — plus
the O(n)-space boolean table you'd write first, give three distinct factorings.

| Lens | Idea |
|---|---|
| **Cyclic sort** ★ | the home of value `v` is index `v-1`; swap each in-range value home (`while nums[nums[i]-1] != nums[i]`), then the first slot not holding its home is the gap |
| **Sign marking** | neutralize out-of-range values to `n+1`, then for each magnitude `v` make `nums[v-1]` negative; the first still-positive slot's index+1 is the answer |
| **Boolean seen-table** | the O(n)-space baseline — mark `seen[v]` for in-range `v`, return the first unseen value; leaves the input intact |

The cyclic sort's `nums[v-1] != v` guard is what keeps it O(n), not O(n²): a swap fires only
when it moves a value to a home that doesn't already hold it, so each swap places one value
permanently — at most `n` swaps total even though the cursor `i` may sit still across several.
Sign marking does strictly linear passes (no inner re-examination) at the cost of clobbering
the values' signs. Both are O(1) auxiliary space; the seen-table trades O(n) space for the
simplest possible reasoning and an untouched input.

## Approaches

Three styles, all agreeing with the Python oracle for the LeetCode examples under `karac run`
**and** `karac build`.

| Approach | File | Shape |
|---|---|---|
| **Cyclic sort** ★ | [`first_missing_positive.kara`](first_missing_positive.kara) | `mut Slice[i64]`, swap to home index `v-1`, scan for the first mismatch |
| Sign marking | [`first_missing_positive_sign.kara`](first_missing_positive_sign.kara) | neutralize to `n+1`, negate `nums[v-1]` as a present-bit, first positive slot wins |
| Boolean seen-table | [`first_missing_positive_seen.kara`](first_missing_positive_seen.kara) | `Vec[bool]` of size `n+1`, mark + scan; input read-only via `Slice[i64]` |

The cyclic sort and sign-marking forms are allocation-free (in-place on the input
`mut Slice[i64]`); the seen-table is the O(n)-space contrast that exercises `Vec[bool]`
allocation + indexed read/write instead of in-place swaps.

## What this kata surfaced

**An `Array[T, N]` passed to a `ref Slice[T]` param segfaulted under `karac build`**
([`B-2026-06-19-1`](../../../../kara/docs/bug-ledger.jsonl), `kata:41`, codegen, **fixed
[`6d207a7e`](../../../../kara/docs/bug-ledger.jsonl)**). The seen-table solver reads its
input without mutating it, so its natural parameter is a read-only slice view. Probing the
parameter forms, `ref Slice[i64]` (a documented mode — design.md § Slices,
`fn average[T: Numeric](xs: ref Slice[T])`) fed an `Array` literal **typechecked, ran
correctly under the interpreter, and segfaulted when built**. `extract_slice_elem_type`
returned `None` through the `TypeKind::Ref` wrapper, so `ref Slice[T]` was classified as a
bare ref param; the call site's `get_data_ptr` identifier fast-path then passed the array's
**raw element storage** as the slice argument, and the callee read `{ptr,len}` out of the
first two elements (`ptr = elem0`, `len = elem1`) — a bogus slice → out-of-bounds / crash. A
`Vec` source accidentally survived (its `{ptr,len,cap}` storage *starts* with `{ptr,len}`);
only an `Array`'s storage lacks the header.

**The fix synthesizes a real slice header for the Array.** `extract_slice_elem_type` now
peels one `Ref`/`MutRef` around a `Slice`/`MutSlice`, and the call path, for a `ref Slice`
param whose argument is an `Array` binding, builds the `{ptr,len}` header via
`coerce_to_slice` and passes a pointer to it — the same shape the rvalue path already used
for `v.as_slice()`. It is narrowed to `Array` sources so a *forwarded* ref-slice binding
keeps using `get_data_ptr` (re-coercing it corrupted the forward — caught and fixed during
the change). Regression test `test_e2e_array_arg_to_ref_slice_param` covers the direct call,
the forward, and the seen-shape (`ref Slice` forward + `Vec[bool]` indexed by a slice value);
full codegen (1618) / ASAN (264) / Linux LSan (slice) / par_codegen (121) green.

**The kata ships the idiomatic form.** The read-only slice view in Kāra is the bare
`Slice[i64]` (already a borrow handle — `ref Slice` is the rarer reference-to-a-borrow), and
the corpus convention is bare `Slice`, which always built correctly. So all three solvers
use `Slice[i64]` / `mut Slice[i64]`; `ref Slice` was a probe that turned up a latent
soundness hole, now closed for every caller.

## Benchmarks

Workload: a reused length-`N=100` buffer is refilled each iteration with a `k`-rotated
permutation of `1..N`, one slot is punched out of range to create a `k`-dependent gap, and
the ★ cyclic sort finds the missing positive. **`TOTAL = 200000`** times, fold the answer
into a rolling checksum (sink `783878544`). The buffer is allocated **once** and overwritten
in place every iteration — the hot loop allocates nothing — so this is **allocation-free**
integer compute, the in-place-array counterpart to #38/#39/#40's heap work. The gap location
varies with the loop index (no hoisting) and the checksum carries a loop-borne dependency, so
it is a single-lane (seq) bench by construction. Apple M5 Pro; `bench/bench.sh` (`hyperfine`).

### Seq lane — runtime (single-threaded in-place cyclic sort)

| | Rust (`overflow-checks=on`) | **Kāra** | C | Rust (`-O`) | Go | Python |
|---|---|---|---|---|---|---|
| time | 51.4 ms | **52.1 ms** | 52.4 ms | 54.8 ms | 59.9 ms | 1603 ms |
| vs Kāra | 1.01× faster (= safety) | — | 1.01× slower | 1.05× slower | 1.15× slower | 30.8× slower |

**On allocation-free compute Kāra is in a dead heat with the C-class — and ties equal-safety
Rust.** This is the #36/#37 result, not the #39/#40 one: with no `malloc`/`free` in the hot
loop, the gap that allocation churn opened in the backtracking katas closes entirely. Kāra
(52.1 ms) lands between `rustc -C overflow-checks=on` (51.4 ms) and C (52.4 ms) — all three
within ~2% — and **ahead** of unchecked `rustc -O` (54.8 ms) and Go (59.9 ms).

- **Equal safety is free here.** Kāra checks arithmetic by default; the apples-to-apples
  comparator is `rustc -C overflow-checks=on` (51.4 ms), which **ties** Kāra (52.1 ms) to
  within 1%. That unchecked `rustc -O` (54.8 ms) is actually *slower* than its checked
  sibling is codegen noise on this swap-and-scan loop (the modulus keeps every value in
  range, so neither traps) — the takeaway is that the checked/unchecked spread is ~6% and
  Kāra sits inside it. No allocation, no String, no `Vec[Vec]` — just indexed loads, compares,
  and swaps, which Kāra lowers as tightly as clang.
- **The residual to clang is compile-time, not runtime.** Runtime is a three-way tie;
  `clang -O3` only leads on *build* speed (45.3 ms, the toolchain floor).

**No par lane — by construction.** The per-iteration solve is pure, but the checksum
reduction carries a loop-borne dependency, so karac's auto-par pass does not fire: the default
and `KARAC_AUTO_PAR=0` binaries are **byte-identical** and both run single-threaded.

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | **1.00 MiB** | 1.05 MiB | 1.00 MiB | 2.67 MiB |
| binary size (seq) | 33.4 KiB | 455.4 KiB | **32.7 KiB** | 2434.1 KiB |
| compile elapsed | 72.4 ms | 84.8 ms | **45.3 ms** |
| compile peak RSS | 13.1 MiB | 27.8 MiB | **2.5 MiB** |

A single 100-element buffer means runtime RSS is tiny and allocator-bound: Kāra and C tie at
**1.00 MiB** (byte-for-byte equal peak), Rust within rounding at 1.05 MiB, while Go's runtime
pays 2.67 MiB and Python's interpreter 6.8 MiB. The seq compute binary references no
par-scheduler runtime, so LTO + `-dead_strip` carve it to **33.4 KiB** — 13.6× under Rust and
within a rounding of C's 32.7 KiB. Compile favours Kāra over `rustc -O` on both elapsed (72.4
vs 84.8 ms) and peak compiler RSS (13.1 vs 27.8 MiB); clang's 45.3 ms / 2.5 MiB is the floor.

## Kāra features exercised

- **In-place `mut Slice[i64]` swaps** — the cyclic-sort and sign-marking solvers mutate the
  input array through a `mut Slice` view, with `nums[v-1]` computed-index reads/writes and
  three-line swaps, no auxiliary allocation.
- **Read-only `Slice[i64]` view** — the seen-table solver takes a shared `Slice[i64]` (the
  idiomatic borrowed view; bare, no `ref`) since it never writes; probing the `ref Slice`
  alternative surfaced (and fixed) [`B-2026-06-19-1`](../../../../kara/docs/bug-ledger.jsonl).
- **`Vec[bool]` presence table** — the seen-table allocates, fills, and indexes a `Vec[bool]`
  of size `n+1`, the allocating contrast to the in-place pair.
- **Checked integer arithmetic at C speed** — index math, negation (sign marking), and the
  checksum fold all run under Kāra's default overflow checking, matching
  `rustc -C overflow-checks=on` to within 1%.
- **Three factorings of one O(n) idea** — cyclic sort, sign marking, and a boolean seen-table,
  all agreeing across the LeetCode examples under both `karac run` and `karac build`.

---

**Bug ledger:** [`B-2026-06-19-1`](../../../../kara/docs/bug-ledger.jsonl) (`kata:41`,
codegen, **fixed `6d207a7e`**) — an `Array[T, N]` passed to a `ref Slice[T]` param had its raw
element storage passed as a bogus `{ptr,len}` slice header (segfault), though it ran correctly
under the interpreter; the fix peels the `Ref` in `extract_slice_elem_type` and synthesizes a
real slice header for Array arguments at the call site. See the
[`karac` bug ledger](../../../../kara/docs/bug-ledger.jsonl).
