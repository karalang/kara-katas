# 157. Read N Characters Given Read4

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** String · Simulation · Design &nbsp;·&nbsp; **Source:** [leetcode.com/problems/read-n-characters-given-read4](https://leetcode.com/problems/read-n-characters-given-read4/) &nbsp;·&nbsp; 🔒 **LeetCode Premium**

A `read4` primitive returns up to **4** characters at a time from a source (fewer than 4 only at EOF). Implement `read(n)` — read exactly `n` characters (or all that remain).

```
src="abc",        read(4)  ->  "abc"        (3)
src="HelloWorld", read(5)  ->  "Hello"      (5)
src="HelloWorld", read(12) ->  "HelloWorld" (10)
src="",           read(3)  ->  ""           (0)
```

**Constraints:** `1 ≤ n ≤ 1000`; `read` is called **once** (see [#158](../158-read-n-characters-given-read4-ii-call-multiple-times/) for the multi-call variant).

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **chunked read4 + tail-trim** ★ | [`read_n.kara`](read_n.kara) ✓ | [`read_n.py`](read_n.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Pull chunks of up to 4 characters until `n` are collected or `read4` returns empty (EOF). Each chunk is appended whole *unless* it would overshoot `n`, in which case only the first `n - total` characters are taken. The source and cursor live in a `Reader` struct; `read4` slices the next ≤4 bytes and advances the cursor.

## Kāra features exercised

- **`mut ref Reader` cursor state** advanced across `read4` calls; `read4` returns a fresh `String` chunk via `rd.src[pos..pos+1]` slicing.
- **String slicing** for both the chunk build and the tail-trim `chunk[0..take]`.
- **`f"{len} {str}"` formatting** for output.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`1973156584`). Workload: read(7) state machine draining a 50000-char buffer x 3200 punched rewinds (lossy #157 read4); rolling-checksum fold over chars read.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 237.7 ms | 0.68× |
| Rust `-O` | 267.8 ms | 0.76× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 292.1 ms | 0.83× |
| **Kāra (codegen)** | 350.6 ms | 1.00× |
| Go | 433.7 ms | 1.24× |
| Python (scale lane) | 45.09 s | 128.61× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   read_n.kara
karac build read_n.kara && ./read_n
python3 read_n.py
diff <(karac run read_n.kara) <(python3 read_n.py) && echo OK
```

## Notes

A 🔒 **LeetCode-Premium** problem (locked; spec reconstructed from its widely-known description). Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
