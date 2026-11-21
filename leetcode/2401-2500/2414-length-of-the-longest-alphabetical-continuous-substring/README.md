# 2414. Length of the Longest Alphabetical Continuous Substring

An **alphabetical continuous string** is a string consisting of
consecutive letters in the alphabet. In other words, it is any substring
of the string `"abcdefghijklmnopqrstuvwxyz"`.

- For example, `"abc"` is an alphabetical continuous string, while
  `"acb"` and `"za"` are not.

Given a string `s` consisting of lowercase letters only, return *the
length of the **longest** alphabetical continuous substring.*

```
s = "abacaba"   ->  2      ("ab")
s = "abcde"     ->  5
```

**Constraints:** `1 <= s.length <= 10^5`; `s` consists of only English
lowercase letters.

A substring is alphabetical exactly when each letter is the one after
the letter before it, so the answer is the longest run of such steps,
plus one. No run passes `z`, so none is longer than 26.

## Approaches

| file | mechanism |
|---|---|
| `alpha.kara` ★ | one scan: the run grows while each byte is one more than the one before, and restarts at 1 otherwise, the longest kept. O(n) |
| `alpha_window.kara` | a window: `start` moves to any letter that does not follow the one before, and every window from `start` to `i` is a candidate. O(n) |
| `alpha_dp.kara` | dynamic programming over `chars()`: `ending[i]` one more than `ending[i - 1]` when `chars[i] as u32` follows, the answer the largest. O(n) |
| `alpha_find.kara` | the alphabet itself: from each start, the string and the alphabet read side by side from that letter's place for as long as they agree. O(26 n) |
| `alpha_iter.kara` | iterators: the adjacent pairs by `windows(2)`, each mapped to whether it steps up by one, a `scan` carrying the run, its `max` the answer; carried by `karac fix` |
| `alpha_solution.kara` | LeetCode's Rust template: the string shadowed by its `as_bytes()`, the best and the run in a `(mut ans, mut cnt)` pair; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; one letter;
the alphabet, and it backwards; the alphabet with `xyz` before it and
`ab` after; `10^5` letters rising half the time and `10^5` rising one
time in a hundred; then 3000 random strings of up to 30 letters from
the first 2 to 26, with a checksum and the total of the answers.
`alpha.py` mirrors the ★ arm and its output is byte-identical, and the
mirror was checked on 20000 random strings of up to 15 letters against
testing every substring against the alphabet.

`alpha_iter.kara` was first written with `.map` straight after
`windows(2)`, which in Kāra returns a `Vec` of slices; `check` reports 1
error there and `karac fix` adds the `.into_iter()` in 1 edit.

`check` first reports 3 errors on the template, and `karac fix` carries
it in one call, reporting 8 edits: the two `mut`s of `(mut ans, mut
cnt)` moved before the whole pattern, in 3 edits; `as_bytes()` written
`bytes()`; the two literals `1` given an `i32` suffix, since the
function returns `ans`; `struct Solution;` given its braces; and the
wrapper's widening `as i64` removed. `s[i] == s[i - 1] + 1` on bytes
and `ans.max(cnt)` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every substring of the string, each compared letter by
letter with the alphabet from its first letter's place, and the longest
that matches. No runs. It
checks 300 random strings of 1 to 12 letters from the first 2 to 26,
which the literal reading answers; then 30 of up to 3000 letters from
all 26 rising half the time; then 30 of up to 3000 letters from the
first 3 rising a third of the time. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | up to 12 letters, the answer is the literal reading's |
| P2 | some substring of the answer's length rises one letter at a time, and none one longer does |
| P3 | the string reversed and each letter mirrored, `a` for `z`: the same answer |
| P4 | the string written twice: at least the answer, and at most the larger of the answer and twice it capped at 26 |
| P5 | the first letter dropped: the answer or one less |
| P6 | each arm agrees with at least three of the other five |

P2 checks every case, the large ones too, by testing each window of the
two lengths once. P3 holds because reversing a rise and mirroring its
letters gives a rise again, P4 because the only new substrings run
across the join, joining a run that ends the string to one that starts
it, and P5 because dropping a letter shortens only the runs that start
there.

The differential prints `360 cases: checksum 769641263, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tests every substring against the alphabet. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the best starting at 0 | P1 61, P2 61, P4 3, P5 28, P6 61 |
| M3 | ★: a broken run restarting at 0 | P1 116, P2 176, P3 90, P5 35, P6 176 |
| M4 | ★: the best one short of the run | P1 239, P2 299, P4 2, P6 299 |
| M7 | window: only a fall breaking the window | P1 117, P2 171, P6 171 |
| M8 | window: a new window opened a letter early | P1 165, P2 225, P3 69, P6 225 |
| M11 | window: the best starting at 2 | P1 61, P2 61, P6 61 |
| M13 | dp: a step of two letters followed | P1 227, P2 287, P6 287 |
| M14 | dp: every run starting at 0 | P1 300, P2 360, P4 5, P6 360 |
| M16 | dp: only the first half walked | P1 132, P2 155, P3 168, P4 8, P5 17, P6 155 |
| M18 | find: the first start skipped | P1 135, P2 135, P3 69, P4 34, P6 135 |
| M20 | find: a run capped at 10 | P1 10, P2 25, P6 25 |
| M21 | find: the alphabet read a letter late | P1 300, P2 360, P6 360 |
| M22 | iter: any rise continuing a run | P1 91, P2 119, P6 119 |
| M23 | iter: a rise counted twice | P1 239, P2 299, P4 5, P5 104, P6 299 |
| M24 | iter: only the last run | P1 108, P2 168, P3 149, P6 168 |
| M27 | solution: a falling step continuing a run | P1 215, P2 275, P6 275 |
| M28 | solution: a run capped at 5 | P1 47, P2 104, P6 104 |

P1, P2 and P6 kill all seventeen, P4 six, P3 five, and P5 four. P3,
P4 and P5 hold an arm's answers against its own on a changed string, so
a mutant that errs the same way on the reversed, doubled or shortened
string passes them; P1 and P2 judge each answer against the string
itself.

Of the thirty-one, fourteen were not kept. Seven fail the same checks
as a kept one: the ★ arm's any rise continuing a run (M1) as the iter
arm's (M22); the window one short (M9) as every run starting at 0
(M14); the dp arm's rise counted twice and only the last run (M12,
M15) as the iter arm's (M23, M24); every other letter of the alphabet
(M19) as a step of two letters followed (M13); the iter arm's broken
run restarting at 0 (M25) as the ★ arm's (M3); and the template's
answer starting at 2 (M31) as the best starting at 2 (M11). Seven fail
apart from every kept one and were left out because those arms keep
their share already: the ★ arm's first pair skipped (M5) and repeated
letter continuing a run (M6); the window arm's last letter never read
(M10); the find arm's walk stopping before z (M17); the iter arm's scan
starting at 0 (M26), which fails as M5 does; and the template's answer
the current run (M29) and broken run restarting at 2 (M30).

## Verification

Every arm prints the same output as `alpha.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.6 to 1.8 s, most of it the two
strings of `10^5` letters. The differential takes 11 s there, 1.6 s
under `karac __mir-llvm-asan` and 0.7 s under `karac run`.

## Benchmarks

The bench builds 10 strings of `10^5` letters, string `i`'s letters
following the one before with odds `(i + 1) / (i + 2)`, once from the
harness's generator, then makes 200 passes, answering every string and
folding each answer plus the pass into the checksum, with the ★ arm in
all five languages. Every implementation prints `200 passes over 10
strings of 10^5 letters: checksum 217420812`. The scan is one compare
and an addition per letter; Kāra checks the addition for overflow and
every index, Rust and Go check every index, and C checks neither.

BENCHTAB
