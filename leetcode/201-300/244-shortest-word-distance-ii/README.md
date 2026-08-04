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
| map of position lists + two-pointer merge ★ | **O(n)** | O(\|p₁\|+\|p₂\|) | [`shortest_distance_ii.kara`](shortest_distance_ii.kara) ✓ | [`shortest_distance_ii.py`](shortest_distance_ii.py) ✓ |
| map of position lists + binary search | **O(n)** | O(min·log max) | [`shortest_distance_binary.kara`](shortest_distance_binary.kara) ✓ | — |
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

**A self-inflicted 1736× slowdown, and the discoverability gap behind it — [kara `B-2026-08-03-9`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl), reframed.**

This kata originally built its index with a read-**clone**-modify-reinsert, on the stated belief that *"Kāra has no in-place mutation of a map value"* — `get` yields a borrow, the map still owns the list until a reinsert lands, so the clone looked mandatory:

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

**That belief was false.** Kāra has *two* in-place paths, and both shipped before this kata was written:

```kara
index.entry(w).or_insert(Vec.new()).push(i);   // Entry API — what this kata uses now
index[w].push(i);                              // index-assign — as #332 already did
```

`entry(k)` returns a view of that key's slot; `or_insert` yields a `mut ref Vec[i64]` — the map's own list when the key is present, a freshly-inserted empty one when it is not — so the `push` lands through the borrow and nothing is copied. It is the direct analogue of Python's `setdefault(w, []).append(i)` and Rust's `entry(w).or_default().push(i)`.

Measured on the degenerate single-key case (`"the"` repeated n times), `KARAC_AUTO_PAR=0` AOT build, same machine, before and after:

| n | clone-reinsert (before) | `entry` (after) | speedup |
|---|---|---|---|
| 32,000 | 0.10 s | 0.006 s | 18× |
| 64,000 | 0.52 s | 0.006 s | 87× |
| 96,000 | 5.02 s | 0.008 s | 643× |
| 128,000 | **13.89 s** | **0.008 s** | **1736×** |

The before column is quadratic — appending the k-th occurrence of a key copies k−1 elements. The after column is flat and lands in CPython's range (0.004–0.013 s across the same sweep). The complexity class was never the language's; it was this file's.

**What the kata actually found is a discoverability gap.** Nothing leads an author from `get`/`insert` to `entry`, and nothing in `karac check` flags the clone-reinsert shape — it compiles clean and answers correctly, only slowly. That gap is real enough to have cost this kata a complexity class, spawned a whole extra variant written to dodge it, and been recorded as a language limitation in three separate places before anyone tested the alternative. The ledger entry is reframed from `perf`/high to `diagnostics`/medium, with a lint offering `entry().or_insert()` as the durable close.

The earlier note about the n=64,000→96,000 step being 10.6× for 1.5× the input — steeper than the quadratic explains — applies only to the removed clone phrasing and is left in the ledger as an open observation about that construction, not about the language.

**No correctness bugs.** All three variants agreed with the oracle on the first clean compile, on all four surfaces.

## Kāra features exercised

- **`Map[String, Vec[i64]]` — a heap-of-heaps map value**, built through `entry(k).or_insert(..)`, which hands back a `mut ref` into the map's own slot so each append lands in place with no copy and no displaced list to free.
- **Nested `match` over two map lookups, merging through the borrows.** Both `get`s stay borrows and the merge reads straight through them — nothing is cloned in the query path. That is load-bearing, not tidiness: a `positions() -> Vec[i64]` helper would copy both lists on every query, making the Kāra query `O(|p₁| + |p₂|)` *allocation* where the C mirror does none, and the benchmark would then be comparing two different algorithms.
- **`lists[s].push(i)` — in-place append into a `Vec[Vec[i64]]` element** (index-pool variant), the same in-place append the direct phrasing gets from `entry(..).or_insert(..)`, reached through an explicit slot table instead.
- **Binary search over a borrowed map-held `Vec[i64]`** — `lower_bound` plus a both-sides insertion-point check, entirely through a borrow.
- **`ref Slice[String]` — the borrow, spelled out.** A bare `Slice[T]` parameter consumes its argument, so the constructor declares `ref` (settled language design, ledger `B-2026-07-01-10`).
- **`Array[String, N]` coercing into `ref Slice[String]`** at six call sites with no copy.
- **`min` as a generic `std.cmp` free function**, and **`.abs()`** on a difference of indices.
- **struct + free functions, no `impl` blocks** — the corpus idiom for design katas (#170, #208, #232).

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup), clang, go
./bench/bench.sh
```

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic LCG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`956710020`). Workload: build a 20,000-word list over a 256-word vocabulary and index it **once**, then 200,000 punches of the two-pointer merge query, each for a different `(word1, word2)` vocabulary pair; sink is a rolling polynomial hash of the distances, a loop-carried dependency so the punch loop is sequential by construction.

Every word is 9 bytes sharing the 5-byte prefix `"delta"`, so hashing walks the whole key and no lookup discriminates on length or first byte; every one of the 20,000 slots holds its own copy, so no lane can shortcut on operands sharing a data pointer (Go's `strings.Clone` is load-bearing for exactly that reason). The C mirror uses a **real dynamic open-addressing map** that grows on load factor, not a table pre-sized to the known vocabulary — a pre-sized table would hand C a free win the other four don't get.

**The bench builds the index with the index-pool phrasing, not the direct one.** The original reason — that the direct build was quadratic — no longer holds: `entry(..).or_insert(..)` makes it O(n), so either phrasing would now be an honest comparison against the four mirrors. The bench is left on the index-pool spine so its published numbers stay comparable with the runs already in `bench-results.json`; re-basing it on the direct phrasing is a separate change that should re-measure all five languages together.

### Runtime — sequential lane

Container x86-64, 2026-08-03, hyperfine 30 runs, `KARAC_AUTO_PAR=0`, every lane 99–101% CPU. `karac` commits to a **v3** deploy baseline, so `c_v3` and `rust_v3` are the ISA-matched comparators — and `rust_v3` is *also* overflow-checked, which makes it the equal-safety twin.

| Impl | Mean ± σ | vs Kāra |
|---|---|---|
| C `clang -O3` | 110.4 ± 4.7 ms | 0.72× |
| Rust `-O` (wrapping) | 112.5 ± 3.8 ms | 0.73× |
| C `clang -O3` @ x86-64-v3 | 116.8 ± 15.1 ms | 0.76× |
| **Kāra (codegen)** | **153.1 ± 14.6 ms** | 1.00× |
| Go | 177.7 ± 10.9 ms | 1.16× |
| Rust overflow-checked @ x86-64-v3 (equal-safety, ISA-matched) | 235.8 ± 7.5 ms | 1.54× |
| Rust `-O -C overflow-checks=on` | 256.6 ± 14.6 ms | 1.68× |

**Kāra is 1.31× behind ISA-matched C and 1.54× ahead of equal-safety Rust.**

Two things worth separating.

**The map costs Kāra something, and the size of it is the finding.** This kata was written to isolate exactly that. [#243](../243-shortest-word-distance/) runs the same `String` type through a map-free linear scan and lands within **1.06×** of C; [#126](../../101-200/126-word-ladder-ii/) and [#127](../../101-200/127-word-ladder/) put the same type inside a hash-keyed BFS and land **3.6×** behind. The prediction was that #244 would fall between them, and it does — **1.31×**. That is informative in a way a single number isn't: two hash lookups per query over a 256-key map cost about a third, so whatever makes word-ladder 3.6× is *not* simply "the map, in proportion to how much you use it." Something else is going on in those two, and this measurement does not explain it.

**Overflow checks are expensive here — and that is Rust's cost, not Kāra's.** `rustc -O` wrapping is 112.5 ms; the identical code with `-C overflow-checks=on` is 256.6 ms, a **2.28×** penalty. In #243 the same flag cost Rust nothing (115.5 → 115.2 ms), because that loop does no arithmetic worth checking. This one does: a subtraction, an `abs`, and two comparisons per merge step across 200,000 × ~156 steps, plus the sink's multiply-add. Kāra checks integer overflow **by default** and still lands at 153.1 ms. The honest reading is narrow: Kāra's checked arithmetic is materially cheaper than Rust's opt-in overflow checking on an arithmetic-dense loop. It is *not* that Kāra beats Rust here — the wrapping row plainly says otherwise.

### Caveats

This is the **container-x86 lane**, which [`BENCHMARKS.md`](../../../BENCHMARKS.md) treats as a corroborating second host with a noise floor around 1.15×. Read nothing below that from it: both headline ratios (1.31×, 1.54×) clear it comfortably, but the Go margin (1.16×) does not and should be read as a **tie**. Note also the σ spread — Kāra's 14.6 ms and C-v3's 15.1 ms are wide enough that the two C rows are not distinguishable from each other.

The **M5 Pro host lane (`results.json`) has not been measured.** This kata is new and there is no Apple-silicon run yet, so `consolidate-bench.sh` will correctly report it as missing, and this kata does not yet appear in the consolidated feed or the graphs. That is pending work, not an omission.

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
