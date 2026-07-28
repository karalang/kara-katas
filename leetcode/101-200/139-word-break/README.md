# 139. Word Break

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Dynamic Programming · String · Hash Set &nbsp;·&nbsp; **Source:** [leetcode.com/problems/word-break](https://leetcode.com/problems/word-break/)

Given a string `s` and a dictionary of words, decide whether `s` can be segmented into a space-separated sequence of one or more dictionary words. Words may be reused.

```
"leetcode",      {leet, code}                 ->  true    # leet + code
"applepenapple", {apple, pen}                 ->  true    # apple + pen + apple
"catsandog",     {cats, dog, sand, and, cat}  ->  false
"aaaaaaaa",      {a, aa, aaa}                  ->  true
```

**Constraints:** `1 ≤ |s| ≤ 300`, `1 ≤ dict size ≤ 1000`, `1 ≤ |word| ≤ 20`, all lowercase.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **prefix DP** ★ | [`word_break.kara`](word_break.kara) ✓ | [`word_break.py`](word_break.py) ✓ |

`✓` runs end-to-end today across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. Zero diagnostics, valgrind-clean.

## The mechanism

`dp[i]` is true when the prefix `s[0..i]` segments cleanly. `dp[0]` is the empty prefix (trivially true). For each end `i`, scan every split point `j < i`: if the prefix `s[0..j]` already segments (`dp[j]`) **and** the piece `s[j..i]` is a dictionary word, then `s[0..i]` segments too. The answer is `dp[n]`. `O(n²)` split points × the substring/Set-lookup cost.

## Kāra features exercised

- **`Set[String]` membership** — `dict.contains(piece)` over a hash set of owned `String`s; the dictionary is built with `.insert`.
- **`String.substring(j, i)`** — the `s[j..i]` prefix-piece extraction inside the double loop (a fresh heap `String` per probe — a real allocation/leak surface, verified clean).
- **`Vec[bool]` DP table** — filled to length `n + 1`, indexed both as a read (`dp[j]`) and a write (`dp[i] = true`).

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`2602274054`). Workload: prefix-DP word break over 2.2M random windows into a build-once string; dict is a SET (flat stamped base-A table; C hand-rolls it).

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-07-27 (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 89.5 ms | 0.74× |
| **Kāra (codegen)** | 121.5 ms | 1.00× |
| Rust `-O` | 123.3 ms | 1.01× |
| Go | 159.0 ms | 1.31× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 160.9 ms | 1.32× |

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   word_break.kara
karac build word_break.kara && ./word_break
python3 word_break.py
diff <(karac run word_break.kara) <(python3 word_break.py) && echo OK
```

## Notes

Clean first-pass dogfood: `Set[String]` + per-probe `substring` allocation + `Vec[bool]` DP, compiled correctly with no friction (interp == build == Python, valgrind-clean). Sets up #140 Word Break II (enumerate every segmentation), which needs backtracking rather than a boolean table.
