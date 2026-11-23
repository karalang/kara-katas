# 2512. Reward Top K Students

You are given two string arrays `positive_feedback` and
`negative_feedback`, containing the words denoting positive and
negative feedback, respectively. Note that **no** word is both positive
and negative.

Initially every student has `0` points. Each positive word in a
feedback report **increases** the points of a student by `3`, whereas
each negative word **decreases** the points by `1`.

You are given `n` feedback reports, represented by a **0-indexed**
string array `report` and a **0-indexed** integer array `student_id`,
where `student_id[i]` represents the ID of the student who has received
the feedback report `report[i]`. The ID of each student is **unique**.

Given an integer `k`, return *the top* `k` *students after ranking them
in **non-increasing** order by their points*. In case more than one
student has the same points, the one with the lower ID ranks higher.

```
positive = ["smart","brilliant","studious"], negative = ["not"],
report = ["this student is studious","the student is smart"],
student_id = [1,2], k = 2      ->  [1,2]
report = ["this student is not studious","the student is smart"]
                               ->  [2,1]
```

**Constraints:** `1 <= positive_feedback.length,
negative_feedback.length <= 10^4`; `1 <= positive_feedback[i].length,
negative_feedback[j].length <= 100`; both consist of lowercase English
letters; no word is present in both; `n == report.length ==
student_id.length`; `1 <= n <= 10^4`; `report[i]` consists of lowercase
English letters and spaces `' '`; there is a single space between
consecutive words of `report[i]`; `1 <= report[i].length <= 100`; `1 <=
student_id[i] <= 10^9`; all the values of `student_id[i]` are unique;
`1 <= k <= n`.

Each report's score is a sum over its words, and the ranking is an
order on (score, id) pairs, higher score first and the lower id at a
tie. The approaches differ in how a word's kind is asked and how the
students are ranked.

## Approaches

| file | mechanism |
|---|---|
| `reward.kara` ★ | the positive and the negative words each in a `Set[String]`, asked with the `Str` of each word `split` from a report; the (-score, id) pairs sorted, and the first k taken. O(total length + n log n) |
| `reward_sorted.kara` | the words in two sorted `Vec`s, asked by `binary_search`; the students' places ordered by `sort_by` with a comparison on score, then id |
| `reward_heap.kara` | every word's weight in one `Map`, 3 or -1; each (-score, id) pushed into a least-first `PriorityQueue`, and k popped |
| `reward_rec.kara` | recursions: a report's score from word `w` on, and a merge sort of the (-score, id) pairs. The score at most 50 deep, the sort about 14 |
| `reward_iter.kara` | iterators: each report's words `map`ped to their weights and `sum`med, `zip`ped with the ids, `collect`ed, sorted, and k `take`n |
| `reward_solution.kara` | LeetCode's Rust template: `Vec<String>` three times and `Vec<i32>` in, `Vec<i32>` out; the words in two `HashSet<&str>`, each report's `split_whitespace` folded into a score, and the pairs ordered by `sort_by` with `then`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and four
more; then 2000 random cases of 1 to 12 reports of 1 to 8 words, from
a vocabulary of 6 with ids to 30 and of 60 with ids to `10^9`, each as a
checksum of the rankings; then the constraints' largest: `10^4` reports
of 1 to 20 words from 400, ids to `10^9` and k of `10^4`; and `10^4`
copies of the first report, k of 5000, every student tied. `reward.py`
mirrors the ★ arm and its output is byte-identical, and the mirror was
checked on 3000 random cases of 1 to 8 reports against scores counted
word by word and k rounds that each take the best student left, and the
two agreed on every case.

The sorted arm was first written with each word turned into a `String`,
`let w = word.to_string();`, and asked of both lists in turn,
`good.binary_search(w)` and then `bad.binary_search(w)`. `check` refused
the second with E0500, `w` moved by the first: `binary_search` was
missing from the list of searches whose argument the ownership check
counts as borrowed, beside `contains`, although its `val: T` is a
borrow. That is B-2026-11-23-65, fixed in the compiler. The arm now asks with
the `Str` itself, which a search over a `Vec[String]` takes as the
element's view (collections.md), as the ★ arm's `Set.contains` does.

`check` first reports 15 errors on the template: the `use
std::collections::HashSet;` line, `struct Solution;`, six `Vec<..>` and
two `HashSet<..>` in angle brackets, the two `&str`, the `&id` pattern,
and the two `&` borrows in `sort_by`. `karac fix` carries it in one
call, reporting 30 edits: the `use` line goes, since `Set` is in the
prelude; `struct Solution {}`; the brackets, `HashSet<&str>` becoming
`Set[Str]`; the `&` pattern and borrows dropped; `take(k as usize)`
becomes `take(k)`; and the wrapper's `.clone()`s, which the `Vec`
arguments do not need, dropped. `split_whitespace`, `fold` and the
`.then(..)` ordering stand.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each report's score counted word by word against every
feedback word in turn, 3 for each positive match and -1 for each
negative one; then k rounds, each taking the student not yet taken with
the highest score, the smaller id at a tie. No set is built and nothing
is sorted. It checks 300 random cases of 1 to 8 reports of 1 to 6 words
from 3 to 8 one-letter words, ids to 40; then 20 of one report; and 40
of 12 reports of one positive and one negative word each, so every
student ties. All 360 are drawn before any arm answers, and 129 of them
ask for every student.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | k ids, distinct, every one a student's |
| P3 | the reports and their ids in the other order: the same answer |
| P4 | every report's words in the other order: the same answer |
| P5 | every id doubled and a negative word added to every report: the answer's ids doubled |
| P6 | each arm agrees with at least three of the other five |

P5 holds because the added word lowers every score by 1 and doubling
keeps the order of the ids, so the ranking is the same students in the
same order.

The differential prints `360 cases, 129 asking every student: checksum
436436390, 12960 checks over 6 arms: 0 failures` under every lane in
Verification; the checksum of the literal answers was checked against a
Python reading that builds the same cases and sorts by (-score, id). On
a failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: the students never sorted | P1 261, P3 299, P6 261 |
| M5 | ★: the first report skipped | P1 256, P2 129, P3 245, P6 256 |
| M6 | ★: the negative words asked first | P1 231, P6 231 |
| M9 | sorted: the larger id first at a tie | P1 163, P6 163 |
| M10 | sorted: every word not positive negative | P1 53, P6 53 |
| M11 | sorted: the best student skipped | P1 360, P2 129, P6 360 |
| M14 | heap: the ids pushed in the other order | P1 242, P6 242 |
| M15 | heap: an unknown word worth 1 | P1 51, P6 51 |
| M16 | heap: one student fewer | P1 360, P2 360, P6 360 |
| M17 | rec: the best word only | P1 187, P6 187 |
| M19 | rec: the first word skipped | P1 168, P4 204, P6 168 |
| M21 | rec: the top k in the other order | P1 233, P6 233 |
| M23 | iter: the ranking taken from the end | P1 299, P6 299 |
| M25 | iter: the ids one along | P1 326, P2 129, P3 279, P6 326 |
| M26 | iter: a negative word worth 3 | P1 186, P6 186 |
| M28 | solution: ties left in report order | P1 116, P3 163, P6 116 |
| M30 | solution: a negative word worth 0 | P1 94, P6 94 |

P1 and P6 kill all seventeen, P2 and P3 four each, and P4 one, the rec
arm's first word skipped (M19).

One of the first thirty-one edits survived and was replaced: the sorted
arm's positive words left unsorted before `binary_search`. The
differential's feedback words are drawn as the first letters in order,
`a` up, so the list is sorted already and the edit changes nothing. It
became ties left in report order (M7).

Fourteen are not kept, and none survives. Four fail exactly as a kept
one: the sorted arm's ties left in report order (M7) as the template's
(M28); the rec arm's merge taking the greater (M18) as the iter arm's
ranking taken from the end (M23); the template's larger id first at a
tie (M29) as the sorted arm's (M9); and the template's best student
skipped (M31) as the sorted arm's (M11). Nine fail as one another, in
four sets: the ★ and template arms' positive word worth 2 (M1, M27);
the ★ and heap arms' negative word worth 1 (M2, M12); the ★, sorted
and iter arms' lowest score first (M3, M8, M22); and the rec arm's
positive word worth 1 and the iter arm's negative word worth -3 (M20,
M24), the same weights in the ratio 1 to -1, so the same ranking. The
heap arm's positive word worth 4 (M13) fails in a way of its own, but
its arm already holds its kept edits.

## Verification

Every arm prints the same output as `reward.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 6.1 to 8.3 s and the differential 2.3 s; under `karac __mir-llvm-asan` the arms take 1.6 to 2.0 s and the differential 1.1 s; and under `karac run` the differential takes 1.1 s.

## Benchmarks

The bench builds 100 cases of 1000 reports once from its own generator,
each with 1 to 200 positive and 1 to 200 negative words from a
vocabulary of 600, reports of 1 to 20 words, distinct ids, and k from 1
to 991; then makes 50 passes. Each pass, for every case, copies the
report at place `(check / 1000 + p) % 1000` over the one at `check %
1000`, asks, and puts it back, folding each id plus the pass into the
checksum. The bench uses the ★ arm in all five languages, each building
its two word sets afresh on every ask: Kāra's `Set`, Rust's `HashSet`,
Go's map, Python's `set`, and in C two open-addressed tables of 1024
slots probed linearly. Every implementation prints `50 passes over 100
cases of 1000 reports: checksum 661782877`.

BENCHTAB
