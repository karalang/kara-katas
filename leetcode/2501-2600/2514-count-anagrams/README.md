# 2514. Count Anagrams

You are given a string `s` containing one or more words. Every
consecutive pair of words is separated by a single space `' '`.

A string `t` is an **anagram** of string `s` if the `i`th word of `t`
is a **permutation** of the `i`th word of `s`.

- For example, `"acb dfe"` is an anagram of `"abc def"`, but `"def cab"`
  and `"adc bef"` are not.

Return *the number of **distinct anagrams** of* `s`. Since the answer
may be very large, return it **modulo** `10^9 + 7`.

```
s = "too hot"  ->  18
s = "aa"       ->  1
```

**Constraints:** `1 <= s.length <= 10^5`; `s` consists of lowercase
English letters and spaces `' '`; there is a single space between
consecutive words.

Each word is permuted on its own, so the count is the product over the
words of a word's distinct rearrangements: the factorial of its length
over the factorials of its letters' counts. The modulus is prime, so
each division is a multiplication by an inverse. The approaches differ
in where the inverses come from and how the product is built.

## Approaches

| file | mechanism |
|---|---|
| `anagrams.kara` ★ | the factorials to `n` built once; each word's letters counted, and each count's factorial divided out by a Fermat power to the modulus less 2. O(n + words 26 log M) |
| `anagrams_inverse.kara` | the inverse factorials built once too: one Fermat power for the inverse of `n!`, then each one below by multiplying back down, so no word asks a power. O(n + log M) |
| `anagrams_running.kara` | the count built letter by letter: the `k`-th letter of a word, when it is the `j`-th of its kind so far, multiplies by `k / j`; the inverses of 1 to `n` from the recurrence `inv[i] = -(M / i) inv[M % i]`. O(n) |
| `anagrams_rec.kara` | recursions: the power by halving the exponent, and the count of the words from place `i` on, a word's share times the count of the rest. At most 50000 deep |
| `anagrams_iter.kara` | iterators: the factorials a `scan` over 1 to `n`, a word's counts a `fold` over its bytes, and the words `fold`ed into the product, the power itself a `fold` over the exponent's 31 bits |
| `anagrams_solution.kara` | LeetCode's Rust template: `String` in, `i32` out; the factorials in a `Vec<u64>`, a `fn` power, and each word's `bytes()` counted into a `[usize; 26]`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's two examples and five
more; then 2000 random sentences of 1 to 6 words of 1 to 8 letters from
3, and 2000 of 1 to 20 words of 1 to 30 letters from 26, each as the
sum of the answers and a checksum; then the constraints' largest: one
random word of `10^5` letters, `10^5` a's, 20000 words of 1 to 4
letters, and words of 1 to 999 letters until 99000 characters are
passed. `anagrams.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 3000 random sentences of
1 to 4 words of 1 to 7 letters, from 2, 3 or 26, against the number of
distinct permutations of each word that `itertools` lists, and the two
agreed on every sentence.

The iter arm's factorials were first written with Rust's `scan`, the
state changed through `*f = *f * i % MOD; Some(*f)`. `check` refuses
that with E0200, since Kāra's `scan` closure takes the state and gives
back the next state with the item, and `karac fix` rewrites it to
`let f = f * i % MOD; Some((f, f))`, as it stands. The ★ arm's
`counts[(b - b'a') as i64]` drew a lossless-cast warning, and `fix`
dropped the cast.

`check` first reports 4 errors on the template: `struct Solution;`,
the `mut b` and `mut e` parameters of `fn pow`, and the `&c` pattern.
`karac fix` carries it in one call, reporting 8 edits: `struct Solution
{}`; each parameter becomes plain with `let mut b = b;` and `let mut e
= e;` as the body's first lines, a scalar being copied in already;
`vec![1u64; n + 1]` becomes `Vec.filled(n + 1, 1u64)`; `split(' ')`
becomes `split(" ")`; the `&` dropped from `for &c`; and the wrapper's
lossless `as i64` dropped. The `[0usize; 26]` array, the `1..=n` range,
the `(b - b'a') as usize` index and the `ans as i32` stand as written.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each word's distinct rearrangements counted one by one, a
letter chosen for the first place from those left, skipping a letter
already tried there, and the rest arranged in turn; the counts
multiplied word by word. No factorial is taken. It checks 300 random
sentences of 1 to 4 words of 1 to 6 letters, from 3 letters or from 26;
then 20 of one word of 1 to 8 letters from 2; and 40 of 10 words of 1
to 4 letters from 2. All 360 are drawn before any arm answers, and 25
of them have only one arrangement.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the words in the reverse order: the same answer |
| P3 | every letter written as its mirror in the alphabet, `a` as `z` and `z` as `a`: the same answer |
| P4 | the sentence, a space and the sentence again: the answer squared |
| P5 | one more word, `ab`: twice the answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases, 25 with one arrangement only:
checksum 487657611, 12960 checks over 6 arms: 0 failures` under every
lane in Verification; the checksum of the literal answers was checked
against a Python reading that builds the same cases and counts the
distinct permutations `itertools` lists. On a failure it prints the
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
| M1 | ★: factorials of one more | P1 335, P5 360, P6 335 |
| M5 | ★: the word one letter short | P1 343, P5 360, P6 343 |
| M6 | ★: the counts kept across words | P1 233, P2 219, P4 360, P5 335, P6 233 |
| M7 | inverse: the greatest inverse of (n - 1)! | P1 345, P4 360, P5 360, P6 345 |
| M8 | inverse: each inverse down times i + 1 | P1 360, P4 360, P5 360, P6 360 |
| M10 | inverse: the a's uncounted | P1 144, P3 146, P6 144 |
| M12 | running: a word's counts kept | P1 221, P4 360, P5 290, P6 221 |
| M13 | running: the place kept across words | P1 266, P4 360, P5 360, P6 266 |
| M14 | running: the inverse of one more | P1 360, P5 360, P6 360 |
| M17 | rec: the last word left out | P1 274, P2 236, P4 274, P5 312, P6 274 |
| M18 | rec: the odd bit dropped | P1 263, P6 263 |
| M19 | rec: the first letter uncounted | P1 218, P6 218 |
| M22 | iter: the power's bits from 1 | P1 12, P6 12 |
| M24 | iter: an odd count past 1 taken one less | P1 132, P6 132 |
| M26 | iter: the product begun at 2 | P1 360, P4 360, P6 360 |
| M27 | solution: the factorials stopped before n | P1 72, P4 72, P5 72, P6 72 |
| M28 | solution: the product begun again each word | P1 239, P2 236, P4 274, P5 274, P6 239 |

P1 and P6 kill all seventeen, P5 eleven, P4 nine, P2 three, and P3 one,
the inverse arm's a's uncounted.

Three of the first thirty-one edits were replaced for failing exactly
as edits to other arms, which left their arms short of kept ones: the
iter arm's every letter counted as `a`, which failed as the ★ arm's
factorials of one more (M1), became an odd count past 1 taken one less
(M24); and the template's exponent halved twice and exponent `M - 1`,
which failed as the rec arm's odd bit dropped (M18), became the
factorials stopped before `n` (M27) and the product begun again each
word (M28).

Fourteen are not kept, and none survives. Twelve fail exactly as a kept
one. Six spoil the inverse of a factorial and fail as the rec arm's odd
bit dropped (M18), on just the 263 sentences with a letter at least twice in
one word, since `0!` and `1!` are 1 whatever their inverse: the ★ arm's
letters' factorials multiplied, Fermat exponent one short and even bits
taken, the inverse arm's each count divided twice, the running arm's
counts never grown, and the rec arm's power ending at the base (M2, M3,
M4, M9, M16, M21). Three fail as the ★ arm's word one letter short
(M5): the rec arm's word worth its length more, the iter arm's word's
factorial dropped, and the template's word one letter short (M20, M25,
M31). The iter arm's factorials doubled (M23) fails as the ★ arm's
factorials of one more (M1); the template's bit test `e & 2` (M29) as
the iter arm's power's bits from 1 (M22), each raising to `(M - 3) / 2`,
which by Euler's criterion is the inverse whenever the factorial is a
square modulo `M`, and so wrong on only 12 sentences; and the
template's `ans` begun at 2 (M30) as the iter arm's product begun at 2
(M26). Two fail in ways of their own, but their arms already hold their
kept edits: the inverse arm's walk down from `n - 1` (M11) and the
running arm's inverses' sign lost (M15).

## Verification

Every arm prints the same output as `anagrams.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 2.2 to 31.0 s and the differential 12.0 s; under `karac __mir-llvm-asan` the arms take 0.7 to 13.0 s and the differential 4.6 s; and under `karac run` the differential takes 0.8 s.

## Benchmarks

The bench builds 20 sentences of just under `10^5` characters once from
its own generator, words of 1 to 200 letters from 26, then makes 4
passes. Each pass asks every sentence once, starting from the place the
checksum so far picks and wrapping around, and folds each answer plus
the pass into the checksum. The bench uses the ★ arm in all five
languages, each with its own Fermat power loop. Every implementation
prints `4 passes over 20 sentences of 10^5: checksum 127138878`.

BENCHTAB
