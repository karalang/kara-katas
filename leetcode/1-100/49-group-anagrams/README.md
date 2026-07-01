# 49. Group Anagrams

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array, Hash Table, String, Sorting &nbsp;·&nbsp; **Source:** [leetcode.com/problems/group-anagrams](https://leetcode.com/problems/group-anagrams/)

Given an array of strings, group the ones that are **anagrams** of each other. Two strings are
anagrams when one is a rearrangement of the other's letters.

```
["eat","tea","tan","ate","nat","bat"]  →  [["eat","tea","ate"],
                                            ["tan","nat"],
                                            ["bat"]]
```

**Constraints:** `1 ≤ strs.length ≤ 10⁴`, `0 ≤ strs[i].length ≤ 100`, each `strs[i]` is lowercase
English letters (`""` is allowed). LeetCode accepts the groups **in any order**; this kata pins a
deterministic **first-appearance** order (see below) so the output is diffable against an oracle.

## Why this kata — one grouping, two fingerprints

An anagram class is an equivalence class under "same multiset of letters". Grouping is therefore
just: compute a **canonical fingerprint** for each word, and bucket words with equal fingerprints.
The two solvers here differ in **nothing but the fingerprint**:

| Lens | Fingerprint | Cost per word |
|---|---|---|
| **Sorted-string key** ★ | `word.sorted()` — the characters sorted ascending. `"tea" → "aet"` | `O(K log K)` |
| **Count signature** | a 26-bucket letter tally, serialised `"c₀#c₁#…#c₂₅#"`. `"tea" → "1#0#…"` | `O(K)` |

Both fingerprints induce the **same partition**, so both solvers produce identical groups. The
count signature trades the per-word sort for a linear letter tally — the standard `O(N·K)` vs
`O(N·K log K)` contrast — while sharing every other line.

### The grouping: an index map, not a value iteration

The natural `Map[key → Vec[word]]` has a subtlety for a *diffable* kata: iterating `map.values()`
walks the buckets in the hash map's **unspecified** order, which can differ between `karac run` and
`karac build` (and won't match Python's insertion-ordered dict). So both solvers use an **index
map** instead:

```
let mut groups:   Vec[Vec[String]] = Vec.new();   // the groups, in first-appearance order
let mut index_of: Map[String, i64] = Map.new();   // fingerprint → its group's index

for word in words {
    match index_of.get(key(word)) {
        Some(gi) => groups[gi].push(word),         // known class — append
        None     => { index_of.insert(key(word), groups.len());   // new class — open a group
                       groups.push([word]); }
    }
}
```

The groups vector is already canonical: classes in **first-appearance** order, words in **input**
order — no post-hoc sort of the groups needed, and no dependence on hash-iteration order. The
Python oracle mirrors it exactly (`dict.setdefault` + `list(values())`), so `karac run`,
`karac build`, and `python3` agree byte-for-byte.

## Approaches

| Approach | File | Fingerprint |
|---|---|---|
| **Sorted-string key** ★ | [`sorted_key.kara`](sorted_key.kara) | `word.sorted()` |
| **Count signature** | [`count_signature.kara`](count_signature.kara) | 26-bucket tally → delimited String |
| Oracle | [`group_anagrams.py`](group_anagrams.py) | `''.join(sorted(w))` |

Everything below `anagram_key` is line-for-line identical between the two `.kara` files — the kata's
whole point is that the grouping machinery is fingerprint-agnostic.

## What this kata surfaced

**A real codegen gap — now fixed in `karac`.** The index-map grouping — `Map[String, i64]` lookups,
`groups[gi].push(word)` mutating a `Vec` element in place, growing a `Vec[Vec[String]]`, and the
count-signature `.bytes()` tally with `f"{counts[i]}#"` — all compiled the first time under both
`karac run` **and** `karac build`. The gap was in the ★ solver's one-liner fingerprint:

```
fn anagram_key(word: ref String) -> String {
    word.sorted()          // the canonical anagram key
}
```

`String.sorted()` **ran correctly under `karac run`** (the interpreter's `chars().sort_unstable()`)
but **failed `karac build`**:

```
error: codegen failed: Vec/String method 'sorted' is not yet supported in codegen
```

— a run/build divergence for a general-purpose String method. `String` already had a family of
allocating transforms lowered through runtime helpers (`trim` / `to_lowercase` / `to_uppercase` /
`replace`); `sorted` had an interpreter implementation but no codegen arm and fell through to the
loud catch-all.

Rather than route around it (a count-signature-only kata, or an ASCII byte-sort inline in the
kata), **the compiler was fixed**: `String.sorted()` now lowers through a new `karac_string_sorted`
runtime helper that mirrors the interpreter's char-sort **byte-for-byte** — it sorts by Unicode
scalar value, not raw byte, so the two backends agree on multi-byte input, not just this kata's
ASCII. It is wired identically to the sibling `karac_string_{trim,to_lowercase,to_uppercase}`
transforms, and the new method arm is guarded so a `String` receiver routes to the helper while
`Vec[T].sorted()` still falls through unchanged (the same String-vs-Vec disambiguation
`String.push` already uses). Regression tests pin it: `e2e_string_sorted_codegen` (literal +
identifier receiver, non-mutating receiver, empty string, anagram equality) and
`asan_string_sorted_no_leak_no_double_free` (the fresh buffer is freed exactly once).

See the [`karac` bug ledger](../../../../kara/docs/bug-ledger.jsonl) entry **B-2026-06-30-12**.

## Kāra features exercised

- **`String.sorted()`** — the anagram key; the method this kata drove into codegen.
- **`Map[String, i64]`** — `get` (→ `Option`), `insert`, matched over `Some`/`None`.
- **`Vec[Vec[String]]`** — grown with `push`, and `groups[gi].push(word)` mutating an indexed
  element in place.
- **`String.bytes()` iteration + byte arithmetic** (`b - b'a'`) and index-assign on a `Vec[i64]`
  tally (count signature).
- **`f"{…}"` interpolation** and `String` building via `push` / `push_str`.

## Running

```bash
# Kāra — interpreter and codegen produce the same output.
karac run   sorted_key.kara
karac build sorted_key.kara && ./sorted_key

# Python oracle
python3 group_anagrams.py

# Verify all three agree (and the count-signature solver too)
diff <(karac run sorted_key.kara)          <(python3 group_anagrams.py) && echo OK
diff <(karac build sorted_key.kara >/dev/null && ./sorted_key) \
     <(karac build count_signature.kara >/dev/null && ./count_signature) && echo OK
```

Both solvers are byte-identical to the oracle under `karac run`, `karac build` (default auto-par),
and `KARAC_AUTO_PAR=0`.
