# 691. Stickers to Spell Word

There are `n` kinds of stickers, each a lowercase English word, and an
unlimited supply of each kind. Cut single letters out of stickers and
rearrange them to spell `target`. Return the fewest stickers needed, or
-1 if the target cannot be spelled.

```
stickers = ["with","example","science"], target = "thehat"  ->  3
stickers = ["notice","possible"],        target = "basicbasic"  ->  -1
```

**Constraints:** 1 <= `n` <= 50; 1 <= `stickers[i].length` <= 10; 1 <=
`target.length` <= 15; all lowercase English letters.

## Approaches

Every arm is `fn min_stickers(stickers: Vec[String], target: String) ->
i64`.

| file | mechanism |
|---|---|
| `stickers_to_spell_word.kara` ★ | a table over the subsets of the target's positions: from each reachable mask, in increasing order, each sticker is applied greedily, each letter filling the first open position that wants it, and the count kept if it is fewer; O(2^m x n x m) |
| `stickers_to_spell_word_bfs.kara` | the same masks as a graph, searched breadth first from the empty mask with a `VecDeque`, a level at a time; only stickers holding the first open letter are tried, since that letter must come from one of them; O(2^m x n x m) |
| `stickers_to_spell_word_memo.kara` | top down over the letters still missing, as a sorted string, in a `Map[String, i64]` memo; again only the stickers holding the first missing letter are tried; O(S x n x 26) for the S multisets reached |
| `stickers_to_spell_word_search.kara` | a depth-first search over the count of each letter still needed, cut once it has used as many stickers as the best so far; a sticker that another holds letter for letter is dropped first; exponential at worst |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 8 lines: the two LeetCode examples; a target
that is itself a sticker; a target with a letter no sticker has; 15 a's
from a sticker of two and from stickers of one and five; 15 different
letters from 26 stickers of one letter each, then with a sticker holding
the whole word added; the largest case, 50 stickers of 10 letters and a
target of 15, from 12 letters; and 300 random problems of up to
30 stickers of 1 to 10 letters and a target of 1 to 12, from 2 to
26 letters, counting the impossible ones, with a checksum.
`stickers_to_spell_word.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: for k = 1, 2, and so
on up to the target's length, go through every multiset of k stickers,
as a list of sticker indices that never decreases, and answer the first
k for which the letters of some multiset cover the target's; -1 if none
does. No sticker is ever needed past the target's length, since each one
used adds a letter. 1,000 random problems are checked, with 1 to
6 stickers of 1 to 5 letters and a target of 1 to 7, all from an
alphabet of 2 to 6 letters, so that letters repeat and about a third of
the problems are impossible.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the stickers listed in reverse answer the same |
| P3 | the target reversed answers the same |
| P4 | with the target added as a sticker, the answer is 1 |

It prints `1000 problems, 4 arms, 16000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a sticker's letter used again after it fills a position | P1 362 |
| M2 | ★: a new count kept even when it is worse | P1 439, P3 128, P4 817 |
| M3 | ★: the empty mask left unreached | P1 707, P4 1000 |
| M4 | bfs: the level counted before the full mask is checked | P1 707, P4 1000 |
| M5 | bfs: stickers without the first open letter tried, those with it skipped | P1 707, P4 1000 |
| M6 | bfs: each level taken as one mask long | P1 371, P2 247, P3 258, P4 655 |
| M7 | memo: one more stored for a remainder than was found | P1 76, P2 67 |
| M8 | memo: the best kept from the last sticker tried, not the fewest | P1 227, P2 287 |
| M12 | memo: an empty remainder not seeded | P1 707, P4 1000 |
| M9 | search: the bound cutting branches one sticker early | P1 68, P2 119, P4 194 |
| M10 | search: a sticker dropped when another matches it in one letter | P1 421, P2 135, P4 591 |
| M11 | search: of two equal stickers, both dropped | P1 102, P4 139 |

P1 kills all twelve. M3, M4, M5 and M12 fail the same 707 problems, the
possible ones: M3, M5 and M12 never finish a target, and M4 answers one
too many, so every possible problem is wrong and every P4 problem, whose
answer is 1, is wrong too. M1 is seen by P1 alone: reusing a letter can
only lower an answer, the reverse orders lower it alike, and an answer
of 1 cannot go lower. P2 and P3 see a mutant only when the order of
stickers or of the target's letters decides which branch it takes. Two
first candidates were dropped as equivalent, since they changed no
answer: bfs queueing a mask it had seen, which only repeats work, and
search taking the last needed letter instead of the first, which is just
as sound. A third, memo taking away only half of each letter, did not
end, its recursion overflowing the stack.

## Verification

Every arm prints the same output as `stickers_to_spell_word.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`08a144fe72` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives rebuilt after the last
`runtime/src` change.

The frozen legacy backends refuse all four arms, the differential and
the bench program at type checking, at the first `*b` over
`s.bytes().iter()`, since legacy gives those items by value where
v2 gives references, and at `next_random(mut seed)` inside
`random_word`, whose `seed` is already a `mut ref`: legacy wants the
marker dropped, while on v2 the marked forward is the spelling (kara
B-2026-10-14-25). Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, the same algorithm in all five
languages. It solves 160 random problems, each 50 stickers of 10 letters
and a target of 15, all from the first 12 letters, the largest size
LeetCode allows, and sums the answers into a checksum. Every
implementation prints `160 problems of 50 stickers and a 15-letter
target: 418 stickers in all, checksum 830191384`, the Kāra program under
`karac __mir-run` included (in 87 s).

Each implementation allocates a table of 2^15 counts per problem and a
count of each letter per sticker; C keeps the stickers in a fixed array
of strings. Spot timings on a shared 4-core container, five interleaved
runs of each compiled program and the Kāra build three more times on its
own (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.28 to 0.38 s |
| Rust (`rustc -O`) | 0.27 to 0.33 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.38 to 0.48 s |
| Go | 0.42 to 0.46 s |
| Python | 11.6 to 11.7 s |
| Kāra (`karac build --mir`) | 0.42 to 0.51 s |
| Kāra, legacy (`karac build`, a copy) | 0.28 to 0.36 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program at `*b` and at `next_random(mut seed)` as above. That edit is by
hand, on top of the `scripts/new-bench.sh` output. A copy outside the
kata that reads `c[b as i64 - 97]` and `next_random(seed)` builds under
legacy, and its row is above. Under `karac __mir-llvm-run` the program
prints the same line in 2.3 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

So the v2 build is about 1.4 times the legacy copy here, inside the
M2 bar of 2 for any one kata, level with Rust with overflow checks and
with Go, and behind C and plain Rust. The comparison with C and Rust
waits until after M4.

## Compiler findings

None new. `karac check` first refused the programs as written, and
`karac fix` repaired every refusal: `&&`, `||` and `!` became `and`,
`or` and `not` in all four arms, a `ref` written at a call site was
dropped, and the memo arm's `solve` gave away its bare, so borrowed,
`rest: String` parameter, so it takes `rest: own String`. All were the
programs' own mistakes, not the compiler's.
