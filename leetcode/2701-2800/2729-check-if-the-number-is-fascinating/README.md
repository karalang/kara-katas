# 2729. Check if The Number is Fascinating

You are given an integer `n` that consists of exactly `3` digits.

We call the number `n` **fascinating** if, after the following
modification, the resulting number contains all the digits from `1` to
`9` **exactly** once and does not contain any `0`'s:

- **Concatenate** `n` with the numbers `2 * n` and `3 * n`.

Return `true` *if* `n` *is fascinating, or* `false` *otherwise*.

```
n = 192  ->  true
n = 100  ->  false
```

**Constraints:** `100 <= n <= 999`.

## Approaches

| file | mechanism |
|---|---|
| `fascinating.kara` ★ | n, 2 n and 3 n written one after another by an f-string; the digits sorted spell "123456789" exactly when every digit from 1 to 9 is there once and no 0 is. O(1) |
| `fascinating_mask.kara` | the digits of n, 2 n and 3 n taken off by `% 10`, with no text at all, each setting its bit of a mask; a 0, or a digit whose bit is already set, fails at once, and nine digits must have been seen. O(1) |
| `fascinating_counts.kara` | an `Array[i64, 10]` counts each digit of the joined text, and the answer asks the counts of 1 to 9 to be 1, by `all`, and that of 0 to be 0. O(1) |
| `fascinating_set.kara` | the joined text must be nine characters long, hold no "0", and its characters gathered into a `Set[char]` must still number nine. O(1) |
| `fascinating_solution.kara` | a Rust solution as LeetCode's Rust users write it, `format!` of the three numbers, the chars sorted and collected back into a `String` by turbofish, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's two examples; 999; every
fascinating number from 100 to 999; and how many of the 900 are, with a
checksum of every verdict. `fascinating.py` mirrors the ★ arm and its
output is byte-identical.

```
true
false
false
[192, 219, 273, 327]
4 of 900 fascinating, checksum 891663036
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the three numbers written one after another into one string,
each of the digits 1 to 9 counted in it and found exactly once, and 0
found nowhere. It checks every n from 100 to 999, LeetCode's whole
domain, and then 2000 random n up to `10^5`, beyond it, where the joined
text is too long.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | where 3 n has four digits or more: false |
| P3 | where n repeats a digit or holds a 0: false |
| P4 | where true: n is a multiple of 3, since the digits 1 to 9 sum to 45 and n + 2 n + 3 n leaves the same remainder by 9 as they do |
| P5 | over 100 to 999, exactly 4 are true, each arm counted once |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2900 cases: checksum 147058292, 87000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by `str.count` gives the same checksum. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. With only four true answers in the domain, most
edits fail a handful of checks: M4 and M8, a 0 let through, fail a
single case, 267, whose joined text 267534801 holds nine different
digits with a 0 in place of the 9. One first choice was equivalent and was replaced: the counts
arm no longer asking that 0 be absent. No n at all joins to the ten
digits 0 to 9 once each (none below `10^6`, checked in Python), so with
the digits 1 to 9 there once each, the text is nine long and holds no 0.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the digits never sorted | P1 4, P5 1, P6 4 |
| M2 | ★: 3 n left out of the text, 2 n written twice | P1 4, P5 1, P6 4 |
| M3 | mask: a repeated digit let through | P1 142, P3 51, P4 97, P5 1, P6 142 |
| M4 | mask: a 0 let through | P1 1, P5 1, P6 1 |
| M5 | counts: a 9 counted as a 0 | P1 4, P5 1, P6 4 |
| M6 | counts: 9 never asked | P1 3, P2 3, P3 1, P5 1, P6 3 |
| M7 | set: the length never asked | P1 163, P2 163, P3 93, P4 99, P5 1, P6 163 |
| M8 | set: a 0 let through | P1 1, P5 1, P6 1 |
| M9 | solution: compared with the digits 0 to 8 | P1 5, P5 1, P6 5 |
| M10 | solution: the text reversed, not sorted | P1 4, P5 1, P6 4 |

## Benchmarks

The bench draws `10^6` three-digit numbers, every 50th one of the four
fascinating ones so that both answers are common, all of them first,
then answers each 5 times by the ★ arm in all five languages: the text
is formatted, its digits sorted and compared. C formats with `snprintf`
and sorts the nine or ten characters by insertion; the others use their
own sort. Every implementation prints `1000000 numbers, 5 rounds: 122040
fascinating, checksum 240676925`.

BENCHTAB

## Verification

All five arms print the same output as `fascinating.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★, mask and set arms checked clean as first written. The counts arm
took one `karac fix`: an `as i64` on the byte difference used as an
index dropped, since a `u8` widens by itself.

LeetCode's Rust template took one `karac fix` of 7 edits, the wrapper
included: `struct Solution {}` added, `format!("{}{}{}", n, 2 * n, 3 *
n)` became the f-string `f"{n}{2 * n}{3 * n}"`, `Vec<char>` became
`Vec[char]`, the turbofish `collect::<String>()` became
`String.from_iter(v.into_iter())`, since a comparison does not fix what
`collect` builds, and `Solution::` became `Solution.`.
