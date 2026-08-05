# 211. Design Add and Search Words Data Structure

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String · Depth-First Search · Design · Trie &nbsp;·&nbsp; **Source:** [leetcode.com/problems/design-add-and-search-words-data-structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/)

Design a dictionary supporting `add_word(word)` and `search(word)`, where a search string may contain the wildcard `.` matching **any single character**. Everything else is an ordinary trie lookup. The wildcard is the whole problem: it turns a linear walk into a branching search.

```
add_word("bad"); add_word("dad"); add_word("mad")

search("pad")  -> false     never added
search("bad")  -> true      exact
search(".ad")  -> true      matches bad / dad / mad
search("b..")  -> true      matches bad
search("...")  -> true      any 3-letter word
search("....") -> false     no 4-letter word exists
```

**Constraints:** `1 ≤ word.length ≤ 25`; `add_word` takes lowercase English letters; `search` takes lowercase letters and `.`; at most 2 dots per search; at most 10⁴ calls total.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **index-pool trie + backtracking DFS** ★ | [`word_dictionary.kara`](word_dictionary.kara) ✓ | [`word_dictionary.py`](word_dictionary.py) ✓ |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike, and all four agree with the Python mirror.

## The mechanism

The store is the **same index-pool trie as [#208](../208-implement-trie-prefix-tree/)**: every node lives in one `Vec[TrieNode]` (root at index 0), children are a `Map[char, i64]` of next-character → child index, and `is_end` flags a terminal. Because nodes reference each other by integer index rather than by handle, the pool can grow with `push` during a walk without invalidating anything already held.

`add_word` is the plain walk-and-create insert — follow the edge for each character, minting a node when the edge is absent, then flag the final node. Unchanged from #208.

`search` is where this kata departs. A literal character has exactly one edge to follow, so it stays a walk; a `.` has no single edge and must try **every** child, succeeding if any branch matches the remaining suffix. That is backtracking, so the walk becomes a recursion:

```
dfs(idx, pos):
    if pos == len:        return is_end[idx]        # consumed the pattern
    if pattern[pos] == '.':
        for (_, child) in children[idx]:            # fan out over every edge
            if dfs(child, pos + 1): return true
        return false
    child = children[idx].get(pattern[pos])
    return child != -1 and dfs(child, pos + 1)      # single edge, no branching
```

The cost split is worth naming: a wildcard-free query is O(len) exactly as in #208, while each `.` multiplies the search frontier by that node's out-degree. LeetCode's "at most 2 dots" constraint is what keeps the worst case tame.

## Kāra features exercised

- **Recursion returning `bool` with early exit** — `if dfs(...) { return true; }` inside the fan-out loop is the backtracking short-circuit; the recursion is the natural expression of the wildcard and is deliberately not flattened into an explicit stack.
- **`for (_, child) in nodes[idx].children`** — destructuring iteration over a `Map[char, i64]` reached *through* an indexed pool element, discarding the key with `_` because a `.` matches regardless of which edge it takes.
- **`ref` vs `mut ref` split across the API** — `add_word` takes `mut ref Vec[TrieNode]` (it grows the pool and flags nodes); `dfs`, `child_of` and `search` take plain `ref`, so the read-only traversal cannot accidentally mutate the trie it is walking.
- **`Option` unwrapped through a helper** — `child_of` matches `children.get(c)` into a plain `i64`, returning the `-1` sentinel for "no edge", which keeps the sentinel comparison out of the recursive hot path.
- **`Map[char, i64]` as a struct field**, mutated in place through a pool index (`nodes[cur].children.insert(c, new_idx)`) — the #208 surface, re-exercised here under a branching reader.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`262567`). Workload: build a 20k-word index-pool trie once, then match 8M PRNG wildcard patterns via backtracking DFS; sink = count of matches.

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-07-27 (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 158.2 ms | 0.86× |
| Rust `-O` | 158.9 ms | 0.86× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 164.2 ms | 0.89× |
| **Kāra (codegen)** | 184.3 ms | 1.00× |
| Go | 198.3 ms | 1.08× |

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   word_dictionary.kara
karac build word_dictionary.kara && ./word_dictionary

# Python
python3 word_dictionary.py

# Verify they agree
diff <(karac run word_dictionary.kara) <(python3 word_dictionary.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — and agrees with the Python mirror on all twelve queries.

**The benchmark measures a different representation than the kata ships, deliberately.** [`word_dictionary.kara`](word_dictionary.kara) uses `Map[char, i64]` children, matching #208 and reading the way the problem is normally written. The bench mirror ([`bench/word_dictionary.kara`](bench/word_dictionary.kara)) instead uses a **flat `Vec[i64]` child array** indexed `cur * alpha + c` over a 6-letter alphabet, because C, Rust and Go would each reach for a different map implementation and the comparison would become a hash-table benchmark rather than a codegen one. The consequence is that the numbers above say nothing about Kāra's `Map[char, i64]` performance — that path is exercised by the correctness run, not the timed one.

The bench is **build-once + punch** per BENCHMARKS.md: a 20,000-word trie is built once, then 8M PRNG patterns are matched, each position independently a wildcard with probability ⅙. The trie is sized so only a fraction of patterns match (sink `262567`), which keeps the sink discriminating rather than saturating at "everything matches". The recursion's data-dependent branching does not vectorise, which is the point — this is a pointer-chase-and-backtrack kernel, the shape where a bounds-checked indexed read costs most against C's raw pointer arithmetic.

## What this kata surfaced

**A codegen-only map-iterator leak — now fixed in `karac`.** [`B-2026-07-23-1`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl): an early `return` out of a `for (k, v) in map` / `for x in set` loop leaked the `karac_map_iter_new` handle. The matching `karac_map_iter_free` was emitted **only in the loop's exit block** — normal exhaustion and `break` both branch through it, but an early `return` routes to the function-exit cleanup drain, which had no record of the iterator. One 16-byte block leaked per early return.

The wildcard search is exactly the shape that finds this: `'.'` fans out across every child and returns the moment a match is found, so the common path is an early `return` from inside a map iteration. Output was correct throughout and the interpreter is GC-clean, so nothing but a leak check on the compiled binary would have caught it — which is why the corpus runs valgrind on `karac build` output rather than trusting agreement with the Python mirror.
