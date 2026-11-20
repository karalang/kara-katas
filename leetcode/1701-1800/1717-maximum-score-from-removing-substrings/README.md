# 1717. Maximum Score From Removing Substrings

You are given a string `s` and two integers `x` and `y`. You can perform
two types of operations any number of times.

- Remove substring `"ab"` and gain `x` points.
  - For example, when removing `"ab"` from `"cabxbae"` it becomes
    `"cxbae"`.
- Remove substring `"ba"` and gain `y` points.
  - For example, when removing `"ba"` from `"cabxbae"` it becomes
    `"cabxe"`.

Return *the maximum points you can gain after applying the above
operations on* `s`.

```
s = "cdbcbbaaabab", x = 4, y = 5      ->  19
s = "aabbaaxybbaabb", x = 5, y = 4    ->  20
```

**Constraints:** `1 <= s.length <= 10^5`; `1 <= x, y <= 10^4`; `s`
consists of lowercase English letters.

## Approaches

| file | mechanism |
|---|---|
| `score.kara` ★ | taking every pair of the dearer kind first never costs one of them, and what is left of each run of `a`s and `b`s is then all of one order, so the cheaper pairs left are as many as can be had. Each pass keeps the letters not yet paired on a stack, and a letter that closes a pair with the top pops it. O(n) |
| `score_counts.kara` | the ★ arm's stack only ever holds the dearer pair's second letters under its first, so two counts stand for it: a second letter that meets an unpaired first scores the dear pair, and at the end of each run the smaller of the two counts left scores the cheap one. O(n) |
| `score_replace.kara` | the dearer pair `replace`d by nothing until none is left, then the other pair the same way, the letters lost halved counting the pairs. O(n^2) at worst |
| `score_solution.kara` | a Rust solution as LeetCode's Rust users write it, two `Vec<u8>` stacks over `s.as_bytes()`, `for &c`, and `stack.last() == Some(&first)`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's two examples, a string with
no pair, equal points, and pairs that only appear once others are gone;
then the answers summed and a checksum for 3000 random strings of up to
12 letters, 300 of up to 1000 and 10 of up to `10^5`, each mostly `a`s
and `b`s. `score.py` mirrors the ★ arm and its output is byte-identical.

```
19
20
0
6
12
3000 strings of up to 12 letters: answers sum to 16062, checksum 510673670
300 strings of up to 1000 letters: answers sum to 344096002, checksum 494106392
10 strings of up to 100000 letters: answers sum to 645110632, checksum 164454183
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every `ab` or `ba` in the string removed in turn, the rest
scored the same way, the best taken, with a `Map` keeping each string's
score once found. It checks 3000 random strings of 1 to 9 letters, each
`a` or `b` four times in nine and `x` once, and points from 1 to 6.
Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every `a` and `b` swapped, with x and y swapped, gives the same answer |
| P3 | the string reversed, with x and y swapped, gives the same answer |
| P4 | the string twice with a `z` between gives twice the answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 535154613, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, every removal tried under `lru_cache`, gives
the same checksum. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Ten edits to the differential, two to four to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. A first M10, the solution's first pass
skipping the string's first letter, was refused at check: `bytes()`
gives a `Slice`, whose adaptors need `.iter()`. It was replaced. M2, M8
and M9 all take the dearer pair again in the second pass, in three arms,
and fail the very same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the cheaper pair taken first | P1 965, P5 965 |
| M2 | ★: the second pass taking the dearer pair again | P1 982, P2 253, P3 253, P5 982 |
| M3 | ★: a pair closed by any unpaired letter on the stack, not only the top | P1 390, P2 26, P3 297, P4 920, P5 390 |
| M4 | counts: a run's unpaired second letters carried into the next | P1 223, P2 71, P3 181, P4 488, P5 223 |
| M5 | counts: a second letter pairs only past one unpaired first | P1 1056, P3 741, P5 1056 |
| M6 | counts: the last run's cheap pairs never scored | P1 754, P2 205, P3 531, P4 754, P5 754 |
| M7 | replace: one pair counted a pass | P1 582, P2 88, P3 88, P4 2114, P5 582 |
| M8 | replace: the second pass taking the dearer pair again | P1 982, P2 253, P3 253, P5 982 |
| M9 | solution: the second pass taking the dearer pair again | P1 982, P2 253, P3 253, P5 982 |
| M10 | solution: the cheap pairs scored at the dear pair's points | P1 802, P5 802 |

## Benchmarks

The bench draws 20 random strings of `10^5` letters, LeetCode's longest,
each `a` or `b` but for one `c` in a hundred, all of them first, then
answers each 100 times by the ★ arm in all five languages. Every
implementation prints `20 strings of 100000 letters, 100 rounds: answers
sum to 499741188300, checksum 981364526`. Kāra, Rust, Go and Python keep
the stacks as vectors of `char`; the C mirror holds the letters as
`uint32_t` in arrays allocated once an answer. The C build also runs
clean under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.919 s |
| Kāra (`karac build`) | 0.929 s |
| C (`clang -O3`) | 1.000 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.126 s |
| Rust (`rustc -O`) | 1.194 s |
| Go | 1.539 s |
| Python | 9.2 s |

The sequential Kāra build is 23% faster than Rust and 18% faster than
Rust with overflow checks on, the equal-safety comparison
(BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.904 s and 0.918 s on one
run).

## Verification

All four arms print the same output as `score.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ arm's `gained` started as a plain `0`, as in Rust, and met the
`i32` points only through `+=`; it kept the default `i64` and was
returned as the `i32` answer, and `karac fix` declared it `gained: i32`.
Its `kept.last() == Some(first)`, a reference to the top against a
`char`, was refused, and the fix wrote `kept.last().cloned()`.

The counts arm's `firsts` and `seconds` meet the `i32` total only through
the free `min`, `total += min(firsts, seconds) * less`. `karac check`
named the narrowing but `karac fix` had no edit for it: the walk that
finds the literals behind an operand did not go into a call of `min` or
`max`. It does since kara `93fd9b2078` (B-2026-11-20-45), and the fix declares both `i32`.

The replace arm rebinds its string `let mut s = s;`, which needs it
owned; `karac fix` wrote both functions' parameter `s: own String`.

LeetCode's Rust template took one `karac fix` of 20 edits:
`struct Solution {}` added, `Vec<u8>` and `Vec::new()` written
`Vec[u8]` and `Vec.new()`, `ans: i32` declared, `for &c in
s.as_bytes()` written `for c in s.bytes()`, `for &c in stack.iter()`
written `for c in stack.iter()`, `&&` written `and`, and `Some(&first)`
written `Some(ref first)`.

The harness first passed each string literal `.to_string()`; a `String`
parameter takes the literal as it is, and `karac fix` dropped the calls.
The differential checked clean as first written. `arm_name` in it
indexes a list of string literals for a `Str`, as #1662's does
(B-2026-11-19-131).
