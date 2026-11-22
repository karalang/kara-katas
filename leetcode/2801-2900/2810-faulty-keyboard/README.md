# 2810. Faulty Keyboard

Your laptop keyboard is faulty, and whenever you type a character `'i'`
on it, it reverses the string that you have written. Typing other
characters works as expected.

You are given a **0-indexed** string `s`, and you type each character
of `s` using your faulty keyboard.

Return *the final string that will be present on your laptop screen.*

```
s = "string"     ->  "rtsng"
s = "poiinter"   ->  "ponter"
```

**Constraints:** `1 <= s.length <= 100`; `s` consists of lowercase
English letters; `s[0] != 'i'`.

## Approaches

| file | mechanism |
|---|---|
| `keyboard.kara` ★ | the screen a `String`, each letter pushed on, each i turning it round by `chars().rev().collect()` |
| `keyboard_deque.kara` | no turning while typing: a `VecDeque[char]` and a flag for the way the screen faces, a letter pushed on the back or the front, the deque read out the right way round at the end |
| `keyboard_chars.kara` | a `Vec[char]` turned in place by `reverse()`, made a `String` once at the end |
| `keyboard_split.kara` | by the pieces between the i's, from `split("i")`: read from the last back, they go alternately on the right as typed and on the left turned round, each pair one layer further in |
| `keyboard_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `Vec::with_capacity` of chars, a `match` on each char, `into_iter().collect()`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; 100
letters, LeetCode's most, with no i; a z and then 50 letters each
followed by an i; 3000 random strings of 1 to 10 letters from a, b and
i; and 50 of up to 100 from the whole alphabet, i as likely as the rest
together, the last two with the sum of the lengths and a checksum.
`keyboard.py` mirrors the ★ arm and its output is byte-identical.

```
rtsng
ponter
abcdefghjklmnopqrstuvwxyzabcdefghjklmnopqrstuvwxyzabcdefghjklmnopqrstuvwxyzabcdefghjklmnopqrstuvwxyz
bbbbbbbbbbbbbbbbbbbbbbbbbzaaaaaaaaaaaaaaaaaaaaaaaaa
3000 short strings: lengths sum to 11965, checksum 906861028
50 long strings: lengths sum to 1226, checksum 171816408
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the keys pressed in turn on a screen of characters, a letter
written at the end, an i making a new screen of the old one's
characters read from the last place to the first; no `rev()` and no
pieces. It draws 2000 random strings of 1 to 10 letters from a, b and
i, then 50 of up to 100 from the whole alphabet, i as likely as the
rest together, the first never an i, all before any arm answers; the
literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 10 letters, the screen is the literal reading's |
| P2 | one letter for each key that is not an i, and no i |
| P3 | the same letters as typed, counted |
| P4 | two more i's typed at the end: the same screen |
| P5 | one more i: the screen turned round |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 717919832, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an i typed as a letter | P1 1376, P2 1426, P3 1426, P4 2050, P5 2050, P6 1426 |
| M2 | ★: the screen never turned | P1 672, P5 1240, P6 720 |
| M3 | deque: a letter put at the back whichever way the screen faces | P1 734, P6 781 |
| M4 | deque: the deque read out forward always | P1 566, P5 1262, P6 590 |
| M5 | chars: the turn taken after the letter, not instead of it | P1 1376, P2 1426, P3 1426, P4 2050, P5 2050, P6 1426 |
| M6 | chars: only the first i turning | P1 460, P4 263, P5 979, P6 506 |
| M7 | split: the left pieces not turned round | P1 475, P5 1122, P6 520 |
| M8 | split: the right pieces read in typing order | P1 317, P5 493, P6 360 |
| M9 | solution: an i also pushed | P1 1376, P2 1426, P3 1426, P4 2050, P5 2050, P6 1426 |
| M10 | solution: the screen read out backward | P1 1213, P6 1262 |

## Benchmarks

The bench draws 20000 strings of 100 letters, LeetCode's longest, about
a fifth of them i, all of them first, then types each 10 times by the ★
arm in all five languages, each i making a fresh screen: C copies into
a new heap buffer and frees the old, Go into a new `[]byte`. Every
implementation prints `20000 strings of 100, 10 rounds: lengths sum to
15349630, checksum 39836877`.

BENCHTAB

## Verification

All five arms print the same output as `keyboard.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The split arm first called `s.split('i')` with a `char`, as Rust
allows; Kāra's `split` takes a `Str`, and `karac fix` wrote `"i"`. The
other own arms and the harness checked clean as first written.

LeetCode's Rust template took 5 `karac fix` edits, the wrapper
included: `struct Solution {}` added; `Vec<char>` became `Vec[char]`;
and `Vec::with_capacity` and `Solution::` took `.`. The `match` with a
`'i' => res.reverse()` arm and `res.into_iter().collect()` are Kāra as
written.
