# 527. Word Abbreviation

Given an array of distinct strings `words`, return the minimal
possible abbreviations for every word. The rules are:

- The initial abbreviation for each word is: the first character,
  then the number of characters in between, followed by the last
  character.
- If more than one word shares the same abbreviation, increase the
  prefix of each of them by one character (the first two characters,
  the number in between, the last character), and repeat until every
  abbreviation is unique.
- If an abbreviation does not make a word shorter, keep the word as it
  is.

```
words = ["like","god","internal","me","internet",
         "interval","intension","face","intrusion"]
  ->  ["l2e","god","internal","me","i6t",
       "interval","inte4n","f2e","intr4n"]
words = ["aa","aaa"]  ->  ["aa","aaa"]
```

**Constraints:** `1 <= words.length <= 400`; `2 <= words[i].length <=
400`; `words[i]` consists of lowercase English letters; all the words
are unique.

## Approaches

Every arm is `fn words_abbreviation(words: Vec[String]) ->
Vec[String]`. Two words can only share an abbreviation if they have
the same length and the same first and last letters, and once they do,
each needs one letter more than the longest prefix it shares with any
other.

| file | mechanism |
|---|---|
| `words_abbreviation.kara` ★ | the rule as stated: walk the words, and while another word has the same abbreviation as this one, lengthen the prefix of all of them by one letter |
| `words_abbreviation_sorted.kara` | group the words by their first abbreviation in a `Map`; sorted, a word needs one letter more than its longest common prefix with either neighbour |
| `words_abbreviation_trie.kara` | a trie per group counting the words through each node; a word's prefix ends at the first node only it passes |
| `words_abbreviation_pairs.kara` | no grouping: compare every word with every other of the same length and last letter |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 7 lines: the abbreviations for five lists
(the two examples, two words that differ in the third letter, three
long words two of which share ten letters, and three words that cannot
be shortened), then for 500 random lists of 2 to 40 distinct words of
2 to 12 letters from the first 1 to 3 letters how many words are kept
whole, the letters in all the abbreviations and a checksum over them,
and last the largest case: 400 words of 40 to 60 letters from 2
letters. `words_abbreviation.py` mirrors the ★ arm and its output is
byte-identical.

The sorted arm groups its words with
`groups.entry(key).or_insert_with(Vec.new).push(i)`, the spelling
`docs/library/collections.md` gives for exactly this. No checker or
backend accepts `Vec.new` as a function value (kara B-2026-10-06-118,
below). So every check of that arm and of the differential below was
run on copies that write `or_insert_with(|| Vec.new())`, the only
change. The files here keep `Vec.new`, and should pass as they stand
once the row is fixed.

## Differential

`differential.kara` holds copies of the four arms and the definition,
written separately from them: for each word, the shortest prefix at
which no other word abbreviates the same way, with the rule spelled
out letter by letter. Each arm is held to the properties below on
1,000 cases of distinct words from the first 1 to 3 letters: a short
list of 2 to 8 words of 2 to 8 letters for P1, and a longer one of 2
to 40 words of 2 to 12 letters for the rest.

| | property |
|---|---|
| P1 | the abbreviations are the definition's, on the short list |
| P2 | the abbreviations are all different |
| P3 | each abbreviation reads back as its word: the word itself, or a prefix of it, the count of letters left out and its last letter |
| P4 | the list back to front gives the same abbreviations, back to front |
| P5 | a word longer than all the others leaves their abbreviations as they were |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only the later words of a clash grow, not this one | P1 114, P4 514 |
| M2 | ★: a word kept whole only when its abbreviation would be longer | P1 584, P3 836 |
| M3 | sorted: only the previous neighbour compared | P1 114 |
| M4 | sorted: each group reversed, not sorted | P1 1, P2 83 |
| M5 | trie: the prefix stops at a node two words share | P1 113, P2 511 |
| M6 | trie: the prefix counted from 1, one letter too long | P1 986 |
| M7 | pairs: words with another last letter compared too | P1 165 |
| M8 | pairs: the prefix as long as the longest shared one, not one more | P1 106, P2 513 |
| E1 | ★: an empty clash tested by its length | 0 |
| E2 | sorted: each group sorted in descending order | 0 |
| E3 | trie: a missing child tested with `< 0` | 0 |
| E4 | pairs: the walk bounded by the other word's length | 0 |

M1 leaves the first word of a clash short while the later ones grow,
so the answer depends on which comes first, and P4 catches it 514
times. M5 and M8 both stop a prefix one letter early wherever two
words share it, so their abbreviations clash (P2). M4 and M7 are the
weakest: unsorted groups only matter when a word's closest match is
not beside it, and comparing words of another last letter only
lengthens a prefix that P1's definition keeps short. E2 is equivalent
because the neighbours of a word are the same whichever way its group
is sorted.

The definition has its own spelling of the rule rather than calling
the ★ arm's `abbreviate`: in a first version it did, and M2, which
edits that function, changed the definition as well, so the other
three arms failed P1 on its account.

## Verification

The ★, trie and pairs arms print the same output as
`words_abbreviation.py` under `karac __mir-run` (the v2 MIR
interpreter) and `karac __mir-llvm-run`, and run clean under `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer): output
identical, no error, no leak. The sorted arm and the differential stop
at `Vec.new` on every backend (above); on the copies that write `||
Vec.new()`, the sorted arm does the same as the other three, and the
differential prints `20000 checks, 0 failures` on both v2 backends and
runs clean under the third. `karac check` passes on the ★, trie and
pairs arms, the bench program and both copies.

The frozen legacy backends refuse every file at type checking. Legacy
types the items of a `Vec`'s `iter()` by value, so it refuses the ★
arm's `*j` ("unary '*' requires 'ref T' ... found 'i64'"), and it
calls `words[i]` passed to a `Str` parameter a move out of an index
(E_INDEX_MOVE_NON_COPY) in the other three. Legacy is frozen, so this
is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 lists of 400 distinct
words (the problem's most) of 8 to 16 letters from the first 2 letters
once, then abbreviates every list in each of 50 rounds. Every
implementation prints `20 lists of 400 words, 50 rounds: 3074650
letters, checksum 45945719`, the Kāra program under `karac __mir-run`
included (in 118 s).

Every mirror builds each abbreviation as a fresh string, as the ★ arm
does; the Rust and Go mirrors also build a fresh clash list on every
round of growing, while C reuses one buffer per call. Spot timings on a
shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.65 to 0.68 s |
| Rust (`rustc -O`) | 0.70 to 0.75 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.76 to 0.81 s |
| Go | 0.84 to 0.87 s |
| Python | 8.2 to 8.4 s |
| Kāra (`karac build --mir`) | 1.29 to 1.31 s |

The legacy `karac build` refuses this program (see Verification). So
`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`df61cbfff6`. Under `karac __mir-llvm-run` the program prints the same
line in 9.9 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

- **B-2026-10-06-118** (open, filed from kata 355): a builtin type's
  constructor cannot be used as a function value.
  `m.entry(k).or_insert_with(Vec.new)`, the library docs' own example,
  is refused with "no associated function 'new' on type 'Vec'". Met
  here in the sorted arm and in the differential's copy of it.
