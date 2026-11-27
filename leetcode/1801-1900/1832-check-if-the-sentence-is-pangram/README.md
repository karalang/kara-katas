# 1832. Check if the Sentence Is Pangram

A pangram is a sentence where every letter of the English alphabet
appears at least once. Given a string `sentence` containing only
lowercase English letters, return `true` if `sentence` is a pangram, or
`false` otherwise.

```
sentence = "thequickbrownfoxjumpsoverthelazydog"  ->  true
sentence = "leetcode"                             ->  false
```

**Constraints:** `1 <= sentence.length <= 1000`, `sentence` consists of
lowercase English letters.

The arms are `fn check_if_pangram(sentence: String) -> bool`.

## Approaches

| file | mechanism |
|---|---|
| `check_if_pangram.kara` ★ | one bit for each letter, set as the letter is seen, and every one of the 26 bits set at the end. O(n) |
| `check_if_pangram_set.kara` | the sentence's letters gathered into a `Set[char]` by `collect`, and the set holding 26 of them. O(n) |
| `check_if_pangram_all.kara` | each of the 26 letters asked for in turn, by `contains` on the sentence, as one `all` over the alphabet's `chars`. O(26 n) |
| `check_if_pangram_count.kara` | an `Array` of 26 counts, one for each letter, and no count left at zero. O(n) |
| `check_if_pangram_solution.kara` | a Rust solution as LeetCode's Rust users write it (`sentence.chars().collect::<HashSet<char>>().len() == 26`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples; four edges,
the alphabet once, the alphabet with no `z`, one letter, and `a` to `y`
39 times over with a `z` at the very end (`true false false true`); the
constraints' most, 1000 letters from the whole alphabet, from all but
`z`, and one letter 1000 times (`the most: true false false`); and 3000
random sentences of 20 to 100 letters from the first 24 to 26 of the
alphabet (`3000 random sentences: 126 pangrams, checksum 781722851`).
`check_if_pangram.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, set and count arms and the harness check clean as
first written. The all arm was first written `sentence.contains(c)` with
`c` a `char`; check refused it, as `contains` takes a `Str` pattern, and
`karac fix` wrote `sentence.contains(c.to_string())`, 1 fix. The
harness's random sentences were first written as 1 to 80 letters from
the first 22 to 26, and only 21 of the 3000 came out pangrams; they are
now 20 to 100 letters from the first 24 to 26. The Rust solution takes
14 fixes by `karac fix`'s count, and its diff is: `use
std::collections::HashSet;` taken off, as `Set` is in Kāra's prelude,
and `struct Solution {}` added in its place;
`sentence.chars().collect::<HashSet<char>>().len()` to
`Set[char].from_iter(sentence.chars()).len()`, as Kāra has no turbofish
and the collected set is the receiver of a further call; and
`Solution::` to `Solution.` at the harness's 10 calls. Every arm's
output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each letter of the alphabet in turn, the sentence walked to
find it, and a pangram when every one is found. It runs 2000 random
sentences of 1 to 100 letters from the first 24 to 26 of the alphabet,
95 of them pangrams. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | fewer than 26 letters are never a pangram |
| P3 | the sentence backwards gives the same answer |
| P4 | the alphabet put after it makes any sentence a pangram |
| P5 | with every copy of its first letter taken out it is none |
| P6 | the ★ arm's answer |

It checks clean as first written. All 60,000 checks pass on every arm:
`2000 cases: checksum 51513032, 60000 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, over the same cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash. The ★ arm's
second edit was first to take each letter's bit from `b`, which runs
below zero on an `a`; the `u8` subtraction stopped with an integer
overflow, a crash, and the edit was replaced. It now sets each even
letter's bit at the odd place above it.

| | edit | failures by property |
|---|---|---|
| M1 | ★: 25 bits asked for, z left out | P1 197, P4 2000, P5 5, P6 788 |
| M2 | ★: each even letter's bit set at the odd place above it | P1 95, P4 2000, P6 380 |
| M3 | set: 25 letters taken as enough | P1 209, P5 95, P6 209 |
| M4 | set: the first letter left out | P1 5, P3 7, P6 5 |
| M5 | all: z never asked for | P1 102, P5 5, P6 102 |
| M6 | all: any one letter taken as enough | P1 1905, P2 523, P5 1977, P6 1905 |
| M7 | count: every letter asked for twice | P1 95, P4 1905, P6 95 |
| M8 | count: z counted as a | P1 95, P4 2000, P6 95 |
| M9 | solution: 25 letters asked for | P1 304, P4 2000, P5 95, P6 304 |
| M10 | solution: only the first 26 letters looked at | P1 95, P4 1999, P6 95 |

## Benchmarks

The bench builds one string of 2000 letters once, each letter a `z` one
time in 600 and otherwise one of `a` to `y`, and makes 100000 calls of
the ★ arm on runs of 500 to 999 of its letters, each run's start and
length drawn from the checksum so far. Each call makes its run a string
of its own. It checks clean as first written. Every implementation
prints `100000 calls: 7902 pangrams, checksum 78333887`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.13 s against Rust's 0.11 s (0.15 s with overflow checks
on), C's 0.06 s and Go's 0.12 s; Python takes 4.2 s.
