# 1023. Camelcase Matching

Given an array of strings `queries` and a string `pattern`, return a
boolean array whose `i`-th entry says whether `queries[i]` matches
`pattern`. A query matches when it can be made by putting small
letters into the pattern, anywhere and any number of them, including
none.

```
queries = ["FooBar","FooBarTest","FootBall","FrameBuffer","ForceFeedBack"]
pattern = "FB"     ->  [true, false, true, true, false]
pattern = "FoBa"   ->  [true, false, true, false, false]
pattern = "FoBaT"  ->  [false, true, false, false, false]
```

**Constraints:** `1 <= pattern.length, queries.length <= 100`,
`1 <= queries[i].length <= 100`, all English letters.

## Approaches

Every letter of a matching query is either the pattern's next letter or
a small letter put in, and a capital can only be the former.

| file | mechanism |
|---|---|
| `camel_match.kara` ★ | two pointers: walk the query with a pointer into the pattern, matching a letter equal to the pattern's next, skipping any other small letter and failing at any other capital; it matches when the pattern was used up. O(total length) |
| `camel_match_backward.kara` | from the back: the same walk from the other end, going back through the query with a pointer to the pattern's last unmatched letter. O(total length) |
| `camel_match_split.kara` | word by word: cut both strings into words at their capitals, after a first word of the small letters before any capital; they match when the query has as many words, each starting with the same capital, and each pattern word's letters appear in order in the query's. O(total length) |
| `camel_match_dp.kara` | a table of prefixes: `can[i][j]` says whether the first `j` letters of the query can be made from the first `i` of the pattern; the query's last letter is either the pattern's last, matched, or a small letter put in. O(query length * pattern length) per query |
| `camel_match_skeleton.kara` | capitals and a subsequence: a query matches exactly when it has the pattern's capitals in the same order and the pattern is a subsequence of it; the capitals are compared as filtered iterators collected into `String`s, and the subsequence is tested the iterator way, `pattern.chars().all(\|c\| rest.any(\|x\| x == c))` with one iterator `rest` over the query carrying on from search to search. O(total length) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines: the answers for LeetCode's three
examples and for four patterns against eight short queries; and for six
groups of random cases (a pattern and 4 to 100 queries of up to 100
letters, over 2 to 26 letters of each case, with a capital at each
place with probability 1/8 to 4/8; half the queries grown from the
pattern by putting in letters, a capital among them with probability
1/8 per letter, and half drawn at random), how many queries match and a
checksum of the answers. `camel_match.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: each letter of the query is either the pattern's next
letter or a small letter put in, both tried by a recursive search. It
checks 20,157 queries: every pattern of 1 to 3 letters over `a`, `b`
and `A` against every query of 1 to 5 letters over them (39 patterns
against 363 queries), then 300 random patterns of 1 to 8 letters over
four letters and their capitals, each with 20 queries of up to 16
letters, half grown from the pattern. Each query is also asked with a
small letter put in at a random place, with a capital put in, read
backwards against the pattern read backwards, and with the case's first
query added after both it and the pattern.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | a match stays a match with a small letter put in |
| P3 | a match is lost with a capital put in, since the pattern has one capital fewer |
| P4 | the query matches exactly when it matches read backwards against the pattern read backwards |
| P5 | a match stays a match with the same text added after both the query and the pattern |
| P6 | each arm agrees with at least two of the other four |

The differential prints `20157 queries: checksum 699408936, 604710
checks over 5 arms: 0 failures` under `karac __mir-run` (15 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Thirty edits to the differential, each run under `karac __mir-run` and
`karac __mir-llvm-run`; fifteen are kept, three to each arm, all
fifteen are killed, each fails the same checks under both, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the pattern not required to be used up | P1 4364, P3 544, P4 1961, P5 224, P6 4364 |
| M2 | ★: small letters refused instead of capitals | P1 3594, P2 817, P3 817, P6 3594 |
| M3 | ★: the pattern's first letter skipped | P1 2992, P4 3723, P6 2992 |
| M4 | backward: the pattern's first letter optional | P1 1755, P3 165, P4 2397, P6 1755 |
| M5 | backward: the query's first letter never read | P1 2316, P2 88, P3 265, P4 2713, P6 2316 |
| M6 | backward: only a stray `A` refused | P1 1002, P3 3426, P6 1002 |
| M7 | split: a capital starting no word after an empty one | P1 951, P2 136, P3 374, P4 1589, P6 951 |
| M8 | split: a word's last letter optional | P1 1667, P4 370, P5 479, P6 1667 |
| M9 | split: words kept without their capitals | P1 1115, P2 223, P4 1037, P6 1115 |
| M10 | dp: capitals put in anywhere after the pattern starts | P1 2837, P3 5119, P4 1871, P6 2837 |
| M11 | dp: a match read from the wrong cell | P1 2577, P5 212, P6 2577 |
| M12 | dp: or for and in a match | P1 15441, P3 17807, P4 944, P6 15441 |
| M13 | skeleton: the capitals compared, the subsequence not tested | P1 2463, P6 2463 |
| M14 | skeleton: each pattern letter searched for from the start of the query | P1 1750, P6 1750 |
| M15 | skeleton: `any` for `all` | P1 2104, P4 444, P6 2104 |

P1 and P6 kill all fifteen, P4 ten, P3 eight, P2 four and P5 three.
P2, P3 and P5 are implications that only a match can fail, so they
catch the edits that wrongly accept, and P4 needs an edit that treats
the two ends of a query differently: the order-blind M13 and M14 escape
both, and only the statement sees them. M3 skips the pattern's first
letter, which read backwards is its last, so the two readings disagree
and P4 sees it. The checks draw a random number for every query whatever the
answers, so every mutant sees the same queries and their counts can be
compared.

Fifteen other edits were tried and set aside. Two change no answer.
Split no longer comparing the first capital: a pattern word's capital is
its first letter, and the query's word holds a capital only at its
start, so the test that the pattern word's letters appear in order in
the query's already compares them. Skeleton comparing only the number
of capitals: with the pattern a subsequence of the query, its capitals
land on capitals of the query in order, so the same number means the
same capitals. The other thirteen were killed too, beyond three per
arm, in four families that fail alike and four on their own: three
accepting capitals after the pattern is used up (★ ending its walk at a
stray capital without failing, ★ reading nothing after the pattern is
used up, split allowing extra words), two accepting capitals before it
starts (backward reading nothing before the pattern is used up, dp
letting capitals in before the pattern), two reading the query and the
pattern in opposite directions (★ walking the query backwards, backward
walking the pattern forwards), and two answering no to everything (dp
with the empty start never true, skeleton taking the query's small
letters for its capitals); and backward skipping the pattern's last
letter, split with no first word for small letters before a capital,
which panics out of bounds, dp making the pattern's last letter
optional, and skeleton testing only the subsequence.

## Verification

Every arm prints the same output as `camel_match.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with
no error; the differential prints its line under all three. `karac
check --output=json` reports no diagnostic for the five arms, the
differential and the bench program. `karac run` and a `karac build`
binary print the same output for every arm and the differential. The
release build is kara `56c60bdf7c`, with runtime archives rebuilt at
`ce706dd131`, the last commit before it to change the runtime. Under
`karac __mir-run` the arms take 2.7 s (★) to 18.4 s (dp).

Writing this kata turned up one compiler gap, in the skeleton arm, and
the Mend loop is how it surfaced:

- The first draft compared the capitals with
  `query.chars().filter(..).collect::[String]() == capitals`. `karac
  check` refuses the turbofish (`::<..>` is Rust's; Kāra has no
  call-site type arguments) and says to annotate the binding instead,
  and `karac fix` applies that as a machine fix by deleting the type
  arguments. What it leaves, `.collect() == capitals`, passes `karac
  check` with no diagnostic and then fails in the MIR builder under
  every backend: `an expression whose type does not lower
  (UnsolvedParam("C"))`. The comparison cannot fix `collect`'s result
  type, since `PartialEq` takes a right-hand type of its own, so the
  spec's answer is a refusal at check time; filed in kara as
  `B-2026-10-29-36`. The arm binds the capitals as the diagnostic says,
  `let caps: String = ...collect();`, and compares the binding.
- The harness first built letters with `char.from_u32(n)`, Rust's name,
  which `karac check` refuses with a pointer to `char.try_from(n)`; that
  diagnostic has no machine fix, since `try_from` returns a `Result`
  where `from_u32` would return an `Option`, and the harness follows it.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench builds 500 random cases of LeetCode's sizes once in all five
languages, each a pattern of 1 to 100 letters (a capital at each place
with probability 2/8) and 100 queries of up to 100 letters, 3,156,737
query letters in all: half grown from the pattern by putting in
letters, a capital among them with probability 1/8 per letter, and half
drawn at random. It answers every case 150 times with the ★ arm,
folding the matches into a count and a checksum of their positions.
About one query in eight matches. Rust and Kāra collect the pattern
into a `Vec` of `char`s per call and walk each query's `chars()`, Go
ranges over runes against a `[]rune`, and C compares bytes. Every
implementation prints `500 cases, 3156737 query letters, 150 rounds:
928050 match, checksum 983364289`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.448 to 0.539 s | 0.472 s |
| Rust (`rustc -O`) | 0.496 to 0.547 s | 0.520 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.518 to 0.613 s | 0.544 s |
| Go | 0.556 to 0.616 s | 0.587 s |
| Python | 9.6 s | |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.593 to 0.667 s | 0.641 s |
| Kāra (`karac build`) | 0.583 to 0.683 s | 0.611 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(its user time stays below its real time) and runs as fast as the
sequential one.

v2 took 1.18 times Rust's median time under overflow checks and 1.36
times C's. The times include building the cases once, several million
random numbers; we did not measure how the time divides between that
and the matching, or where Kāra's gap goes.
