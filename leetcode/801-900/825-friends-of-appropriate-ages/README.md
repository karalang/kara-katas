# 825. Friends Of Appropriate Ages

There are `n` people, and `ages[i]` is the age of person `i`. Person `x`
does not send a friend request to person `y` (`x != y`) if any of these
holds:

- `age[y] <= 0.5 * age[x] + 7`
- `age[y] > age[x]`
- `age[y] > 100 && age[x] < 100`

Otherwise `x` sends `y` a request. Requests are one-way, and nobody
sends one to themself. Return the total number of requests.

```
ages = [16,16]                ->  2   each asks the other
ages = [16,17,18]             ->  2   17 -> 16, 18 -> 17
ages = [20,30,100,110,120]    ->  3   110 -> 100, 120 -> 110, 120 -> 100
```

**Constraints:** `1 <= n <= 2 * 10^4`, `1 <= ages[i] <= 120`.

## Approaches

Whether `x` asks `y` depends only on their two ages, of which there
are 120. For integer ages the conditions come to one range, `x / 2 + 8
<= y <= x`: the half age is `y >= x / 2 + 8` once rounded, and the third
condition needs `y > x`, which the second already refuses. So nobody
under 15 asks or is asked.

| file | mechanism |
|---|---|
| `num_friend_requests.kara` ★ | the people counted by age, and every pair of ages tested with the statement's three conditions as written, each pair that passes adding the product of the two counts, less the count once when the ages are the same. O(n + A^2) for A = 120 ages |
| `num_friend_requests_prefix.kara` | the counts turned into a running total of the people at each age or younger, so each age's range `x / 2 + 8` to `x` is one subtraction. O(n + A) |
| `num_friend_requests_sorted.kara` | the ages sorted, and two pointers that only move right: one past the people too young to be asked, the other past the people no older than the asker. O(n log n) |
| `num_friend_requests_iter.kara` | the counts built by a `fold`, and the answer a `sum` over the ages from 15 of each age's count times a `sum` over its range, less the asker |
| `differential.kara` | the four arms against the statement read person by person, four properties |

Every arm prints the same 11 lines: LeetCode's three examples; five
small cases (one person; three aged 14, who ask nobody; two aged 15, the
youngest who ask each other; 99, 100 and 101, around the third
condition; and a set at the edges of each other's ranges); two lists of
LeetCode's largest size, 20,000 random ages and 20,000 people aged 120;
and 300 random lists of up to 30 ages, with a total and a checksum.
`num_friend_requests.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every ordered pair of two different people, with the half age
computed in floating point as it is written. Its 800 cases have up to 40
people each and come in four kinds of 200: any age; ages at the edges,
13 to 16 where asking starts, 28 to 31, and 99 to 102 around the third
condition; four ages, each many times; and ages under 15 beside ages 95
to 120.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the ages in reverse order give the same answer |
| P3 | a person under 15 added anywhere changes nothing |
| P4 | everyone twice gives 4 times the answer, plus 2 for each person 15 or older, who asks their own copy and is asked back |

It prints `800 cases, 12800 checks over 4 arms: 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the half age compared with `<` for `<=` | P1 282, P3 13, P4 262 |
| M2 | ★: a person asks themself | P1 796, P4 796 |
| M3 | ★: someone of the asker's own age refused | P1 626, P4 796 |
| M4 | ★: the third condition's `and` written `or` | P1 746, P4 793 |
| M5 | prefix: the range one age too low | P1 278, P3 9 |
| M6 | prefix: the asker not taken out | P1 796, P4 796 |
| M7 | prefix: ages from 16 only | P1 98, P4 174 |
| M8 | sorted: no one of the asker's own age counted | P1 762, P4 796 |
| M9 | sorted: the young pointer one age too far | P1 278, P4 224 |
| M10 | sorted: the ages not sorted | P1 765, P2 745, P3 704, P4 710 |
| M11 | iter: the range one age too high | P1 322 |
| M12 | iter: the asker's own age left out | P1 796 |

P1 kills all twelve. The first edit tried for M3, dropping the third
condition, survived every case and was replaced: it is an equivalent
mutant, since `y > 100 and x < 100` implies `y > x`, which the second
condition already refuses, and the differential with the condition
deleted prints 0 failures. P4 misses M5, M11 and M12, whose wrong
answers still obey the doubling law; it catches the edits that touch a
person's own age (M2, M3, M6, M8), which is what its `2 for each person`
term counts. P2 sees only M10, the one arm that depends on the order of
its input.

## Verification

Every arm prints the same output as `num_friend_requests.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The release build
that runs `check` and `__mir-run` and the debug build that runs
`__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` are both at kara
`909d2c7a1f`, with the runtime archives built from that tree.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`), the legacy JIT
(`karac run`), `karac build` and an auto-par build print the same output
for all four arms, and the interpreter and `karac build` print the
differential's line. Legacy's checker refuses the bench program, which
passes `lists[round % count]` to a bare parameter and so, under legacy's
rules, moves it out of an index. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
lists of 20,000 random ages from 1 to 120 once, LeetCode's largest. Each
of 50,000 rounds answers the next list afresh: 20,000 counts, then the
pairs of the ages present, at most 14,400 tests. Every implementation
prints `50000 rounds of 64 lists: total 3972652701673, checksum
794154366`, the Kāra program under `karac __mir-run` included, in 1,683
s with the interpreter's step limit raised by `KARAC_MIR_MAX_STEPS`.

Spot timings on a shared 4-core container, eight runs of each compiled
program and 13 of v2's, five of them interleaved, and two of Python
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.59 to 1.87 s |
| Rust (`rustc -O`) | 1.64 to 1.76 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.41 to 1.66 s |
| Go | 1.57 to 1.69 s |
| Python | 90.3 to 90.9 s |
| Kāra (`karac build --mir`) | 1.72 to 2.12 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 1.84 s, against C's
1.60, Rust's 1.65 (1.57 under overflow checks) and Go's 1.63: 1.15 times
C's time. Under valgrind's cachegrind v2 runs 24.3 billion instructions,
against Rust's 19.0 billion and C's 14.9 billion, yet the times stand
closer than the counts. Most likely all five spend most of their time on
the 20,000 increments of the counting loop, where each increment waits
for the last one to the same age, and so are held to the same pace (not
traced). Built for `x86-64-v3`, the target `karac build` uses, C takes
1.65 to 1.88 s and Rust with overflow checks 1.50 to 1.79 s, against
v2's 1.85 to 2.12 s in the same five interleaved runs. Python takes 90
s, about 56 times C's time. The comparison with C and Rust waits until
after M4.

## Compiler findings

Nothing new in v2: every arm, the differential and the bench program run
on every v2 lane as written, and in the first spelling tried.
