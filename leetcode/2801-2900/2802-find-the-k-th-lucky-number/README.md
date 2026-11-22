# 2802. Find The K-th Lucky Number

We know that `4` and `7` are **lucky** digits. Also, a number is called
**lucky** if it contains **only** lucky digits.

You are given an integer `k`, return *the* `k`*-th lucky number
represented as a **string**.

```
k = 4      ->  "47"
k = 10     ->  "477"
k = 1000   ->  "777747447"
```

**Constraints:** `1 <= k <= 10^9`.

## Approaches

There are 2^L lucky numbers of L digits, and in increasing order they
run through the L-digit strings of 4 and 7 as binary counting runs
through 0 and 1; so the k-th is k + 1 in binary below its leading bit,
0 written 4 and 1 written 7.

| file | mechanism |
|---|---|
| `lucky.kara` ★ | k + 1's leading bit found by doubling, then each bit below it read from the top with `&`, 0 a 4 and 1 a 7, into a `String` |
| `lucky_blocks.kara` | by blocks: the lengths skipped while k is past all 2^L of them, then the place within the block written in L binary digits, last first, into a `Vec[String]` turned round and joined |
| `lucky_heap.kara` | as a heap: the lucky numbers in order are a complete binary tree in level order, so the k-th is the (k - 1) / 2-th with a 4 after when k is odd and a 7 when it is even, by recursion |
| `lucky_bytes.kara` | on bytes from the end: k + 1 halved until 1 is left, each remainder a byte pushed, the bytes turned round and made a `String` by `String.from_utf8` |
| `lucky_solution.kara` | a Rust solution as LeetCode's Rust users write it, `format!("{:b}", k + 1)` with its leading 1 skipped by `chars().skip(1)` and each bit mapped by a `match` on `char`s, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples; the first;
k = 10^9, LeetCode's largest; the last lucky number of 29 digits; 3000
random k from 1 to 1000; and 50 up to 10^9, the last two with the sum of
the lengths and a checksum of the digits. `lucky.py` mirrors the ★ arm
and its output is byte-identical.

```
47
477
777747447
4
77477744774747744747444444447
77777777777777777777777777777
3000 k up to 1000: lengths sum to 23936, checksum 461433801
50 k up to 10^9: lengths sum to 1404, checksum 789304676
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the positive integers in turn, each written out and kept when
its digits are all 4 and 7, until the k-th is kept; no bits and no
blocks. It draws 2000 random k from 1 to 14, then 50 up to 10^9, all
before any arm answers; the literal reading is asked only of the first
2000.

| | property |
|---|---|
| P1 | k up to 14, the answer is the literal reading's |
| P2 | only 4 and 7, and L digits with 2^L - 1 <= k < 2^(L + 1) - 1 |
| P3 | the (k + 1)-th: longer, or as long and greater |
| P4 | the (2k + 1)-th and the (2k + 2)-th: the k-th with a 4 and a 7 after |
| P5 | 4 and 7 swapped: the answer at the same place from its block's end |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 196601601, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: k + 1's leading bit missed when k + 1 is a power of 2 | P1 450, P2 450, P3 413, P4 450, P5 701, P6 450 |
| M2 | ★: a 0 bit written 7 and a 1 bit 4 | P1 2000, P3 1637, P4 2050, P6 2050 |
| M3 | blocks: a k at the end of its block left in it | P1 288, P2 288, P3 413, P4 450, P5 406, P6 288 |
| M4 | blocks: the digits never turned round | P1 874, P3 588, P4 2050, P6 924 |
| M5 | heap: the last digit 4 for even k | P1 2000, P3 1637, P4 2050, P6 2050 |
| M6 | heap: the parent taken as k / 2 | P1 1550, P2 1600, P3 1600, P4 2050, P5 2050, P6 1600 |
| M7 | bytes: the leading 1 written as a digit too | P1 2000, P2 2050, P5 2050, P6 2050 |
| M8 | bytes: an even remainder written 7 | P1 2000, P3 1637, P4 2050, P6 2050 |
| M9 | solution: two bits skipped | P1 2000, P2 2050, P3 450, P5 1888, P6 2050 |
| M10 | solution: the 1 bit mapped to 4 | P1 2000, P3 1637, P4 2050, P6 2050 |

## Benchmarks

The bench draws 200000 k up to 10^9, LeetCode's largest, all of them
first, then answers each 10 times by the ★ arm in all five languages,
each answer a fresh string; the C answer is a heap buffer, freed after
it is read, as the other languages allocate theirs. Every
implementation prints `200000 k up to 10^9, 10 rounds: lengths sum to
55340430, checksum 457906837`.

BENCHTAB

## Verification

All five arms print the same output as `lucky.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms and the harness checked clean as first written.

LeetCode's Rust template took 3 `karac fix` edits, the wrapper
included: `struct Solution {}` added; `format!("{:b}", k as i64 + 1)`
became the f-string `f"{k as i64 + 1:b}"`; and `Solution::` became
`Solution.`. The chain `.chars().skip(1).map(|c| match c { '0' => '4',
_ => '7' }).collect()` into a `String` is Kāra as written.
