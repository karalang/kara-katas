# 2135. Count Words Obtained After Adding a Letter

You are given two **0-indexed** arrays of strings `startWords` and
`targetWords`. Each string consists of **lowercase English letters**
only.

For each string in `targetWords`, check if it is possible to choose a
string from `startWords` and perform a **conversion operation** on it to
be equal to that from `targetWords`.

The **conversion operation** is described in the following two steps:

1. **Append** any lowercase letter that is **not present** in the string
   to its end. For example, if the string is `"abc"`, the letters `'d'`,
   `'e'`, or `'y'` can be added to it, but not `'a'`. If `'d'` is added,
   the resulting string will be `"abcd"`.
2. **Rearrange** the letters of the new string in **any** arbitrary
   order. For example, `"abcd"` can be rearranged to `"acbd"`, `"bacd"`,
   `"cbda"`, and so on. Note that it can also be rearranged to `"abcd"`
   itself.

Return the **number of strings** in `targetWords` that can be obtained by
performing the operations on **any** string of `startWords`.

Note that you will only be verifying if the string in `targetWords` can
be obtained from a string in `startWords` by performing the operations.
The strings in `startWords` **do not** actually change during this
process.

```
startWords = ["ant","act","tack"], targetWords = ["tack","act","acti"]  ->  2
startWords = ["ab","a"], targetWords = ["abc","abcd"]                    ->  1
```

**Constraints:** `1 <= startWords.length, targetWords.length <= 5 *
10^4`; `1 <= startWords[i].length, targetWords[j].length <= 26`; each
string consists of lowercase English letters only; no letter occurs
more than once in any string of `startWords` or `targetWords`.

No letter repeats in a word and the letters may be put in any order, so
a word is just its set of letters: 26 bits. A target is obtained when
taking away one of its letters leaves the set of some start word.
O((s + t) * 26).

## Approaches

| file | mechanism |
|---|---|
| `words.kara` ★ | each word's letters as bits of an `i64`; the start words' masks collected into a `Set[i64]`, and each target's letters taken away in turn by `^` |
| `words_sorted.kara` | no bits: each start word's letters sorted into a `String` in a `Set[String]`; each target sorted, and each of its letters left out by slicing round it, `f"{t[..i]}{t[i + 1..]}"`, under `any` |
| `words_forward.kara` | forwards: every set a start word can grow into, its mask with each letter it lacks added, listed up front in one `Set[i64]`; a target counts when its own mask is there, by `filter` and `count`; masks built by `fold` over `bytes().iter()` |
| `words_struct.kara` | a `struct Letters` built `of` a word, asked whether it `has` a letter and for itself `without` one (`ref self`); the starts counted in a `Map[i64, i64]` through `entry().or_insert(0)` |
| `words_search.kara` | no hash: the start masks sorted into a `Vec[i64]` and looked up by `binary_search`; each target's letters peeled off lowest first with `rest & -rest`; the mask built by a closure |
| `words_solution.kara` | LeetCode's Rust template: a `HashSet` of masks built with `c as u8 - b'a'`, looked up by `contains(&..)`; carried by `karac fix` in four rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(a target the same as a start, the same letters in another order, a
letter added and moved, and a target met three times), each with its
answer; then the total and a checksum over 2000 random pairs of lists of
1 to 6 words, each of distinct letters from the first 3, 4 or 6 in
turn; then the constraints' largest, 50000 words in each list, of 1 to 8
letters from the first 10 and of 1 to 26 from all 26. `words.py` mirrors
the ★ arm and its output is byte-identical.

One compiler gap was met, in the differential, and fixed in karac
d2b676af88 (B-2026-11-14-60): the checker refused `turn(p.starts)` after
`(0..6).map(|arm| answer(arm, p.starts, p.targets)).collect()`, as a
consume of `p.starts` under the closure's borrow, though the closure was
gone once `collect` returned, and a call through `turn`, whose parameter
borrows, consumes nothing.

`karac fix` carries the template in five rounds of 19, 1, 4, 2 and 2 edits:
Rust's spellings (the `use` dropped, `<..>` to `[..]`, `HashSet::new` to
`HashSet.new`, `for w in &start_words` to `for w in ref start_words`,
the `&` dropped from `contains(&(..))`, `struct Solution;` to `struct
Solution {}`, the adapter's `&Vec` to `ref Vec`, `Solution::` to `.`);
then `HashSet` to `Set`; then each `c as u8` to `c as u32 as u8`, since
a `char` does not cast to `u8` in one step, and the adapter's `as i64`
dropped, since an `i32` widens on return; then the `ref` dropped from
the adapter's two parameters, which borrow already. The adapter's two
`clone()`s, handed to the template's borrowing parameters, were kept
until the `redundant_clone` lint that kata 2125 asked for landed (karac
B-2026-11-14-3), and the fifth round drops them. Two arms were written with Rust's `w.bytes().fold(..)`,
and `karac fix` put in the `.iter()` that Kāra's byte slice needs.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a target counts when some start word, with some letter of the
alphabet it lacks appended, can be rearranged into it, the rearranging
checked by sorting both; no letter set is formed. It checks 300 random
pairs of lists of 1 to 5 words of distinct letters from the first 3, 4
or 6 in turn; then 30 whose targets are mostly start words with a letter
added and shuffled in; then 30 of words of 1 to 4 letters from all 26.
All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the targets in reverse order: the same answer |
| P3 | every word of both lists reversed: the same answer |
| P4 | every letter moved on by one, z to a: the same answer |
| P5 | every start word listed twice: the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 pairs: checksum 461977519, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
pairs by the same appending and sorting. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Twenty-seven edits to the differential, four to five to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a target counted once per letter that works | P1 43, P6 43 |
| M4 | ★: each letter's bit one place up | P1 140, P6 140 |
| M5 | ★: only the first letter taken away | P1 130, P3 131, P6 130 |
| M6 | sorted: the letters unsorted | P1 90, P6 90 |
| M7 | sorted: the last letter never left out | P1 77, P6 77 |
| M9 | sorted: the target found whole among the starts | P1 106, P6 106 |
| M11 | forward: the last letter of the alphabet never added | P4 1 |
| M13 | forward: every target read with an a | P1 104, P4 175, P6 104 |
| M26 | forward: the first start never grown | P1 76, P5 76, P6 76 |
| M14 | struct: `has` asking the letter after | P1 153, P6 153 |
| M15 | struct: `without` leaving the letter in | P1 184, P6 184 |
| M27 | struct: the letter a never tried | P1 53, P4 53, P6 53 |
| M19 | search: the starts unsorted | P1 88, P6 88 |
| M20 | search: the whole mask looked up | P1 171, P6 171 |
| M21 | search: the highest letter alone tried | P1 129, P6 129 |
| M23 | solution: the adapter's lists swapped | P1 223, P5 166, P6 223 |
| M25 | solution: the template's mask kept across targets | P1 132, P2 106, P6 132 |

P1 and P6 kill sixteen, P4 three, P5 two, and P3 and P2 one each. The
answer depends only on which letter sets the words hold, so most wrong
edits show at once against the literal reading and the other arms, and
the four other properties are there for the edits that tie the answer
to something every right answer ignores. P4 moves every letter on by
one, which sees an edit that treats one letter apart: the forward arm
never adding z (M11), which no draw of P1 meets, since no target there
is a start with z added, while one draw has a target that is a start
with y added, and the shift makes that y a z; every target read with an a (M13); and the letter a
never tried (M27). P5 lists every start twice, which sees the forward
arm's first start never grown (M26), since the copy grows it, and the
adapter's lists swapped (M23), since the doubled starts are then
counted as targets. P3 reverses every word, which moves which letter
comes first (M5). P2 reverses the targets, which moves which target
comes first after the template's mask is left over from the one before
(M25).

Of the twenty-seven, ten were not kept. One is equivalent: the search
arm's lowest bit cleared by `rest & (rest - 1)` instead of `^`, which
peels the same bit. Nine fail as a kept one does: the template's
`break` dropped, as M1; the target itself taken as a start by the ★
arm, a start's own letter added again and the start itself listed by
the forward arm, and a letter not in the target taken away by the
struct, as M9; the ★ arm adding the letter rather than taking it away,
as M15; the sorted arm keeping the next letter twice, as M21; the
struct never trying z, as M11; and the template's first start dropped,
as M26.

## Verification

Every arm prints the same output as `words.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 8.6 s to 11.7 s and the
differential 1.6 s.

## Benchmarks

The bench builds 4 pairs of lists of 50000 words once, each word of 1 to
6 distinct letters from the first 12; then solves every pair 25 times,
one start word and one target word replaced by new ones before each
solve so that no solve repeats one before, with the ★ arm in all five
languages; C's set of start masks is an open-addressing table, since C
has none of its own. Every implementation prints `100 solves: 4168281
words in all, checksum 941192079`.

BENCHTAB
