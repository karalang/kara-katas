# 2859. Sum of Values at Indices With K Set Bits

You are given a **0-indexed** integer array `nums` and an integer `k`.

Return *an integer that denotes the **sum** of elements in* `nums`
*whose corresponding **indices** have **exactly*** `k` *set bits in
their binary representation.*

The **set bits** in an integer are the `1`'s present when it is
written in binary.

- For example, the binary representation of `21` is `10101`, which
  has `3` set bits.

```
nums = [5,10,1,5,2], k = 1  ->  13
nums = [4,3,2,1], k = 2     ->  1
```

**Constraints:** `1 <= nums.length <= 1000`; `1 <= nums[i] <= 10^5`;
`0 <= k <= 10`.

## Approaches

| file | mechanism |
|---|---|
| `bits.kara` ★ | every index's set bits counted by `count_ones`, and the values at the indices with exactly k of them summed, in one chain of `enumerate`, `filter`, `map` and `sum` |
| `bits_clear.kara` | the bits counted by hand: `i & (i - 1)` clears the lowest set bit, so the number of times it can be done before i is 0 is its count |
| `bits_table.kara` | a table of bit counts built up from the front: i has the bits of i / 2, and one more when it is odd |
| `bits_gosper.kara` | only the indices with k bits visited, in increasing order, by Gosper's hack: the lowest set bit c = i & -i, r = i + c carries the lowest run of ones up one place, and the ones it cleared, less one, come back at the bottom as ((r ^ i) >> 2) / c |
| `bits_solution.kara` | a Rust solution as LeetCode's Rust users write it: one chain, `enumerate()`, `filter(\|(i, _)\| i.count_ones() as i32 == k)`, `map(\|(_, &x)\| x)` and `sum()`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's two examples; 1000
values of 10^5, LeetCode's most, for every k from 0 to 10; then 3000
random arrays of 1 to 20 values up to 10 with k up to 5, and 300 of 1
to 1000 values up to 10^5 with k up to 10, as a total and a checksum.
`bits.py` mirrors the ★ arm and its output is byte-identical.

```
13 1
[100000, 1000000, 4500000, 12000000, 21000000, 25200000, 20800000, 11300000, 3600000, 500000, 0]
3000 short arrays: sums total 26967, checksum 121320036
300 long arrays: sums total 719786673, checksum 286882455
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: each index written out in binary as text by
`f"{i:b}"`, its `'1'` characters counted, and the values whose index
has k of them added. It draws 2000 random arrays of 1 to 40 values up
to 20 with k up to 6, then 50 of up to 1000 values up to 10^5 with k
up to 10, all before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | every value doubled: twice the answer |
| P3 | the answers for k from 0 to 10 add up to the whole array |
| P4 | the array padded with zeros to twice its length: the same answer |
| P5 | every value at an index without k set bits made 0: the same answer |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, sums total 138073898: checksum
429155705, 61500 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python reading of the same cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. A first draft of M7 crashed with a division by
zero before any property was asked, and was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: at least k bits taken, not exactly k | P1 1049, P3 2010, P5 1049, P6 1049 |
| M2 | ★: the bits of the value counted, not the index | P1 1431, P3 50, P5 1002, P6 1431 |
| M3 | clear: the count stopping at the last bit | P1 547, P5 274, P6 547 |
| M4 | clear: the last index never looked at | P1 278, P3 2050, P4 278, P6 278 |
| M5 | table: an odd index's own bit left out | P1 1341, P5 274, P6 1341 |
| M6 | table: the half taken from the wrong end | P1 1502, P3 987, P5 1256, P6 1502 |
| M7 | gosper: the next index's low bits shifted one place too few | P1 874, P3 1959, P5 775, P6 874 |
| M8 | gosper: the cleared ones brought back one place too high | P1 874, P3 1959, P5 775, P6 874 |
| M9 | solution: k bits or fewer | P1 1769, P3 2050, P5 1769, P6 1769 |
| M10 | solution: the index summed, not the value | P1 1338, P2 1067, P3 2044, P4 1371, P6 1338 |

## Benchmarks

The bench draws 2000 arrays of 1000 values up to 10^5, LeetCode's
most, with k up to 10, all of them first, then answers each 100 times
by the ★ arm in all five languages. C counts the bits with
`__builtin_popcountll`, Go with `bits.OnesCount`, Python with
`int.bit_count`. Every implementation prints `2000 arrays, 100 rounds:
sums total 897943354500, checksum 712464649`.

A caveat on the plain C and Rust rows: `bench.sh` builds Kāra at
x86-64-v3, which has the `popcnt` instruction, as it builds the
matched-ISA C and Rust twins, and Go's `bits.OnesCount` uses it when
the CPU has it; but `clang -O3` and `rustc -O` with no target CPU
build for plain x86-64 and count the bits in software, and `objdump`
finds no `popcnt` in either binary. Measured by hand on a loaded
machine, the plain C binary took 0.37 s and 0.12 s with `-mpopcnt`.
Compare Kāra with the matched-ISA rows.

BENCHTAB

## Verification

All five arms print the same output as `bits.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The harness, as first written, passed `full.clone()` for every k, and
`karac check` reported `redundant_clone`, the parameter only borrowing
it; `karac fix` passed `full`. The arms checked clean.

LeetCode's Rust template took 9 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; `Vec<..>`
became `Vec[..]`; `|(_, &x)|` and `|&x|` lost their `&`; `Solution::`
took `.`, and the wrapper's `as i64` went, an `i32` widening. `i.count_ones()
as i32 == k` was accepted as written.
