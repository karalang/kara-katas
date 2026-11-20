# 1720. Decode XORed Array

There is a **hidden** integer array `arr` that consists of `n`
non-negative integers.

It was encoded into another integer array `encoded` of length `n - 1`,
such that `encoded[i] = arr[i] XOR arr[i + 1]`. For example, if
`arr = [1,0,2,1]`, then `encoded = [1,2,3]`.

You are given the `encoded` array. You are also given an integer
`first`, that is the first element of `arr`, i.e. `arr[0]`.

Return *the original array* `arr`. It can be proved that the answer
exists and is unique.

```
encoded = [1,2,3], first = 1          ->  [1,0,2,1]
encoded = [6,2,7,3], first = 4        ->  [4,2,0,7,4]
```

**Constraints:** `2 <= n <= 10^4`; `encoded.length == n - 1`;
`0 <= encoded[i] <= 10^5`; `0 <= first <= 10^5`.

## Approaches

| file | mechanism |
|---|---|
| `decode.kara` ★ | XOR undoes itself, so `arr[i + 1]` is `arr[i] ^ encoded[i]`: from the first value each next one follows, pushed onto a vector of the right capacity. O(n) |
| `decode_scan.kara` | the values as an iterator: `once(first)` chained to a `scan` over the codes whose state is the last value, each code giving the next value as both the new state and the item. O(n) |
| `decode_prefix.kara` | XOR is associative, so `arr[i]` is `first` XORed with every code before it: the codes' running XOR written into a filled array one place to the right, then every place XORed with `first`. O(n) |
| `decode_solution.kara` | a Rust solution as LeetCode's Rust users write it, `std::iter::once(first).chain(encoded.iter().scan(first, \|acc, &e\| { *acc ^= e; Some(*acc) })).collect()`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's two examples, one code, two
codes of 0, and the largest values; then the values summed and a
checksum for 3000 random arrays of up to 12 codes up to 15, 300 of up to
1000 codes up to `10^5`, and 10 of up to `10^4` codes up to `10^5`.
`decode.py` mirrors the ★ arm and its output is byte-identical.

```
[1, 0, 2, 1]
[4, 2, 0, 7, 4]
[0, 5]
[7, 7, 7]
[100000, 0, 1, 100001]
3000 arrays of up to 12 codes up to 15: values sum to 167519, checksum 652475663
300 arrays of up to 1000 codes up to 100000: values sum to 9346361291, checksum 589450278
10 arrays of up to 10000 codes up to 100000: values sum to 2940997728, checksum 916239648
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: `arr[0]` is `first`, and each next value is the one value
from 0 to 15 whose XOR with the one before it is the code between them,
found by trying each. It checks 3000 random arrays of 1 to 10 codes from
0 to 15 and a first value from 0 to 15. Every case is drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer starts with the first value and encodes to the codes |
| P3 | the first value XORed with a mask gives every value XORed with it |
| P4 | the codes reversed, from the answer's last value, give the answer reversed |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 773147140, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, each next value the first in `range(16)` whose
XOR with the last is the code, gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M1 and M5 both make every value the
first XORed with its own code, and M4 and M9 both give each place the
value before it; each pair fails the very same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each value the first XORed with the code, not the last | P1 2698, P2 2698, P4 2709, P5 2698 |
| M2 | ★: the first value pushed with its low bit flipped | P1 3000, P2 3000, P4 3000, P5 3000 |
| M3 | ★: the code ORed onto the last value, not XORed | P1 2896, P2 2896, P3 2682, P4 2648, P5 2896 |
| M4 | scan: each place yields the state before its code | P1 2979, P2 2979, P4 2709, P5 2979 |
| M5 | scan: the state never moved past the first value | P1 2698, P2 2698, P4 2709, P5 2698 |
| M6 | scan: the first value given twice | P1 3000, P2 3000, P4 2979, P5 3000 |
| M7 | prefix: the codes read from the end | P1 2671, P2 2671, P5 2671 |
| M8 | prefix: the first place left at 0, the first value not XORed onto it | P1 2811, P2 2811, P3 2812, P4 2984, P5 2811 |
| M9 | solution: each place yields the value before its code | P1 2979, P2 2979, P4 2709, P5 2979 |
| M10 | solution: the first code skipped | P1 3000, P2 3000, P4 2687, P5 3000 |

## Benchmarks

The bench draws 200 random arrays of `10^4` codes up to `10^5`,
LeetCode's largest, all of them first, then decodes each 100 times by
the ★ arm in all five languages; each answer is a fresh vector. Every
implementation prints `200 arrays of 10000 codes, 100 rounds: last
values sum to 1273863700, checksum 542117265`. The C build also runs
clean under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.087 s |
| Rust (`rustc -O`) | 0.167 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.389 s |
| Kāra (`karac build`) | 0.414 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.417 s |
| Go | 0.515 s |
| Python | 6.8 s |

The sequential Kāra build takes 2.50x Rust's time and 1.07x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.087 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.409 s and 0.410 s on one
run).

## Verification

All four arms print the same output as `decode.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★, scan and prefix arms checked clean as first written. Kāra's
`scan` closure takes its state by value and returns the next state with
the item, `Some((state, item))`, where Rust's takes `&mut` state and
returns only the item.

LeetCode's Rust template took one `karac fix` of 8 edits:
`struct Solution {}` added, `Vec<i32>` written `Vec[i32]`,
`std::iter::once` written `once`, `|acc, &e|` written `|acc, e|`, and
the `scan` closure's body `*acc ^= e; Some(*acc)` rewritten to Kāra's
form, `let acc = acc ^ e; Some((acc, acc))`.

The differential's literal reading finds each next value with
`(0..16).find(|v| arr[i] ^ v == encoded[i]).unwrap()` and pushes it
onto the `Vec[i32]`. The range's literals keep the default `i64`, since
an operator does not fix a literal's type, so the value found is an
`i64` and the push narrowed. `karac check` said so, but only to write
`as i32`: the walk that traces an `i64` back to a range of literals
followed closure parameters and `collect`, not a `let` binding of the
range's item. Since kara `93fd9b2078` (B-2026-11-20-46) it does, the refusal names
the range, and `karac fix` writes `0i32..16`. `arm_name` indexes a list
of string literals for a `Str`, as #1662's differential does
(B-2026-11-19-131).
