# 875. Koko Eating Bananas

Koko loves to eat bananas. There are `n` piles of bananas, the `i`-th
pile has `piles[i]` bananas. The guards have gone and will come back in
`h` hours. Koko can decide her bananas-per-hour eating speed of `k`.
Each hour, she chooses some pile of bananas and eats `k` bananas from
that pile. If the pile has less than `k` bananas, she eats all of them
instead and will not eat any more bananas during this hour. Koko likes
to eat slowly but still wants to finish eating all the bananas before
the guards return. Return the minimum integer `k` such that she can eat
all the bananas within `h` hours.

```
piles = [3,6,7,11],      h = 8  ->  4
piles = [30,11,23,4,20], h = 5  ->  30
piles = [30,11,23,4,20], h = 6  ->  23
```

**Constraints:** `1 <= piles.length <= 10^4`, `piles.length <= h <=
10^9`, `1 <= piles[i] <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `min_eating_speed.kara` ★ | binary search on the speed: at speed k a pile of p bananas takes ceil(p / k) hours, so the hours for all piles only fall as k rises, and the slowest speed that finishes within h hours is found by binary search over 1 to the largest pile, which always finishes (one pile an hour, and h is at least the number of piles). O(n log M) for piles up to M |
| `min_eating_speed_bounds.kara` | the same search between bounds taken from the total: no speed below ceil(total / h) can finish, since an hour eats at most k bananas, and each pile takes under p / k + 1 hours, so when h > n any k with total / k <= h - n finishes. The two bounds are often far closer together than 1 and the largest pile |
| `min_eating_speed_gallop.kara` | galloping up from the slowest speed: speeds 1, 2, 4, 8, ... are tried until one finishes, and a binary search between the last that failed and the first that finished finds the answer; the hours are counted down and the count stops as soon as they run out. O(n log K) for answer K |
| `min_eating_speed_recursive.kara` | the search written as recursion: `slowest(lo, hi)`, given that `hi` finishes, halves the range and recurses into the half that holds the answer; the hours are counted with remainder, p / k and one more when p % k is not 0 |
| `min_eating_speed_grouped.kara` | equal piles counted once: a `Map` from pile size to how many piles have it, so each distinct size costs one division per speed tried, its hours multiplied by its count. O(n + d log M) for d distinct sizes |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's three examples and eight
more (a single pile of 1 in 1 hour; a pile of 10^9, LeetCode's largest,
in 1 hour, in 10^9 hours and in 10^9 - 1 hours, answers 10^9, 1 and 2;
four piles of 5 in 7 hours, which still needs 5; three piles of 1 and
one of 999,999,999 in 10 hours, answer 142,857,143; and 10^4 piles of
10^9 in 10^4 hours and in 10^9 hours, answers 10^9 and 10^4); the
answers for 3,000 random sets of 1 to 8 piles of up to 20 bananas with
up to 29 hours to spare, 12,740 in all; and 20 sets of 10^4 piles,
LeetCode's largest, half of them up to 10^9 bananas and half up to
1000, with h up to 10^9 or up to 10^5 above the number of piles, with a
checksum. `min_eating_speed.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: Koko eating hour by hour, each hour k bananas from the pile
she is on or the whole pile if it has fewer, with the speeds 1, 2, 3,
... tried in turn until one finishes within h hours. It checks 1,700
sets of piles: 1,500 of 1 to 8 piles of up to 20 bananas with up to 29
hours to spare against the statement, and 200 of 1 to 60 piles of up to
10^9 or up to 1000 bananas, with up to 10^6 or 100 hours to spare,
against the other properties. The ★ arm's speeds sum to 16,283,766,192.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the answer finishes within h hours and one slower does not |
| P3 | more hours never need a faster speed |
| P4 | the piles in another order give the same answer |
| P5 | every pile multiplied by c, 2 to 5, needs a speed above c(answer - 1) and at most c times the answer |
| P6 | one more pile, no bigger than the answer, and one more hour keep the answer |

It prints `1700 sets of piles, speeds sum to 16283766192, 50000 checks
over 5 arms: 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: finishing with no hour to spare counted as too slow | P1 393, P2 520 |
| M2 | ★: a part-eaten pile not counted | P1 691, P2 845, P6 265 |
| M3 | ★: the search capped at the smallest pile | P1 1272, P2 1439 |
| M4 | bounds: the lower bound one too high | P1 1034, P2 1086, P5 826, P6 74 |
| M5 | bounds: the upper bound taken as the lower | P1 414, P2 560, P6 222 |
| M6 | bounds: the search steps two past a slow speed | P1 416, P2 524, P3 30, P5 602, P6 171 |
| M7 | gallop: the search starts one too high | P1 482, P2 485, P5 507 |
| M8 | gallop: an extra hour for a pile that divides evenly | P1 529, P2 594, P6 90 |
| M9 | gallop: speeds galloped by fours | P1 623, P2 704, P5 772 |
| M10 | recursive: the extra hour added for a pile with no remainder | P1 645, P2 799, P5 78, P6 330 |
| M11 | recursive: the search capped at the last pile | P1 221, P2 258, P4 359, P6 1023 |
| M12 | recursive: one hour over allowed | P1 406, P2 535 |
| M13 | grouped: repeated sizes counted once | P1 415, P2 440, P6 95 |
| M14 | grouped: a size's hours added once, plus an hour per repeat | P1 294, P2 311 |
| M15 | grouped: the largest pile never a speed | P1 62, P2 64, P5 64 |

P1 and P2 kill all fifteen. P4 kills only M11, the one mutant whose
answer depends on which pile comes last. P3 kills only M6, whose search
can step over the answer: a mutant that is wrong by the same rule at
every h stays monotone in h, so more hours still never ask it for a
faster speed. Three mutants tried first were replaced. The bounds arm's
upper bound taken from h - n + 1 hours instead of h - n was equivalent:
the hours are strictly below total / k + n, so that speed still
finishes, and M5 takes the lower bound as the upper instead. A gallop
that counted using up every hour as too slow (`left <= 0`) never
finished when h equals the number of piles and doubled its speed until
it overflowed, and a recursion that never tried speed 1 recursed without
end on piles of one banana; M8 and M11 replace them.

## Verification

Every arm prints the same output as `min_eating_speed.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `e3f5faf572` and the runtime
archives at `e903d5b111`, with no runtime change between them. Under
`karac __mir-run` the arms take 5 to 10 s each and the differential 9 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends refuse all five arms, the differential and
the bench program at a `*` on a `for` element, saying the value is not a
reference, where v2 yields a reference. Legacy is frozen, so this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 20 sets of
10^4 piles, LeetCode's largest, half of them up to 10^9 bananas and half
up to 10^6, built once; then 600 searches, each over one of the sets
with h from 10^4 up to 10^9 or up to 10^6 above the number of piles,
summing the speeds and a checksum. Each search counts the hours about
30 times, so the run makes some 1.8 x 10^8 divisions, and the piles fit
in the cache. Every implementation prints `600 searches over 10000
piles: speeds sum to 6275396065, checksum 816972623`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.44 to 0.50 s | 0.47 s |
| Rust (`rustc -O`) | 0.44 to 0.58 s | 0.47 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.49 to 0.55 s | 0.52 s |
| Go | 1.36 to 1.63 s | 1.42 s |
| Python | 14.7 s | |
| Kāra (`karac build --mir`) | 0.70 to 0.82 s | 0.74 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 874's does. Legacy refuses the bench program
(above), so it has no lane here.

v2 takes 1.4 times Rust's median time under overflow checks and 1.6
times C's. Under valgrind's cachegrind C runs 1.78 billion instructions,
Rust with overflow checks 2.43 billion and v2 3.60 billion, all of it in
`main`, where each program inlines the hours loop. The two checked loops
are alike: both add with an overflow check, test whether the operands
fit in 32 bits to take the shorter divide, and add the quotient with an
overflow check. Rust tests the divisor for 0 and -1 once, before the
loop; v2 keeps three more compare-and-branch steps per pile inside it,
tests on values that do not change in the loop (read from the
disassembly; which checks they are is inferred). The divide is most likely the
larger cost in every language. Go checks its divisor too and takes 3.0
times C's time. The comparison with C and Rust waits until after M4.
