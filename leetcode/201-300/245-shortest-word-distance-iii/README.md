# 245. Shortest Word Distance III

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · String · Two Pointers &nbsp;·&nbsp; **Source:** [leetcode.com/problems/shortest-word-distance-iii](https://leetcode.com/problems/shortest-word-distance-iii/) &nbsp;·&nbsp; 🔒 **LeetCode Premium**

[#243](../243-shortest-word-distance/) with one constraint dropped: `word1` and `word2` **may be the same word**, and then they mean two *different* occurrences of it.

```
["practice", "makes", "perfect", "coding", "makes"]

"makes", "coding"  ->  1     indices 3 and 4
"makes", "makes"   ->  3     indices 1 and 4 — two occurrences of one word
```

**Constraints:** `1 ≤ wordsDict.length ≤ 3·10⁵`; `1 ≤ wordsDict[i].length ≤ 10`; lowercase English letters; both words occur in the list.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| unified one-pass: last index matching **either** word ★ | O(n) time, O(1) space | [`shortest_distance_iii.kara`](shortest_distance_iii.kara) ✓ | [`shortest_distance_iii.py`](shortest_distance_iii.py) ✓ |
| explicit two-case split: same-word loop / #243 loop | O(n) time, O(1) space | [`shortest_distance_split.kara`](shortest_distance_split.kara) ✓ | — |
| index lists: adjacent gaps when same, two-pointer merge when not | O(n) time, O(n) space | [`shortest_distance_lists.kara`](shortest_distance_lists.kara) ✓ | — |

`✓` marks agreement with the Python mirror under **interpreter** (`karac run --interp`), **JIT** (`karac run`), and **codegen** (`karac build`), under the default auto-parallelising build and `KARAC_AUTO_PAR=0` alike. All three Kāra variants are byte-identical on all four surfaces — and, per the randomized differential below, on 4,000 further random inputs as well.

## The mechanism

**Dropping that one constraint breaks #243's scan, and it is worth being precise about why.** #243 keeps two last-seen indices and tests them with `else if`:

```
if words[i] == word1:      last1 = i; ...
elif words[i] == word2:    last2 = i; ...
```

The `elif` is not a micro-optimisation — it encodes the assumption that a slot matches *at most one* of the requested words, which the precondition `word1 != word2` guaranteed. Remove that guarantee and every slot holding `"makes"` matches the first branch, the second branch never runs, `last2` stays `-1`, and the function returns its upper bound. The bug is silent: the code still compiles, still runs, and still returns a plausible number.

The **unified** fix stops tracking two variables and tracks one — the last index matching *either* word — then asks whether the new match forms a legal pair with it:

```
if words[i] == word1 or words[i] == word2:
    if prev != -1 and (same or words[prev] != words[i]):
        best = min(best, i - prev)
    prev = i
```

`same` is `word1 == word2`, computed once. When the words are the same, every consecutive pair of occurrences is legal. When they differ, a pair is legal exactly when the predecessor held the *other* word. It degenerates to #243's answer in the second case, costs one extra `String` comparison per matched slot — paid on hits only, not on every slot — and needs no separate code path.

The **split** variant writes the two problems as two loops and dispatches once. Its same-word loop rests on an argument worth stating: only **consecutive** occurrences can win. If `p < q < r` all hold the word then `r - p > r - q`, so any pair that skips an occurrence is beaten by one that doesn't — a single `prev` suffices, no inner loop. That variant is the easier of the two to verify; the unified one is the easier to extend.

Both use the family's `best = n` convention: the list has `n` slots, so no two distinct positions can be `n` or more apart, which makes it a genuine upper bound that doubles as the "no such pair" answer with no separate found flag. That case is reachable here in a way it isn't in #243 — a word present exactly **once**, queried against itself, has no second occurrence to pair with, which is why `["one","two","three"]` with `"two"`/`"two"` is in the test set.

## What it found

**No compiler bugs — and the negative result is backed by 4,000 random cases, not by the fifteen hand-written ones.**

The fifteen queries in each `main()` are a specification, not a test. [`differential.kara`](differential.kara) and its twin [`differential.py`](differential.py) are the actual check: a shared LCG generates 4,000 random lists of 1–9 words over a three-letter alphabet — small and repetitive on purpose, so same-word pairs, adjacent duplicates, absent words and singleton occurrences are all dense rather than rare — and every case is answered by **all three algorithms**, which must agree with each other and with Python:

```
$ python3 differential.py
algorithms disagree on 0 of 4000 cases
614058389

$ karac run --interp differential.kara   ->  614058389
$ karac run           differential.kara   ->  614058389
$ karac build         differential.kara   ->  614058389   (auto-par, the default)
$ KARAC_AUTO_PAR=0 karac build …          ->  614058389
```

Three independent algorithms × four execution surfaces × 4,000 inputs, one hash, no divergence. That is what "no bugs found" is worth here.

It is worth saying plainly that the first version of this kata shipped with two variants and fifteen assertions, which is thinner than the corpus rule ("probe **every** canonical way to write the problem") actually asks for. The index-list phrasing was missing, and the four-surface claim rested on a hand-picked input set that could not have caught an edge case nobody thought of. Both are fixed here.

**Why a family's third kata is still worth writing when it finds nothing.** #243 turned up a diagnostic gap and #244 a quantified quadratic-build gap ([`B-2026-08-03-9`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl)). #245's Kāra surface is deliberately plain — `ref Slice[String]`, `String` equality and inequality, short-circuit `or`, `min`, `Vec[i64]` growth — so the value is the control: the compound `or`-guarded condition, the `bool` threaded through a hot loop, and the returned-`Vec` shape all behave identically on interpreter, JIT, and both build modes across a wide input space. A clean result on a broad differential is evidence; a clean result on fifteen chosen inputs is barely a claim.

## Kāra features exercised

- **Short-circuit `or` in a compound loop condition** — `words[i] == word1 or words[i] == word2` and the nested `prev >= 0 and (same or words[prev] != words[i])`, the latter mixing an `i64` comparison, a `bool` binding, and a `String` inequality in one predicate.
- **`String` inequality (`!=`) against two borrowed operands** — `words[prev] != words[i]`, comparing two *indexed slice elements* rather than an element against a parameter, which is the distinct shape here.
- **A `bool` computed once and read in the hot loop** (`same`), where the alternative is re-comparing two `String`s per iteration.
- **`ref Slice[String]`** — the borrow spelled out at the callee, so `report` can be called fifteen times over six arrays (a bare `Slice[T]` parameter consumes its argument; settled language design, ledger `B-2026-07-01-10`).
- **`Array[String, N]` coercing into `ref Slice[String]`** at every call site with no copy.
- **`min` as a generic `std.cmp` free function**, and `else if` chains on mutually exclusive arms (split variant).

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup), clang, go
./bench/bench.sh
```

[`bench/`](bench/) carries a scaled cross-language variant — same algorithm and a shared deterministic LCG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`604519376`).

**The workload is deliberately identical to [#243](../243-shortest-word-distance/)'s** — same 256-word vocabulary, same LCG, same 20,000-word list, same 2,000 punches — so the two benches are directly comparable. #245's scan *is* #243's with one constraint dropped, so the gap between them is exactly what supporting the same-word case costs: one extra `String` comparison per matched slot, and a short-circuit `or` in the hot test instead of an `else if` chain. Half the punches are same-word queries (the case #243 cannot answer), alternated rather than segregated so the branch predictor can't learn the pattern and turn half the run into a different measurement.

Carried over from #243: every word is 9 bytes sharing the prefix `"delta"` so no comparison exits on length or first byte; every slot holds its own copy so no lane can shortcut on shared data pointers (Go's `strings.Clone`); and the scan has no early exit, so measured work is data-independent.

### Runtime — sequential lane

Container x86-64, 2026-08-03, hyperfine 30 runs, `KARAC_AUTO_PAR=0`, every lane 99–101% CPU. `karac` targets a **v3** deploy baseline, so `c_v3` and `rust_v3` are the ISA-matched comparators; `rust_v3` is also overflow-checked.

| Impl | Mean ± σ | vs Kāra |
|---|---|---|
| Rust `-O -C overflow-checks=on` | 217.5 ± 8.8 ms | 0.79× |
| Rust `-O` (wrapping) | 221.9 ± 5.5 ms | 0.81× |
| Rust overflow-checked @ x86-64-v3 | 233.9 ± 10.1 ms | 0.85× |
| C `clang -O3` | 256.5 ± 8.7 ms | 0.94× |
| C `clang -O3` @ x86-64-v3 | 260.2 ± 8.1 ms | 0.95× |
| **Kāra (codegen)** | **274.2 ± 9.3 ms** | 1.00× |
| Go | 331.5 ± 14.8 ms | 1.21× |

**Kāra is 1.05× behind ISA-matched C and 1.17× behind equal-safety Rust, and leads Go by 1.21×.**

**Overflow checks are free here — and that is the interesting half.** Rust wrapping is 221.9 ms, checked is 217.5 ms; the checked build is nominally *faster*, which with σ ≈ 5–9 ms simply means the two are indistinguishable. That reproduces #243 (115.5 → 115.2 ms) and stands in sharp contrast to [#244](../244-shortest-word-distance-ii/), where the same flag cost Rust **2.28×**. The explanation is entirely in the workload: this loop is `String`-comparison-bound with almost no arithmetic to check, while #244's merge does a subtraction, an `abs` and two comparisons per step. Kāra checks by default, so where checks are free it pays nothing, and where they aren't it has already paid — which is why its position relative to Rust swings between these two katas.

**The family now brackets what the map costs Kāra**, which is the point of having built three of them on one spine:

| kata | shape | Kāra vs ISA-matched C |
|---|---|---|
| #243 | linear scan, no map | 1.06× |
| **#245** | **linear scan + same-word support** | **1.05×** |
| #244 | two map lookups + merge per query | 1.31× |
| #126 / #127 | `String` keys inside a hash-keyed BFS | ~3.6× |

#245 landing on top of #243 is the control that makes the other two rows mean something: the extra comparison per hit costs nothing measurable, so the 1.31× at #244 is attributable to the map rather than to anything about how these katas are written. And the jump from 1.31× to 3.6× remains unexplained by map usage alone — two lookups per query cost a third, so whatever word-ladder is doing is a different problem.

### Caveats

This is the **container-x86 lane**, which [`BENCHMARKS.md`](../../../BENCHMARKS.md) treats as a corroborating second host with a noise floor around 1.15×. Read nothing below that from it: the **1.05× and 1.07× C rows are ties**, and so is the 1.17× equal-safety-Rust gap. Only the Go margin (1.21×) and the Rust-wrapping gap (1.24×) clear the floor, and both only barely. The comparison that carries real weight here is the *cross-kata* one against #243, since both were measured the same way on the same workload.

The **M5 Pro host lane (`results.json`) has not been measured** — this kata is new and there is no Apple-silicon run yet, so `consolidate-bench.sh` will correctly report it as missing and the kata stays out of the consolidated feed and graphs until one is done.

## Running

```bash
# Kāra — both variants, all backends, same output.
karac run   shortest_distance_iii.kara
karac run   shortest_distance_split.kara
karac run   shortest_distance_lists.kara
karac build shortest_distance_iii.kara && ./shortest_distance_iii

# Python
python3 shortest_distance_iii.py

# Verify they agree
for v in shortest_distance_iii shortest_distance_split shortest_distance_lists; do
    diff <(karac run $v.kara) <(python3 shortest_distance_iii.py) && echo "$v OK"
done

# Randomized differential: 4,000 cases, three algorithms, must match Python
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"
```

## Notes

Verified byte-identical under `karac run --interp` (tree-walk), `karac run` (JIT), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — with both Kāra variants agreeing with the Python mirror.

**Where this sits in the family.** #243 asks the question once and answers in O(1) space; [#244](../244-shortest-word-distance-ii/) asks it repeatedly and pays for an index up front; #245 asks it once again but widens what "a pair" means. The three share a `best = n` convention and a test-set spine on purpose, so a change in one is visible as a divergence in the others. #245 is closest to #243 — same per-query O(n) scan, same O(1) space — which makes the pair directly comparable: the unified loop's extra `String` comparison per hit is the whole difference between them.
