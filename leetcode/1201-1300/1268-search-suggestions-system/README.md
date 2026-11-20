# 1268. Search Suggestions System

You are given an array of strings `products` and a string `searchWord`.

Design a system that suggests at most three product names from
`products` after each character of `searchWord` is typed. Suggested
products should have a common prefix with `searchWord`. If there are more
than three products with a common prefix, return the three
lexicographically minimum products.

Return a list of lists of the suggested products after each character of
`searchWord` is typed.

```
products = ["mobile","mouse","moneypot","monitor","mousepad"], searchWord = "mouse"
  ->  [["mobile","moneypot","monitor"],["mobile","moneypot","monitor"],
       ["mouse","mousepad"],["mouse","mousepad"],["mouse","mousepad"]]
products = ["havana"], searchWord = "havana"
  ->  [["havana"],["havana"],["havana"],["havana"],["havana"],["havana"]]
products = ["bags","baggage","banner","box","cloths"], searchWord = "bags"
  ->  [["baggage","bags","banner"],["baggage","bags","banner"],["baggage","bags"],["bags"]]
```

**Constraints:** `1 <= products.length <= 1000`; `1 <= products[i].length
<= 3000`; `1 <= sum(products[i].length) <= 2 * 10^4`; all the strings of
`products` are unique; `products[i]` consists of lowercase English
letters; `1 <= searchWord.length <= 1000`; `searchWord` consists of
lowercase English letters.

The arms are `fn suggested_products(products: Vec[String], search_word:
String) -> Vec[Vec[String]]`.

## Approaches

| file | mechanism |
|---|---|
| `suggested_products.kara` ★ | by binary search: the products sorted once; for each prefix typed, a binary search finds the first product not below it, and the suggestions are up to three from there that start with it. O(n log n + L log n) comparisons |
| `suggested_products_narrow.kara` | by narrowing: the products sorted, and the window of those that match the prefix so far shrinks from both ends as each letter is typed; the suggestions are the window's first three |
| `suggested_products_trie.kara` | by a trie in a `Vec`: the products inserted in sorted order, each node keeping the first three that pass through it, so a prefix's suggestions are its node's list |
| `suggested_products_filter.kara` | by filtering: the products sorted, and for each prefix the first three that start with it, by `filter(..).take(3)`. O(n log n + L n) prefix tests |
| `suggested_products_dfs.kara` | by a trie walked in order: a trie of `SortedMap[char, Trie]` children built through a `mut ref` cursor, a word marked where it ends, and a prefix's suggestions the first three words a depth-first walk below its node meets |
| `suggested_products_solution.kara` | a Rust solution as LeetCode's Rust users write it (`mut products: Vec<String>`, `sort()`, `partition_point`, a prefix grown a letter at a time), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 5 lines: LeetCode's three examples; 1000 random
searches among 1 to 40 words of 1 to 6 letters from the first 2 to 4 of
the alphabet (`1000 random searches: 5192 suggestions, checksum
67772765`); and the constraints' top, 1000 words of up to 20 letters and
a search of 1000 letters that starts with one of them (`1000 lists, the
first sizes [3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 0], checksum 607919559`).
`suggested_products.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, filter and dfs arms checked clean as first written,
and `karac fix` repaired the rest. In every harness it removed the
`.to_string()` on the search word's literal, which a borrowed `String`
parameter takes as it is. The narrow arm took 3 fixes: `bytes()` returns
a `Vec[u8]`, so `.iter()` before `.collect()`, and Rust's `as_bytes()` to
`bytes()`. The trie arm took 1: a `(b - b'a') as i64` index whose cast is
a lossless widening Kāra does by itself. The solution arm takes one round
of 18 fixes: `mut products: Vec<String>` to `products: own Vec[String]`
and a `let mut products = products;`, as Rust's owned parameter means;
`Vec<..>` to brackets; `::` to `.`; `starts_with(&prefix)` to
`starts_with(prefix)`; and `struct Solution;` to `struct Solution {}`. No
gap was met.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: after each letter typed, every product with the typed prefix,
sorted, and the first three of them. 2000 random searches of 1 to 6
letters among 1 to 15 different words of 1 to 5 letters, each from the
first 2 to 4 letters of the alphabet, so that prefixes are shared often.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the products in reverse order give the same lists |
| P3 | a list per letter, each of at most three, in order, each word with its prefix |
| P4 | a longer prefix never has more suggestions |
| P5 | a product that matches nothing (`zz`) added anywhere changes nothing |
| P6 | the ★ arm's answer |

All 72,000 checks pass on every arm: `2000 searches: checksum 320870574,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the same
checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the binary search passes a product equal to the prefix | P1 1110, P6 5550 |
| S2 | ★: at most two suggestions | P1 1030, P6 5150 |
| N1 | narrow: the window's end never moves | P1 1032, P3 1032, P5 776, P6 1032 |
| N2 | narrow: the products not sorted | P1 1306, P2 1385, P3 1295, P5 376, P6 1306 |
| T1 | trie: the products inserted unsorted | P1 1120, P2 1385, P3 1036, P6 1120 |
| T2 | trie: each node keeps four | P1 687, P3 687, P6 687 |
| F1 | filter: `take(4)` | P1 687, P3 687, P6 687 |
| F2 | filter: `contains` for `starts_with` | P1 1560, P3 1560, P6 1560 |
| D1 | dfs: a node's own word after its children's | P1 1075, P3 1041, P4 15, P6 1075 |
| D2 | dfs: the walk stops at two | P1 1030, P6 1030 |
| O1 | solution: `take(4)` | P1 687, P3 687, P6 687 |
| O2 | solution: `partition_point` passes a product equal to the prefix | P1 1110, P6 1110 |

All twelve are caught, every one by P1, the statement read literally. P3,
the lists' form, catches every edit that suggests too many, out of order
or without the prefix, and none of the four that only drop a word (S1, S2,
D2, O2): what is left is still well formed. P2, the order of the input,
sees only the two edits that skip the sort, and P5 the narrow arm's two,
whose window can reach the `zz` at the end. D1 is the one P4 catches, on
15 searches: a node's word pushed after its children's escapes the walk's
check on the count, so a list can run to four, and does so unevenly from
one prefix to the next.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (the products sorted, a binary search for each prefix typed, and up
to three products from there that start with it) on 100 random lists of
1000 words of 1 to 10 letters from `a` to `d` built once, each searched
for its own 20-letter word, 100 rounds; every suggestion folded into a
checksum. Every program prints `100 rounds of 100 searches among 1000
words: checksum 205211732`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 1.550 to 1.700 s | 1.623 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.573 to 1.746 s | 1.609 s |
| Rust (`rustc -O`) | 1.382 to 1.477 s | 1.428 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.355 to 1.509 s | 1.418 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 1.338 to 1.500 s | 1.396 s |
| C (`clang -O3`) | 1.296 to 1.364 s | 1.313 s |
| C (`clang -O3 -march=x86-64-v3`) | 1.294 to 1.385 s | 1.339 s |
| Go | 1.570 to 1.708 s | 1.633 s |
| Python | 2.136 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on is about 12% ahead of Kāra (1.418 s
against 1.609 s). C is about 18% ahead of Kāra (1.313 s against 1.609
s); Go runs level with Kāra (1.633 s against 1.609 s). Kāra is about 25%
ahead of Python (1.609 s against 2.136 s). No profile was taken.
