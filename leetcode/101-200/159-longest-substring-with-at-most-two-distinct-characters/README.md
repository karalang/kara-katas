# 159. Longest Substring with At Most Two Distinct Characters

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Hash Table · String · Sliding Window &nbsp;·&nbsp; **Source:** [leetcode.com/problems/longest-substring-with-at-most-two-distinct-characters](https://leetcode.com/problems/longest-substring-with-at-most-two-distinct-characters/) &nbsp;·&nbsp; 🔒 **LeetCode Premium**

Given a string `s`, return the length of the **longest substring that contains at most two distinct characters**.

```
"eceba"      ->  3   ("ece")
"ccaabbb"    ->  5   ("aabbb")
"abcabcabc"  ->  2
"aaaaaa"     ->  6
```

**Constraints:** `0 ≤ |s|`; `s` consists of English letters.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **sliding window + count map** ★ | [`longest_two_distinct.kara`](longest_two_distinct.kara) ✓ | [`longest_two_distinct.py`](longest_two_distinct.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

A single O(n) sliding window. Grow the right edge one char at a time, recording each char's count in a `Map[char, i64]`. The map's **size** is the number of distinct chars in the window — whenever it exceeds 2, shrink from the left: decrement the leftmost char's count, and `remove` it from the map when the count reaches zero. After each step the window `[left, right]` is valid, so the answer is the running maximum of its width.

## Kāra features exercised

- **`Map[char, i64]`** — `char`-keyed hash map with `.get` → `Option`, `.insert`, `.remove`, and `.len()` as the distinct-count. The `Option` returned by `insert`/`remove` is discarded with `let _ = …` (Kāra treats `Option` as implicitly `#[must_use]`).
- **`s.chars().collect()` → `Vec[char]`** — decode UTF-8 once so the window can index chars in O(1) (`s[i]` on a `String` is deliberately a compile error).
- **`ref Map` parameter** — the `count_of` helper borrows the map read-only.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`4218300`). Workload: two-pointer sliding window over a 20000-char buffer (alphabet 8), width-96 sub-ranges x 100 punched reps; per-call fixed count table (kata Map[char,i64] as a flat array, C hand-rolls the same); data-dependent left-shrink loop.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 453.4 ms | 0.79× |
| Go | 532.7 ms | 0.93× |
| **Kāra (codegen)** | 572.8 ms | 1.00× |
| Rust `-O` | 723.4 ms | 1.26× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 725.2 ms | 1.27× |
| Python (scale lane) | 38.65 s | 67.47× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   longest_two_distinct.kara
karac build longest_two_distinct.kara && ./longest_two_distinct
python3 longest_two_distinct.py
diff <(karac run longest_two_distinct.kara) <(python3 longest_two_distinct.py) && echo OK
```

## Notes

A 🔒 **LeetCode-Premium** problem (locked; spec reconstructed from its widely-known description). Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
