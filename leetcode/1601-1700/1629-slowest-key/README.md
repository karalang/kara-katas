# 1629. Slowest Key

A newly designed keypad was tested, where a tester pressed a sequence of
`n` keys, one at a time.

You are given a string `keysPressed` of length `n`, where
`keysPressed[i]` was the `ith` key pressed in the testing sequence, and
a sorted list `releaseTimes`, where `releaseTimes[i]` was the time the
`ith` key was released. Both arrays are **0-indexed**. The `0th` key was
pressed at the time `0`, and every subsequent key was pressed at the
**exact** time the previous key was released.

The tester wants to know the key of the keypress that had the **longest
duration**. The `ith` keypress had a **duration** of
`releaseTimes[i] - releaseTimes[i - 1]`, and the `0th` keypress had a
duration of `releaseTimes[0]`.

Note that the same key could have been pressed multiple times during the
test, and these multiple presses of the same key **may not** have had
the same **duration**.

*Return the key of the keypress that had the **longest duration**. If
there are multiple such keypresses, return the lexicographically largest
key of the keypresses.*

```
releaseTimes = [9,29,49,50],     keysPressed = "cbcd"   ->  'c'
releaseTimes = [12,23,36,46,62], keysPressed = "spuda"  ->  'a'
```

**Constraints:** `releaseTimes.length == n`; `keysPressed.length == n`;
`2 <= n <= 1000`; `1 <= releaseTimes[i] <= 10^9`;
`releaseTimes[i] < releaseTimes[i+1]`; `keysPressed` contains only
lowercase English letters.

## Approaches

| file | mechanism |
|---|---|
| `keys.kara` ★ | the answer is the largest `(duration, key)` pair: tuples compare field by field, so a tie on duration goes to the larger key, as asked. One pass over `release_times.iter().zip(keys_pressed.chars())`, `best = max(best, (time - previous, key))`. O(n) |
| `keys_table.kara` | each letter's longest press in a `[i64; 26]`, filled from the key bytes; then the first letter counting down from `z` whose longest press is the longest of all, which settles a tie with no comparison of keys. O(n + 26) |
| `keys_loop.kara` | the keys collected into a `Vec[char]` and walked by index with the times; a press beats the best when it lasts longer, or as long with a larger key. O(n) |
| `keys_solution.kara` | LeetCode's Rust template: the keys as bytes, the best kept as a `(duration, byte)` tuple compared directly. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples, a tie on the
first press won by the larger key, and a tie won by `z` though it comes
first; then the answers strung together while short, and a checksum,
for 3000 random problems of up to 6 presses from `a` to `c` held 1 to 4
ms, 300 of up to 1000 presses of any key held up to 100 ms, and 10 of up
to 1000 held up to 30000 ms. `keys.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every press's duration listed, the longest found, and the
largest key among the presses that long. It checks 3000 random problems
of 2 to 8 presses, every other one with keys from `a` to `d` held 1 to 3
ms, so ties are common, and the rest with any key held 1 to 50 ms. Every
random choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every release time doubled leaves the answer |
| P3 | one more press, longer than all before it, is the answer, whatever its key |
| P4 | the answer is one of the keys pressed |
| P5 | a 1 ms press of `a` put first leaves the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 905306897, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M3 stops the run: with `z` never
looked at, the countdown walks below `a` when `z` is the answer, and
Kāra stops with `runtime error: index out of bounds` (exit 101).

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the previous release never moves on, so a press lasts from 0 | P1 1929, P6 1929 |
| M2 | ★: the first press starts at 1, not 0 | P1 239, P2 88, P5 239, P6 239 |
| M3 | table: the countdown starts at `y` | index out of bounds |
| M4 | table: the first press lasts 0 | P1 628, P5 628, P6 628 |
| M5 | table: a letter's last press kept, not its longest | P1 383, P6 383 |
| M6 | loop: a tie goes to the smaller key | P1 875, P5 29, P6 875 |
| M7 | loop: the walk starts at the third press | P1 598, P5 1226, P6 598 |
| M8 | loop: a tie always goes to the later press | P1 462, P6 462 |
| M9 | template: only the duration compared, so a tie keeps the earlier press | P1 497, P5 36, P6 497 |
| M10 | template: the first press's key read off the second | P1 643, P5 643, P6 643 |

A first M10, `let mut best = (0, keys[0])` (the first press counted as
lasting 0), did not compile: the tuple's `0` settles at `i64` beside the
`u8`, and `best = press` with an `(i32, u8)` press is refused. That is
kara `B-2026-11-19-41`, below.

## Benchmarks

The bench draws 1000 random problems of 1000 presses, of any key held 1
to 1000 ms, all of them first, then answers each 100 times by the ★ arm
in all five languages. Every implementation prints `1000 problems of
1000 presses, answered 100 times: checksum 277917837`. The C build also
runs clean under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `60902ec48` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.072 s |
| Go | 0.138 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.162 s |
| Rust (`rustc -O`) | 0.163 s |
| Kāra (`karac build`) | 0.234 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.238 s |
| Python | 8.4 s |

Kāra is the slowest compiled lane, about 1.5 times Rust. C and Go walk
the keys as bytes; Rust and Kāra decode them with `chars()` and compare
`(i32, char)` tuples, which is the ★ arm as written. Why Kāra's loop is
slower than Rust's was not looked into.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.218 s and
0.222 s on one run).

## Verification

All four arms print the same output as `keys.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`60902ec48`.

## Writing it

The ★, table and loop arms checked clean as first written, the ★ arm's
`max` of two `(i32, char)` tuples and its `zip` of an `i32` iterator
with `chars()` included.

LeetCode's Rust template takes one `karac fix` of 5 edits:
`struct Solution {}`, `Vec<i32>` to `Vec[i32]`, `as_bytes()` to
`bytes()`, and `Solution::` to `Solution.`. It then checks and agrees
with no hand edit.

The differential, as first written, met two diagnostics. A `char` passed
to `String.contains` is refused with a fix to `got.to_string()`, which
`karac fix` applies. And `[1].iter().chain(release_times.iter().map(|t|
t + 1))` (the shifted times of P5) yields `ref` items against `i32`
ones; the error read `ref i64` against `i32` and offered nothing,
because the literal had settled at its default. Kara `0aec9d514` lets the
literal take the other side's items, so the error now reads `ref i32`
and offers `.cloned()` on the receiver, which the differential takes.

Kara `B-2026-11-19-41` (open) is the one gap met: a tuple literal whose
number sits beside a typed part, `let mut best = (0, keys[0])`, settles
the number at `i64`, so a later `best = press` with an `(i32, u8)`
press is refused, where `(0, 1)` beside `(v[0], 2)` is held open. The
arms do not use the form; it came from a mutant, which was replaced.
