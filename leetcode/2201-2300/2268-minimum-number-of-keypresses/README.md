# 2268. Minimum Number of Keypresses

You have a keypad with `9` buttons, numbered from `1` to `9`, each
mapped to lowercase English letters. You can choose which characters
each button is matched to as long as:

- All 26 lowercase English letters are mapped to.
- Each character is mapped to by **exactly** `1` button.
- Each button maps to **at most** `3` characters.

To type the first character matched to a button, you press the button
once. To type the second character, you press the button twice, and so
on.

Given a string `s`, return *the **minimum** number of keypresses needed
to type* `s` *using your keypad.*

**Note** that the characters mapped to by each button, and the order
they are mapped in cannot be changed.

```
s = "apple"         ->  5
s = "abcdefghijkl"  ->  15
```

**Constraints:** `1 <= s.length <= 10^5`; `s` consists of lowercase
English letters.

A keypad gives nine first places, nine second and eight third, and a
letter costs its count times its place. Swapping two letters so that
the more frequent one has the lower place never costs more, so the
counts sorted from the largest take the places in order: the i-th
costs `i / 9 + 1` presses. O(n).

## Approaches

| file | mechanism |
|---|---|
| `keys.kara` ★ | the 26 counts in a `Vec`, `sort_by(\|a, b\| b.cmp(a))`, the i-th priced `i / 9 + 1` |
| `keys_heap.kara` | the nonzero counts into a `PriorityQueue.max_first()`, taken off largest first, the k-th priced `k / 9 + 1` |
| `keys_rank.kara` | no sort: each letter's place is the number of letters typed more often, a tie going to the earlier letter; 26 by 26 comparisons over an `Array` of counts |
| `keys_struct.kara` | `struct Keypad` of how many letters each of the nine buttons holds; `assign` (`mut ref self`) puts the next letter, most often typed first, on the emptiest button and returns its presses |
| `keys_iter.kara` | in chains: a `fold` over the bytes counts the letters, then `sort_by`, and `enumerate().map(..).sum()` prices them |
| `keys_solution.kara` | LeetCode's Rust template: `String` in, `i32` out; `vec![0; 26]`, `sort_unstable_by`, each priced `i as i32 / 9 + 1`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and five
more (one letter, 1; the alphabet once, 51; one letter ten times, 10;
ten letters with the tenth the rarest, 29; ten letters twice each, 22),
each with its count; then 2000 random strings of 1 to 60 letters from
the first 3, 10, 12 or 26, with a checksum; then three of the
constraints' longest, 10^5 letters: random from all 26 (195184), all
`a` (100000), and weighted, `z` 26 times as often as `a` (154016).
`keys.py` mirrors the ★ arm and its output is byte-identical.

The iter arm was first written `fold(Vec.filled(26, 0), |mut acc, b| ..)`
over `s.bytes()`. `karac check` names the `mut` on a closure parameter
as Rust's and asks for `let mut acc = acc;` in the body, and `karac fix`
applies it, with the `.iter()` that `fold` needs on the `Slice[u8]`.

`karac fix` carries the template in two rounds. The first reports 6
edits: `vec![0; 26]` to `Vec.filled(26, 0)`, `sort_unstable_by` to
`sort_by`, the pattern `&c` to `c`, `struct Solution;` to `struct
Solution {}`, `Solution::` to `Solution.`, and `let mut ans: i32 = 0`,
since `ans` is the template's `i32` tail. Rust infers the counts as
`i32` from `ans += c * (i as i32 / 9 + 1)`. In Kāra the fill's literal
keeps the default `i64` beside an `i32` operand (design.md §8
Literals), so the second round finds that line a narrowing. It used to
get only the advice to write `as i32`, though the same line written
`cnt[i] * ..` was offered the fill's suffix: a loop's element was not
traced back to the fill (B-2026-11-18-82). It is now, and `karac fix`
writes `Vec.filled(26, 0i32)` and drops the adapter's `as i64`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every keypad, as the place on its button that each of the
26 letters takes, the letters in alphabetical order, with nine first
places, nine second and eight third; the least cost found by a search
over the letters and the places still free, memoised. No sort and no
ranking by count. It checks 300 random strings of 1 to 40 letters from
the first 3, 10, 12, 20 or 26; then 30 of exactly ten letters, the
tenth once; then 30 of all 26 letters. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the cost is the literal reading's |
| P2 | the letters relabelled, the alphabet turned by seven: the same cost |
| P3 | the string reversed: the same cost |
| P4 | the string twice over: twice the cost |
| P5 | at least the length and at most three times it, and exactly the length when at most nine letters are used |
| P6 | each arm agrees with at least three of the other five |

The literal reading's places are counts per place rather than buttons:
any keypad fills its buttons from the first place, so it has as many
first places as buttons in use, and 26 letters on nine buttons of at
most three each is always nine, nine and eight.

The differential prints `360 cases: checksum 516924446, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that sorts
the `s.count` of each letter and zips them with the places. On a
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
| M2 | ★: never sorted | P1 279, P2 342, P5 81, P6 279 |
| M5 | ★: a letter's count capped at 5 | P1 70, P4 273, P5 50, P6 70 |
| M6 | ★: the place by `i % 3` | P1 350, P5 149, P6 350 |
| M7 | heap: a min-first heap | P1 201, P6 201 |
| M9 | heap: the places from 1 | P1 220, P5 19, P6 220 |
| M11 | heap: letters typed once left out | P1 301, P4 301, P5 261, P6 301 |
| M12 | rank: ties never broken | P1 151, P6 151 |
| M15 | rank: three letters a place | P1 281, P5 118, P6 281 |
| M16 | rank: the first letter never compared | P1 161, P2 146, P6 161 |
| M17 | struct: one button | P1 350, P5 350, P6 350 |
| M19 | struct: sorted from the smallest | P1 360, P5 159, P6 360 |
| M20 | struct: the presses one fewer | P1 360, P5 360, P6 360 |
| M24 | iter: each letter counted twice | P1 360, P5 193, P6 360 |
| M25 | iter: letters 13 apart counted as one | P1 147, P6 147 |
| M26 | iter: the third places dropped | P1 45, P6 45 |
| M30 | solution: two letters to a count | P1 170, P2 83, P6 170 |
| M31 | solution: the largest count skipped | P1 360, P5 265, P6 360 |

P1 and P6 kill all seventeen, P5 eleven, P2 three, P4 two, and P3
none. This kata's properties are weak, and P1 carries it. Every arm
reads only the counts, so reversing the string changes nothing for any
edit, and doubling it doubles every count, which every edit but two
prices linearly: the count capped at 5 and the letters typed once left
out. Relabelling catches only the edits that treat letters by name,
`a` left out of the ranking, the counts never sorted and two letters
sharing a count. P5 catches the edits that price the first nine letters
at anything but one press, or that miss the length's bounds. Four
edits are wrong only with ten letters or more, where the order of the
counts first matters: a min-first heap, ties never broken, letters 13
apart sharing a count, and the third places dropped, which needs 19.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. All fourteen fail as a kept one does: the ★,
rank, iter and template arms' order turned (M1, M14, M22, M27) as the
struct arm's sorted from the smallest (M19); the ★ arm's eight letters
a place, the struct arm's eight buttons and the iter arm's place
counted from 1 (M3, M21, M23) as the heap arm's places from 1 (M9); the
★ arm's first places free (M4) as the struct arm's presses one fewer
(M20); the heap arm's place never moved on and the template's count
unpriced (M8, M29) as the heap arm's min-first heap (M7), each wrong
for exactly the 201 cases of ten letters or more; the heap arm's only
the top taken and the struct arm's fullest button (M10, M18) as the
struct arm's one button (M17); the rank arm's ties counted both ways
(M13) as its ties never broken (M12); and the template's three letters
a place (M28) as the rank arm's (M15).

## Verification

Every arm prints the same output as `keys.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★ arm and the template take 0.7 s, the
heap arm 0.8 s, the struct arm 0.9 s, the iter arm 1.0 s, the rank arm
1.7 s, and the differential 3.2 s.

## Benchmarks

The bench answers 40 strings of the constraints' longest, 10^5
letters, from the first 3, 10, 12 and 26 letters in turn, with the ★
arm in all five languages. Every implementation prints `40 strings of
10^5: checksum 933710288`. Each builds its string a letter at a time
from the same generator; C sorts the counts with `qsort`, Go with
`sort.Slice`.

BENCHTAB
