# 2526. Find Consecutive Integers from a Data Stream

For a stream of integers, implement a data structure that checks if the
last `k` integers parsed in the stream are **equal** to `value`.

Implement the **DataStream** class:

- `DataStream(int value, int k)` initializes the object with an empty
  integer stream and the two integers `value` and `k`.
- `boolean consec(int num)` adds `num` to the stream of integers.
  Returns `true` if the last `k` integers are equal to `value`, and
  `false` otherwise. If there are less than `k` integers, the condition
  does not hold true, so returns `false`.

```
DataStream(4, 3); consec(4), consec(4), consec(4), consec(3)
  ->  false, false, true, false
```

**Constraints:** `1 <= value, num <= 10^9`; `1 <= k <= 10^5`; at most
`10^5` calls will be made to `consec`.

The last `k` numbers all equal `value` exactly when the run of matches
ending at the newest number is at least `k` long, so the stream itself
need not be kept. The approaches differ in what they keep of it.

## Approaches

| file | mechanism |
|---|---|
| `stream.kara` ★ | a counter of the run of matches ending at the newest number, reset to 0 by any other; true when it reaches `k`. O(1) a call |
| `stream_queue.kara` | the latest `k` numbers in a `VecDeque` and a count of the matches among them, the oldest leaving as each new one comes |
| `stream_ring.kara` | the latest `k` numbers in a ring of `k` slots, the `i`-th number written to slot `i % k`, and a count of the matching slots |
| `stream_mismatch.kara` | the position of the latest number that is not `value`, and how many came: true when that position lies at least `k` places back, or there is none and `k` came |
| `stream_iter.kara` | iterators over the whole stream kept in a `Vec`: the last `k` walked by `rev().take(k)` and tested with `all`. O(k) a call, stopping at the first number that differs |
| `stream_solution.kara` | LeetCode's Rust template: a `struct DataStream` of `i32` fields, `new` returning `Self`, and `consec(&mut self, num: i32)` counting the run; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Each arm is a `DataStream` with `new` and `consec`, and two small
functions, `open_stream` and `feed`, through which the harness drives
it; the template's cast its `i64` arguments to the `i32` it takes.
Every arm prints the same 10 lines: LeetCode's example and five more,
as the answers written `T` and `F`; then 2000 random streams of 1 to 60
numbers from 1 to 3 with `value` 1 to 3 and `k` 1 to 6, as how many
answers are true and a checksum; then three streams of the constraints'
`10^5` calls: with `k = 10^5` and one number in each 50 not `value`,
with `k = 100` and all `value`, and with `k = 3` and `value` drawn half
the time. The all-`value` stream takes `k = 100` rather than `10^5`
because the iter arm walks `k` numbers on every call. `stream.py`
mirrors the ★ arm and its output is byte-identical, and the mirror was
checked on 3000 random streams of 1 to 40 numbers from 1 to 3 with `k`
1 to 8 against a test of the last `k` numbers after every call, and the
two agreed on every stream.

`check` reported one error on each of the five Kāra arms as first
written: `consec(self: mut ref DataStream, ..)` is Rust's way to type a
receiver, and the error says that in Kāra the mode goes before `self`.
`karac fix` rewrote each as `mut ref self`.

`check` first reports 3 errors on the template: the `&mut self`
receiver, the path call `DataStream::new`, and the `&mut DataStream`
parameter of `feed`. `karac fix` carries it in one call, reporting 3
edits: `mut ref self`, `DataStream.new`, and `mut ref DataStream`. The
template's `-> Self` and its field shorthand `DataStream { value, k,
cnt: 0 }` are accepted as written.

## Differential

`differential.kara` holds copies of the six arms, each `DataStream`
renamed after its arm, and the statement read literally: after each
number the whole stream so far is looked at again, and the answer is
whether it holds at least `k` numbers whose last `k` all equal `value`.
Nothing is carried from one call to the next. It checks 300 random
streams of 1 to 30 numbers from 1 to 3 with `value` 1 to 3 and `k` 1
to 4; 30 of 1 to 30 numbers from 1 to `10^9` against a `value` drawn
half the time, with `k` 1 to 4; and 30 of `value` alone with `k` 1 to
40. All 360 are drawn before any arm answers, and 186 of them are never
true. An arm's answers are a string of `T` and `F`, one for each
number.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | no `T` among the first `k - 1`, and a `T` only where the number is `value` |
| P3 | `k` one less (when `k > 1`): every `T` stays a `T` |
| P4 | one more number, not `value`: the same answers, then an `F` |
| P5 | every number turned into `value`: `k - 1` `F`s, then all `T`s |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases, 186 never true: checksum 303142895,
12960 checks over 6 arms: 0 failures` under every lane in Verification;
the checksum of the literal answers was checked against a Python
reading that builds the same cases and tests the last `k` numbers after
every call. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the run reaching k minus 1 | P1 251, P2 124, P4 72, P5 269, P6 251 |
| M4 | ★: the run begun at 1 | P1 54, P2 54, P5 269, P6 54 |
| M5 | ★: the run exactly k | P1 106, P3 108, P5 321, P6 106 |
| M7 | queue: the window one longer | P1 166, P3 28, P5 321, P6 166 |
| M8 | queue: the leaving match not counted off | P1 262, P2 160, P3 203, P4 43, P5 321, P6 262 |
| M9 | queue: a full window enough | P1 313, P2 308, P4 341, P6 313 |
| M12 | ring: the matches among the first k not counted | P1 100, P5 329, P6 100 |
| M14 | ring: each number counted twice | P1 70, P3 38, P5 171, P6 70 |
| M15 | ring: one match short enough | P1 256, P2 221, P4 137, P6 256 |
| M18 | mismatch: no stranger enough | P1 120, P2 120, P5 288, P6 120 |
| M19 | mismatch: the stranger recorded after the count | P1 152, P6 152 |
| M20 | mismatch: only the first stranger kept | P1 300, P2 295, P4 312, P6 300 |
| M23 | iter: the first k walked | P1 158, P2 40, P4 56, P6 158 |
| M24 | iter: any match enough | P1 236, P2 228, P3 211, P4 139, P6 236 |
| M26 | iter: the newest skipped | P1 179, P2 171, P4 60, P6 179 |
| M28 | solution: the count more than k | P1 174, P5 329, P6 174 |
| M30 | solution: k read as 1 | P1 272, P2 158, P5 288, P6 272 |

P1 and P6 kill all seventeen, P2 eleven, P5 ten, P4 eight, and P3 five.

Three of the first thirty-one edits survived, all to the ring arm, and
were replaced. Writing each number one slot on only turns the ring; the
count of matches never reaches `k` before `k` numbers came, the first
slots holding 0, which no number is; and slots begun at `value` are
never counted, being overwritten before any is read. All three are
equivalent. They became the ring arm's matches among the first `k` not
counted, each number counted twice, and one match short enough (M12,
M14, M15).

Fourteen are not kept, and none survives. Eight fail exactly as a kept
one. The queue arm's newest leaving instead and the ring arm's old slot
read after it is written (M10, M16) fail as the iter arm's first `k`
walked (M23); the queue arm's one match short enough (M11) as the ring
arm's (M15); the ring arm's overwritten match kept (M13) as the queue
arm's leaving match not counted off (M8); the mismatch arm's gap more
than `k` and the iter arm's last `k + 1` walked (M21, M22) as the
mismatch arm's stranger recorded after the count (M19), each asking
one number more; the iter arm's length not checked (M25) as the
mismatch arm's no stranger enough (M18); and the template's `value`
read as the number fed (M31) as the queue arm's full window enough
(M9). The other six fail in three ways of their own, in arms that
already hold their kept edits: the ★ arm's run never reset and the
template's count kept on a stranger (M2, M29); the ★ arm's run reset to
1, the mismatch arm's gap at least `k - 1` and the template's count from
1 after a stranger (M3, M17, M27); and the ★ arm's run halved by a
stranger (M6).

## Verification

Every arm prints the same output as `stream.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.2 to 11.3 s and the differential 1.1 s; under `karac __mir-llvm-asan` the arms take 0.5 to 2.4 s and the differential 0.6 s; and under `karac run` the differential takes 0.4 s.

## Benchmarks

The bench builds `10^5` random numbers from 1 to 3 once from its own
generator, then makes 1250 passes. Each pass opens a fresh stream with
`value = check % 3 + 1` and `k = check % 8 + 1`, feeds it every number,
and folds the count of true answers plus the pass into the checksum.
The bench uses the ★ arm in all five languages. Every implementation
prints `1250 passes over 10^5 numbers: checksum 931898217`.

BENCHTAB
