# 170. Two Sum III - Data structure design

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Hash Table · Two Pointers · Design &nbsp;·&nbsp; **Source:** [leetcode.com/problems/two-sum-iii-data-structure-design](https://leetcode.com/problems/two-sum-iii-data-structure-design/) &nbsp;·&nbsp; 🔒 **LeetCode Premium**

Design a structure with two operations: `add(number)` inserts a number, and `find(value)` returns `true` iff **some pair** of the added numbers sums to `value`. Numbers may repeat; a value pairs with itself only if it was added at least twice.

```
add(1); add(3); add(5);
find(4) -> true   (1 + 3)
find(7) -> false
add(3);            // two 3s now
find(6) -> true   (3 + 3)
```

**Constraints:** `-10⁵ ≤ number, value ≤ 10⁵`; up to `10⁴` calls to `add` and `find`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **count map + complement scan** ★ | [`two_sum_iii.kara`](two_sum_iii.kara) ✓ | [`two_sum_iii.py`](two_sum_iii.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Store a `Map[number → count]`. `add` bumps the count (O(1)). `find(value)` scans the **distinct keys**: for key `k` the complement is `value - k`. If the complement differs from `k`, it just has to be present; if it **equals** `k` (a self-pair like `3 + 3`), the count must be at least 2. This makes `add` fast and `find` O(distinct) — the standard trade for a workload with many more adds than finds. (The mirror trade — sorted list + two pointers, O(1)-ish find, O(n) add — is the other classic answer.)

## Kāra features exercised

- **Struct + free functions, no impl blocks** — the corpus idiom: a `TwoSum { counts: Map[i64,i64] }` with `add(ds: mut ref TwoSum, …)` and `find(ds: ref TwoSum, …)`. This exercises a `Map`-field struct threaded through `mut ref` / `ref` receivers.
- **`Map` iteration** — `for k in ds.counts.keys()`, with `.get` → `Option` matched inside the loop. The `find` result is a boolean, so hash-iteration order does not affect output (deterministic across run/build).
- **Self-pair count check** — the `complement == k` branch requires `count >= 2`.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`762965`). Workload: build a 170-add sparse multiset over [0,6K) keys (~168 distinct), then 1.2M full-scan find(target) queries; sink=count of trues. NOTE: Kara/Rust/Go/Python use a hash map; C hand-rolls a direct-address count table + distinct-key list (same membership semantics)..

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 577.0 ms | 0.11× |
| Rust `-O` | 3.11 s | 0.57× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 3.15 s | 0.58× |
| **Kāra (codegen)** | 5.42 s | 1.00× |
| Go | 5.49 s | 1.01× |
| Python (scale lane) | 16.29 s | 3.01× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   two_sum_iii.kara
karac build two_sum_iii.kara && ./two_sum_iii
python3 two_sum_iii.py
diff <(karac run two_sum_iii.kara) <(python3 two_sum_iii.py) && echo OK
```

## Notes

A 🔒 **LeetCode-Premium** problem (locked; spec reconstructed from its widely-known description). Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
