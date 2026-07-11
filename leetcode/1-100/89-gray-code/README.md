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

> ⚠️ **Machine caveat.** Measured on a **shared x86-64 Linux cloud container** (Intel Xeon @ 2.80 GHz, 4 vCPU, Linux 6.18.5; karac from current `main`). These are container numbers only — this kata has **no M5 `results.json` yet**; it will be re-benched on the corpus's Apple M5 Pro and the canonical table added then. Don't compare absolute times/sizes/RSS against sibling katas' M5 tables; [`bench/results.container-x86.json`](bench/results.container-x86.json) records the real host.

**Workload.** The closed form `gray(i) = i ^ (i >> 1)` generates the **N = 65536** codes. Storing them into a Vec is a **vectorizable refill loop** the optimizer would erase (`BENCHMARKS.md` pitfall), so the bench **folds** each code through a **rolling polynomial hash** — the loop-carried hash serialises the pass and keeps the shift/XOR observable. For **K = 2500** iterations (seeded by the loop index, each code XOR-ed with the iteration index so nothing hoists) it rolls the 65536 codes into a per-iteration accumulator, then combines those. The measured work is the shift/XOR + multiply-add-mod fold inner loop — **pure scalar arithmetic, no arrays**. All five compiled mirrors must agree on `140491298` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded (the loop-carried sum is not a reduction the auto-par pass can split; the default build is verified equal to `KARAC_AUTO_PAR=0`). **Cloud-container numbers.**

| Implementation | Wall time |
|---|---|
| go   gray_code                                | 751.8 ± 2.7 ms |
| **kāra gray_code**                            | **788.0 ± 1.7 ms** |
| c    gray_code (clang -O3)                     | 789.0 ± 5.3 ms |
| rust gray_code (rustc -O, overflow-checks=on)  | 789.4 ± 2.3 ms |
| rust gray_code (rustc -O)                      | 790.8 ± 6.7 ms |

A **five-way dead heat** — kāra, C, and both Rust builds land within **~3 ms** of each other (well inside the noise), with kāra nominally 2nd of five and ahead of C and both Rust variants. This is a **latency-bound** loop: the `acc = (acc·131 + …) % mod` fold is a tight dependency chain (multiply → add → mod, each waiting on the last), so the shift/XOR bit-ops — and kāra's overflow checks — execute in the shadow of that chain and cost nothing. Only Go edges ahead (~1.05×). At equal safety kāra ties `rustc -O -C overflow-checks=on` exactly (788.0 vs 789.4 ms). Python at K=120 (1/20 the iterations) is ~0.91 s, timed separately.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — and on this **latency-bound** multiply-add-mod fold chain all five languages land in a dead heat (the bit-ops, and kāra's overflow checks, execute in the shadow of the mod-chain dependency). C calibrates the metal floor, Go is the other native data point, Python (run at a fraction of the iteration count, timed separately) the ergonomic foil.
