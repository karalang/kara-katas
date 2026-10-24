# 989. Add to Array-Form of Integer

The **array-form** of an integer `num` is an array representing its
digits in left to right order.

- For example, for `num = 1321`, the array form is `[1,3,2,1]`.

Given `num`, the **array-form** of an integer, and an integer `k`,
return the **array-form** of the integer `num + k`.

```
num = [1,2,0,0], k = 34   ->  [1,2,3,4]
num = [2,7,4], k = 181    ->  [4,5,5]
num = [2,1,5], k = 806    ->  [1,0,2,1]
```

**Constraints:** `1 <= num.length <= 10^4`; `0 <= num[i] <= 9`; `num`
does not contain any leading zeros except for the zero itself;
`1 <= k <= 10^4`.

## Approaches

`num` can be 10,000 digits long, far past any integer type, so every
arm adds digit by digit; `k` is small enough to hold in an `i64`.

| file | mechanism |
|---|---|
| `add_to_array_form.kara` ★ | k as the carry: k is added to the last digit as if it were a carry, each place keeps the last digit of the carry and passes the rest left, and what is left when the digits run out gives the leading digits. O(n + log k) |
| `add_to_array_form_digits.kara` | k as digits too: k is turned into its own digit list, and the two lists are added the schoolbook way from their last digits, with a carry. O(n + log k) |
| `add_to_array_form_deque.kara` | in place, in a deque: the digits are copied into a `VecDeque`, k is added into it from the last place, and whatever is left once the digits run out goes on the front a digit at a time. O(n + log k) |
| `add_to_array_form_recursive.kara` | recursive: the sum up to a digit is the sum up to the digit before, with the carry out of this place, followed by this place's digit; the recursion is n deep. O(n + log k) |
| `add_to_array_form_limbs.kara` | base 10^9 limbs: the digits are packed nine at a time into limbs, k is added to the lowest with the carry passed up, and the limbs are unpacked, every one but the top as exactly nine digits. O(n + log k) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 16 lines. The first ten are LeetCode's three
examples and seven more: `[0] + 1`; a carry out of every digit
(`[9, 9, 9] + 1`); a k longer than num, from `[0]`, `[5]` and `[1]`; a
carry that stops inside num (`[9, 9, 9, 9, 9] + 10000`); and a carry
into the last of twelve digits. Then two numbers of LeetCode's largest
size, 10,000 digits: all nines plus 1, which carries through all of
them, and the digits 1 to 0 repeated plus 10,000. Then totals over
random sums: 300 of up to 6 digits, 3,000 of up to 100, 300 of up to
30 that are mostly nines, so carries run long, and three of 10,000
digits, each k drawn from 1 to 10,000. `add_to_array_form.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the integer whose digits num lists is built in an `i64`, k
is added, and the sum is written out as text whose characters are the
answer's digits. It checks 3,200 random sums: 3,000 of up to 12 digits,
which fit, against the statement, and 200 of up to 500 digits, with few
nines and mostly nines in turn, against the other properties.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 sums |
| P2 | adding k and then another k2 is adding k2 and then k |
| P3 | with a digit d after num, the answer ends in (d + k) % 10 and the rest is num plus (d + k) / 10 |
| P4 | taking k away from the answer, the schoolbook way, gives back num |
| P5 | the answer's digits are 0 to 9 with no leading zero, and it is as long as the longer of num and k or one digit longer |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 sums of 66609 digits: 68580 digits out, checksum
422518634, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (7.0 s) and `karac __mir-llvm-run`, and the same
under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-five edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the loop ends with the digits | P1 1213, P5 1074, P6 1217 |
| M2 | ★: the answer never reversed | P1 2983, P2 3190, P3 3198, P4 3183, P5 322, P6 3183 |
| M3 | ★: the whole carry written as a digit | P1 2999, P2 3196, P3 3198, P4 3199, P5 3199, P6 3199 |
| M4 | digits: k's digits never reversed | P1 2931, P3 3188, P4 3130, P5 51, P6 3130 |
| M5 | digits: the last carry dropped | P1 499, P2 55, P3 1, P5 358, P6 501 |
| M6 | digits: the carry never passed on | P1 2801, P3 1425, P4 2977, P5 27, P6 2990 |
| M7 | deque: what is left of k put at the back | P1 1208, P2 1263, P3 934, P4 1212, P5 413, P6 1212 |
| M8 | deque: what is left of k put in as one digit | P1 512, P2 5, P4 490, P5 513, P6 513 |
| M9 | deque: the walk stops a digit short | P1 1436, P2 946, P4 1440, P5 16, P6 1440 |
| M10 | recursive: the carry never passed on | P1 2999, P3 2872, P4 2902, P5 742, P6 3199 |
| M11 | recursive: it stops when the carry runs out | P1 2777, P2 232, P3 2, P4 1760, P5 2834, P6 2977 |
| M12 | recursive: the last digit skipped | P1 2981, P2 3199, P3 2867, P4 3181, P5 1756, P6 3181 |
| M13 | limbs: eight digits packed a limb | P1 1015, P2 22, P3 1395, P4 1212, P5 193, P6 1212 |
| M14 | limbs: a lower limb padded to eight digits | P1 128, P2 3, P3 294, P4 265, P5 191, P6 265 |
| M15 | limbs: the top limb padded too | P1 2727, P3 3200, P5 2909, P6 2909 |

P1, P5 and P6 kill all fifteen, P3 and P4 twelve each, and P2 ten.
P4 is blind to an answer that loses its carry out: M1 and M5 give
`[0, 0, 0]` for `[9, 9, 9] + 1`, and taking 1 away borrows through
every place back to `[9, 9, 9]`. It is blind to M15's leading zeros
too, which subtraction drops. P5 sees those three, by the length and
the leading zero. P2 compares a mutant only with itself, so it misses
the five whose wrong sum still does not care which k goes first: M1
adds modulo 10 to the power of num's length, M4 adds k's digits
reversed, M6 adds digit by digit with no carry, M10 adds k into the
last digit alone, modulo 10, and M15's leading zeros vanish when its
answer is packed into limbs again. P3 also compares a mutant with
itself, on num and on num with a digit after it, and misses M8 and M9,
which go wrong the same way on both (inferred, not traced).

Ten other edits were tried and set aside, all killed. Three failed
exactly the same checks as a kept one: digits never reversing the
answer and recursive writing a digit before the rest, as M2, and
recursive stopping when the digits run out, as M1. Seven were sound
but beyond three an arm: ★ ending the loop when the carry runs out
(which fails exactly M11's checks) and skipping the last digit (M12's);
digits dropping k's first digit; deque never taking the carry off a
digit and stopping when the carry is under 10; limbs stopping the
carry at the top limb and unpacking the lowest limb first. None
survived and none crashed.

## Verification

Every arm prints the same output as `add_to_array_form.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `395f71ae05`, the runtime
archives rebuilt at `d867340a02`, whose runtime sources are the same.
Under `karac __mir-run` the arms take 0.7 s (★) to 2.1 s (deque, which
copies the digits into a `VecDeque` and back), and the differential
7.0 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. The program draws 20
random numbers of LeetCode's largest size, 10,000 digits, once. In each
of 1,000 rounds it adds a random k from 1 to 10,000 to every number,
each round starting from a different one, and folds each answer's last
six digits into a checksum. Every implementation prints `1000 rounds
over 20 numbers of 10000 digits: 200000000 digits out, checksum
644182104`. Each call walks all 10,000 digits, pushes each onto a fresh
list and reverses it. C grows its list in a doubling array, as `Vec`
does.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `395f71ae05`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.616 to 0.662 s | 0.648 s |
| Rust (`rustc -O`) | 0.594 to 0.751 s | 0.630 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.591 to 0.657 s | 0.634 s |
| Go | 2.598 to 2.956 s | 2.829 s |
| Python | 17.8 s | |
| Kāra (`karac build --mir`) | 0.588 to 0.673 s | 0.626 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 28 times
Kāra's.

v2 took 0.99 times Rust's median time under overflow checks and 0.97
times C's. Under valgrind's cachegrind v2 ran 7,460 million
instructions and 1,209 million branches with 0.45 million
mispredicted, Rust with overflow checks 7,876 million, 1,036 million
and 0.33 million, and C 6,354 million, 709 million and 0.29 million.
Almost no branch is mispredicted in any of them: the loop's only
data-dependent test is whether a carry is left, and after the last few
digits it never is. Every program grows each answer from an empty list,
but where the others free an answer as soon as it is folded, Go leaves
it and every outgrown slice behind it to the garbage collector, about
160 KB a call; that fits Go taking four times as long (inferred, not
traced).
