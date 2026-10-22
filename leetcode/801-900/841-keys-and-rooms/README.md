# 841. Keys and Rooms

There are `n` rooms labelled `0` to `n - 1`, and all of them are locked
except room 0. The goal is to visit every room, but a locked room can be
entered only with its key. Each room holds a set of distinct keys, each
labelled with the room it opens, and visiting a room picks up all of its
keys. Given `rooms`, where `rooms[i]` is the set of keys in room `i`,
return `true` if every room can be visited and `false` otherwise.

```
rooms = [[1],[2],[3],[]]            ->  true
rooms = [[1,3],[3,0,1],[2],[0]]     ->  false
```

**Constraints:** `2 <= n <= 1000`, `0 <= rooms[i].length <= 1000`, `1 <=
sum(rooms[i].length) <= 3000`, `0 <= rooms[i][j] < n`, and the keys in
each room are distinct.

## Approaches

Every arm finds the rooms that room 0 leads to through the keys; they
differ in the order they open them and how they keep track.

| file | mechanism |
|---|---|
| `keys_and_rooms.kara` ★ | a stack: every room opened goes on a stack, and a room taken off it gives up its keys, each key to a room not yet opened opening it and putting it on the stack; a count of the rooms opened is compared with `n`. O(n + keys) |
| `keys_and_rooms_queue.kara` | breadth first: a `VecDeque` of rooms in the order their keys are found, each room taken from the front visited and the keys to rooms not yet seen added at the back; then every room must be seen. O(n + keys) |
| `keys_and_rooms_recursive.kara` | depth first by recursion: visiting a room marks it and visits each room it holds a key to that is not yet marked. O(n + keys) |
| `keys_and_rooms_sweeps.kara` | sweeps until nothing opens: sweep after sweep over all the rooms, every open room's keys open the rooms they fit, until a sweep opens nothing; then no room may be shut. O(n (n + keys)) at worst, one sweep for each room a chain of keys passes backwards |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 16 lines: LeetCode's two examples; eight more
(two rooms with and without the key to room 1, a chain of keys running
backwards, a room holding only its own key, room 0 holding every key,
two pairs of rooms that open each other, a key to room 2 that leads back
to room 1, and a room holding keys that are all of no use because no one
can reach it); two chains of LeetCode's most rooms, 1000, one forwards
and one backwards; three sets of 1000 rooms with up to LeetCode's most
keys, 3000, put in random rooms, two of them threaded so that every room
is reachable; and 300 random cases with how many can visit every room
and a checksum. `keys_and_rooms.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: a room can be visited when it is room 0 or a room that can be
visited holds its key, worked out as the closure of "holds the key to"
over every pair of rooms. Its 1,600 cases come in four kinds of 400: 2
to 6 rooms with any number of keys; up to 12 rooms with few keys; up to
12 rooms threaded so that every room is reachable, with one key then
taken away; and up to 12 rooms with many keys. In 447 of them every room
can be visited.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | rooms 1 to `n - 1` given new numbers by a shuffle give the same answer |
| P3 | every room's keys in the opposite order give the same answer |
| P4 | a key to room 0 put in every room that lacks one gives the same answer |
| P5 | a new room holding no keys, its key put in room 0, gives the same answer |

It prints `1600 cases, 447 with every room visited, 32000 checks over 4
arms: 0 failures` under `karac __mir-run` and `karac __mir-llvm-run`,
and the same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: room 0 not counted | P1 447 |
| M2 | ★: a room's last key ignored | P1 423, P3 64, P4 304, P5 24 |
| M3 | ★: room 0 not marked opened | P1 347, P4 352 |
| M4 | queue: room 0 not marked seen | P1 216, P4 216 |
| M5 | queue: only the first new key of each room taken | P1 204, P3 131, P5 243 |
| M6 | queue: the last room not checked | P1 144, P2 43, P5 144 |
| M7 | recursive: the visit going only to higher rooms | P1 269, P2 68 |
| M8 | recursive: each room's first key not followed | P1 395, P3 64 |
| M9 | recursive: the visit starting at room 1 | P1 398, P2 83, P4 428 |
| M10 | sweeps: one sweep only | P1 181, P2 68 |
| M11 | sweeps: a shut room's keys used too | P1 169 |
| M12 | sweeps: one room left shut allowed | P1 252 |

P1 kills all twelve. M1 fails exactly the 447 cases where every room can
be visited, since it never reaches its count; it, M11 and M12 only P1
sees, because each misjudges a case the same way however its rooms are
numbered or its keys ordered. P2, the rooms renumbered, sees the edits
that lean on room numbers: the last room (M6), higher rooms only (M7),
room 1 (M9), and one sweep in number order (M10). P3, the keys reversed,
sees the edits that lean on where a key sits in its room (M2, M5, M8).
P4 sees the edits that get room 0 wrong once some room holds its key: M3
counts room 0 a second time, M4 sees it only through that key, and under
M9 a key back to room 0 lets the visit from room 1 reach everything. P5
puts the new key last in room 0, so it sees M2, which ignores it, M5,
which takes only room 0's first new key, and M6, whose unchecked last
room is now the new one. M6 is the weakest kill, 144 checks: it needs
every room but the last to be reachable.

## Verification

Every arm prints the same output as `keys_and_rooms.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `4a744e1ec3`, and the runtime archives are
current with them. Under `karac __mir-run` the ★, queue and recursive
arms take 0.25 s, the sweeps arm 1.5 s (the backward chain of 1000 rooms
takes it 1000 sweeps), and the differential 1.6 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends run the ★ arm right: `karac run --interp`,
`karac run`, `karac build` and a `KARAC_AUTO_PAR=1` build all print the
same output. They refuse the other three arms and the differential at
`*key`, a key read through `rooms[room].iter()`: legacy types the loop
variable as an `i64`, not a reference, though `karac check` accepts it
on v2. Legacy refuses the bench program as moving a case out of an
index, which v2's borrowing parameters do not do. Legacy is frozen, so
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
cases once, each of LeetCode's most rooms, 1000: case `g` puts 2000
keys, each to a random room, in random rooms, and when `g` is even then
threads the rooms in a shuffled order, each holding a key to the next,
so that every room can be visited, which brings it to at most 2999 keys.
Each of 36,000 rounds asks the next case. Every implementation prints
`36000 rounds of 64 cases: 18000 with every room visited, checksum
374295988`, the Kāra program under `karac __mir-run` included, in 44 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.75 to 1.05 s |
| Rust (`rustc -O`) | 0.78 to 1.23 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.80 to 1.03 s |
| Go | 0.80 to 0.99 s |
| Python | 3.8 to 4.2 s |
| Kāra (`karac build --mir`) | 0.81 to 0.88 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 0.85 s, against Rust's
0.84 (0.85 under overflow checks), C's 0.78 and Go's 0.84: 1.0 times
Rust's time under overflow checks, 1.09 times C's and 1.01 times Go's.
Under valgrind's cachegrind C runs 1.22 billion instructions and 257
million branches, Rust 1.56 billion and 369 million and v2 2.02 billion
and 553 million, but the three mispredict about alike, 53, 54 and 57
million branches; most likely those, on the scattered reads of the
marks, are where the time goes, which would leave v2's extra
instructions little to add (not traced). Built for `x86-64-v3`, the
target `karac build` uses, C takes 0.79 to 0.84 s and Rust with overflow
checks 0.86 to 0.97 s, against v2's 0.79 to 0.88 s in the same five
interleaved runs. Python takes 4.0 s, about 5 times C's time. The
comparison with C and Rust waits until after M4.

## Compiler findings

B-2026-10-21-82: an empty list literal `[]` in an `if` branch whose
element type comes only from the other branch passed `karac check` and
stopped both v2 lanes with `a type that failed to check is not lowered
yet`. The harness's natural `chain.push(if i < 999 { [i + 1] } else { []
});` hit it, so it bound the room to an annotated `let` first. The row
was fixed in kara 14180cd414, and the harness is back to the natural
form, which all four arms run right under `karac __mir-run`, `karac
__mir-llvm-run` and `karac __mir-llvm-asan` at kara c8c0d4a166.
