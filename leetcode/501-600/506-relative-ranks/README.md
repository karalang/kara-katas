# 506. Relative Ranks

You are given an integer array `score` of size `n`, where `score[i]` is
the score of the `i`th athlete in a competition. All the scores are
guaranteed to be unique.

The athletes are placed based on their scores, where the 1st place
athlete has the highest score, the 2nd place athlete has the 2nd
highest score, and so on. The placement of each athlete determines
their rank:

- The 1st place athlete's rank is `"Gold Medal"`.
- The 2nd place athlete's rank is `"Silver Medal"`.
- The 3rd place athlete's rank is `"Bronze Medal"`.
- For the 4th place to the `n`th place athlete, their rank is their
  placement number (i.e., the `x`th place athlete's rank is `"x"`).

Return an array `answer` of size `n` where `answer[i]` is the rank of
the `i`th athlete.

```
score = [5,4,3,2,1]   ->  ["Gold Medal","Silver Medal","Bronze Medal","4","5"]
score = [10,3,8,9,4]  ->  ["Gold Medal","5","Bronze Medal","Silver Medal","4"]
```

**Constraints:** `n == score.length`; `1 <= n <= 10^4`;
`0 <= score[i] <= 10^6`; all the values in `score` are unique.

## Approaches

Every arm is `fn find_relative_ranks(score: Vec[i64]) -> Vec[String]`.

| file | mechanism |
|---|---|
| `find_relative_ranks.kara` ★ | the indices sorted by score, highest first (`order.sort_by_key(\|i\| -score[i])`); the k-th index in that order is the athlete in place k + 1, and a `match` on the place gives the medal or `f"{place + 1}"`. O(n log n) |
| `find_relative_ranks_heap.kara` | every athlete pushed onto a `PriorityQueue.max_first()` as (score, index) and popped off highest first, the k-th pop taking place k; the numbers come from `place.to_string()` |
| `find_relative_ranks_buckets.kara` | the scores are whole numbers up to 10^6, so a `Vec` indexed by score holds who scored it, sized by `*score.iter().max().unwrap()`; walking it from the top score down meets the athletes in place order. O(n + max score) |
| `find_relative_ranks_count.kara` | one `map` over the scores: an athlete's place is one more than the scores above it, counted with a `filter` over all of them. O(n^2), no sorting |
| `differential.kara` | the four arms on 1,500 random lists, five properties |

Every arm prints the same 7 lines: the two LeetCode examples, one
athlete, two, rising scores, the extremes 0 and 10^6, and for 300
random lists of 1 to 30 different scores (spread 3, 1,000 or 33,000
apart in turn, shuffled) the count of athletes and a checksum of the
ranks' characters. `find_relative_ranks.py` mirrors the ★ arm and its
output is byte-identical.

The harness reads each character's code as `let code: i64 = ch as
i32;`, the spec's form (a `char` casts to `i32`, and widening to `i64`
is implicit at a binding). Until kara B-2026-10-13-21 was fixed
(below), the v2 backends never widened that cast: `karac __mir-run`
refused every arm as written, and `karac __mir-llvm-run` printed the
right output only because the upper half of the slot happened to hold
zeros. The differential and mutants below were run then, on copies
whose harness wrote `let code = ch as i32 as i64;`. Every arm was
rechecked as written at kara `e85c10e377`, after the fix.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random lists of 1 to 12 different scores: the j-th is j * spread
plus less than spread, shuffled, with spread 1, 3 or 1,000 in turn.

| | property |
|---|---|
| P1 | the ranks are the reference's, which places the athletes by selection, the highest score not yet placed each round |
| P2 | every place from 1 to n is named exactly once |
| P3 | three times every score plus 7 keeps the ranks |
| P4 | the athletes in reverse order get their ranks reversed |
| P5 | every score taken from the highest turns place p into place n + 1 - p |

To read a rank back as a place, the differential matches on
`i64.parse(rank)` with `Ok` and `Err`, the spec's form, which the
implementation does not have yet (kara B-2026-10-12-6, below). It was
run on a copy that matches `Some` and `None` instead, which prints
`1500 cases, 4 arms, 30000 checks, 0 failures` under `karac __mir-run`.

## Mutation testing

Ten edits to the copy of `differential.kara`, two to each arm and two
equivalent ones, each run under `karac __mir-run`. All eight
non-equivalent ones are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: sorted lowest first (`\|i\| score[i]`) | P1 1358 |
| M2 | ★: the places after the medals are one too small (`f"{place}"`) | P1 1096, P2 1096, P5 1096 |
| M3 | heap: smallest-first (`PriorityQueue.new()`) | P1 1358 |
| M4 | heap: second place gets `"Bronze Medal"` | P1 1358, P2 1358, P5 1358 |
| M5 | buckets: a score of 0 is never reached (`while s > 0`) | P1 676, P2 676, P3 676, P5 1500 |
| M6 | buckets: `who` holds the index, not one more than it | P1 1500, P2 1500, P4 1358, P5 1500 |
| M7 | count: an athlete counts itself (`*t >= s`) | P1 1500, P2 1500, P5 1500 |
| M8 | count: places start at 0 | P1 1500, P2 1500, P5 1500 |
| E1 | buckets: one bucket more (`top + 2`) | 0 |
| E2 | ★: every rank starts as `"?"` | 0 |

E1 is equivalent because no score is above `top`, so the extra bucket
stays empty. E2 is equivalent because every athlete gets a place, so
every starting rank is written over.

M1 and M3 are the same wrong answer, the lowest score first, written
into two arms, and fail the same 1,358 cases, every list of two or
more. Only P1 sees them: ranking from the bottom still names each place
once, ignores how far apart the scores are and which order they come
in, and turns over exactly as P5 expects when the scores do. M2 and
M4 name a place twice, so P2 sees them, and so does P5, since the
place of the athlete turned over is then wrong too; M2 does so only
from four athletes on (1,096 cases). M5 drops the athlete who scored 0,
in the 676 lists that hold a 0, and P5 sees it in all 1,500, because
turning the scores over always puts someone on 0. P3 sees it because
three times every score plus 7 has no 0, so the stretched list is
ranked right. M6 makes athlete 0 invisible and shifts the others' ranks
one place left, so the result depends on where in the list each
athlete is, which P4 sees. M7 and M8 are the count arm one place off,
one each way: every rank is wrong but the order is kept, and P2 and
P5 see both.

## Verification

All four arms print the same output as `find_relative_ranks.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak, as written. The copy of the differential described under
Differential prints `30000 checks, 0 failures` on both and runs clean
under the third. `karac check` passes on the ★, heap and count arms
and the bench program. On the buckets arm it passes with
`KARAC_CHECK_LIBRARY=1`, and default `karac check` refuses
`*score.iter().max().unwrap()` (see Compiler findings). It refuses the
differential for that and for the `Ok` and `Err` patterns, which no
check passes.

On the frozen legacy backends, the ★ and heap arms agree: `karac run
--interp`, LLJIT, legacy `karac build` and a `KARAC_AUTO_PAR=1` build
print the same output, the harness's cast included. The buckets and
count arms are refused by all three at type checking: legacy types an
iterator's items by value, so it refuses the buckets arm's
`*score.iter().max().unwrap()` and the count arm's `*t` in its
`filter`, both "unary '*' requires 'ref T' ... found 'i64'". The
differential is refused too: by `karac run --interp` at
`place_of(other[i])` ("cannot move out of an index expression"), which
v2 reads as a borrow, and by legacy `karac build` at the same `*` as
the buckets arm. Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 500 lists of 10,000
athletes (the problem's most), all different scores from 0 to 10^6
(the j-th is j * 100 plus less than 100, shuffled), once. Then it ranks
each list once, folding the length of every rank into a checksum.
Every implementation prints `500 lists of 10000 athletes: 19462500
characters, checksum 77294114`, the Kāra program under `karac
__mir-run` included (in 26 s).

Every mirror sorts the indices by score, highest first, and makes a
fresh string for every rank, as the ★ arm's `match` gives a fresh
`String`: Rust a stable `sort_by_key` and `to_string` or `format!`, Go
`slices.SortStableFunc` and `strconv.Itoa`, Python `sorted` and an
f-string, and C `qsort` (the scores are all different, so a stable
sort is not needed) and `strdup`. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.03 to 1.11 s |
| Rust (`rustc -O`) | 0.58 to 0.69 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.56 to 0.67 s |
| Go | 1.44 to 1.52 s |
| Python | 5.4 s |
| Kāra (`karac build --mir`) | 1.06 to 1.17 s |

The sort calls its key closure through a function pointer for every
comparison (kara B-2026-10-13-18, filed from kata 502), and each place
from 4 on is an f-string, which costs three allocations on the v2
backend (kara B-2026-10-13-20, filed from kata 504).

The legacy `karac build` refuses this program: "cannot move out of an
index expression", on `find_relative_ranks(all[c])`, which v2 reads as
a borrow. So `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`486f47f97d`. Under `karac __mir-llvm-run` the program prints the same
line in 5.8 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

kara B-2026-10-13-21 (miscompile, fixed in kara `64dbf3323c`): an
`as` cast to a narrower integer that lands in a wider binding or
return slot was never widened. The harness's `let code: i64 = ch as
i32;` made `karac __mir-run` stop at "invalid MIR: assigning i32 to
_106 of type i64". On `karac __mir-llvm-run` the four bytes of the
`i32` went into an 8-byte slot whose other four held whatever was
there. In this program that was zero and the output came out right
(five runs of the ★ arm as written, all right), but in the row's
three-line program the same cast printed 94505382909996 for 44. `karac
check` passed it, and `karac run --interp` got it right. The same cast
as an argument, a `Vec` element or a field was right on both v2
backends. Since the fix every arm runs right as written on both v2
backends.

Two existing rows show up here too.

kara B-2026-10-12-6 (open, from kata 388): `i64.parse` returns
`Option[i64]` where the spec gives `Result[i64, ParseError]`, so the
differential's `match i64.parse(rank) { Ok(p) => ..., Err(_) => 0 }`,
the spec's form, is refused by `karac check` and every backend.

The buckets arm sizes its `Vec` with `*score.iter().max().unwrap()`:
the spec gives `v.iter().max()` as an `Option[ref i64]`. It runs on
both v2 backends and passes `karac check` with `KARAC_CHECK_LIBRARY=1`,
but default `karac check` types the item by value and refuses the `*`.
As for katas 495 and 502, default `karac check` does not see the Kāra
library's iterator types; kara B-2026-10-12-23 was closed in
`7609de871d` for serde programs only.
