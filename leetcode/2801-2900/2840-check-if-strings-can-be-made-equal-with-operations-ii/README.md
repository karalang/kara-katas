# 2840. Check if Strings Can be Made Equal With Operations II

You are given two strings `s1` and `s2`, both of length `n`, consisting
of **lowercase** English letters.

You can apply the following operation on **any** of the two strings
**any** number of times:

- Choose any two indices `i` and `j` such that `i < j` and the
  difference `j - i` is **even**, then **swap** the two characters at
  those indices in the string.

Return `true` *if you can make the strings* `s1` *and* `s2` *equal, and*
`false` *otherwise*.

```
s1 = "abcdba", s2 = "cabdab"  ->  true
s1 = "abe", s2 = "bea"        ->  false
```

**Constraints:** `n == s1.length == s2.length`; `1 <= n <= 10^5`; `s1`
and `s2` consist only of lowercase English letters.

## Approaches

| file | mechanism |
|---|---|
| `strings.kara` ★ | a swap an even distance apart keeps every letter on places of its parity, and any order of those places can be reached, so the strings match when each parity holds the same letters: counts in one table of 2 x 26 over the two strings `zip`ped, s1 up and s2 down, all back to zero |
| `strings_sorted.kara` | each string's even and odd letters pulled out with `step_by` and `skip`, each half sorted, and the `(Vec[u8], Vec[u8])` pairs compared |
| `strings_map.kara` | a `Map` keyed by (parity, letter) through `entry().or_insert()`: s1's letters counted in, s2's counted out, an entry removed when it reaches zero, a letter missing failing at once, and the map empty at the end |
| `strings_swaps.kara` | the operations made: for each place in turn, a letter of s2's kind looked for at a later place of the same parity in s1 and swapped in; O(n^2), for the harness's lengths |
| `strings_solution.kara` | a Rust solution as LeetCode's Rust users write it: a `[[0i32; 26]; 2]` of counts indexed by `i & 1` and `(c - b'a') as usize` over `bytes().enumerate()` of both strings, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's two examples and one
letter against itself and against another; 10^5 letters, LeetCode's
most, against themselves reversed, and 99999 likewise, equal for an odd
length; then 3000 random pairs of 1 to 8 letters over a, b and c, and
300 of up to 2000 over all 26, a third random, a third the first
shuffled within its parities and a third that with one letter changed,
as counts and checksums. `strings.py` mirrors the ★ arm and its output
is byte-identical.

```
true false true false
false true
3000 short pairs: 1429 true, checksum 108433513
300 long pairs: 104 true, checksum 388883059
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every string s1 reaches by swaps an even distance
apart, found by a search to a fixed point over a `Set[String]`, and
whether s2 is among them. It draws 2000 pairs of 1 to 6 letters over a,
b and c, then 50 of up to 1000 over all 26, the second strings made as
the harness's are, all before any arm answers; the literal reading is
asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 6 letters, the answer is the literal reading's |
| P2 | s1 and s2 the other way round: the same answer |
| P3 | s1 against itself: true |
| P4 | every letter of both moved on one, z to a: the same answer |
| P5 | both strings reversed: the same answer |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, 951 true: checksum 751042989,
61500 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python reading of the same cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Nine are killed, each the same
way under both backends. M5 survives and is equivalent: the strings are
the same length, so a letter of s2 with nothing left to match leaves
some count of s1's unspent, and the map is not empty at the end.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one table for both parities | P1 34, P6 34 |
| M2 | ★: s2 counted up too | P1 935, P3 2050, P6 951 |
| M3 | sorted: the odd letters left unsorted | P1 218, P5 156, P6 234 |
| M4 | sorted: the odd letters taken from the start | P1 247, P5 330, P6 256 |
| M5 | map: a letter of s2 not in the map let pass | survives: equivalent (above) |
| M6 | map: keyed by letter alone | P1 780, P3 1740, P6 796 |
| M7 | swaps: a letter looked for at any distance | P1 34, P6 34 |
| M8 | swaps: the last place never looked at | P1 240, P5 230, P6 256 |
| M9 | solution: the parity read from the letter | P1 826, P2 4, P3 1807, P4 305, P5 102, P6 842 |
| M10 | solution: only the even row checked | P1 247, P5 330, P6 256 |

## Benchmarks

The bench draws 200 pairs of 10^5 letters, LeetCode's most, the second
the first shuffled within its parities and, for half of them, one
letter changed, all of them first, then answers each 20 times by the ★
arm in all five languages. Every implementation prints `200 pairs of
100000, 20 rounds: 2060 true, checksum 425263933`.

BENCHTAB

## Verification

All five arms print the same output as `strings.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The harness, as first written, passed `text(long.clone())`, and `karac
check` reported `redundant_clone`, "`long.clone()` copies `long` for a
parameter that only borrows it"; `karac fix` passed `long`. The four
own arms checked clean.

LeetCode's Rust template took 7 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`;
`bytes().enumerate()` took `.iter()` twice, Kāra's `bytes()` being a
`Vec[u8]`; `|&x|` lost its `&`; `&str` became `Str`, and `Solution::`
took `.`. The `[[0i32; 26]; 2]`, its suffix not the default, and the
`(c - b'a') as usize` index were accepted as written.
