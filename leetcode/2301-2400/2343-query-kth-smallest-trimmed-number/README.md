# 2343. Query Kth Smallest Trimmed Number

You are given a **0-indexed** array of strings `nums`, where each string
is of **equal length** and consists of only digits.

You are also given a **0-indexed** 2D integer array `queries` where
`queries[i] = [k_i, trim_i]`. For each `queries[i]`, you need to:

- **Trim** each number in `nums` to its **rightmost** `trim_i` digits.
- Determine the **index** of the `k_i`th smallest trimmed number in
  `nums`. If two trimmed numbers are equal, the number with the
  **lower** index is considered to be smaller.
- Reset each number in `nums` to its original length.

Return *an array* `answer` *of the same length as* `queries`, *where*
`answer[i]` *is the answer to the* `i`th *query*.

**Note:** To trim to the rightmost `x` digits means to keep removing
the leftmost digit, until only `x` digits remain. Strings in `nums` may
contain leading zeros.

```
nums = ["102","473","251","814"], queries = [[1,1],[2,3],[4,2],[1,2]]   ->  [2,2,1,0]
nums = ["24","37","96","04"], queries = [[2,1],[2,2]]                    ->  [3,0]
```

**Constraints:** `1 <= nums.length <= 100`;
`1 <= nums[i].length <= 100`; `nums[i]` consists of only digits; all
`nums[i].length` are equal; `1 <= queries.length <= 100`;
`queries[i].length == 2`; `1 <= k_i <= nums.length`;
`1 <= trim_i <= nums[i].length`.

Every number has the same width, so two trimmed numbers have the same
number of digits, leading zeros kept, and compare as integers exactly
as their text compares. The numbers run to 100 digits, past any
integer type, so the text is what is compared.

## Approaches

| file | mechanism |
|---|---|
| `trimmed.kara` ★ | for each query the indices sorted by `sort_by_key` on (trimmed text, index), and the k-th taken. O(m n log n) comparisons |
| `trimmed_radix.kara` | radix sort: the order for each trim from the order for one digit fewer, by a stable counting sort on the next digit to the left, read through `bytes()`; each query reads its order. O(width (n + 10) + m) |
| `trimmed_naive.kara` | by rank: each index's rank the number of trimmed numbers before its own, smaller or equal and earlier, and the index of rank k - 1 the answer. O(m n^2) comparisons |
| `trimmed_heap.kara` | a `PriorityQueue.max_first()` of (trimmed text, index), the largest popped whenever more than k are held, so the largest kept is the k-th. O(m n log k) |
| `trimmed_iter.kara` | iterators: the numbers `enumerate`d and `map`ped to (trimmed text, index), `collect`ed and sorted, and the k-th read with `nth` |
| `trimmed_solution.kara` | LeetCode's Rust template: a `Vec<usize>` of indices sorted by `sort_by` with `&a, &b` patterns, the trimmed slices compared with `cmp` and ties broken with `then`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; one number;
three equal numbers; 100 numbers of 100 digits under 100 queries, with
the answers' sum and the first and last; then 2000 random cases of 1 to
10 numbers of 1 to 6 digits from an alphabet of 2 to 10 under 1 to 5
queries, with a checksum and the answers' sum. `trimmed.py` mirrors the
★ arm and its output is byte-identical.

The radix arm was first written `s.bytes().collect()`; `bytes()` is a
`Slice[u8]`, and `karac fix` put in the `.iter()` an adaptor needs, one
edit. The naive arm was first written with `a.byte_at(p)`, after
`char_at`, comparing digit by digit; there is no `byte_at`, and `karac
check` said only that, with no word of `a.bytes()[p]` (B-2026-11-21-38,
fixed: it now names `.bytes()[i]` and `char_at`, and fixes the call to
the first). The arm now
compares the trimmed `Str`s with `<`, which is also faster under the
interpreter.

`karac fix` carries the template in one call, reporting 23 edits.
`check` first reports 13 errors and offers 20 edits for them: the
twelve brackets of the five `Vec<..>`; the four `&` of the patterns
`&a`, `&b` and the two `|&x|` dropped; the two `&` of the arguments
`&nums[b][..]` and `&b` dropped; `struct Solution;` to
`struct Solution {}`; and `Solution::` to `Solution.` in the harness's
wrapper. The other three follow from those: the two `as usize` to
`as i64` and the `Vec[usize]` of indices to `Vec[i64]`, since an index
is an `i64`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each number trimmed to its rightmost `trim` digits and read
as the integer it is, and the smallest (number, index) taken out `k`
times, the `k`-th taken out the answer. No sorting and no text
comparison. It checks 300 random cases of 1 to 8 numbers of 1 to 6
digits from an alphabet of 2 to 10 under 1 to 4 queries; then 30 of up
to 30 numbers of up to 18 digits under up to 10 queries; then 30 of up
to 100 numbers of up to 100 digits, past what an integer holds. All 360
are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 18 digits, the answers are the literal reading's |
| P2 | for the first query's trim, the answers for `k` = 1 to `n` are every index once, their trimmed numbers never falling |
| P3 | a digit put before every number: the same answers |
| P4 | a number of zeros put first: each `k` one later gives the index one later |
| P5 | a number of nines put last: the same answers |
| P6 | each arm agrees with at least three of the other five |

P3 holds because no trim reaches the new first digit. P4 holds because
the zeros are no larger than any trimmed number and come first in
index, so they are the smallest at every trim and push every other
place one on; P5 because the nines are no smaller than any trimmed
number and come last, so they come after every other. `karac fix`
dropped twelve `.clone()`s of vectors passed to parameters that only
borrow them.

The differential prints `360 cases: checksum 988313234, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and sorts by `int` of each tail. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the numbers trimmed from the left | P1 186, P2 175, P3 162, P6 215 |
| M4 | ★: the sort left out | P1 245, P2 281, P6 274 |
| M6 | ★: the k-th largest | P1 280, P2 318, P4 360, P5 360, P6 310 |
| M7 | radix: each digit placed from the back of the last order | P1 192, P2 148, P4 136, P5 8, P6 222 |
| M8 | radix: the digits read from the left | P1 204, P2 229, P3 274, P6 232 |
| M10 | radix: the first order by falling index | P1 123, P4 61, P5 5, P6 132 |
| M13 | naive: every equal number counted before | P1 330, P2 360, P4 159, P6 360 |
| M14 | naive: the rank one too many | P1 330, P2 360, P5 173, P6 360 |
| M16 | naive: index 0 never counted before | P1 226, P4 297, P5 173, P6 253 |
| M18 | heap: one more kept than k | P1 272, P2 323, P5 173, P6 302 |
| M19 | heap: the whole number pushed, untrimmed | P1 184, P2 170, P6 213 |
| M20 | heap: nothing popped while pushing | P1 272, P2 323, P5 360, P6 302 |
| M23 | iter: the numbers cut after the k-th place | P1 200, P2 213, P3 205, P6 228 |
| M24 | iter: every index read as 0 | P1 271, P2 323, P4 360, P6 300 |
| M26 | iter: each index read from the other end | P1 284, P2 312, P4 360, P5 360, P6 314 |
| M28 | solution: the numbers compared in falling order | P1 280, P2 318, P4 347, P5 359, P6 310 |
| M31 | solution: one digit fewer kept | P1 245, P2 277, P6 275 |

P1 and P6 kill all seventeen, P2 fifteen, P5 nine, P4 eight and P3
three. P2 misses only the two edits that still list every index once in
the order of its trimmed number and differ only among equal ones: the
radix arm's first order by falling index, and the naive arm's index 0
never counted before. P3, a digit put before every number, fails only
the edits that read the front of a number: trimmed from the left, the
digits read from the left, the numbers cut after the k-th place. P4 and
P5, zeros put first and nines put last, fail the edits that misplace the
smallest or largest trimmed numbers or break ties the wrong way: the
k-th largest, each digit placed from the back, the first order by
falling index, every equal number counted before, index 0 never counted
before, an index read as 0 or from the other end, and the numbers
compared in falling order; P5 also fails the edits that keep or rank
one too many, which a run of nines at the end exposes.

Of the thirty-one, fourteen were not kept. Two crash under both
backends: the radix arm's digit counted at its own slot (M9) and the
heap arm's every kept number dropped at the k-th (M21), each with an
index out of bounds. Ties broken by the larger index in the ★ arm (M1)
and the template (M27), and ties counted from the later index in the
naive arm (M12), fail as the radix arm's first order by falling index
(M10); one digit fewer kept in the ★ arm (M3) and the order for one
digit fewer read in the radix arm (M11) as one digit fewer in the
template (M31); the sort left out of the iter arm (M22) as in the ★ arm
(M4); the smallest popped first in the heap arm (M17) as the k-th
largest in the ★ arm (M6); and the numbers trimmed from the left in the
template (M29) as in the ★ arm (M2). Always the smallest in the ★ arm
(M5) and the template (M30) fail alike and apart from every kept one,
as do the naive arm's other number trimmed one shorter (M15) and the
iter arm's n-th read as the first (M25); they were left out to keep
three to an arm and two to the template.

## Verification

Every arm prints the same output as `trimmed.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.58 to 1.07 s but the naive
arm, which ranks every number against all the others, 3.1 s. The
differential takes 32.5 s there and 0.9 s under `karac
__mir-llvm-run`.

## Benchmarks

The bench builds 10 cases of 100 numbers of 100 digits under 100
queries once, from a scramble that never repeats, then makes 50 passes,
pass `p` folding each answer plus `p` into the checksum, with the ★ arm
in all five languages. Every implementation prints `50 passes over 10
cases of 100 numbers of 100 digits under 100 queries: checksum
174033010`. Kāra and Rust sort by an owned key, the trimmed text copied
into a `String` with the index; C and Go compare the tails in place,
and Python's `sorted` builds each element's key once.

BENCHTAB
