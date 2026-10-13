# 516. Longest Palindromic Subsequence

Given a string `s`, find the longest palindromic subsequence's length
in `s`.

A subsequence is a sequence that can be derived from another sequence
by deleting some or no elements without changing the order of the
remaining elements.

```
s = "bbbab"  ->  4    ("bbbb")
s = "cbbd"   ->  2    ("bb")
```

**Constraints:** `1 <= s.length <= 1000`; `s` consists only of
lowercase English letters.

## Approaches

Every arm is `fn longest_palindrome_subseq(s: Str) -> i64` and reads the
string through `.bytes()`.

| file | mechanism |
|---|---|
| `longest_palindrome_subseq.kara` ★ | a table over substrings: `best[i][j]` for `s[i..=j]` is the inside's plus 2 when the ends are equal, else the better of dropping either end; filled from the last i back. O(n^2) time and space |
| `longest_palindrome_subseq_memo.kara` | the same recurrence top-down on (i, j), each answer kept in a `Vec[Vec[Option[i64]]]`, `None` for not yet worked out, that goes down the recursion as `mut ref`. O(n^2) |
| `longest_palindrome_subseq_rolling.kara` | the table's row i reads only row i + 1, so only two rows are kept and exchanged after each i with `mem.swap(mut row, mut next)`. O(n^2) time, O(n) space |
| `longest_palindrome_subseq_lcs.kara` | the longest common subsequence of the string and its reverse (`to_vec`, `reverse`), which is always as long as the longest palindromic subsequence; the classic table over prefixes. O(n^2) |
| `differential.kara` | the four arms on 1,500 random strings, five properties |

Every arm prints the same 8 lines: the two LeetCode examples, one
letter, no letter repeated, a palindrome, `"character"`, a 31-letter
palindrome, and for 300 random strings of 1 to 80 letters (from the
first 2, 5 or 26 in turn) the total and a checksum.
`longest_palindrome_subseq.py` mirrors the ★ arm and its output is
byte-identical.

The two-rows arm exchanges its rows with `mem.swap`, the spelling
core-semantics.md §3.7 and design.md give. No checker or backend
resolves it (kara B-2026-10-13-25, below): `karac check` and every
backend refuse the arm, and the differential, which holds a copy of
it. So every check of that arm and of the differential below was run
on copies that write `swap(mut row, mut next)`, the bare name the
implementation has, the only change. The files here keep `mem.swap`,
and should pass as they stand once the row is fixed.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random strings of 1 to 10 letters from the first 2, 3 or 26 in
turn.

| | property |
|---|---|
| P1 | the answer is the reference's: every subsequence, one bit of a mask per letter, the longest that reads the same both ways |
| P2 | the string backwards has the same answer |
| P3 | renaming the letters, a for z, b for y and so on, changes nothing |
| P4 | the string followed by itself backwards, a palindrome, gives twice its length |
| P5 | the answer is at least the most frequent letter's count and at most the length |

The copy described under Approaches prints `1500 cases, 4 arms, 30000
checks, 0 failures` under `karac __mir-run`.

## Mutation testing

Twelve edits to that copy of `differential.kara`, two to each arm that
change its answers, and four that do not, each run under `karac
__mir-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: equal ends add 1, not 2 | P1 1064, P4 1500, P5 743 |
| M2 | ★: unequal ends drop only the first | P1 443, P2 618, P5 305 |
| M3 | memo: one letter counts 0 | P1 1040, P5 610 |
| M4 | memo: equal ends keep the last letter inside, `(i + 1, j)` | P1 837, P2 157, P4 1500, P5 469 |
| M5 | two rows: the rows never exchanged | P1 1500, P4 1500, P5 1500 |
| M6 | two rows: unequal ends read `next[j - 1]`, not `next[j]` | P1 331, P2 604, P5 181 |
| M7 | lcs: the copy never reversed | P1 1199 |
| M8 | lcs: a match adds 2 | P1 1500, P4 1500, P5 984 |
| E1 | ★: the table one larger each way | 0 |
| E2 | memo: the table one larger each way | 0 |
| E3 | two rows: the first row one longer | 0 |
| E4 | lcs: the answer also takes the cell above's, `.max(common[n - 1][n])` | 0 |

E1 to E3 only add cells nothing reads. E4 holds because the table
never falls going down a column, so the cell above is never larger.

M7 compares the string with itself, so its answer is always the
length: that is symmetric, unmoved by renaming, right for the
doubled-back string and inside P5's bounds, so only the reference sees
it. M3 loses the middle letter of every odd-length palindrome, which
the doubled-back string, an even one, never has. M2 and M6 lean to one
end of the string, and P2, which turns it round, sees them. M5 never
fills the row it reads and answers 0 for every string.

## Verification

The ★, memo and lcs arms print the same output as
`longest_palindrome_subseq.py` under `karac __mir-run` (the v2 MIR
interpreter) and `karac __mir-llvm-run`, and run clean under `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer): output
identical, no error, no leak. So do the copies of the two-rows arm and
the differential described under Approaches; the differential copy
prints `30000 checks, 0 failures` on the first two and runs clean
under the third. `karac check` passes on the ★, memo and lcs arms, the
two copies and the bench program, and refuses the two-rows arm and the
differential as written (see Compiler findings).

On the frozen legacy backends, `karac run --interp` prints the same
output for the ★, memo and lcs arms and the copy of the two-rows arm.
LLJIT and legacy `karac build` fail on all of them at codegen: "no
handler for method 'bytes'" on a `Str`. Legacy refuses the copy of the
differential at type checking, since it types the items of a `for`
over `.bytes()` and over a `Vec`'s `iter()` by value and so refuses
the `*b` and `*k` reads. Legacy is frozen, so these are noted, not
filed.

## Benchmarks

The bench program uses the ★ arm. It builds 120 random strings of
1,000 letters (the problem's most), from the first 4 or all 26 in
turn, and solves each once. Every implementation prints `120 strings
of 1000 letters: 58332 in all, checksum 949952459`, the Kāra program
under `karac __mir-run` included (in 79 s).

Every mirror builds a fresh n by n table for every call, as the ★ arm
does with `vec![vec![0; n]; n]`: Rust a `Vec` of `Vec`s, Go a slice of
slices, Python a list of lists, and C an array of `calloc`'d rows.
Spot timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.42 to 0.51 s |
| Rust (`rustc -O`) | 0.45 to 0.51 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.44 to 0.51 s |
| Go | 0.42 to 0.43 s |
| Python | 10.9 to 11.2 s |
| Kāra (`karac build --mir`) | 0.18 to 0.22 s |

The legacy `karac build` refuses this program ("no handler for method
'bytes'", see Verification). So `bench.sh` builds the Kāra program with
`karac build --mir`, the v2 compiled backend. That edit is by hand, on
top of the `scripts/new-bench.sh` output. The `--mir` row is timed at kara `e85c10e377`. Under
`karac __mir-llvm-run` the program prints the same line in 1.8 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

kara B-2026-10-13-25 (missing-feature, open): `mem.swap(a, b)`,
`mem.replace(d, v)` and `mem.take(d)`, the spelling core-semantics.md
§3.7 and design.md give for moving values out of places, do not
resolve: `karac check` and every backend stop at "undefined name
'mem'". The implementation has them only as the bare prelude
functions `swap`, `replace` and `take`, and `import std.mem` is an
unknown module. With the prefix dropped the two-rows arm and the
differential pass `karac check` and run right on both v2 backends.
