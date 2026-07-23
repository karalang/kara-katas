# 212. Word Search II

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Trie · Backtracking · Matrix · DFS &nbsp;·&nbsp; **Source:** [leetcode.com/problems/word-search-ii](https://leetcode.com/problems/word-search-ii/)

Given an `m x n` board of characters and a list of words, return every word that can be spelled by a path of **orthogonally adjacent** cells (up/down/left/right), using each cell at most once per word.

```
board = o a a n     words = ["oath","pea","eat","rain"]
        e t a e
        i h k r     ->  ["eat","oath"]
        i f l v
```

**Constraints:** `1 ≤ m, n ≤ 12`, `1 ≤ words.length ≤ 3·10⁴`, words are lowercase letters.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **trie + board DFS** ★ | [`word_search_ii.kara`](word_search_ii.kara) | [`word_search_ii.py`](word_search_ii.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Running the single-word Word Search once per word re-walks the board thousands of times. Instead, build a **trie** of all the words and sweep the board **once**, descending the trie in lockstep with the DFS. From a cell, follow the trie's child edge for that cell's letter; if there is no such edge the entire branch is dead and gets pruned — that pruning is what turns a brute-force blow-up into something fast. A trie node flagged as a word-end means the path spelled a target word, so it's collected, and the flag is **cleared** so the same word is reported once even if the board contains it in several places.

Cells are marked visited (overwritten with a sentinel) while a branch explores and restored on the way back out — ordinary backtracking, but shared across all words at once because the trie carries every target simultaneously. Results are sorted for a canonical order.

This is [#208](../208-implement-trie-prefix-tree/)'s trie fused with grid backtracking — a strictly richer traversal than either the plain trie or plain Word Search.

## Kāra features exercised

- **Trie + grid together** — an index-pool `Vec[TrieNode]` (children a `Map[char, i64]`) driving a DFS over a mutable `Vec[Vec[char]]` board, with in-place cell marking (`board[r][c] = '#'`) and restore.
- **Four `mut ref` parameters through recursion** — `board`, `nodes`, `path`, and `results` all thread through `dfs`; the top-level call marks the fresh owned bindings (`dfs(board, …, mut nodes, …, mut path, mut results)`) while recursive calls forward the already-`mut ref` bindings unmarked.
- **`Vec[String]` selection sort** via parallel-assignment swap (`v[i], v[j] = v[j], v[i]`) with `String` `<` comparison, and `String` built from a `Vec[char]` path via `push(char)`.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`16961616561`). Workload: build a 4k-word trie once, then run the trie-guided 12x12 board DFS over 40k fresh PRNG boards; sink = traversal checksum.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 460.7 ms | 0.60× |
| Rust `-O` | 560.9 ms | 0.72× |
| Go | 612.7 ms | 0.79× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 651.9 ms | 0.84× |
| **Kāra (codegen)** | 774.1 ms | 1.00× |
| Python (scale lane) | 20.80 s | 26.87× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   word_search_ii.kara
karac build word_search_ii.kara && ./word_search_ii
python3 word_search_ii.py
diff <(karac run word_search_ii.kara) <(python3 word_search_ii.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean (no leak despite the mutable board, per-node `Map` children, and `Vec[String]` result churn). Oracle-only.
