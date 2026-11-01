# 45. Jump Game II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array, Dynamic Programming, Greedy &nbsp;·&nbsp; **Source:** [leetcode.com/problems/jump-game-ii](https://leetcode.com/problems/jump-game-ii/)

From index 0, `nums[i]` is the maximum forward jump length from `i`. Return the **minimum**
number of jumps to reach the last index. The input is generated so the last index is always
reachable.

```
[2,3,1,1,4]  →  2   (0 → idx1 → last)
[2,3,0,1,4]  →  2
```

**Constraints:** `1 ≤ n ≤ 10⁴`, `0 ≤ nums[i] ≤ 1000`, and the last index is always reachable.
This is the optimization sibling of [#55 Jump Game](https://leetcode.com/problems/jump-game/),
which asks only *whether* the end is reachable; here we count the fewest hops. The jump count
never exceeds `n-1`, so every value stays far inside `i64`.

## Why this kata — minimum jumps as implicit-BFS layers

The minimum number of jumps equals the number of **BFS layers** in the implicit graph
"`i → any j in (i, i+nums[i]]`": layer 0 is `{0}`, and layer `k+1` is every new index first
reachable from layer `k`. The first time BFS touches an index, it does so in the fewest jumps.
The three canonical solvers are three factorings of that single fact — collapse the layers,
walk them explicitly, or drop the shortcut and write the full recurrence:

| Lens | Idea |
|---|---|
| **Greedy range expansion** ★ | one scan with `farthest` (running max of `i+nums[i]`) and `current_end` (the current layer's right edge); reaching `current_end` spends a jump and extends it to `farthest` — O(n) time, O(1) space |
| **Explicit BFS layers** | keep the current layer as an index window `[lo, hi]`, sweep it for the farthest reach to get the next window `[hi+1, next_hi]`, one jump per layer — O(n) time, O(1) space |
| **Bottom-up DP** | `dp[j]` = min jumps to reach `j`; relax forward from each reached `i` over `(i, i+nums[i]]` — O(n²) time, O(n) space |

The greedy file is the layered BFS with the layer boundaries *folded into a single scalar*
(`current_end`); the BFS file keeps those boundaries **visible** as an index window; the DP file
discards the "first arrival is cheapest" shortcut and makes the relaxation recurrence literal,
paying O(n²) for it. It is the same in-place-scan footing as
[#41](../41-first-missing-positive/) and [#42](../42-trapping-rain-water/), here over a
shortest-path-by-layers relation.

## Approaches

Three styles, all agreeing with the Python oracle for the LeetCode examples under `karac run`
**and** `karac build`.

| Approach | File | Shape |
|---|---|---|
| **Greedy range expansion** ★ | [`jump_game_ii.kara`](jump_game_ii.kara) | `Slice[i64]`, three i64 scalars (`jumps`/`current_end`/`farthest`), one linear pass, no allocation |
| Explicit BFS layers | [`jump_game_ii_bfs.kara`](jump_game_ii_bfs.kara) | `Slice[i64]`, a `[lo, hi]` index window swept per layer, four scalars, no allocation |
| Bottom-up DP | [`jump_game_ii_dp.kara`](jump_game_ii_dp.kara) | one `Vec[i64]` of length n seeded to an `n+1` sentinel, forward relaxation |

The greedy and BFS forms are both allocation-free (a read-only `Slice[i64]` view + scalars) and
O(n); they differ only in whether the layer boundary is a single scalar or an explicit window.
The DP form allocates one `Vec[i64]` and pays O(n²) — the literal-recurrence contrast, the same
table-vs-scan trade as [#42](../42-trapping-rain-water/).

## What this kata surfaced

**No compiler change was needed — all three solvers typechecked, ran, and built correctly on
the first pass,** and all three agree with the Python oracle under both `karac run` and
`karac build`. There is no codegen drama to report either: unlike [#42](../42-trapping-rain-water/),
whose converging-pointer branch the stock `-O` backends pessimize into a latency-bound `csel`
chain, #45's greedy scan is a plain forward sweep with two cheap, well-predicted branches
(`i + nums[i] > farthest` and `i == current_end`). Every compiler lowers it the same obvious
way, so the benchmark is the corpus's quiet baseline case: **Kāra lands dead-even with C, Go,
and the equal-safety Rust comparator on a tight scalar loop**, with the differences inside
run-to-run noise (§ Benchmarks). That parity-with-no-asterisk is itself the finding here.

## Benchmarks

Workload: a reachable length-`N=1000` array `nums` (entries `1 + i%4`, so every index can always
step at least one forward and the answer is well-defined under every punch) is built **once**,
then **`TOTAL = 200000`** times a single slot is punched (`nums[k%n] = 1 + k%9`, a wider reach
that shortens some jumps). The punch is **not reverted**, so the array state carries forward, the
★ greedy solve runs over the evolving array, and each jump count is folded into a rolling
checksum (sink `92502267`). The per-iteration cost is therefore the **greedy min-jumps scan
itself**, not an O(n) refill — the hot loop **allocates nothing**, the answer varies with the
loop index (no hoisting), and the checksum carries a loop-borne dependency, so this is a
single-lane (seq) bench by construction. Apple M5 Pro; `bench/bench.sh` (`hyperfine`).
Measured 2026-10-31 (`measured_at` 2026-11-01T02:07Z) with karac `g6697158fa` (v2/MIR
backend).

### Seq lane — runtime (single-threaded greedy range expansion)

| | Rust (`overflow-checks=on`) | Go | C | Rust (`-O`) | **Kāra** | Python |
|---|---|---|---|---|---|---|
| time | 101.7 ± 1.2 ms | 103.2 ± 2.9 ms | 108.0 ± 1.8 ms | 109.7 ± 1.9 ms | **112.8 ± 4.6 ms** | 6680 ms (last measured 2026-06-19, not re-run) |
| vs Kāra | 1.11× faster (= safety) | 1.09× faster | 1.04× faster | 1.03× faster | — | 64.4× slower (2026-06-19 ratio) |

**Kāra is near parity** — C and `rustc -O` land within ~4% of it, Go and the equal-safety
comparator within ~11% (Kāra's own run-to-run σ is ±4.6 ms). Against the previous
(2026-06-19, legacy-backend) run this is flat: Kāra/Rust 1.04× → 1.03×, Kāra/C 1.01× → 1.04×,
Kāra/Go 1.03× → 1.09×. The one comparator that moved is checked Rust: `rustc -C
overflow-checks=on` (101.7 ms) was ~3% *slower* than plain `rustc -O` last time and is now
~7% *faster* than it, so Kāra/checked-Rust went 1.01× → 1.11× while Kāra held steady against
unchecked Rust. On a branch-predictable forward scalar loop there is no safety tax to isolate
— the checked and unchecked Rust builds trade places run to run — and no codegen choice to
diverge on. Python runs the identical algorithm interpreted, 64× behind (2026-06-19 run, not
re-run).

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | **1.03 MiB** | 1.08 MiB | **1.03 MiB** | 2.56 MiB |
| binary size (seq) | 295.8 KiB | 455.4 KiB | **32.7 KiB** | 2434.1 KiB |
| compile elapsed | 113.9 ms | 88.4 ms | **44.5 ms** |
| compile peak RSS | 56.7 MiB | 28.7 MiB | **2.6 MiB** |

A single 1000-element `i64` buffer means runtime RSS is tiny and allocator-bound: Kāra and C
tie at **1.03 MiB** (1 081 680 vs 1 081 656 bytes, 24 bytes apart), Rust within rounding at
1.08 MiB, while Go's runtime pays 2.56 MiB and Python's interpreter 6.8 MiB (last measured
2026-06-19, not re-run). The Kāra binary is **295.8 KiB** — 1.5× under Rust's 455.4 KiB but 9×
C's 32.7 KiB; every MIR-backend Kāra binary is ~300–390 KB where the legacy backend's were
~34 KB (tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md)). Compile now favours
`rustc -O` over `karac` on both elapsed (88.4 vs 113.9 ms) and peak compiler RSS (28.7 vs
56.7 MiB); clang's 44.5 ms / 2.6 MiB is the floor.

**No par lane — by construction.** The per-iteration solve is pure, but the checksum reduction
carries a loop-borne dependency, so karac's auto-par pass does not fire: neither the default
nor the `KARAC_AUTO_PAR=0` build's emitted IR (`KARAC_MIR_LL`) contains a call of
`karac_mir_task_spawn`, and the two binaries are **byte-identical** (re-checked with karac
`g6697158fa`); both run single-threaded.

## Kāra features exercised

- **Read-only `Slice[i64]` view** — both the ★ greedy and the BFS solver take the input as a
  bare `Slice[i64]` (the idiomatic borrowed view) since they never write, walking it with a
  handful of i64 scalars and no allocation, the in-place-scan footing of
  [#41](../41-first-missing-positive/) and [#42](../42-trapping-rain-water/).
- **`Vec[i64]` DP table with a sentinel** — the DP solver allocates one `Vec[i64]` of length n,
  seeds it to an `n+1` "infinity" sentinel, and relaxes it forward by computed index, the
  allocating contrast to the scalar scans.
- **Sliding index window** — the BFS solver advances a `[lo, hi]` layer window and sweeps it
  with a nested loop that still totals one linear pass (`lo` chases `hi+1`).
- **Checked integer arithmetic that ties C-class** — the index math, the `i+nums[i]` reach
  compares, and the checksum fold all run under Kāra's default overflow checking and land
  within 1.03× of `rustc -O` and 1.11× of `rustc -C overflow-checks=on` on this scalar loop.
- **Three factorings of one shortest-path-by-layers idea** — greedy collapse, explicit layer
  window, and full DP recurrence — all agreeing across the LeetCode examples under both
  `karac run` and `karac build`.

---

**Bug ledger:** none — no compiler change was required for this kata (all three solvers
typechecked, ran, and built correctly on the first pass, and agree with the oracle under both
`karac run` and `karac build`). Unlike [#42](../42-trapping-rain-water/) there is no codegen
characterization either: the greedy scan is branch-predictable and every toolchain lowers it
the same way, so the bench is a clean parity baseline. See the
[`karac` bug ledger](../../../../kara/docs/bug-ledger.jsonl) for the cross-kata history.
