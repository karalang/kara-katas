# 187. Repeated DNA Sequences

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Hash Table · String · Sliding Window · Hash Function · Bit Manipulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/repeated-dna-sequences](https://leetcode.com/problems/repeated-dna-sequences/)

Return every length-10 substring (over the DNA alphabet `A/C/G/T`) that appears **more than once** in the string.

```
"AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"  ->  ["AAAAACCCCC","CCCCCAAAAA"]
```

**Constraints:** `1 ≤ |s| ≤ 10⁵`; `s` consists of `A`, `C`, `G`, `T`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **sliding window + count map** ★ | [`repeated_dna.kara`](repeated_dna.kara) | [`repeated_dna.py`](repeated_dna.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Slide a width-10 window across the string and count each 10-mer in a `Map[String, i64]`. A sequence is recorded exactly once — the first time its count crosses **1 → 2** — so the output is each repeated sequence in first-repeat order (deterministic across backends; LeetCode accepts any order). O(n) windows, each an O(10) substring hash.

## Kāra features exercised

- **`Map[String, i64]` counter with `String` keys** — the canonical grouping/counting idiom. Each iteration `get`s (borrows the key), and on a duplicate `insert`s over an existing key. This is the exact `String`-keyed overwrite surface the [#49 map-of-lists](../../1-100/49-group-anagrams/) work drove into the compiler's leak-fix (B-2026-07-22-12 / the older duplicate-key B-2026-06-20-9); here the value is a scalar `i64`, and it is verified valgrind-clean.
- **`s[i..i+10].to_string()`** — an owned `String` key minted per window from a slice.
- **`Option` match + `.clone()`** — record on the count transition, then reinsert.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`6435360`). Workload: length-10 dup-window scan over a 1M-base PRNG DNA buffer x 30 punched passes; rolling 2-bit hash + direct-address 2^20 stamp/count table (C-style, uniform across all five langs).

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-11-01, karac g6697158fa (0.9.0-dev.14057, v2/MIR backend) (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O` | 68.6 ± 1.4 ms | 0.92× |
| C `clang -O3` | 69.1 ± 3.0 ms | 0.93× |
| **Kāra (codegen)** | 74.7 ± 2.7 ms | 1.00× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 91.2 ± 1.7 ms | 1.22× |
| Go | 92.8 ± 3.6 ms | 1.24× |

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

Kāra is third: **1.09×** behind `rustc -O` and **1.08×** behind C, and now **ahead** of equal-safety Rust (**1.22×** ahead, 74.7 vs 91.2 ms) and Go (**1.24×** ahead). Against the previous feed (2026-07-28, legacy backend `karac 0.1.0`) Kāra gained past the 10% noise line on every comparator: Kāra/Rust 1.43× → 1.09×, Kāra/C 1.45× → 1.08×, Kāra/Go 1.08× → 0.81×, and Kāra/equal-safety-Rust 1.08× → 0.82×; Kāra moves from last of five to third. The comparators ran 30–32% slower this session (machine state) while Kāra held at ~75 ms, so the ratios, not the milliseconds, carry the comparison.

Binary size: C 32.8 KiB, **kāra 295.8 KiB** (302,880 B), Rust 455.6 KiB, Go 2.38 MiB; every v2/MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (this kata's was 34,320 B on 2026-07-28), tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). Peak RSS is set by the 2^20 count table: C 24.72 MiB, Rust 24.73 MiB, **kāra 24.75 MiB**, Go 27.50 MiB. Compile-cold: clang 46.5 ms < rustc 91.4 ms < **karac 121.5 ms** (2.61× clang, 1.33× rustc); compile peak RSS clang 2.6 MiB, rustc 28.7 MiB, **karac 58.8 MiB**.

## Running

```bash
karac run   repeated_dna.kara
karac build repeated_dna.kara && ./repeated_dna
python3 repeated_dna.py
diff <(karac run repeated_dna.kara) <(python3 repeated_dna.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Benchmarked: see § Benchmarks.
