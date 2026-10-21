# 833. Find And Replace in String

Given a string `s` and `k` replacement operations as three lists
`indices`, `sources` and `targets` of length `k`, perform them all and
return the result. Operation `i` checks whether `sources[i]` occurs at
index `indices[i]` of the original string; if it does not, nothing
happens, and if it does, that occurrence is replaced by `targets[i]`.
All the replacements happen at the same time, so none moves the indices
of another, and the test cases are made so that the replacements do not
overlap.

```
s = "abcd", indices = [0,2], sources = ["a","cd"], targets = ["eee","ffff"]  ->  "eeebffff"
s = "abcd", indices = [0,2], sources = ["ab","ec"], targets = ["eee","ffff"] ->  "eeecd"
```

**Constraints:** `1 <= s.length <= 1000`, `1 <= k <= 100`, `0 <=
indices[i] < s.length`, `1 <= sources[i].length, targets[i].length <=
50`, and every letter is a lowercase English letter.

## Approaches

Every arm finds the operations whose source occurs at their index in the
original string; they differ in how they record those and build the
answer.

| file | mechanism |
|---|---|
| `find_replace_string.kara` ★ | a table by index: each matching operation is recorded at its index, and one walk over the string writes a recorded operation's target and skips its source, or copies the letter. O(n + total source length) |
| `find_replace_string_splice.kara` | right to left: the operations ordered by index, last first, and each matching one spliced into a copy of the string. Working from the right, a splice never moves a stretch a later operation looks at. O(k log k + k n) |
| `find_replace_string_iter.kara` | an iterator chain: the three lists `zip`ped into triples, the matching ones kept with `filter`, `collect`ed and sorted by index, then a cursor copying the letters between matches in slices. O(k log k + n) |
| `find_replace_string_chars.kara` | letter by letter: the string and each source taken apart into `char`s and compared one by one, the source not running past the end, with a table of `Option`s by index as in the ★ arm. O(n + total source length) |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 12 lines: LeetCode's two examples; eight more
(three operations given out of order, a one-letter string replaced and
left alone, a source running past the end, operations at both ends given
last first, a source that is the whole string, a source that would match
only after another operation's replacement, and two operations at one
index of which one matches); a string of LeetCode's greatest length,
1000, with 100 operations, shown by its answer's length and a checksum;
and 300 random cases with their total length and a checksum. In those,
two in three sources are the stretch of the string at their index and
the third has its last letter changed, and the operations come in a
shuffled order. `find_replace_string.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: at each position every operation is looked at, and one whose
source occurs at its index there puts its target in place of the source;
a position no operation starts at keeps its letter. Its 1,600 cases come
in four kinds of 400: strings of 1 to 8 letters, where sources reach the
ends and some run past them; strings up to 300 letters with up to
LeetCode's 100 operations; sources up to LeetCode's 50 letters; and
strings of one letter with the operations side by side. The first and
last kinds add operations at any index, an index already used included,
whose source crosses the other operations' stretches and holds a letter
the string does not, so that it never matches while the targets may hold
that letter.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the operations in the opposite order give the same answer |
| P3 | every target set to its own source gives back the string |
| P4 | the operations that do not match left out give the same answer |
| P5 | the answer's length is the string's, less each matching source's, plus its target's |

It prints `1600 cases, 32000 checks over 4 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the source looked for one letter late | P1 1311, P3 224, P4 223, P5 1228 |
| M2 | ★: one letter skipped after a target, not the source | P1 1335, P3 1335, P5 1335 |
| M3 | ★: an operation that does not match clearing its index | P1 331, P2 436, P4 331, P5 292 |
| M4 | splice: the source looked for in the spliced string | P1 21, P2 17, P4 21, P5 18 |
| M5 | splice: the source's last letter kept | P1 1457, P3 1457, P5 1457 |
| M6 | splice: the target put after the source | P1 1457, P3 1457, P5 1457 |
| M7 | iter: the letters after the last match dropped | P1 863, P3 863, P5 863 |
| M8 | iter: the cursor left at the match | P1 1457, P3 1457, P5 1457 |
| M9 | iter: each source paired with the next operation's target | P1 1456, P2 1410, P3 1346, P4 1249, P5 1362 |
| M10 | chars: a source running past the end matched by its part inside | P1 172, P3 172, P4 172, P5 139 |
| M11 | chars: the source's last letter not compared | P1 1380, P2 454, P3 1384, P4 1380, P5 1293 |
| M12 | chars: the target written backwards | P1 1413, P3 859 |

P1 kills all twelve. P2, the order of the operations, sees only the
edits that let one operation undo or depend on another: M3, where a
source that does not match wipes out a match at the same index, M4,
where a splice to the right makes a source match that did not, M9 and
M11. Every arm is otherwise free of the order by construction. P3 is
blind to M3 and M4, because every source matches its own index once the
targets are the sources, and P4 is blind to every edit that only
misplaces letters around a match. P5 counts letters, so it does not see
M12, which keeps every letter and writes them backwards. M4 is the
weakest kill: it needs a source that does not match to sit across a
stretch that a splice to its right changes into it, which only the first
and last kinds of case build, and 77 checks fail. Before those kinds
added such sources, it survived all 1,600 cases.

## Verification

Every arm prints the same output as `find_replace_string.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `cd64cc58b3`, and the runtime archives are
current with them. Under `karac __mir-run` each arm takes 0.2 to 0.4 s
and the differential 7.5 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends do not run this kata. The legacy interpreter
(`karac run --interp`) prints the eight fixed cases right and then the
wrong length and checksum for the random ones, for the ★, splice and
iterator arms alike: the harness passes `mut seed` to `random_word`
alongside a `next_random(mut seed)` argument, and the legacy interpreter
writes the parameter's copy back over the inner call's update. A
two-line program, `take(mut s, bump(mut s))`, prints `22 22` on v2 and
`12 12` on legacy. Legacy refuses the letter-by-letter arm, the
differential and the bench program as moving a `String` out of an index,
which v2's borrowing parameters do not do, and its compiled backends
refuse the harness's `Iterator.last()` over bytes and the iterator arm's
`collect`. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
cases once, each a string of LeetCode's greatest length, 1000, of the
letters a and b, with LeetCode's greatest number of operations, 100, on
disjoint stretches of 1 to 10 letters with 0 to 3 letters between them,
in a shuffled order; two in three sources match and each target is 1 to
7 letters. Each of 300,000 rounds runs the next case and reads one
letter of the answer. Every implementation prints `300000 rounds of 64
cases: 269958008 letters, checksum 150959203`, the Kāra program under
`karac __mir-run` included, in 260 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.96 to 1.17 s |
| Rust (`rustc -O`) | 1.20 to 1.45 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.16 to 1.44 s |
| Go | 2.70 to 3.31 s |
| Python | 16.9 to 17.8 s |
| Kāra (`karac build --mir`) | 2.24 to 2.82 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 2.60 s, against Rust's
1.34 (1.29 under overflow checks), C's 1.03 and Go's 3.10: 2.0 times
Rust's time under overflow checks, 2.5 times C's, and 0.84 times Go's.
Under valgrind's cachegrind C runs 7.5 billion instructions and 3.5
billion branches, Rust 10.6 and 4.5 billion and v2 22.0 and 6.7 billion,
of them 252 million indirect, about 840 a call against C's 180. Most
likely the gap is the answer built one letter at a time: each `push_str`
of a one-letter slice is a call that checks the slice's bounds and may
grow the buffer, where C copies a byte (not traced). Built for
`x86-64-v3`, the target `karac build` uses, C takes 0.92 to 1.09 s and
Rust with overflow checks 1.25 to 1.37 s, against v2's 2.36 to 2.55 s in
the same five interleaved runs. Python takes 17 s, about 17 times C's
time. The comparison with C and Rust waits until after M4.

## Compiler findings

None on v2: every arm, the differential and the bench program pass
`karac check` and run on both v2 backends as written. `String` has no
`replace_range`, which a splice arm would reach for, but
docs/library/strings.md does not list one either, so the arm builds the
spliced string with an f-string.
