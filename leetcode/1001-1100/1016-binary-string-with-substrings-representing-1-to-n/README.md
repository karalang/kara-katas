# 1016. Binary String With Substrings Representing 1 To N

Given a binary string `s` and a positive integer `n`, return true if the
binary form of every integer from 1 to `n` is a substring of `s`, and
false otherwise. A substring is a contiguous run of characters.

```
s = "0110", n = 3  ->  true
s = "0110", n = 4  ->  false   ("100" is not in s)
```

**Constraints:** `1 <= s.length <= 1000`, each character of `s` is `'0'`
or `'1'`, `1 <= n <= 10^9`.

## Approaches

`n` can be far larger than anything `s` could hold, so every arm first
needs a reason to stop early. Dropping the last bit of `x`'s binary form
leaves `x / 2`'s, so `x / 2` is a substring wherever `x` is. The numbers
in `(n / 2, n]` have at most two bit lengths, and `s` has at most
`len(s)` substrings of each length, so when there are more than
`2 len(s)` of them they cannot all appear.

| file | mechanism |
|---|---|
| `query.kara` ★ | the upper half: after the bound, search `s` for the binary form of each `x` from `n` down to `n / 2 + 1`, since every smaller number is a substring of one of those. O(len(s)^2 log n) |
| `query_all.kara` | every number: the same bound, then the statement as written, each of 1 to `n` searched for. O(len(s)^2 log n) |
| `query_set.kara` | the values present: read every substring that starts with a 1 as a number, extending it a bit at a time while it stays at most `n`, keep the values in a `Set`, and compare its size with `n`. O(len(s) log n) |
| `query_window.kara` | one window per length: for each bit length up to `n`'s, slide a window of that length along `s`, keeping its value as it moves, and tick off each value in range. O(len(s) log n) |
| `query_trie.kara` | a trie of suffixes: insert each suffix that starts with a 1, cut off once its value passes `n`, into a binary trie in one flat `Vec`; each node is a distinct value, so the answer is whether there are `n` nodes. O(len(s) log n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 19 lines: twelve examples, LeetCode's two
among them, up to `n = 10^9` on a one-bit string; for six groups of
random strings (8 to 1,000 bits, with a 1 at each place with probability
1/8, 1/2 or 7/8) asked for every `n` up to a limit, how many pairs hold,
the largest `n` that holds and a checksum; and the strings made by
writing the binary forms of 1 to `m` one after another, for `m` up to
300, which all hold for `n = m`, and 287 of which still hold with `m`'s
own form cut off the end, because it appears across the earlier forms.
`query.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each of 1 to `n` written out bit by bit and compared at every
position of `s`. It asks 18,064 questions: every string of 1 to 9 bits
(1,022) against every `n` up to 12, 100 random strings of 10 to 60 bits
up to 40, 15 random strings of 200 bits up to 60, and the binary forms
of 1 to `m` written out, for `m` up to 40, up to `m + 2`.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | holding for `n` means holding for `n - 1` |
| P3 | a bit added at either end of `s` keeps it holding |
| P4 | never for `n >= 4 len(s) + 2`, and for `n = 1` exactly when `s` has a 1 |
| P5 | stripping `s`'s leading zeros changes nothing |
| P6 | each arm agrees with at least two of the other four |

The differential prints `18064 queries: checksum 639895171, 457615
checks over 5 arms: 0 failures` under `karac __mir-run` (26 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Twenty-seven edits to the differential, each run under `karac __mir-run`
and `karac __mir-llvm-run`; fifteen are kept, three to each arm, all
fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the lowest of the upper half skipped | P1 805, P2 470, P4 9, P5 18, P6 805 |
| M2 | ★: `n / 2` searched too, which for `n = 1` is the form `0` | P1 10, P4 10, P5 36, P6 10 |
| M3 | ★: every other number searched | P1 1459, P2 1459, P6 1459 |
| M4 | all: 1 never searched | P1 9, P4 9, P5 9, P6 9 |
| M5 | all: `n` never searched | P1 1148, P4 9, P5 9, P6 1148 |
| M6 | all: the test inverted | P1 6238, P3 96, P4 1177, P5 96, P6 6238 |
| M7 | set: substrings with leading zeros read too | P1 9122, P2 1129, P3 1155, P4 1167, P5 109, P6 9122 |
| M8 | set: `n` itself never kept | P1 6142, P4 1168, P6 6142 |
| M9 | set: the leading 1 dropped | P1 7225, P2 1056, P3 1112, P4 1095, P6 7225 |
| M10 | window: the first full window missed | P1 439, P4 10, P5 439, P6 439 |
| M11 | window: one past the length's range | P1 4974, P6 4974 |
| M12 | window: the bit leaving the window worth half | integer overflow panic at `differential.kara:69:22`, exit 101 |
| M13 | trie: a suffix's first node always new | P1 6743, P2 506, P3 769, P4 1121, P6 6743 |
| M14 | trie: suffixes with leading zeros inserted | P1 6480, P2 277, P3 306, P4 1159, P5 457, P6 6480 |
| M15 | trie: the newest node taken instead of the child | P1 5877, P2 873, P3 1780, P6 5877 |

P1 and P6 kill the fourteen that finish, P4 eleven, P5 eight, P2 seven
and P3 six; M12 is killed by Kāra's overflow check, the stale bit
driving the window's value past `i64` in both lanes. The checks draw no random number that
depends on an answer, so every mutant sees the same questions and their
counts can be compared.

Twelve other edits were tried and set aside. Five change no answer the
differential sees. ★ without its bound and window without its count
bound lose only a shortcut to an answer the search reaches anyway; set
and trie accepting at least `n` values or nodes cannot hold more than
`n`; and ★ with its bound halved (`n - n / 2 > len(s)`) answers no
question here differently, though counting alone does not rule out a
longer string on which it would. Two more window
edits panic exactly as M12 (the length never growing, and the leaving
bit dropped a step late). Three failed exactly the same checks as M11:
★ searching for decimal forms, all for octal forms, and set reading
every bit as a 1, each of which makes every true answer for `n >= 2`
false. The other two were killed too, beyond three per arm: trie
inserting `n + 1` and flipping every bit.

## Verification

Every arm prints the same output as `query.py` under `karac __mir-run`
(the v2 MIR interpreter) and `karac __mir-llvm-run`, and under `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error; the
differential prints its line under all three. `karac check
--output=json` reports no diagnostic for the five arms, the differential
and the bench program, so `karac fix` had nothing to do. `karac run` and
a `karac build` binary print the same output for every arm and the
differential. The release build is kara `56c60bdf7c`, with runtime
archives rebuilt at `ce706dd131`, the last commit before it to change
the runtime. Under `karac __mir-run` the arms take 0.75 s (★) to 17.3 s
(window); ★ and all stop at the first missing number, while the others
read the whole string for every `n`.

Writing this kata turned up two compiler performance gaps, both in the
compiled `s.contains(f"{x:b}")` the ★ arm runs on every number: kara
`B-2026-10-29-32` (a short needle's `contains`) and `B-2026-10-29-33`
(the `{x:b}` format). See § Benchmarks.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages on 200 random strings of
1,000 bits, each asked for every `n` from 1 to 400: 2,251,192 binary
forms of 1 to 9 bits, searched for over 424,572,466 bytes of string in
all. Every implementation prints `200 strings of 1000 bits, n = 1..400:
33779 hold, checksum 87861930`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.210 to 0.330 s | 0.234 s |
| Rust (`rustc -O`) | 0.303 to 0.479 s | 0.366 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.304 to 0.453 s | 0.336 s |
| Go | 0.213 to 0.298 s | 0.227 s |
| Python | 1.95 s | |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.897 to 2.077 s | 1.986 s |
| Kāra (`karac build`) | 1.879 to 2.132 s | 1.981 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(its user time equals its real time) and runs as fast as the sequential
one.

v2 took 5.9 times Rust's median time under overflow checks and 8.5
times C's, and was no faster than Python. Under callgrind the Kāra binary
runs 17.8 billion instructions: about half in `memchr` and `memcmp`,
called from the search, a quarter formatting `{x:b}`, and the rest in
the loops themselves and in malloc and free. The two causes, measured apart:

- `contains` with a needle of at most 16 bytes is compiled to a `memchr`
  for the needle's first byte and a `memcmp` of the rest at each hit. On
  a binary string that byte is every other one, so the search makes two
  library calls per two bytes. Searching one of the bench's strings
  425,000 times for an absent 9-bit form takes 1.351 s, against 0.144 s
  for C `strstr` and 0.187 s for Rust (`B-2026-10-29-32`).
- `f"{x:b}"` parses its format spec again on every call, through two
  heap strings: 130 ns a number, against 38 ns for Rust's `format!` and
  22 ns for C's malloc and bit loop, while a plain `f"{x}"` costs Kāra
  about 5 ns (`B-2026-10-29-33`).
