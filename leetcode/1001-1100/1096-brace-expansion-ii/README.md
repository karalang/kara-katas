# 1096. Brace Expansion II

Under the grammar given below, strings can represent a set of lowercase
words. Let `R(expr)` denote the set of words the expression represents.

- Single letters represent a singleton set containing that word:
  `R("a") = {"a"}`, `R("w") = {"w"}`.
- When we take a comma-delimited list of two or more expressions, we
  take the union of possibilities: `R("{a,b,c}") = {"a","b","c"}`,
  `R("{{a,b},{b,c}}") = {"a","b","c"}` (each distinct word written only
  once in the final answer).
- When we concatenate two expressions, we take the set of possible
  concatenations between two words where the first word comes from the
  first expression and the second word comes from the second
  expression: `R("{a,b}{c,d}") = {"ac","ad","bc","bd"}`,
  `R("a{b,c}{d,e}f{g,h}") = {"abdfg", "abdfh", "abefg", "abefh",
  "acdfg", "acdfh", "acefg", "acefh"}`.

Formally, the three rules: for every lowercase letter `x`, `R(x) = {x}`;
for expressions `e1, e2, ... , ek` with `k >= 2`, `R({e1, e2, ...}) =
R(e1) ∪ R(e2) ∪ ...`; for expressions `e1` and `e2`, `R(e1 + e2) = {a +
b for (a, b) in R(e1) × R(e2)}`, where `+` denotes concatenation and `×`
the cartesian product.

Given an expression representing a set of words under the given grammar,
return the sorted list of words that the expression represents.

```
expression = "{a,b}{c,{d,e}}"          ->  ["ac","ad","ae","bc","bd","be"]
expression = "{{a,z},a{b,c},{ab,z}}"   ->  ["a","ab","ac","z"]
```

**Constraints:** `1 <= expression.length <= 60`; `expression[i]`
consists of `'{'`, `'}'`, `','` or lowercase English letters; the given
expression represents a set of words based on the grammar given in the
description.

The arms are `fn brace_expansion_ii(expression: String) ->
Vec[String]`. A word can come from an expression more than one way:
`{a,ab}{c,bc}` gives `abc` both as `a` + `bc` and as `ab` + `c`, and it
is written once.

## Approaches

| file | mechanism |
|---|---|
| `brace_expansion_ii.kara` ★ | a recursive descent: a union is concatenations separated by commas, a concatenation a run of letters and braced unions, each returning a `SortedSet[String]`, so duplicates go and the answer comes out sorted |
| `brace_expansion_ii_stack.kara` | an explicit stack in place of the recursion: the union so far and the concatenation so far are two `Vec[String]`s, pushed at `{` as a tuple and popped at `}`; sorted and deduplicated at each `}` and at the end |
| `brace_expansion_ii_rewrite.kara` | rewriting, breadth first: the first `}` and the `{` before it are an innermost group, replaced by each of its options in turn, each new expression queued once (a `Set[String]` of those seen) in a `VecDeque`; an expression with no braces left is a word. `find`, `rfind`, slices and `split` |
| `brace_expansion_ii_tree.kara` | the expression read into an `enum` tree of letters, concatenations and unions, then its words by iterator chains: a union is a `flat_map` over its options, a concatenation a `fold` |
| `brace_expansion_ii_postfix.kara` | as arithmetic: concatenation is an operator `*`, written in wherever a letter or `}` meets a letter or `{`, binding tighter than the union `,`; shunting-yard to postfix, then a stack of word lists evaluates it |
| `brace_expansion_ii_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `expression.as_bytes()`, `&mut usize`, `BTreeSet<String>`, `format!`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the grammar's rules read literally, six properties |

Every arm prints the same 15 lines: the words of LeetCode's two examples
and ten more (a single letter, a run of letters, a flat union, a union
of one letter three times, a union out of order, nested braces, the word
that comes two ways, four braces around one letter, letters between
groups), then over 2000 random expressions of up to 60 characters the
number of words and a checksum (`7162 words, checksum 982388189`), and
two of LeetCode's longest: eight unions of three letters, 56 characters
and 3^8 = 6561 words, and fourteen letters nested thirteen deep and
followed by a union of two (`28 words`). `brace_expansion_ii.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the grammar's rules
read literally: an expression is cut into the parts of its
concatenation by counting braces, a braced part into its options at the
commas outside any inner group, and the words are built rule by rule
from those strings. A second reading of the grammar matches a word
against an expression, the positions where a match can end carried
through the same parts. It checks 2000 problems in four kinds of 500,
each at most 24 characters, so that two of them side by side or one
inside braces stay within LeetCode's 60: expressions of the grammar over
2 to 5 letters, nested up to 3 deep; single letters and flat unions of
single letters; nested 3 deep over two letters one at a time, so that
most words come more than one way; and runs of up to three of two
letters, where different splits meet in the same word. Each problem is
paired with another of its kind. Every random choice is drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the rules' words, sorted |
| P2 | the answer is sorted with no word twice, and every word matches the expression |
| P3 | the expression in braces, and in a union with itself, gives the same answer |
| P4 | a union with the paired expression, either way round, is the two answers together, sorted and deduplicated |
| P5 | the expression followed by the paired one gives every word of one followed by every word of the other, sorted and deduplicated |
| P6 | every letter renamed, `a` to `z` and `z` to `a`, gives the answer renamed and sorted again |

All 72,000 checks pass on every arm: `2000 problems: checksum
465327374, 72000 checks over 6 arms: 0 failures`. A Python reading of
the same problems, by the mirror, gives the same checksum.

P1 builds the words; P2 only matches them. P3 to P6 compare the arm
only with itself.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All thirty are caught. Fifteen are kept, no two failing the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a union of two options at most | P1 484, P2 462, P3 289, P4 562, P5 563 |
| M2 | ★: a closing brace not passed | P1 493, P2 470, P4 1005, P5 753 |
| M3 | ★: each part put in front | P1 1158, P2 1158, P5 1841 |
| M4 | ★: a concatenation starts with no words | P1 2000 |
| M5 | ★: the last option replaces the union | P1 716, P4 1891 |
| M6 | stack: the answer not deduplicated at the end | P5 1 |
| M7 | stack: a letter put in front | P1 1001, P2 1001, P5 1525 |
| M8 | stack: the inner union kept alongside | P1 590, P2 590, P5 1056 |
| M9 | rewrite: the first open brace, not the one that matches | stops: `unwrap()` on `None` |
| M10 | rewrite: two options at most | P1 400 |
| M11 | rewrite: the last closing brace taken | P1 122, P2 122, P3 753, P4 1056, P6 122 |
| M12 | tree: a closing brace read as a letter | P1 753, P2 753, P3 2000, P4 2000, P5 753, P6 753 |
| M13 | postfix: concatenation no tighter than union | P1 296, P2 279, P3 1354, P4 1747 |
| M14 | postfix: never deduplicated | P1 354, P2 354, P3 2000, P4 652, P5 522, P6 354 |
| M15 | solution: a union read past its closing brace | P1 753, P2 718, P3 2000, P4 2000, P5 943 |

Of the fourteen that run to the end, P1 catches thirteen, P2 ten, P5
nine, P4 eight, P3 six and P6 three. P1 misses only M6: the stack arm
deduplicates at every `}`, so only a word that comes two ways at the
top level, outside every brace, is left twice. One problem in 2000 has
such a word once another expression follows it, and only P5 sees it.
P3 to P6 between them catch all but two: an arm whose every
concatenation starts empty (M4) answers nothing for every expression,
and nothing agrees with nothing; and two options at most (M10) loses
only in a union of three, which braces, renaming and pairing all keep.
P6 is the weakest because most edits do not depend on which letters
are used. The three it sees give words that do not match the expression
at all (M11, M12), or the same word twice (M14), and the renamed answer
it expects is sorted and deduplicated afresh.

Of the fifteen not kept, nine fail exactly as a kept edit: M3 is also
the tree, postfix and solution arms putting each part in front; M4 is
also the solution arm starting a concatenation empty and the tree arm
dropping a union's first option, so a lone concatenation has none; M5
is also the stack arm dropping every option but the last, and the tree
and solution arms' last option replacing the union. The other six fail
in ways of their own but were not needed: the stack arm putting a group
before what came before it, the rewrite arm putting the option in front
and skipping an expression when its option was seen, the tree and
solution arms doubling every letter, the postfix arm writing no
concatenation before a brace, and a comma that pops nothing.

## Verification

Every arm prints the same output as `brace_expansion_ii.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file but the note it prints for mutual recursion
(design.md §12) on the ★, tree and solution arms and the differential,
whose parsers are a union and a concatenation calling each other
(`karac run` prints it too, on stderr); `karac fix` has nothing to
apply.

The kata found no compiler gap. `karac fix` carried every Rust spelling
tried across:

- The ★ arm's `for w in concat_of(s, mut at) { words.insert(w); }` moves
  each word out of a set the loop owns; a bare `for` borrows, and the
  fix adds `.into_iter()`.
- The rewrite arm was written with `Deque`, `find('}')` on a `char`,
  `(&e[..open], &e[close + 1..])` and `format!`. Three rounds took it
  to `VecDeque`, `find("}")`, plain slices, an f-string, and `own
  String` on the parameter the queue takes.
- The Rust solution reaches a clean check in three rounds: the syntax
  (`Vec<..>`, `&[u8]` to `Slice[u8]`, `&mut usize` to `mut ref usize`,
  `Self::` to `Solution.`, `&&` to `and`, `for a in &res` to `for a in
  ref res`, `format!` to an f-string), then `struct Solution {}` and
  `BTreeSet` to `SortedSet`, then `as_bytes()` to `bytes()` and `usize`
  to `i64` with `0usize` to `0`.
- In the bench, `words[0].bytes().chain(..)` took two rounds: `bytes()`
  is a `Slice[u8]` in Kāra, not an iterator, and each side gets an
  `.iter()`.

## Benchmarks

The bench builds 64 expressions once, each a concatenation of five
unions of 2 or 3 options of a letter or two, a quarter of them a union
of two letters followed by a letter, all of at most 60 characters,
LeetCode's longest. Each of 200 rounds changes one letter in every
expression and expands it with the stack arm, whose two `Vec[String]`s
every implementation can hold the same way: 12,800 expansions and 2.36
million words. Every implementation prints `200 rounds over 64
expressions: 2358947 words, checksum 958505912`. Each word is its own
heap string in every language: C `malloc`s each and sorts with `qsort`
and `strcmp`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `33ef2a7ad2`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.326 to 0.377 s | 0.335 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.330 to 0.385 s | 0.342 s |
| Rust (`rustc -O`) | 0.328 to 0.399 s | 0.345 s |
| C (`clang -O3`) | 0.336 to 0.414 s | 0.346 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.338 to 0.396 s | 0.353 s |
| Go | 0.371 to 0.431 s | 0.390 s |
| Kāra (`karac build`) | 0.405 to 0.465 s | 0.420 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.404 to 0.479 s | 0.426 s |
| Python | 0.670 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. C and Rust tie, Go takes about 1.13x their time and Kāra about
1.23x; the gap was not traced. Python takes about 1.6x Kāra's time; most
of the work is building and sorting short strings.
