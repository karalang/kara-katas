# 1018. Binary Prefix Divisible By 5

Given a binary array `nums`, let `x_i` be the number whose binary form
is `nums[0..=i]`, most significant bit first. Return a list of booleans
whose `i`-th entry says whether `x_i` is divisible by 5.

```
nums = [0, 1, 1]  ->  [true, false, false]    (0, 1, 3)
nums = [1, 1, 1]  ->  [false, false, false]   (1, 3, 7)
```

**Constraints:** `1 <= nums.length <= 10^5`, each `nums[i]` is 0 or 1.

## Approaches

The prefixes grow by a bit at each step, so after 63 bits they no longer
fit an `i64`; but each prefix is twice the last plus its new bit, so
whether 5 divides it depends only on the last one's remainder.

| file | mechanism |
|---|---|
| `prefix.kara` ★ | running remainder: `r = (2r + bit) mod 5`, and the prefix is a multiple of 5 when `r` is 0. O(n) |
| `prefix_table.kara` | a five-state machine: the ten transitions written as a table and followed, accepting in state 0. O(n) |
| `prefix_full.kara` | the prefix in full: kept exactly in base `10^9` limbs, doubled with the bit added, and tested by its last decimal digit. O(n^2 / 30) |
| `prefix_weights.kara` | place weights: powers of 2 mod 5 repeat 1, 2, 4, 3, so count the ones at each index mod 4 and weigh the counts by how far each class sits above the last bit. O(n) |
| `prefix_lazy.kara` | reducing late: let the prefix grow as a plain `i64`, test it with one remainder, and reduce it mod 5 only once it passes `2^60`. O(n) |
| `differential.kara` | the five arms against the prefixes computed exactly, six properties |

Every arm prints the same 16 lines: the answers for ten arrays,
LeetCode's two examples among them; and for six groups of random arrays
(10 to 3,000 bits, with a 1 at each place with probability 1/8, 1/2 or
7/8), how many answers are true, the longest run of true answers and a
checksum. `prefix.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and checks 9,720
arrays: every array of 1 to 12 bits (8,190), 1,500 random arrays of 13
to 200 bits and 30 of 1,000, with 1 to 7 ones in 8. Each array is also
asked with a 0 after it, a 0 before it, `0000` put in at a random place,
and one random bit turned over.

| | property |
|---|---|
| P1 | the answers for the first 62 prefixes, computed exactly as `i64`s, and one answer for each bit |
| P2 | a 0 after the array repeats the last answer |
| P3 | a 0 before the array adds a true answer in front |
| P4 | `0000` put in anywhere changes no later answer and repeats the answer before it four times, since 16 is 1 mod 5 |
| P5 | turning a bit over changes no earlier answer, and leaves no later answer true in both, since it moves every later prefix by a power of 2 |
| P6 | each arm agrees with at least two of the other four |

The differential prints `9720 arrays: checksum 599191209, 291600 checks
over 5 arms: 0 failures` under `karac __mir-run` (13 s) and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Thirty edits to the differential, each run under `karac __mir-run` and
`karac __mir-llvm-run`; fifteen are kept, three to each arm, all
fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: remainders mod 10 | P1 7126, P2 959, P4 757, P6 7151 |
| M2 | ★: the prefix not doubled | P1 7863, P6 7878 |
| M3 | ★: each answer one prefix late | P1 9706, P2 1927, P4 2091, P5 2967, P6 9706 |
| M4 | table: state 4's transitions swapped | P1 3840, P4 1817, P5 1460, P6 3911 |
| M5 | table: state 4 on a 1 back to 0 | P1 4440, P5 1806, P6 4537 |
| M6 | table: state 0's transitions swapped | P1 9720, P2 2040, P3 9720, P4 2904, P5 3032, P6 9720 |
| M7 | full: limbs of `10^9 + 7`, not a power of 10 | P1 1354, P2 261, P4 1312, P5 634, P6 1363 |
| M8 | full: the bits never added | P1 9706, P5 9720, P6 9706 |
| M9 | full: the top limb tested | P1 1323, P2 266, P4 1258, P5 1201, P6 1341 |
| M10 | weights: the cycle 1, 2, 3, 4 | P1 8485, P2 2703, P4 2929, P6 8488 |
| M11 | weights: ones marked, not counted | P1 7145, P5 5196, P6 7161 |
| M12 | weights: the classes counted the wrong way round | P1 4922, P6 4955 |
| M13 | lazy: reduced mod 3 | P1 225, P2 8, P4 763, P5 91, P6 1011 |
| M14 | lazy: divided by 5, not reduced | P1 165, P2 151, P4 1097, P5 831, P6 1124 |
| M15 | lazy: the bits inverted | P1 9720, P2 3866, P3 9720, P4 8257, P6 9720 |

P1 and P6 kill all fifteen, P4 and P5 ten, P2 nine and P3 two. P6
counts more arrays than P1 for most of them because P1 checks only the
first 62 prefixes; M13 and M14 go wrong only after the first reduction,
past bit 60,
at the last few prefixes P1 checks. The checks
draw no random number that depends on an answer, so every mutant sees
the same arrays and their counts can be compared.

Fifteen other edits were tried and set aside. Four change no answer:
full computing a carry ten times too big, which spoils the upper limbs
but not the lowest, the only one tested; weights rotated to 3, 1, 2, 4,
which is three times the right cycle mod 5; lazy reducing mod 10 instead
of 5; and lazy waiting until `2^62`, still the largest value that can be
doubled in an `i64`. Three failed exactly the same checks as a kept
one: table indexing by `state + 2 * bit` (as M2), full accepting only a
last digit of 0 (as M1), and full never doubling the lowest limb (as
M8). The other eight were killed too, beyond three per arm: ★ with the
test inverted, remainders mod 4 and a start of 1; table accepting state
4 too and starting in state 2; weights leaving a class out and refusing
an all-zero prefix; and lazy never reducing, which overflows `i64` in
both lanes.

## Verification

Every arm prints the same output as `prefix.py` under `karac __mir-run`
(the v2 MIR interpreter) and `karac __mir-llvm-run`, and under `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error; the
differential prints its line under all three. `karac check
--output=json` reports no diagnostic for the five arms, the differential
and the bench program, so `karac fix` had nothing to do. `karac run` and
a `karac build` binary print the same output for every arm and the
differential. The release build is kara `56c60bdf7c`, with runtime
archives rebuilt at `ce706dd131`, the last commit before it to change
the runtime. Under `karac __mir-run` the arms take 0.4 s (table) to
1.2 s (full).

The harness first printed each array with `{nums:?}`, which `karac
check` refuses: `?` is reserved for Debug formatting, not implemented
yet, as design.md says, and the diagnostic points to `{nums}`, which
prints a `Vec` the same way. No compiler gap turned up.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench builds one random array of 2,000,000 bits and answers it 50
times in all five languages, turning one bit over before each round and
folding the answers into a count and a sum of the true answers' indices:
100 million steps of the remainder, each a multiplication, an addition
and a remainder by 5, and an answer array allocated per round. Every
implementation prints `50 rounds over 2000000 bits: 20017002 true,
index sum 357932935`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.788 to 0.849 s | 0.805 s |
| Rust (`rustc -O`) | 0.735 to 0.811 s | 0.747 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.772 to 0.865 s | 0.803 s |
| Go | 1.134 to 1.243 s | 1.186 s |
| Python | 10.1 s | |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.783 to 0.855 s | 0.824 s |
| Kāra (`karac build`) | 0.793 to 0.878 s | 0.836 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(its user time equals its real time) and runs as fast as the sequential
one.

v2 took 1.03 times Rust's median time under overflow checks and 1.02
times C's. Each step's remainder feeds the next, so the loop is one
dependent chain in every language, and the four compiled programs land
within a few percent of each other. Go is about 1.5 times slower; we
did not measure where its time goes.
