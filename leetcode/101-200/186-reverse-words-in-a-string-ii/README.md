# 186. Reverse Words in a String II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Two Pointers · String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/reverse-words-in-a-string-ii](https://leetcode.com/problems/reverse-words-in-a-string-ii/) &nbsp;·&nbsp; 🔒 **LeetCode Premium**

Reverse the **order of the words** in a character array **in place**, with O(1) extra space. Words are separated by single spaces; no leading or trailing spaces.

```
"the sky is blue"  ->  "blue is sky the"
"a b c"            ->  "c b a"
```

**Constraints:** the input is a character array; single-space separators.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **reverse-all then reverse-each-word** ★ | [`reverse_words_ii.kara`](reverse_words_ii.kara) | [`reverse_words_ii.py`](reverse_words_ii.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

The classic two-reversal trick, both steps in-place index swaps:

1. **Reverse the entire array.** `"the sky"` → `"yks eht"` — now the words are in the right *order* but each is spelled backwards.
2. **Reverse each word back.** Walk the array; at every space (and the end), reverse the run since the last boundary. `"yks eht"` → `"sky the"`.

No auxiliary buffer, O(n) time, O(1) extra space (the [#151](../151-reverse-words-in-a-string/) contrast collects words into a `Vec` instead — this variant is the in-place one).

## Kāra features exercised

- **In-place `Vec[char]` index swaps** — `reverse_range` swaps `a[i]`/`a[j]` (char is a `Copy` scalar, so no heap churn), driven twice: once over the whole array, then per word.
- **`s.chars().collect()` → `Vec[char]`** for the mutable character array, rebuilt to a `String` with `push` in a `for c in a` loop.
- **`mut ref Vec[char]` parameter** with the `mut` call-site marker on the fresh binding.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`1522595584532`). Workload: ~30K-char word buffer (i64 codes) built once, 3000 in-place two-reversal word-reversal passes with a per-pass char punch; sink=sum of per-pass Horner checksums of the buffer bytes.

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-11-01, karac g6697158fa (0.9.0-dev.14057, v2/MIR backend) (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Go | 388.2 ± 6.0 ms | 0.93× |
| C `clang -O3` | 391.1 ± 5.3 ms | 0.94× |
| Rust `-O` | 402.2 ± 4.2 ms | 0.97× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 402.4 ± 5.6 ms | 0.97× |
| **Kāra (codegen)** | 415.6 ± 4.7 ms | 1.00× |

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

Kāra is last of five, but all five sit within 7% of each other: **1.03×** behind both Rust builds (`rustc -O` and equal-safety), **1.06×** behind C and **1.07×** behind Go. Against the previous feed (2026-07-27, legacy backend `karac 0.1.0`: 0.96× Rust, 0.98× C, 1.00× Go, where Kāra led by a hair) every ratio moved by under 10%, so this is flat; the reorder from first to last is a shuffle inside a 7% band. Every comparator ran 14–16% slower this session (machine state), so compare the ratios, not the milliseconds.

Binary size: C 32.7 KiB, **kāra 295.8 KiB** (302,880 B), Rust 455.7 KiB, Go 2.38 MiB; every v2/MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (this kata's was 34,256 B on 2026-07-27), tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). Peak RSS: C 1.25 MiB, **kāra 1.34 MiB**, Rust 1.36 MiB, Go 2.97 MiB. Compile-cold: clang 53.5 ms < rustc 98.7 ms < **karac 124.1 ms** (2.32× clang, 1.26× rustc); compile peak RSS clang 2.6 MiB, rustc 28.1 MiB, **karac 59.0 MiB**.

## Running

```bash
karac run   reverse_words_ii.kara
karac build reverse_words_ii.kara && ./reverse_words_ii
python3 reverse_words_ii.py
diff <(karac run reverse_words_ii.kara) <(python3 reverse_words_ii.py) && echo OK
```

## Notes

A 🔒 **LeetCode-Premium** problem (locked; spec reconstructed from its widely-known description). Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Benchmarked: see § Benchmarks.
