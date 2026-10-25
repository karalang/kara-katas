# 1000. Minimum Cost to Merge Stones

There are `n` piles of `stones` arranged in a row. The `ith` pile has
`stones[i]` stones.

A move consists of merging exactly `k` **consecutive** piles into one
pile, and the cost of this move is equal to the total number of stones
in these `k` piles.

Return *the minimum cost to merge all piles of stones into one pile*.
If it is impossible, return `-1`.

```
stones = [3,2,4,1], k = 2    ->  20
stones = [3,2,4,1], k = 3    ->  -1
stones = [3,5,1,2,6], k = 3  ->  25
```

**Constraints:** `n == stones.length`; `1 <= n <= 30`;
`1 <= stones[i] <= 100`; `2 <= k <= 30`.

## Approaches

Each move turns `k` piles into one, `k - 1` fewer, so the row can end
as one pile only when `k - 1` divides `n - 1`. The last move merges `k`
piles, each made from a stretch of the row, and costs every stone;
the cheapest way to make those stretches is the same question asked of
shorter rows. Every arm is an interval table over stretches of the
row; they differ in what a cell holds, in which way it is filled, and
in how a stretch is cut.

| file | mechanism |
|---|---|
| `merge_stones.kara` ★ | a table by length: a cell holds the least cost of merging a stretch into as few piles as it can be, which is one exactly when `k - 1` divides its length less one; the first of those piles comes from a stretch that ends as one, so the cut steps by `k - 1`, and a stretch that ends as one pays for every stone. O(n³ / k) |
| `merge_stones_piles.kara` | by number of piles: a cell holds the least cost of turning a stretch into exactly `p` piles, for every `p` up to `k`, the first of them one pile and the rest `p - 1`; one pile is `k` piles and a last move. The table fills by length, in one flat list. O(n³ k) |
| `merge_stones_memo.kara` | the same question from the top: a recursion on the stretch and the pile count, the last of the `p` piles cut off as one pile, a pile count out of reach answered at once, and a `Map` keeping every answer. O(n³ k) |
| `merge_stones_recursive.kara` | the table by length asked from the top: the same cells and cuts as ★, by recursion, with a list of answers, -1 for none yet, so each stretch is worked out once. O(n³ / k) |
| `merge_stones_parts.kara` | `k` parts of one pile: a cell holds the least cost of merging a stretch into one pile, which is every stone in it and the cheapest cut into `k` parts that each end as one pile, found by a small table of its own for each stretch. O(n⁴) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 19 lines. The first ten are LeetCode's three
examples and seven more: one pile, with `k` = 2 and 5, which costs
nothing; two piles with `k` = 2, and with `k` = 3, which cannot be
merged; three piles merged at once; four piles whose pairs are best
merged first; and five piles where merging the middle first costs
more. Then six rows of up to LeetCode's 30 piles: 30 piles of 100 with
`k` = 2, `k` = 30 and `k` = 3, which cannot end as one pile; 29 piles
of 1 to 29 with `k` = 3 and 15; and 29 piles of 100 and 1 in turn with
`k` = 5. Then totals over random rows of 1 to 100 stones a pile, with
`k` from 2 to 5, half of them with a pile count that `k` can merge to
one pile: 300 rows of up to 6 piles, 3,000 of up to 15 and 300 of up to
30. `merge_stones.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every way to make the moves, each merging `k` piles
side by side into one at the cost of their stones, tried in turn until
one pile is left, and the cheapest of them, or -1 if none gets there.
It checks 3,200 random rows, made as the arms' random rows are: 3,000
of up to 7 piles with `k` up to 4 against the statement, and 200 of up
to 30 piles with `k` up to 9 against the other properties.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 rows |
| P2 | the row reversed gives the same answer |
| P3 | every pile doubled doubles the answer, and leaves -1 as it is |
| P4 | -1 exactly when `k - 1` does not divide `n - 1` |
| P5 | one pile grown by `d`, 1 to 10, adds at least `d` and at most `d` for every merge to a possible answer, nothing to the answer for one pile, and leaves -1 as it is |
| P6 | each arm agrees with at least two of the other four |

P5's bounds hold because the grown pile is in at least one merge and
at most in all of them: the old best plan on the new row costs at most
`d` a merge more, and the new best plan on the old row costs at least
`d` less.

It prints `3200 rows of 14880 piles: 529 impossible, checksum
521110761, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (12.4 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Thirty-nine edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`: twenty-five first, then
fourteen more for the three arms that had fewer than three kept.
Fifteen are kept, three to each arm, all fifteen are killed, and each
fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every cut tried, not every `k - 1`th | P1 627, P6 698 |
| M2 | ★: the last move not paid | P1 1943, P5 2056, P6 2056 |
| M3 | ★: no check that one pile can be reached | P1 454, P4 529, P5 296, P6 529 |
| M4 | piles: the first pile never a single one | P1 1943, P4 2056, P6 2056 |
| M5 | piles: the answer read as `k` piles | P1 2546, P4 615, P5 916, P6 2671 |
| M6 | piles: the last pile left out of the last move | P1 1943, P2 2040, P5 443, P6 2056 |
| M7 | memo: a single pile costs 1 | P1 2546, P3 2671, P5 615, P6 2671 |
| M8 | memo: the key mixes up stretches whose ends add up the same | P1 646, P2 466, P6 732 |
| M9 | memo: the last cut kept, not the cheapest | P1 1109, P2 1443, P6 1203 |
| M10 | recursive: a stretch of `k` costs nothing | P1 1943, P5 609, P6 2056 |
| M11 | recursive: paid when `k` divides the length less one | P1 1943, P5 1384, P6 2056 |
| M12 | recursive: the cut steps by `k` | P1 888, P2 1087, P6 973 |
| M13 | parts: the first part free | P1 1349, P6 1447 |
| M14 | parts: the first pile left out of the last move | P1 1943, P2 2040, P5 485, P6 2056 |
| M15 | parts: a single pile costs its stones | P1 2546, P5 1633, P6 2671 |

P1 and P6 kill all fifteen, P5 nine, P2 five, P4 three and P3 one. The
counts read off the rows: of the 3,000 small rows 454 cannot end as
one pile, 603 are one pile already and 1,943 need moves; over all
3,200, 529, 615 and 2,056. M4 answers -1 for every row that needs
moves, and M2 0, so both fail the 1,943; M5, M7 and M15 are wrong on
every possible row, single piles too, 2,546, and M3 on every
impossible one, 454. Every edit but M7 still answers with a sum of
stone counts, which doubles with the stones, so P3 sees only M7, whose
extra 1 a pile does not double. Reversing the row sees the edits that
treat its two ends differently: M6 and M14, which leave the last or
the first pile out of the last move, and M12, which cuts from the left
in steps of `k`; and M8 and M9, whose wrong answers depend on the
order the stretches and cuts are tried in, which reversing changes
(inferred). P4 sees the three that answer -1 for a row that can be
merged, or a number for one that cannot. P5 sees nine whose answer
does not grow with a pile within its bounds, among them M2, which pays
nothing, and M7 and M15, which charge a single pile for itself and so
do not leave its answer at nothing.

Twenty-four other edits were tried and set aside. Sixteen failed
exactly the same checks as a kept one. Three pay nothing for the last
move, or leave the answer at 0, as M2: piles and memo turning `k`
piles into one without paying, and recursive starting its list of
answers at 0, which reads as known. Twelve answer -1 for every row
that needs moves, as M4: piles never making `k` piles, never as many
piles as the stretch has, and never leaving the rest as a single pile;
memo asking for the last part as two piles, and never leaving the last
part or the front as a single pile; parts never cutting a later part
right after the first pile, never making `k` parts, and never leaving
the first or the last part as a single pile; and piles and memo
keeping the dearest cut, which never moves off the starting "none".
And parts keeping the last cut fails M9's checks. Four were sound but
beyond three an arm: ★ leaving stretches of `k` piles at 0, and paying
when `k - 1` divides the length; memo paying the last move twice; and
parts starting every stretch as one pile for nothing. Three survived
and are equivalent. Memo without its cut for a pile count out of reach
reaches none anyway, since a stretch that ends as `p` piles has a
length that leaves `p` over multiples of `k - 1`, and the recursion
keeps that. Memo's key leaving out the pile count makes `p` = 1 and
`p` = `k` share a key for the same stretch, the only two counts it can
reach, but `k` is asked for only by `1` on the same stretch, just
before `1` stores its own answer. Parts not skipping the lengths that
cannot end as one pile finds no cut into `k` such parts for them, and
leaves them at none. One timed out after 300 seconds in both lanes:
recursive never reading its list of answers, which is right but works
every stretch out again each time it is asked, exponentially often.
None crashed.

## Verification

Every arm prints the same output as `merge_stones.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `395f71ae05`, the runtime
archives rebuilt at `d867340a02`, whose runtime sources are the same.
Under `karac __mir-run` the arms take 0.79 s (★) to 3.95 s (parts,
which builds a table of its own for every stretch), and the
differential 12.4 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. The program draws 20
rows once, with `k` from 2 to 11 twice over, each with as many piles of
1 to 100 stones, up to LeetCode's 30, as that `k` can merge down to one
pile: 30 for `k` = 2, 29 for `k` = 3, 28 for `k` = 4, and so on. In
each of 5,000 rounds it runs the arm on every row, each round starting
from a different one, and folds every cost into a checksum. Every
implementation prints `5000 rounds over 20 rows of up to 30 piles:
cost 324425000, checksum 619238425`. Each call allocates a fresh table
of up to 30 rows of 30, a list a row, and fills it.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `395f71ae05`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.222 to 0.269 s | 0.237 s |
| Rust (`rustc -O`) | 0.311 to 0.523 s | 0.364 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.330 to 0.405 s | 0.353 s |
| Go | 0.602 to 0.716 s | 0.658 s |
| Python | 18.0 s | |
| Kāra (`karac build --mir`) | 0.355 to 0.475 s | 0.374 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 48 times
Kāra's. Rust's plain median came out above its median with overflow
checks; its runs spread the widest.

v2 took 1.06 times Rust's median time under overflow checks and 1.58
times C's. Under valgrind's cachegrind v2 ran 5,047 million
instructions and 1,172 million branches with 24.2 million
mispredicted, Rust with overflow checks 4,988 million, 1,155 million
and 22.3 million, and C 3,119 million, 400 million and 12.7 million.
v2 and Rust run almost the same instructions and branches; C takes a
third of their branches, which fits the bounds checks on each read of
the table that the other two make and C does not (inferred).
