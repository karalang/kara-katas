# 53. Maximum Subarray

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Divide and Conquer · Dynamic Programming &nbsp;·&nbsp; **Source:** [leetcode.com/problems/maximum-subarray](https://leetcode.com/problems/maximum-subarray/)

Given an integer array `nums`, find the contiguous **subarray** (containing at least one number)
with the largest sum, and return that sum.

```
nums = [-2,1,-3,4,-1,2,1,-5,4]  →  6      the subarray [4,-1,2,1]
nums = [1]                       →  1
nums = [5,4,-1,7,8]              →  23     the whole array
nums = [-3,-2,-5,-1]             →  -1     all negative — the least-bad single element
```

**Constraints:** `1 ≤ nums.length ≤ 10⁵`, `−10⁴ ≤ nums[i] ≤ 10⁴`. LeetCode's follow-up asks for the
`O(n log n)` divide-and-conquer solution in addition to the `O(n)` one — this kata pins both, plus a
third `O(n)` framing.

## Why this kata — one number, three unrelated derivations

Maximum Subarray is the smallest problem where three genuinely different algorithmic ideas converge on
the *same* integer, and the kata is about seeing them as three views of one recurrence rather than
three tricks:

| Lens | State | The idea in one line |
|---|---|---|
| **Kadane (DP)** ★ | two scalars | best subarray ending *here* = `max(x, here + x)`; track the global best |
| **Prefix minus running min** | two scalars | `sum(i..j) = P[j+1] − P[i]`; best right-end = `P[j+1] − min(earlier prefixes)` |
| **Divide and conquer** | recursion | answer is `max(left, right, best-crossing-the-middle)` |

**Kadane** is the dynamic-programming face: a one-step recurrence on "the best run ending at `i`",
where a negative running total is simply dropped because a negative prefix can only hurt what follows.
**Prefix-min** is the same answer read off the *geometry* of the prefix-sum curve — the largest
subarray sum is the largest drop from a later prefix down to the lowest earlier one, so a single
left-to-right pass tracking the running minimum suffices. **Divide and conquer** is the recursive
face LeetCode names as its follow-up: the maximum subarray is entirely in the left half, entirely in
the right half, or it straddles the midpoint — and the straddling case is the only one the split
cannot delegate, solved by scanning outward from the middle for the best suffix + best prefix.

**The shared correctness pin — the empty subarray is not allowed.** All three must return `-1` on
`[-3,-2,-5,-1]`, not `0`. That single rule is what forces each solver's seeding:

- **Kadane** seeds `best` and `here` with `nums[0]` and sweeps from index 1, so `best` can never fall
  back to "take nothing".
- **Prefix-min** would happily report `0` (subtract a prefix from itself) if it let the subarray be
  empty; it seeds `best = nums[0]` and scores each right-end against the minimum of *strictly earlier*
  prefixes, keeping every candidate subarray non-empty.
- **Divide and conquer** never even represents the empty subarray: the base case `lo == hi` returns
  the lone element, and `best_cross` seeds both halves with the two midpoint cells a straddling
  subarray is required to contain.

Three seedings, one rule — that convergence is the kata.

### The prefix-sum identity, spelled out

Let `P[0] = 0` and `P[k] = nums[0] + … + nums[k-1]`. Then `sum(nums[i..j]) = P[j+1] − P[i]`, so for a
fixed right end the best sum is `P[j+1] − min(P[0..j])`. Sweeping once while maintaining the running
prefix and the running minimum of all *earlier* prefixes turns that into an `O(1)`-space scan — the
same asymptotics as Kadane, derived from a completely different starting point. The "earlier" ordering
(score first, then fold the current prefix into the minimum) is exactly what keeps the chosen subarray
non-empty.

## Approaches

| Approach | File | Time · Space | Answer via |
|---|---|---|---|
| **Kadane (DP)** ★ | [`kadane.kara`](kadane.kara) | `O(n)` · `O(1)` | running `here`/`best` recurrence |
| **Prefix minus running min** | [`prefix_min.kara`](prefix_min.kara) | `O(n)` · `O(1)` | `P[j+1] − min earlier prefix` |
| **Divide and conquer** | [`divide_conquer.kara`](divide_conquer.kara) | `O(n log n)` · `O(log n)` | `max(left, right, cross)` |
| Oracle | [`maximum_subarray.py`](maximum_subarray.py) | `O(n)` | mirrors the ★ solver + identical output format |

All three `.kara` files share a line-for-line-identical test harness (12 cases spanning mixed,
all-positive, all-negative, single-element and zero-crossing arrays, one answer per line plus a
`sums:` summary) and diff byte-for-byte against the Python oracle under `karac run`, `karac build`,
and the default auto-par build.

## What this kata surfaced

A **clean pass** — like [#51 N-Queens](../51-n-queens/), all three solvers compiled and produced the
oracle's output byte-for-byte on the first A/B run across `karac run`, `karac build`
(`KARAC_AUTO_PAR=0`), and the default auto-par build. No compiler gap turned up.

The three exercises that could plausibly have snagged — a `mut ref String` accumulator threaded
through a helper (the same forwarded-`mut ref` shape that hid
[B-2026-07-03-13](../../../../kara/docs/bug-ledger.md) in [#52](../52-n-queens-ii/), here on a heap
`String` instead of an `i64`), a doubly-recursive `dc` returning by value, and negative `i64` array
literals fed through `Slice[i64]` — each behaved correctly on all three surfaces. The auto-par build in
particular did *not* mis-parallelize `divide_conquer`'s two recursive calls (contrast
[B-2026-07-03-14](../../../../kara/docs/bug-ledger.md), where a return-value reduction whose delta
recursed crashed under auto-par): the D&C combine is `max(l, r, c)`, not a `+`-reduction, so the
reduction analyzer never engaged it.

## Kāra features exercised

- **Two-scalar `O(1)` DP scan** — Kadane's `here = max(x, here + x)` / `best = max(best, here)`, no
  allocation, the running-value idiom kata [#42](../42-trapping-rain-water/) leans on.
- **Prefix-sum reframing** — `P[j+1] − min earlier prefix` as an equivalent `O(1)`-space single pass.
- **Doubly-recursive divide and conquer over index ranges** — `dc(lo, hi)` splitting at an
  overflow-safe midpoint and recombining with a linear `best_cross` scan.
- **`Slice[i64]` from `Array[i64, N]`** carrying negative literals, passed down recursion unchanged.
- **`mut ref String` accumulator** threaded through a shared `report` helper to fold the per-case
  answers into one summary line.

## Benchmarks

```bash
brew install hyperfine    # one-time, also needs rustc (rustup), clang, go, karac
./bench/bench.sh          # KARA_BENCH_INCLUDE_PY=1 to include the Python row
```

`bench/bench.sh` builds the Rust file with `rustc -O`, the C file with `clang -O3`, the Kāra file
with `karac build` (`KARAC_AUTO_PAR=0`), and the Go module with `go build` (all cached in
`bench/target/`, gitignored), then times them with `hyperfine` per the
[BENCH.md protocol](../../../BENCH.md) and writes [`bench/results.json`](bench/results.json).

| File | What it does |
|---|---|
| [`bench/maxsub_bench.kara`](bench/maxsub_bench.kara) | **Kadane kernel** over 120 000 LCG-generated length-1000 arrays, one `i64` sink |
| [`bench/maxsub_bench.rs`](bench/maxsub_bench.rs) | mirror; `rustc -O` |
| [`bench/maxsub_bench.c`](bench/maxsub_bench.c) | mirror; `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | mirror; `go build` |
| [`bench/maxsub_bench.py`](bench/maxsub_bench.py) | mirror; CPython |

**Workload.** A deterministic LCG (the classic glibc recurrence, `state ← (1103515245·state + 12345)
mod 2³¹`) streams pseudo-random values in `[-50, 49]` straight into Kadane's `(here, best)` recurrence,
restarting every 1000 elements to simulate a length-1000 input array, and folding each array's answer
into one `i64` sink. So the benchmark is literally "solve Maximum Subarray on a batch of 120 000
arrays" — the ★ solver's kernel — with **no allocation**: elements are generated inline, never stored.
Everything is overflow-safe by construction (Kāra **traps on `i64` overflow** by default —
[design.md § Arithmetic Overflow](../../../../kara/docs/design.md)): `state < 2³¹` keeps the product
`1103515245·state < 2⁶¹` inside `i64`, and the fold of 120 000 array-answers stays far below `i64`.
The generator is integer-only and identical across languages, so the sink folds to one **bit-exact,
cross-language-diffable** value (`111687926`) that every language prints identically.

### Runtime

Snapshot — M5 Pro, 2026-07-03, hyperfine `--warmup 5 --runs 30`, means:

| Implementation | Wall time | User-CPU |
|---|---|---|
| **`kara maxsub_bench`** (codegen, seq) | **154.4 ms ± 2.1 ms** | 152.2 ms |
| `c    maxsub_bench` (clang -O3) | 155.0 ms ± 1.8 ms | 152.4 ms |
| `rust maxsub_bench` (rustc -O) | 155.1 ms ± 1.4 ms | 152.9 ms |
| `rust maxsub_bench` (`-C overflow-checks=on`) | 155.8 ms ± 1.1 ms | 153.4 ms |
| `go   maxsub_bench` (go build) | 330.8 ms ± 4.0 ms | 326.2 ms |
| `py   maxsub_bench` (CPython) | 13448 ms | — |

**This kernel is a three-way tie at the noise floor — and Kāra is in it with overflow checks on.** The
hot path per element is a multiply (`state·1103515245`), two modulos (`mod 2³¹` and `mod 100`), a
subtract, and Kadane's compare-select — dominated by the two modulos and the multiply. Kāra **traps on
integer overflow by default** ([design.md § Arithmetic Overflow](../../../../kara/docs/design.md));
`rustc -O`, C, and Go all **silently wrap**. Yet the overflow checks Kāra inserts on the multiply and
the adds are cheap enough to hide under the modulo latency, so the default-safe build lands
**154.4 ms — level with unsafe `clang -O3` (155.0) and `rustc -O` (155.1), and a hair ahead of
safety-matched Rust** (`-C overflow-checks=on`, 155.8 ms). All four sit inside ~1.5 ms of each other,
well under a single run's noise. Kāra is **2.14× faster than Go** (330.8 ms) and **~87× faster than
CPython**.

Contrast [#52](../52-n-queens-ii/), where the shift/mask-heavy backtracker left Kāra's overflow checks
exposed and the default-safe build trailed `rustc -O`'s silent-wraparound by ~2×. The difference is
purely where the checks fall: under a modulo they are free; on a bare shift-and-mask kernel they cost.
On this arithmetic kernel Kāra's default-safe output is indistinguishable from what the wrapping
compilers ship.

### Compile time, binary size, memory

Snapshot — M5 Pro, 2026-07-03, hyperfine `--warmup 1 --runs 10` (compile, cold via `--prepare`);
size and peak RSS are single deterministic samples.

| Compiler | Compile (cold) | Binary | Peak RSS |
|---|---|---|---|
| `clang -O3` | 81.8 ms | 32.7 KiB | 1.00 MiB |
| `rustc -O` | 74.9 ms | 455.4 KiB | 1.05 MiB |
| **`karac build`** | **75.2 ms** | **33.0 KiB** | **1.02 MiB** |
| `go build` | — (excluded; mixes module + std-lib link) | 2434.1 KiB | 2.58 MiB |

Kāra emits a binary **~14× smaller than Rust** and line-ball with C (33.0 vs 32.7 KiB), and ties C and
Rust for peak RSS (~1.0 MiB, ~2.5× under Go and ~6.6× under CPython). Its cold compile is on par with
`rustc -O` (75.2 vs 74.9 ms) and edges `clang` on this run (whose 81.8 ms ± 18.8 ms was unusually
noisy). Every figure lands within noise of [#52](../52-n-queens-ii/)'s — the two katas compile the
same shape of tiny integer kernel.
