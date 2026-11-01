# 1031. Maximum Sum of Two Non-Overlapping Subarrays

Given an integer array `nums` and two integers `firstLen` and
`secondLen`, return the maximum sum of elements in two non-overlapping
subarrays with lengths `firstLen` and `secondLen`. The array with
length `firstLen` could occur before or after the array with length
`secondLen`, but they have to be non-overlapping.

```
nums = [0,6,5,2,2,5,1,9,4],    firstLen = 1, secondLen = 2  ->  20
nums = [3,8,1,3,2,1,8,9,0],    firstLen = 3, secondLen = 2  ->  29
nums = [2,1,5,6,0,9,5,0,3,8],  firstLen = 4, secondLen = 3  ->  31
```

**Constraints:** `firstLen` and `secondLen` are at least 1;
`firstLen + secondLen` is at most `nums.length`, which is at most
1,000; every value is from 0 to 1,000.

## Approaches

| file | mechanism |
|---|---|
| `max_two.kara` ★ | one pass over prefix sums: walk the end `i` of the right-hand window; when it is the second-length window, the best first-length window ending at or before its start is a running maximum, and the same with the two lengths the other way round. O(n) |
| `max_two_pairs.kara` | every pair of windows: each start of the first-length window against each start of the second-length one, keeping the pairs where one ends at or before the other starts, each sum one subtraction of prefix sums. O(n^2) |
| `max_two_sides.kara` | the best window to the right: slide a window of each length along the array for the sum starting at every index, keep the best right-hand window starting at each index or later, and pair every left-hand window with the best one starting where it ends, once with each length on the left. O(n) |
| `max_two_memo.kara` | recursion with a memo: from index `i` on, with some windows still to place, skip `nums[i]` or start a wanted window there; the best, or `None` when the windows wanted no longer fit, is kept in a `Map` keyed by `(i, windows wanted)`. O(n) states |
| `max_two_table.kara` | a table from the right: `best[i][w]` is the largest sum of the windows in the set `w` placed in `nums[i..]`, or -1 when they do not fit (every value is at least 0, so no real sum is -1), filled from the right end. O(n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 18 lines: the answers for eight arrays,
LeetCode's three examples among them; for six groups of random arrays
(3,000 of 4 values down to 10 of 1,000, with values up to 1 to 1,000
and random lengths), the sum of the answers and a checksum; and four
answers on 1,000 values, every one 1,000 or rising from 0 to 999.
`max_two.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: of every first-length subarray and every second-length one
that share no index, the largest total, each summed element by element.
It checks 1,206 cases: every array of 2 to 4 values from 0 to 2 with
every pair of lengths that fits (576), then 600 random arrays of 2 to 30
values and 30 of 31 to 300, with values up to 3, 20 or 1,000 and random
lengths. The 1,176 arrays of at most 30 values are searched in full.
Each case is also asked with the two lengths swapped, with the array
reversed, and with every value raised by a random amount from 1 to 50.

| | property |
|---|---|
| P1 | the statement read literally, on arrays of at most 30 values |
| P2 | which length is called first does not matter |
| P3 | reversing the array does not change the answer |
| P4 | with every value raised by `k`, the answer rises by `k` for each of the `firstLen + secondLen` values |
| P5 | the answer is at least the best window of both lengths together, which splits into two that do not overlap, and at most the best window of each length added |
| P6 | each arm agrees with at least two of the other four |

The differential prints `1206 cases (1176 searched in full): checksum
951028693, 36030 checks over 5 arms: 0 failures` under `karac
__mir-run` (2.9 s), `karac __mir-llvm-run` and `karac __mir-llvm-asan`
with no error.

## Mutation testing

Thirty edits to the differential, each run under `karac __mir-run` and
`karac __mir-llvm-run`. Fifteen are kept, three to each arm. All fifteen
are killed, each fails the same checks under both backends, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the pairs that start at index 0 never tried | P1 811, P3 470, P4 500, P5 650, P6 815 |
| M2 | ★: only the window just left, not the best so far | P1 139, P2 311, P3 311, P6 160 |
| M3 | ★: the right-hand window measured with the wrong length | P1 561, P2 850, P3 112, P4 575, P5 427, P6 586 |
| M4 | pairs: two windows that touch counted as overlapping | P1 659, P4 500, P5 661, P6 661 |
| M5 | pairs: the last start of the second window never tried | P1 80, P2 174, P3 162, P6 87 |
| M6 | pairs: the first window never at index 0 | P1 89, P2 167, P3 179, P6 92 |
| M7 | sides: the window starting at `j`, not the best from `j` on | P1 359, P6 387 |
| M8 | sides: the right-hand window never just after the left | P1 552, P3 126, P4 500, P5 554, P6 554 |
| M9 | sides: the first value never slid out of the window | P1 936, P3 968, P4 1206, P5 572, P6 964 |
| M10 | memo: the other window marked placed | P1 1166, P4 1206, P5 1196, P6 1196 |
| M11 | memo: no window ending at the last value | P1 809, P3 470, P4 500, P5 642, P6 819 |
| M12 | memo: the first choice found kept | P1 517, P3 600, P5 399, P6 545 |
| M13 | table: a value never skipped | P1 510, P3 600, P5 385, P6 539 |
| M14 | table: the next window may share the last value | P1 754, P6 757 |
| M15 | table: a window of the second length never started | P1 1176, P4 1206, P5 1206, P6 1206 |

P1 and P6 kill all fifteen. P3 and P5 each kill ten, P4 eight, and P2
four. P2 sees only the edits that treat the two lengths differently: ★
keeping only the window just left (M2) or measuring with the wrong
length (M3), and pairs never trying one of the windows at one end (M5,
M6). P3 misses the edits that go as wrong on the reversed array as on
the array itself, such as windows that touch counted as overlapping
(M4). P4 sees the edits whose answer does not rise with every value,
such as a window that loses values or a pair that is no longer
two windows. P5 misses the edits that only pick a lesser pair (M2, M5,
M6, M7), and the edits that let two windows share a value (M14), which
stays within its upper bound. The checks draw random numbers for every
case whatever the answers, so every mutant sees the same cases and
their counts can be compared.

Fifteen other edits were tried and set aside. Three change no answer
and are equivalent: memo never skipping the last value (with a window
still wanted, nothing fits after it anyway), and table counting windows
that do not fit as 0 or adding -1 for them. Those two count a lone
window as a pair, and with every value at least 0 a lone window never
beats the best pair: it lies inside a window of both lengths
together, which splits into two that do not overlap. The other twelve were
killed too, beyond three per arm. Three fail exactly alike, `P1 144,
P2 311, P3 311, P6 151`, with the first length only ever on the left,
in ★, pairs and sides. Eight fail as a kept mutant does: ★ with no pair
ending at the last value as M11; sides never keeping the first window's
sum as M1; sides always leaving a value between the windows as M4;
pairs allowing an overlap of one value as M14; pairs keeping the last
pair as M12; memo never skipping a value as M13; memo looking up the
memo for both windows wanted as M10; and table never starting a window
at index 0 as M15. ★ dropping the prefix sums for the bare values fails
on its own.

## Verification

Every arm prints the same output as `max_two.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. The differential prints its line under all three. `karac run` and
a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reported one thing: the memo
arm's two recursive calls passed the memo to a `mut ref` parameter
without the call-site `mut` (E0218). It came with a machine-applicable
replacement, `karac fix` wrote `mut memo` at both, and every file then
checks clean. The release build is kara `6697158faf`, with runtime
archives rebuilt at that commit. Under `karac __mir-run` the arms take
0.2 s (★) to 2.9 s (pairs). No correctness gap turned up. The bench
below found a speed one, filed on kara `B-2026-10-31-38`.

## Benchmarks

The bench builds 1,000 random arrays of 1,000 values (LeetCode's
largest), with values from 0 to 1,000 and random lengths, once in all
five languages, then answers each array 200 times with the ★ arm,
folding the answers into a sum and a checksum. Every call allocates its
prefix sums: a `Vec` in Kāra and Rust, a slice in Go, a list in Python
and a `calloc`'d array in C. Every implementation prints `1000 arrays
of 1000 values, 200 rounds: sum 76148312200, checksum 110075006`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.181 to 0.253 s | 0.192 s |
| Rust (`rustc -O`) | 0.194 to 0.233 s | 0.215 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.231 to 0.325 s | 0.238 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.643 to 0.712 s | 0.647 s |
| Kāra (`karac build`) | 0.619 to 0.661 s | 0.650 s |
| Go | 0.795 to 0.907 s | 0.830 s |
| Python | 27.9 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(its user time stays below its real time) and runs as fast as the
sequential one.

v2 took 2.72 times Rust's median time under overflow checks and 3.37
times C's. With no rounds, building the arrays takes 11 ms in Kāra and
in Rust, so the gap is in the calls. Callgrind at 10 rounds counts 357
million instructions for Kāra against Rust's 259 million, so most of the
gap is cycles, not instructions. The prefix loop shows why. Rust keeps
the running sum in a register:
`add (%rbx,%rcx,8),%rax; jo; mov %rax,0x8(%r14,%rcx,8)`. Kāra reloads
`prefix[i]`, the word the previous trip stored, so every trip waits on
store-to-load forwarding. It also reloads `nums`' buffer pointer from
its header and checks two bounds. That is kara `B-2026-10-31-38`, first
measured on Apple silicon for kata 64, and the row now carries this
x86 measurement.
