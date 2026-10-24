# 937. Reorder Data in Log Files

You are given an array of `logs`. Each log is a space-delimited string
of words, where the first word is the **identifier**.

There are two types of logs:

- **Letter-logs**: all words (except the identifier) consist of
  lowercase English letters.
- **Digit-logs**: all words (except the identifier) consist of digits.

Reorder these logs so that:

1. The **letter-logs** come before all **digit-logs**.
2. The **letter-logs** are sorted lexicographically by their contents.
   If their contents are the same, then sort them lexicographically by
   their identifiers.
3. The **digit-logs** maintain their relative ordering.

Return the final order of the logs.

```
["dig1 8 1 5 1","let1 art can","dig2 3 6","let2 own kit dig","let3 art zero"]
  ->  ["let1 art can","let3 art zero","let2 own kit dig","dig1 8 1 5 1","dig2 3 6"]
["a1 9 2 3 1","g1 act car","zo4 4 7","ab1 off key dog","a8 act zoo"]
  ->  ["g1 act car","a8 act zoo","ab1 off key dog","a1 9 2 3 1","zo4 4 7"]
```

**Constraints:** `1 <= logs.length <= 100`; `3 <= logs[i].length <=
100`; all the tokens of `logs[i]` are separated by a single space;
`logs[i]` is guaranteed to have an identifier and at least one word
after the identifier.

## Approaches

| file | mechanism |
|---|---|
| `reorder_log_files.kara` ★ | each log cut at its first space into identifier and contents; digit-logs kept in a list in order, letter-logs sorted with `sort_by` on contents and then identifier, and the two lists joined. O(n log n) comparisons for `n` logs |
| `reorder_log_files_keys.kara` | one stable `sort_by_key` over all the logs: a letter-log's key is `"0"`, its contents, a byte below the space and its identifier, so a contents that is a prefix of another still comes first; a digit-log's key is `"1"`, and stability keeps the digit-logs in order. O(n log n) comparisons |
| `reorder_log_files_insertion.kara` | an insertion sort by hand over the letter-logs' bytes, comparing contents from just after each identifier, a shorter contents that runs out first coming first, then the identifiers the same way. O(n²) comparisons |
| `reorder_log_files_words.kara` | each log split into words; letter-logs compared word by word after the identifiers, a list that runs out first coming first, then by identifier, which is the same order as comparing the contents as strings since the space is below every letter; merge sorted by hand. O(n log n) comparisons |
| `reorder_log_files_passes.kara` | the letter-logs sorted stably by identifier and then by contents, the less significant key first as a card sorter does. O(n log n) comparisons |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and five
more (digit-logs only, which keep their order; equal contents ordered by
identifier, `a10` before `a9` as strings; contents that are prefixes of
one another, `art` before `art c` before `art can` before `arta`; each
kind with one-letter identifiers; and one log), each with its answer;
for 300 random lists of 1 to 100 logs, identifiers of 1 to 4 characters
and contents of 1 to 4 words of up to 3 letters or digits, the logs and
a checksum of the answers; and two of LeetCode's largest, 100 logs of
100 characters, half of them letter-logs, and 100 letter-logs with the
same contents, so that only the identifiers decide. `reorder_log_files.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the letter-logs first, each time the one with the least
contents left and of those the least identifier, then the digit-logs in
the order they came. It checks 3,200 random lists: 3,000 of 1 to 12 logs
with identifiers of 1 or 2 characters and 1 or 2 words of 1 or 2
characters, against the statement, and 200 of 1 to 100 logs with
identifiers of up to 4 characters and up to 6 words of up to 4, against
the other properties; 29,679 logs, 14,844 of them letter-logs.
Identifiers come from `a`, `b`, `0` and `1`, and the words from `a`, `b`
and `c`, or digits, so equal contents and contents that are prefixes of
one another turn up often.

| | property |
|---|---|
| P1 | the statement's order, on the small lists |
| P2 | the same logs, with every letter-log before every digit-log |
| P3 | each letter-log in order with the next, and the digit-logs in the order they came |
| P4 | the logs shuffled give the same letter-logs in the same order, then the digit-logs in their new order |
| P5 | the letter-logs alone come out as they did, and a digit-log added at the end comes out last |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 lists, 29679 logs, 14844 letter-logs, 95000 checks over
5 arms: 0 failures` under `karac __mir-run` (17 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: identifiers before contents | P1 1822, P3 2011, P6 2011 |
| M2 | ★: contents starting with 9 taken as letters | P1 774, P2 912, P3 716, P4 930, P5 354, P6 936 |
| M3 | ★: the contents cut with the space | P1 2583, P2 2686, P3 2079, P4 2786, P5 3088, P6 2779 |
| M4 | keys: digit-logs keyed `"0"` | P1 2490, P2 2686, P4 2686, P5 2950, P6 2686 |
| M5 | keys: a space between contents and identifier | P1 104, P3 161, P6 161 |
| M6 | keys: nothing between contents and identifier | P1 747, P3 884, P4 7, P6 884 |
| M7 | insertion: a longer contents first | P1 686, P3 815, P4 872, P6 815 |
| M8 | insertion: ties by identifier in reverse | P1 385, P3 430, P6 430 |
| M9 | insertion: the last byte of each never compared | P1 1526, P3 1690, P4 1678, P6 1690 |
| M10 | words: a longer word list first | P1 649, P3 779, P6 779 |
| M11 | words: lists of two never sorted | P1 1446, P3 1633, P4 1909, P6 1633 |
| M12 | words: the identifier deciding the kind | P1 2535, P2 2514, P3 2408, P4 2661, P5 3152, P6 2731 |
| M13 | passes: no pass by identifier | P1 207, P3 234, P4 243, P6 234 |
| M14 | passes: contents starting with 0 taken as letters | P1 768, P2 912, P3 739, P4 945, P5 2, P6 939 |
| M15 | passes: each digit-log put first | P1 2618, P2 2686, P3 2437, P4 2815, P5 3200, P6 2815 |

P1 and P6 kill all fifteen, P3 fourteen, P4 eleven, and P2 and P5 six
each. P2 and P5 kill the six that put a log on the wrong side: the four
that tell the kinds apart wrongly (M2, M3, M12, M14) and the two that
put the digit-logs first (M4, M15). Of those, P5's added digit-log
starts with a 9 a ninth of the time, which is how it sees M2, and with
a 0 only when it is `0`, which is all it sees of M14. The other nine
keep every log on its side and only order the letter-logs wrongly.

P4 kills the mistakes whose order depends on the order the logs come in,
which a shuffle changes: the comparisons that call different logs equal
(M6, where `a` with identifier `b1` and `ab` with identifier `1` get the
same key, and M13, where equal contents keep the order they came in),
the comparisons that are not orders at all (M7, and M9, which stops one
byte short and then calls the side with a byte left the later), and M11,
whose pairs stay as they came; with the six that put a log on the wrong
side. The other four (M1, M5, M8, M10) sort by a consistent order, just
the wrong one, so a shuffle changes nothing.

P3 misses only M4: its digit-logs, all keyed the same, keep their order,
and its letter-logs are in order, only after the digit-logs.

Ten other edits were tried and set aside. Six failed exactly the same
checks as a kept mutant: ★ ordering different contents by the whole
log, keys putting the identifier before the contents, words comparing
the identifiers first and passes making its second pass by the whole
log all order by identifier first, as M1; ★ breaking ties by identifier
in reverse, as M8; and insertion taking the space as the first byte of
the contents, as M3. Four were sound but beyond three an arm (keys
keying the digit-logs by the whole log, insertion moving each log past
the ones before it, words comparing words in reverse, and passes
telling the kind by the identifier's last character).

## Verification

Every arm prints the same output as `reorder_log_files.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 0.5 to 1.2 s each and the
differential 17 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The ★, keys and passes arms print the same output under the frozen
legacy interpreter, the legacy JIT and both legacy builds, with and
without auto-par. Legacy refuses the insertion arm and the differential
at the first `*` on an element of a `Vec`'s `.iter()` ("unary '*'
requires 'ref T', ... found 'u8'"), legacy's older rule, under which
the element is a copy; under v2 it is a reference and the `*` is
required. It refuses the words arm at `log.split(" ").map(...)`, since
its `split` returns a `Vec` that needs an explicit `.iter()` ("no method
'map' on type 'Vec'"), and the bench program at
`reorder_log_files(lists[(r + i) % count])`, a move out of an index
("cannot move ... out of an index"), which v2's borrowing parameters
make a borrow. Legacy is frozen, so none of this is filed.

## Benchmarks

The bench program builds 200 lists of 100 logs once, LeetCode's most,
each log an identifier of a letter and its place in the list, then words
of 1 to 8 letters from `a` to `e`, or of digits, up to 20 to 100
characters; in each of 200 rounds it runs the ★ arm on every list, each
round starting from a different one, and folds the identifiers of the
answers into a checksum. Every implementation prints `200 rounds over
200 lists of 100 logs: 4000000 logs, checksum 55872837`. Rust and Kāra
copy each letter-log's contents, identifier and whole log into a
record, as the ★ arm does; Go keeps them as views into the log, and C
sorts pointers to the logs with `qsort`, copying nothing. The
identifiers are distinct within a list, so no two letter-logs tie and
`qsort` not being stable cannot matter.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.31 to 0.35 s | 0.32 s |
| Rust (`rustc -O`) | 0.94 to 1.12 s | 0.99 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.90 to 1.12 s | 0.98 s |
| Go | 0.80 to 0.99 s | 0.86 s |
| Python | 2.66 s | |
| Kāra (`karac build --mir`) | 1.02 to 1.25 s | 1.07 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about 8 times C's: its sort is written
in C and compares its tuples' strings there.

v2 takes 1.09 times Rust's median time under overflow checks and 3.30
times C's. Under valgrind's cachegrind v2 runs 8.75 billion instructions
and 1.36 billion branches with 51.1 million mispredicted, Rust with
overflow checks 7.03 billion, 1.21 billion and 52.2 million, and C 1.59
billion, 0.21 billion and 14.0 million. v2 is close to Rust, and both
are far from C; that the gap to C is the three strings copied for each
letter-log, which C does not make, is inferred, not profiled.
</content>
</invoke>
