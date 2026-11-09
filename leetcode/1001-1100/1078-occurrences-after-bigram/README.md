# 1078. Occurrences After Bigram

Given two strings `first` and `second`, consider occurrences in some text
of the form `"first second third"`, where `second` comes immediately
after `first`, and `third` comes immediately after `second`. Return an
array of all the words `third` for each occurrence of `"first second
third"`.

```
text = "alice is a good girl she is a good student", first = "a", second = "good"
  ->  ["girl", "student"]
text = "we will we will rock you", first = "we", second = "will"
  ->  ["we", "rock"]
```

**Constraints:** `1 <= text.length <= 1000`; `text` consists of lowercase
English letters and spaces; all the words in `text` are separated by a
single space; `1 <= first.length, second.length <= 10`; `first` and
`second` consist of lowercase English letters; `text` has no leading or
trailing spaces.

Occurrences may overlap (`"a a a a"` with `a`, `a` gives `a` twice), and
the answers come in the order of the text.

The arms take the text and the two words as `String` and return the
answers as a `Vec[String]`.

## Approaches

| file | mechanism |
|---|---|
| `occurrences.kara` ★ | the text split at its spaces into `Vec[Str]`, views into the text, and every word whose two words before it are `first` and `second` copied out with `to_string`. O(n) |
| `occurrences_windows.kara` | the words as owned `String`s, `windows(3)` over them, the windows whose first two words are the bigram kept and their third word cloned. O(n) |
| `occurrences_scan.kara` | one pass over the bytes with no list of words: the scan keeps where the last two words began and ended, and when a word ends after a `first` and a `second` it is cut out with `substring`. O(n) |
| `occurrences_find.kara` | the bigram searched for as text: `find` of `" first second "` in the text padded with a space at each end, the word after a match read up to the next space, and the search restarted one word on so that overlapping bigrams are all seen. O(n * \|bigram\|) |
| `occurrences_zip.kara` | iterators only: `split_whitespace` words zipped with themselves one and two words on (`skip(1)`, `skip(2)`), filtered on the pair and mapped to the third. O(n) |
| `occurrences_solution.kara` | LeetCode's Rust template (`struct Solution;`, `Vec<&str>`, `text.split(' ')`, `Vec::new()`, `&&`, `Solution::`, and LeetCode's own spelling `find_ocurrences`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 14 lines: the answers for LeetCode's two
examples and eight more; how many words 3000 random texts up to 40
characters and 1000 up to 1000 characters answer, their letters in all
and a checksum; how many of 500 `a`s follow `a a`; and how many words of
`ab c` 200 times and a last `ab` follow `c ab` (199) and `ab c` (200).
The random texts are words of a vocabulary of up to 12 random words, so
that bigrams recur and overlap, and `first` and `second` are each a word
of the text two times in three. `occurrences.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the words read character by character up to each space, and
for every three places `i`, `j`, `k` of the text with `j = i + 1` and
`k = j + 1`, the word at `k` when the word at `i` is `first` and the word
at `j` is `second`. It checks 2000 problems, 1000 texts up to 30
characters over a vocabulary of 1 to 4 words of 1 or 2 letters out of
two, and 1000 up to 120 characters over up to 8 words of up to 4 letters
out of up to four. Every random choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the letters of the text and the bigram renamed (each moved on by the same amount in the alphabet) rename the answer |
| P3 | every answer is a word of the text, and there are at most two fewer answers than words |
| P4 | the text, a word neither text has, and a second text over the same vocabulary answer the first text's answers, that word when the first text ends with the bigram, and the second text's answers |
| P5 | the text cut after any word answers a prefix of the answer |
| P6 | over every distinct bigram of the text, the answers number two fewer than the words |

All 72,000 checks pass on every arm: `2000 problems: checksum 929568398,
72000 checks over 6 arms: 0 failures`. A Python reading of the same
problems with `str.split` gives the same checksum.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Twenty-eight are caught, each the
same way under both backends; two of those stop with an index out of
bounds on both (the windows arm taking pairs for triples, the solution
arm's window one word early). Fifteen are kept, no two failing the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the third word never an answer (`for i in 3..`) | P1 633, P4 622, P6 1736 |
| M2 | ★: either word of the bigram enough (`or`) | P1 1260, P4 1671, P6 1282 |
| M3 | ★: the bigram read backwards | P1 619, P4 253, P6 667 |
| M4 | ★: the last word never an answer | P1 624, P4 624, P6 1736 |
| M5 | ★: the second word given for the third | P1 762, P4 685 |
| M6 | windows: only the first word checked | P1 1104, P4 1328, P6 1242 |
| M7 | windows: split at a letter, not a space | P1 1295, P4 685, P6 1736 |
| M8 | windows: `second` checked a word late | P1 1004, P4 918, P6 785 |
| M9 | scan: the space after a word kept | P1 1185, P3 1185, P4 854, P5 1185 |
| M10 | find: overlapping bigrams skipped | P1 566, P4 246, P6 1049 |
| M11 | find: the bigram matched as a prefix (no space after `second`) | P1 1474, P3 1442, P4 685, P6 1852 |
| M12 | find: the rest of the text taken as the word | P1 1185, P3 1185, P4 1416, P5 1185 |
| M13 | zip: the third word the second | P1 1318, P3 449, P4 685, P6 1852 |
| M14 | zip: `first` negated | P1 1577, P4 1325, P6 1394 |
| M15 | solution: answers in reverse order (`insert(0, ..)`) | P1 404, P4 979, P5 437 |

P1 and P4 catch all fifteen, P6 eleven, P3 four, P5 three and P2 none.
P2 cannot see an edit that treats every letter alike, and none of these
singles one out; it stays as a check on the arms' byte handling. P5 sees
only the edits that change an answer's spelling or order (M9, M12, M15),
and P3 those that invent a word the text lacks or answer more than
its bound.

Of the fifteen not kept, two are the crashes above and seven fail as a
kept edit: the first word dropped in the solution arm, the scan's bigram
at the very start skipped and the find arm's text unpadded at its front
fail as M1; the scan's last word never closed as M4; the solution arm's
`second` never checked as M6; the scan's first word never moved on as
M7; and the zip arm's second word skipped too far as M8. The first word
given for the third in the windows and zip arms fail alike, and the zip
arm's `second` compared with `first` and the solution's repeated answers
kept once each fail in a way of its own but were not needed. The other
two are equivalent and survive: the scan arm's length test before
`substring(start, end) == word` (the comparison already fails on a
different length), and the find arm's `begin < padded.len() - 1` for
`begin < padded.len()` (a match ends at a space, so the next word starts
before the last character, or the match took the trailing pad).

## Verification

Every arm prints the same output as `occurrences.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file. Under `karac __mir-run` the arms take 0.6 s to 2.1 s (the zip
arm the slowest) and the differential 25.7 s.

The kata found one diagnostics gap, fixed in kara with
`tests/kata_1078_slice_hint.rs`:

- **`.slice(a, b)` on a `Vec` got a bare "no method".** The
  differential's prefix property first took the first `cut` words as
  `words.slice(0, cut)`, JavaScript's spelling, and the checker said only
  "no method 'slice' on type 'Vec'". The library's run of elements is the
  range index `v[a..b]`, a `Slice[T]`. The error now says so for a `Vec`,
  an array or a slice, and `karac fix` writes `words[0..cut]` when both
  bounds are an integer literal or a name. Kara B-2026-11-09-3.

Every file went through `karac fix`. In the harness it removed the
`-> String` from a closure (`|seed: mut ref i64| -> String { .. }`, Rust's
spelling; Kāra infers a closure's return type); in the scan arm it
dropped the `ref` on two parameters, which borrow by default; in the
differential it took a lossless `as i64` and two more `ref`s. The Rust arm
reaches a clean check in two rounds: the syntax (`struct Solution {}`,
three `Vec[..]`s, `&str` to `Str`, `Vec.new`, `and`, `Solution.`), then
the `' '` separator, which Kāra's `split` takes as the string `" "`.

## Benchmarks

The bench builds 100 texts of up to 1000 characters once, from a
vocabulary of 12 words of 1 to 4 letters out of three, and asks each text
about 8 bigrams, 6 on average its own. Each of 300 rounds asks all 800 in
an order that changes with the round, with the ★ arm, and folds every
answer into a checksum. Every implementation prints `300 rounds of 800
bigrams over 100 texts: 2334000 words found, checksum 501635174`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `5fe8006173`
on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 1.231 to 1.316 s | 1.264 s |
| Go | 1.477 to 1.630 s | 1.545 s |
| Kāra (`karac build`) | 1.714 to 1.798 s | 1.765 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.724 to 1.918 s | 1.768 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.790 to 2.011 s | 1.845 s |
| Rust (`rustc -O`) | 1.817 to 1.985 s | 1.866 s |
| Python | 5.8 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (1.76 s) is below its real time.

The work is 240,000 splits of a text of about 1000 characters into views
and the copies of 2.3 million answer words. Kāra and Rust do the same
thing, a `Vec` of views and an owned `String` per answer, and Kāra runs
5% under Rust. Go's `strings.Split` and its answers share the text's
bytes, so Go copies no answer; C copies each answer with `malloc` as
LeetCode's C signature returns them, but keeps its views in one array per
call with no bounds checks. Python's `str.split` runs in C and takes 3.3x
Kāra.
