# 205. Isomorphic Strings

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Hash Table · String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/isomorphic-strings](https://leetcode.com/problems/isomorphic-strings/)

Two strings are **isomorphic** if the characters of `s` can be consistently replaced to get `t` — a one-to-one mapping where order is preserved and no two characters map to the same one.

```
"egg",   "add"    ->  true
"foo",   "bar"    ->  false   (o must map to both a and r)
"paper", "title"  ->  true
"ab",    "aa"     ->  false   (a and b collide on target a)
```

**Constraints:** `1 ≤ |s| = |t| ≤ 5·10⁴`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **two-way character map** ★ | [`isomorphic.kara`](isomorphic.kara) | [`isomorphic.py`](isomorphic.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Isomorphism is a **bijection**, so one map isn't enough — you need both directions. `s→t` catches an inconsistent forward mapping (a source character that would have to map to two different targets); `t→s` catches two distinct sources colliding on the same target. Walk the strings in lockstep; on each pair, verify both maps agree (or record the new binding). The first contradiction returns false. O(n) time.

## Kāra features exercised

- **Two `Map[char, char]`** — the forward and backward character bijection tables, with `get` (→ `Option`, matched) and `insert` (discarded `Option` result). `char`-keyed *and* `char`-valued maps.
- **`s.chars().collect()` → `Vec[char]`** for O(1) lockstep indexing of both strings.
- **Empty-string edge** — `"" , ""` is trivially isomorphic (the loop never runs).

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`80126`). Workload: is_isomorphic (two-map bijection) over 600K sliding width-200 windows (version-stamped map kernel).

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O -C overflow-checks=on` (equal-safety) | 426.6 ms | 0.99× |
| **Kāra (codegen)** | 430.6 ms | 1.00× |
| Rust `-O` | 435.5 ms | 1.01× |
| Go | 444.3 ms | 1.03× |
| C `clang -O3` | 460.3 ms | 1.07× |
| Python (scale lane) | 10.69 s | 24.82× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   isomorphic.kara
karac build isomorphic.kara && ./isomorphic
python3 isomorphic.py
diff <(karac run isomorphic.kara) <(python3 isomorphic.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
