# 243. Shortest Word Distance

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Array · String · Two Pointers &nbsp;·&nbsp; **Source:** [leetcode.com/problems/shortest-word-distance](https://leetcode.com/problems/shortest-word-distance/) &nbsp;·&nbsp; 🔒 **LeetCode Premium**

Given a list of words and two **different** words that both occur in it, return the smallest `|i - j|` over positions `i` holding `word1` and `j` holding `word2`.

```
["practice", "makes", "perfect", "coding", "makes"]

"coding", "practice"  ->  3     indices 3 and 0
"makes",  "coding"    ->  1     indices 4 and 3 — the SECOND "makes"
```

**Constraints:** `2 ≤ wordsDict.length ≤ 3·10⁴`; `1 ≤ wordsDict[i].length ≤ 10`; lowercase English letters; `word1` and `word2` both occur in the list and `word1 != word2`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **two last-seen indices, one pass** ★ | [`shortest_distance.kara`](shortest_distance.kara) ✓ | [`shortest_distance.py`](shortest_distance.py) ✓ |
| index lists + two-pointer merge | [`shortest_distance_lists.kara`](shortest_distance_lists.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike, and both variants agree with the Python mirror on all eight cases.

## The mechanism

The insight is that **you never need to remember more than one position per word.** Walking left to right, when the scan lands on `word1` at index `i`, the only `word2` that can improve the answer is the *most recent* one — every earlier `word2` is strictly farther from `i`, and every later `word2` gets its own turn when the scan reaches it and looks back at this `word1`. So two integers suffice:

```
last1 = last2 = -1
for i in 0..n:
    if words[i] == word1: last1 = i; if last2 >= 0: best = min(best, last1 - last2)
    elif words[i] == word2: last2 = i; if last1 >= 0: best = min(best, last2 - last1)
```

One pass, O(n) time, O(1) space, and no candidate pair is skipped. The symmetry is what makes it work: each hit only ever looks *backwards* at the other word, and between them the two branches cover every cross-pair exactly once.

`best` starts at `n` rather than at a sentinel. The list has `n` slots, so no two distinct positions can be `n` or more apart — `n` is a genuine upper bound that doubles as the "word never appeared" answer without a separate found flag. LeetCode guarantees both words are present; the kata reports that case rather than trapping on it, which is why `["one","two","three"]` with `"four"` is in the test set.

The second variant collects **every** position of each word and merges the two ascending lists with a two-pointer walk, advancing whichever cursor is behind. Same O(n) time but O(n) space and two passes, so for a single query it is strictly the worse way. It earns its place because it is the shape that survives the sequel: [#244](https://leetcode.com/problems/shortest-word-distance-ii/) asks the same question repeatedly against a fixed list, and the answer there is to build these position lists *once* and leave only the merge in the query path. Here they are rebuilt per call — the honest starting point for #244, and a distinct compiler surface (`Vec[i64]` growth, `.abs()`, two cursors).

## Kāra features exercised

- **`ref Slice[String]` — the borrow, spelled out.** A *bare* `Slice[T]` parameter consumes its argument: Kāra declares parameter modes on the callee (`ref` = borrow, bare = move) and call sites never write `ref`, so `fn report(words: Slice[String], ...)` called twice on one array is a genuine use-after-move. `ref` is the fix, and both variants call `report` eight times over six arrays on the strength of it.
- **String equality against a borrowed operand** — `words[i] == word1` compares an indexed `Slice` element with a `ref String`, the kata's entire inner loop.
- **`else if` on mutually exclusive arms** — `word1 != word2` is a precondition, so the second test is skipped on a `word1` hit; one comparison less per slot than two independent `if`s.
- **`min` as a generic `std.cmp` free function** — the same stdlib `min` measured in isolation by [#64](../../1-100/64-minimum-path-sum/), here against `a < b ? a : b` in C and `.min()` in Rust.
- **`Array[String, N]` coercing into `ref Slice[String]`** at the call site, six times over, with no copy.
- **`.abs()` on a difference of indices** (merge variant) and `Vec[i64]` grown by `push` in a scan.

## What it found

**No new bugs.** One diagnostic fired, and it was correct: the first draft declared `words: Slice[String]` and called `report` repeatedly on one array, which `karac check` rejected as `E0500 value 'd1' moved here, used again here`. The hint attached to it — *"declare the callee parameter `ref` if it only reads"* — was the fix.

Worth recording, because it looks like a bug and is not: bare `Slice[T]` params consuming their argument is deliberate language design, settled in ledger `B-2026-07-01-10`. That entry offered two fix directions for the same class in the stdlib — declare the params `ref`, or give `Slice[T]` borrow mode by default — and chose the first, declaring `ref Slice[f64]` across `stats.kara`. So bare-means-consume is the intended rule and `ref` is the intended spelling. The narrowing probes that established this (only `Array` of a `Copy` element escapes, because it *is* `Copy`; and the print family borrows via the separate `B-2026-07-02-21` fix, so a call inside an f-string is the one position that looks exempt) are in the session scratchpad, not the corpus — there is nothing here for `oracle/` to demonstrate.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`810985766`). Workload: build a 20,000-word list once over a 256-word vocabulary (every word 9 chars sharing a 5-char prefix, so String equality does real byte work instead of exiting early on a length or first-byte mismatch), then 2,000 punches of the one-pass two-last-seen-index scan, each for a different (word1, word2) vocabulary pair; sink is a rolling polynomial hash of the 2,000 distances, a loop-carried dependency so the punch loop is sequential by construction. NOTE: the C mirror stores {const char*, len} and compares length-then-memcmp rather than strcmp, so all five languages pay the same length-check-then-compare cost — a strcmp mirror would measure a different operation.

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-07-29 (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 114.9 ms | 0.94× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 115.2 ms | 0.95× |
| Rust `-O` | 115.5 ms | 0.95× |
| Go | 118.2 ms | 0.97× |
| **Kāra (codegen)** | 121.8 ms | 1.00× |

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`, karac f80bb80b605f); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   shortest_distance.kara
karac build shortest_distance.kara && ./shortest_distance

# The index-list variant
karac run   shortest_distance_lists.kara

# Python
python3 shortest_distance.py

# Verify they agree
diff <(karac run shortest_distance.kara) <(python3 shortest_distance.py) && echo OK
diff <(karac run shortest_distance_lists.kara) <(python3 shortest_distance.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — with both Kāra variants agreeing with the Python mirror.

**The benchmark is a near dead heat, and that is the finding.** The measured kernel is two length-checked `memcmp`s and a branch per slot, repeated over 40M slots; there is no hashing, no allocation and no arithmetic in it. All four compiled languages land within 6% of each other, because there is very little for a compiler to differentiate on. Three checks that this is a real measurement and not a benchmark that optimised itself away:

- **It scales linearly.** Doubling the punch count doubles the time (C 114 → 221 → 448 ms across 40M / 80M / 160M slot visits; Kāra 121 → 236 → 466), so the scan is not being hoisted or elided.
- **The ratio is stable across scales.** Kāra/C held at 1.06×, 1.07×, 1.04× over those same three sizings, so the 6% is a property of the code, not of one noisy run.
- **Working-set size doesn't move it.** Re-sizing to 2,000 words × 20,000 punches and 500 × 80,000 — identical total work, an order of magnitude less memory touched — left every lane within 7% of where it started. An earlier reading of mine that this loop was memory-bound (CPython lands only ~5× behind, which looked like everyone waiting on the same memory) was wrong; the sizing sweep disproved it.

**Overflow checks are free here** — 115.2 ms checked vs 115.5 ms wrapping, comfortably inside σ. Nothing in the loop does arithmetic worth checking, which is the honest reason, not a codegen win.

**What the near-parity does and does not say.** This kata isolates plain `String` equality with no map anywhere in it, and there Kāra is 1.06× behind C and 1.03× behind Go. That is worth putting next to [#127](../../101-200/127-word-ladder/) and [#126](../../101-200/126-word-ladder-ii/), where the same `String` type inside a **hash-keyed** BFS puts Kāra 3.6× behind C and 1.75× behind Go. Those deficits therefore sit in the map/hashing path, not in `String` handling generally. It says nothing about Rust either way — Kāra is within 1.06–1.14× of equal-safety Rust on all three katas.

The C mirror carries an explicit length and compares length-then-`memcmp` rather than reaching for `strcmp`. Every word here is the same 9 bytes, so the length check never discriminates; a `strcmp` mirror would have measured a different primitive (walk-to-NUL with no length available) and reported representation overhead as though it were algorithm. The Go mirror's `strings.Clone` per slot is load-bearing for the same reason: Go's string `==` short-circuits true on pointer equality, and letting `list[i]` alias its vocabulary entry would hand that lane a free win the other four don't get.
