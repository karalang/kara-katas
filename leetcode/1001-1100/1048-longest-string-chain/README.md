# 1048. Longest String Chain

You are given an array of `words` where each word consists of lowercase
English letters.

`wordA` is a **predecessor** of `wordB` if and only if we can insert
**exactly one** letter anywhere in `wordA` **without changing the order of
the other characters** to make it equal to `wordB`. For example, `"abc"` is
a predecessor of `"abac"`, while `"cba"` is not a predecessor of `"bcad"`.

A **word chain** is a sequence of words `[word1, word2, ..., wordk]` with
`k >= 1`, where `word1` is a predecessor of `word2`, `word2` is a
predecessor of `word3`, and so on. A single word is trivially a word chain
with `k == 1`.

Return the **length** of the **longest possible word chain** with words
chosen from the given list of `words`.

```
words = ["a","b","ba","bca","bda","bdca"]      ->  4  ("a","ba","bda","bdca")
words = ["xbc","pcxbcf","xb","cxbc","pcxbc"]   ->  5
words = ["abcd","dbqca"]                       ->  1
```

**Constraints:** `1 <= words.length <= 1000`; `1 <= words[i].length <= 16`;
`words[i]` consists of lowercase English letters.

## Approaches

A word's longest chain is one longer than the longest ending at any of its
predecessors, the words it becomes with one letter taken out. Taken
shortest first, every predecessor is settled before the words built on it.

| file | mechanism |
|---|---|
| `longest_chain.kara` ★ | sorted by length, a `Map[String, i64]` from word to chain; each predecessor built as `f"{w[..i]}{w[i + 1..]}"` and looked up. O(n L^2) |
| `longest_chain_pairs.kara` | no map: every earlier word one letter shorter tested with two indices that may skip one letter of the longer. O(n^2 L) |
| `longest_chain_memo.kara` | down from each word: recursion over the predecessors in a `Set`, each answer kept in a memo `Map`. O(n L^2) |
| `longest_chain_layers.kara` | length buckets walked upward, a map of only the length below kept. O(n L^2) |
| `longest_chain_iter.kara` | the ★ walk as `filter_map(..).max().map(|n| n + 1).unwrap_or(1)`, the answer `chain.values().cloned().max()` |
| `differential.kara` | the five arms against the statement read literally, six properties |

The four arms other than ★ build a predecessor as `w[0..i].to_string() +
w[i + 1..w.len()].to_string()`: Kāra's `+` appends an owned `String`, so
the right half is copied first.

Every arm prints the same 14 lines: the answers for LeetCode's three
examples and seven more (`["a", "a", "aa"]`, where a repeated word is not a
step, and `["b", "c", "d", "e"]`, where no word has a predecessor, among
them); the total and a checksum of the answers for 2000 random lists of 1
to 12 words of 1 to 4 letters from a, b, and for 300 lists of 1 to 200
words of 1 to 8 letters from a to d; the answer for 1000 words of up to 16
letters from a, b, c (8); and a ladder of 16 words, `a` to
`abcdefghijklmnop`, given longest first (16). `longest_chain.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: word `j` follows word `i` when inserting one letter, any letter
at any place, turns `i` into `j`, and the longest chain is the longest path
found by trying every word next from every word. It checks 3000 random
lists: 2000 of 1 to 10 words of 1 to 4 letters from a, b, where chains are
long and words repeat, and 1000 of 1 to 12 words of 1 to 6 letters from a,
b, c.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is at least 1, at most the number of words, and at most the number of distinct lengths |
| P3 | the list reversed, and rotated by one, gives the same answer |
| P4 | a word of the list added again changes nothing |
| P5 | every word with a `z` added on the end, put in the list beside the words, makes the answer one longer |
| P6 | each arm agrees with at least two of the other four |

P2 holds because a chain's words grow one letter at a time, so no two share
a length. P4 holds because a repeated word is not its own predecessor. P5
holds because the `z` words extend the longest chain by one, and a chain
through them gains nothing more: a `z` word's only predecessors are its own
word and other `z` words.

The differential prints `3000 lists: checksum 600632313, 90000 checks over
5 arms: 0 failures` under `karac __mir-run` (14 s), `karac
__mir-llvm-run` and `karac __mir-llvm-asan` with no error, and the same
line under `karac run` and from a `karac build` binary. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Fifteen are kept, three to
each arm. All fifteen are killed, each fails the same way under both
backends, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: never sorted | P1 1011, P3 1301, P4 141, P5 22, P6 1011 |
| M2 | ★: the first letter never taken out | P1 466, P6 466 |
| M3 | ★: no letter taken out, so a word finds an earlier copy of itself | P1 1607, P2 46, P4 2262, P5 3000, P6 1607 |
| M4 | pairs: any number of letters skipped | P1 1323, P5 890, P6 1323 |
| M5 | pairs: the word just before never tried | P1 742, P3 612, P4 352, P5 990, P6 742 |
| M6 | pairs: `or` for `and` | P1 2677, P2 2308, P4 3000, P5 2726, P6 2677 |
| M7 | memo: a remembered answer one longer | P1 1820, P2 829, P3 1034, P4 1318, P5 3000, P6 1820 |
| M8 | memo: every shorter string taken for a word | P1 3000, P2 3000, P6 3000 |
| M9 | memo: the last predecessor, not the best | P1 31, P6 31 |
| M10 | layers: the length below never kept | P1 1854, P5 3000, P6 1854 |
| M11 | layers: one-letter words skipped | P1 1226, P2 77, P6 1226 |
| M12 | layers: the last word's chain, not the best | P1 1181, P3 406, P4 97, P6 1181 |
| M13 | iter: the worst predecessor (`min`) | P1 74, P6 74 |
| M14 | iter: the last letter never taken out | P1 457, P5 2587, P6 457 |
| M15 | iter: sorted alphabetically | P1 410, P6 410 |

P1 and P6 kill all fifteen, P5 eight, P4 six, P2 five and P3 four. M2, M9,
M13 and M15 are seen only by P1 and P6: each answer is a chain the list
really holds, only not the longest, so it stays in range, does not move
with order or a repeat, and grows by one with the `z` words, whose step
takes out the last letter, which M2 still tries. P2 sees an answer longer than the list (M3,
M6, M7, M8) or 0 (M11). P3 sees the edits whose answer moves with the
list's order: an unsorted walk (M1), a neighbour never compared (M5), the
last bucket's word (M12) and a memo that grows with each visit (M7). P4
sees the edits that count a repeated word as a step (M3, M6, M7) and three
of those that depend on order, since the repeat goes at the end. P5 misses
the edits that also give the wrong answer on the list with the `z` words
one longer: M2, M8, M9, M11, M12, M13 and M15.

Fifteen other edits were set aside. Five fail exactly as a kept one does:
pairs never sorted (as M1), the ★ arm taking the last word's chain (as
M12), layers keeping the last predecessor (as M9), and iter not counting
the step or taking the shortest chain (both as M10: every answer is then
1, the shortest word's chain). Five, one in each arm, count a word
alone as 0 and fail alike, with no kept twin: P1 3000, P2 1146, P6 3000.
Four fail in ways of their own: ★ counting a step twice, pairs never
comparing lengths, memo remembering 1, and memo starting only from the
first word. One crashes: layers taking out the last letter too slices `w`
past its end, and both backends stop with the same "string slice bounds
1..0 out of range".

## Verification

Every arm prints the same output as `longest_chain.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file. The runs used a release build of kara `c08132e019`.
Under `karac __mir-run` the arms take 0.9 s (★, layers) to 8.5 s (pairs).

The arms passed `karac check` as first written. Written the way Rust
writes them, the predecessor needed the Mend loop twice, and both times
the loop stopped short before kara `0db31d7bdf`:

- `format!("{}{}", &w[..i], &w[i + 1..])` became the f-string with each
  `&` carried into its hole, `f"{&w[..i]}{&w[i + 1..]}"`, which the check
  refused twice with no fix. The rewrite now drops the `&`: a hole only
  displays the value it names.
- `w[..i].to_string() + &w[i + 1..]` became `+ ref w[i + 1..]`, refused
  with "found 'ref Str'" and no fix. That refusal now says Rust's `s + &t`
  is `s + t.to_string()`, and `karac fix` writes it.

## Benchmarks

The bench builds 100 lists of 2000 words of 1 to 16 letters from a, b, c
once in all five languages, then runs the ★ arm on every list five times,
adding up the answers and folding each into a checksum. Every
implementation prints `100 lists of 2000 words, 5 rounds: total 4465,
checksum 9278222`. With three letters most short words are present, so
chains run long and most predecessors are found in the map.

Each implementation sorts a copy of the list by length and keeps a hash map
from word to chain length, built afresh for each list: Kāra's `Map` and
Rust's `HashMap` (both SipHash-1-3), Go's `map`, a dict in Python. C's map
is a chained hash table under FNV-1a with each word copied in as its key,
and each predecessor built in a stack buffer. Rust builds a predecessor as
`w[0..i].to_string() + &w[i + 1..]`, Go as `w[:i] + w[i+1:]`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `c08132e019` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.240 to 0.315 s | 0.269 s |
| Kāra (`karac build`) | 0.435 to 0.510 s | 0.473 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.426 to 0.560 s | 0.476 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.447 to 0.560 s | 0.504 s |
| Go | 0.504 to 0.555 s | 0.522 s |
| Rust (`rustc -O`) | 0.517 to 0.630 s | 0.550 s |
| Kāra, the predecessor as `w[0..i].to_string(); pred.push_str(..)` | 0.572 to 0.705 s | 0.652 s |
| Kāra, the predecessor as `w[0..i].to_string() + w[i + 1..w.len()].to_string()` | 0.742 to 0.853 s | 0.819 s |
| Python | 1.8 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.46 s) matches its real time.

Kāra took 0.94 times Rust's median time under overflow checks, and 1.77
times C's. The two extra Kāra rows are the ★ bench with only the
predecessor's spelling changed. The f-string builds the predecessor once.
The `+` the other four arms use makes three strings, the two halves and
their sum, and takes 1.72 times as long. Rust's `to_string() + &str` makes
one string and grows it, like the `push_str` row.
