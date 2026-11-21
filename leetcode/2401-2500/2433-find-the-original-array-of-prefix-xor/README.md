# 2433. Find The Original Array of Prefix Xor

You are given an **integer** array `pref` of size `n`. Find and return
*the array* `arr` *of size* `n` *that satisfies*:

- `pref[i] = arr[0] ^ arr[1] ^ ... ^ arr[i]`.

Note that `^` denotes the **bitwise-xor** operation.

It can be proven that the answer is **unique**.

```
pref = [5,2,0,3,1]  ->  [5,7,2,3,2]
pref = [13]         ->  [13]
```

**Constraints:** `1 <= pref.length <= 10^5`; `0 <= pref[i] <= 10^6`.

Each prefix is the one before it XOR the next value, and XOR is its own
inverse, so the value is the prefix XOR the prefix before, and the
first value is its own prefix. That one XOR per value is the whole
answer; the other ways of writing it differ in where the result is
kept, how the XOR is taken, or how literally the statement is read.

## Approaches

| file | mechanism |
|---|---|
| `original.kara` ★ | one pass, the prefix before carried, each value its prefix XOR that one pushed onto a new list. O(n) |
| `original_naive.kara` | the statement read directly: each value its prefix XOR the XOR of every value found before it, taken afresh. O(n^2) |
| `original_inplace.kara` | the list taken by `own` and each prefix XORed with the one before it from the back, so every prefix is read before it changes; no new list. O(n) |
| `original_bits.kara` | bit by bit: a bit of a value set exactly when that bit of its prefix differs from the prefix before's, for each of the 20 bits a value up to `10^6` holds. O(20 n) |
| `original_iter.kara` | iterators: the prefixes before as `once(0)` `chain`ed before the list's `cloned` values, `zip`ped with the list, each pair XORed by `map` and gathered by `collect`. O(n) |
| `original_solution.kara` | LeetCode's Rust template: `std::iter::once(pref[0])` chained before `pref.windows(2)`, each window's two prefixes XORed, and `collect()`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; one zero;
every prefix the same, so every value after the first is 0; the
constraints' largest value, `10^6`, against 0 in turn; then `10^4`
random prefixes from 0 to `10^6`, and `10^4` that rise by one from 0,
each as a checksum; and 3000 random lists of 1 to 12 prefixes from 0 to
1 up to 0 to 63, as a checksum of every answer's checksum. The largest
cases hold `10^4` prefixes, not the constraints' `10^5`, because the
naive arm takes each XOR afresh. `original.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on every array of 1 to 4
values from 0 to 15, 69904 of them, by feeding in its prefix XORs and
getting the array back.

`check` first reports 4 errors on the template, and `karac fix` carries
it in one call, reporting 7 edits: the brackets of both `Vec<i32>`, four
edits; `std::iter::once` written `once`, Kāra's `once` needing no module
path; `struct Solution;` given its braces; and, once the template
parses, `.into_iter()` put after `pref.windows(2)`, since Kāra's
`windows` returns a `Vec` of slices, not an iterator. The closure
`|w| w[0] ^ w[1]` over each slice and the bare `collect()`, whose type
comes from the return type, stand as Kāra.

Two other spellings came up while writing the arms. The harness first
walked its cases with a bare `for pref in cases`, which borrows each
element, so the in-place arm's `own` parameter drew `E0313`; it walks
them by `cases.into_iter()`, and each arm takes its own list. And the
iter arm's `once(0).chain(pref.iter())` drew a bound error, the chain
being of `i64` and `ref i64`, whose message named `.cloned()`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each value searched for from 0 upward until the XOR of the
values found before it and it equals its prefix. No prefix is XORed
with the one before it. It checks 300 random lists of 1 to 12 prefixes
from 0 to 1 up to 0 to 63; then 30 of up to 200 prefixes from 0 to
1023; then 30 of up to 200 from 0 to 1023, each prefix a copy of the one
before it half the time. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | every prefix XORed with one constant from 1 to 1023: the answer with its first value XORed with it, the rest the same |
| P3 | the answer's own prefix XORs are the list |
| P4 | the list with its last prefix repeated: the answer and a 0 |
| P5 | the first half of the list, rounded up: the first half of the answer |
| P6 | each arm agrees with at least three of the other five |

P2 holds because the constant cancels in every XOR of two prefixes and
stays only in the first. P4 holds because a value that leaves the
prefix as it was is 0, and P5 because each value depends only on its
prefix and the one before.

The differential prints `360 cases: checksum 337761688, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and runs the same search. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the before never moved | P1 330, P2 334, P3 330, P4 346, P6 330 |
| M3 | ★: OR for XOR | P1 318, P2 334, P3 318, P4 346, P6 318 |
| M4 | ★: AND NOT for XOR | P1 324, P2 308, P3 324, P6 324 |
| M8 | naive: only the value before | P1 308, P2 310, P3 308, P4 317, P6 308 |
| M9 | naive: the first value skipped | P1 316, P2 334, P3 316, P4 26, P6 316 |
| M11 | naive: the XOR so far never reset | P1 308, P2 310, P3 308, P4 318, P6 308 |
| M14 | inplace: the last left out of the walk | P1 322, P2 334, P3 322, P4 356, P5 298, P6 322 |
| M15 | inplace: the prefix after taken | P1 333, P2 334, P3 333, P4 346, P5 321, P6 333 |
| M16 | inplace: the first value cleared | P1 342, P2 360, P3 342, P6 342 |
| M17 | bits: only 9 bits | P1 60, P2 180, P3 60, P6 60 |
| M18 | bits: bit 0 skipped | P1 330, P2 186, P3 330, P6 330 |
| M19 | bits: the bit set when equal | P1 360, P3 360, P4 360, P6 360 |
| M22 | iter: the list zipped with itself | P1 359, P2 360, P3 359, P6 359 |
| M23 | iter: the before two back | P1 330, P2 334, P3 330, P4 326, P6 330 |
| M25 | iter: the before 1 at the start | P1 360, P3 360, P6 360 |
| M28 | solution: windows of three | P1 334, P3 334, P4 326, P5 310, P6 334 |
| M29 | solution: the window's first value | P1 332, P2 334, P3 332, P4 346, P6 332 |


P1, P3 and P6 kill all seventeen, P2 fourteen, P4 eleven and P5 three.

Fourteen are not kept. Thirteen fail exactly as a kept one. Five leave
every prefix as it is, so the answer is the list itself, as the ★
arm's before never moved (M1) does: the ★ arm's prefix itself kept
(M6), the naive arm's last value left out (M7), the bits arm's before
never moved (M20) and the template's window's second value (M31).
Three XOR each prefix with the prefix before it twice removed, as the
naive arm's only the value before (M8) does: the ★ arm's value before
taken for the prefix before (M2), the naive arm's prefixes XORed, not
the values (M10), and the in-place arm's walk from the front (M12),
which reads each prefix after it has changed. The ★ arm's first value
0 and the template's first prefix dropped (M5, M27) fail as the in-place
arm's first value cleared (M16); the in-place arm's first left out of
the walk (M13) as the naive arm's first value skipped (M9); the bits
arm's each bit one place up (M21) as the iter arm's list zipped with
itself (M22);
and the iter arm's OR for XOR and pair added (M24, M26) as the ★ arm's
OR for XOR (M3). One
fails apart from every kept one and was left out because that arm keeps
its share already: the template's last prefix for the first (M30).

Two of the first run were replaced, both in the naive arm and both
crashes under both backends: the value itself in the XOR read past the
values found so far, an index out of bounds, and the sum for the XOR
grew past `2^63`, an integer overflow. They became the last value left
out (M7) and the XOR so far never reset (M11).

## Verification

Every arm prints the same output as `original.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.3 to 0.6 s, but for the naive
arm, which takes 11.1 s there, 3.0 s under `karac __mir-llvm-asan` and
0.4 s under `karac run`: on the cases of `10^4` prefixes it takes `5 *
10^7` XORs. The differential takes 20.3 s under `karac __mir-run`, its
literal reading searching up to 1024 values for each of up to 200
prefixes, 5.2 s under `karac __mir-llvm-asan` and 0.5 s under `karac
run`.

## Benchmarks

The bench builds `10^5` prefixes from 0 to `10^6`, the constraints'
largest, once from its own generator. It then makes 1000 passes; pass
`p` sets one prefix to `p`, so no answer can be carried from one pass to
the next, then answers the list and folds every value of the answer
into the checksum. The bench uses the ★ arm, one pass pushing onto a
new list, in all five languages. Every implementation prints `1000
passes over 10^5 prefixes: checksum 599699628`. Every answer fills a
fresh growable list, pushed one value at a time (`Vec`, `Vec`, a slice
by `append`, a Python list), and in C a buffer grown by doubling with
`realloc`.

BENCHTAB
