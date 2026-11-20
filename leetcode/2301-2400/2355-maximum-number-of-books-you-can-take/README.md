# 2355. Maximum Number of Books You Can Take

You are given a **0-indexed** integer array `books` of length `n` where
`books[i]` denotes the number of books on the `i`th shelf of a
bookshelf.

You are going to take books from a **contiguous** section of the
bookshelf spanning from `l` to `r` where `0 <= l <= r < n`. For each
index `i` in the range `l <= i < r`, you must take **strictly fewer**
books from shelf `i` than shelf `i + 1`.

Return *the **maximum** number of books you can take from the
bookshelf.*

```
books = [8,5,2,7,9]               ->  19
books = [7,0,3,4,5]               ->  12
books = [8,2,3,7,3,4,0,1,4,3]     ->  13
```

**Constraints:** `1 <= n <= 10^5`; `0 <= books[i] <= 10^5`.

Taking from a run ending at `r`, it is best to take all of shelf `r`
and, going left, the lesser of what a shelf holds and one fewer than
the shelf after it. Taking `books[i]` from shelf `i`, the shelves to its
left give one fewer each until one, `j`, holds fewer than that, which is
where `books[j] - j < books[i] - i`; from there the run continues as the
best run ending at `j`. A run of 10^5 shelves can hold
`5 * 10^9` books, past `i32`, which is why LeetCode's answer is an
`i64`.

## Approaches

| file | mechanism |
|---|---|
| `books.kara` ★ | a monotonic stack increasing in `books[k] - k`: its top is the nearest shelf `j` that caps the run at `i`, and the best run ending at `i` is the falling sum down to `j` plus the best ending at `j`. O(n) |
| `books_naive.kara` | every right end, walking left with the falling take until a shelf would give nothing. O(n m) for `m` the most books on a shelf |
| `books_scan.kara` | the stack's recurrence, the cap found by scanning left from `i` while the falling take is still above 0. O(n m) |
| `books_jumps.kara` | the stack's recurrence, the cap found through a table of each shelf's own cap: a shelf that does not cap `i` cannot be passed by anything between it and its own cap, so the search jumps there. O(n) amortized, with no stack |
| `books_iter.kara` | iterators: for each right end, the shelves to its left by `rev`, the falling take carried by `scan` and stopped by `take_while`, summed; the best by `max` |
| `books_solution.kara` | LeetCode's Rust template: the ★ arm's stack over `i32` shelves with `usize` indices, `while let Some(&top) = stack.last()` and `as i64` casts; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples; one empty
shelf; 2000 shelves rising by one, and falling; `10^5` shelves of up to
`10^5` books every 50th and up to 200 between; then 2000 random arrays
of 1 to 30 shelves of 0 to 1 up to 0 to 40 books, with a checksum and
the answers summed. `books.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked against every range walked
from its right end on 3000 random arrays.

The scan arm was first written to scan left until it found the cap or
ran out of shelves. A shelf of few books, `b`, can be capped only by a
shelf within `b` of it, so on the line of `10^5` shelves it scanned to
the start for nearly every shelf, `5 * 10^9` steps, and the interpreter
took 98 s. It now stops once the falling take reaches 0, as the naive
arm's walk does.

The iter arm was first written with `.sum::<i64>()` inside the `map`.
`check` refuses the turbofish, which Kāra does not have, and says to
annotate a binding instead; the sum is now `let left: i64`.

`karac fix` carries the template in one call, reporting 21 edits.
`check` first reports 7 errors, each with its edit: `struct Solution;`
given braces, the angle brackets of `Vec<i32>` and `Vec<usize>` made
square, `Vec::new` and the `::` call written with `.`, and the two
`Some(&top)` and `Some(&j)` patterns made `Some(top)` over
`.cloned()`. The rest follow: `vec![0i64; n]` made `Vec.filled(n, 0)`,
`usize` made `i64`, the `i64` suffixes dropped, and every `as i64` on an
index dropped, since an index is already an `i64`; `books[top] as i64`
went with them, the `i32` shelf widening to the `i64` it is subtracted
from. `let b = books[i] as i64` stands. The edit to
`((i + 1) as i64).min(b)` leaves `((i + 1)).min(b)`, its parentheses
doubled, as the
template here keeps them; `karac fmt` would print `(i + 1).min(b)`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every range of shelves from `l` to `r`, all of shelf `r`
taken and each shelf to its left the lesser of what it holds and one
fewer than the shelf after it; a range whose leftmost take would fall
below 0 is not allowed. No caps, no recurrence. It checks 300 random
arrays of 1 to 30 shelves of 0 to 1 up to 0 to 40 books; then 30 of up
to 400 shelves of up to `10^5`; then 30 of up to 300 shelves rising by 0
to 2 with random dips. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 30 shelves, the answer is the literal reading's |
| P2 | from the most books on one shelf to all the books |
| P3 | an empty shelf put before the first and after the last: the same answer |
| P4 | the shelves given twice over with an empty shelf between: the same answer |
| P5 | every shelf given one more book: from the answer to the answer plus the number of shelves |
| P6 | each arm agrees with at least three of the other five |

P4 holds because no run can cross an empty shelf from the right: taking
0 there leaves nothing strictly fewer for the shelf before it. P5's
upper bound holds because the best run with one more book on every
shelf, each take lowered by one, is a run of the original shelves, less
at most one book a shelf.

The differential prints `360 cases: checksum 569342498, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and walks every range. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a shelf whose key is one less popped too | P1 109, P2 5, P3 26, P4 26, P6 132 |
| M4 | ★: the falling sum one short per shelf | P1 242, P2 5, P3 122, P6 291 |
| M5 | ★: no shelf ever pushed | P1 257, P2 147, P3 233, P4 240, P6 306 |
| M7 | naive: the walk stopped at a take of 2 | P1 98, P5 1, P6 128 |
| M10 | naive: the first shelf never reached | P1 98, P3 124, P4 124, P6 124 |
| M11 | naive: an equal take allowed | P1 251, P5 35, P6 307 |
| M12 | scan: the scan stopped a shelf early | P1 169, P5 147, P6 204 |
| M13 | scan: a shelf whose key is one less passed over | P1 107, P2 3, P3 19, P4 19, P6 130 |
| M15 | scan: an uncapped run not stopped at the first shelf | P1 179, P2 103, P3 207, P5 137, P6 207 |
| M17 | jumps: a jump past the cap's cap | P1 192, P2 2, P3 116, P4 130, P6 237 |
| M18 | jumps: every cap recorded as none | P1 201, P2 50, P3 191, P4 206, P6 247 |
| M19 | jumps: a capped run one shelf short | P1 242, P2 37, P3 133, P6 291 |
| M22 | iter: the walk stopped at a take of 1 | P1 144, P5 4, P6 174 |
| M24 | iter: the left shelves walked from the left | P1 242, P3 300, P4 126, P6 298 |
| M25 | iter: the right end not counted | P1 302, P2 74, P6 358 |
| M29 | solution: the cap's best added twice | P1 245, P2 111, P5 208, P6 301 |
| M30 | solution: an empty shelf never pushed | P1 104, P2 12, P3 169, P4 226, P5 78, P6 104 |

P1 and P6 kill all seventeen, P2 and P3 eleven each, P4 eight and P5
seven. P5, a book more on every shelf, fails the edits that end a walk
or a scan at the wrong take (M7, M11, M12, M15, M22) and two of the
template's, since the extra book moves where every walk ends; the naive
arm's walk stopped at a take of 2 fails it on a single case. P4, the
shelves twice over with an empty shelf between, fails the edits that let
a run reach across that shelf, popping, passing over or never recording
a shelf that should cap it, and those that lose the first shelf or walk
the wrong way, which the copy then shows in the middle.

Of the thirty-one, fourteen were not kept, and two first written were
replaced. A shelf of equal key kept as a cap, in the ★ and scan arms,
killed nothing: a shelf `j` with `books[j] - j = books[i] - i` holds
exactly the take the falling run from `i` would want there, so stopping
at `j` and adding the best run ending at `j` gives the same total as
walking on. The two now pop or pass over a shelf whose key is one less
(M1, M13). The cap's own best never added in the ★ arm (M2) and half
of it added in the scan arm (M14) fail alike; a shelf's own books
ignored on the naive arm's walk (M8) fails as no shelf ever pushed
(M5), both taking every right end down to 0 as if no shelf capped it;
the naive arm's right end not counted (M9) as the iter arm's (M25); and
books compared without their places in the jumps arm (M21) as in the
template (M28). The ★ arm's uncapped run not stopped at 0 books (M3)
and last run kept (M6), the scan arm's first shelf never a right end
(M16), the jumps arm's cap shelf's books added (M20), the iter arm's
equal take allowed (M23) and walk started one book short (M26), and the
template's uncapped run one book short (M27) and shelf read one book
higher (M31) fail apart from every kept one; they were left out to keep
three to an arm and two to the template.

## Verification

Every arm prints the same output as `books.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the jumps, ★ and template arms take 0.6 to
1.2 s, the scan and naive arms 1.6 and 2.4 s, and the iter arm 17.6 s:
it does the naive arm's walk, about `10^7` steps on the line of `10^5`
shelves, but through a chain of five iterator adapters per step, where
the naive arm runs one loop. Compiled, the two take 0.32 and 0.25 s.
The differential takes 22 s under `karac __mir-run`, most of it the
iter and naive arms on the arrays of up to 400 shelves of up to `10^5`,
and 0.50 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 arrays of `10^5` shelves once, array `a` holding up
to `10^5` books on every `(a + 2)^2`-th shelf and up to `100 (a + 1)`
between, then makes 50 passes, pass `p` folding each answer, taken mod
`10^9 + 7`, plus `p` into the checksum, with the ★ arm in all five
languages. Every implementation prints `50 passes over 10 arrays of
10^5 shelves: checksum 471286283`. Each call allocates its own table of
bests and its stack, but C, which keeps both in static arrays.

BENCHTAB
