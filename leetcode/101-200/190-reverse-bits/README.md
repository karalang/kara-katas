# 190. Reverse Bits

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Divide and Conquer · Bit Manipulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/reverse-bits](https://leetcode.com/problems/reverse-bits/)

Reverse the bits of a 32-bit **unsigned** integer.

```
43261596   (00000010100101000001111010011100)
  -> 964176192 (00111001011110000010100101000000)
1          ->  2147483648   (bit 0 → bit 31)
4294967295 ->  4294967295   (all ones)
```

**Constraints:** the input is a 32-bit unsigned integer.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **shift-and-peel** ★ | [`reverse_bits.kara`](reverse_bits.kara) | [`reverse_bits.py`](reverse_bits.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Shift the answer left one bit at a time while peeling the input's **low** bit off the right: `result = (result << 1) | (x & 1)`, then `x >>= 1`. After 32 steps, the input's bit 0 has migrated to the answer's bit 31, bit 1 to bit 30, and so on — a full mirror. O(32) = O(1).

## Kāra features exercised

- **Bitwise operators on `i64`** — `<<`, `>>`, `&`, `|` — the whole kernel. Values live in Kāra's signed `i64` but are masked to 32-bit behaviour; the intermediate `result << 1` peaks at 2³², well inside `i64`, so the default checked arithmetic never trips.
- **Fixed 32-iteration loop** — the constant-width shift-register idiom.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`17179869173845686`). Workload: 32-step bit-reversal over an 8M-value loop-carried PRNG stream, summed (very cheap per-op: compiled langs reduce the reversal to a handful of instructions, so the compiled lane is startup-dominated; the Python scale lane runs the naive 32-step loop).

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-11-01, karac g6697158fa (0.9.0-dev.14057, v2/MIR backend) (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O` | 9.7 ± 0.2 ms | 0.84× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 9.8 ± 0.1 ms | 0.85× |
| C `clang -O3` | 11.3 ± 0.2 ms | 0.98× |
| **Kāra (codegen)** | 11.5 ± 0.3 ms | 1.00× |
| Go | 78.7 ± 0.7 ms | 6.83× |

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

Kāra is fourth: **1.19×** behind `rustc -O` and **1.18×** behind equal-safety Rust, at parity with C (**1.02×**), and **6.83×** ahead of Go. Against the previous feed (2026-07-27, legacy backend `karac 0.1.0`: 1.19× Rust, 1.00× C, 0.14× Go) every ratio moved by 2% or less, so flat. Every comparator ran 14–16% slower this session (machine state), so compare the ratios, not the milliseconds; at ~11 ms the compiled lane is largely startup.

Binary size: C 32.7 KiB, **kāra 295.8 KiB** (302,880 B), Rust 455.4 KiB, Go 2.38 MiB; every v2/MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (this kata's was 33,776 B on 2026-07-27), tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). Peak RSS: C 1.02 MiB, **kāra 1.03 MiB**, Rust 1.08 MiB, Go 2.66 MiB. Compile-cold: clang 41.4 ms < rustc 75.3 ms < **karac 108.3 ms** (2.62× clang, 1.44× rustc); compile peak RSS clang 2.6 MiB, rustc 24.8 MiB, **karac 55.9 MiB**.

## Running

```bash
karac run   reverse_bits.kara
karac build reverse_bits.kara && ./reverse_bits
python3 reverse_bits.py
diff <(karac run reverse_bits.kara) <(python3 reverse_bits.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Benchmarked: see § Benchmarks.
