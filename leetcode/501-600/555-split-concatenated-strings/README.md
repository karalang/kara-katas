# 555. Split Concatenated Strings

You are given an array of strings `strs`. You could concatenate these
strings together into a loop, where for each string, you could choose to
reverse it or not. Among all the possible loops, return the
lexicographically largest string after cutting the loop, which will make
the looped string into a regular one. Specifically, to find the
lexicographically largest string, you need to experience two phases:
concatenate all the strings into a loop, where you can reverse some
strings or not and connect them in the same order as given; then cut and
make one breakpoint in any place of the loop, which will make the looped
string into a regular one starting from the character at the cutpoint.
Your job is to find the lexicographically largest one among all the
possible regular strings.

```
strs = ["abc", "xyz"]  ->  "zyxcba"
strs = ["abc"]         ->  "cba"
```

**Constraints:** `1 <= strs.length <= 1000`, `1 <= strs[i].length <=
1000`, `1 <= sum(strs[i].length) <= 1000`, and `strs[i]` consists of
lowercase English letters.

## Approaches

Every arm is `fn split_loop(strs: Vec[String]) -> String`. The cut falls
inside some string i, read one way or the other. The rest of the loop is
then read from string i + 1 round to i - 1, and each of those strings
sits whole in the middle of the answer, so each is best turned whichever
way is larger. Every arm turns each string its larger way first, then
tries every string, both ways, cut at every place, with the rest of the
loop between the two parts. That is O(L^2) for L letters in all.

| file | mechanism |
|---|---|
| `split_concatenated_strings.kara` ★ | `String`s throughout; each candidate is `f"{t[k..]}{middle}{t[..k]}"`, compared with `>` |
| `split_concatenated_strings_bytes.kara` | every string a `Vec[u8]`, each candidate built with `extend_from_slice` and compared as a vector with `>` |
| `split_concatenated_strings_peak.kara` | the ★ arm, but only cuts just before the largest letter anywhere are built, since the answer must start with it |
| `split_concatenated_strings_chain.kara` | every string a `Vec[char]`, each candidate collected from `t[k..].iter().chain(middle.iter()).chain(t[..k].iter())` |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 11 lines: the two examples, five small lists
(one letter, equal strings, strings that are each other's reverse), a
checksum over 300 random lists, and three lists of 1,000 letters, the
problem's most: 1,000 strings of one letter, one string of 1,000, and
100 strings of 10 from `a` and `b`. `split_concatenated_strings.py`
mirrors the ★ arm and its output is byte-identical.

The bytes and chain arms compare two vectors with `>`, which design.md
allows (`impl[T: Ord] Ord for Vec[T]`). Every backend refused it at type
checking ("type 'Vec[u8]' does not implement PartialOrd") until kara
B-2026-10-06-92 was fixed in `d3f7020d95`; the arms kept that spelling,
and now run as written.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: every way to turn the strings (2^n of
them), each loop cut at every place, the largest string kept. Each arm
is held to the properties below on 1,000 random lists of 1 to 5 strings
of 1 to 4 letters, from the first 2, 3 or 26 letters in turn.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the answer has the same letters as the strings |
| P3 | the answer is at least the strings joined as given |
| P4 | the list started one string later gives the same answer |
| P5 | every string read backwards gives the same answer |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`. It builds the reversed list with
`flipped.push(s.chars().rev().collect())`, which those three take and
`karac check` refuses ("expected 'String', found 'Vec[char]'", kara
B-2026-10-12-33, open). Until B-2026-10-06-92 was fixed, its copies of
the bytes and chain arms' `>` on vectors stopped it at type checking
everywhere, and a copy comparing through a hand-written function was
checked instead.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed. They were first run on the copy
that compares through a function, while B-2026-10-06-92 was open, and
run again on the differential as written once it was fixed, with the
same counts; E2, which edited the copy's function, now turns the bytes
arm's own `candidate > answer` into `>=`.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the strings in the middle left as given, not turned | P1 362, P5 548 |
| M2 | ★: the cut string read forwards only | P1 275, P5 555 |
| M3 | bytes: the middle read round the other way | P1 462, P3 19 |
| M4 | bytes: the part before the cut written first as well | P1 974, P2 974, P3 105 |
| M5 | peak: the largest letter assumed to be `z` | P1 923, P2 923, P3 923 |
| M6 | peak: the smallest letter kept, not the largest | P1 967, P2 324, P3 716 |
| M7 | chain: the part before the cut left off | P1 566, P2 534 |
| M8 | chain: every string turned its smaller way | P1 556, P3 44 |
| E1 | ★: a tie taken as well | 0 |
| E2 | bytes: equal byte strings counted as greater | 0 |
| E3 | peak: a string turned on a tie as well | 0 |
| E4 | chain: the last two parts chained first | 0 |

P5 sees M1 and M2 more often than P1 does: both depend on which way each
string was given, which is exactly what P5 changes and the right answer
does not depend on. M5 cuts nowhere unless some string holds a `z`, and
so answers an empty string on the 923 lists without one; M6 likewise
when no string holds an `a`. P2 sees every mutant that loses or repeats
letters (M4, M7 and the empty answers). P4 sees none: every arm already
treats the list as a loop, and none of these edits changes where it
starts. The four E mutants change only which of two equal strings is
kept, or how a chain is grouped.

## Verification

Every arm prints the same output as `split_concatenated_strings.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. The differential prints its line under all three. `karac check`
passes all four arms and the bench program, and refuses the differential
on B-2026-10-12-33 (above). The bytes and chain arms and the
differential were rechecked at kara `83fab1e1e8` (debug build) and
`f5c72b653e` (release build, for `check` and `__mir-run`), which differ
in no `src` or `runtime` file, after B-2026-10-06-92 was fixed; until
then they stopped at type checking, and copies comparing through a
function were checked instead.

The frozen legacy backends: the ★ and peak arms print the same output
under `karac run --interp`, and fail under `karac run` and `karac
build`, whose codegen does not take `s.chars().rev().collect()`
("`Iterator.rev()` is not yet supported ... for this chain shape"). The
bytes and chain arms stop at type checking there, at `>` on two vectors
(the fix for B-2026-10-06-92 is on the v2 pipelines only), the chain arm
also on `*c` over a `Vec[char]`'s `iter()`. Legacy is frozen, so these
are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 random lists once, each
of 1,000 letters in all (the problem's most) in strings of 1 to
40 letters from the first 2 to 26; then 30 times over every list is
answered, and the length of each answer and its first and middle bytes
go into a checksum. Every implementation prints `100 lists,
4934 strings, 30 rounds each: checksum 705967510`, the Kāra program
under `karac __mir-run` included (35.8 s).

Each implementation builds every candidate as a fresh string of the
three parts: `format!` in Rust, `+` in Go and Python, and in C a
`malloc`'d buffer filled with three `memcpy`s, then compared with the
best so far and kept or freed. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine). The compiled rows were timed again together, with the
compiler at kara `7609de871d`, once B-2026-10-14-5 was fixed; Python's
is the first timing:

| | time |
|---|---|
| C (`clang -O3`) | 0.21 to 0.24 s |
| Rust (`rustc -O`) | 1.21 to 1.26 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.05 to 1.21 s |
| Go | 2.84 to 3.01 s |
| Python | 2.37 to 2.44 s |
| Kāra (`karac build --mir`) | 0.52 to 0.63 s |

The legacy `karac build` refuses this program: it moves `lists[(round *
7 + g) % count]` out of the index (E_INDEX_MOVE_NON_COPY) where
v2 borrows it. So `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 12.0 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

The Kāra row was about 4x Rust's at first (5.18 to 5.96 s at kara
`af2123abc5`), and the f-string was why (kara B-2026-10-14-5, filed
from this kata): the v2 backend's f-string checked each `String` hole as
UTF-8 again and copied the whole result twice. Built instead with three
`push_str` into a `String.new()`, the same program ran in 0.97 to
1.10 s. The bench kept the f-string, the natural spelling. Since the
fix (kara `fdb1d5fc22` and `5a4a35bb58`), an f-string made only of text
is summed, allocated once and copied into, so the Kāra row is now about
half of Rust's `format!` and two and a half times C's.

## Compiler findings

| id | status | what |
|---|---|---|
| B-2026-10-14-5 | fixed (`fdb1d5fc22`, `5a4a35bb58`), filed from this kata | an f-string with `String` holes was about 5x three `push_str` on `karac build --mir`; the bench program's Kāra row, re-timed above |
| B-2026-10-06-92 | fixed (`d3f7020d95`) | `>` on two `Vec`s was refused at type checking though design.md declares `Ord` for `Vec[T]`; the bytes and chain arms and the differential now run as written |
| B-2026-10-12-33 | open | `karac check` refuses `v.push(cs.iter().collect())` into a `Vec[String]`; the differential |

Recheck the differential under `karac check` once B-2026-10-12-33 is
fixed.
