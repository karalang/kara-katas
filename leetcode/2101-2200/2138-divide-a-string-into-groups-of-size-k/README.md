# 2138. Divide a String Into Groups of Size k

A string `s` can be partitioned into groups of size `k` using the
following procedure:

- The first group consists of the first `k` characters of the string,
  the second group consists of the next `k` characters of the string,
  and so on. Each character can be a part of **exactly one** group.
- For the last group, if the string **does not** have `k` characters
  remaining, a character `fill` is used to complete the group.

Note that the partition is done so that after removing the `fill`
character from the last group (if it exists) and concatenating all the
groups in order, the resultant string should be `s`.

Given the string `s`, the size of each group `k` and the character
`fill`, return *a string array denoting the **composition of every
group** `s` has been divided into, using the above procedure*.

```
s = "abcdefghi", k = 3, fill = "x"     ->  ["abc","def","ghi"]
s = "abcdefghij", k = 3, fill = "x"    ->  ["abc","def","ghi","jxx"]
```

**Constraints:** `1 <= s.length <= 100`; `s` consists of lowercase
English letters only; `1 <= k <= 100`; `fill` is a lowercase English
letter.

The groups start every k letters; each is the slice from its start to k
on or to the end, and only the last can be short, made up with the
fill. O(n + k).

## Approaches

| file | mechanism |
|---|---|
| `divide.kara` ★ | a slice every k letters, `s[start..(start + k).min(n)]`, the last made up with the fill by `push` |
| `divide_padded.kara` | the string made up with the fill to a whole number of groups first, so every group is the same plain slice, collected by `map` over the group numbers |
| `divide_chunks.kara` | the letters as a `Vec[char]` cut by `chunks(k)`, which gives a `Vec` of slices, so `into_iter()` before `map`; each chunk collected into a `String` |
| `divide_struct.kara` | a `struct Grouper` fed one letter at a time by `add` (`mut ref self`), closing its open group when full; `finish` (`own self`) makes up the last and hands over the groups |
| `divide_fold.kara` | one `fold` over the letters carrying the pair (groups closed, group open), its closure taking a tuple pattern and handing the owned pair on; the binding `let mut (groups, open)` |
| `divide_solution.kara` | LeetCode's Rust template: `collect::<Vec<char>>()`, `chunks`, `k as usize`; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(groups of one, one group longer than the string, one group exactly the
string, and a fill that is also a letter of the string), each with its
groups; then the count of groups and a checksum over 2000 random strings
of 1 to 20 letters from the first 2, 5 or 26 in turn, k of 1 to 8 and a
random fill; then the constraints' largest, 100 letters in groups of 1,
7 and 100. `divide.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in four rounds of 9, 2, 1 and 1 edits:
Rust's spellings (`Vec<..>` to `Vec[..]`, `s.chars().collect::<Vec<char>>()`
to `Vec[char].from_iter(s.chars())`, `struct Solution;` to `struct
Solution {}`, the adapter's `&String` to `ref String`, `Solution::` to
`.`); then `k as usize` to `k as i64`, since Kāra's lengths are `i64`,
and the `into_iter()` that the `Vec` from `chunks` needs before `map`;
then the `ref` dropped from the adapter's parameter, which borrows
already; then the adapter's `s.clone()` dropped, which the template's
borrowing parameter never needed (the `redundant_clone` lint, karac
B-2026-11-14-3). The template writes `s.chars()` on one line and
`.collect::<Vec<char>>()` on the next, and the fix-it first closed
`from_iter(` on a line of its own after the break, leaving a lone `)`
for the next round; fixed in karac 200ca97370, which closes it where the
receiver ends.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: there are as many groups as k goes into the length, rounded
up, and the j-th letter of group g is the letter at g k + j, or the fill
when there is none; no slice is cut and no group is grown. It checks
300 random strings of 1 to 12 letters from the first 2, 3 or 26 in
turn, k of 1 to 6 and a random fill; then 30 whose length k divides;
then 30 with k longer than the string. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the groups are the statement read literally |
| P2 | the groups joined are the string, then fills, to a whole number of k |
| P3 | every group is k letters long |
| P4 | the string cut to its whole groups: the same groups but the last when it was short |
| P5 | k the string's length: one group, the string itself |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 strings: checksum 726067075, 12960
checks over 6 arms: 0 failures` under every lane in Verification; the
checksum of the literal groups was checked against a Python reading of
the same strings. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Twenty-six edits to the differential, four to five to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: each slice one letter short | P1 282, P2 282, P5 343, P6 282 |
| M3 | ★: the last group made up one short | P1 185, P2 185, P3 185, P6 185 |
| M5 | ★: a letter skipped between groups | P1 236, P2 236, P4 49, P6 236 |
| M6 | padded: a single fill | P1 119, P2 119, P6 119 |
| M8 | padded: the groups overlapping | P1 181, P2 181, P6 181 |
| M9 | padded: made up with the first letter | P1 176, P2 176, P6 176 |
| M11 | chunks: a short chunk made up with one fill | P1 119, P2 119, P3 119, P6 119 |
| M12 | chunks: each chunk reversed | P1 240, P2 240, P5 292, P6 240 |
| M13 | chunks: the chunks of the letters reversed | P1 292, P2 292, P4 110, P5 292, P6 292 |
| M14 | grouper: a group closed one letter early | P1 302, P2 197, P3 302, P4 226, P5 329, P6 302 |
| M15 | grouper: a last group of one letter dropped | P1 73, P2 73, P6 73 |
| M17 | grouper: the open group never cleared | P1 289, P2 289, P3 236, P4 167, P5 360, P6 289 |
| M19 | fold: a group closed at k + 1 | P1 236, P2 167, P3 236, P4 113, P6 236 |
| M20 | fold: the open group never pushed | P1 185, P2 185, P6 185 |
| M21 | fold: made up with `'a'` | P1 178, P2 178, P6 178 |
| M23 | solution: the template's groups made up past k | P1 360, P2 360, P3 360, P5 360, P6 360 |
| M24 | solution: the adapter passing k - 1 | P1 297, P2 226, P3 297, P4 226, P5 329, P6 297 |

P1, P2 and P6 kill all seventeen, P3 seven, P5 seven and P4 six. P2
joins the groups and asks for the string made up with fills, which any
lost, moved, doubled or wrong letter breaks, so it sees every edit P1
does; it counts fewer only for groups cut at the wrong size, whose
letters can still join to the right string (M14, M19, M24). P3 asks
every group for k letters; it sees an edit that leaves one too short or
too long: the last made up one short or with a single fill (M3, M11),
groups cut at the wrong size (M14, M19, M24), a group never cleared
(M17), or made up past k (M23). P5 sets k to the length, so the answer
is the string whole; it sees an edit that changes a full group: a slice
one short (M2), a chunk or the letters reversed (M12, M13), a group
closed early or never cleared (M14, M17), made up past k (M23), or k
less one (M24). P4 cuts the string to its whole groups, which keeps
them as they were; it sees an edit that ties a group to where the
string ends: a letter skipped between groups (M5), the letters reversed
(M13), groups cut at the wrong size (M14, M19, M24), and a group never
cleared (M17).

Of the twenty-six, nine were not kept. None is equivalent and none
fails by a crash. Six fail as a kept one does: the ★ arm's short last
group dropped, the padded arm's groups counted on the string, and the
fold arm's open group pushed only when full, as M20; the ★ arm's last
group never made up and the grouper's one fill too many, as M3; and the
chunks arm's chunks of k + 1, as M19. Three are killed with checks of
their own but were left out because their arms keep their share: the
grouper's open group dropped when closed (P1 289, P2 289, P4 114, P5
360, P6 289), and the adapter passing `'x'` for the fill (P1 180, P2
180, P6 180) and dropping the last letter (P1 319, P2 319, P4 109, P5
314, P6 319).

## Verification

Every arm prints the same output as `divide.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.2 s to 0.4 s and the
differential 0.5 s.

## Benchmarks

The bench builds 1000 strings of 100 letters once; then solves each 100
times, one letter redrawn and k and the fill drawn anew before each
solve so that no solve repeats one before, 100000 solves in all, with
the ★ arm in all five languages. Every implementation prints `100000
solves: 569422 groups, checksum 390727161`.

BENCHTAB
