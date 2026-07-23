# 229. Majority Element II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Boyer–Moore Voting · Counting &nbsp;·&nbsp; **Source:** [leetcode.com/problems/majority-element-ii](https://leetcode.com/problems/majority-element-ii/)

Return every element that appears **more than ⌊n/3⌋** times. Because three distinct values each over n/3 would total more than n, there can be **at most two** such elements.

```
[3,2,3]              ->  [3]
[1,1,1,3,3,2,2,2]    ->  [1,2]
[1,2,3,4]            ->  []
```

**Constraints:** `1 ≤ nums.length ≤ 5·10⁴`, `-10⁹ ≤ nums[i] ≤ 10⁹`. Target: O(n) time, O(1) space.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **two-candidate Boyer–Moore vote** ★ | [`majority_element_ii.kara`](majority_element_ii.kara) | [`majority_element_ii.py`](majority_element_ii.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

The classic majority vote finds a single >n/2 element by pairing off different values until one survives. The >n/3 version runs **two** votes at once: keep two candidates with two counts. For each value, bump the matching candidate; if neither matches but a count has hit 0, adopt the value there; otherwise the value cancels one vote from **both** candidates (decrement both). After the pass, the two candidates are the only values that *could* exceed n/3.

The vote guarantees survivors but not that they actually clear the bar — a decisive answer needs a **second counting pass** to tally each candidate's real frequency and keep only those strictly above ⌊n/3⌋. Two linear passes, O(1) extra space. Results are ordered ascending for a canonical output.

## Kāra features exercised

- **Two-candidate state machine** — four `i64` accumulators updated through a `count > 0 and x == cand` guarded `if`/`else if` chain, so an unadopted candidate (count 0) never spuriously matches.
- **Verification pass + threshold** — a second `Slice[i64]` scan and a strict `real > n/3` test; `Vec[i64]` result built by `push`.
- **In-place two-element ordering** — `result[0], result[1] = result[1], result[0]` (parallel assignment) canonicalises the at-most-two answer without a general sort.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`8162979`). Workload: two-candidate Boyer-Moore vote + verify over a width-16 sliding window across a 3M LCG array (branchy, loop-carried counts).

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O -C overflow-checks=on` (equal-safety) | 547.4 ms | 0.81× |
| C `clang -O3` | 549.4 ms | 0.81× |
| Rust `-O` | 592.5 ms | 0.88× |
| Go | 664.5 ms | 0.98× |
| **Kāra (codegen)** | 674.7 ms | 1.00× |
| Python (scale lane) | 9.25 s | 13.71× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   majority_element_ii.kara
karac build majority_element_ii.kara && ./majority_element_ii
python3 majority_element_ii.py
diff <(karac run majority_element_ii.kara) <(python3 majority_element_ii.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
