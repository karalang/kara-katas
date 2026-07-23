# 228. Summary Ranges

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Array · Two Pointers &nbsp;·&nbsp; **Source:** [leetcode.com/problems/summary-ranges](https://leetcode.com/problems/summary-ranges/)

Given a **sorted** array of **distinct** integers, return the smallest sorted list of ranges covering every number. A consecutive run `a, a+1, …, b` is written `"a->b"`; a lone number is `"a"`.

```
[0,1,2,4,5,7]    ->  ["0->2","4->5","7"]
[0,2,3,4,6,8,9]  ->  ["0","2->4","6","8->9"]
```

**Constraints:** `0 ≤ nums.length ≤ 20`, `-2³¹ ≤ nums[i] ≤ 2³¹−1`, strictly increasing.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **run scan** ★ | [`summary_ranges.kara`](summary_ranges.kara) | [`summary_ranges.py`](summary_ranges.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Track where the current run **started**. Walk the array; at each position, if the value isn't exactly one more than the previous one, the run has ended at that previous value — emit it (as `"start"` if the run is a single number, else `"start->end"`) and begin a new run at the current value. A single sentinel step past the end flushes the final run so the last group isn't lost. One pass, O(n).

## Kāra features exercised

- **`Slice[i64]` scan producing a `Vec[String]`** — ranges accumulate into an owned string vector returned by value.
- **`f"{start}->{end}"` interpolation** — negative endpoints format naturally (`-3->-1`), and the single-vs-range choice is a plain `start == end` branch.
- **Sentinel loop bound** — iterating `i` up to and including `n` lets the same break condition close both interior runs and the trailing run.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`333678318888000`). Workload: numeric summary-ranges scan (ranges + endpoint sum) over a 1M strictly-increasing LCG array, 250 passes.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O` | 276.1 ms | 0.19× |
| C `clang -O3` | 280.7 ms | 0.19× |
| Go | 1.28 s | 0.88× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 1.41 s | 0.97× |
| **Kāra (codegen)** | 1.45 s | 1.00× |
| Python (scale lane) | 40.87 s | 28.16× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   summary_ranges.kara
karac build summary_ranges.kara && ./summary_ranges
python3 summary_ranges.py
diff <(karac run summary_ranges.kara) <(python3 summary_ranges.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
