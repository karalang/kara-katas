# 1505. Minimum Possible Integer After at Most K Adjacent Swaps On Digits

You are given a string `num` holding the digits of a very large integer
and an integer `k`. You may swap any two adjacent digits at most `k`
times. Return the smallest integer you can obtain, as a string.

```
num = "4321", k = 4                  ->  "1342"
num = "100", k = 1                   ->  "010"   (leading zeros allowed)
num = "36789", k = 1000              ->  "36789"
num = "22", k = 22                   ->  "22"
num = "9438957234785635408", k = 23  ->  "0345989723478563548"
```

**Constraints:** `1 <= num.length <= 3 * 10^4`; `num` holds digits only and
has no leading zeros; `1 <= k <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `swaps.kara` ★ | greedily, each place takes the smallest digit whose nearest copy can be brought there with the swaps left. Bringing the copy at original index `i` costs `i` less the digits already taken from before it, counted by a Fenwick tree; each digit's indices wait in a queue. O(10 n log n) |
| `swaps_window.kara` | the greedy by hand: each place looks at the next `k + 1` digits, takes the first copy of the smallest, and rotates it to the front, spending one swap per digit it passes. O(n min(n, k)) |
| `swaps_sorted.kara` | the ★ arm's greedy with the taken indices in a sorted `Vec`, the count before an index by binary search, and each digit's indices in a `VecDeque`. O(n) per insert |
| `swaps_iter.kara` | the window greedy with iterators: the window's smallest by `enumerate().min_by_key(..)` (the first of equals), then `remove` and `insert`. Refused by `karac check` until B-2026-11-08-12 was fixed |
| `swaps_solution.kara` | LeetCode's Rust template (`as_bytes`, `vec![Vec::new(); 10]`, `if let Some(&i) = pos[d].last()`, `wrapping_neg`), the ★ arm's greedy, carried by `karac fix`; blocked by B-2026-11-08-13 until it was fixed |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 11 lines: the answers for LeetCode's five
examples and three more, then a checksum of every digit of every answer
for 3000 numbers of 1 to 8 digits (`k` up to 30), 300 of 1 to 200 (`k` up
to 3000), and 3 of 1 to 1500 (`k` up to 10^6), each drawn from the first
1 to 10 digits. `swaps.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the
statement read literally: a breadth-first search over every number at
most `k` adjacent swaps reach, keeping the least. It checks 2000 problems
of 1 to 6 digits with `k` up to 8. Every random choice of a problem is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer has the same digits as the number |
| P3 | one more swap allowed never makes the answer larger |
| P4 | with `k` at least `n (n - 1) / 2` the answer is the digits sorted |
| P5 | the answer is at most `k` adjacent swaps from the number |
| P6 | each arm agrees with at least two of the other four |

The differential prints `2000 problems: checksum 480984163, 60000 checks
over 5 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property. The iterator and Rust
arms joined it once B-2026-11-08-12 and -13 were fixed; the mutations
below were run with the three arms before them, when P6 asked each arm to
agree with at least one of the other two, and none was added for them.

## Mutation testing

Twenty edits to the differential, six or seven to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run`. Twelve are kept, four
to each arm. Seventeen are killed, each the same way under both backends
and none by a crash; three survive, all equivalent. No two kept ones fail
the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a copy taken only when it costs less than the swaps left | P1 553, P2 200, P3 200, P4 47, P6 553 |
| M2 | ★: a copy's cost read as its original index | P1 1031, P2 1031, P3 366, P6 1031 |
| M3 | ★: no swaps spent | P1 222, P5 222, P6 222 |
| M4 | ★: the digits tried largest first | P1 1055, P3 351, P4 390, P6 1055 |
| M5 | window: the window one digit short | P1 353, P4 11, P6 353 |
| M6 | window: the last copy of the smallest taken, not the first | P1 231, P3 6, P6 231 |
| M7 | window: one swap spent per move, whatever the distance | P1 201, P5 68, P6 201 |
| M8 | window: the window's first two digits never compared | P1 640, P4 220, P6 640 |
| M9 | sorted: half the digits taken before counted | P1 908, P2 905, P3 497, P6 908 |
| M10 | sorted: a taken index appended, not inserted in order | P1 113, P2 80, P3 46, P5 28, P6 113 |
| M11 | sorted: one swap more allowed than are left | P1 343, P5 343, P6 343 |
| M12 | sorted: each digit's last copy tried, not its first | P1 1043, P2 1030, P3 434, P4 109, P6 1043 |

P1 and P6 kill all twelve, P3 seven, P2 five, P4 five, and P5 four. P2
sees the edits that let a copy be taken twice or a wrong copy be counted:
a digit then comes out twice and another never.

The other eight: the ★ arm's Fenwick query stepping down by one (P1 261,
P5 261, P6 261), the sorted arm popping the back of a queue (P1 183, P5
183, P6 183), the ★ arm's update starting one index late on odd indices
(P1 448, P2 421, P3 213, P6 448), and the window arm leaving the last
digit unshifted (P1 702, P2 696, P4 231, P5 1, P6 702) fail with
signatures of their own but add no property; the sorted arm spending half
the cost fails as M3. Three
survive and are equivalent: the window arm without its `left == 0` early
stop (a window of one digit moves nothing), the window arm swapping
`best` with `best.min(n - 1)` (always itself), and the sorted arm's
binary search on `<= i - 1` for `< i` (the same on integers).

## Iterator arm: B-2026-11-08-12

`karac check` refuses the iterator arm: after
`let (offset, _) = digits[i..end].iter().enumerate().min_by_key(..).unwrap();`
it says `digits` cannot be borrowed as `mut ref T` because it is also
borrowed as `Slice[T]` at that line, at `digits.remove(..)` and
`digits.insert(..)`. Nothing holds the borrow: `offset` is an `i64` and
the `_` binds nothing. Measured on a five-line program: the refusal needs
both the range slice and the tuple pattern. `v.iter()` for `v[0..3].iter()`,
or `.unwrap().0` for the pattern, checks. `karac __mir-run` accepted the
arm and printed the expected output, so only the front-end checker
objected. Fixed in kara `edc6b01e2` (a `let` that destructures a slice
read keeps the slice borrowed only through the parts that still borrow
it); the arm checks as written and agrees on every lane.

## Rust template: B-2026-11-08-13

The Rust arm was written as LeetCode's Rust template plus a thin `i64`
wrapper. `karac fix` makes 7 edits and then 4, and one of them changes
the program's meaning: `if let Some(&i) = pos[d].last()` becomes
`if let Some(i) = pos[d].last()`. Rust's `&i` copies the `usize` out of
the `Option<&usize>`; without it `i` is a reference into `pos[d]`, and
the later `pos[d].pop()` is refused (E0516, no fix). The edit that keeps
the meaning is `pos[d].last().cloned()`. With that written by hand (and
`before: i32` until B-2026-11-07-57, as in kata 1504), `karac fix` makes 8
more edits and the arm checks and prints the ★ arm's output. Fixed in
kara `f4b3b2a3b`: the `&` sigil's fix now writes `.cloned()` on the
scrutinee. Run on the Rust spelling again, `karac fix` writes
`if let Some(i) = pos[d].last().cloned()`, and the file holds that.

## Benchmarks

The bench builds 60 numbers of 30000 digits once (drawn from the first 1
to 10 digits, `k` from 0 to about 10^7) and answers each by the ★ arm in
all five languages. Every implementation prints `60 numbers of 30000
digits: checksum 821574564`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `83c2a5580` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.084 to 0.136 s | 0.103 s |
| Rust (`rustc -O`) | 0.098 to 0.113 s | 0.109 s |
| Kāra (`karac build`) | 0.107 to 0.124 s | 0.117 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.110 to 0.126 s | 0.121 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.125 to 0.139 s | 0.132 s |
| Go | 0.204 to 0.267 s | 0.237 s |
| Python | 5.88 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.137 s) is below its real time (0.191 s).

Kāra is 0.92x Rust under overflow checks by median. Building the 1.8
million digits is part of every timing.

## Verification

All five arms print the same output as `swaps.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them.
Under `karac __mir-run` the arms take 0.5 to 0.6 s and the differential
0.8 s.

## Writing it

The arms were written in Kāra. `karac fix` made 8 or 9 edits to each: a
`ref Vec[i64]` parameter is a bare one, and `"4321".to_string()` in the
harness is a plain literal where a `String` is wanted.
