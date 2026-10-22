# 842. Split Array into Fibonacci Sequence

Given a string of digits `num`, split it into a Fibonacci-like sequence:
a list `f` of non-negative integers, each below `2^31`, with at least
three numbers, where `f[i] + f[i + 1] == f[i + 2]` for every `i`. When
the string is split into pieces, no piece may start with `0` unless it
is the number `0` itself. Return any Fibonacci-like sequence split from
`num`, or `[]` if there is none.

```
num = "1101111"      ->  [11, 0, 11, 11]   ([110, 1, 111] is also right)
num = "112358130"    ->  []
num = "0123"         ->  []
```

**Constraints:** `1 <= num.length <= 200`, and `num` holds only digits.

## Approaches

LeetCode accepts any split. So that every arm prints the same answer,
each returns the same one: the split whose first number is shortest, and
then its second. Every arm rests on the same fact, that the first two
numbers decide the rest.

| file | mechanism |
|---|---|
| `split_into_fibonacci.kara` ★ | the first two numbers decide the rest: every pair of lengths for the first two numbers is tried, the first's shortest first and then the second's, each at most 10 digits since no number passes 2^31 - 1; each sum's digits are matched against the string until it runs out, a sum passes 2^31 - 1 or the digits differ. O(n) for each of at most 100 pairs |
| `split_into_fibonacci_backtrack.kara` | backtracking: from each position every number the next digits can make is tried, shortest first, stopping at a leading 0, at 2^31 - 1, or, after the first two, at a number past the sum it must equal; a number that fits is pushed, the rest is split the same way, and it is popped on failure |
| `split_into_fibonacci_concat.kara` | whole strings: for each pair of first two numbers the sequence they start is written out as one string, sum after sum, while it is shorter than the input, and compared with the input |
| `split_into_fibonacci_digits.kara` | sums in digits: the numbers are kept as their digits and each sum worked out digit by digit with a carry, a number past 2^31 - 1 told by comparing its digits with `2147483647`; nothing is converted to an integer until the answer is |
| `differential.kara` | the four arms against the statement read literally, four properties |

Every arm prints the same 18 lines: LeetCode's three examples; eleven
more (`"11235813"`, `"000"`, `"0000"`, `"101"`, the one- and two-digit
strings `"1"` and `"10"`, `"1011"`, which needs a 0 in the middle, a
sequence that passes 2^31 - 1 at its third number, one of `2147483647,
0, 2147483647, 2147483647`, which stays exactly at the limit, and
`"1023"`); three strings of LeetCode's most digits, 200, the sequences
from 1, 1 and from 0, 0 and the one from 98765, 43210; and 300 random
strings with how many split and a checksum. `split_into_fibonacci.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the first two numbers may have any lengths, a number is a
part with no leading 0 unless it is `0` and no greater than 2^31 - 1,
each later number must be the next part of the string written out, the
split must use the whole string and have at least three numbers, and of
the splits the one whose first number is shortest, then its second, is
taken. It reads every part as a string, with none of the arms' bounds on
the lengths; it stops trying longer parts only once one is not a number,
since a part that is not a number stays one when it grows.

Its 1,600 cases come in four kinds of 400: 1 to 10 digits drawn from `0`
alone, from `0` and `1`, or from `0` to `2`; sequences two numbers below
20 start, written out to 3 to 42 digits, one in three with a digit
changed; the same from numbers of up to 1, 3 or 6 digits, out to 62
digits; and sequences that run up to 2^31 - 1, a quarter of them from
two 9-digit numbers, a quarter whose first number has 10 digits, a
quarter whose second has, one in four of those three with a digit
changed and half with `a + 2b` written after them, and a quarter that
are three numbers summing to 2^31 - 1 or one past it. 807 of them split.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the answer is a split of the input, or `[]` |
| P3 | each prefix of the answer written out, ending at a number after the third and before the last, gives the statement's answer for it |
| P4 | the input with one more number written after it, the sum of the answer's last two numbers (or `1` when there is no answer), gives the statement's answer for it |

It prints `1600 cases, 807 split, 25600 checks over 4 arms: 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a leading 0 allowed | P1 21, P2 21, P4 51 |
| M2 | ★: no 2^31 - 1 limit on a sum | P1 59, P2 59, P4 207 |
| M3 | ★: a split of two numbers accepted | P1 342, P2 342, P3 195, P4 43 |
| M4 | ★: the first number at most 9 digits | P1 77 |
| M5 | backtrack: a split of two numbers accepted | P1 342, P2 342, P3 195, P4 43 |
| M6 | backtrack: no 2^31 - 1 limit | P1 59, P2 59, P4 207 |
| M7 | backtrack: a leading 0 allowed | P1 27, P2 27, P4 62 |
| M8 | concat: the second number at most 9 digits | P1 80 |
| M9 | concat: the sequence written one sum short | P1 121, P3 49, P4 12 |
| M10 | digits: a carry out of the top digit dropped | P1 453, P4 38 |
| M11 | digits: 2147483648 not too big | P1 59, P2 59 |
| M12 | digits: the input's last number not checked | P1 807, P4 19 |

P1 kills all twelve. P2, which checks the answer without knowing the
statement's, sees every edit that returns something that is not a split
at all: a part with a leading 0 (M1, M7), a number past 2^31 - 1 (M2,
M6, M11) or only two numbers (M3, M5). The edits that only miss a split
(M4, M8, M9, M10, M12) it cannot see, since `[]` is always allowed. P4
writes one more sum after the answer, so it sees the limit edits most
(M2, M6, 207 each): a sequence that ends just below 2^31 - 1 is pushed
past it. M12 fails exactly the 807 cases that split, since the last
number never fits. M4 and M8 need a 10-digit first or second number and
are seen only by P1, on the cases built for them.

Two edits first survived. The 10-digit and limit edits (M4 and M11)
killed nothing until the fourth kind gained the cases with a 10-digit
first or second number and the three numbers summing to 2^31 - 1 or one
past it. And the first M8, dropping the whole-string arm's check of a
leading 0 on its second number, cannot be killed: that arm compares the
input with the numbers written out, and a number is never written with a
leading 0, so the check only saves work. It was replaced by the edit
that shortens the second number.

## Verification

Every arm prints the same output as `split_into_fibonacci.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `9b3f18a2c7`, and the runtime archives are
current with them. Under `karac __mir-run` the arms take 0.2 to 0.37 s
and the differential 10.7 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends refuse every arm, the differential and the
bench program at a `*x` read through `.iter()` over integers or bytes:
legacy types the loop variable as the integer itself, not a reference,
though `karac check` accepts it on v2. Legacy also refuses the
differential's `add(seq[k - 2], seq[k - 1])` as moving a `Vec[u8]` out
of an index, which v2's borrowing parameters do not do. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
strings once, each at most LeetCode's 200 digits: string `g` writes out
the sequence two random numbers of up to 1, 3 or 5 digits start, sum
after sum, while it stays within 200 digits and 2^31 - 1, and one string
in four then has one digit changed. Each of 240,000 rounds splits the
next string. Every implementation prints `240000 rounds of 64 strings:
180000 split, checksum 626390444`, the Kāra program under `karac
__mir-run` included, in 330 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.61 to 0.73 s |
| Rust (`rustc -O`) | 0.52 to 0.60 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.53 to 0.59 s |
| Go | 0.71 to 0.77 s |
| Python | 11.3 to 11.7 s |
| Kāra (`karac build --mir`) | 0.95 to 1.05 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 0.98 s, against Rust's
0.53 (0.55 under overflow checks), C's 0.63 and Go's 0.75: 1.78 times
Rust's time under overflow checks, 1.56 times C's and 1.31 times Go's.
Under valgrind's cachegrind C runs 10.0 billion instructions and 1.22
billion branches, Rust 8.0 billion and 1.33 billion, and v2 16.0 billion
and 2.88 billion, with 94 million mispredicted against C's 38 and Rust's
50 million. Each sum the ★ arm writes out becomes a `String` and then a
`Vec[u8]` of its bytes, two allocations where Rust makes one and C none;
most likely those and the copy between them are much of v2's extra work
(not traced). Built for `x86-64-v3`, the target `karac build` uses, C
takes 0.64 to 0.68 s and Rust with overflow checks 0.53 to 0.58 s,
against v2's 0.98 to 1.04 s in the same five interleaved runs. Python
takes 11.5 s, about 18 times C's time. The comparison with C and Rust
waits until after M4.
