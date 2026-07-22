# 191. Number of 1 Bits

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Divide and Conquer · Bit Manipulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/number-of-1-bits](https://leetcode.com/problems/number-of-1-bits/)

Return the number of set bits (the **Hamming weight**) of an integer.

```
11         (1011)      ->  3
128        (10000000)  ->  1
4294967295 (all ones)  ->  32
```

**Constraints:** the input is a non-negative integer (32-bit range).

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Brian Kernighan** ★ | [`number_of_1_bits.kara`](number_of_1_bits.kara) | [`number_of_1_bits.py`](number_of_1_bits.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

**`x & (x - 1)` clears the lowest set bit.** Subtracting 1 borrows through the trailing zeros, flipping that lowest `1` to `0` and the zeros below it to `1`; the `AND` then wipes exactly that block. Repeat until `x` is 0, counting iterations — the loop runs **once per set bit**, so it's O(popcount) rather than O(bit-width), a win on sparse inputs.

## Kāra features exercised

- **Bitwise `&` and integer `-` on `i64`** in the Kernighan reduction `x = x & (x - 1)`.
- **Data-dependent loop count** — the number of iterations equals the answer, which is exactly why the kernel resists auto-vectorization (see the benchmark).

## Benchmarks

> **Machine.** Container-only reference run — a shared **x86-64 Linux cloud container** ([`bench/results.container-x86.json`](bench/results.container-x86.json)); canonical Apple-M5 numbers (`bench/results.json`) are pending a maintainer run. Absolute times are noisy on the shared host; **within-run cross-language ratios are the signal.**

Compute-bound, seq-only kata — the purely-ALU counterpart to the memory-bound [#189](../189-rotate-array/). **Build-once + punch**: fill `N = 2_000_000` LCG values, then sum `hamming_weight(nums[i] ^ round)` over `K = 10` rounds. XOR-ing with the round index makes each round's input differ (no hoisting), and the Kernighan `x &= x-1` chain is a data-dependent loop — **not** auto-vectorizable — so this measures a genuine sequential ALU workload. All five mirrors print the same sink (`310007300`).

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc, clang, go, karac
./bench/bench.sh
```

### Equal-safety: ahead of `rust_ovf`; a small check tax vs wrapping C

Container snapshot, hyperfine `--warmup 5 --runs 30`:

| Run | Mean ± σ | vs kāra |
|---|---|---|
| c `popcount` (`clang -O3`) | 365.7 ± 2.8 ms | 1.09× ahead |
| rust `popcount` (`-O`, wrapping) | 378.3 ± 9.6 ms | 1.06× ahead |
| go `popcount` | 387.2 ± 4.8 ms | 1.03× ahead |
| **kāra `popcount` (codegen)** | **400.3 ± 5.2 ms** | — |
| rust `popcount` (`overflow-checks=on`) | 483.2 ± 18.3 ms | **kāra 1.21× ahead** |
| python `popcount` | 18.98 ± 0.19 s | (scale only; 3 runs) |

The honest comparison is at **equal safety**. Kāra bounds-checks every `nums[j]` load and overflow-checks the `count + 1` / `x - 1` by default; `rustc -O` and `clang -O3` do neither. Matching that safety with `-C overflow-checks=on` moves Rust to **483 ms** — and against *that* lane **Kāra is ahead** (400 vs 483). Against wrapping C/Rust (~370 ms) Kāra pays only ~9%: the Kernighan kernel is a tight ALU chain LLVM lowers near-optimally for either frontend, so the check tax is small — the mirror image of [#189](../189-rotate-array/)'s memory-bound regime and a milder version of [#169](../169-majority-element/)'s check-bound scan.

## Running

```bash
karac run   number_of_1_bits.kara
karac build number_of_1_bits.kara && ./number_of_1_bits
python3 number_of_1_bits.py
diff <(karac run number_of_1_bits.kara) <(python3 number_of_1_bits.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean.
