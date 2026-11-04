# 1044. Longest Duplicate Substring

Given a string `s`, consider all *duplicated substrings*: (contiguous)
substrings of `s` that occur 2 or more times. The occurrences may
overlap.

Return **any** duplicated substring that has the longest possible
length. If `s` does not have a duplicated substring, the answer is `""`.

```
s = "banana"   ->  "ana"
s = "abcd"     ->  ""
```

**Constraints:** `2 <= s.length <= 3 * 10^4`; `s` consists of lowercase
English letters.

"Any" leaves the answer open when several substrings share the longest
length, as in `"abcabc"` with a different first letter. Every arm here
returns the same one, the smallest in dictionary order, so that their
outputs can be compared byte for byte.

## Approaches

Every arm but the diagonal one rests on one fact: if a substring of
length `len` occurs twice, so does its prefix of length `len - 1`. The
lengths that repeat therefore run from 0 up to the answer's, and a
binary search over `len` finds the longest.

| file | mechanism |
|---|---|
| `longest_dup.kara` ★ | the binary search, each length checked with a rolling polynomial hash (base 131, modulus `10^9 + 7`): a `Map[i64, Vec[i64]]` from each window's hash to the starts of the earlier windows with that hash, and a window whose bytes equal one of them repeats. O(n log n) expected |
| `longest_dup_suffix.kara` | a suffix array by prefix doubling, each pass a `sort_by_key` on the pair of ranks of a suffix's first `k` bytes and the `k` after, then Kasai's walk for each suffix's common prefix with the one before it. O(n log^2 n) |
| `longest_dup_set.kara` | the binary search, each length checked by putting every window, as a `String`, into a `Set[String]`. No hashing by hand and no collisions to rule out, at the price of copying every window |
| `longest_dup_diag.kara` | every distance `d` between two occurrences, one pass each comparing byte `i` with byte `i + d` and keeping the length of the run of matches. No search and no hashing. O(n^2) time, O(1) space |
| `longest_dup_iter.kara` | the binary search, each length one iterator chain: the windows collected into a `Vec[Str]` and sorted, then `windows.windows(2).iter().find(..)` for the first pair of equal neighbours |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 15 lines: the answers for ten strings,
LeetCode's two examples among them, with `"aa"` and `"ab"` (the
shortest, with and without an answer), `"aaaaa"` (overlapping
occurrences), `"abcabc"` and `"zxyzxyxyz"` (two answers of the longest
length, the smaller one returned), `"mississippi"` and
`"theeuntheeuntheeun"`; for every string of 2 to 12 letters from "ab"
and of 2 to 7 from "abc", the number of cases, the total length of the
answers and a checksum; the same for 300 random strings of 2 to 200
letters from 2 to 26; and the two largest, 5000 random letters (answer
`"agzm"`) and the first 5000 letters of the Fibonacci word, whose answer
is 2582 letters long. `longest_dup.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every length from the longest down, the windows of that
length that occur at two different starts, and the smallest of them;
the first length with one is the answer. It checks 4333 strings: every
string of 2 to 10 letters from "ab" (2044) and of 2 to 6 from "abc"
(1089), 1000 random strings of 2 to 16 letters from 2 to 5, and 200 of
17 to 300 letters from 2 to 26. The 4133 of at most 16 letters are also
read literally.

| | property |
|---|---|
| P1 | the answer is the statement read literally, on at most 16 letters |
| P2 | the answer occurs at least twice, or is `""` |
| P3 | no substring one letter longer occurs twice |
| P4 | the answer is the smallest repeated substring of its length |
| P5 | the string reversed gives an answer of the same length |
| P6 | each arm agrees with at least two of the other four |

The differential prints `4333 strings (4133 read literally): checksum
928696807, 128990 checks over 5 arms: 0 failures` under `karac
__mir-run` (15 s), `karac __mir-llvm-run` and `karac __mir-llvm-asan`
with no error, and the same line under `karac run` and from a `karac
build` binary. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Fifteen are kept, three to
each arm. All fifteen are killed, each fails the same way under both
backends, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first window that repeats kept, not the smallest | P1 644, P4 737, P6 737 |
| M2 | ★: the search goes on two lengths past one that repeats | P1 1737, P3 1827, P6 1827 |
| M3 | ★: `n - 1` never tried | P1 68, P3 68, P6 68 |
| M4 | suffix: a shorter suffix sorted after a longer one it starts | P1 127, P2 127, P4 127, P5 160, P6 127 |
| M5 | suffix: the doubling stops with two ranks still tied | P1 55, P2 58, P4 58, P5 31, P6 58 |
| M6 | suffix: every rank taken as distinct after one pass | P1 353, P2 24, P3 277, P4 217, P5 318, P6 410 |
| M7 | set: the last window skipped | P1 1575, P3 1256, P4 590, P5 1506, P6 1580 |
| M8 | set: the search skips the length below a miss | P1 1838, P3 1902, P6 1902 |
| M9 | set: no answer of one letter | P1 681, P3 686, P6 686 |
| M10 | diag: a run never reset on a mismatch | P1 2564, P2 2764, P4 2764, P6 2764 |
| M11 | diag: no repeats one letter apart (`d` from 2) | P1 1518, P3 1176, P4 427, P6 1526 |
| M12 | diag: no tie-break, the first run as long as the best kept | P1 622, P4 710, P6 710 |
| M13 | iter: the first pair of unequal neighbours | P1 4133, P2 4265, P3 68, P4 4265, P6 4333 |
| M14 | iter: windows sorted largest first | P1 1203, P4 1328, P6 1328 |
| M15 | iter: the first pair of neighbours skipped | P1 1413, P3 830, P4 791, P5 422, P6 1424 |

P1 and P6 kill all fifteen, P4 eleven, P3 nine, P5 five and P2 five.
P2 sees only edits that return a substring that does not repeat at all:
the suffix arm's broken order (M4 to M6) pairs suffixes that are not
neighbours, M10 counts a run across a mismatch, and M13 returns a
window that is there once. Every other wrong answer still repeats: it
is too short (P3), or the wrong one of its length (P4). P5 sees the
suffix arm's broken orders (M4 to M6), whose wrong pairings fall
differently on the reversed string, and two edits that lose a window
(M7, the last one) or a pair of them (M15, the first in sorted order),
which on the reversed string is a different one. An
edit that only picks the wrong one of the longest, such as M1, M12 and
M14, keeps the length and so passes P5. The checksum line folds the ★
arm's answers, so it moves only under edits to the ★ arm.

Fifteen other edits were set aside. One is equivalent: Kasai's loop
stopping one letter before the end of suffix `i`. Suffix `i` is
compared with `j`, the one before it in the order, and a common prefix
that reached the end of suffix `i` would make suffix `i` a prefix of
suffix `j` and so put it first, so the bound on `i` never stops the
loop. Ten fail exactly as a kept one does: the largest window of the
longest length kept, in the ★, suffix, set and diagonal arms (as M14);
the last window left out of the ★ and iterator arms, the set arm's
windows one byte short and the diagonal arm's last pair of each `d`
skipped (as M7); and the ★ arm's leading power one too high and the
set arm never keeping a first repeat, which fail alike (P1 4045, P3
4245, P6 4245). Two fail in ways of their own: the iterator arm missing
the last pair of neighbours (P1 799, P3 799, P5 412, P6 799) and its
search stopping one length early (P1 2001, P3 2082, P6 2082). Two panic
on a string slice out of range under both backends: Kasai carrying the
whole common prefix over to the next suffix, and the diagonal arm's run
starting one letter early.

## Verification

Every arm prints the same output as `longest_dup.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with
no error. `karac run` and a `karac build` binary print the same output
for every arm and the differential. `karac check --output=json` reports
nothing on any file. The runs used a release build of kara
`56fd1de206`, which has the fix below. Under `karac __mir-run` the arms take 1.5 s
(set) to 2.7 s (iterator), and 18 s for the diagonal arm, whose O(n^2)
pass over each of the two 5000-letter strings is 12.5 million byte
comparisons.

The arms went through the Mend loop, with `karac fix` supplying the
`ref` bindings (`Some(ref f) => window < f` in the set arm), the integer
casts and the `.to_string()` on the iterator arm's answer. Writing the iterator arm the way Rust does
turned up one gap, fixed in kara at `6ef646c141` (B-2026-11-04-51): Rust's
`windows.windows(2).find(..)`, with no `.iter()`, drew "no method
'find' on type 'Vec', did you mean 'fill'?" and no fix, where `map` or
`filter` called the same way get the `.iter()` hop as a fix. The
typechecker's list of iterator methods had drifted from the iterator
surface and lacked `find`, `position`, `nth`, `rev` and `flatten`; all
five now get the fix. One step remains open (B-2026-11-04-52): over a
`Vec[Vec[T]]`, `.iter().flatten()` is refused with the right spelling,
`.flat_map(|v| v.iter())`, in the message but not as a fix.

## Benchmarks

The bench builds 12 strings of 30000 letters once in all five
languages, drawn from the first 2, 4, 8 or 26 letters in turn, every
other one with a block of 3750 letters copied to a second place so that
its answer is long. It then runs the ★ arm over every string twice,
adding up the answers' lengths and folding each answer into a checksum.
Every implementation prints `12 strings of 30000 letters, 2 rounds:
total length 45244, checksum 819661520`. Doubling the rounds doubles
C's time (0.58 to 0.63 s against 0.28 to 0.31 s), so no compiler hoists
the search out of the round loop. Each round is about 15 lengths tried
on each string, each a pass of 30000 windows through a hash table, some
5 million lookups in all.

The table is where the implementations part ways. Kāra, Rust and Go
each use their standard hash map, keyed by the window's hash, with a
growable list of starts for each key, as the ★ arm does. C has no
standard map, so its mirror chains the starts through flat arrays
sized once per length and spreads the keys with one multiply, with no
allocation per key and no keyed hash function. The C row is that
hand-built table as much as the compiler.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.241 to 0.367 s | 0.270 s |
| Kāra (`karac build`) | 0.891 to 1.133 s | 1.072 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.929 to 1.247 s | 1.127 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.980 to 1.363 s | 1.176 s |
| Rust (`rustc -O`) | 1.071 to 1.421 s | 1.194 s |
| Go | 1.579 to 1.753 s | 1.659 s |
| Python | 4.7 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
`KARAC_AUTO_PAR_DEBUG=1` reports every loop kept in order, and its user
time (1.05 s) matches its real time.

Kāra took 0.96 times Rust's median time under overflow checks, and 4.2
times C's. Python took 4.2 times Kāra's, closer than on most katas; its
dictionary, the bulk of the work here, is written in C.
