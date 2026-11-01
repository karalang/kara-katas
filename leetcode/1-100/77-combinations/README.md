# 77. Combinations

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Backtracking &nbsp;·&nbsp; **Source:** [leetcode.com/problems/combinations](https://leetcode.com/problems/combinations/)

Given two integers `n` and `k`, return **all combinations of `k` numbers chosen from the range `[1, n]`**. Order within a combination and among the combinations doesn't matter.

```
n = 4, k = 2  ->  [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
n = 1, k = 1  ->  [[1]]
```

**Constraints:** `1 ≤ n ≤ 20`; `1 ≤ k ≤ n`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Start-indexed backtracking** ★ | [`combinations.kara`](combinations.kara) ✓ via `karac run` / `karac build` | [`combinations.py`](combinations.py) ✓ |
| **+ "not enough left" prune** | [`combinations_pruned.kara`](combinations_pruned.kara) ✓ | — |
| **Gosper's hack** — iterative bitmask enumeration | [`combinations_bitmask.kara`](combinations_bitmask.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output across all eight test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and all three approaches agree with each other and with the Python mirror.

## The backtracking — one mutable path, snapshot at the leaf

A depth-first search over a **start index** picks `k` strictly-increasing values:

```
if path.len() == k:   snapshot path into the output, return
for i in start ..= n:
    path.push(i)
    backtrack(start = i + 1)     # i+1, never i — each number used at most once
    path.pop()                   # restore the parent's path
```

Recursing with `start = i + 1` keeps the path strictly increasing, so every `k`-subset is visited **exactly once** in lexicographic order — the index discipline *is* the dedup, no `HashSet` needed. One mutable `path` carries the choices on the current branch; `push` / recurse / `pop` brackets each choice so the parent's path is exactly restored, and the only copy is the `path.clone()` snapshot at each leaf. This is the same start-indexed DFS as kata [#39](../39-combination-sum/), minus the reuse (there a pick recurses at `i`; here at `i + 1`).

**Start-indexed backtracking** ([`combinations.kara`](combinations.kara)) is the ★.

**+ prune** ([`combinations_pruned.kara`](combinations_pruned.kara)) adds the standard cutoff: with `need = k - path.len()` values still to pick, the last start value that can still complete is `n - need + 1`, so the loop runs `start ..= n - need + 1` instead of `start ..= n` — dead branches (too few numbers left) are never entered. Same combinations, a trimmed tree.

**Gosper's hack** ([`combinations_bitmask.kara`](combinations_bitmask.kara)) is a completely different lens — **no recursion at all**. Each combination is a bitmask with exactly `k` bits set (bit `j` ⇒ number `j+1`), and the hack walks to the next-larger integer with the same popcount in O(1) bit ops:

```
c = x & (0 - x)                 # isolate the lowest set bit
r = x + c                       # ripple past that run of ones
x = (((x ^ r) >> 2) / c) | r    # slide the trailing ones back down
```

from `(1 << k) - 1` until `x` reaches `1 << n`. Gosper emits masks in integer order, not lexicographic, so the decoded combinations are sorted (a small selection sort over `Vec[Vec[i64]]`) to line up with the ★. It's the pure bit-twiddling method — the same bitmask-as-set idea kata [#51](../51-n-queens/) uses — and, as a distinct codegen surface (shifts / `&` / `|` / `^` / integer divide / the `Vec[Vec]` element swap), a deliberate probe that these lower identically across interpreter, JIT and codegen.

## Kāra features exercised

- **Recursion threading `mut ref Vec[i64]` + `mut ref Vec[Vec[i64]]`** — `path` and the output accumulator recurse as mutable borrows; the root call writes the call-site markers (`mut path`, `mut out`) since both are fresh owned bindings, interior calls forward the already-`mut ref` bindings unmarked (the call-site-marker rule, shared with kata [#39](../39-combination-sum/)).
- **`path.clone()` leaf snapshot** — the one copy per emitted combination, into `Vec[Vec[i64]]`; interior nodes mutate the single shared `path` in place.
- **`path.push(i)` / `path.pop()` bracketing** — the choose/undo backtracking move on a `Vec[i64]` stack.
- **`Vec[Vec[i64]]` indexed read** — `combos[c]` in the harness binds a combination out of the result for printing/hashing (the borrowed-nested-collection read of kata [#48](../48-rotate-image/)).
- **`k == 0` edge** — `combine(4, 0)` yields the single empty combination `[]`, exercising the length-0 base case and an empty `Vec[i64]` snapshot.
- **Bitwise ops + `Vec[Vec[i64]]` element swap** — the Gosper variant exercises `<<` / `>>` / `&` / `|` / `^` / integer `/` and `x & (0 - x)`, plus swapping two `Vec[i64]` rows in place (`out[i], out[min_idx] = out[min_idx], out[i]`); all lower identically across every engine.

**v1 note.** Counts (up to `C(20,10) = 184,756`) and values fit i64 trivially; the per-case sink is `count:hash` so it is both count- and content-sensitive. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`.

The Gosper's-hack variant surfaced [`B-2026-07-11-10`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) — its `k == 0` case pushes the single empty combination, and `out.push(Vec.new())` where `out: Vec[Vec[i64]]` failed typecheck with `expected 'Vec<i64>', found 'Vec<?T0>'` instead of inferring the inner element type from `push`'s statically-known parameter type. The DFS solvers never hit it: their empty combination comes from `path.clone()` of an already-typed `path`. Low severity and ergonomics-only — a clean, actionable error rather than a run/build divergence — so the kata took the idiomatic one-line annotation (`let empty: Vec[i64] = Vec.new()`) rather than being routed around. The compiler fix landed 2026-07-11 (deep-resolving both the receiver element type and the argument through the substitutions the unification had just populated, before the assignability check), and `out.push(Vec.new())` infers correctly today; [`combinations_bitmask.kara`](combinations_bitmask.kara) still carries the explicit binding, which now reads as a naming choice rather than a workaround.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   combinations.kara
karac build combinations.kara && ./combinations

# The pruned and Gosper's-hack variants (identical output):
karac run combinations_pruned.kara
karac run combinations_bitmask.kara

# Python
python3 combinations.py

# Verify they all agree
diff <(karac run combinations.kara) <(python3 combinations.py)              && echo OK
diff <(karac run combinations.kara) <(karac run combinations_pruned.kara)   && echo OK
diff <(karac run combinations.kara) <(karac run combinations_bitmask.kara)  && echo OK
```

## Benchmarks
Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`combinations.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5 re-bench (2026-11-01).** Measured on the corpus's **Apple M5 Pro reference machine** (arm64, 6P+12E; clang 21 / rustc 1.95 / go 1.26) with **karac g6697158fa** (0.9.0-dev.14057, the v2/MIR backend; the legacy backend was deleted 2026-10-23). The first M5 snapshot (2026-07-10/11, legacy backend) replaced an earlier x86-64 cloud-container one. **The five-way dead heat holds:** all five runtimes sit inside ~1 %, each within the others' σ; kāra's ratios to every comparator are flat since July (Kāra/Rust 0.97× → 1.00×, Kāra/C 1.00× → 1.00×, Kāra/Go 1.00× → 0.99×). `bench/results.json` records the M5 host.

**Workload.** The pruned start-indexed backtracking (the ★) run as an **enumerate-and-fold**: the recursion visits all **C(16, 8) = 12,870** combinations and folds each leaf's values into a threaded accumulator (no `Vec`-of-`Vec` storage — so the measured work is the **DFS recursion itself**, not allocation), for **K = 1,500** iterations seeded by the loop index so nothing hoists. All five compiled mirrors must agree on `667304351` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded, ~99.9 % CPU (the loop-carried sum is not a reduction the auto-par pass can split — `karac build --concurrency-report` reports `<no parallelization opportunities detected>`, and the default build emits no call of `karac_mir_task_spawn`, verified in the emitted IR (`KARAC_MIR_LL`), same as its `KARAC_AUTO_PAR=0` twin). **M5 Pro numbers, karac g6697158fa, 2026-11-01.**

| Implementation | Wall time |
|---|---|
| rust combinations (rustc -O, overflow-checks=on) | **547.4 ± 6.6 ms** |
| **kāra combinations**                            | **548.1 ± 5.1 ms** |
| rust combinations (rustc -O)                     | 548.8 ± 5.6 ms |
| c    combinations (clang -O3)                     | 550.2 ± 5.1 ms |
| go   combinations                                | 553.5 ± 6.2 ms |

A **~1 % five-way dead heat**. On this recursion-bound backtracking kāra lands **2nd of five, 1.001× the equal-safety `rustc -O -C overflow-checks=on` row** (547.4 ms) and level with plain `rustc -O` (548.8 ms), C (550.2 ms) and Go (553.5 ms) — every gap is smaller than the rows' σ, so the order is not meaningful. Overflow checks are free here (the workload is call/branch-bound, not arithmetic-bound), which is why the overflow-checked Rust build is no slower than the wrapping one. Python was last measured 2026-07-11 and not re-run: at 1/10 the iteration count it took ~0.69 s (~14× kāra projected, at July's kāra time).

Compile-cold on the M5 is clang 43.9 ms < rustc 87.0 ms < **karac 112.5 ms** (2.6× clang, 1.29× rustc). Binary size: c 32.8 KiB, **kāra 295.8 KiB**, rust 455.8 KiB, go 2.38 MiB; every MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB, tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). Peak RSS: c 1.00 MiB, **kāra 1.03 MiB**, rust 1.08, go 2.70 MiB. The runtime is a dead heat. See [`bench/results.json`](bench/results.json) for exact records.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — and on this recursion-bound backtracking the five languages land within about 1 % of each other (2026-11-01). C calibrates the metal floor, Go is the other native data point, Python (run at 1/10 the iteration count, timed separately; last measured 2026-07-11) the ergonomic foil.
