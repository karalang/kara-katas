# 214. Shortest Palindrome

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** String · KMP · Rolling Hash &nbsp;·&nbsp; **Source:** [leetcode.com/problems/shortest-palindrome](https://leetcode.com/problems/shortest-palindrome/)

Prepend the **minimum** number of characters to the front of `s` so the result is a palindrome, and return that shortest palindrome.

```
"aacecaaa"  ->  "aaacecaaa"
"abcd"      ->  "dcbabcd"
"aabba"     ->  "abbaabba"
"a"         ->  "a"
```

**Constraints:** `0 ≤ |s| ≤ 5·10⁴`, `s` is lowercase English letters.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **KMP prefix-function** ★ | [`shortest_palindrome.kara`](shortest_palindrome.kara) | [`shortest_palindrome.py`](shortest_palindrome.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

The characters you must prepend are exactly the reverse of the part of `s` that lies **after its longest palindromic prefix** — the more of `s` that is already a palindrome from the front, the less you add.

Finding that prefix is the KMP trick. Concatenate `s + '#' + reverse(s)` and compute the **prefix-function** (failure table): `fail[i]` is the length of the longest proper prefix of the string up to `i` that is also a suffix there. The `'#'` separator (a character outside the alphabet) prevents a match from straddling the join, so the table's last entry is the longest prefix of `s` that equals a suffix of `reverse(s)` — i.e. the longest palindromic prefix of `s`. Prepend the reverse of the remaining tail, then append `s`. O(n) time.

## Kāra features exercised

- **`s.chars().collect()` → `Vec[char]`** for O(1) indexing, and a built `Vec[char]` concatenation (`s + '#' + reverse`) assembled by pushes.
- **KMP failure table in a `Vec[i64]`** — the two-cursor prefix-function with the `len = fail[len-1]` fallback, driven entirely by index arithmetic and `char` equality.
- **`String` assembled with `push(char)`** — the reversed tail then the original, the "read as indices, build with chars" idiom.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`132598368`). Workload: KMP prefix-function (lps) over 259488 sliding windows of a binary-alphabet string; loop-carried failure-fallback kernel.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 342.2 ms | 0.84× |
| **Kāra (codegen)** | 406.6 ms | 1.00× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 417.6 ms | 1.03× |
| Rust `-O` | 424.9 ms | 1.04× |
| Go | 650.3 ms | 1.60× |
| Python (scale lane) | 39.49 s | 97.11× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   shortest_palindrome.kara
karac build shortest_palindrome.kara && ./shortest_palindrome
python3 shortest_palindrome.py
diff <(karac run shortest_palindrome.kara) <(python3 shortest_palindrome.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
