# 2800. Shortest String That Contains Three Strings

Given three strings `a`, `b`, and `c`, your task is to find a string
that has the **minimum** length and contains all three strings as
**substrings**.

If there are multiple such strings, return the **lexicographically
smallest** one.

Return *a string denoting the answer to the problem.*

```
a = "abc", b = "bca", c = "aaa"   ->  "aaabca"
a = "ab", b = "ba", c = "aba"     ->  "aba"
```

**Constraints:** `1 <= a.length, b.length, c.length <= 100`; `a`, `b`,
`c` consist only of lowercase English letters.

## Approaches

Some shortest answer starts with one of the words and takes them in
some order, each either inside what came before or joined to it at its
longest overlap; so six orders, each merged left to right, cover every
candidate, and the answer is the shortest of them, the least of equal
lengths.

| file | mechanism |
|---|---|
| `shortest.kara` ★ | the six orders as an array of index triples, `merge` keeping a word whole when `contains` finds it and otherwise joining it at the longest `k` whose first `k` letters the result `ends_with`; the best kept by length, then letters |
| `shortest_prefix.kara` | the overlap read off the prefix function of the word, a separator and the result so far, at its last place, in a `Vec[u8]`; the rest as ★ |
| `shortest_sorted.kara` | the orders made by a recursive swap, every merged result collected and sorted by `(length, letters)` with `sort_by_key`, the first the answer |
| `shortest_bytes.kara` | by hand on bytes: the orders as three nested loops over distinct indices, `contains` and the overlap both loops comparing bytes, and `+` joining |
| `shortest_solution.kara` | a Rust solution as LeetCode's Rust users write it, an associated `merge` on `&str` comparing `s[s.len() - i..]` with `t[..i]`, called as `Self::merge`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; three
100-letter words, LeetCode's longest, all the same; three that share no
letter, its length and both ends; three that chain, its length and a
digest of its letters; 3000 random triples of 1 to 4 letters from a to
c; and 50 of up to 100 letters from a and b or from the whole alphabet,
the last two with the sum of the lengths and a checksum of the digests.
`shortest.py` mirrors the ★ arm and its output is byte-identical.

```
aaabca
aba
100
300 xxx zzz
102 35436556
3000 short triples: lengths sum to 16452, checksum 516761163
50 long triples: lengths sum to 7823, checksum 785677648
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every string of the inputs' letters, shortest first and in
letter order within a length, until one holds all three words; no
merging and no overlap. It draws 2000 random triples of 1 to 3 letters
from a and b, then 50 of up to 100 letters, LeetCode's longest, from a
and b or from a to y, all before any arm answers; the literal reading is
asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 3 letters each, the answer is the literal reading's |
| P2 | every word inside, and no longer than the three end to end |
| P3 | the words given in the orders b, c, a and c, b, a: the same answer |
| P4 | every letter one later in the alphabet: the answer so shifted |
| P5 | the answer given back with a and b: the answer itself |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 474068313, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. Three first edits (a word found only past its
first place, the overlap tried from one short of the shorter word, and
the solution's overlap never the whole shorter word) survived: each is
undone by the containment test or by another order of the three words,
so the shortest string is unchanged, and they were replaced by the three
shown.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a word already inside joined anyway | P1 50, P5 126, P6 56 |
| M2 | ★: the shortest overlap taken, not the longest | P1 36, P6 49 |
| M3 | prefix: the separator left out | killed under both: runtime error: string slice bounds 4..3 out of range (len 3) |
| M4 | prefix: a mismatch falls back to nothing, not the next border | P1 17, P6 24 |
| M5 | sorted: the candidates sorted by letters alone | P1 632, P6 654 |
| M6 | sorted: a word never left in its own place | killed under both: runtime error: index out of bounds |
| M7 | bytes: the last letter of a word never compared | P1 50, P5 126, P6 56 |
| M8 | bytes: the last letter of an overlap never compared | P1 574, P6 606 |
| M9 | solution: equal lengths broken toward the greater | P1 689, P6 720 |
| M10 | solution: the overlap read from the front of the first word | P1 632, P2 321, P5 150, P6 664 |

## Benchmarks

The bench draws 2000 triples of up to 100 letters, LeetCode's longest,
from a and b, so that the words overlap and contain each other often,
all of them first, then answers each 200 times by the ★ arm in all five
languages. Every implementation prints `2000 triples of up to 100, 200
rounds: lengths sum to 58053600, checksum 263940367`.

BENCHTAB

## Verification

All five arms print the same output as `shortest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

Five `karac fix` edits in my own code, each a Rust habit: the harness's
`s.bytes().fold(...)` took the `.iter()` an adaptor needs (applied to
the harness of every arm); the sorted arm's `vec![...]` became a list
literal; and in the bytes arm, the `Slice[u8]` that `.bytes()` gives
passed to a `Vec[u8]` parameter took `.to_vec()` at both arguments, and `s + t[k..]`
took `.to_string()` on the `Str` view, since `+` appends an owned
`String`. The differential's literal reading first built its strings
with `while place > 0 { ...; place /= q }`, which never ends for inputs
of one letter (q = 1) and ran a build out of memory; it counts the
letters now.

LeetCode's Rust template took 16 `karac fix` edits, the wrapper
included: `struct Solution {}` added; `&str` became `Str` twice; the two
`format!` became f-strings; `[&a, &b, &c]` became `[ref a, ref b, ref
c]`; `String::new` became `String.new`; both `Self::merge` became
`Solution.merge` and the `&` on the inner call's result was dropped; `||`
became `or` twice and `&&` became `and`; and the wrapper's
`Solution::` became `Solution.`.
