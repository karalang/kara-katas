# 1653. Minimum Deletions to Make String Balanced

You are given a string `s` consisting only of characters `'a'` and `'b'`.

You can delete any number of characters in `s` to make `s` **balanced**.
`s` is **balanced** if there is no pair of indices `(i, j)` such that
`i < j` and `s[i] = 'b'` and `s[j] = 'a'`.

Return *the **minimum** number of deletions needed to make* `s`
***balanced***.

```
s = "aababbab"   ->  2
s = "bbaaaaabb"  ->  2
```

**Constraints:** `1 <= s.length <= 10^5`; `s[i]` is `'a'` or `'b'`.

## Approaches

| file | mechanism |
|---|---|
| `minimum_deletions.kara` ★ | one pass, counting the b's read so far: an a after them is either deleted, one more than the prefix before it needed, or kept, and then every b before it goes. O(n) |
| `minimum_deletions_split.kara` | every split point: the b's before it and the a's after it go, the a's counted once and the split walked from 0 to n. O(n) |
| `minimum_deletions_stack.kara` | a stack of letters: an a meeting a b on top pops it, one deletion for each such "ba" pair. O(n) |
| `minimum_deletions_solution.kara` | LeetCode's Rust template: the ★ arm's recurrence over the bytes with `std::cmp::min`. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's two examples, one a (0),
four b's (0), and `"bbbaa"` (2); then the deletions summed and a
checksum for 3000 random strings of up to 10 letters, 1000 of up to 1000
and 20 of up to `10^5`. `minimum_deletions.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every way of keeping some of the letters is tried, and the
fewest deletions among those that leave no b before an a is the answer.
It checks 3000 random strings of 1 to 10 a's and b's. Every string is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the string reversed with a and b swapped gives the same answer |
| P3 | a b added at the end or an a at the start gives the same answer |
| P4 | an a added at the end adds 0 or 1 to the answer |
| P5 | each arm agrees with at least two of the other three |

P2 holds because reversing and swapping maps a "b before a" pair to
another such pair. P3 holds because a b at the end or an a at the start
is never in such a pair.

The differential prints `3000 problems: checksum 588508000, 60000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. One first try was replaced: the
template counting `b_count + 1` in place of `b_count` no longer
type-checks. `b_count` is an `i64` there, its literal kept the default
because `+` does not fix a literal's type, and `dp: i32` cannot take the
`min` without a cast; `karac check` offers `b_count: i32`.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a deleted a not counted | P1 2099, P5 2099 |
| M2 | ★: every a deleted | P1 1961, P2 2496, P3 3000, P5 1961 |
| M3 | ★: the b's counted as at most one | P1 1280, P5 1280 |
| M4 | split: the b's before the split never counted | P1 2099, P5 2099 |
| M5 | split: the best start at 0 | P1 2099, P5 2099 |
| M6 | split: an a counted as a b before the split too | P1 1961, P2 2496, P3 3000, P5 1961 |
| M7 | stack: an a pairs with an a on top | P1 1948, P2 1947, P3 1015, P5 1948 |
| M8 | stack: a paired b left on the stack | P1 809, P2 1488, P5 809 |
| M9 | template: each b counted twice | P1 809, P2 1446, P5 809 |
| M10 | template: the letters' roles swapped | P1 1634, P3 2852, P5 1634 |

## Benchmarks

The bench draws 500 random strings of `10^5` letters, LeetCode's
longest, each with its own chance of a b from 0 to 100 percent, all of
them first, then answers each by the ★ arm in all five languages. Every
implementation prints `500 strings of 100000 letters: deletions sum to
12687874, checksum 890383350`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

TIMINGS

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. PARNOTE

## Verification

All four arms print the same output as `minimum_deletions.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`SHA`.

## Writing it

The ★ and stack arms checked clean as first written. The split arm took
the string's bytes with Rust's `s.as_bytes()`, and `karac fix` turned it
into `s.bytes()`.

LeetCode's Rust template takes one `karac fix` of 6 edits:
`struct Solution;` to `struct Solution {}`, `dp` declared `dp: i32` for
the `i32` it returns, `for &c in s.as_bytes()` to `for c in s.bytes()`,
`std::cmp::min` to `min`, and the `as i64` on the harness's call to it
dropped as an `i32` widening. The arm then checks and agrees with no hand
edit.
