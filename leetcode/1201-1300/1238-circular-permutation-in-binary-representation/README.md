# 1238. Circular Permutation in Binary Representation

Given 2 integers `n` and `start`. Your task is return **any** permutation
`p` of `(0, 1, 2, ..., 2^n - 1)` such that:

- `p[0] = start`
- `p[i]` and `p[i + 1]` differ by only one bit in their binary
  representation.
- `p[0]` and `p[2^n - 1]` must also differ by only one bit in their
  binary representation.

```
n = 2, start = 3  ->  [3,2,0,1]           (11,10,00,01); [3,1,0,2] is another
n = 3, start = 2  ->  [2,6,7,5,4,0,1,3]   (010,110,111,101,100,000,001,011)
```

**Constraints:** `1 <= n <= 16`; `0 <= start < 2^n`.

## Approaches

| file | mechanism |
|---|---|
| `circular_permutation_in_binary_representation.kara` ★ | the reflected Gray code moved to `start`: the `i`th code `i ^ (i >> 1)` differs from the next in one bit, and the last from the first, and an XOR with `start` keeps every difference while sending code 0 to `start`. O(2^n) |
| `circular_permutation_in_binary_representation_reflect.kara` | the Gray code built by reflection, a bit at a time (the list so far, then the same list backwards with the new bit set), then the cycle turned to begin at `start` by slicing at its `position`. O(2^n) |
| `circular_permutation_in_binary_representation_greedy.kara` | a walk on the hypercube from `start`, each step flipping the lowest bit that reaches a value not yet visited: from 0 that walk is the reflected Gray code, and XOR with `start` maps it onto the walk from `start`, so it never gets stuck. O(n 2^n) |
| `circular_permutation_in_binary_representation_halves.kara` | the Gray code by recursion on `n` (the code for `n - 1` bits, then the same code backwards with the top bit set), every value then XORed with `start`. O(2^n) |
| `circular_permutation_in_binary_representation_rotate.kara` | a Rust solution as LeetCode's Rust users write it (the code reflected with `res.push(res[j] \| 1 << i)` over `(0..res.len()).rev()`, then turned with `res.iter().position(\|&x\| x == start)` and `rotate_left`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Any permutation meeting the three conditions is right, and the arms
give two different ones: the ★, greedy and halves arms `start ^ i ^ (i >>
1)`, and the reflect and rotate arms the Gray code turned to begin at
`start`. So the harness checks each answer against the conditions and
prints the verdict, not the permutation. Every arm prints the same 4
lines: LeetCode's two examples, each `a cycle: true`; for 1000 random
cases with `n` from 1 to 12, `1000 cycles, 678836 values`; and for `n =
16` from 0, from 40000 and from 65535, `3 of 3 cycles of 65536`.
`circular_permutation_in_binary_representation.py` mirrors the ★ arm,
and its output is byte-identical. Every arm gives the same output under
`karac run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the four Kāra arms check clean as written. The rotate arm
takes one round of 5 fixes (among them `Vec<i32>` to `Vec[i32]`, `vec![0]`
to `[0]`, `|&x|` to `|x|`) and checks clean.

## Gaps

LeetCode's best-known Rust solution, `(0..1 << n).map(|i| start ^ i ^ (i
>> 1)).collect()`, is held out of the kata. After `karac fix` writes
`Vec<i32>` as `Vec[i32]`, it is refused with `trait bound `C:
FromIterator[i64]` is not satisfied; `Vec[i32]` implements
`FromIterator[i32]`` and no fix, three rounds running. The refusal
follows design.md §8: beside `start`, an `i32` that widens into the
default, the range's literals stay `i64`, where Rust infers the range's
type from `start ^ i`. But the message names neither the range nor the
literal that kept the default, and `karac fix` offers no suffix, so the
Mend loop has no step (B-2026-11-19-33). Writing the range's first bound
`0i32` makes it check, and is the fix asked for.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: the answer sorted is every value from 0 to `2^n - 1`, it
begins at `start`, and each value and the next, and the last and the
first, differ in exactly one bit, counted bit by bit. 2000 cases: the
first 40 with `n` from 1 to 4, the rest with `n` from 1 to 12, each with
a random `start`.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | `2^n` values |
| P3 | `start` first |
| P4 | each step, and the wrap from last to first, flips one bit |
| P5 | no value twice |
| P6 | each bit flipped an even number of times around the cycle, as any closed walk must |

All 60,000 checks pass on every arm: `2000 cases: checksum 711530905,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python, with the same
cases and the ★ arm's answer checked against the conditions, gives the
same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the code shifted two places, not one | P1 1821, P4 1821, P6 1821 |
| S2 | ★: the last code left out | P1 2000, P2 2000, P4 2000, P5 2000, P6 2000 |
| F1 | reflect: the copy not reversed | P1 1821, P4 1821, P6 1821 |
| F2 | reflect: the cycle not turned to `start` | P1 1807, P3 1807 |
| G1 | greedy: the top bit taken when every lower one is used | NOT CAUGHT |
| G2 | greedy: a visited value not marked | P1 1646, P5 1646 |
| H1 | halves: the new bit one place too high | P1 2000, P4 2000, P5 2000, P6 2000 |
| H2 | halves: the second half not reversed | P1 1821, P4 1821, P6 1821 |
| R1 | rotate: turned the wrong way | P1 1645, P3 1645 |
| R2 | rotate: the copy not reversed | P1 1821, P4 1821, P6 1821 |

Nine of the ten are caught, each by P1, the statement read literally.
The tenth, G1, the greedy walk taking the top bit without testing it
once every lower one leads to a value already visited, is an equivalent
mutant: the walk never gets stuck, so when every lower bit is used the
top one always reaches a new value. Four mutations make a cycle that is
not a Gray code, a step that flips more than one bit, in the 1821 cases
with `n` of 2 or more: the ★ arm's code shifted two places (S1), and the
reflected copy not reversed in the reflect, halves and rotate arms (F1,
H2, R2). P4, each step flipping one bit, catches those, and so does P6,
each bit flipped an even number of times around the cycle. Two fail
every case: the ★ arm that leaves out the last code (S2), which P2, `2^n`
values, catches, and the halves arm's new bit one place too high (H1),
whose values run past `2^n - 1`. The two arms that turn the Gray code to
begin at `start` turned it wrongly, the reflect arm not at all (F2) and
the rotate arm the wrong way (R1); only P3, `start` first, catches them
besides the statement. And the greedy walk with a value not marked as
visited (G2) comes back to one, which P5, no value twice, catches.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm's answer for n = 16 from 64 starts, each checked as a cycle (every
value once, one bit between neighbours and across the wrap); prints the
cycles found and a checksum of their middle values. Every program prints
`n = 16, 64 starts: 64 cycles, checksum 288382710`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.009 to 0.014 s | 0.010 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.009 to 0.015 s | 0.009 s |
| Rust (`rustc -O`) | 0.009 to 0.014 s | 0.009 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.009 to 0.014 s | 0.010 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.008 to 0.010 s | 0.008 s |
| C (`clang -O3`) | 0.008 to 0.016 s | 0.009 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.007 to 0.014 s | 0.007 s |
| Go | 0.031 to 0.040 s | 0.033 s |
| Python | 1.136 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 10% ahead of Rust with overflow checks on (0.009 s
against 0.010 s), and the two ranges overlap. C runs level with Kāra
(0.009 s against 0.009 s); Go takes about 3.7x Kāra's time. Python takes
about 126x Kāra's time. No profile was taken.
