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

## Benchmarks
<!-- bench-staleness -->
> **Figures in this section are a 2026-07-26 snapshot; the feed was last measured 2026-07-28.** Where the two disagree, [`bench/results.json`](bench/results.json) and the [charts](../../../BENCHMARKS.md) are current; the numbers below are kept because the analysis around them explains *why* the shape is what it is, and that reasoning outlives the milliseconds.

[`bench/`](bench/) — `bash bench/bench.sh` (generated by
`scripts/new-bench.sh`). Read
[`../../../BENCHMARKS.md`](../../../BENCHMARKS.md) before quoting any of these.

> **Host:** shared **x86-64 Linux cloud container**, committed as
> `bench/results.container-x86.json`, not `results.json` — the latter is
> reserved for canonical Apple M5 Pro numbers and is the only file
> `scripts/consolidate-bench.sh` feeds into the top-level chart. This kata has
> no M5 run, so it is deliberately absent from the consolidated feed. Only the
> **within-file cross-language ratios** are comparable.

**Workload.** Build-once + punch: the word list is generated once — every
5-letter word over the 5-letter alphabet `{a..e}`, so 3,125 words — then
punched with 24 different `(begin, end)` pairs. Each punch runs both of the
kata's phases unchanged: a BFS recording **all** same-level predecessors into a
`Map[String, Vec[String]]`, then a DFS walking that map back from `end`
enumerating every shortest ladder.

The enumeration cannot blow up: every word over `{a..e}` is in the set, so a
pair at Hamming distance `d` has exactly `d!` shortest ladders — one per order
of fixing the `d` differing positions — bounded at 120. Sink = `125559906`,
identical in all six lanes (including the equal-hash Rust sibling and Python).

### Runtime — 30 runs, 5 warmup

| Lane | mean ± σ | vs kāra |
|---|---|---|
| c | 83.4 ms ± 4.9 | 4.06× faster |
| rust (overflow-checks=on) | 256.9 ms ± 36.1 | 1.32× faster |
| rust | 275.0 ms ± 36.2 | 1.23× faster |
| go | 308.1 ms ± 16.4 | 1.10× faster |
| **kāra** | **338.5 ms ± 44.9** | — |

### Same story as #127, and it reproduces the same ratio

Kāra's `Map[String, _]` hashes with **FxHash**; Rust's default `HashMap` uses
SipHash-1-3. [`word_ladder_ii_fasthash.rs`](bench/word_ladder_ii_fasthash.rs)
gives Rust the same FxHash construction. One hyperfine session, 20 runs:

| Lane | mean ± σ |
|---|---|
| rust, FxHash (equal-hash) | **202.9 ms ± 7.2** |
| rust, SipHash (default) | 266.5 ms ± 11.8 |
| kāra | 361.7 ms ± 16.5 |

**1.78× behind at equal hash**, against
[#127](../127-word-ladder/)'s 1.62× on the same graph with a lighter
algorithm. Two independent kernels landing at 1.6–1.8× is what makes
[`B-2026-07-26-2`](../../../../kara/docs/bug-ledger.md) — `Map[String, _]`
build + probe running ~2.45× behind an equal-hash Rust `HashMap` — a standing
number rather than a one-kata artifact.

This kata adds a second cost on top of #127's: `preds` is a
`Map[String, Vec[String]]` read-modify-written **per edge** (get a `Vec[String]`
copy, push, insert back), which is the densest ownership shape in the corpus
after [#332](../../301-400/332-reconstruct-itinerary/). Note it is written that
way in all five mirrors — the C version explicitly copies the list out, appends
and writes it back rather than appending in place, so it pays the same work.

### C's 4.06×, with the asymmetry named

C's map is hand-rolled open addressing using **the same FxHash constants**, so
the hash is matched. What is not matched is allocation: C builds each candidate
word into an automatic `char[8]` while Kāra/Rust/Go allocate a `String`.
[#127](../127-word-ladder/) sizes that at ~1.4× on the identical candidate loop
(78.5 ms → 112.8 ms with `malloc`/`free` per candidate); the same asymmetry
applies here, and it is disclosed rather than corrected because a
malloc-per-5-byte-word C mirror is not code anyone would write.

**Go**'s `map[string]T` uses an AES-NI-based hash the language does not let you
swap, so its 1.10× sits on a third hash, neither SipHash nor FxHash.

### Compile, size, memory

| Metric | kāra | rust | c | go |
|---|---|---|---|---|
| Compile (cold) | 687.9 ms ± 16.3 | 359.9 ms ± 13.6 | 162.4 ms ± 12.6 | — |
| Binary size | **410.2 KiB** | 3904.1 KiB | 20.2 KiB | 2177.6 KiB |
| Runtime peak RSS | 5.1 MiB | 4.4 MiB | 2.3 MiB | 7.5 MiB |
| Compile peak RSS | **101.7 MiB** | 133.3 MiB | 99.0 MiB | — |

At 687.9 ms this is the slowest `karac build` in the corpus — the two-phase
solver is the largest single translation unit here, carrying monomorphised
hash/eq pairs for `Map[String, i64]` *and* `Map[String, Vec[String]]`. Still
0.52× of `rustc -O` on the same program.

Python is present as a correctness oracle only; it is absent from the feed
(`KARA_BENCH_INCLUDE_PY` defaults to `0`).
