# 1009. Complement of Base 10 Integer

The complement of an integer is the integer you get when you flip all
the `0`'s to `1`'s and all the `1`'s to `0`'s in its binary
representation. For example, the integer `5` is `"101"` in binary and
its complement is `"010"` which is the integer `2`.

Given an integer `n`, return *its complement*.

```
n = 5   ->  2   (101 -> 010)
n = 7   ->  0   (111 -> 000)
n = 10  ->  5   (1010 -> 0101)
```

**Constraints:** `0 <= n < 10^9`.

The binary representation has no leading zeros, so only the bits up to
`n`'s highest 1 are flipped, and `0` is written `"0"`, whose complement
is `1`.

## Approaches

| file | mechanism |
|---|---|
| `bitwise_complement.kara` ★ | an all-ones mask: grow `1, 11, 111, ...` until it covers `n`, then XOR. O(log n) |
| `bitwise_complement_bits.kara` | bit by bit: walk `n`'s bits from the lowest by halving, and set the answer's bit wherever `n` has a 0; the walk stops at the highest 1. O(log n) |
| `bitwise_complement_text.kara` | through the text: write `n` in binary as characters, flip each, and read the text back. O(log n) |
| `bitwise_complement_smear.kara` | smearing the top bit: OR `n` with itself shifted right by 1, 2, 4, 8 and 16, which spreads the highest 1 into every bit below it and gives the mask in five steps, enough for the 30 bits below 10^9. O(1) |
| `bitwise_complement_recursive.kara` | recursion on the last bit: the complement of `n` is the complement of `n / 2` followed by the flipped last bit, and a single bit flips to the other. O(log n) calls |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's three examples and six
edges (0, 1, 2, 2^29 and the all-ones number below it, and 999,999,999,
the largest `n`); the complements of every `n` from 0 to 32 on one line;
and totals over every `n` up to 100,000 and over 20,000 random `n` below
10^9, each of a random length from 1 to 30 bits.
`bitwise_complement.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: it finds `n`'s binary digits from the top, taking the
largest power of two at most `n` as the leading 1 and subtracting each
lower power that fits, flips every digit and adds the powers back up.
It checks 9,091 values of `n`: every `n` up to 6,000, every power of two
below 2^30 with the numbers on either side of it, and 3,000 random `n`
below 10^9 of random length.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | for `n >= 1`, `n + c + 1` is a power of two `p` with `p / 2 <= n < p` |
| P3 | no bit is set in both `n` and its complement `c` |
| P4 | for `n >= 1`, `2n` has the complement `2c + 1` and `2n + 1` the complement `2c` |
| P5 | where `c` is not 0, the complement of `c` is `n` with its leading run of ones taken off |
| P6 | each arm agrees with at least two of the other four |

P2 holds because `n` and its complement together fill every bit up to
`n`'s highest 1. P4 is appending a bit to `n`, which appends the flipped
bit to the complement. P5 holds because the complement of `n` starts
with `n`'s first 0, so complementing again loses the ones before it.

It prints `9091 values of n: checksum 45824119, 270400 checks over 5
arms: 0 failures` under `karac __mir-run` (4.2 s) and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Twenty-five edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the mask grown past an all-ones `n` | P1 254, P2 254, P4 254, P5 656, P6 254 |
| M2 | ★: the mask a power of two, not all ones | P1 8884, P2 8884, P3 8742, P4 8985, P5 8742, P6 8884 |
| M3 | ★: the mask one bit short | P1 8884, P2 8884, P3 8884, P4 101, P5 8884, P6 8884 |
| M4 | bits: 0 gives 0 | P1 106, P6 106 |
| M5 | bits: the zeros counted, not placed | P1 8627, P2 8627, P3 6124, P4 8731, P5 8500, P6 8627 |
| M6 | bits: every place one too high | P1 8731, P2 8731, P3 8731, P4 8985, P5 8731, P6 8731 |
| M7 | text: the digits left lowest first | P1 8473, P2 8473, P3 8473, P4 8985, P5 8731, P6 8473 |
| M8 | text: the digits written flipped | P1 9091, P2 8985, P3 8985, P4 8985, P5 8985, P6 9091 |
| M9 | text: every digit set | P1 8985, P2 8985, P3 8985, P4 8985, P5 9091, P6 8985 |
| M10 | smear: the shift by 16 left out | P1 27, P2 27, P4 15, P5 27, P6 27 |
| M11 | smear: the shift by 1 left out | P1 5425, P2 5425, P4 363, P5 6635, P6 5425 |
| M12 | smear: the shift by 8 XORed in | P1 7870, P2 7870, P3 7210, P4 7315, P5 7868, P6 7870 |
| M13 | recursive: a single bit kept, not flipped | P1 9091, P2 8985, P3 8985, P5 8985, P6 9091 |
| M14 | recursive: the last bit kept, not flipped | P1 8884, P2 8884, P3 8742, P4 8985, P5 6989, P6 8884 |
| M15 | recursive: 1 split into 0 and its bit | P1 8985, P2 8985, P5 9091, P6 8985 |

P1 and P6 kill all fifteen, P2 and P5 fourteen each, P4 twelve and P3
ten. The checks draw no random number that depends on an answer, so
every mutant sees the same `n` and their counts can be compared. M4
fails only the statement and agreement: the other properties leave out
`n = 0`, and its 106 failures are the zeros among the inputs, most of
them random draws one or two bits long.

M10 found a gap in the first version of the differential, which had
only the counting and random parts. The shift by 16 matters only when
`n`'s highest 1 has no other 1 within the 16 places below it, and a
random `n` almost always has one, so the edit failed no check. The
powers of two and their neighbours were added for it, and the edit now
fails on 27 of them, from 2^16 up.

Ten other edits were tried and set aside. Three change no answer: the ★
arm subtracting `n` from the mask instead of XORing, the same thing
when every bit of `n` is in the mask; the bits arm stopping before the
highest bit, which is a 1 and flips to nothing; and the text arm not
writing the leading 1, which flips to a leading 0. Four failed exactly
the same checks as a kept one: the ★ arm's mask starting at 0 and the
smear arm's 0 giving 0, as M4; and the bits arm placing the ones
instead of the zeros and the smear arm returning its mask, as M9. Two
stopped with an integer overflow under both backends, as the edit makes
it: the text arm reading its digits back in base 3, and the recursive
arm shifting by two places per bit, each when P5 feeds the arm its own
answer, already too large, to complement again. One was killed but
beyond three an arm: the recursive arm's single bit giving 1.

## Verification

Every arm prints the same output as `bitwise_complement.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer)
with no error; the differential prints its line under all three.
`karac check` passes all five arms, the differential and the bench
program. `karac run` and a `karac build` binary print the same output
for every arm and the differential. The release build is at kara
`8b6e8a9088`, with the runtime archives rebuilt there. Under `karac
__mir-run` the arms take 0.3 s (smear) to 6.2 s (text).

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages: 1,000,000 values of
`n` below 10^9, each of a random length, drawn once, and 50 rounds
that each take the complement of every `n` plus the round number and
fold the round's sum into a checksum. The mask loop runs once per bit
of `n` and stops at a length that changes at random from one `n` to the
next, so its exit is mispredicted about once a call in every language.
Every implementation prints `50 rounds over 1000000 values of n:
checksum 351038280`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `8b6e8a9088`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.906 to 0.958 s | 0.924 s |
| Rust (`rustc -O`) | 0.890 to 0.955 s | 0.909 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.833 to 0.874 s | 0.862 s |
| Go | 0.804 to 0.894 s | 0.866 s |
| Python | 35.7 s | |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.805 to 0.893 s | 0.849 s |
| Kāra (`karac build`, auto-parallel) | 0.242 to 0.282 s | 0.273 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane the other languages are compared in. Python's run
is about 42 times the sequential Kāra's.

v2 took 0.98 times Rust's median time under overflow checks and 0.92
times C's. Under valgrind's cachegrind v2 ran 2,983 million
instructions with 55.8 million branches mispredicted, Rust with
overflow checks 3,507 million and 53.4 million, Rust without them 2,806
million and 56.7 million, and C 2,778 million and 56.7 million.

A plain `karac build` runs the sum over the values on all four cores,
since kara turned automatic parallelism on by default on 2026-10-26, and
takes 0.32 times the sequential build's time with the same checksum
(0.90 s of CPU time against 0.27 s of wall time). The other languages'
programs here are sequential, so that row is Kāra against itself.
