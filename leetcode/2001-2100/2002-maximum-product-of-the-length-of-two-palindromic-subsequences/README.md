# 2002. Maximum Product of the Length of Two Palindromic Subsequences

Given a string `s`, find two disjoint palindromic subsequences of `s` such
that the product of their lengths is maximized. The two subsequences are
disjoint if they do not both pick a character at the same index. Return the
maximum possible product of the lengths of the two palindromic subsequences.

```
s = "leetcodecom"   ->  9    ("ete" and "cdc")
s = "bb"            ->  1    ("b" and "b")
s = "accbcaxxcxx"   ->  25   ("accca" and "xxcxx")
```

**Constraints:** `2 <= s.length <= 12`; `s` consists of lowercase English
letters only.

Twelve positions give 4096 subsets, so every approach enumerates them as
bitmasks.

## Approaches

| file | mechanism |
|---|---|
| `palindromes.kara` ★ | for each mask whose letters read as a palindrome, the letters left out get their longest palindromic subsequence by interval DP. O(2^n n^2) |
| `palindromes_pairs.kara` | every palindromic mask collected with its length, then every pair with no position in common multiplied. O(4^n) |
| `palindromes_submask.kara` | `within[m]`, the longest palindrome using only positions in `m`, from its submasks one position smaller; each palindromic mask pairs with `within` of its complement. O(2^n n) |
| `palindromes_iter.kara` | the palindromic masks from `filter` over `1..1 << n` (a mask tested by `zip` with its reverse and `all`), then `flat_map` over ordered disjoint pairs and `max`. O(4^n) |
| `palindromes_peel.kara` | a mask tested by peeling its lowest and highest set bits (`trailing_zeros`, `leading_zeros`), the palindromic masks sorted longest first, and the pair search cut off once no pair can win. O(4^n) worst |
| `palindromes_solution.kara` | LeetCode's Rust template (`impl Solution`, `as_bytes`, `usize` masks, `(mut i, mut j)`, an `&str` wrapper), carried by `karac fix` to one remaining error: blocked by B-2026-11-07-3 |
| `differential.kara` | the five arms that check against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's three
examples and five more; then the sum and a checksum of the answers for 1500
strings of 2 to 8 letters over 1 to 3 letters, and for 60 strings of 9 to
12 letters over 2 to 5 letters. `palindromes.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms that check and the
statement read literally: every way of giving each position to the first
subsequence, the second, or neither, kept when both are non-empty
palindromes, the largest product of their lengths. It checks 1000 problems
of 2 to 7 letters over 1 to 4 letters. Every random choice of a problem
(the string, a renaming of its letters, a letter to append) is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally (strings of up to 6 letters) |
| P2 | the string reversed leaves the answer |
| P3 | the letters renamed one-to-one leave the answer |
| P4 | one more letter appended never lowers the answer |
| P5 | the answer lies between 1 and `floor(n / 2) * ceil(n / 2)` |
| P6 | each arm agrees with at least two of the other four |

The differential prints `1000 problems: checksum 519790476, 30000 checks
over 5 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property. The Rust-template arm
joins it, as a sixth, once it checks.

## Mutation testing

Twenty-five edits to the differential, five to each of its arms, each run
under `karac __mir-run` and `karac __mir-llvm-run`. Fifteen are kept, three
to each arm. All twenty-five are killed, each fails the same way under both
backends, none by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the left-out letters' palindrome read as their count | P1 222, P6 281 |
| M2 | ★: a single letter worth nothing in the DP | P1 410, P5 201, P6 448 |
| M3 | ★: the DP's skip taking the shorter side | P1 40, P4 212, P6 72 |
| M4 | pairs: the palindrome test stopping one pair early | P1 205, P6 244 |
| M5 | pairs: each length one more than the count | P1 821, P5 969, P6 1000 |
| M6 | pairs: only pairs with the first mask | P1 459, P2 312, P6 638 |
| M7 | submask: `within` not passed down from submasks | P1 21, P4 48, P5 30, P6 31 |
| M8 | submask: the complement read as the mask itself | P1 679, P5 801, P6 847 |
| M9 | submask: a palindrome's own length one short | P1 821, P5 466, P6 1000 |
| M10 | iter: the smallest product taken | P1 620, P6 799 |
| M11 | iter: the sum of the two lengths less one for their product | P1 345, P6 524 |
| M12 | iter: only the outer pair of letters compared | P1 41, P6 69 |
| M13 | peel: the high bit read one too low | P1 235, P2 127, P6 302 |
| M14 | peel: the pruning one step too eager | P1 339, P4 42, P5 201, P6 352 |
| M15 | peel: only the low bit peeled | P1 112, P6 200 |

P1 and P6 kill all fifteen, P5 six, P4 three, P2 two and P3 none. P3 is
blind by construction: no arm, correct or edited, reads a letter except to
compare it with another, and a one-to-one renaming keeps every comparison.
It stays as a guard on that very fact. P2 sees the edits that favour one
end of the string (M6 keeps the pairs of the first mask, which holds the
lowest position; M13 misreads the highest bit). P4 sees the edits that can
lose ground when a letter is added (a shorter side of the DP, an eager cut,
a `within` that forgets a submask's best).

The other ten fail as a kept one does, or add nothing. The ★ arm taking
every mask as a palindrome and the iterator arm's ordered pairs allowed to
overlap fail as M1 and as the pairs arm's overlapping pairs do; that last
signature is shared three ways (pairs, iterator, peel ignoring overlap).
The ★ arm's DP adding one for a match fails as M11; the iterator arm's
palindrome test against the letters unreversed as M1; the peel arm sorted
shortest first as M10. The pairs arm counting only masks below the top
position and the submask arm's `full` missing its top position fail alike,
and the submask arm's `within` never starting from its own length fails
with counts of its own. Two first drafts survived every check and were
replaced, both equivalent: the ★ arm never picking the last position (the
left-out side picks it, and the product is symmetric), and the iterator
arm's length `count_ones().min(m)` (a mask is never below its count of
ones).

## Verification

Every arm but the Rust template prints the same output as `palindromes.py`
under `karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`,
and `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any of them. Under `karac __mir-run` the arms take 1.8 s
(submask) to 2.8 s (pairs), but the iterator arm 24.9 s, and the
differential 16.3 s.

The five arms were written in Kāra. The ★ arm first read the bytes as
`s.bytes().collect()`, which the checker refuses with a fix (`bytes()` is
a `Slice[u8]`, and adaptors need `.iter()`); it reads `s.bytes().to_vec()`.
The pairs, iterator and peel arms carried `as i64` after `count_ones()`,
which `karac fix` removes, and the peel arm's `!` for a bitwise complement
is `~`. The iterator arm first compared a Vec's iterator with its reverse
by `.eq(..)`, which the library does not have (`docs/library/iterators.md`
lists no `eq`); it reads `zip(..).all(..)`.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in two rounds (twelve edits, then six) to one error it has no fix for:
`let mut best = 0;` takes `i64` on the spot, so `best.max(x * y)` over
`i32` lengths and the `i32` return are refused. Rust types that literal
`i32` from its later uses; design.md §8 says Kāra's literals default last
too, and B-2026-11-07-3 tracks that the checker does not yet. The `&str`
wrapper had no working fix before this kata: the `&T` edit made it `ref
Str`, and a `String` argument does not pass as `ref Str`, so every call
failed with no fix. `&str` now becomes `Str` in one edit (kara f753a3e8bb,
`tests/kata_2002_check_gaps.rs`).

## Benchmarks

The bench builds 3000 strings of 12 letters over 2 to 5 letters once in all
five languages and runs the ★ arm on each: 12.3 million masks, each split
into its picked and left-out letters, and the DP for the palindromic ones.
Every implementation prints `3000 strings: sum 88756, checksum 219526616`.
Every language allocates the picked, left-out and reversed buffers and the
DP table per mask, as the Kāra program does.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `f753a3e8bb` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 1.037 to 1.129 s | 1.070 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.210 to 1.306 s | 1.235 s |
| Kāra (`karac build`) | 1.246 to 1.278 s | 1.262 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.252 to 1.369 s | 1.286 s |
| Rust (`rustc -O`) | 1.324 to 1.381 s | 1.358 s |
| Go | 1.877 to 2.090 s | 1.977 s |
| Python | 10.5 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (1.254 s) is below its real time.

Kāra is 1.04x Rust under overflow checks, inside the spread of either. The
work is mostly allocation: three small buffers per mask and an `n`-row DP
table for each palindromic one, so all three native languages spend their
time in the allocator rather than in arithmetic (inferred from the program's
shape, not measured). Rust without overflow checks is slower than with them
in these runs, which is noise of that size, not a property of the checks.
