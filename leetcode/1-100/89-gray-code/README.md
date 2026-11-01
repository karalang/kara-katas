# 89. Gray Code

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Math · Backtracking · Bit Manipulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/gray-code](https://leetcode.com/problems/gray-code/)

An **n-bit Gray code sequence** is a permutation of `0 .. 2ⁿ` where the first element is `0`, every adjacent pair differs in **exactly one bit**, and the first and last also differ in one bit. Return any valid such sequence (the canonical one is the *binary-reflected* Gray code).

```
n = 2  ->  [0, 1, 3, 2]        (00, 01, 11, 10)
n = 1  ->  [0, 1]
```

**Constraints:** `1 ≤ n ≤ 16`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Direct XOR formula** `i ^ (i >> 1)` ★ | [`gray_code.kara`](gray_code.kara) ✓ via `karac run` / `karac build` | [`gray_code.py`](gray_code.py) ✓ |
| **Reflect-and-prefix construction** | [`gray_code_reflect.kara`](gray_code_reflect.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output across all six test cases (`n = 0..5`), under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other, with the Python mirror, **and with a full Gray-code-property check** (permutation of `0..2ⁿ`, single-bit adjacent *and* wrap-around transitions, verified for `n = 0..8`). Both compile with **zero diagnostics**.

## Two ways to the same reflected code

**Direct XOR formula** ([`gray_code.kara`](gray_code.kara), the ★) is the one-liner: the i-th binary-reflected Gray code is

```
gray(i) = i ^ (i >> 1)
```

XOR-ing `i` with itself shifted right by one flips exactly the bit positions where `i`'s binary representation *changes* from one place to the next — which is precisely the single-bit-difference property. So the whole sequence is one pass emitting `i ^ (i >> 1)` for `i` in `0 .. 2ⁿ`, O(1) work per element.

**Reflect-and-prefix construction** ([`gray_code_reflect.kara`](gray_code_reflect.kara)) builds the same sequence by its recursive *definition* instead of the closed form. Start from `G(0) = [0]`; to grow `G(k-1)` into `G(k)`, keep it as-is, then append a **mirrored** copy (iterated back-to-front) with the new high bit `1 << (k-1)` OR-ed in:

```
G(k) = G(k-1)  ++  reverse(G(k-1)) each | (1 << (k-1))
```

The reflection is what preserves the single-bit property: within each half the bits change as in `G(k-1)`, and at the seam the two mirrored middle elements differ only in the freshly-added high bit. Doubling `n` times yields the `2ⁿ` codes in the **same order** as `i ^ (i >> 1)`. A distinct surface from the ★ — a growing `Vec[i64]` read back-to-front *while it is being appended to*, driven by a descending `i64` index down to `-1`.

## Kāra features exercised

- **Bit operators** — `^` (XOR), `>>` (right shift), `<<` (left shift), and `|` (OR) on `i64`; the ★ is `i ^ (i >> 1i64)`, the total count is `1i64 << n`, and the reflect build sets the high bit with `out[j] | high`.
- **Growing a `Vec` while reading its own prefix** — the reflect variant's `out.push(out[j] | high)` appends to `out` while indexing an earlier slot, a self-referential-but-safe read (the read resolves before the push).
- **Descending `i64` index to `-1`** — `while j >= 0 { … j = j - 1 }` walks the prefix in reverse, `out[j]` read only while `j >= 0` (signed compare, no underflow read).
- **`String` building via `push_str` + interpolation** — `show` renders `[a, b, …]` from the sequence.

**v1 note.** `n ≤ 16` so `2ⁿ ≤ 65536` and all codes fit i64; the per-case sink folds each sequence's length and values into a running polynomial hash. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`, and both satisfy the Gray-code property check on every case.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   gray_code.kara
karac build gray_code.kara && ./gray_code

# The reflect-and-prefix variant (identical output):
karac run gray_code_reflect.kara

# Python
python3 gray_code.py

# Verify they all agree
diff <(karac run gray_code.kara) <(python3 gray_code.py)                  && echo OK
diff <(karac run gray_code.kara) <(karac run gray_code_reflect.kara)      && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`gray_code.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5 re-bench (2026-11-01).** Measured on the corpus's **Apple M5 Pro reference machine** (arm64, 6P+12E; clang 21 / rustc 1.95 / go 1.26) with **karac g6697158fa** (0.9.0-dev.14057, the v2/MIR backend; the legacy backend was deleted 2026-10-23). The first M5 snapshot (2026-07-11, legacy backend) replaced an earlier x86-64 cloud-container one. Still a **five-way dead heat** — all five land within **0.9 %** (≤ 5.4 ms) of each other, kāra included; kāra's ratio to every comparator is flat since July (1.00× Rust, 1.00× C, 1.00× Go). `bench/results.json` records the M5 host.

**Workload.** The closed form `gray(i) = i ^ (i >> 1)` generates the **N = 65536** codes. Storing them into a Vec is a **vectorizable refill loop** the optimizer would erase (`BENCHMARKS.md` pitfall), so the bench **folds** each code through a **rolling polynomial hash** — the loop-carried hash serialises the pass and keeps the shift/XOR observable. For **K = 2500** iterations (seeded by the loop index, each code XOR-ed with the iteration index so nothing hoists) it rolls the 65536 codes into a per-iteration accumulator, then combines those. The measured work is the shift/XOR + multiply-add-mod fold inner loop — **pure scalar arithmetic, no arrays**. All five compiled mirrors must agree on `140491298` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded, ~99.9 % CPU (`karac build --concurrency-report` finds no parallelizable region, and the default build emits no call of `karac_mir_task_spawn`, verified in the emitted IR (`KARAC_MIR_LL`), same as its `KARAC_AUTO_PAR=0` twin). **M5 Pro numbers, karac g6697158fa, 2026-11-01.**

| Implementation | Wall time |
|---|---|
| rust gray_code (rustc -O, overflow-checks=on)  | **582.3 ± 6.6 ms** |
| go   gray_code                                | 583.1 ± 6.1 ms |
| **kāra gray_code**                            | **584.8 ± 6.4 ms** |
| rust gray_code (rustc -O)                      | 586.1 ± 5.4 ms |
| c    gray_code (clang -O3)                     | 587.7 ± 4.0 ms |

A **five-way dead heat** — all five land within **0.9 %** (582.3 to 587.7 ms), kāra nominally 3rd, every gap inside the rows' σ, so the order is not meaningful. This is a deeply **latency-bound** loop: the `acc = (acc·131 + …) % mod` fold is a tight dependency chain (multiply → add → mod, each waiting on the last), so IPC is *below 1* (kāra 0.87, C 0.78) and the wall-clock is set entirely by that chain's latency. On the July legacy build kāra retired 1.11× C's instructions (2.02 G vs 1.82 G) — its shift/XOR + overflow-check work — but every extra instruction executes in the chain's shadow for free, so the clocks tie (the `B-2026-07-10-5` latency-hidden regime at its most extreme). At equal safety kāra ties `rustc -O -C overflow-checks=on` (1.004×, inside both rows' σ). Python is timed separately (not re-run 2026-11-01).

Compile-cold on the M5 is clang 41.1 ms < rustc 72.9 ms < **karac 107.3 ms** (2.6× clang, 1.47× rustc). Binary size: c 32.6 KiB, **kāra 295.7 KiB**, rust 455.4 KiB, go 2.38 MiB; every MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB, tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). Peak RSS: c 1.00 MiB, **kāra 1.03 MiB**, rust 1.08, go 2.55 MiB. See [`bench/results.json`](bench/results.json) for the exact records (the older container-host records are in [`bench/results.container-x86.json`](bench/results.container-x86.json)).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — and on this **latency-bound** multiply-add-mod fold chain all five languages land in a dead heat (the bit-ops, and kāra's overflow checks, execute in the shadow of the mod-chain dependency). C calibrates the metal floor, Go is the other native data point, Python (run at a fraction of the iteration count, timed separately) the ergonomic foil.
