# 126. Word Ladder II

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** BFS · Backtracking · Hash Table · String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/word-ladder-ii](https://leetcode.com/problems/word-ladder-ii/)

Given `beginWord`, `endWord`, and a `wordList`, return **every** shortest transformation sequence from `beginWord` to `endWord` — changing exactly one letter per step, with every intermediate word in the list. Return `[]` if none exists.

```
begin = "hit", end = "cog", words = [hot,dot,dog,lot,log,cog]
  -> [[hit,hot,dot,dog,cog], [hit,hot,lot,log,cog]]        (2 shortest ladders, length 5)

begin = "hit", end = "cog", words = [hot,dot,dog,lot,log]  (no cog)   -> []
begin = "red", end = "tax", words = [ted,tex,red,tax,tad,den,rex,pee] -> 3 ladders, length 4
```

**Constraints:** `1 ≤ word length ≤ 10`, `1 ≤ wordList.length ≤ 500`, all lowercase, all equal length.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **BFS level-graph + DFS reconstruction** ★ | [`word_ladder_ii.kara`](word_ladder_ii.kara) ✓ | [`word_ladder_ii.py`](word_ladder_ii.py) ✓ |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the Kāra solver agrees with the Python mirror. The oracle is validated against the **known LeetCode answers** (hit→cog = 2 ladders/len 5, red→tax = 3/len 4, an a/b hypercube = 6/len 4, plus the two 0-ladder cases). The solver compiles with zero errors and is valgrind-clean.

> **Compiler bug surfaced & fixed by this kata.** The BFS advances its frontier with `cur = nxt` — a whole-`Vec[String]` variable reassignment. Under `karac build` this freed only the old Vec's outer `{ptr,len,cap}` buffer and **stranded every element String** (a leak per BFS level). The move-overwrite eager-free handled `Vec[shared]` elements but bailed for a value `String` element. Fixed in the compiler ([kara `B-2026-07-18-52`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl)) — a `String`/nested-`Vec` value element now drains through the same recursive walk the scope-exit cleanup uses. The kata is now valgrind-clean on every surface.

## The mechanism

**BFS level-graph + DFS reconstruction** ([`word_ladder_ii.kara`](word_ladder_ii.kara), the ★). Two phases:

1. **BFS building predecessors.** Expand a frontier one letter at a time. For each newly-reached word, record **all** predecessors at the previous level — a word is committed to `visited` only *after* the whole level, so multiple same-level parents are captured (that is what produces *multiple* shortest ladders). Stop at the level that first reaches `end`.
2. **DFS reconstruction.** Walk the predecessor map back from `end` to `begin`, emitting each shortest path. The running path is threaded through the recursion; when it reaches `begin`, the ladder is complete.

To keep the oracle deterministic without pinning a ladder order, the solver reports per case `count` (number of ladders), `len` (ladder length), and an **order-independent digest** (the sum of per-ladder hashes), then folds a global sink — the [#113](../113-path-sum-ii/) discipline.

## Kāra features exercised

- **`Map[String, Vec[String]]` predecessor map** — get-or-default, `push`, re-insert; the richest nested-collection shape in the corpus so far.
- **`Map[String, i64]` as a set** — `word_set` / `visited` / per-level `in_next` frontier dedup.
- **BFS frontier swap `cur = nxt`** — a whole-`Vec[String]` variable reassignment (the construct that surfaced `B-2026-07-18-52`).
- **`mut ref` accumulators threaded through recursion** — the DFS carries the path `Vec[String]` plus `count`/`digest` as `mut ref` out-params (the in-scope `mut ref` forwards without a call-site marker; parity with [#124](../124-binary-tree-maximum-path-sum/)).
- **Owned-`String` collection storage with `.clone()`** — Strings stored into two collections (a map key and a frontier Vec) are cloned at the consuming site, the idiomatic ownership pattern the Rust mirror would also use.
- **`String.push(char)` neighbour construction** — rebuild each one-letter-changed candidate, checked against the word set.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   word_ladder_ii.kara
karac build word_ladder_ii.kara && ./word_ladder_ii

# Python
python3 word_ladder_ii.py

# Verify they agree
diff <(karac run word_ladder_ii.kara) <(python3 word_ladder_ii.py) && echo OK
```

## Notes

This is a **dogfood-first** kata: its value is exercising the compiler's nested-collection and ownership machinery on a genuinely hard graph search (it found `B-2026-07-18-52`). The workload is small (LeetCode caps `wordList` at 500), so there is no cross-language benchmark — the [#124](../124-binary-tree-maximum-path-sum/) tree traversal is the neighbouring benchmark data point.
