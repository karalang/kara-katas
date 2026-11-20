# 1255. Maximum Score Words Formed by Letters

Given a list of `words`, list of single `letters` (might be repeating)
and `score` of every character.

Return the maximum score of **any** valid set of words formed by using
the given letters (`words[i]` cannot be used two or more times).

It is not necessary to use all characters in `letters` and each letter
can only be used once. Score of letters `'a'`, `'b'`, `'c'`, ... ,`'z'`
is given by `score[0]`, `score[1]`, ... , `score[25]` respectively.

```
words = ["dog","cat","dad","good"], letters = ["a","a","c","d","d","d","g","o","o"],
score = [1,0,9,5,0,0,3,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0]                       ->  23
words = ["xxxz","ax","bx","cx"], letters = ["z","a","b","c","x","x","x"],
score = [4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,10]                      ->  27
words = ["leetcode"], letters = ["l","e","t","c","o","d"],
score = [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0]                       ->  0
```

**Constraints:** `1 <= words.length <= 14`; `1 <= words[i].length <=
15`; `1 <= letters.length <= 100`; `letters[i].length == 1`;
`score.length == 26`; `0 <= score[i] <= 10`; `words[i]`, `letters[i]`
contain only lower case English letters.

The arms are `fn max_score_words(words: Vec[String], letters: Vec[char],
score: Vec[i64]) -> i64`, all borrowed.

## Approaches

| file | mechanism |
|---|---|
| `max_score_words.kara` ★ | backtracking: each word's letter counts once, then every word in turn left out or, when the letters on hand cover it (`(0..26).all(..)`), taken through a `mut ref` count of letters left and given back after |
| `max_score_words_subsets.kara` | every set of words by dynamic programming over bit masks: a set's letter counts are those of the set without its lowest word, found with `trailing_zeros`, plus that word's |
| `max_score_words_gray.kara` | every set of words in Gray-code order, one word taken or put back per step, the letter counts, the score and the number of letters overspent kept up to date by that one word |
| `max_score_words_prune.kara` | branch and bound in a `Search` struct with a `mut ref self` method: the words the letters can cover at all, best score first, searched take-first, and a branch dropped once its score with every word still to come cannot pass the best found |
| `max_score_words_solution.kara` | a Rust solution as LeetCode's Rust users write it (`[0; 26]`, `c as u8 - b'a'`, `Self::dfs(&words, 0, &mut cnt, &score)`, `bytes()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples; the total
and a checksum of the best scores for 300 random cases of 1 to 14 words
of 1 to 15 letters and 1 to 100 letters to spend, from the first 3 to 26
letters of the alphabet (`total 24042, checksum 827874942`); and one
case at the constraints' top, 14 words of 15 letters and 100 letters
from the first 4 letters (242). `max_score_words.py` mirrors the ★ arm,
and its output is byte-identical. Every arm gives the same output under
`karac run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the four Kāra arms checked clean as first written. The
harness was first written with `('a' as i64 + k) as char`, which Kāra
refuses since not every integer is a character (E_INT_AS_CHAR, naming
`char.try_from`), and with a `s.parse_int()` of my own invention, which
reads "no method 'parse_int' on type 'Str'"; it is written with Rust's
`(b'a' + k as u8) as char` and Kāra's `i64.parse(s)`. The solution arm
takes one round of fixes, 33 edits by `karac fix`'s count (`struct
Solution;` to `struct Solution {}`, `Vec<..>` to brackets, `[i32; 26]`
to `Array[i32, 26]`, `&mut` to `mut ref` and `mut cnt`, the `&` on the
other arguments dropped, `Self::dfs` to `Solution.dfs` at all three
calls, `c as u8` to `c as u32 as u8`, `usize` to `i64` for the index
parameter, and `let mut s = 0` given its `i32`). All five check clean.

## Gaps

None found: every arm, as written, checks after its fixes, and runs and
builds alike. The `parse_int` misnaming above reads as a plain "no
method", and the compiler is taught to name `i64.parse(s)` for it.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every set of the words tried, each set's letters taken one by
one from a copy of the letters given, a letter not there spoiling the
set, and the best total of the letters' scores. 2000 cases of 1 to 7
words of 1 to 5 letters, 1 to 15 letters to spend, from the first 2 to
6 letters of the alphabet.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the words in reverse order give the same score |
| P3 | the letters given twice give at least the same score |
| P4 | every letter's score doubled doubles the best score |
| P5 | a word of letters not given (`zz`) added gives the same score |
| P6 | the ★ arm's score |

All 60,000 checks pass on every arm: `2000 cases: checksum 232330263,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python, with
`Counter`s over every set, gives the same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a word taken only when every letter has one to spare | P1 1672, P6 6688 |
| S2 | ★: the letters of a taken word never given back | P1 981, P2 657, P3 12, P6 3924 |
| U1 | subsets: a set's counts built on the set shifted down, not the set less its lowest word | P1 1000, P2 1088, P5 398, P6 1000 |
| U2 | subsets: the set of every word never tried | P1 522, P5 522, P6 522 |
| G1 | Gray code: a letter overspent only at two short | P1 1265, P2 1028, P3 204, P5 343, P6 1265 |
| G2 | Gray code: a word put back without its score taken off | P1 1234, P2 1275, P6 1234 |
| P1 | branch and bound: the bound only the next word's score | P1 62, P2 10, P6 62 |
| P2 | branch and bound: a word never left out | P1 337, P2 30, P3 22, P6 337 |
| L1 | solution: a letter overspent by one let through | P1 1315, P6 1315 |
| L2 | solution: a taken word's score kept even when leaving it out is better | P1 270, P2 391, P3 13, P6 270 |

All ten are caught, every one by P1, the statement read literally, and
by P6, which fails on the other four arms too when the ★ arm is the one
mutated (S1, S2). P2, the words reversed, catches the seven whose answer
hangs on the words' order: those that carry state from one word to the
next (S2, G1, G2), build a set on the wrong one (U1), take the last
word's result over the best (L2), or search in an order that a bound
cuts short (P1, P2). P5, a word that can never be made added, catches
the three it moves: it changes which set is the set of every word (U2)
and which sets build on which (U1), and its two missing letters throw
off G1's count of letters overspent, raised at two short but lowered on
the way back at one short.
P3, the letters given twice, catches four, all of which fall short with
plenty of letters only some of the time. S1 and L1, which misjudge
whether a word fits by one letter in either direction, keep every
property but P1 and P6, as does every mutation for P4: none touches how
scores add, and a best set stays best with every score doubled.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (backtracking, every word in turn left out or, when the letters on
hand cover it, taken) on 100 random cases built once, each 14 words of 1
to 15 letters and 100 letters to spend from the first 6 letters of the
alphabet; each asked 3 times, every best score folded into a checksum.
Every program prints `3 rounds of 100 cases of 14 words: checksum
680636717`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.463 to 0.600 s | 0.515 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.459 to 0.585 s | 0.492 s |
| Rust (`rustc -O`) | 0.309 to 0.446 s | 0.342 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.400 to 0.491 s | 0.424 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.385 to 0.464 s | 0.402 s |
| C (`clang -O3`) | 0.108 to 0.180 s | 0.110 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.095 to 0.129 s | 0.098 s |
| Go | 0.540 to 0.645 s | 0.577 s |
| Python | 15.73 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on is about 14% ahead of Kāra (0.424 s
against 0.492 s), and the two ranges overlap. Kāra takes about 4.5x C's
time (0.492 s against 0.110 s); Kāra is about 15% ahead of Go (0.492 s
against 0.577 s). Python takes about 32x Kāra's time. No profile was
taken.
