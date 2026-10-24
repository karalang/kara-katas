# 935. Knight Dialer

The chess knight has a **unique movement**: it may move two squares
vertically and one square horizontally, or two squares horizontally and
one square vertically (with both forming the shape of an **L**).

We have a chess knight and a phone pad as shown below; the knight **can
only stand on a numeric cell**.

```
1 2 3
4 5 6
7 8 9
* 0 #
```

Given an integer `n`, return how many distinct phone numbers of length
`n` we can dial.

You are allowed to place the knight **on any numeric cell** initially
and then you should perform `n - 1` jumps to dial a number of length
`n`. All jumps should be **valid** knight jumps.

As the answer may be very large, **return the answer modulo
`10^9 + 7`**.

```
n = 1     ->  10
n = 2     ->  20
n = 3131  ->  136006598
```

**Constraints:** `1 <= n <= 5000`.

## Approaches

| file | mechanism |
|---|---|
| `knight_dialer.kara` ★ | one count for each digit of the numbers of the current length ending on it, all 1 at length 1; each jump, a digit's new count is the sum of the old counts on the digits a jump away, and the answer is the sum of the counts. O(n) |
| `knight_dialer_groups.kara` | the keypad's symmetry: the four corners, the 2 and the 8, the 4 and the 6, and the 0 each keep equal counts, so four counts are carried, the 5 counting only at length 1. O(n) |
| `knight_dialer_matrix.kara` | the 10 x 10 jump matrix raised to the power `n - 1` by repeated squaring; the sum of its entries is the answer. O(10³ log n) |
| `knight_dialer_memo.kara` | recursion on a digit and the jumps left, each result kept in a table so it is worked out once. O(n), recursion `n` deep |
| `knight_dialer_board.kara` | the keypad laid out as 4 rows of 3 cells with the two beside the 0 missing, and the jumps worked out from the board: two rows and one column, or one row and two columns, onto a cell that exists. O(n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples; the first
ten answers; `n` = 23, the last answer below `10^9 + 7`, and 24, the
first reduced by it; for every `n` from 1 to 300, the answers' sum and a
checksum; and three large lengths, 4999, 5000 (LeetCode's largest) and
2048. `knight_dialer.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every walk of `n - 1` jumps from every digit counted one at a
time, a jump being any move between two digits whose rows and columns on
the pad differ by 1 and 2. It checks 3,200 random lengths: 3,000 of 1 to
7 against the statement, and 200 of 1 to 100 against the other
properties; the lengths sum to 21,716.

The answers obey `a(n) = 6 a(n - 2) - 4 a(n - 4)` from `n` = 6 (at
`n` = 5 the 5, which counts only at length 1, breaks it), which P3, P4
and P5 use; for `n` below 6 each checks the first answers instead.

| | property |
|---|---|
| P1 | the statement's answer, on the small lengths |
| P2 | from 0 to `10^9 + 6`, and, for `n` from 2 to 23, before anything is reduced, from two to three times the answer one shorter, since after the first digit every number stands on a key with two or three jumps |
| P3 | the recurrence, from the arm's own answers two and four shorter |
| P4 | `a(n)² - a(n - 2) a(n + 2) = 4 (a(n - 2)² - a(n - 4) a(n))`, the recurrence's Cassini identity |
| P5 | the answer from the arm's own four answers `k` shorter, `k` random, with `x^k` reduced modulo `x^4 - 6x² + 4` |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 lengths summing to 21716, checksum 242895136, 95000
checks over 5 arms: 0 failures` under `karac __mir-run` (31 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

The first version checked 200 lengths up to 1,000 and asked each arm for
its answers two and four shorter and two longer once for every property
that used them; it took 135 s under `karac __mir-run`. It now asks once
for each and checks lengths up to 100.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one jump short | P1 2544, P2 452, P3 2179, P4 2179, P5 2181, P6 2743 |
| M2 | ★: the total starting at 1 | P1 3000, P2 452, P3 3200, P4 3200, P5 3200, P6 3200 |
| M3 | ★: the 5 jumping to itself | P1 2544, P3 2743, P4 2743, P5 2743, P6 2743 |
| M4 | groups: the 4 and 6 never reached from the 0 | P1 2544, P2 452, P3 2743, P4 1753, P5 2743, P6 2743 |
| M5 | groups: 9 for one digit | P1 456, P3 457, P4 457, P5 457, P6 457 |
| M6 | groups: the 0 left out of the total | P1 2544, P2 452, P3 1753, P4 1753, P5 1753, P6 2743 |
| M7 | matrix: the even bits multiplied in | P1 2544, P2 2169, P3 2743, P4 2743, P5 2742, P6 2743 |
| M8 | matrix: each jump counted twice | P1 2544, P2 2589, P3 2743, P4 2743, P5 2743, P6 2743 |
| M9 | matrix: the identity with only its first column | P1 2096, P3 1301, P4 1301, P5 1301, P6 2291 |
| M10 | memo: a finished number counted twice | P1 3000, P2 2, P3 2210, P4 2210, P5 2210, P6 3200 |
| M11 | memo: each stored count one too many | P1 2096, P3 2291, P4 2291, P5 2291, P6 2291 |
| M12 | memo: no number starting with 0 | P1 3000, P3 2210, P4 2210, P5 2210, P6 3200 |
| M13 | board: keys beside the 0 instead of the 0 | P1 3000, P3 3200, P4 3200, P5 3200, P6 3200 |
| M14 | board: two down and one left in place of two down and one right | P1 1679, P3 1871, P4 1871, P5 1871, P6 1871 |
| M15 | board: the two blank cells counted for one digit | P1 456, P2 452, P3 457, P4 457, P5 457, P6 457 |

P1, P3, P4, P5 and P6 kill all fifteen and P2 eight. The counts fall in
a few sizes: 3,000 and 3,200 are every length, 2,544 and 2,743 every
length above 1, 456 and 457 length 1 alone, 1,753 lengths 2 to 5, where
P3, P4 and P5 check the first answers, and 452 length 2.

P2 sees a mistake only where it changes how fast the answers grow. At
`n` = 2 five fall below twice their own answer at 1 (M1, M2, M4, M6,
M15); M7 and M8 change the growth everywhere, M8 doubling it at every
jump; and M10 doubles every answer, which keeps every ratio until the
doubled answer is first reduced, at `n` = 23. The other seven grow at
the right rate: off by a fixed amount (M3), wrong at length 1 only (M5),
wrong from length 3 on by amounts that keep the ratio (M9, M11),
starting from the wrong keys (M12 never on the 0, M13 on the two cells
beside it instead), or, for M14, right at length 2, since the lost jumps
and the doubled ones balance.

The answers of M6 and M4 still obey a recurrence, so the properties
built on one catch them only through the first answers. M6 leaves the
0's count out of the total, and any fixed mix of the four group counts
obeys the same recurrence, so P3, P4 and P5 fail it only at lengths 2 to
5. M4's corners, 2 and 8, and 4 and 6, never reached from the 0, grow
fourfold every two jumps, which breaks P3's and P5's recurrence; but
answers growing fourfold every two jumps make both sides of P4's
identity 0, so P4 fails it only at lengths 2 to 5. M9 starts the power
from a matrix whose every row is the 0's row of the identity, which
gives ten times the numbers starting on the 0: right at lengths 1 and 2,
wrong from 3.

Seven other edits were tried and set aside. Three failed exactly the
same checks as each other, so none was kept: ★ never reaching the 4 from
the 0, and groups reaching the 0 from only one side key or the 2 and 8
from only one corner. Three failed exactly the same checks as a kept
mutant: board never jumping to the bottom row, as M4; matrix skipping
entries of 1 in the product, which answers 0 from length 2 on (and 0
obeys every recurrence), as M6; and matrix raising to one power too
many, as M10. One was equivalent: memo taking a stored count of 0 as not
stored, since only the 5 ever stores 0 and working it out again gives 0.

## Verification

Every arm prints the same output as `knight_dialer.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 0.15 to 3.2 s each and the
differential 31 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The groups arm prints the same output under the frozen legacy
interpreter, the legacy JIT and both legacy builds, with and without
auto-par. Legacy refuses the other four arms, the differential and the
bench program at the first `*` on an element of a `Vec[i64]`'s
`.iter()` ("unary '*' requires 'ref T', ... found 'i64'"), legacy's
older rule; under v2 the element is a reference and the `*` is
required. Legacy is frozen, so none of this is filed.

## Benchmarks

The bench program runs the ★ arm on every length from 4,901 to 5,000,
the top of LeetCode's range, in each of 20 rounds, each round starting
from a different length. Every implementation prints `20 rounds over n
from 4901 to 5000: answers summing to 984927497420, checksum 19390351`.
C keeps the jumps in a fixed table with each digit's count of jumps; the
others keep them as a list of lists.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.09 to 0.13 s | 0.10 s |
| Rust (`rustc -O`) | 0.37 to 0.45 s | 0.42 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.39 to 0.47 s | 0.41 s |
| Go | 0.63 to 0.78 s | 0.73 s |
| Python | 17.6 s | |
| Kāra (`karac build --mir`) | 0.47 to 0.53 s | 0.49 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about 178 times C's.

v2 takes 1.19 times Rust's median time under overflow checks and 4.95
times C's. Under valgrind's cachegrind v2 runs 8.09 billion instructions
and 1.40 billion branches with 49.5 million mispredicted, Rust with
overflow checks 7.46 billion, 1.25 billion and 9.93 million, and C 1.24
billion and 10.0 million branches with 7,800 mispredicted. C's table
has a fixed size and its counts of jumps are constants, so clang can
unroll the whole jump, which would explain its few branches; v2's five
mispredictions a jump against Rust's one would come from the loops over
jump lists of 0, 2 and 3 entries. Both are inferred, not profiled.
