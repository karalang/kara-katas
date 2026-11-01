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
Measured 2026-10-31 (`measured_at` 2026-11-01T02:03Z) with karac `g6697158fa` (v2/MIR
backend).

### Seq lane — runtime (single-threaded in-place cyclic sort)

| | Rust (`overflow-checks=on`) | C | Rust (`-O`) | **Kāra** | Go | Python |
|---|---|---|---|---|---|---|
| time | 54.5 ± 1.0 ms | 56.1 ± 1.3 ms | 59.4 ± 2.3 ms | **61.3 ± 1.1 ms** | 63.1 ± 1.2 ms | 1603 ms (last measured 2026-06-19, not re-run) |
| vs Kāra | 1.12× faster (= safety) | 1.09× faster | 1.03× faster | — | 1.03× slower | 30.8× slower (2026-06-19 ratio) |

**On allocation-free compute Kāra stays in the C-class pack, now at its back rather than its
middle.** This is still the #36/#37 result, not the #39/#40 one: with no `malloc`/`free` in the
hot loop, the large gap that allocation churn opened in the backtracking katas does not appear.
Kāra (61.3 ms) is 1.03× unchecked `rustc -O`, 1.09× C, and 1.03× *ahead* of Go. Against the
previous (2026-06-19, legacy-backend) run that is near flat: Kāra/Rust 0.95× → 1.03×, Kāra/C
1.00× → 1.09×, Kāra/Go 0.87× → 0.97×.

- **The equal-safety comparator moved most.** Kāra checks arithmetic by default; the
  apples-to-apples comparator is `rustc -C overflow-checks=on` (54.5 ms), which went from tying
  Kāra (1.01×) to leading it by 1.12×. As before, checked Rust is *faster* than its unchecked
  `rustc -O` sibling (54.5 vs 59.4 ms) — codegen noise on this swap-and-scan loop (the modulus
  keeps every value in range, so neither traps); the checked/unchecked spread is ~9%, and Kāra
  now sits just outside it. No allocation, no String, no `Vec[Vec]` — just indexed loads,
  compares, and swaps.
- **Compile is no longer a Kāra win.** `clang -O3` is the build-speed floor (50.1 ms) and
  `rustc -O` (93.5 ms) now builds faster than `karac` (114.8 ms) — see the table below.

**No par lane — by construction.** The per-iteration solve is pure, but the checksum
reduction carries a loop-borne dependency, so karac's auto-par pass does not fire: neither the
default nor the `KARAC_AUTO_PAR=0` build's emitted IR (`KARAC_MIR_LL`) contains a call of
`karac_mir_task_spawn`, and the two binaries are **byte-identical** (re-checked with karac
`g6697158fa`); both run single-threaded.

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | 1.05 MiB | 1.06 MiB | **1.02 MiB** | 2.69 MiB |
| binary size (seq) | 295.8 KiB | 455.4 KiB | **32.7 KiB** | 2434.1 KiB |
| compile elapsed | 114.8 ms | 93.5 ms | **50.1 ms** |
| compile peak RSS | 56.4 MiB | 27.7 MiB | **2.5 MiB** |

A single 100-element buffer means runtime RSS is tiny and allocator-bound: C peaks at
**1.02 MiB**, Kāra at 1.05 MiB (32 KiB over C) and Rust at 1.06 MiB, while Go's runtime pays
2.69 MiB and Python's interpreter 6.8 MiB (last measured 2026-06-19, not re-run). The Kāra
binary is **295.8 KiB** — 1.5× under Rust's 455.4 KiB but 9× C's 32.7 KiB; every MIR-backend
Kāra binary is ~300–390 KB where the legacy backend's were ~34 KB (tracked as
[`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md)). Compile now favours `rustc -O` over
`karac` on both elapsed (93.5 vs 114.8 ms) and peak compiler RSS (27.7 vs 56.4 MiB); clang's
50.1 ms / 2.5 MiB is the floor.

## Kāra features exercised

- **In-place `mut Slice[i64]` swaps** — the cyclic-sort and sign-marking solvers mutate the
  input array through a `mut Slice` view, with `nums[v-1]` computed-index reads/writes and
  three-line swaps, no auxiliary allocation.
- **Read-only `Slice[i64]` view** — the seen-table solver takes a shared `Slice[i64]` (the
  idiomatic borrowed view; bare, no `ref`) since it never writes; probing the `ref Slice`
  alternative surfaced (and fixed) [`B-2026-06-19-1`](../../../../kara/docs/bug-ledger.jsonl).
- **`Vec[bool]` presence table** — the seen-table allocates, fills, and indexes a `Vec[bool]`
  of size `n+1`, the allocating contrast to the in-place pair.
- **Checked integer arithmetic near C speed** — index math, negation (sign marking), and the
  checksum fold all run under Kāra's default overflow checking, within 1.12× of
  `rustc -C overflow-checks=on` and 1.09× of C.
- **Three factorings of one O(n) idea** — cyclic sort, sign marking, and a boolean seen-table,
  all agreeing across the LeetCode examples under both `karac run` and `karac build`.

---

**Bug ledger:** [`B-2026-06-19-1`](../../../../kara/docs/bug-ledger.jsonl) (`kata:41`,
codegen, **fixed `6d207a7e`**) — an `Array[T, N]` passed to a `ref Slice[T]` param had its raw
element storage passed as a bogus `{ptr,len}` slice header (segfault), though it ran correctly
under the interpreter; the fix peels the `Ref` in `extract_slice_elem_type` and synthesizes a
real slice header for Array arguments at the call site. See the
[`karac` bug ledger](../../../../kara/docs/bug-ledger.jsonl).
