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
- **Data-dependent loop count** — the number of iterations equals the answer. clang and karac now replace the loop with a hardware popcount (`llvm.ctpop`, `cnt`); `rustc -O` keeps the loop (see the benchmark).

## Benchmarks

Compute-bound, seq-only kata — the purely-ALU counterpart to the memory-bound [#189](../189-rotate-array/). **Build-once + punch**: fill `N = 2_000_000` LCG values, then sum `hamming_weight(nums[i] ^ round)` over `K = 10` rounds. XOR-ing with the round index makes each round's input differ (no hoisting). All five mirrors print the same sink (`310007300`).

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-11-01, karac g6697158fa (v2/MIR backend) (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean ± σ | vs Kāra |
|---|---|---|
| C `clang -O3` | 7.0 ± 0.1 ms | 0.52× |
| **Kāra (codegen)** | **13.5 ± 1.4 ms** | 1.00× |
| Rust `-O` | 235.8 ± 2.3 ms | 17.43× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 259.1 ± 3.6 ms | 19.15× |
| Go | 274.5 ± 3.8 ms | 20.29× |
| Python | 18.98 ± 0.19 s | last measured on the x86 container (see below), not re-run |

**What this measures on arm64: idiom recognition, not general codegen quality.** The Kernighan loop `x = x & (x - 1)` counting iterations *is* a population count, and both `clang -O3` and karac now recognise it: the loop is replaced by `llvm.ctpop` in the IR and a `cnt` (vector popcount) sequence in the binary (verified in the emitted IR, `KARAC_MIR_LL`, and the disassembly). `rustc -O` does not make that transform for this source, so Rust (and, by its timing, Go) still runs the data-dependent loop once per set bit — that, not anything else about the code, is the whole 17× Kāra-vs-Rust gap. The remaining 1.92× behind C is measured once both sides run `cnt`; its cause has not been profiled here (Kāra's bounds-checked `nums[j]` loads and overflow-checked sum are the unverified suspects), and at ~13 ms the σ is ±10%. Every sink matches, so this is a real transform, not a miscompile.

**Before/after, in ratios.** In the 2026-07-28 M5 run (karac 0.1.0, legacy backend) Kāra still ran the loop: 1.11× behind Rust, 0.96× of Go, and **37.62× behind C**, which already made the popcount transform. On 2026-11-01 Kāra is 0.06× of Rust (17× ahead), 0.05× of Go, and 1.92× behind C. The MIR build of this kernel matches legacy dd86e3955 to within 1.03× in instructions, so the recognition landed in the compiler between July and October, not with the MIR switch. (All comparators ran ~16% slower in absolute terms this session — machine state — so compare ratios, not milliseconds.)

Binary size: Kāra 302,872 B vs C 33,512 B, Rust 466,312 B, Go 2,492,514 B. Every MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB, tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md).

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc, clang, go, karac
./bench/bench.sh
```

### Equal-safety: ahead of `rust_ovf`; a small check tax vs wrapping C

> **History (2026-11-01 note).** The table and paragraph below are a container snapshot from a shared **x86-64 Linux cloud container** ([`bench/results.container-x86.json`](bench/results.container-x86.json)), measured before the popcount transform and on a target where the kernel stayed a loop for C too. Their ranking (C/Rust/Go slightly ahead of Kāra, Kāra ahead of `rust_ovf`, "a small check tax") is not the current M5 result — see the table above.

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
