# 2024. Maximize the Confusion of an Exam

A teacher writes a test of `n` true/false questions, and wants to confuse
the students by making the answer key hold as many consecutive equal
answers as possible. You are given the key `answerKey`, where
`answerKey[i]` is `'T'` or `'F'`, and an integer `k`: you may change any
answer, `'T'` to `'F'` or `'F'` to `'T'`, at most `k` times. Return the
greatest number of consecutive `'T'`s or consecutive `'F'`s the key can
hold after the changes.

```
answerKey = "TTFF",      k = 2  ->  4
answerKey = "TFFT",      k = 1  ->  3
answerKey = "TTFTTFTT",  k = 1  ->  5
```

**Constraints:** `1 <= n <= 5 * 10^4`; `answerKey[i]` is `'T'` or `'F'`;
`1 <= k <= n`.

A run of `c` after the changes is a window of the key that holds at most
`k` of the other answer, so the answer is the longest window holding at
most `k` `F`s or at most `k` `T`s. Such windows close under shrinking,
which is what lets a sliding window find the longest.

## Approaches

| file | mechanism |
|---|---|
| `confuse.kara` ★ | for each answer `c`, a window over the key's bytes that grows on the right and gives up its left end while it holds more than `k` of the other answer; the longer of the two. O(n) |
| `confuse_pair.kara` | one window over `chars()` counting its `T`s and `F`s in a tuple, giving up its left end while even the smaller count is more than `k`. O(n) |
| `confuse_grow.kara` | a window that never shrinks: it slides one place whenever its length passes the count of the answer it holds most of, plus `k`, so its length is always the best so far, and the answer is its length at the end. O(n) |
| `confuse_prefix.kara` | prefix counts of `T`; for each right end a hand-written binary search for the leftmost start holding at most `k` `F`s, and again for `T`s. O(n log n) |
| `confuse_brute.kara` | every start, the window grown one answer at a time until both counts pass `k`. O(n^2) at worst |
| `confuse_solution.kara` | LeetCode's Rust template (a closure `|c: u8| -> i32` over `as_bytes()`, `let (mut l, mut cnt, mut res) = (0usize, 0, 0)`, `res.max((r - l + 1) as i32)`, run for `b'T'` and `b'F'`), carried by `karac fix` to a clean check |
| `differential.kara` | all six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's three
examples and five more; then the total and a checksum of the answers for
3000 keys of 1 to 30 answers, each with its own share of `T`, `k` from 1
to the length, and for 6 keys of 1500 answers with 5 to 95 `T`s in 100 and
`k` from 1 to 300. `confuse.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every set of at most `k` answers flipped, out of all `2^n`, and
the longest run of one answer in each key that results. It checks 1500
problems, each a key of 1 to 10 answers, `T` or `F` at even odds, with `k`
from 1 to the key's length. Every random choice of a problem is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the key reversed leaves the answer |
| P3 | every `T` swapped with `F` leaves the answer |
| P4 | one more change lengthens the answer unless it is already the whole key: `answer(k + 1) > answer(k)`, or `answer(k) == n` |
| P5 | the answer is at least the longest run already in the key and at least `min(k + 1, n)`, and at most `n` |
| P6 | each arm agrees with at least three of the other five |

P2 and P3 hold because a run is a run read backwards, and a run of `T`
after the swap is a run of `F` before it. P4 holds because the best window
for `k`, if it is not the whole key, has a neighbour, and one more change
covers it. P5's lower bound is the `k + 1` answers any window of that
length can be made equal with `k` changes, since one of them is already
right.

A first draft of P4 said one more change adds at most one; it is false,
since a change can join two runs: `TFFTTF` with `k = 1` gives 3 and with
`k = 2` gives 5 (`TFFFFF`). The differential caught its own property on
the first run, all five correct arms failing it alike.

The differential prints `1500 problems: checksum 88935121, 54000 checks
over 6 arms: 0 failures` under every lane in Verification; a Python copy of
the literal reading gives the same checksum. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Sixteen are kept, two or
three to each arm. All thirty are killed, each fails the same way under
both backends, none by a crash or a hang, and no two kept ones fail the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the best taken before the window shrinks | P1 167, P2 99, P6 167 |
| M2 | ★: only `T` tried | P1 286, P3 590, P5 97, P6 286 |
| M3 | ★: the length one short | P1 1500, P4 1291, P5 747, P6 1500 |
| M4 | pair: the left end always taken off `t` | P1 69, P2 55, P3 109, P5 3, P6 69 |
| M5 | pair: the window shrunk while the smaller count is `k` | P1 437, P5 46, P6 437 |
| M6 | pair: an `F` counted as a `T` | P1 209, P6 209 |
| M7 | grow: the most never raised | P1 1077, P5 1077, P6 1077 |
| M8 | grow: the slide not taken off its count | P1 86, P6 86 |
| M9 | prefix: the search one start too far | P1 1357, P4 1148, P5 604, P6 1357 |
| M10 | prefix: the `F` count one short | P1 147, P3 164, P6 147 |
| M11 | prefix: the search never trying the first start | P1 1205, P2 99, P4 1207, P5 604, P6 1205 |
| M12 | brute: the counts kept across starts | P1 75, P2 119, P5 6, P6 75 |
| M13 | brute: a window fits only when both counts fit | P1 636, P5 221, P6 636 |
| M14 | Rust: the first answer never in a window | P1 277, P2 89, P4 143, P5 143, P6 277 |
| M15 | Rust: only `F` tried | P1 304, P3 590, P5 82, P6 304 |
| M16 | Rust: `k` halved | P1 651, P4 204, P5 90, P6 651 |

P1 and P6 kill all sixteen, P5 twelve, P2 five, P4 five and P3 four. P5
bounds the answer by the longest run already there, `k + 1` and `n`; it
misses only the edits that overcount without passing `n` (M1, M6, M8) and
the `F` count one short (M10). P2 reverses the key and sees the edits that
treat its two ends unevenly: a best taken mid-shrink (M1), a left end
mishandled (M4, M12), a first start or first answer left out (M11, M14).
P3 swaps the answers and sees the edits that treat them unevenly: one
answer tried (M2, M15), a left end always taken off `t` (M4), the `F`
count alone short (M10). P4 asks for one more change, which an edit sees
when it is off by a constant (M3, M9) or loses a fixed position or half
of `k` (M11, M14, M16).

M6 never counts an `F`, so its window never shrinks and its answer is
always `n`; it fails exactly the 209 problems whose answer is less than
`n`. The ★ arm allowed `k + 1`, the grow arm counting every answer on one
side, the brute arm breaking one answer late, and the Rust arm with `k + 1`
or with its `F` window never shrinking fail the same 209. The other
failures that match a kept one: the pair arm's best before the shrink
(M1); the ★ arm with one change fewer, the grow arm sliding at exactly
`most + k` and the Rust arm shrinking at `k` (M5); the grow and brute arms
one short (M3); the pair arm shrinking by the larger count and the prefix
arm's larger start (M13); the prefix arm's `T`
start alone (M15); the brute arm's first start alone (M12).

Six drafts were replaced. Two survived, and both are equivalent: the ★
arm shrinking by `if` instead of `while` (the window grows by one a step,
so giving up one a step keeps it valid, the grow arm's own idea), and the
prefix arm counting `F` instead of `T` (it searches for both answers, so
which one is prefix-counted changes nothing). The ★ arm's left end given
up without its count and the Rust arm counting the answer itself ran the
left end past the key and crashed on an index; the Rust arm's left end
never moved looped forever. The Rust arm's `F` window never shrinking
failed as M6.

## Verification

Every arm prints the same output as `confuse.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them. Under `karac __mir-run` the arms take 0.3 s to 1.7 s (brute) and
the differential 3.6 s.

The five arms were written in Kāra and reached a clean check through
`karac fix` in one round each: it turned `bytes().collect()` into
`bytes().iter().collect()` (`bytes()` is already a `Vec[u8]`), `'T' as u8`
into the byte literal `b'T'`, and `let (mut t, mut f) = (0, 0)` into
`let mut (t, f) = (0, 0)`.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` alone, in three rounds (8, 3 and 1 edits), with
two compiler changes made for it. The first round carries the closure's
`-> i32` (Kāra infers a closure's return type), the `mut` inside the tuple
pattern, the unit struct, the `&String` and the `::` path. The second
turns `as_bytes()` into `bytes()`, drops the `0usize` suffix, and writes
`0i32` for `res`'s literal. The third drops the wrapper's `ref`.

The `usize` suffix had been refused as a `usize` mixed with `i64` in
arithmetic, `r - l + 1`, with no fix: kara 8bee9acf06 gives it the same
fix as an assignment or a comparison has. And dropping `-> i32` took away
what typed `res`: the tuple's literal then took the default `i64`, so
`res.max((r - l + 1) as i32)` was refused ("`max` expects an argument of
type `i64`, got `i32`") with no fix and no binding named, and the tail
`longest(b'T').max(longest(b'F'))` narrowed. Ledger row B-2026-11-08-53;
kara bfd2f7b286 names the binding and writes the literal's suffix, `(0, 0,
0i32)`, since a tuple's literal is inline (design.md §8 Literal
suffixes). The same fix carries katas 2006 (`[0i32; 101]`) and 2012
(`Vec.filled(n, 0i32)`).

## Benchmarks

The bench builds 20 keys of 100000 answers, `T` with 50, 70, 90, 97 or 99
in 100 and `k` from 1 to 10000, once in all five languages, and runs the ★
arm on each for 5 rounds: 100 calls. Every implementation prints
`100 calls: total 2500680, checksum 595688042`. The Kāra arm copies the
key's bytes into a `Vec[u8]` on each call (`bytes().iter().collect()`, as
the kata writes it); the others read the string's bytes in place.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.103 to 0.120 s | 0.107 s |
| Rust (`rustc -O`) | 0.108 to 0.141 s | 0.111 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.113 to 0.145 s | 0.116 s |
| Kāra (`karac build`) | 0.110 to 0.145 s | 0.116 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.112 to 0.154 s | 0.118 s |
| Go | 0.122 to 0.135 s | 0.126 s |
| Python | 3.4 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.115 s) is not above its real time (0.116 s).

The sequential Kāra program is 1.02x Rust under overflow checks and 1.11x
C.