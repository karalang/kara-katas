# 1625. Lexicographically Smallest String After Applying Operations

You are given a string `s` of **even length** consisting of digits from
`0` to `9`, and two integers `a` and `b`.

You can apply either of the following two operations any number of
times and in any order on `s`:

- Add `a` to all odd indices of `s` **(0-indexed)**. Digits post `9` are
  cycled back to `0`. For example, if `s = "3456"` and `a = 5`, `s`
  becomes `"3951"`.
- Rotate `s` to the right by `b` positions. For example, if
  `s = "3456"` and `b = 1`, `s` becomes `"6345"`.

Return *the **lexicographically smallest** string you can obtain by
applying the above operations any number of times on* `s`.

```
s = "5525", a = 9, b = 2  ->  "2050"
s = "74",   a = 5, b = 1  ->  "24"
s = "0011", a = 4, b = 2  ->  "0011"
```

**Constraints:** `2 <= s.length <= 100`; `s.length` is even; `s`
consists of digits from `0` to `9` only; `1 <= a <= 9`;
`1 <= b <= s.length - 1`.

## Approaches

| file | mechanism |
|---|---|
| `smallest.kara` ★ | every reachable string is a rotation by a multiple of `gcd(b, n)`, with some count of `a` added to its odd digits and, when `b` is odd (a rotation then swaps the parities), to its even digits too; ten counts each cover every multiple of `a` mod 10. Every such string is made and the least kept. O(n^2 / gcd(b, n) * 100) |
| `smallest_bfs.kara` | the statement read straight: a breadth-first walk from `s` over every string the two operations reach, each once, with a `VecDeque` and a `Set[String]` of those seen. O(states * n) |
| `smallest_greedy.kara` | one string per rotation: the odd count that makes digit 1 least and the even count that makes digit 0 least make the whole rotation least. O(n^2 / gcd(b, n)) |
| `smallest_solution.kara` | LeetCode's Rust template: a recursive depth-first walk with a `HashSet` of the strings seen and the least kept through a `&mut String`. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples, a case
whose odd `b` lets the even digits change too (`"43987654"`, 7, 3 gives
`00553311`), and an even rotation that leaves the even digits alone
(`"9999999999"`, 5, 4 gives `9494949494`); then the cases already their
own smallest and a checksum of every answer's digits for 1000 random
cases of up to 10 digits, 100 of up to 40, and 10 of up to 100.
`smallest.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: both operations applied to every string reached so far,
round after round, into a `SortedSet[String]` until a round adds nothing,
and the set's least string taken. It checks 300 random cases of 2 to 12
digits, `a` in `1..=9` and `b` in `1..n`. Every random choice is drawn
before any arm answers. The interpreter takes about 36 s.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is no greater than `s`, which is reachable |
| P3 | the answer's own answer is itself |
| P4 | starting from `s` rotated by `b` gives the same answer |
| P5 | starting from `s` with `a` added to its odd digits gives the same answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `300 problems: checksum 649644382, 7200 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. The first M5, the breadth-first walk
rotating left rather than right, survived, and is no mutant at all: a
rotation left by `b` is a rotation right by `n - b`, and the two
generate the same rotations. It was replaced by the walk losing its
rotation.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the even digits never change, whatever `b` | P1 165, P3 130, P5 126, P6 165 |
| M2 | ★: rotations by multiples of `b`, not of `gcd(b, n)` | P1 82, P3 28, P4 77, P6 82 |
| M3 | ★: the additions on the even digits | P1 95, P5 102, P6 95 |
| M4 | breadth-first: the additions on the even digits | P1 95, P5 102, P6 95 |
| M5 | breadth-first: no rotation, the added string twice | P1 251, P4 296, P6 251 |
| M6 | greedy: the odd count chosen as if `a` were one more | P1 225, P3 112, P4 35, P5 176, P6 225 |
| M7 | greedy: the even count chosen when `b` is even, not odd | P1 246, P3 130, P5 126, P6 246 |
| M8 | template: the additions on the even digits | P1 95, P5 102, P6 95 |
| M9 | template: the greatest string kept, not the least | P1 300, P2 292, P6 300 |
| M10 | template: a rotation by 1, not by `b` | P1 107, P6 107 |

## Benchmarks

The bench draws 200 random cases of 100 digits, with `a` and `b`, all of
them first, then each one's answer by the ★ arm in all five languages:
every candidate string made afresh and compared. Every implementation
prints `200 cases of 100 digits: 2257 zeros in the answers, checksum
830443087`. The C build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `eb32a1ff0` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.203 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.263 s |
| Kāra (`karac build`) | 0.264 s |
| Rust (`rustc -O`) | 0.303 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.318 s |
| Go | 0.482 s |
| Python | 8.3 s |

Kāra is ahead of both Rust builds and Go, and a third behind C. The work
is building 872440 strings of 100 digits, one push per digit,
and comparing each with the best; C writes into a buffer and compares
with `strcmp`. Why Kāra beats Rust here was not looked into.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is not above its real time (0.261 s and 0.262 s on one run).

## Verification

All four arms print the same output as `smallest.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`eb32a1ff0`.

## Writing it

The breadth-first arm first pushed each new string with
`for next in [added, rotated] { if seen.insert(next.clone()) { queue.push_back(next); } }`.
A bare `for` borrows its elements, so `next` cannot move into the queue;
`karac fix` wrote `queue.push_back(next.clone())`, one of the two ways
the diagnostic offers (the other, `.into_iter()`, would move instead of
copy). The differential's literal reading first took the least string
with `reached.first()`, Rust's `BTreeSet` name; Kāra's `SortedSet` calls
it `min()`, and `karac fix` renamed it. The ★ and greedy arms checked
clean as first written.

LeetCode's Rust template takes one `karac fix` of 28 edits: the
`use std::collections::HashSet` line deleted (`Set` is in the prelude),
`struct Solution {}`, `HashSet::new()` to `Set.new()`, `Self::dfs` to
`Solution.dfs`, `&mut seen` arguments to `mut seen`, `&mut HashSet<String>`
and `&mut String` parameters to `mut ref Set[String]` and
`mut ref String`, `usize` to `i64`, `!` to `not`,
`s.clone().into_bytes()` to `s.clone().bytes().to_vec()`,
`String::from_utf8` to `String.from_utf8`, and `format!` with slices to
an f-string. It then checks and agrees with no hand edit. No compiler
gap was met.
