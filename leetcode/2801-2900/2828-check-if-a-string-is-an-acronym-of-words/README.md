# 2828. Check if a String Is an Acronym of Words

Given an array of strings `words` and a string `s`, determine if `s` is
an **acronym** of words.

The string `s` is considered an acronym of `words` if it can be formed
by concatenating the **first** character of each string in `words` in
order. For example, `"ab"` can be formed from `["apple", "banana"]`,
but it can't be formed from `["bear", "aardvark"]`.

Return `true` *if* `s` *is an acronym of* `words`*, and* `false`
*otherwise.*

```
words = ["alice","bob","charlie"],                  s = "abc"     ->  true
words = ["an","apple"],                             s = "a"       ->  false
words = ["never","gonna","give","up","on","you"],   s = "ngguoy"  ->  true
```

**Constraints:** `1 <= words.length <= 100`; `1 <= words[i].length <=
10`; `1 <= s.length <= 100`; `words[i]` and `s` consist of lowercase
English letters.

## Approaches

| file | mechanism |
|---|---|
| `acronym.kara` ★ | the lengths first, one letter of s for each word, then every word's first byte against s's byte at the same place, by `zip` and `all`, in one expression |
| `acronym_collect.kara` | the first char of every word collected into a `String`, compared with s whole |
| `acronym_index.kara` | a `while` over the places of s and the words together, returning at the first mismatch, the counts compared at the end |
| `acronym_prefix.kara` | s consumed a char at a time, each word asked whether it `starts_with` the one-char slice off the front of what is left, and s used up exactly when the words are |
| `acronym_solution.kara` | a Rust solution as LeetCode's Rust users write it: each word's `chars().next().unwrap()`, `collect::<String>()`, compared with `s`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples; one word;
two words against four letters; 100 words whose acronym is the
alphabet run round to 100 letters; and 5000 random cases of 1 to 100
words of 1 to 10 letters from 'a' to 'c', s their acronym with one
letter redrawn, one cut (never the last) or one added, or left alone,
as a count and a checksum. `acronym.py` mirrors the ★ arm and its
output is byte-identical.

```
true
false
true
true
false
true
5000 cases: 1645 true, checksum 604162698
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: each word's first character sliced off and appended to
a `String` in order, and that string compared with s. It draws 3000
random cases as the harness does, all before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the words and s both reversed: the same answer |
| P3 | true: s with an 'a' added at the end is false |
| P4 | every word cut to its first letter and given the tail "zz": the same answer |
| P5 | the words against their own acronym: true |
| P6 | each arm agrees with at least three of the other four |

P3 first said s with a letter added is always false; a case whose s
lost its last letter and whose last word starts with 'a' is made whole
by the added 'a', and all five arms answered true there, rightly. The
property now holds only from a true answer.

The differential prints `3000 cases, 1001 true: checksum 840499948,
90000 checks over 5 arms: 0 failures` under every lane in Verification,
and a Python reading of the same cases gives the same checksum. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the lengths never compared | P1 66, P2 145, P3 1033, P6 66 |
| M2 | ★: any letter matching enough | P1 481, P6 481 |
| M3 | collect: each word's last char taken | P1 994, P4 11, P5 2980, P6 994 |
| M4 | collect: the acronym compared reversed | P1 970, P5 2936, P6 970 |
| M5 | index: a mismatch ignored | P1 486, P6 486 |
| M6 | index: extra words allowed | P1 51, P2 88, P3 17, P6 51 |
| M7 | prefix: a word holding the letter anywhere | P1 330, P4 330, P6 330 |
| M8 | prefix: letters left over in s accepted | P1 15, P2 57, P3 1016, P6 15 |
| M9 | solution: the acronym compared with a letter of s dropped | P1 1047, P2 57, P5 3000, P6 1047 |
| M10 | solution: the words' acronym taken one short | P1 1042, P2 88, P5 3000, P6 1042 |

## Benchmarks

The bench draws 20000 cases of 100 words of up to 10 letters,
LeetCode's most, s their acronym with one case in four given a letter
redrawn, all of them first, then answers each 100 times by the ★ arm in
all five languages. Every implementation prints `20000 cases of 100
words, 100 rounds: 1668600 true, checksum 865574867`.

BENCHTAB

## Verification

All five arms print the same output as `acronym.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms and the harness checked clean as first written. The
differential's literal reading first appended each slice by `formed +
w[..1]`, and `karac check` reported E0208: `+` on a `String` takes an
owned `String`, and a slice is a `Str` view (design.md § Operator
traits), where Rust's `String + &str` is accepted; `karac fix` added
the `.to_string()`.

LeetCode's Rust template took 9 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`;
`collect::<String>()` became `String.from_iter(..)` around the whole
iterator chain; `Vec<..>` became `Vec[..]`, `&str` `Str`, and
`Solution::` took `.`.
