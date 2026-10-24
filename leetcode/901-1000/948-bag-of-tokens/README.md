# 948. Bag of Tokens

You start with an initial **power** of `power`, an initial **score** of
`0`, and a bag of tokens given as an integer array `tokens`, where each
`tokens[i]` denotes the value of token `i`.

Your goal is to **maximize** the total **score** by strategically
playing these tokens. In one move, you can play an **unplayed** token in
one of the two ways (but not both for the same token):

- **Face-up**: If your current power is **at least** `tokens[i]`, you
  may play token `i`, losing `tokens[i]` power and gaining `1` score.
- **Face-down**: If your current score is **at least** `1`, you may play
  token `i`, gaining `tokens[i]` power and losing `1` score.

Return *the **maximum** possible score you can achieve after playing
**any** number of tokens*.

```
tokens = [100],                power = 50   ->  0
tokens = [200,100],            power = 150  ->  1
tokens = [100,200,300,400],    power = 200  ->  2
```

**Constraints:** `0 <= tokens.length <= 1000`; `0 <= tokens[i], power <
10^4`.

## Approaches

| file | mechanism |
|---|---|
| `bag_of_tokens_score.kara` ★ | the tokens sorted; a face-up play should cost as little as it can and a face-down play bring as much as it can, so the smallest is played face up while the power pays for it, and otherwise a point is given up to play the largest face down, as long as a point and another token are left; the best score seen is the answer. O(n log n) |
| `bag_of_tokens_score_prefix.kara` | a closed form: with the `j` largest face down, the power to spend is the power given plus their sum, and the most of the smallest it pays for, among the tokens not face down, is `k`, read off the sums of the smallest; the answer is the best `k - j`. Such a game can always be played in order once the smallest token can be played, since each face-down play comes right after a face-up one and brings at least what the next face-up play costs. `k` only grows as `j` does, so one walk finds every `k`. O(n log n) for the sort |
| `bag_of_tokens_score_heaps.kara` | the same play as ★ with the tokens left unsorted and drawn from two `PriorityQueue`s, one giving the smallest first and the other, holding each token negated, the largest; a token played from one queue stays in the other and is passed over when it comes out, and the smallest drawn but not paid for goes back. Each token is kept with its index as one number, `value * 2048 + index`. O(n log n) |
| `bag_of_tokens_score_counts.kara` | how many tokens there are of each value, counted in a list as long as the largest value, and the same play walked over it from both ends. O(n + largest value) |
| `bag_of_tokens_score_grid.kara` | for every `k` smallest played face up and `j` largest played face down, the most power any order of those plays can leave, or none when no order can make them all, a face-down play needing a point first; rows of `k` built one at a time, each from the one before by a face-up play and then along itself by face-down plays, and the best `k - j` reached is the answer. Every order is weighed, not only the greedy one. O(n^2) time, O(n) space |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's three examples and five
more (an empty bag, three tokens of 0 with no power, three equal tokens
the power pays for one at a time, a large token that pays for three
small ones once it is played face down, and four tokens the power pays
for all at once); for 300 random bags of 0 to 40 tokens from 0 to 99 and
power from 0 to 199, the tokens, the scores added up and a checksum; and
five of LeetCode's largest, 1,000 tokens: random tokens from 0 to 9,999
with power 5,000, with no power, and with power equal to their sum; the
tokens 1 to 1,000 with power 1; and 1,000 tokens of 9,999 with power
9,999. `bag_of_tokens_score.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every sequence of moves, each playing an unplayed token face
up when the power is at least its value or face down when the score is
at least 1, and the highest score any of them reaches, a position being
which tokens were played which way, one base-3 digit each, searched from
once. It checks 3,200 random bags: 3,000 of up to 6 tokens from 0 to 9
with power up to 15, against the statement, and 200 of up to 300 tokens
from 0 to as much as 9,999 with power up to twice that, against the
other properties; 39,825 tokens.

| | property |
|---|---|
| P1 | the statement's highest score, on the small bags |
| P2 | at least as many as the smallest tokens the power pays for all face up, at most every token, and at least 1 exactly when the smallest token can be played |
| P3 | the tokens in a random order, with every token and the power times 3, give the same score |
| P4 | more power never gives less, and power equal to the sum of the tokens gives every token |
| P5 | one more token of 0 gives exactly one more when the smallest token could already be played and at least one more when it could not; one more random token never gives less |
| P6 | each arm agrees with at least two of the other four |

A token of 0 gives more than one point when the smallest token could not
be played before: it is the point that lets a large token be played face
down, which can then pay for several small ones (`[3,3,9]` with no power
scores 0, and with a 0 added scores 2).

It prints `3200 bags of 39825 tokens, scores adding to 17970, checksum
858292230, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
(26 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the tokens never sorted | P1 945, P2 1065, P3 964, P5 2151, P6 1141 |
| M2 | ★: the largest token never played | P1 822, P2 645, P4 2796, P5 404, P6 913 |
| M3 | ★: face down bringing one less | P1 90, P3 12, P6 104 |
| M4 | prefix: each sum one token, not a running sum | P1 1281, P6 1478 |
| M5 | prefix: half of each face-down token | P1 256, P3 1, P6 449 |
| M6 | prefix: a point when the smallest cannot be played | P1 753, P2 755, P4 404, P5 630, P6 755 |
| M7 | heaps: the index paid, not the value | P1 1403, P2 402, P3 440, P4 18, P5 545, P6 1588 |
| M8 | heaps: the largest queue keyed by the wrong index | P1 169, P3 206, P5 250, P6 358 |
| M9 | heaps: each face-up play costing half | P1 971, P3 218, P6 1167 |
| M10 | counts: two points needed to play face down | P1 148, P5 153, P6 153 |
| M11 | counts: a face-up token never used up | P1 1374, P5 604, P6 1571 |
| M12 | counts: face up costing the largest value | P1 1357, P2 1397, P4 2330, P5 1795, P6 1555 |
| M13 | grid: the row with every token face up never weighed | P1 644, P2 645, P4 2796, P5 404, P6 645 |
| M14 | grid: each row starting from the one before, unpaid | P1 1953, P2 351, P6 2151 |
| M15 | grid: no face down with no power left | P1 52, P5 20, P6 52 |

P1 and P6 kill all fifteen, P5 ten, P2 seven, P3 six and P4 five.

P3 kills M1, M3, M5, M7, M8 and M9. M1, which plays the tokens in the
order given, and M7 and M8, which confuse a token with its index, are
tied to the order the shuffle changes; M3's one less does not grow
threefold with the values, and M9's and M5's halves round differently
once the values are tripled (M5's only once). The other nine make
mistakes that scale with the values and ignore the order.

P4 kills M2, M6, M7, M12 and M13. M2 never plays the largest token and
M13 never weighs every token face up, so neither reaches every token
when the power pays for all; M7 and M12 pay something other than each
token's value, which the sum of the values need not cover; and M6
answers 1 for an empty bag, where power equal to the sum, 0, should
give 0.

P2 misses eight, M3 to M5 and M8 to M11 and M15: on every bag their
scores stay between the smallest tokens the power pays for and every
token, with a point exactly when the smallest can be played. That they
must was not worked out.

Thirty-three other edits were tried and set aside. Nineteen failed
exactly the same checks as each other, in seven groups, so none of them
was kept: six that play the smallest token face down or none at all (★,
prefix, heaps, counts and grid giving up the smallest, and prefix never
giving any up); three that play face down with no point (★ and grid
allowing it, and prefix with no check that the smallest can be played);
★ and grid not playing a token that costs all the power left; ★ giving
no point up face down and grid not counting face-down plays against the
score; ★ and grid never playing the last token; prefix not paying a sum
equal to its power and grid not counting a state with no power left;
and ★ and grid making each face-up play cost one less. Ten survived
every check. Six are equivalent: ★ keeping the last score and counts
the score after the last face-up play, since in this play a face-down
play brings the largest token and is always followed by a face-up one,
so the score only returns to where it was and the last is the best;
prefix never cutting its count back, since a count above `n - j` was
reached at `j - 1`, where it scored one more; heaps needing two other
tokens to play face down, since with two left, giving a point for one
and playing the other face up ends where it began; and grid holding one
token back from face down and letting a token be played both ways,
which only reach states scoring less than ones already counted. Whether
the other four are equivalent was not worked out: heaps drawing played
tokens again and not marking a face-up token as played (both can go
wrong only on equal values, where the token drawn is worth the same),
prefix not keeping its count off the face-down tokens, and grid keeping
the last way to a count rather than the most power. Three were sound
but beyond three an arm (★ never playing the smallest token, prefix
never trying all but one face down, and grid starting with one more
power). One crashed: heaps not putting back the smallest token drawn,
with an index out of bounds.

## Verification

Every arm prints the same output as `bag_of_tokens_score.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 0.16 to 2.4 s each and the
differential 26 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy pipeline in that build refuses everything here: the ★, heaps
and grid arms at `bag_of_tokens_score(examples[i], powers[i])` and the
bench program at `bag_of_tokens_score(bags[b], powers[b])`, a move out
of an index ("cannot move ... out of an index"), which v2's borrowing
parameters make a borrow; and the prefix and counts arms and the
differential at the first `*` on an element of a `Vec[i64]`'s `.iter()`
("unary '*' requires 'ref T', ..."), legacy's older rule, under which
the element is a copy. Legacy has since been removed from kara, so none
of this is filed.

## Benchmarks

The bench program builds 20 bags of 1,000 tokens once, LeetCode's
largest, each of random tokens from 0 to 9,999 with a random power from
0 to 9,999; in each of 500 rounds it runs the ★ arm on every bag, each
round starting from a different one, and folds the scores into a
checksum. Every implementation prints `500 rounds over 20 bags of 1000
tokens: scores adding to 4462500, checksum 405592647`. Each call copies
the bag and sorts the copy, and the sort is most of the work: C sorts
with `qsort`, Rust with `sort` (stable), Go with `slices.Sort`, Python
with `sorted`, and Kāra with `Vec.sort`, which for a `Vec[i64]` the
runtime hands to Rust's `sort_unstable` (`runtime/src/lib.rs`,
`karac_vec_sort_i64_8`).

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.71 to 0.75 s | 0.72 s |
| Rust (`rustc -O`) | 0.14 to 0.16 s | 0.16 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.15 to 0.18 s | 0.16 s |
| Go | 0.49 to 0.56 s | 0.50 s |
| Python | 2.13 s | |
| Kāra (`karac build --mir`) | 0.10 to 0.14 s | 0.11 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 3 times C's:
its `sorted` is written in C and needs no comparison function called
through a pointer.

v2 takes 0.69 times Rust's median time under overflow checks and 0.15
times C's. Under valgrind's cachegrind v2 runs 1.16 billion
instructions and 0.12 billion branches with 7.2 million mispredicted,
Rust with overflow checks 1.41 billion, 0.14 billion and 13.1 million,
and C 2.85 billion, 0.40 billion and 56 million, 102 million of its
branches indirect: `qsort` calling its comparison function for every
comparison. That v2 beats Rust because its unstable sort does less work
than Rust's stable `sort` on these bags is inferred, not profiled; the
bench measures each language's usual sort more than the play after it.
