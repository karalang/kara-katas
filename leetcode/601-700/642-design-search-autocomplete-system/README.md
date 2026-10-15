# 642. Design Search Autocomplete System

Design the autocomplete of a search engine. The system is made from a
history: sentence `sentences[i]` was typed `times[i]` times. Then
sentences are typed into it one character a call, each ended by `#`. For
every character but `#`, `input(c)` returns the three hottest sentences
of the history that start with what has been typed of the current
sentence, hottest meaning typed most often and, among sentences typed
equally often, first in ASCII order; or as many as there are, if fewer.
For `#` it returns nothing and adds the typed sentence to the history,
once more.

```
AutocompleteSystem(["i love you","island","iroman","i love leetcode"],
                   [5,3,2,2])
input("i")  ->  ["i love you","island","i love leetcode"]
input(" ")  ->  ["i love you","i love leetcode"]
input("a")  ->  []
input("#")  ->  []
```

**Constraints:** 1 to 100 sentences in the history, each of 1 to
100 lowercase letters and spaces, typed 1 to 50 times; every `c` a
lowercase letter, a space or `#`; at most 5,000 calls.

## Approaches

Every arm is `struct AutocompleteSystem` with `fn new(sentences:
Vec[String], times: Vec[i64]) -> AutocompleteSystem` and `fn input(mut
ref self, c: char) -> Vec[String]`, sorting with one comparison: the
higher count first, then the smaller sentence.

| file | mechanism |
|---|---|
| `autocomplete.kara` ★ | a trie of 27 branches, each sentence's last node keeping its count; each call follows the typed character down, walks everything below, sorts what it gathers and keeps three; O(subtree) a call |
| `autocomplete_cached.kara` | the same trie, each node also keeping its own three hottest in order, updated along the sentence's path whenever a count grows; O(1) a call |
| `autocomplete_narrowing.kara` | no trie: a `Map` of counts, the first character of a sentence picking every sentence that starts with it and each later one keeping those that still match; O(candidates) a call |
| `autocomplete_sorted.kara` | the sentences kept in ASCII order beside a `Map` of counts: a binary search finds the typed prefix, and the sentences starting with it follow it together; O(log n + matches) a call |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 9 lines: the LeetCode example; six more
(equally hot sentences in ASCII order, a space before a letter; a typed
sentence overtaking the history; no history at all; a prefix no sentence
starts with, then typed in and found; more than three matches, the
fourth hottest left out; and sentences that start each other), each as
LeetCode prints its answers, `null` first for the constructor; a
checksum of the answers of 300 random systems of up to 7 sentences of up
to 6 characters from `ab `, with 1 to 40 characters typed; and a
checksum for the problem's largest, 100 sentences of up to
100 characters from `abc ` and 5,000 calls. `autocomplete.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
the history as a list of sentences and counts, and each call's answer
chosen by picking the first in rank among the sentences starting with
what has been typed, then the first of the rest, three times over, with
no sorting. Each of 1,000 cases has 0 to 6 different sentences of up to
5 characters from `ab `, typed 1 to 4 times each, and 1 to 30 characters
typed: sentences ended by `#`, half the time one of the history's, the
last perhaps cut short.

| | property |
|---|---|
| P1 | every answer is the definition's |
| P2 | an answer to `#` is empty, and every other holds at most three different sentences of the history, each starting with what has been typed |
| P3 | each answer is in rank order by the history's counts, and a sentence of the history starting with what has been typed but left out ranks after all three named |
| P4 | the history given in the other order gives the same answers |
| P5 | a system made with no history, the history then typed in first (each sentence and a `#`, as many times as its count), gives the same answers to the script |

It prints `1000 cases (15402 calls), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac
__mir-llvm-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: equally hot sentences in reverse ASCII order | P1 493, P3 493 |
| M2 | ★: the walk not sent back to the root after `#` | P1 821, P2 53, P3 814, P5 748 |
| M3 | cached: a sentence's old entry kept beside its new one | P1 531, P2 531, P3 531, P5 762 |
| M4 | cached: a sentence's count set to what is added, not added to | P1 319, P3 319, P5 436 |
| M5 | narrowing: candidates kept if they hold the prefix anywhere | P1 251, P2 251 |
| M6 | narrowing: a new sentence entered with a count of 0 | P1 438, P3 438, P5 438 |
| M7 | sorted: the search finding the first sentence after the prefix, not at it | P1 800, P3 800 |
| M8 | sorted: a new sentence put at the end | P1 745, P3 745, P4 657 |
| E1 | ★: a node gathered when its count is not 0 | 0 |
| E2 | cached: the root left off the path whose lists are updated | 0 |
| E3 | narrowing: the candidates kept after `#` | 0 |
| E4 | sorted: the run read while before the prefix and a `~` | 0 |

P1 kills all eight, and P3 all but M5, whose extra candidates break
P2 instead: they need not start with what has been typed. P2 also sees
M2, whose walk goes on from a stale node and so names sentences that do
not start with what has been typed, and M3, which can name a sentence
twice. P5 sees the four whose answers depend on how a count was reached:
M2 and M6, which mistreat a sentence typed in with `#`, which P5 does
for the whole history; M3, which keeps a stale entry each time a count
grows; and M4, which forgets every count but the last. P4 sees only
M8, whose list of sentences is out of order, so that which ones the
search finds depends on the order they came in. The four survivors
cannot change an answer: no count is ever negative; the root's list is
never read, since every answer comes after a character; `typed` is empty
after `#`, so the next character searches the whole map anyway; and
every sentence starting with the prefix comes before the prefix and a
`~`, which sorts after the letters and the space, while every other
sentence after the prefix differs from it at a character that sorts
higher, so comes after the prefix and a `~` too.

## Verification

Every arm prints the same output as `autocomplete.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes every arm, the
differential and the bench program. All at kara `d6111aa22a` for the
debug build, with the runtime archives rebuilt from that tree, and
`14acd67779` for the release build that runs `check` and `__mir-run`.

The frozen legacy backends refuse every arm and the differential at type
checking. Their parameters are still owned under legacy, so
`system.add(sentences[i], times[i])` in each constructor moves an
element out of a `Vec`; and legacy rejects the `mut` marker design.md
asks for where a `mut ref` binding is handed on, as in `next_random(mut
seed)` inside `random_sentence` and the ★ arm's `gather(nodes, child,
..., mut found)`. Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 10 histories once, each of
100 different sentences of up to 100 characters from `abc ` with times
of 1 to 100, and a script of 5,000 calls for each, sentences ended by
`#`, half the time one of the history's and otherwise a new one. Then
40 rounds each type one script, picked by the round, into a new system
made from its history, putting the length and the first and last
characters of every name answered into a checksum. Every implementation
prints `40 rounds of 5000 calls: 123028 names, checksum 656350514`, the
Kāra program under `karac __mir-run` included (in 81 s).

Each implementation walks the trie below the prefix and builds a new
string for every node it passes, as the Kāra does: Rust with `format!`,
C with a `malloc`'d copy freed after the walk below it, Go with string
concatenation and Python with `+`; each sorts what it gathers with the
same comparison (`qsort` in C). Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine), each including making the histories:

| | time |
|---|---|
| C (`clang -O3`) | 0.65 to 0.68 s |
| Rust (`rustc -O`) | 1.23 to 1.26 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.19 to 1.24 s |
| Go | 1.52 to 1.57 s |
| Python | 11.3 s |
| Kāra (`karac build --mir`) | 1.01 to 1.03 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program for the two reasons above. That edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside the kata that leaves out
the markers, borrows `ref` in `gather` and the constructor, and clones
each sentence it adds builds under legacy, but the binary stops at once
with `free(): double free detected`, so there is no legacy time to hold
v2 to. Legacy is frozen, so that is noted, not filed. Under `karac
__mir-llvm-run` the program prints the same line in 6.1 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

So the v2 build runs ahead of Rust and Go and takes about one and a half
times C, which builds its paths with a plain `malloc` and `memcpy`. Most
of the work is allocating, copying and freeing those paths; the
comparison with C and Rust waits until after M4.

## Compiler findings

None. The legacy refusals and the legacy copy's double free above are
not filed because legacy is frozen.
