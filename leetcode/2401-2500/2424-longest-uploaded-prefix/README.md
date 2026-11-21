# 2424. Longest Uploaded Prefix

You are given a stream of `n` videos, each represented by a **distinct**
number from `1` to `n` that you need to "upload" to a server. You need
to implement a data structure that calculates the length of the
**longest uploaded prefix** at various points in the upload process.

We consider `i` to be an uploaded prefix if all videos in the range `1`
to `i` (**inclusive**) have been uploaded to the server. The longest
uploaded prefix is the **maximum** value of `i` that satisfies this
definition.

Implement the `LUPrefix` class:

- `LUPrefix(int n)` Initializes the object for a stream of `n` videos.
- `void upload(int video)` Uploads `video` to the server.
- `int longest()` Returns the length of the **longest uploaded prefix**
  defined above.

```
["LUPrefix", "upload", "longest", "upload", "longest", "upload", "longest"]
[[4], [3], [], [1], [], [2], []]
->  [null, null, 0, null, 1, null, 3]
```

**Constraints:** `1 <= n <= 10^5`; `1 <= video <= n`; all values of
`video` are **distinct**; at most `2 * 10^5` calls **in total** will be
made to `upload` and `longest`; at least one call will be made to
`longest`.

The longest prefix only grows, and it grows past a video only once that
video is uploaded. So a flag for each video and the prefix so far are
enough: `longest` walks the prefix on past every flag set beyond it, and
each video is walked past once over the whole stream.

Kāra writes the class `LuPrefix`, since a type name spells an acronym as
one word.

## Approaches

| file | mechanism |
|---|---|
| `prefix.kara` ★ | a `Vec[bool]` of flags, one past `n` as a sentinel, and the prefix so far; `upload` sets a flag and `longest` moves the prefix on while the next flag is set. O(1) amortized per call |
| `prefix_set.kara` | a `SortedSet[i64]` of the videos still missing, 1 to `n + 1` at the start; `upload` takes a video out, and `longest` is the least one left, less one. O(log n) per call |
| `prefix_union.kara` | union-find over the uploaded videos, with path halving, each joined to an uploaded neighbour so that a set's root is its largest video; video 0 stands uploaded from the start, so `longest` is the root of 0's set. O(α(n)) per call |
| `prefix_naive.kara` | the statement read directly: the uploaded videos in a `Set[i64]`, and `longest` counting up from 1 while each next video is in it. O(n) per call to `longest` |
| `prefix_iter.kara` | iterators: the ★ arm's flags and prefix, with `longest` moving the prefix on by the `count` of the flags past it, `take_while` set, over a slice from the prefix. O(1) amortized |
| `prefix_solution.kara` | LeetCode's Rust template: `struct LUPrefix` with a `vec![false; n as usize + 2]` of flags and a `usize` prefix, `&mut self` methods, and the answer handed back `as i32`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's example; videos in order;
videos backwards; video 1 last; then the constraints' largest, `10^5`
videos in a random order with a `longest` after every upload, and `10^5`
with one after every tenth on average; `10^5` videos in blocks of 100,
each block backwards, with a `longest` after every block; and 3000
random scripts of 1 to 12 videos, as a checksum and the total. Each
script is a list of calls, `(0, video)` an upload and `(1, 0)` a call to
`longest`. `prefix.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 20000 random scripts of up
to 10 videos against a Python set of the uploads scanned from 1.

`check` first reports 4 errors on the template, and `karac fix` carries
it in one call, reporting 14 edits: the brackets of `Vec<bool>`; each
`&mut self` written `mut ref self`; `LUPrefix::new` written with `.`;
`vec![false; n as usize + 2]` written `Vec.filled(n as i64 + 2, false)`;
`usize` written `i64`; the casts `video as usize` and the wrapper's
`as i64` on the method's `i32` answer dropped, since each widens without
one; and every `LUPrefix` written `LuPrefix` (`W0298`, an acronym in
capitals). `Self`, the `while` over `self.up[self.p + 1]` and
`self.p as i32` stand as Kāra.

The naive arm scans from 1 at every call to `longest`, so on the blocks
case the harness calls it once per block, not after every upload: with
a call after every upload, the scans add up to `5 * 10^9` steps, and the
first version took 73 s compiled.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: at each call to `longest`, the videos 1, 2, 3, ... each
looked for among the uploads so far by a walk of them, and the answer
is how many are found before the first that is not. No flags or set
are kept. It checks 300 random scripts of 1 to 10 videos, each
uploading a random number of them in a random order; then 30 of up to
100 videos, all uploaded; then 30 of up to 100, all uploaded in order
but for a few neighbours swapped. A `longest` follows an upload with
probability 1 in 1 to 3, a quarter of the scripts start with one, and
every script ends with one. All 360 are drawn before any arm
answers. The first version tried every length from `n` down, each of
its videos looked for by a walk, and on scripts of up to 200 videos it
took minutes under `karac __mir-run`.

| | property |
|---|---|
| P1 | the answers are the literal reading's |
| P2 | the answers never fall, and none passes the number of uploads before it |
| P3 | every `longest` called twice: every answer twice |
| P4 | the uploads between two calls to `longest` reversed: the same answers |
| P5 | the videos never uploaded uploaded at the end, largest first, then `longest`: the answers and then `n` |
| P6 | each arm agrees with at least three of the other five |

P2 holds because uploads only add to the prefix and a prefix of length
`i` needs `i` uploads. P3 holds because `longest` changes nothing the
answer depends on, P4 because the answer depends only on which videos
are uploaded, not on their order, and P5 because once every video is
uploaded the whole range is the prefix.

The differential prints `360 cases: checksum 889557335, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and counts up from 1 while `length + 1 in seen`. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one step per call | P1 138, P3 138, P5 293, P6 138 |
| M2 | ★: the next but one looked at | P1 260, P5 360, P6 260 |
| M6 | ★: the last video never counted | P1 126, P5 360, P6 126 |
| M7 | set: 0 kept missing | P1 360, P2 360, P5 360, P6 360 |
| M9 | set: the largest missing read | P1 342, P2 342, P6 342 |
| M11 | set: even videos never removed | P1 148, P5 327, P6 148 |
| M12 | union: no join downward | P1 220, P5 360, P6 220 |
| M13 | union: no join upward | P1 135, P4 59, P5 318, P6 135 |
| M14 | union: the low set hung past the video | P1 171, P2 101, P4 40, P5 120, P6 171 |
| M18 | naive: the count started at 1 | P1 276, P2 161, P6 276 |
| M19 | naive: one less returned | P1 360, P2 276, P5 360, P6 360 |
| M21 | naive: a gap of one stepped over | P1 178, P2 165, P6 178 |
| M22 | iter: the count set, not added | P1 182, P2 168, P3 220, P5 150, P6 182 |
| M23 | iter: every flag beyond counted | P1 247, P2 177, P3 247, P6 247 |
| M25 | iter: the gaps counted | P1 360, P2 235, P5 228, P6 360 |
| M27 | solution: one more returned | P1 360, P2 249, P5 360, P6 360 |
| M31 | solution: never less than 1 | P1 276, P2 132, P6 276 |


P1 and P6 kill all seventeen, P5 twelve, P2 eleven, P3 three and P4
two.

Fourteen are not kept. Thirteen fail exactly as a kept one: the ★ arm's
and the template's flag set one low and the iter arm's next video
skipped (M3, M29, M24) as the ★ arm's next but one looked at (M2); the ★
arm's one more returned and the set arm's first missing returned (M4,
M10) as the template's one more returned (M27); the ★ arm's and the
template's prefix started at 1 (M5, M30) as the naive arm's count
started at 1 (M18); the set arm's next video marked uploaded and the
naive arm's next video inserted (M8, M20) as the union arm's no join
downward (M12); the union arm's root of 1 read (M15) as the template's
never less than 1 (M31); the naive arm's one step only (M17) as the set
arm's even videos never removed (M11); the iter arm's every video taken
as uploaded (M26) as the set arm's largest missing read (M9); and the
template's one step per call (M28) as the ★ arm's (M1).

One survives, and is equivalent: the union arm's join down never
checked (M16) hangs the set below a new video under it even when the
video below is not uploaded. A parent there still points up, to an
uploaded video, and never into the set of 0, whose videos are all
uploaded, so the root of 0, the answer, is the same.

## Verification

Every arm prints the same output as `prefix.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.4 to 2.4 s, but for the naive
and set arms, which take 31 s and 27 s there and 1.1 s and 0.5 s under
`karac run`: the naive arm scans its `Set` from 1 at every call, and
the set arm makes `10^5` inserts into and removals from a `SortedSet`
per large case, each a run of interpreted tree steps. The differential
takes 1.6 s under `karac __mir-run`, 1.3 s under `karac
__mir-llvm-asan` and 0.8 s under `karac run`.

## Benchmarks

The bench builds 10 scripts of `10^5` uploads once from its own
generator: script `s` is the videos 1 to `10^5` in order, shuffled
within windows of `2^(s + 3)`, so the prefix grows in steps of every
size from 8 to 4096 videos. It then makes 50 passes, running every
script on a fresh structure with a `longest` after every upload, the
constraints' largest, and folding each answer plus the pass into the
checksum. The bench uses the ★ arm, the flags and the prefix so far, in
all five languages. Every implementation prints `50 passes over 10
scripts of 10^5 uploads: checksum 501476579`. The flags are a list of
booleans in every language, made afresh for every script, and in C a
`calloc`'d array freed after it.

BENCHTAB
