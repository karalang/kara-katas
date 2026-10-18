# 747. Largest Number At Least Twice of Others

In the list `nums` the largest value is unique. Return its index if it
is at least twice every other value, and -1 otherwise.

```
nums = [3, 6, 1, 0]  ->   1
nums = [1, 2, 3, 4]  ->  -1
```

**Constraints:** 2 to 50 values; 0 <= `nums[i]` <= 100; the largest
value is unique.

## Approaches

The largest value is at least twice every other exactly when it is at
least twice the second largest, so every arm comes down to finding those
two.

| file | mechanism |
|---|---|
| `dominant_index.kara` ★ | one pass keeping the largest value's index and the second largest value; O(n) |
| `dominant_index_twopass.kara` | the statement read straight: find the largest, then check every other value against it; O(n), two passes |
| `dominant_index_sort.kara` | sort (value, index) pairs and compare the last two; O(n log n) |
| `dominant_index_count.kara` | count each value from 0 to 100, read the two largest down from 100, then find where the largest sits; O(n + 101) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 11 lines: the two LeetCode examples; both
orders of 0 and 1; a largest value exactly twice the other, and one more
than twice; 100 against two 50s and a 49; a single 1 among zeros; a list
of 50 random values below 100 with one 100, and one with the others at
most 50; and 300 random lists of 2 to 11 values, with how many have a
dominant value and a checksum. `dominant_index.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which tries every index against every other value and returns the first
index whose value is at least twice all the others. 3,000 random lists
are checked, each of 2 to 8 values with a unique largest value of 1 to
33 at a random place, and the others below it or, half the time, at most
half of it, so that 1,809 of them have a dominant value. The largest is
kept to 33 so that P3's tripled values stay within the constraint.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the values in reverse order give the index reversed, n - 1 - i, or -1 still |
| P3 | every value tripled gives the same answer |
| P4 | half the largest value, rounded down, added at the end gives the same answer |

It prints `3000 lists (1809 with a dominant value), 4 arms,
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
| M1 | ★: exactly twice not enough | P1 380, P4 522 |
| M2 | ★: the old largest not kept as the second | P1 279, P2 537 |
| M3 | ★: the second largest updated by a smaller value | P1 819, P2 677, P4 372 |
| M4 | twopass: exactly twice not enough | P1 380, P4 522 |
| M5 | twopass: the first value never checked | P1 137, P2 262 |
| M6 | twopass: the largest checked against itself | P1 1809 |
| M7 | sort: the largest checked against the smallest | P1 1027, P4 164 |
| M8 | sort: the position in sorted order returned | P1 1328, P2 1809, P4 1809 |
| M9 | sort: the largest only checked against the second, not twice it | P1 1191 |
| M10 | count: the second largest searched from the largest itself | P1 1809 |
| M11 | count: the largest checked against the second, not twice it | P1 1191 |
| M12 | count: the index of the second largest returned | P1 1809, P2 475, P4 1020 |
| E1 | ★: the second largest starting at 0, not -1 | 0 |
| E2 | twopass: a tie for the largest going to the later index | 0 |
| E3 | count: one more unused count | 0 |

P1 kills all twelve. M1 and M4 are one mistake in two arms, refusing a
largest value of exactly twice the second, and fail exactly the same
checks; P4 sees it as well, since half an even largest value added at
the end is exactly half of it. M9 and M11 are likewise one mistake,
comparing the largest with the second rather than with twice it, and
fail the same 1,191 checks. M6 and M10 compare the largest with itself,
so every list with a dominant value answers -1: they fail on all
1,809 such lists, and only P1 sees them, since -1 is consistent under
every transformation. P2 sees the edits that depend on order,
M2, M3, M5, M8 and M12, since reversing the list moves which value is
met first. P3 sees none: every comparison here is between a value and
twice another, which tripling every value does not change. E1 starts the
second largest at 0 rather than -1, the same thing for values that are
never negative; E2 sends a tie for the largest to the later index, and
the largest is unique; E3 adds a count that is never read.

## Verification

Every arm prints the same output as `dominant_index.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`1a5c083e3a`, whose last compiler change is `4655692faa`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept the ★, two-pass and sort arms and the
bench program: each of those arms prints the same output under the
legacy interpreter, `karac run`, `karac build` and an auto-par build.
They refuse the count arm and the differential at type checking, at a
`*` over a vector's `iter()` (`count[*x]`), since legacy gives those by
value where v2 gives references. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes a pool
of 100,000 random values from 0 to 51 once, and for each of 2 million
lists copies 50 values from a random place in the pool into one buffer
and sets one of them, chosen in turn, to 100, so that the largest is
unique as LeetCode promises and is dominant in about a third of the
lists. Every implementation prints `2000000 lists of 50 values:
725413 have a dominant value, indices sum to 17781430`, the Kāra program
under `karac __mir-run` included (in 40 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.26 to 0.29 s |
| Rust (`rustc -O`) | 0.25 to 0.30 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.25 to 0.28 s |
| Go | 0.27 to 0.33 s |
| Python | 7.2 to 7.6 s |
| Kāra (`karac build --mir`) | 0.28 to 0.34 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
2.2 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 0.30 s,
level with Go (0.30), against C's 0.27 and Rust's 0.26 with or without
overflow checks, about a tenth behind C and an eighth behind Rust. Under
valgrind's cachegrind v2 runs 2.6 billion instructions and 0.51 billion
branches, against C's 1.3 billion and 0.12 billion and Rust's
1.5 billion and 0.21 billion; the extra branches are presumably bounds
and overflow checks, almost all predicted (v2 mispredicts 1.0% of its
branches, C 6.7%), which is why the time gap is so much smaller than the
instruction gap (inferred, not read from the code). The legacy build of
the same program ran 0.27 to 0.29 s, a median of 0.29 s in the
interleaved runs, so v2 is within a few per cent of legacy, inside M2's
limit of twice legacy; new katas' benches are outside M2's frozen set in
any case. The comparison with C and Rust waits until after M4.

## Compiler findings

None new.
