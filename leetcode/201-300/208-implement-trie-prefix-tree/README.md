# 208. Implement Trie (Prefix Tree)

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Trie · Hash Table · Design &nbsp;·&nbsp; **Source:** [leetcode.com/problems/implement-trie-prefix-tree](https://leetcode.com/problems/implement-trie-prefix-tree/)

Build a **trie** (prefix tree) supporting three operations:

- `insert(word)` — add a word.
- `search(word)` — `true` iff the exact word was inserted.
- `starts_with(prefix)` — `true` iff any inserted word has this prefix.

```
insert("apple")
search("apple")      -> true
search("app")        -> false   (a prefix, never inserted as a word)
starts_with("app")   -> true
insert("app")
search("app")        -> true
```

**Constraints:** words and prefixes are lowercase `a–z`, `1 ≤ length ≤ 2000`, up to 3·10⁴ operations.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **index-pool trie, `Map[char,i64]` children** ★ | [`trie.kara`](trie.kara) | [`trie.py`](trie.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Each node maps a next-character to a child node and carries an `is_end` flag. All nodes live in a single pool (`Vec[TrieNode]`, root = index 0) and reference their children by integer index — the same allocation-free arena idiom the linked-list and tree katas use, here with a `Map[char, i64]` edge table per node instead of fixed child slots.

`insert` walks the word one character at a time; whenever the needed child edge is absent it mints a fresh node (pushed to the pool) and records the edge, then flags the terminal node `is_end`. `search` and `starts_with` share a single `walk` that follows edges as far as the input goes, returning the node reached or `-1` on a missing edge — `search` additionally checks `is_end`, while `starts_with` only needs the walk to succeed. Each operation is O(length).

## Kāra features exercised

- **`Map[char, i64]` as a struct field** — a `char`-keyed edge table living inside a `TrieNode`, mutated in place through an indexed pool element (`nodes[cur].children.insert(c, idx)`) and read via `.get(c) → Option`.
- **Index-pool arena** — `Vec[TrieNode]` grown by `push` during traversal while integer indices stay stable across the growth.
- **`mut ref` vs `ref` split** — `insert` takes `mut ref Vec[TrieNode]` (it grows the pool and flags nodes); `search` / `starts_with` / `walk` take `ref` (read-only traversal).
- **`char`-keyed map ownership** — the whole `Vec[TrieNode]`, each element owning a heap `Map`, drops cleanly (valgrind-verified).

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`14588245`). Workload: build a 30k-word index-pool trie once, then walk 8M PRNG query words (data-dependent pointer-chase; sink = weighted prefix+exact hits).

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 236.4 ms | 0.82× |
| Rust `-O` | 242.2 ms | 0.84× |
| Go | 253.2 ms | 0.88× |
| **Kāra (codegen)** | 288.5 ms | 1.00× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 288.9 ms | 1.00× |
| Python (scale lane) | 11.79 s | 40.87× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   trie.kara
karac build trie.kara && ./trie
python3 trie.py
diff <(karac run trie.kara) <(python3 trie.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
