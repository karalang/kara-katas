# 1178. Number of Valid Words for Each Puzzle

With respect to a given `puzzle` string, a `word` is valid if both the
following conditions are satisfied:

- `word` contains the first letter of `puzzle`.
- For each letter in `word`, that letter is in `puzzle`.

For example, if the puzzle is `"abcdefg"`, then valid words are `"faced"`,
`"cabbage"`, and `"baggage"`, while invalid words are `"beefed"` (does not
include `'a'`) and `"based"` (includes `'s'` which is not in the puzzle).

Return an array `answer`, where `answer[i]` is the number of words in the
given word list `words` that is valid with respect to the puzzle
`puzzles[i]`.

```
words = ["aaaa","asas","able","ability","actt","actor","access"],
puzzles = ["aboveyz","abrodyz","abslute","absoryz","actresz","gaswxyz"]
    ->  [1,1,3,2,4,0]
words = ["apple","pleas","please"],
puzzles = ["aelwxyz","aelpxyz","aelpsxy","saelpxy","xaelpsy"]
    ->  [0,1,3,2,0]
```

**Constraints:** `1 <= words.length <= 10^5`, `4 <= words[i].length <=
50`, `1 <= puzzles.length <= 10^4`, `puzzles[i].length == 7`, `words[i]`
and `puzzles[i]` consist of lowercase English letters, and each
`puzzles[i]` has no repeated characters.

The arms are `fn find_num_of_valid_words(words: Vec[String], puzzles:
Vec[String]) -> Vec[i64]`. The two Rust arms keep the method LeetCode
gives Rust users, returning `Vec[i32]`, inside `impl Solution`, and a
one-line `find_num_of_valid_words` calls it.

## Approaches

Whether a word is valid depends only on the set of its letters, so every
arm reads each word as that set. A puzzle has seven letters and its first
is required, so at most 64 sets can be valid for it: the first letter with
any choice of the other six.

| file | mechanism |
|---|---|
| `valid_words.kara` ★ | each word's set one bit per letter, counted in a `Map` through `entry(..).or_insert(0)`; each puzzle's subsets of its other six letters walked with `sub = (sub - 1) & rest`, the first letter added, and the counts summed with `get_or`. O(total letters + 64 per puzzle) |
| `valid_words_sorted.kara` | no map: the sets sorted into one `Vec`, run-length counted, and each of a puzzle's 64 candidate sets found with `binary_search`. O(w log w + 64 log w per puzzle) |
| `valid_words_trie.kara` | a trie of each word's distinct letters in alphabetical order, a `Vec` of `struct Node { next: Array[i64, 26], ends }`; a puzzle walks it by recursion through its own letters only, and counts the words that end once the walk has passed its first letter |
| `valid_words_dfs.kara` | the ★ arm's `Map`, filled with `count[m] = count.get_or(m, 0) + 1`, and each puzzle's 64 sets chosen by recursion, one letter in or out at a time, over a `Slice[u8]` |
| `valid_words_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `HashMap<i32, i32>` filled with `*freq.entry(mask).or_insert(0) += 1`, `p.as_bytes()`, `for &b in &p[1..]`, and `freq.get(&(sub \| first)).unwrap_or(&0)` summed into an unannotated `cnt` pushed into an unannotated `Vec::with_capacity`), carried to Kāra by `karac fix` |
| `valid_words_chain.kara` | another Rust solution, in iterator chains (each word's set a `chars().fold(0u32, ..)`, counted in an unannotated `HashMap` through `entry`, each puzzle's 64 sets built with `filter` and `fold` and summed from `*count.get(&set).unwrap_or(&0)`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's two examples; a case with a
word of one letter, a word with a letter the puzzle lacks, one word three
times, a first letter only one word has and a puzzle no word fits (`small:
[3, 5, 1, 1, 0]`); 300 random problems of 1 to 30 words over the first 9
letters and 1 to 10 puzzles (`300 random problems: 2524 valid in all,
checksum 880543908`); and 100000 words of 4 to 50 letters and 10000
puzzles, the constraints' most, over the first 12 letters (`100000 words,
10000 puzzles: 47287380 valid in all, checksum 988285863`).
`valid_words.py` mirrors the ★ arm and its output is byte-identical; with
`lit` it checks every puzzle against every distinct set of letters the
words have, and its output is the same. Every arm gives the same output
under `karac run` and `karac build`.

The Mend loop: the four Kāra arms take no fixes. The Rust arms take one
round each, 32 fixes and 23. Both: `use std::collections::HashMap;`
dropped; `struct Solution;` to `struct Solution {}`; `Vec<..>` to
`Vec[..]`; `HashMap<..>` and `HashMap::new()` to `Map[..]` and
`Map.new()`; `Solution::` to `Solution.`; `get(&k)` to `get(k)` and
`unwrap_or(&0)` to `unwrap_or(0)`. The solution arm's: `for w in &words` to
`for w in ref words`, `as_bytes()` to `bytes()`, `for &b in &p[1..]` to
`for b in p[1..]`, `Vec::with_capacity` to `Vec.with_capacity`, and the
annotations `res: Vec[i32]` and `cnt: i32`, the first of which is the
fix this kata added. The chain arm's: `c as u8` to `c as u32 as u8`, since
a `char` holds any Unicode scalar, which 8 bits cannot, and Kāra makes the
truncation explicit. Both arms' outputs match on the first run.

Two compiler gaps came up on the way, fixed in kara `26ae8bff93`:

- The chain arm was refused with no fix (kara B-2026-11-16-228). Its map is
  unannotated, so its counts are open integers until a use fixes them;
  they come back through `*count.get(&set).unwrap_or(&0)` and are summed
  into the method's `i32` answer. The `0` of `unwrap_or` is a literal in
  a `ref T` slot, which design.md § References types as a `T`, but Kāra
  typed it `i64` on its own, so it fixed the map's counts to `i64`, and
  the `i32` sum was refused as a narrowing. Now a literal in a `ref` slot
  whose `T` is still open joins it, and a later use fixes both, as Rust
  types the `&0` from the map. A `T` already fixed is unchanged: the
  literal is range-checked against it.
- The solution arm was refused with no fix (kara B-2026-11-16-229). It
  builds `let mut res = Vec::with_capacity(puzzles.len())`, pushes a
  `cnt` that `cnt += ..` over `i32` counts left an `i64` (design.md §8:
  an operator does not fix a literal binding, so `cnt` needed `: i32`,
  which `karac fix` already wrote), and returns `res` as `Vec[i32]`. The
  refusal named the annotation in prose only. Now an open
  `Vec.new()`/`Vec.with_capacity(..)` or `VecDeque` binding refused at a
  use for a nested numeric mismatch gets a machine fix writing the wanted
  type on the binding, and `karac fix` writes both annotations in one
  round.

The differential as first written took four fixes, each a `.clone()`
dropped from an argument the callee only borrows, and takes none now.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each puzzle, each word checked letter by letter, valid when
it holds the puzzle's first letter and every letter of it is in the
puzzle. 400 random problems over the first 7 to 10 letters: 1 to 25 words
of 1 to 9 letters drawn from 1 to 8 of them, every fourth word spelled from
a puzzle's own letters so that valid words come up often, and 1 to 8
puzzles; the first five problems have one word.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | each puzzle's last six letters shuffled, its first kept, gives the same answers |
| P3 | the words in the other order, each spelled backwards, give the same answers |
| P4 | every word twice gives every count twice |
| P5 | the letters renamed by a random permutation of the alphabet give the same answers |
| P6 | the ★ arm's answer |

All 14,400 checks pass on every arm: `400 problems: checksum 735578032,
14400 checks over 6 arms: 0 failures`, in 9.3 s under `karac __mir-run`,
and the same under `karac __mir-llvm-run` and `karac build`.

## Mutation testing

Eighteen edits to the differential, three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All eighteen are caught.

| # | mutation | failures by property |
|---|---|---|
| A1 | ★: the puzzle's second letter never allowed | P1 327, P2 318, P6 1635 |
| A2 | ★: the first letter left out of every set looked up | P1 389, P6 1945 |
| A3 | ★: each word's set its last letter alone | P1 363, P3 359, P6 1815 |
| S1 | sorted: the puzzle's last letter never picked | P1 322, P2 301, P6 322 |
| S2 | sorted: words with the same set counted once | P1 143, P4 383, P6 143 |
| S3 | sorted: the picks one letter early | P1 377, P2 301, P6 377 |
| T1 | trie: a letter after the first forgets it was passed | P1 350, P5 314, P6 350 |
| T2 | trie: the first letter not required | P1 389, P6 389 |
| T3 | trie: words with the same set counted once | P1 143, P4 383, P6 143 |
| F1 | dfs: the puzzle's second letter never chosen | P1 327, P2 318, P6 327 |
| F2 | dfs: each chosen letter taken as the next one | P1 373, P5 348, P6 373 |
| F3 | dfs: a letter twice in a word cancels out | P1 346, P6 346 |
| X1 | solution: only the whole puzzle looked up | P1 383, P6 383 |
| X2 | solution: the puzzle's second letter required instead of its first | P1 389, P2 353, P6 389 |
| X3 | solution: each set's first word counted twice | P1 383, P4 383, P6 383 |
| R1 | chain: the puzzle's last letter never picked | P1 322, P2 301, P6 322 |
| R2 | chain: the first letter left out of every set | P1 389, P6 389 |
| R3 | chain: every word given an a | P1 253, P5 343, P6 253 |

A mutation of the ★ arm fails P6 on every arm, since P6 compares each arm
with the ★ arm; P1, P2 and P3 name the ★ arm itself. S2 and T3, which
count a set once however many words have it, fail P1 in 143 problems,
those with two words of one set, and P4, which doubles every word, in
383. F3 passes P3, since a word spelled backwards has each letter as often
as before. Three more edits look like faults and pass all 14,400 checks
under both backends, since they are equivalent: the chain arm picking the
letters whose bit is clear rather than set, and picking them from the end
of the puzzle rather than the start (either way every choice of the six
comes up once), and the sorted arm testing `>=` for `==` when it extends a
run (the sets come sorted, so no set is below the last).

An edit planned for the chain arm, counting each set once with
`*count.entry(m).or_insert(0) = 1;`, was refused instead of running. Rust
types that `1` from the map, but Kāra fixed the map's open counts to
`i64` at the store through `*`, and the `Vec[i32]` answer they are summed
into was refused as a narrowing (kara B-2026-11-16-230, open). The
`v[i] = 7` of an open `Vec` already leaves the element open; a store
through `*` does not yet. R3 gives every word an `a` instead.

## Benchmarks

`bench/` times the ★ arm against the same map of letter sets in C, Rust,
Go and Python: 100000 words of 4 to 50 letters, each drawn from 1 to 7 of
the first 14 letters, and 10000 puzzles of 7 distinct letters of the first
14, the constraints' most, built once, then 20 calls, every answer folded
into a checksum. Rust counts in a `HashMap`, Go in a `map`, Python in a
`dict`; C has no map, so it counts in an open-addressing table of 32768
slots with linear probing and a one-multiply hash. Every program prints
`20 calls: checksum 334420685`.

Timings on a 4-core container (Intel Xeon, 2.3 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac `f1e5ad6e06`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.212 to 0.246 s | 0.217 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.213 to 0.264 s | 0.220 s |
| Rust (`rustc -O`) | 0.168 to 0.182 s | 0.173 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.190 to 0.245 s | 0.195 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.184 to 0.214 s | 0.192 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.073 to 0.098 s | 0.077 s |
| C (`clang -O3`) | 0.068 to 0.092 s | 0.070 s |
| Go | 0.182 to 0.236 s | 0.193 s |
| Python | 3.92 to 4.22 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; user time is within 3% of wall time for both Kāra
rows, so both ran on one core. Kāra takes about 1.15x the time of
overflow-checked Rust built for the same baseline, the equal-safety
comparison, 2.9x C's and 1.14x Go's; Python takes about 18x. Building the
words and puzzles once takes 24 ms in Kāra, 23 ms in checked Rust and 5
ms in C (each measured with no calls), so a call takes about 9.8 ms in
Kāra, 8.5 ms in checked Rust and 3.6 ms in C. A call hashes 100000 sets
into the map and looks up 640000, and Kāra's `Map` and Rust's `HashMap`
both hash with SipHash, which resists collision attacks, where C's table
hashes with one multiply; that the hash is most of C's lead was inferred
from that, not profiled.
