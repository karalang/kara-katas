# 31. Next Permutation

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array, Two Pointers &nbsp;·&nbsp; **Source:** [leetcode.com/problems/next-permutation](https://leetcode.com/problems/next-permutation/)

Rearrange `nums` into the **next** greater permutation in lexicographic order.
If `nums` is already the greatest arrangement (strictly descending), wrap it to
the least (fully ascending). The replacement must be done **in place** with only
constant extra memory.

```
[1, 2, 3]  →  [1, 3, 2]
[3, 2, 1]  →  [1, 2, 3]      (already greatest — wraps to least)
[1, 1, 5]  →  [1, 5, 1]
```

**Constraints:** `1 ≤ nums.length ≤ 100`; `0 ≤ nums[i] ≤ 100`.

## Why this kata — the in-place lexicographic step

The other end of the two-pointer in-place family from
[#27 remove-element](../27-remove-element/) and
[#88 merge-sorted-array](../88-merge-sorted-array/): those *compact* (a write
head chases a read head); this one *steps* — it computes the very next point in
the permutation lattice and resets the tail, all with O(1) scratch. The whole
thing is four pointer moves:

| Move | What | Why |
|---|---|---|
| **1. Pivot** | walk from the right while non-increasing; first `i` with `nums[i] < nums[i+1]` | the suffix `nums[i+1..]` is then the longest descending (= maximal) tail |
| **2. Wrap** | no pivot ⇒ array is fully descending (already greatest) | fall through to the reverse, which flips it to fully ascending |
| **3. Successor** | scan the descending suffix for the first `j` with `nums[j] > nums[i]`, swap | the smallest value still greater than the pivot — the minimal bump |
| **4. Reverse** | reverse the suffix `nums[i+1..]` (descending → ascending) | resets the tail to the smallest arrangement |

The insight worth internalizing: the suffix after the pivot is **already
sorted descending**, so move 3 has a sorted run to search and move 4 is a plain
two-pointer reverse — never a sort. That descending-suffix invariant is what the
binary-search variant below leans on.

## Approaches

Two styles, both byte-identical to the Python oracle across all 11 cases, under
`karac run` **and** `karac build`.

| Approach | File | Shape |
|---|---|---|
| **Linear successor scan** ★ | [`next_permutation.kara`](next_permutation.kara) | the canonical four-move: pivot, linear right-to-left scan for the successor, swap, two-pointer tail reverse |
| Binary-search successor | [`next_permutation_bsearch.kara`](next_permutation_bsearch.kara) | identical except the successor is found by **binary search** over the descending suffix — the predicate `nums[j] > nums[i]` is true on a prefix, so upper-mid bisection lands on its last true index |

Both are O(n) overall (the pivot find and the tail reverse dominate). The
binary-search style does not lower the complexity — it is the instructive
contrast: a successor lookup in a sorted run is exactly what binary search
answers, and the descending suffix hands that sorted run to you for free. The
linear scan is the tighter, branch-predictable inner loop; the bisection is the
one that *names* the invariant it depends on.

## What this kata uncovered

**Flat curve — no `karac` bug.** The whole four-move algorithm — the
non-increasing pivot scan, the `nums[i] <-> nums[j]` successor swap, and the
two-pointer tail reverse — compiled and ran first-try under **both** backends,
in both styles. The binary-search variant's upper-mid bisection
(`mid = lo + (hi - lo + 1) / 2`, the off-by-one-prone form that biases the
midpoint up to avoid an infinite loop when `hi = lo + 1`) was correct first-try
as well. This rides the same hardened `mut Slice[i64]` index/assign + `for`/`while`
+ `String` `push_str` surface that the two-pointer compaction katas
([#27](../27-remove-element/), [#88](../88-merge-sorted-array/)) and the radix
render katas ([#43](../43-multiply-strings/)) already cleared — nothing new for
the front-end or codegen to trip on.

## Benchmarks
<!-- bench-staleness -->
> **Figures in this section are undated; the feed was last measured 2026-06-16.** Where the two disagree, [`bench/results.json`](bench/results.json) and the [charts](../../../BENCHMARKS.md) are current; the numbers below are kept because the analysis around them explains *why* the shape is what it is, and that reasoning outlives the milliseconds.
> Comparative claims below ("ahead of C", "leads Rust", ratios) were true of the snapshot and have **not** been re-verified against the current feed — treat them as historical, not as the standing result.

Workload: start from the sorted array `[0, 1, …, 9]` and call `next_permutation`
`10!` times to walk **every** permutation of 10 elements in lexicographic order
(the `10!`-th call wraps back to sorted), folding a rolling checksum of each
permutation into one accumulator; the whole run is **`REPEAT = 8`** such full
enumerations — `8 · 10! ≈ 29M` in-place steps (sink `1352365570`). The checksum
is the un-elidable observation: every permutation must be produced *and* read in
order, so no comparator can fold the enumeration away. The enumeration carries a
hard loop-borne dependency (each permutation is computed in place from the
previous), so it does **not** auto-parallelize — a single-lane (seq) bench by
construction. Apple M5 Pro; `bench/bench.sh` (`hyperfine`).

### Seq lane — runtime (single-threaded permutation enumeration)

| | C | Rust (`-O`) | **Kāra** | Rust (`overflow-checks=on`) | Go | Python |
|---|---|---|---|---|---|---|
| time | 290.0 ms | 291.1 ms | **293.6 ms** | 296.5 ms | 322.3 ms | 16377 ms |
| vs Kāra | 1.01× faster | 1.01× faster | — | **1.00× (equal-safety parity)** | 1.10× slower | 56× slower |

**The compute-bound counterpoint to [#43](../43-multiply-strings/).** Multiply
Strings was allocation- *and* arithmetic-bound — a per-result `Vec[i64]` + a
growing `String`, where Kāra's small-object-allocation gap + checked-arith tax
put it at **1.37× Rust** at equal safety. Next Permutation removes both: the
array lives in a fixed `Array[i64, 10]`, the algorithm steps it **in place**, and
the only arithmetic is the bounded checksum (modulus `2^31 - 1`, nothing ever
near an overflow). The honest comparison is at equal safety: Kāra checks integer
overflow by default, and `rustc -O` *wraps*. With no heap traffic and no real
overflow-check pressure, **Kāra is dead even with Rust and C** — 293.6 ms vs
Rust's 291.1 ms (`-O`, wrap) and C's 290.0 ms, both ~1.01×, and at **equal overflow
safety it reaches parity** — 293.6 ms vs Rust's 296.5 ms with
`-C overflow-checks=on`, a 1.00× tie (Kāra a hair ahead, well inside the noise).
This is the honest flip side of #43: when the workload is pure in-place integer
compute rather than small-object allocation, the residual Kāra carries elsewhere
simply isn't there.

**No par lane — by construction.** The enumeration is inherently serial: each
permutation is derived in place from the one before it, so karac's
auto-par-on-reduction pass does not fire — verified here, the default and
`KARAC_AUTO_PAR=0` binaries agree on the sink and both run single-threaded
(cpu 99.6 %).

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | 1.03 MiB | 1.08 MiB | **1.00 MiB** | 2.86 MiB |
| binary size (seq) | **33.1 KiB** | 455.4 KiB | 32.8 KiB | 2434.1 KiB |
| compile elapsed | **77.9 ms** | 88.9 ms | 46.8 ms |
| compile peak RSS | **13.5 MiB** | 26.0 MiB | 2.6 MiB |

The no-allocation shape shows in memory too: Kāra's runtime RSS (1.03 MiB)
**ties C and Rust** to within rounding — the same flat-heap profile #43 now also
reaches on memory once its RC-aliasing slack was fixed. With
nothing on the heap, there is no slack to surface.

The binary is **33.1 KiB** — an order of magnitude under the ~295 KiB auto-par
floor and 13.8× smaller than Rust's 455 KiB: this seq compute binary references no
`String`/`Vec`/par-scheduler runtime symbol, so LTO + `-dead_strip` carve nearly
the whole runtime away (within 0.3 KiB of C's 32.8 KiB). Compile still favors
Kāra over `rustc -O` on both elapsed (77.9 vs 88.9 ms) and peak compiler RSS
(13.5 vs 26.0 MiB).

**Where this lands.** A pure in-place integer-compute kernel: Kāra ties Rust and
C on runtime (parity with checked-Rust at equal safety, 1.00×), ties them on
memory, and wins on binary size and compile. Paired with #43 it draws the line cleanly — Kāra's residual is
small-object allocation + checked arithmetic on hot allocation paths, and when a
workload touches neither, Kāra is right on the systems-language floor.

## Kāra features exercised

- **`mut Slice[i64]` two-pointer scans** — the non-increasing pivot walk, the
  right-to-left successor scan, and the converging-pointer tail reverse, all
  index/assign in place with no allocation.
- **Forward-without-marker call sites** — `report` forwards its in-scope
  `mut Slice` to `fmt`/`next_permutation` with no call-site marker (design.md
  Feature 4 Part 1½, Rule 2); `main` passes `mut a1` (a fresh owned `Array`) with
  the marker.
- **Upper-mid binary search** — the `bsearch` style's
  `mid = lo + (hi - lo + 1) / 2` bisection over the descending suffix, the
  bias-up form that terminates on the two-element window.
- **`String` accumulation render** — `fmt` builds `[a, b, c]` via `push_str(", ")`
  + `push_str(f"{nums[i]}")`, the amortized-O(1) in-place append (`String + String`
  does not typecheck; f-string self-append is O(n²) — see [#2](../2-add-two-numbers/)).

---

**Bug ledger:** flat curve — the two-pointer in-place + binary-search surface
produced no miscompile or front-end gap (no `B-ID` minted). See the
[`karac` bug ledger](../../../../kara/docs/bug-ledger.md).
