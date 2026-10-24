# 936. Stamping The Sequence

You are given two strings `stamp` and `target`. Initially, there is a
string `s` of length `target.length` with all `s[i] == '?'`.

In one turn, you can place `stamp` over `s` and replace every letter in
`s` with the corresponding letter from `stamp`.

- For example, if `stamp = "abc"` and `target = "abcba"`, then `s` is
  `"?????"` initially. In one turn you can place `stamp` at index 0, 1
  or 2 of `s`, giving `"abc??"`, `"?abc?"` or `"??abc"`. Note that
  `stamp` must be fully contained in the boundaries of `s` in order to
  stamp.

We want to convert `s` to `target` using **at most**
`10 * target.length` turns.

Return an array of the index of the left-most letter being stamped at
each turn. If we cannot obtain `target` from `s` within
`10 * target.length` turns, return an empty array.

```
stamp = "abc",  target = "ababc"    ->  [0,2]      ([1,0,2] is also accepted)
stamp = "abca", target = "aabcaca"  ->  [3,0,1]
```

**Constraints:** `1 <= stamp.length <= target.length <= 1000`; `stamp`
and `target` consist of lowercase English letters.

## Approaches

| file | mechanism |
|---|---|
| `moves_to_stamp.kara` ★ | the stamps peeled off in reverse: a window can be the last stamp left when each of its letters matches the stamp or is already erased, and one is not erased yet; every window is swept again and again, each one that fits erased to `?`, until the whole target is erased or a sweep erases nothing, and the erased windows, last first, are the stamps. O(n (n - m) m) for a stamp of `m` letters and a target of `n` |
| `moves_to_stamp_queue.kara` | the same peeling with work only where something changed: each window counts the letters that differ from the stamp, each newly erased letter goes on a queue, and taking it off counts it off every window it differed in, a window being peeled when it reaches none. O(n m) |
| `moves_to_stamp_frontier.kara` | the sweeps of ★, but after the first only over the windows holding a letter the sweep before erased, since no other window can have started to fit. O(n m) a sweep at worst |
| `moves_to_stamp_layers.kara` | forwards: in the finished string each letter shows one offset of the stamp on top, and each stamp shows one unbroken run, since a later stamp, being as long, can only cover one end of an earlier one. From one letter to the next the offset steps on, or a new stamp starts at offset 0 on top, or, after a stamp's last letter, at any offset underneath. A table filled from the right finds the runs; stamps not shown from offset 0 go first, right to left, then those shown from it, left to right. O(n m) |
| `moves_to_stamp_memo.kara` | the same runs found by a search from the left that tries a new stamp first and remembers each letter and offset that fails, with the stamps then placed in an order where each comes after every neighbour it lies on. O(n m) |
| `differential.kara` | the five arms against the statement read literally, six properties |

The arms return different stamps for the same target: for LeetCode's
second example ★ and frontier return `[0, 3, 1]`, queue `[2, 3, 0, 1]`,
and layers and memo `[3, 0, 1]`. So every arm prints, for each case,
whether it gave stamps and whether they are right: `stamped` when
stamping its answer in turn onto `?`s gives the target within
`10 * target.length` turns, `cannot be stamped` for an empty answer, and
`INVALID STAMPS` otherwise.

Every arm prints the same 14 lines: LeetCode's two examples and seven
more (a target equal to the stamp, a stamp of one letter, two letters in
the wrong order, a letter the stamp lacks, and three that need stamps
over stamps); for 300 random cases, a stamp of 1 to 5 letters from `a`,
`b` and `c` and a target of up to 60 letters, made by stamping, made by
stamping with one letter changed, or random, how many were stamped, the
targets' letters and a checksum; and four of LeetCode's largest, with
targets of 1,000 letters: all `a` for the stamp `a`, made by stamping
with stamps of 10 and of 500 letters, and the first of those with its
last letter changed to one the stamp lacks. `moves_to_stamp.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: from `n` `?`s, every stamp at every place, turn after turn,
keeping every string reached, until the target turns up or nothing new
can be reached. It checks 3,200 random cases, each a stamp from `a`,
`b` and `c` and a target made by stamping, made by stamping with one
letter changed, or random: 3,000 with targets of up to 7 letters against
the statement, and 200 with stamps of up to 20 letters and targets of up
to 300 against the other properties; the targets hold 43,448 letters and
1,542 are stamped.

| | property |
|---|---|
| P1 | stamps exactly when the statement reaches the target, on the small cases |
| P2 | stamps given, stamped in turn onto `?`s, give the target within `10 * target.length` turns, and a target made by stamping always gets them |
| P3 | the stamp and the target both reversed get stamps exactly when they do as they are |
| P4 | a target holding a letter the stamp lacks gets none, and one that gets right stamps still gets them with the stamp written in front |
| P5 | a target that gets right stamps followed by another made by stamping, which also does, still gets them |
| P6 | each arm agrees with at least two of the other four on whether there are stamps |

It prints `3200 cases, targets of 43448 letters, 1542 stamped, 95000
checks over 5 arms: 0 failures` under `karac __mir-run` (8 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the stamps in the order they were peeled | P2 723, P4 74, P5 32 |
| M2 | ★: a window's first letter never compared | P1 218, P2 231, P3 331, P4 137, P6 223 |
| M3 | ★: one sweep only | P1 321, P2 278, P3 584, P6 415 |
| M4 | queue: the window starting at an erased letter skipped | P1 107, P2 116, P3 215, P5 149, P6 192 |
| M5 | queue: every erased letter counted off | P1 153, P2 330, P4 248, P5 112, P6 178 |
| M6 | queue: the leftmost window holding a letter skipped | P1 115, P2 127, P3 215, P4 139, P5 138, P6 201 |
| M7 | frontier: only the windows starting at an erased letter | P1 314, P2 270, P3 583, P6 403 |
| M8 | frontier: each window looked at again once at most | P1 38, P2 73, P3 93, P4 1, P6 107 |
| M9 | frontier: a window fits only once its first letter is erased | P1 1438, P2 1067, P6 1542 |
| M10 | layers: the last letter at any offset | P1 92, P2 303, P3 160, P6 92 |
| M11 | layers: a new stamp underneath at any letter | P1 106, P2 357, P5 5, P6 137 |
| M12 | layers: each stamp placed where it is first shown | P2 548 |
| M13 | memo: offset 1 never tried after a stamp ends | P1 138, P2 104, P3 220, P6 169 |
| M14 | memo: a new stamp underneath at any letter | P1 106, P2 578, P6 137 |
| M15 | memo: stamps shown from offset 0 not split off | P2 1034, P4 508, P5 244 |

P2 kills all fifteen, P1 and P6 twelve, P3 eight, and P4 and P5 six
each. Three mutants say rightly whether there are stamps and give the
wrong ones: M1 returns them backwards, M12 starts each stamp at the
first letter it shows, and M15 merges a stamp shown from offset 0 into
the one before. P1, P3 and P6 look only at whether there are stamps and
miss all three; P2 replays them, and P4 and P5 replay the stamps for
their new targets, which is how they see M1 and M15 even where P2 does
not. M12's stamps are wrong only for a target that needs a stamp shown
from past its first letter. P4 and P5 ask about their new targets only
when the arm's own stamps were right, and none of those new targets
caught M12, so only P2 sees it.

M9 never stamps anything: the target's first letter is erased only by
the window starting there, which with this edit never fits. It fails
exactly the targets that can be stamped, and since a reversed target
can be stamped exactly when the target can, P3 misses it, as P4 and P5
do, which ask something only of a target that got stamps. M3, M7 and
M13 stop short in the same direction, answering no stamps for some
targets that have them, which P4 and P5 again cannot see; M10, M11 and
M14 answer stamps where there are none, which then fail the replay in
P2. P3 sees the mistakes that treat one end of a window or of the
target differently from the other (M2, M4, M6, M7, M10, M13), and two
that depend on the order the windows are looked at in: one sweep only
(M3), which peels from the left, and M8.

Nine other edits were tried and set aside. Five failed exactly the same
checks as another edit: frontier with no frontier after the first sweep
and layers with no new stamp on top, as M3; ★ never trying the last
window, as M9, since then the target's last letter is never erased; and
★ and queue giving stamps with one letter left, as each other. Three
were sound but beyond three an arm (queue returning the stamps backwards,
layers placing the stamps not shown from offset 0 left to right, and
memo letting its last letter show any offset). One was equivalent: memo
counting off a right neighbour it did not lie on, which can only happen
once that neighbour has been placed.

## Verification

Every arm prints the same output as `moves_to_stamp.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 0.5 to 1.0 s each and the
differential 8 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

Legacy refuses all five arms, the differential and the bench program at
the first `*` on an element of a vector's `.iter()` ("unary '*'
requires 'ref T', ... found 'i64'", or `'u8'` in the bench program),
legacy's older rule; under v2 the
element is a reference and the `*` is required. Legacy is frozen, so
none of this is filed.

## Benchmarks

The bench program builds 50 targets of 1,000 letters once, LeetCode's
largest, each made by stamping at random with its own stamp of 5 to 20
letters from `a`, `b` and `c` until no `?` is left, and every other one
then with one letter changed; in each of 100 rounds it runs the ★ arm on
every target, each round starting from a different one, and folds the
stamps into a checksum. Every implementation prints `100 rounds over 50
targets of 1000 letters: 3500 stamped, 738500 stamps, checksum
358320122`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.26 to 0.35 s | 0.28 s |
| Rust (`rustc -O`) | 0.34 to 0.44 s | 0.36 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.32 to 0.35 s | 0.34 s |
| Go | 0.62 to 0.67 s | 0.65 s |
| Python | 23.8 s | |
| Kāra (`karac build --mir`) | 0.47 to 0.55 s | 0.49 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about 85 times C's.

v2 takes 1.45 times Rust's median time under overflow checks and 1.75
times C's. Under valgrind's cachegrind v2 runs 7.88 billion instructions
and 1.58 billion branches with 33.5 million mispredicted, Rust with
overflow checks 5.47 billion, 0.81 billion and 31.6 million, and C 3.60
billion, 0.30 billion and 6.6 million. v2 mispredicts about as often as
Rust and runs about twice its branches; that the extra branches are
bounds checks on `t[p + k]` and `s[k]` in the window loop, which Rust's
optimizer removes, is inferred, not profiled.
</content>
</invoke>
