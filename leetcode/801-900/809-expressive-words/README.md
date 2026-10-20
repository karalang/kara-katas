# 809. Expressive Words

In a string like `heeellooo` the letters fall into groups of the same
letter: `h`, `eee`, `ll`, `ooo`. A word is stretched by taking one of
its groups and adding more of the same letter, so that the group is
three letters or more: from `hello`, the `o` group can become `ooo` to
make `hellooo`, but not `oo`, and the `ll` group can then become `lllll`
to make `helllllooo`. A word is stretchy when some number of these steps
make it equal to `s`. Return how many of the given words are stretchy.

```
s = "heeellooo",  words = ["hello", "hi", "helo"]  ->  1
s = "zzzzzyyyyy", words = ["zzyy", "zy", "zyy"]    ->  3
```

**Constraints:** `1 <= s.length, words.length <= 100`, `1 <=
words[i].length <= 100`, and `s` and every word are lowercase letters.

## Approaches

| file | mechanism |
|---|---|
| `expressive_words.kara` ★ | walk `s` and the word together a group at a time: the two groups must be of the same letter, and the group in `s` as long as the word's, or longer and three letters at least; the word is stretchy if both end together. O(\|s\| + the words' lengths) |
| `expressive_words_rle.kara` | write `s` and each word as their groups, a letter and its count, and compare the two lists group by group |
| `expressive_words_recursive.kara` | `matches(s, i, word, j)`: both at their ends, or a matching pair of groups and the rest matching after them |
| `expressive_words_iter.kara` | each string folded into its groups, the groups of `s` and of each word zipped and checked with `all`, and the words that pass counted with `filter` |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 9 lines: LeetCode's two examples and a third
from its tests; `abcd` against shorter, longer and reordered words,
where only the word itself fits; `aaa`, which `a`, `aa` and `aaa` reach
and `aaaa` does not; `aa`, which only `aa` reaches, since a group of two
cannot be made from one; `a` alone; LeetCode's largest, `s` of 100
letters in 20 groups of 5 and 100 words of the same letters with groups
of 1 to 6, the third of them with a group of 6 not stretchy; and 300
random rounds of 8 words, with the stretchy words counted and a
checksum. `expressive_words.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition by
search: from the word, make one group longer, to three letters or more,
in every way that keeps the string no longer than `s`, and again from
each string made, until `s` is made or nothing new is. Its 1,600 cases
have 6 words each, one of them made at random, and come in four kinds of
400: up to 4 groups of up to 4 letters from `a` to `c`, with words of
the same letters and groups of 1 to 5; groups of 1 to 3 of `a` and `b`,
so that short groups, which must match exactly, are common, and words of
`a` and `b` alone; up to 3 groups of up to 7 letters; and words that are
`s` with one change, a group one shorter or one longer, a letter
changed, a group left out, or a letter added at the end. Every case is
checked against the definition.

| | property |
|---|---|
| P1 | the definition's count, and its verdict on each word alone |
| P2 | `s` and every word written backwards give the same count |
| P3 | every letter renamed the same way, moved on in the alphabet, gives the same count |
| P4 | `s` is stretchy from itself, and `s` with each group of three letters or more made one longer never counts fewer words |

It prints `1600 cases (2108 of 9600 words stretchy), 4 arms, 25600
checks, 0 failures` under `karac __mir-run` and `karac __mir-llvm-run`,
and the same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a group of two in s grown from one | P1 300 |
| M2 | ★: letters left over in the word accepted | P1 395, P2 435 |
| M3 | ★: a group of three letters or more in s that the word lacks accepted, unless it is the last | P1 109, P2 147 |
| M4 | run-length: a word's group one longer than s's accepted | P1 1029 |
| M5 | run-length: a group of three in s held to the word's length | P1 316 |
| M6 | run-length: the first group split after its first letter | P1 339, P2 284 |
| M7 | recursive: groups cut at three letters | P1 510, P4 339 |
| M8 | recursive: letters left over in s accepted | P1 259, P2 382 |
| M9 | recursive: the word's group, not s's, held to three letters | P1 594 |
| M10 | iter: a word missing its last groups accepted | P1 259, P2 382 |
| M11 | iter: the groups' letters not compared | P1 392 |
| M12 | iter: a later letter joining the group before it | P1 784, P2 884, P3 61 |

P1 kills all twelve. P2 sees the six edits that treat one end of a
string differently from the other: letters left over in the word (M2) or
in `s` (M8), and a word missing its last groups (M10), are let through
only at the end; a group of `s` that the word lacks (M3) only before the
end, while the walk still has letters of the word to compare; the first
group split (M6) only at the front; and a later letter joining the group
before it (M12) only in one reading order. P3 sees only M12, the one
edit that depends on which letters are used rather than on whether they
match. P4 sees only the groups cut at three letters (M7): a group of
three in `s` made one longer is cut into three and one, and the extra
piece has nothing to match in a word that was stretchy, so the stretched
`s` counts fewer words. M8 and M10 fail the same number of cases: a word
missing the groups `s` ends with is the same thing as `s` with letters
left over.

## Verification

Every arm prints the same output as `expressive_words.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`71b497f24d`, whose last compiler change is `ae626e6c60`. The runtime
archives were built after the last runtime change, `7e85d320d5`.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy compiler refuses every program here but the recursive
arm. The ★ arm, the run-length arm, the differential and the bench
program pass `words[k]` to a function, and legacy reads that as moving a
`String` out of an index (`E_INDEX_MOVE_NON_COPY`), legacy taking a bare
parameter as owned rather than borrowed. The iterator arm's `filter`
closure becomes once-callable under legacy, since it takes the captured
`target` as owned, and legacy types the byte the fold closure reads as a
`u8` rather than a reference, so refuses its `*`. The recursive arm
makes the legacy JIT, `karac build` and an auto-par build panic in
codegen (`src/codegen/method_call.rs:3350`), and under the legacy
interpreter it prints the first eight lines right and then `300 random
rounds of 8 words: 502 stretchy, checksum 139958728`, where the mirror
and every v2 lane print 482 and `246567122`. Legacy is frozen, so all of
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 cases are
made once, each `s` of 25 groups of 1 to 4 letters from `a` to `e` and
100 words, three in four of them `s` with its groups shrunk as far as
they may be, a third of those then with one group made one letter too
long, and the rest random strings of up to 100 letters. Each of 200,000
rounds counts the stretchy words of the next case. Every implementation
prints `200000 rounds of 100 words: 9850000 stretchy, checksum
909665872`, the Kāra program under `karac __mir-run` included, in 1,647
s with `KARAC_MIR_MAX_STEPS` raised past its default of 40 billion
steps.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 4.17 to 4.45 s |
| Rust (`rustc -O`) | 4.03 to 4.32 s |
| Rust (`rustc -O -C overflow-checks=on`) | 4.27 to 4.62 s |
| Go | 4.69 to 5.16 s |
| Python | 127.79 to 129.09 s |
| Kāra (`karac build --mir`) | 4.83 to 6.10 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 13.6 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 4.91 s,
against C's 4.23, Rust's 4.23 (4.28 under overflow checks) and Go's
5.00; the 6.10 s run is one outlier, the other seven are 4.83 to 4.91 s.
Under valgrind's cachegrind v2 runs 22.3 billion instructions and 7.97
billion branches, 8.3% of them mispredicted, against Rust's 15.7 billion
and 4.84 billion (11.7%) and C's 16.9 billion and 4.84 billion (11.7%).
Legacy refuses the bench program (see Verification), so there is no
legacy timing to set v2 against. The comparison with C and Rust waits
until after M4.

## Compiler findings

B-2026-10-20-18 (kara ledger, filed from this kata, fixed in kara
`18685fefd3`): the iterator arm's `fold(Vec.new(), |out: Vec[(u8, i64)],
b| ...)` was refused by `karac check` and `karac __mir-run`, `expected
'Vec[?T2]', found 'Vec[(u8, i64)]'`: the element type of the empty
`Vec.new()` passed as fold's start was never solved from the closure's
annotated accumulator. Binding the start to a typed `let` first passed.
The arm now has the natural spelling again, and every surface runs it.
