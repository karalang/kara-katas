# 843. Guess the Word

A list of unique six-letter words is given, and one of them is the
secret. A judge, `Master`, answers `guess(word)`: `-1` if `word` is not
in the list, and otherwise the number of places where `word` and the
secret hold the same letter. Each test also gives `allowedGuesses`, and
it passes if the secret is guessed within that many calls; the judge
then says "You guessed the secret word correctly." and otherwise "Either
you took too many guesses, or you did not find the secret word."

```
secret = "acckzz", words = ["acckzz","ccbazz","eiowzz","abcczz"], allowedGuesses = 10
    ->  You guessed the secret word correctly.
secret = "hamada", words = ["hamada","khaled"], allowedGuesses = 10
    ->  You guessed the secret word correctly.
```

**Constraints:** `1 <= words.length <= 100`, `words[i].length == 6`, the
words are lowercase and distinct, the secret is one of them, and `10 <=
allowedGuesses <= 30`. The tests are made so that a reasonable strategy
wins.

## Approaches

The judge is a `Master` struct holding the list, the secret, the
allowance, a guess counter and whether the secret was found; `guess` is
a `mut ref self` method on it, and every arm takes it as a `mut ref
Master`. Every arm keeps the words still possible, guesses one of them,
and keeps the words that share exactly as many places with the guess as
the secret does, which the secret always does. They differ in which
possible word they guess.

| file | which word is guessed |
|---|---|
| `guess_the_word.kara` ★ | minimax: the places every pair of words share are worked out once; the guess is the possible word whose answer leaves the fewest possible words in the worst case, its largest group of words sharing the same number of places with it, short of a full match. O(n^2) to set up and O(n^2) for each guess |
| `guess_the_word_squares.kara` | the fewest left on average: the possible word whose groups have the smallest sum of squares, which is n times the number of words its answer leaves on average when every word is equally likely to be the secret. O(n^2) for each guess, the places counted afresh each time |
| `guess_the_word_zeros.kara` | the fewest strangers: two random words most often share no place, so the commonest answer is 0, and a 0 rules out least when many words share nothing with the guess; the guess is the possible word with the fewest possible words sharing no place with it. O(n^2) for each guess |
| `guess_the_word_letters.kara` | the commonest letters: for every place, how often each letter stands there among the possible words; the guess is the possible word whose six counts sum highest, which is the number of places it shares with the possible words altogether, the word most like the rest. O(n) for each guess |
| `differential.kara` | the four arms playing the judge on random lists, five properties |

Every arm takes the first word on a tie. A fifth arm guessing the
possible word whose answer could come out the most ways was dropped: on
random lists of 100 words it needed up to 12 guesses, more than the 10
LeetCode may allow.

Every arm prints the same 11 lines: LeetCode's two examples; a list of
one word; 26 words that differ only in their last letter, where each
guess rules out only itself, with the secret the 10th word to be
guessed, the 11th, and the 11th with 30 guesses allowed; the 64 words of
six letters from `a` and `b`, with two secrets; 100 random words of all
26 letters, and of three letters; and 300 random lists of up to 100
words from 2 to 26 letters with how many were won within 10 guesses and
a checksum. Only the 11th word of the 26 is lost. `guess_the_word.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and a judge that also
keeps every guess and its answer. Each of its 400 cases draws a list and
a secret, and each arm plays it, and plays it again with the letters
renamed and the places reordered. The cases come in four kinds of 100:
up to 100 random words of all 26 letters; up to 40 random words of 2 to
6 letters; up to 60 words near one to four random words, each with two
places given a random letter; and up to 30 words near one or two random
words, each with one place changed. The first three kinds are allowed
LeetCode's fewest guesses, 10; the last is the kind no strategy wins
quickly, since a guess rules out few words, and is allowed its most, 30.
In 2,000 cases tried while writing it, no arm needed more than 10
guesses on the first three kinds.

| | property |
|---|---|
| P1 | the secret is guessed within the allowance |
| P2 | no guess is a word outside the list |
| P3 | every guess shares, with each earlier guess, as many places as the secret did: it could still be the secret |
| P4 | no word is guessed twice, and nothing is guessed after the secret |
| P5 | the list with its letters renamed and its places reordered takes as many guesses, and is won |

It prints `400 cases, 11248 words, 8000 checks over 4 arms: 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error. It also prints the most guesses
each arm took, 9, 9, 10 and 9, and all of them, 1327, 1306, 1390 and
1362: the sum of squares takes the fewest.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first possible word always guessed | P1 3, P5 3 |
| M2 | ★: the first word never possible | P1 46, P5 46 |
| M3 | ★: an answer of 5 taken for the secret | P1 55, P5 55 |
| M4 | squares: the largest sum of squares guessed | P1 16, P5 16 |
| M5 | squares: sizes summed, not squared | P1 3, P5 3 |
| M6 | squares: the last word never possible | P1 32, P5 32 |
| M7 | zeros: the first place not compared | P5, then a crash in the arm |
| M8 | zeros: words sharing one place counted as strangers | P1 10, P5 10 |
| M9 | zeros: the first possible word always guessed | P1 3, P5 3 |
| M10 | letters: the first possible word always guessed | P1 3, P5 3 |
| M11 | letters: the last place not scored | P5 185 |
| M12 | letters: words sharing fewer than the answer kept too | P1 29, P3 255, P5 29 |

P1 kills ten. P5 fails wherever P1 does, since a renamed list must also
be won, and it alone sees M11: scoring only five places makes the guess
depend on which place is last, so reordering the places changes the
number of guesses in 185 cases. M7 compares only five places, so it
loses the secret from its possible words; P5 fails first, and then the
arm, whose loop counts on the secret staying possible, reads past the
end of its emptied list and the run stops at an index out of bounds. P3
sees M12, whose kept words need not agree with the answers. The
strategies that always guess the first possible word (M1, M5, which ties
every word, M9 and M10) lose only 3 of the 300 lists allowed 10 guesses,
needing up to 13.

P2 and P4 kill nothing, and cannot here: every arm guesses only words
from its list, and an arm that kept the word it guessed would guess it
again forever rather than twice. The first M2 and M8 were such edits,
keeping words that share more places with the guess (★) and keeping the
words that do not match the answer (zeros); both hung, and were
replaced.

## Verification

Every arm prints the same output as `guess_the_word.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its lines under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `c877ae87ac`, and the runtime archives are
current with them. Under `karac __mir-run` the ★ arm takes 4.4 s, the
sum-of-squares arm 11.8 s, the fewest-strangers arm 3.9 s, the
commonest-letters arm 1.3 s, and the differential 24 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends refuse every arm, the differential and the
bench program. They refuse passing a word read out of a vector, such as
`shared(letters[i], letters[j])`, as moving it out of an index, which
v2's borrowing parameters do not do, and a `*b` or `*c` read through
`.iter()` over bytes or integers, where legacy types the loop variable
as the value itself though `karac check` accepts it on v2. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
lists once, each of LeetCode's most words, 100, distinct random words of
six letters from the first 4, 8, 16 or 26 letters in turn, each with a
random secret and its judge, set up once. Each of 6,000 rounds resets
the next list's judge to no guesses and plays it, allowing 10. Every
implementation prints `6000 rounds of 64 lists: 6000 found, checksum
18348422`, the Kāra program under `karac __mir-run` included, in 222 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.22 to 0.28 s |
| Rust (`rustc -O`) | 0.43 to 0.53 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.12 to 1.29 s |
| Go | 0.64 to 0.77 s |
| Python | 22.3 to 22.9 s |
| Kāra (`karac build --mir`) | 1.18 to 1.26 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 1.21 s, against Rust's
0.45 (1.17 under overflow checks), C's 0.24 and Go's 0.70: 1.03 times
Rust's time under overflow checks, 5.0 times C's and 1.73 times Go's.
Overflow checks cost Rust 2.6 times its time here, more than on most
katas. The C twin keeps the pair table, the possible words and the
groups in fixed arrays and allocates nothing in a round, where the
others allocate the table and the lists each time. Under valgrind's
cachegrind C runs 2.6 billion instructions and 80 million branches, Rust
7.7 billion and 1.20 billion and v2 7.5 billion and 2.03 billion, with
129 million mispredicted against Rust's 19 million and C's 2 million;
most likely v2's mispredicts are in counting the groups, the inner loop
that runs `possible.len()` squared times for every guess (not traced).
Built for `x86-64-v3`, the target `karac build` uses, C takes 0.17 s and
Rust with overflow checks 1.13 to 1.26 s, against v2's 1.22 to 1.25 s in
the same five interleaved runs. Python takes 22.6 s, about 94 times C's
time. The comparison with C and Rust waits until after M4.
