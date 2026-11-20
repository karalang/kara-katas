# 1734. Decode XORed Permutation

There is an integer array `perm` that is a permutation of the first `n`
positive integers, where `n` is always **odd**.

It was encoded into another integer array `encoded` of length `n - 1`,
such that `encoded[i] = perm[i] XOR perm[i + 1]`. For example, if
`perm = [1,3,2]`, then `encoded = [2,1]`.

Given the `encoded` array, return *the original array* `perm`. It is
guaranteed that the answer exists and is unique.

```
encoded = [3,1]          ->  [1,2,3]
encoded = [6,5,4,6]      ->  [2,4,1,5,3]
```

**Constraints:** `3 <= n < 10^5`; `n` is odd; `encoded.length == n - 1`.

## Approaches

| file | mechanism |
|---|---|
| `decode.kara` ★ | the XOR of all of `perm` is the XOR of 1 to n, and since n is odd the codes at odd places, `encoded[1]`, `encoded[3]`, ..., pair off every value but the first. XORing their XOR out of the whole leaves `perm[0]`, and from it each next value is the last XORed with its code, pushed onto a vector. O(n) |
| `decode_fold.kara` | the same as iterators: `(1..n + 1).fold` XORs 1 to n, `skip(1).step_by(2)` takes the codes at odd places to a second `fold`, and `once(first)` chained to a `scan` over the codes gives the values. O(n) |
| `decode_prefix.kara` | the running XOR of the codes, written one place to the right in a filled array, holds `perm[0] ^ perm[i]` at each place. Over all n places `perm[0]` appears an odd number of times and 1 to n once each, so the array's XOR and that of 1 to n together are `perm[0]`, which every place is then XORed with. O(n) |
| `decode_solution.kara` | a Rust solution as LeetCode's Rust users write it, `total ^= i` over `1..=n as i32`, `odd ^= encoded[i]` over `(1..n - 1).step_by(2)` and `perm[i + 1] = perm[i] ^ encoded[i]` into a `vec![0; n]`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 7 lines: LeetCode's two examples, the smallest
n, and 1 to 9 in order; then the values summed and a checksum for 3000
random permutations of an odd n up to 9, 300 of up to 1001 and 10 of up
to 99999, LeetCode's largest, each shuffled by Fisher-Yates and then
encoded. Each batch also checks every answer against the permutation
it was drawn from and prints `wrong` on a mismatch, which no arm does.
`decode.py` mirrors the ★ arm and its output is byte-identical.

```
[1, 2, 3]
[2, 4, 1, 5, 3]
[3, 2, 1]
[1, 2, 3, 4, 5, 6, 7, 8, 9]
3000 permutations of up to 9: values sum to 69513, checksum 475658714
300 permutations of up to 1001: values sum to 47311212, checksum 995344112
10 permutations of up to 99999: values sum to 24991124653, checksum 558206077
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the permutation of 1 to n whose neighbours XOR to the codes,
found by trying each first value from 1 to n, following the codes from
it, and keeping the one whose values are 1 to n each once. It checks
3000 random permutations of an odd n from 3 to 9, shuffled by
Fisher-Yates and encoded. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is a permutation of 1 to n and encodes to the codes |
| P3 | the codes reversed give the answer reversed |
| P4 | the answer with its first two values swapped, encoded, decodes to itself |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 561019142, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, the first of `itertools.permutations` of 1 to
n whose neighbours XOR to the codes, gives the same checksum. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Eight of them fail every problem on P1,
since a wrong first value makes every value wrong. M5 and M10 both take
the XOR of 1 to n as the first value, and fail the very same checks; it
is right by chance in 235 problems. M2 and M7 both leave every value
XORed with one constant, which the reversed codes leave the same, so
neither fails P3 or P4.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the codes at even places XORed out, not those at odd places | P1 3000, P2 3000, P4 3000, P5 3000 |
| M2 | ★: n left out of the XOR of 1 to n | P1 3000, P2 3000, P5 3000 |
| M3 | ★: each value the first XORed with its code, not the last | P1 3000, P2 3000, P3 3000, P4 3000, P5 3000 |
| M4 | fold: every other code from the first, not the second | P1 3000, P2 3000, P4 3000, P5 3000 |
| M5 | fold: the first value the XOR of 1 to n alone | P1 2765, P2 2765, P3 3000, P4 3000, P5 2765 |
| M6 | fold: each place yields the value before its code | P1 3000, P2 3000, P3 3000, P4 3000, P5 3000 |
| M7 | prefix: each place XORed with its index, not its index plus 1 | P1 3000, P2 3000, P5 3000 |
| M8 | prefix: the first place not XORed with the first value | P1 3000, P2 3000, P3 3000, P4 3000, P5 3000 |
| M9 | solution: the codes at even places XORed out | P1 3000, P2 3000, P4 3000, P5 3000 |
| M10 | solution: the first value the XOR of 1 to n alone | P1 2765, P2 2765, P3 3000, P4 3000, P5 2765 |

## Benchmarks

The bench draws 50 random permutations of 99999, LeetCode's largest
odd n, all of them first, then decodes each 40 times by the ★ arm in
all five languages; each answer is a fresh vector. Every implementation
prints `50 permutations of 99999, 40 rounds: first values sum to
102594800, checksum 243297786`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ad6400d909` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.130 s |
| Rust (`rustc -O`) | 0.208 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.489 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.519 s |
| Kāra (`karac build`) | 0.522 s |
| Go | 0.740 s |
| Python | 20 s |

The sequential Kāra build takes 2.50x Rust's time and 1.06x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md).
Rust's lead is its wrapping arithmetic: with overflow checks on it is
level, so the gap is the cost of overflow-checked arithmetic, not a
missed optimization. C is the fastest here at 0.130 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.521 s and 0.526 s on one
run).

## Verification

All four arms print the same output as `decode.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `ad6400d909`.

## Writing it

The ★ arm took one `karac fix` of 2 edits: `all` and `rest`, plain `0`s
that meet the `i32` codes only through `^=`, were declared `: i32`. The
prefix arm's `first` took the same fix.

The fold arm seeded both folds with a plain `0` and bound them by
`let`s, so `all`, `rest` and `first = all ^ rest` were `i64`, and so
were the items of `once(first).chain(..scan(first, ..))`. `karac check`
refused the `collect` into the `Vec[i32]` answer, "`Vec[i32]`
implements `FromIterator[i32]`, not `FromIterator[i64]`", with no fix:
the walk that traces a `collect`'s items back to a literal took a
`scan` seeded with one, not a value a `let` binds to one. Since kara
`045accc7ad` (B-2026-11-20-64) it follows `once(first)` and a `scan`'s start through
the `let`s, the refusal names `all`'s literal, and `karac fix` wrote
`fold(0i32, ..)` in both folds.

LeetCode's Rust template took one `karac fix` of 9 edits:
`struct Solution {}` added, `Vec<i32>` written `Vec[i32]`, `total` and
`odd` declared `: i32`, and `vec![0; n]` written `Vec.filled(n, 0i32)`.
`1..=n as i32` and `(1..n - 1).step_by(2)` carried over as written.

The differential took one `karac fix` of 3 edits, each a cast the
`i32` values took to `i64` by themselves dropped: `seen[v as i64]`
twice and `sorted[i] as i64 == i + 1`. `arm_name` in it indexes a list
of string literals for a `Str`, as #1662's does (B-2026-11-19-131).
