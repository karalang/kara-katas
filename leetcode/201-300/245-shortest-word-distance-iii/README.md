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

`✓` marks agreement with the Python mirror under **interpreter** (`karac run --interp`), **JIT** (`karac run`), and **codegen** (`karac build`), under the default auto-parallelising build and `KARAC_AUTO_PAR=0` alike. Both Kāra variants are byte-identical on all four surfaces.

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

**No compiler bugs.** Both variants compiled clean on the first `karac check` and agreed with the oracle on all fifteen queries across all four surfaces.

That is worth recording rather than skipping. This kata's Kāra surface is deliberately plain — `ref Slice[String]`, `String` equality, `min`, one `while` — and the interesting content is algorithmic, not linguistic. A kata that finds nothing still does its job when it is the third in a family: #243 and #244 between them turned up a diagnostic gap and a quantified quadratic-build gap ([`B-2026-08-03-9`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl)), and the value of running the same shapes a third time is the negative result — the `or`-guarded compound condition and the `same` flag threaded through a hot loop behave identically on interpreter, JIT, and both build modes.

## Kāra features exercised

- **Short-circuit `or` in a compound loop condition** — `words[i] == word1 or words[i] == word2` and the nested `prev >= 0 and (same or words[prev] != words[i])`, the latter mixing an `i64` comparison, a `bool` binding, and a `String` inequality in one predicate.
- **`String` inequality (`!=`) against two borrowed operands** — `words[prev] != words[i]`, comparing two *indexed slice elements* rather than an element against a parameter, which is the distinct shape here.
- **A `bool` computed once and read in the hot loop** (`same`), where the alternative is re-comparing two `String`s per iteration.
- **`ref Slice[String]`** — the borrow spelled out at the callee, so `report` can be called fifteen times over six arrays (a bare `Slice[T]` parameter consumes its argument; settled language design, ledger `B-2026-07-01-10`).
- **`Array[String, N]` coercing into `ref Slice[String]`** at every call site with no copy.
- **`min` as a generic `std.cmp` free function**, and `else if` chains on mutually exclusive arms (split variant).

## Running

```bash
# Kāra — both variants, all backends, same output.
karac run   shortest_distance_iii.kara
karac run   shortest_distance_split.kara
karac build shortest_distance_iii.kara && ./shortest_distance_iii

# Python
python3 shortest_distance_iii.py

# Verify they agree
for v in shortest_distance_iii shortest_distance_split; do
    diff <(karac run $v.kara) <(python3 shortest_distance_iii.py) && echo "$v OK"
done
```

## Notes

Verified byte-identical under `karac run --interp` (tree-walk), `karac run` (JIT), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — with both Kāra variants agreeing with the Python mirror.

**Where this sits in the family.** #243 asks the question once and answers in O(1) space; [#244](../244-shortest-word-distance-ii/) asks it repeatedly and pays for an index up front; #245 asks it once again but widens what "a pair" means. The three share a `best = n` convention and a test-set spine on purpose, so a change in one is visible as a divergence in the others. #245 is closest to #243 — same per-query O(n) scan, same O(1) space — which makes the pair directly comparable: the unified loop's extra `String` comparison per hit is the whole difference between them.
