# 244. Shortest Word Distance II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · String · Hash Table · Two Pointers · Design &nbsp;·&nbsp; **Source:** [leetcode.com/problems/shortest-word-distance-ii](https://leetcode.com/problems/shortest-word-distance-ii/) &nbsp;·&nbsp; 🔒 **LeetCode Premium**

Design a structure initialised once with a list of words, which then answers repeated `shortest(word1, word2)` queries — the smallest `|i - j|` over positions `i` holding `word1` and `j` holding `word2`.

```
WordDistance(["practice", "makes", "perfect", "coding", "makes"])

shortest("coding", "practice")  ->  3     indices 3 and 0
shortest("makes",  "coding")    ->  1     indices 4 and 3 — the SECOND "makes"
```

**Constraints:** `1 ≤ wordsDict.length ≤ 3·10⁴`; `1 ≤ wordsDict[i].length ≤ 10`; lowercase English letters; `word1` and `word2` both occur and `word1 != word2`; at most `5·10⁴` calls to `shortest`.

## Approaches

| Approach | Build | Query | Kāra | Python |
|---|---|---|---|---|
| map of position lists + two-pointer merge ★ | O(n²) — see below | O(\|p₁\|+\|p₂\|) | [`shortest_distance_ii.kara`](shortest_distance_ii.kara) ✓ | [`shortest_distance_ii.py`](shortest_distance_ii.py) ✓ |
| map of position lists + binary search | O(n²) — see below | O(min·log max) | [`shortest_distance_binary.kara`](shortest_distance_binary.kara) ✓ | — |
| index-pool indirection + two-pointer merge | **O(n)** | O(\|p₁\|+\|p₂\|) | [`shortest_distance_pool.kara`](shortest_distance_pool.kara) ✓ | — |

`✓` marks agreement with the Python mirror under **interpreter** (`karac run --interp`), **JIT** (`karac run`), and **codegen** (`karac build`), under the default auto-parallelising build and `KARAC_AUTO_PAR=0` alike. All three Kāra variants produce byte-identical output on all four surfaces.

## The mechanism

#243 asks this question **once** against a list, and there the winning answer keeps two integers and never allocates. The sequel changes one word — *repeatedly* — and that word changes the unit of work. A per-query scan re-reads all `n` words to answer a question about the handful of slots that actually hold `word1` or `word2`, so with `5·10⁴` queries against `3·10⁴` words it does 1.5 billion slot visits to extract a few thousand answers.

So pay once. Build `word -> ascending positions` at construction, and the query collapses to a merge over exactly the two lists it cares about:

```
a = b = 0
while a < len(p1) and b < len(p2):
    best = min(best, abs(p1[a] - p2[b]))
    if p1[a] < p2[b]: a += 1
    else:             b += 1
```

Advance whichever cursor is behind. The one that is ahead can only get farther from its partner, so the pair it would form next is never better — the same argument that makes #243's two-last-seen-indices scan correct, just run over two explicit lists instead of the live scan. Positions arrive in ascending order for free because construction walks the list left to right, so nothing is ever sorted.

The **binary-search** variant walks the shorter list and binary-searches the longer one for each entry, checking both sides of the insertion point. It trades `O(|p₁| + |p₂|)` for `O(min · log max)`, which loses for two words of comparable frequency and wins decisively when one is rare and the other is everywhere — `"the"` against a hapax. Real query workloads are skewed that way, which is why it is worth writing rather than a curiosity. Both variants run against the same inputs and must agree exactly, which is what makes the pair useful: two independent implementations of one specification.

## What it found

**A quantified performance gap in a bread-and-butter idiom — [kara `B-2026-08-03-9`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl), open, high.**

Kāra has no in-place mutation of a map **value**. So extending a word's position list is a read-**clone**-modify-reinsert — `get` yields a borrow, the map still owns the list until the reinsert lands, so the clone is not optional:

```kara
match index.get(w) {
    Some(existing) => {
        let mut hits: Vec[i64] = existing.clone();   // <-- FULL COPY
        hits.push(i);
        let _ = index.insert(w, hits);
    }
    ...
}
```

Appending the k-th occurrence of a key therefore copies `k-1` elements, and building the index for a key seen `k` times costs **O(k²)**. Every mirror language does it in O(k): Python `setdefault(w, []).append(i)`, Rust `entry(w).or_default().push(i)`, Go `m[w] = append(m[w], i)`, C++ `m[w].push_back(i)`.

Measured on the degenerate single-key case (`"the"` repeated n times), `KARAC_AUTO_PAR=0` AOT build against CPython 3 on the same machine:

| n | Kāra | CPython |
|---|---|---|
| 32,000 | 0.10 s | 0.004 s |
| 64,000 | 0.52 s | 0.011 s |
| 96,000 | 5.60 s | 0.009 s |
| 128,000 | **13.37 s** | 0.013 s |

Four times the input costs Kāra 134× the time while CPython stays flat — at n=128,000 Kāra is roughly **1000× slower than CPython** doing identical work. It is not the buffer cache: `KARAC_BUF_CACHE=0` reproduces the same curve.

The gap has an in-language escape, which is the third variant. Routing the lists through an index indirection — `Map[String, i64]` for word→slot plus a side `Vec[Vec[i64]]` — makes the append `lists[s].push(i)`, which mutates in place:

| n | direct `Map[K, Vec[V]]` | index-pool |
|---|---|---|
| 32,000 | 0.10 s | 0.00 s |
| 64,000 | 0.49 s | 0.00 s |
| 96,000 | 5.98 s | 0.00 s |
| 128,000 | 14.21 s | 0.00 s |

So it is a performance **trap**, not a wall — and it stays filed as high anyway, because the trap is silent (nothing in `karac check` warns; the code compiles clean and answers correctly, only slowly) and because the direct phrasing is what every mirror language's idiom translates to, so it is what a newcomer writes first. The indirection is a known corpus workaround (#49's `count_signature.kara` uses the same trick) rather than something the language guides anyone toward.

**The direct phrasing is kept as the primary kata file.** Per the corpus rule the gap is filed, not routed around: `shortest_distance_ii.kara` stays written the natural way, and `shortest_distance_pool.kara` sits beside it as the phrasing that scales today.

One thing deliberately **not** claimed: the step from n=64,000 to n=96,000 is 10.6× for 1.5× the input, steeper than the quadratic the construction explains. Ruling out the buffer cache did not identify what it is. A plausible reading is the clone's working set (source + destination, 2 × 768 KB at n=96,000) outgrowing L2 so every copy streams from DRAM — but that was not confirmed, and it is recorded in the ledger entry as an open observation rather than a finding.

**No correctness bugs.** All three variants agreed with the oracle on the first clean compile, on all four surfaces.

## Kāra features exercised

- **`Map[String, Vec[i64]]` — a heap-of-heaps map value**, built by read-clone-modify-reinsert, and the ownership surface that entails: the displaced old `Vec[i64]` is freed by the discard of `insert`'s `Option` result on every append.
- **Nested `match` over two map lookups, merging through the borrows.** Both `get`s stay borrows and the merge reads straight through them — nothing is cloned in the query path. That is load-bearing, not tidiness: a `positions() -> Vec[i64]` helper would copy both lists on every query, making the Kāra query `O(|p₁| + |p₂|)` *allocation* where the C mirror does none, and the benchmark would then be comparing two different algorithms.
- **`lists[s].push(i)` — in-place append into a `Vec[Vec[i64]]` element** (index-pool variant), the operation whose absence for map values is the finding above.
- **Binary search over a borrowed map-held `Vec[i64]`** — `lower_bound` plus a both-sides insertion-point check, entirely through a borrow.
- **`ref Slice[String]` — the borrow, spelled out.** A bare `Slice[T]` parameter consumes its argument, so the constructor declares `ref` (settled language design, ledger `B-2026-07-01-10`).
- **`Array[String, N]` coercing into `ref Slice[String]`** at six call sites with no copy.
- **`min` as a generic `std.cmp` free function**, and **`.abs()`** on a difference of indices.
- **struct + free functions, no `impl` blocks** — the corpus idiom for design katas (#170, #208, #232).

## Running

```bash
# Kāra — all three variants, all backends, same output.
karac run   shortest_distance_ii.kara
karac run   shortest_distance_binary.kara
karac run   shortest_distance_pool.kara
karac build shortest_distance_ii.kara && ./shortest_distance_ii

# Python
python3 shortest_distance_ii.py

# Verify they agree
for v in shortest_distance_ii shortest_distance_binary shortest_distance_pool; do
    diff <(karac run $v.kara) <(python3 shortest_distance_ii.py) && echo "$v OK"
done
```

## Notes

Verified byte-identical under `karac run --interp` (tree-walk), `karac run` (JIT), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — with all three Kāra variants agreeing with the Python mirror.

**Why this kata earns its place next to #243.** They share a merge and nothing else. #243 measures plain `String` equality in a linear scan and lands in a near dead heat across five languages, because there is almost nothing for a compiler to differentiate on. #244 moves the work into the *map*: two hash lookups and a two-pointer walk per query, with the list built once. That is the path where the corpus has repeatedly found Kāra behind — [#127](../../101-200/127-word-ladder/) and [#126](../../101-200/126-word-ladder-ii/) put Kāra 3.6× behind C with the same `String` type inside a hash-keyed BFS, while #243's map-free scan is within 1.06×. This kata isolates that difference deliberately: same problem family, same string handling, map moved from incidental to central.

The empty-list convention is shared with #243 on purpose. `best` starts at the list length rather than a sentinel — the list has that many slots, so no two distinct positions can be that far apart, which makes it a genuine upper bound that doubles as the "word never appeared" answer with no separate found flag. LeetCode guarantees both words are present; the kata reports that case rather than trapping on it, which is why `["one","two","three"]` queried for `"four"` is in the test set of both katas.
