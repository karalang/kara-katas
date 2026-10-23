# 880. Decoded String at Index

You are given an encoded string `s`. To decode the string to a tape, the
encoded string is read one character at a time and the following steps
are taken:

- If the character read is a letter, that letter is written onto the
  tape.
- If the character read is a digit `d`, the entire current tape is
  repeatedly written `d - 1` more times in total.

Given an integer `k`, return the `k`-th letter (1-indexed) in the
decoded string.

```
s = "leet2code3", k = 10  ->  "o"
s = "ha22", k = 5  ->  "h"
s = "a2345678999999999999999", k = 1  ->  "a"
```

**Constraints:** `2 <= s.length <= 100`, `s` consists of lowercase
English letters and digits `2` through `9`, `s` starts with a letter,
`1 <= k <= 10^9`, `k` is at most the length of the decoded string, and
the decoded string has fewer than `2^63` letters.

## Approaches

| file | mechanism |
|---|---|
| `decode_at_index.kara` ★ | the tape's length, then back from the end: going forward a letter adds one to the length and a digit d multiplies it by d; going back, at each character k is taken modulo the tape's length there, since that tape is a shorter one repeated, and the length divided by the digit or one taken off for the letter. The answer is the first letter met with k a multiple of the length, the letter that ends a tape of length k. O(length of s) |
| `decode_at_index_search.kara` | binary search on the tape's lengths: the length after each character never falls, and the first character whose length reaches k holds the answer, a letter that ends a tape of exactly k, or a digit that repeats the tape before it, into which k is moved, `(k - 1) % before + 1`, before searching again. O(length of s * log(length of s)) |
| `decode_at_index_recursive.kara` | recursion from the end: `locate(i, k)` finds the k-th letter of the tape that s up to i decodes to; a digit moves k into the tape before it, and a letter is the answer when it ends a tape of exactly k, the k-th letter otherwise being in the tape before it. O(length of s) |
| `decode_at_index_restart.kara` | forward, starting over: decoding from the start, the tape's length is followed until the k-th letter is written, or until a digit would carry the tape past k; then k is moved into the tape before that digit and the walk starts over on the part of s ahead of it. The length never passes k, so nothing can overflow. O(length of s squared) |
| `decode_at_index_runs.kara` | runs of letters and digits: s splits into runs of some letters and then some digits, each writing its letters after the tape so far and repeating the whole by the product of its digits. Going back over the runs, k is moved into one copy, and either lands on one of the run's letters or goes on into the run before. O(length of s) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's three examples and seven
more (the last letter of `leet2code3`; `abc`, with no digit; the last
two letters of `a2b3c4`; `y959q969u3hb22odq595` at k = 222,280,369; the
third example at k = 10^9; and the alphabet followed by nine digit 9s
between letters, at k = 10^9); the letters, as bytes, of 3,000 cases of
up to 12 characters, 295,579 in all, with a checksum; and of 2,000 cases
of up to 100 characters with k up to 10^9 and the decoded string up to
10^18 letters, with a checksum. `decode_at_index.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the tape written out, each letter onto it and for each digit
the whole tape repeated, and its k-th letter taken. It checks 6,000
cases: 3,000 of up to 12 characters from 4 letters, the tape up to 300
letters long, against the statement; and 3,000 of LeetCode's sizes, up to
100 characters from 26 letters with k up to 10^9 and the tape up to 10^18
letters, against the other properties. The ★ arm's letters, as bytes,
sum to 640,717.

| | property |
|---|---|
| P1 | the statement's letter, on a tape of up to 300 letters |
| P2 | the answer is one of the letters of s |
| P3 | more characters after s change nothing, since its tape begins the longer one's |
| P4 | when s ends in a digit, k gives the same letter as k moved into the tape ahead of the digit; when s ends in a letter, the tape's last letter is that letter |
| P5 | within the letters s starts with, the k-th letter is the k-th of s |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on all 6,000 cases. It prints `6000 cases, letters
sum to 640717, 165000 checks over 5 arms: 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a digit returned when k is a multiple of the tape | P1 292, P2 605, P4 39, P6 605 |
| M2 | ★: the letter after the k-th | P1 2052, P3 188, P4 4406, P5 3708, P6 4348 |
| M3 | ★: the letter before the k-th | P1 2063, P3 294, P4 3922, P5 5531, P6 4343 |
| M4 | search: each digit read as one less | P1 900, P3 1539, P4 265, P6 2917 |
| M5 | search: k moved into the tape as k % size, 0 for its last letter | P1 406, P4 56, P6 980 |
| M6 | search: the last character never searched | P1 450, P3 642, P4 4437, P5 175, P6 643 |
| M7 | recursive: the first letter from the end with a tape of k or more | P1 2183, P3 5451, P5 5141, P6 5017 |
| M8 | recursive: k moved one letter on into the tape before a digit | P1 1150, P3 2011, P5 2582, P6 2941 |
| M9 | recursive: the k-th letter from the end | P1 1740, P3 3695, P4 4406, P5 5274, P6 3585 |
| M10 | restart: k moved one letter on into the tape before a digit | P1 1044, P4 483, P6 2803 |
| M11 | restart: each digit read as one more | P1 564, P4 3850, P6 2194 |
| M12 | restart: a digit taken to pass k one letter early | P1 176, P4 1019, P6 359 |
| M13 | runs: k equal to the tape ahead of a run taken as in the run | P1 167, P2 373, P3 28, P6 373 |
| M14 | runs: each digit read as one less | P1 785, P3 930, P4 3850, P6 2593 |
| M15 | runs: a run's letters read from its end | P1 1717, P3 455, P4 3100, P5 3361, P6 3631 |

P1 and P6 kill all fifteen. Only the mutants that can return a digit,
M1 and M13, fail P2. M4 and M14 are one fault in two arms but fail
different cases: the search arm reads every digit one less in the
lengths it searches, while the runs arm uses the lengths only to find
the tape ahead of each run. Five mutants tried first were replaced, all
in the arms that rely on k staying within the tape they walk: the first
length past k searched for and each digit read as one less in the restart
arm both left k beyond every tape, so the walk never ended (stopped at
120 s); a letter taken when k is 1 in the recursive arm walked past the
start of s; a run's digits added in the runs arm overflowed the length;
and the tape ahead of each run taken as empty counted letters past the
run. M4, M9, M11, M14 and M15 replace them.

## Verification

Every arm prints the same output as `decode_at_index.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `89d76e3ff2` and the runtime
archives at `e903d5b111`, with no runtime change between them. Under
`karac __mir-run` the arms take under 1 s each and the differential 6
s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends disagree with v2 and with each other. Its
interpreter prints the same output for all five arms, but a different
letter sum for the differential (639,645, with 0 failures). Its JIT and
`karac build --legacy`, with and without auto-par, print the ten fixed
cases right for every arm but different letter sums and checksums for
the random cases, a different pair in each lane, while printing the
differential's line as v2 does. Every random case reads the letter as
`decode_at_index(s, k).bytes()[0]`, a byte of a returned `String` that
nothing holds, which most likely is what legacy reads after it is freed
(inferred, not traced). Legacy also refuses the bench program at
`strings[j]` passed to a function, saying it moves a `String` out of an
index, where v2 lends it. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 1,000 encoded
strings of LeetCode's sizes, 2 to 100 characters with the decoded string
up to 10^18 letters, built once; then 1,000,000 queries, each on the
next string in turn with k drawn up to 10^9 and no further than its
decoded length, summing the letters' bytes and a checksum. Kāra and Rust
return a one-letter `String`, as LeetCode's function does, and allocate
it on every query; C returns a `char` and Go a substring of `s`, neither
allocating. Every implementation prints `1000000 queries over 1000
strings: letters sum to 109350075, checksum 803128152`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.37 to 0.39 s | 0.38 s |
| Rust (`rustc -O`) | 0.38 to 0.42 s | 0.39 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.49 to 0.53 s | 0.51 s |
| Go | 0.52 to 0.60 s | 0.54 s |
| Python | 9.6 s | |
| Kāra (`karac build --mir`) | 0.51 to 0.56 s | 0.53 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 879's does. Legacy refuses the bench program
(above), so it has no lane here.

v2 takes 1.04 times Rust's median time under overflow checks and 1.40
times C's. Rust's own overflow checks cost it 30%: the forward pass
multiplies the length by each digit and adds one for each letter, and
the walk back takes one off for each letter, so most of each query's
arithmetic is checked (inferred from the two Rust timings, not
traced). Under valgrind's
cachegrind C runs 1.51 billion instructions and 0.20 billion branches,
Rust with overflow checks 1.91 billion and 0.48 billion, and v2 2.26
billion and 0.54 billion. The comparison with C and Rust waits until
after M4.
