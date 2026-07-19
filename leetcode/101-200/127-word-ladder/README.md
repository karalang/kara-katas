# 127. Word Ladder

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** BFS · Hash Table · String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/word-ladder](https://leetcode.com/problems/word-ladder/)

Return the length of the **shortest** transformation sequence from `beginWord` to `endWord` — one letter changed per step, every intermediate word in the list — counting both endpoints, or `0` if none exists.

```
begin = "hit", end = "cog", words = [hot,dot,dog,lot,log,cog]  ->  5   (hit·hot·dot·dog·cog)
begin = "hit", end = "cog", words = [hot,dot,dog,lot,log]      ->  0   (cog absent)
begin = "red", end = "tax", words = [ted,tex,red,tax,tad,…]    ->  4
```

**Constraints:** `1 ≤ word length ≤ 10`, `1 ≤ wordList.length ≤ 5000`, all lowercase, equal length.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Level-order BFS** ★ | [`word_ladder.kara`](word_ladder.kara) ✓ | [`word_ladder.py`](word_ladder.py) ✓ |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the Kāra solver agrees with the Python mirror. The scalar answers are validated against known LeetCode values (hit→cog 5, red→tax 4, plus 0/2/3/hypercube-4 cases). The solver compiles with zero diagnostics and is valgrind-clean.

## The mechanism

**Level-order BFS** ([`word_ladder.kara`](word_ladder.kara), the ★). Seed the frontier with `begin`; each round, expand every word in the frontier to its one-letter-changed neighbours present in the word set, enqueueing the unvisited ones into the next frontier. The round at which `end` first appears is the answer. `word_set` and `visited` are `Map[String, i64]` used as sets; neighbours are rebuilt with `String.push(char)` and membership-checked. This is the length-only sibling of [#126 Word Ladder II](../126-word-ladder-ii/), which reconstructs *all* shortest ladders — #127 keeps only the depth counter, so no predecessor map or DFS is needed.

## Kāra features exercised

- **`Map[String, i64]` as a set** — `word_set` membership and `visited` dedup.
- **BFS frontier swap `cur = nxt`** — a whole-`Vec[String]` reassignment (the construct whose element-leak `#126` fixed via [kara `B-2026-07-18-52`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl); #127 is valgrind-clean on that same path).
- **Owned-`String` collection storage with `.clone()`** — the key stored into `visited` is cloned at the consuming site.
- **`String.push(char)` neighbour construction** and **modular sink fold** (Kāra checks integer overflow by default, so the running digest is reduced mod 1e9+7).

## Running

```bash
karac run   word_ladder.kara
karac build word_ladder.kara && ./word_ladder
python3 word_ladder.py
diff <(karac run word_ladder.kara) <(python3 word_ladder.py) && echo OK
```

## Notes

Dogfood-first kata (small BFS workload; LeetCode caps `wordList` at 5000), so no cross-language benchmark — [#124](../124-binary-tree-maximum-path-sum/) is the neighbouring benchmark data point. It shares the [#126](../126-word-ladder-ii/) BFS/`Map`/`String` machinery and confirms that path is leak-clean after `B-2026-07-18-52`.
