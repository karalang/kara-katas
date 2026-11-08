# 1073. Adding Two Negabinary Numbers

Given two numbers `arr1` and `arr2` in base -2, return the result of
adding them together. Each number is given as an array of 0s and 1s, from
most significant bit to least significant bit: `arr = [1,1,0,1]`
represents `(-2)^3 + (-2)^2 + (-2)^0 = -3`. A number in array format is
guaranteed to have no leading zeros: either `arr == [0]` or `arr[0] == 1`.
Return the result in the same format: an array of 0s and 1s with no
leading zeros.

```
arr1 = [1,1,1,1,1], arr2 = [1,0,1]  ->  [1,0,0,0,0]
arr1 = [0],         arr2 = [0]      ->  [0]
arr1 = [0],         arr2 = [1]      ->  [1]
```

**Constraints:** `1 <= arr1.length, arr2.length <= 1000`; every digit is 0
or 1; neither number has a leading zero.

Two at one place is -1 at the next, since `2 * (-2)^k = -(-2)^(k+1)`. So
the digits add from the low end like binary, except that the carry is
the negative of binary's: a place's sum `s`, from -1 to 3, writes `s & 1`
and carries `-(s >> 1)`, which is -1, 0 or 1.

The arms take the two numbers as `Vec[i64]` and return the sum the same
way.

## Approaches

| file | mechanism |
|---|---|
| `negabinary.kara` ★ | the digits added from the low end with two indices counting down past zero, `s & 1` written and `-(s >> 1)` carried; the leading zeros popped and the digits reversed. O(n1 + n2) |
| `negabinary_table.kara` | each place's sum looked up in a `match` of the digit it writes and the carry it passes (`-1 => (1, 1)`, `2 => (0, -1)`, ..), the place counted up from the low end; `digits.iter().rev().collect()`. O(n1 + n2) |
| `negabinary_normalize.kara` | the two numbers added place by place with no carry, then the places put right from the low end: a 2 or 3 gives up 2 and takes 1 from the next place, a -1 takes 2 and gives 1 to it. O(n1 + n2) |
| `negabinary_recursive.kara` | recursion on the low digits: the lowest digit of the sum, then the sum of what is left with the new carry, written into a `mut ref Vec[i64]`. O(n1 + n2), a call a digit |
| `negabinary_pairs.kara` | two digits at a time in base 4: a pair is worth `lo - 2 * hi`, from -2 to 1, and a sum of pairs and a carry `t` writes the pair worth `t - 4 * c` with `c = (t + 2).div_euclid(4)`. O(n1 + n2) |
| `negabinary_solution.kara` | LeetCode's Rust template (`struct Solution;`, `Vec<i32>`, `i32` indices from `len() as i32 - 1`, `arr1[i as usize]`, `\|\|` and `&&`, `*ans.last().unwrap()`, `Vec::new()`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 15 lines: the sums for LeetCode's three examples
and six more; how many of 3000 random pairs up to 12 digits and of 300 up
to 1000 digits sum to zero, the digits of the sums in all and a checksum;
and the sums of 1000 ones with itself and with 1, of 1010.. with 999
ones, and of 1 with 1000 ones. `negabinary.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the two numbers' values as integers (`v * -2 + d` digit by
digit), added, and the sum written back in base -2 by taking the
remainder that is 0 or 1 (`rem_euclid(2)`) and dividing the rest by -2
until nothing is left. It checks 2000 problems of three numbers each,
1000 up to 6 digits and 1000 up to 24; one time in four the second is the
first's negation, so the sum is 0. Every random choice is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the sum is the statement read literally |
| P2 | the two numbers swapped give the same sum |
| P3 | `a` plus 0 is `a` |
| P4 | `(a + b) + c` is `a + (b + c)` |
| P5 | `a` plus its negation is 0, the negation being `a` plus `a` moved up a place (`a * -2`) |
| P6 | each arm agrees with at least three of the other five |

The differential prints `2000 problems: checksum 19577956, 72000 checks
over 6 arms: 0 failures` under every lane in Verification; a Python
reading of the same 2000 problems gives the same checksum. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Fifteen are kept, two or three to
each arm; every kept edit fails the same way under both backends, none
by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the carry with its sign wrong (`s >> 1`) | P1 1581, P5 1898, P6 1581 |
| M2 | ★: the digit as `s % 2`, so a sum of -1 writes -1 | P1 468, P4 1068, P6 468 |
| M3 | ★: a zero sum trimmed to nothing | P1 537, P3 102, P5 2000, P6 537 |
| M4 | table: 2 carries 1 | P1 1581, P4 1010, P5 1898, P6 1581 |
| M5 | table: 3 carries nothing | P1 79, P4 277, P6 79 |
| M6 | normalize: a -1 never put right | P1 468, P4 452, P6 468 |
| M7 | normalize: a 3 left as 0 | P1 79, P4 275, P6 79 |
| M8 | recursive: the carry by truncating division (`-(s / 2)`) | P1 468, P4 821, P6 468 |
| M9 | recursive: the trim looks at the low digit | P1 786, P3 850, P4 765, P6 786 |
| M10 | recursive: the first carry 1 | P1 2000, P3 2000, P5 2000, P6 2000 |
| M11 | pairs: the carry by truncating division (`(t + 2) / 4`) | P1 901, P4 915, P5 1631, P6 901 |
| M12 | pairs: a pair worth -2 written as 1 | P1 1040, P3 1189, P4 1245, P5 1189, P6 1040 |
| M13 | solution: every other digit of `arr1` | P1 1794, P2 1909, P3 1794, P4 1425, P5 1794, P6 1794 |
| M14 | solution: a leading zero kept on a sum of one digit | P1 527, P5 1898, P6 527 |
| M15 | solution: `arr2`'s last digit dropped | P1 1909, P2 1953, P4 1776, P6 1909 |

P1 and P6 kill all fifteen, P4 eleven, P5 eight, P3 five and P2 two. P2
sees only the edits that treat the two numbers unequally (M13 and M15).
P4 misses the edits whose error does not depend on the order of the
additions: a carry of the wrong sign, a trim to nothing, a first carry of
1 and a kept leading zero (M1, M3, M10, M14). The two edits that mishandle a
place's 3 (M5, M7) fail nearly the same checks and are told apart only by
P4, 277 against 275.

Of the fifteen not kept, three never finish: a sum of -1 carrying -1 in
the table arm, and a -1 taking 1 from the next place in the normalize
arm, each carry another -1 forever and stop at the 120 s limit under the
interpreter, and the solution's carry taken from the low bit grows its
digits until the interpreter is killed for memory; under LLVM all three
exhaust memory (`panic: out of memory`). Four fail as a
kept edit or as each other: the ★ arm's last carry dropped and the
table's (alike), the digits left low first in the ★ and solution arms
(alike), `b` read from its high end in the table and normalize arms
(alike), and the normalize arm's 2 giving 1 to the next place as M1. The
other five fail in ways of their own and are left out to keep two or
three to each arm: the recursive arm's top digit of `b` dropped and `a`
counted twice, and the pairs arm's high digit of `b` counted up, pairs
that overlap, and a pair written high digit first.

## Verification

Every arm prints the same output as `negabinary.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file. Under `karac __mir-run` the arms take 0.6 s to 1.5 s and the
differential 5.4 s.

Every file went through `karac fix`, which changed nothing in the arms
written in Kāra. The Rust arm reaches a clean check in two rounds: the
syntax (`struct Solution {}`, `Vec[..]` for `Vec<..>`, `Vec.new` and
`Solution.` for the `::` paths, `or` and `and` for `||` and `&&`), then
`carry: i32`. The template keeps its carry as `let mut carry = 0;`,
copies it into the place's sum (`let mut x = carry;`), adds `i32` digits
to that and pushes `x & 1` onto a `Vec[i32]`. Only operators use the
literal, so it keeps its default `i64` (design.md §8 Literals) and the
push is refused. The kata found one gap, fixed in kara `a0bb430292` with
`tests/kata_1073_check_gaps.rs`:

- **No fix for a copy of a defaulted literal binding.** The refusal
  offers the binding's annotation (B-2026-11-08-20) when a literal `let`
  is named in the refused expression, but `x` is a copy of `carry`, so
  check gave only "write an explicit 'as i32'" and `karac fix` had
  nothing to apply. A copy is now traced to its literal: the refusal
  names `carry` and the fix writes `carry: i32`. Kara B-2026-11-08-62.

## Benchmarks

The bench builds 2000 pairs of numbers up to 1000 digits once, in all
five languages, the way the arms' random sets do, and adds each pair 20
times with the ★ arm. Every implementation prints `40000 calls: 26548220
digits, checksum 938969863`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with kara `d95eccd728`
on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.076 to 0.121 s | 0.079 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.078 to 0.102 s | 0.080 s |
| Rust (`rustc -O`) | 0.079 to 0.109 s | 0.081 s |
| Kāra (`karac build`) | 0.080 to 0.092 s | 0.082 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.083 to 0.106 s | 0.085 s |
| Go | 0.157 to 0.185 s | 0.168 s |
| Python | 3.5 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.073 s) is below its real time.

Kāra, C and both Rust builds run within 7% of each other's medians,
inside the spread of their runs. Each call walks both numbers once from
the low end and pushes a digit a place onto a growing array, which all
four do the same way; the checked additions cost Kāra and checked Rust
nothing measurable here. Go takes 2.1x; it is not broken down here.
