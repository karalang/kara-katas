# 1567. Maximum Length of Subarray With Positive Product

Given an array of integers `nums`, find the maximum length of a subarray
where the product of all its elements is positive. A subarray is a
consecutive sequence of zero or more values taken out of the array.
Return the maximum length of a subarray with positive product.

```
nums = [1,-2,-3,4]       ->  4
nums = [0,1,-2,-3,-4]    ->  3
nums = [-1,-2,-3,0,1]    ->  2
```

**Constraints:** `1 <= nums.length <= 10^5`; `-10^9 <= nums[i] <= 10^9`.

## Approaches

A product is positive when it holds no zero and an even count of
negatives, so only the signs matter and no product is ever formed.

| file | mechanism |
|---|---|
| `positive.kara` ★ | the longest run ending here with a positive product and the longest with a negative one: a positive value lengthens both (a negative run only if there is one), a negative one swaps them, a zero ends both. O(n) |
| `positive_segments.kara` | the array cut at its zeros by `split`; a piece with an even count of negatives is positive whole, and with an odd count the longest positive part drops everything up to its first negative (`position`) or everything from its last (`rposition`). O(n) |
| `positive_parity.kara` | the parity of the prefix's count of negatives: a subarray is positive when its two ends see the same parity with no zero between, so each index looks back to the first place since the last zero its parity was seen, kept in an `Array[Option[i64], 2]`. O(n) |
| `positive_solution.kara` | LeetCode's Rust template (`get_max_len(nums: Vec<i32>) -> i32`, the ★ arm over a tuple of three counters), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's three examples, then
`[-1]`, `[0]`, `[5]`, `[-1, 2]`, a longer array cut by a zero, and four
values of `-10^9` (whose product would overflow); then the sum of the
answers and a checksum for 3000 random arrays of up to 10 values from -5
to 5, 300 of up to 1000 and 30 of up to 100000 values up to `10^9`, a
value 0 one time in 5, 50 and 1000, and otherwise negative one time in
three. `positive.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every subarray, its sign worked out from its count of zeros
and of negatives, the longest positive one kept. It checks 3000 arrays of
1 to 10 values from -3 to 3, every random choice drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is at most the length, and at least 1 when a value is positive |
| P3 | the array reversed leaves the answer |
| P4 | every value replaced by its sign leaves the answer |
| P5 | a 0 and then the array again put after it leaves the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 975959696, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a positive value starts a negative run where there was none | P1 579, P3 724, P6 579 |
| M2 | ★: a negative value's new negative run one short | P1 1707, P3 951, P6 1707 |
| M3 | ★: a zero leaves the positive run standing | P1 592, P5 2030, P6 592 |
| M4 | segments: an odd piece never drops from its last negative | P1 374, P2 167, P3 788, P6 374 |
| M5 | segments: a piece positive whole only with no negative | P1 1097, P6 1097 |
| M6 | segments: the first negative kept when dropping up to it | P1 995, P3 847, P6 995 |
| M7 | parity: a zero restarts the even parity at the array's start | P1 1022, P3 1065, P5 2586, P6 1022 |
| M8 | parity: a zero keeps the parity it found | P1 307, P2 9, P3 512, P5 1233, P6 307 |
| M9 | template: the negative run taken from the new positive one | P1 1256, P2 459, P3 968, P6 1256 |
| M10 | template: the best negative run returned | P1 2862, P2 352, P6 2862 |

## Benchmarks

The bench builds 20 arrays of 200000 values once, each value 0 one time
in 5000 and otherwise of 1 to 1000, negative one time in three, and makes
20 passes, each flipping the sign of one value of every array and asking
it by the ★ arm, in all five languages. Every implementation prints
`20 passes over 20 arrays of 200000 values: lengths sum 7677310, checksum
564882199`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.392 s |
| C (`clang -O3`) | 0.417 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.426 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.428 s |
| Kāra (`karac build`) | 0.430 s |
| Go | 0.482 s |
| Python | 9.6 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.43 s and 0.45 s on one run).

Kāra is 1.00x Rust under overflow checks by median. Not traced. The loop
is a three-way branch on each value's sign with a data-dependent next
state, so no implementation vectorizes it, and every compiled row is
within 23% of the fastest.

## Verification

All four arms print the same output as `positive.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The ★ and segments arms were written in Kāra and checked as written. The
parity arm was first written with Rust's `[Option[i64]; 2]` for its
table; `karac fix` rewrote it to `Array[Option[i64], 2]` in one round.

The Rust template took five rounds of `karac fix`, 6 changed lines, then
1 added, then 2, 1 and 1 changed:

1. the `Vec<..>` types to `Vec[..]`, `let (mut positive, mut negative,
   mut best)` to `let mut (positive, negative, best)`, `for &x in &nums`
   to `for x in ref nums`, the wrapper's `|&x|` to `|x|`, and
   `Solution::` to `Solution.`;
2. `struct Solution {}` added;
3. `best`'s literal to `0i32`, and the wrapper's `as i64` dropped (an
   `i32` widens);
4. `positive`'s literal to `0i32`;
5. `negative`'s literal to `0i32`.

Rounds 3 to 5 each reported one error: once `best` is `i32`,
`best.max(positive)` needs `positive` to be one, and `positive = negative
+ 1` then needs `negative`, but each surfaces only after the round
before. The same three counters as separate `let`s take three rounds the
same way. Filed as B-2026-11-14-18. It checks and agrees with no hand
edit.
