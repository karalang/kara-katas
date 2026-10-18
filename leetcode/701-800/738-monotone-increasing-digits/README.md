# 738. Monotone Increasing Digits

An integer has monotone increasing digits when each pair of adjacent
digits `x` and `y`, `x` first, has `x <= y`. Given an integer `n`,
return the largest number no greater than `n` with monotone increasing
digits.

```
n = 10    ->  9
n = 1234  ->  1234
n = 332   ->  299
```

**Constraints:** 0 <= `n` <= 10^9.

## Approaches

When the digits of `n` are already monotone the answer is `n`. Otherwise
the answer keeps the longest monotone start of `n` that it can, lowers
one digit by one, and fills every place after it with 9s; the arms
differ in how they find that digit and whether they work on a list of
digits, on the number itself or on its text.

| file | mechanism |
|---|---|
| `monotone_increasing_digits.kara` ★ | put the digits in a `Vec`, find the first place where a digit is larger than the next, step back over the equal digits before it so that the lowered digit is the first of them, lower it by one and make every later digit a 9; O(d) for d digits |
| `monotone_increasing_digits_arith.kara` | no list of digits: walk the places from the units up, and wherever a digit is larger than the one to its right, cut the number below that place to zeros and subtract one, which lowers the digit and turns everything to its right into 9s; the lowered digit is then compared with the next place to its left in turn |
| `monotone_increasing_digits_build.kara` | choose the answer's digits from the left, each as large as it can be: a digit is possible when the digits so far, then it, then it again in every place left make a number no greater than `n`, since that is the smallest way to finish with it; O(9 d) |
| `monotone_increasing_digits_fromright.kara` | work on the decimal text of `n`: walk from the right, lowering a digit by one wherever it is larger than the one after it and remembering the place after it, then make every digit from the leftmost remembered place a 9 |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 16 lines: the three LeetCode examples; eleven
more numbers, among them `0`, `100`, `1000000000`, `111111110` and
`123454321`; 10,000 random numbers of 1 to 10 digits up to 10^9 with how
many are already monotone and a checksum of the answers; and the sum of
the answers for every number under a hundred thousand.
`monotone_increasing_digits.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the largest number with monotone digits no greater than `n`, looked up
by binary search in the sorted list of every such number. A number with
monotone digits is a choice of how many times to use each digit 1 to
9, written in order, so the list is made by counting through every such
choice of at most ten digits: 92,378 numbers with 0. Before the cases,
the differential checks the list against a digit test on every number
below 100,000, and both find 2,002. 3,000 numbers are checked: a third
random numbers of 1 to 9 digits, a third a listed number moved up or
down by at most 10, and a third numbers of 1 to 9 digits made of one
digit with another in about one place in four. 904 of them are already
monotone.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the answer has monotone digits and is between 0 and `n` |
| P3 | the answer for `n + 1` is no smaller |
| P4 | the answer is its own answer, and `n` is its own answer exactly when its digits are monotone |

It prints `92378 monotone numbers listed, 2002 below 100000, digit test
finds 2002` and `3000 numbers (904 already monotone), 4 arms,
48000 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no step back over equal digits | P1 496, P2 496, P4 496 |
| M2 | ★: equal neighbours taken for a drop | P1 1433, P4 2539 |
| M3 | ★: the places after the drop made 0s | P1 2096, P2 2078, P3 171, P4 2078 |
| M4 | arith: equal neighbours cut | P1 1581, P4 2539 |
| M5 | arith: the cut not followed by subtracting one | P1 2096, P2 2096, P4 157 |
| M6 | arith: the leading place never compared | P1 795, P2 795, P4 211 |
| M7 | build: a finish one place too long | P1 2936, P4 2934 |
| M8 | build: a digit tried with 9s after it | P1 1881, P4 580 |
| M9 | build: a finish equal to n refused | P1 840, P4 2936 |
| M10 | fromright: the first 9 left out | P1 2096, P2 1393, P3 171, P4 1393 |
| M11 | fromright: the 9s starting a place late | P1 2096, P2 1393, P3 171, P4 1393 |
| M12 | fromright: the first two places never compared | P1 795, P2 795, P4 211 |
| E1 | build: a digit tried down to 1, not down to the last digit | 0 |
| E2 | arith: one more place, past the leading digit | 0 |
| E3 | ★: stepping back over larger digits too | 0 |

P1 kills all twelve, and P4 does too: every edit gives some number an
answer that is not its own answer, or makes a monotone number not its
own. M10 and M11 are one mistake, the 9s starting a place late, and fail
the same 5053 checks; M6 and M12 are one mistake in two arms, the first
two places never compared, and fail the same 1801. M2 and M4 both take
equal neighbours for a drop and fail the same 2539 checks under
P4, since a monotone number with a repeated digit is then not its own
answer. P2 sees the edits whose answer is not monotone: M1 lowers a
digit below the equal one before it, M3 and M5 leave 0s after the drop,
M6 and M12 leave the first two places out of order, and M10 and
M11 leave a lowered digit before an unchanged larger one. The rest give
a monotone answer that is merely too small, which only P1 and P4 can
see. P3 sees M3, M10 and M11, whose wrong answers can fall from one
number to the next. E1 tries digits down to 1 rather than down to the
last digit chosen, but that digit always passes, since the digits so far
with it repeated make the finish that passed one step before;
E2 compares one place more, the leading digit with the 0 to its left,
which is never larger; E3 steps back over digits no smaller than the one
at the drop, but the digits before the first drop are in order, so those
are the equal ones.

## Verification

Every arm prints the same output as `monotone_increasing_digits.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and under `karac __mir-llvm-asan` (AddressSanitizer)
with no error; the differential prints its line under all three. `karac
check` passes all four arms, the differential and the bench program. The
debug build that runs `__mir-llvm-run`, `__mir-llvm-asan` and `build
--mir` and the release build that runs `check` and `__mir-run` are both
at kara `3df39964e7`, whose last compiler change is `56339e6224`. The
runtime archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse the ★ and fromright arms, the
differential and the bench program at type checking, at a `*` over a
vector's `iter()` (`*d` over the digits, `*b` over the bytes, `*v` over
the list of monotone numbers), since legacy gives those by value where
v2 gives references. They accept the arith and build arms, which print
the right output under the legacy interpreter, `karac run`, `karac
build` and an auto-par build. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws
3,000,000 random numbers from 0 to 1,000,000,000, two draws of the
generator each, and sums their answers; each call puts the number's
digits in a fresh growable array, as the ★ arm does, which in C is a
`realloc`ed buffer freed at the end of the call. Every implementation
prints `3000000 random numbers: 201 already monotone, answers sum to
1352320521506198`, the Kāra program under `karac __mir-run` included (in
56 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.20 to 0.27 s |
| Rust (`rustc -O`) | 0.27 to 0.33 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.26 to 0.38 s |
| Go | 0.57 to 0.66 s |
| Python | 5.0 to 5.2 s |
| Kāra (`karac build --mir`) | 0.22 to 0.32 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 2.2 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is level with C at the medians of the interleaved runs
(0.23 s against 0.22), a sixth ahead of Rust (0.27) and a quarter ahead
of Rust under overflow checks (0.30), and well ahead of Go (0.60). Under
valgrind's cachegrind it runs 3.2 billion instructions against C's
3.1 and Rust's 4.0, with 570 million branches against 454 and 556, and
23 million mispredicted against 14 and 18. Why Go takes more than twice
as long was not traced. The comparison with C and Rust waits until after
M4.

## Compiler findings

None new.
