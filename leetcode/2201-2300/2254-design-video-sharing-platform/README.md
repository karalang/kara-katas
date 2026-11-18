# 2254. Design Video Sharing Platform

You have a video sharing platform where users can upload and delete
videos. Each `video` is a **string** of digits, where the `i`th digit of
the string represents the content of the video at minute `i`. For
example, the first digit represents the content at minute `0` in the
video, the second digit represents the content at minute `1`, and so on.
Viewers of videos can also like and dislike videos. Internally, the
platform keeps track of the **number of views, likes, and dislikes** on
each video.

When a video is uploaded, it is associated with the smallest available
integer `videoId` starting from `0`. Once a video is deleted, the
`videoId` associated with that video can be reused for another video.

Implement the `VideoSharingPlatform` class:

- `VideoSharingPlatform()` Initializes the object.
- `int upload(String video)` The user uploads a `video`. Return the
  `videoId` associated with the video.
- `void remove(int videoId)` If there is a video associated with
  `videoId`, remove the video.
- `String watch(int videoId, int startMinute, int endMinute)` If there
  is a video associated with `videoId`, increase the number of views on
  the video by `1` and return the substring of the video string starting
  at `startMinute` and ending at `min(endMinute, video.length - 1)`
  (**inclusive**). Otherwise, return `"-1"`.
- `void like(int videoId)` Increases the number of likes on the video
  associated with `videoId` by `1` if there is a video associated with
  `videoId`.
- `void dislike(int videoId)` Increases the number of dislikes on the
  video associated with `videoId` by `1` if there is a video associated
  with `videoId`.
- `int[] getLikesAndDislikes(int videoId)` Return a **0-indexed**
  integer array `values` of length `2` where `values[0]` is the number
  of likes and `values[1]` is the number of dislikes on the video
  associated with `videoId`. If there is no video associated with
  `videoId`, return `[-1]`.
- `int getViews(int videoId)` Return the number of views on the video
  associated with `videoId`, if there is no video associated with
  `videoId`, return `-1`.

```
upload("123"), upload("456"), remove(4), remove(0), upload("789"),
watch(1, 0, 5), watch(1, 0, 1), like(1), dislike(1), dislike(1),
getLikesAndDislikes(1), getViews(1)
  ->  0, 1, 0, "456", "45", [1, 2], 2

watch(0, 0, 1), like(0), dislike(0), getLikesAndDislikes(0), getViews(0)
  ->  "-1", [-1], -1
```

**Constraints:** `1 <= video.length <= 10^5`; the sum of `video.length`
over all calls to `upload` does not exceed `10^5`; `video` consists of
digits; `0 <= videoId <= 10^5`; `0 <= startMinute < endMinute < 10^5`;
`startMinute < video.length`; at most `10^5` calls in total.

The ids freed by `remove` wait in a min-heap: `upload` takes the
smallest of them, and a new id one past the highest used only when none
is free. Every id below the next new one is either held or in the heap,
so the smallest free id is the heap's least, or the next new one. A
watch cuts the video at `min(endMinute, length - 1)`. Upload and remove
O(log n), every other call O(1).

## Approaches

| file | mechanism |
|---|---|
| `videos.kara` ★ | a `struct Video` per id in `Vec[Option[Video]]`, and the ids freed by `remove` in a `PriorityQueue`, which pops the smallest first; a watch, a like and a dislike write through `Some(mut ref video)`; the watch cuts `content[start..last + 1]` |
| `videos_map.kara` | a `Map[i64, Video]` of the videos held, a `SortedSet` of the freed ids taken by `pop_first`, and the next id never used; a watch is `substring(start, end + 1)`, which stops at the video's end by itself |
| `videos_enum.kara` | `enum Slot { Free, Held(Video) }` in a `Vec` indexed by id, the calls on one slot written as `Slot` methods that `match self`, and the lowest free id kept as a number: `upload` fills it and walks up past the held slots, `remove` lowers it to the id it frees; upload O(n) at worst |
| `videos_columns.kara` | one column per field: contents, views, likes and dislikes in parallel `Vec`s, a `Vec[bool]` of the ids held, and the freed ids in a binary min-heap written out by hand in a `Vec[i64]`, `sift_up` after a push and `sift_down` after the root is taken |
| `videos_iter.kara` | iterator methods and `Option` combinators: a `Map[i64, Video]`, the freed ids in a `Set[i64]` whose smallest `upload` takes by `iter().min()`, a watch cut by `chars().skip(start).take(..)`, and the reads finished with `map` and `unwrap_or`; upload O(f) in the f ids free |
| `videos_solution.kara` | LeetCode's Rust template: `struct VideoSharingPlatform` with `fn new() -> Self` and `&mut self` / `&self` methods on `i32` ids; the videos, views and likes in three `HashMap`s, the freed ids in a `BinaryHeap<Reverse<i32>>`, and a watch `v[start..=end]` with the end held by `(end_minute as usize).min(v.len() - 1)`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Each arm runs a list of calls, each `(kind, numbers, text)`, through its
platform and gives the answers as strings. Every arm prints the same 8
lines: LeetCode's two examples and four more (freed ids taken back
smallest first; a watch past the end; a video removed twice; a reused id
that starts again from no views, likes or dislikes), each with its
answers; then 3000 platforms of 1 to 30 calls with the number of answers
and a checksum; then 4 platforms of 2.5 * 10^4 calls, 10^5 in all as the
constraints allow. Calls name ids up to one past the uploads so far, and
videos have 3 to 8 digits. `videos.py` mirrors the ★ arm and its output
is byte-identical.

The ★ arm writes `Some(mut ref video)` where `Some(video)` should do:
under `mut ref self`, `match self.slots[id] { Some(video) => video.views
+= 1, .. }` binds `video` as a `ref` and the write is refused, though a
field place `match self.one` is accepted (kara B-2026-11-17-152).

`karac fix` carries the template in one round of 52 edits: the `use`
lines dropped, `HashMap` to `Map` and `BinaryHeap<Reverse<i32>>` to
`PriorityQueue[i32]` with the `Reverse` taken off the push and the pop,
`::new()` to `.new()`, `&mut self` to `mut ref self` and `&self` to
`self`, `video: String` to `own String`, every `&video_id` key made
`video_id`, `as usize` retyped to `as i64` where it meets `v.len()`,
`"-1".to_string()` to `"-1"`, `Some(&(l, d))` to `Some((l, d))`, `vec![..]`
to `[..]`, and `unwrap_or(&-1)` to `unwrap_or(-1)`. The `as usize`
inside `.min(v.len() - 1)` had no fix until kara B-2026-11-17-147.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the videos held as a plain list of records in no order, an
upload's id the smallest of 0, 1, 2, ... that no record has, found by
trying each in turn; every other call a search of the list, and a watch
built minute by minute from the video's characters. It checks 300 random
platforms of 1 to 30 calls; then 30 of 40 to 80 calls with as many
removes as uploads, so ids are freed and taken back often; then 30 of 20
to 40 calls on ids up to 2, where most calls find a video. All 360 are
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answers are the literal reading's |
| P2 | each watch's answer `-1`, or some uploaded video's text from the watch's start minute, cut short at most |
| P3 | one answer per upload, watch and get, and each watch's no longer than `end - start + 1` |
| P4 | each upload's id held by no video at that moment, and no more than the number held |
| P5 | an upload right after the remove of a held id: an id no larger |
| P6 | each arm agrees with at least three of the other five |

P4 and P5 replay the ids held from the arm's own answers, so they judge
the free-id bookkeeping without the literal reading. The differential
prints `360 cases: checksum 707626588, 12960 checks over 6 arms: 0
failures` under every lane in Verification; the checksum of the literal
answers was checked against a Python reading with a dict of held videos,
each upload's id the least of `range(len + 1)` not held, and a watch a
slice. On a failure it prints the first ten and then the count by
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
| M1 | ★: freed ids never taken back | P1 158, P4 158, P5 89, P6 158 |
| M2 | ★: the last minute never shown | P1 240, P6 240 |
| M3 | ★: a watch not counted | P1 54, P6 54 |
| M7 | map: a new id one too high | P1 336, P4 336, P6 336 |
| M8 | map: the id after the freed one kept as free | P1 158, P4 158, P5 83, P6 158 |
| M10 | map: the largest freed id taken | P1 39, P4 21, P5 18, P6 39 |
| M13 | enum: the walk up stopping before the end | P1 306, P4 306, P6 306 |
| M14 | enum: a dislike counted as a like | P1 21, P6 21 |
| M15 | enum: a watch begun a minute late | P1 266, P2 257, P6 266 |
| M17 | columns: `sift_down` taking the larger child | P1 9, P4 7, P6 9 |
| M18 | columns: the root never swapped up | P1 23, P4 8, P5 14, P6 23 |
| M20 | columns: id 0 never held | P1 249, P4 85, P5 26, P6 249 |
| M23 | iter: a taken id left free | P1 131, P4 131, P6 131 |
| M24 | iter: a watch one minute long | P1 175, P3 175, P6 175 |
| M25 | iter: a missing video's likes `[0, 0]` | P1 151, P6 151 |
| M27 | solution: a new video begun at one view | P1 133, P6 133 |
| M30 | solution: the last minute left off | P1 266, P6 266 |

P1 and P6 kill all seventeen, P4 nine, P5 five, and P2 and P3 one each.
P4 and P5 fail every edit to the free ids, and P5 the ones that hand out
an id above one just freed: a heap that does not keep its least at the
root (M18), a set taken from the wrong end (M10). The edits to views,
likes and dislikes only P1 sees. P2 fails a watch begun late (M15) and
P3 one cut long (M24); a watch cut short passes both, as P3 allows. The
first version of P2 asked that every text reversed leave the answers
alone but for each watch's characters; it killed nothing in thirty-one
and was replaced.

Of the thirty-one, fourteen were not kept, and none survives, crashes
or differs between the backends. Seven fail as a kept one does: freed
ids never taken back in the template (M28) and the enum arm's lowest id
raised by a remove (M12) as the ★ arm's (M1); the ★ arm's one view too
many (M6) as the template's new video at one view (M27); the iter arm's
largest freed id (M22) as the map arm's (M10); its watch counted twice
(M26) as the ★ arm's watch not counted (M3); the template's dislike as
a like (M29) as the enum arm's (M14); and the columns arm's last minute
left off (M21) as the template's (M30). Two fail as each other: the enum
arm's free slot giving 0 views and the template's removed video keeping
its views (M16, M31). The other five fail in ways of their own and are
left out because their arms keep three: the ★ arm's like as a dislike
and free slot freed again (M4, M5), the map arm's watch a minute short
and likes and dislikes swapped (M9, M11), and the columns arm's reused
id keeping its views (M19).

## Verification

Every arm prints the same output as `videos.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the columns arm takes 1.3 s, the ★ and map arms
1.4 s, the template 1.7 s, the iter arm 1.8 s, the enum arm 4.4 s, and
the differential 1.2 s. The enum arm's time is its upload, which walks
up past every held slot.

## Benchmarks

The bench answers 120 platforms of 2.5 * 10^4 random calls, videos of 3
to 8 digits, with the ★ arm in all five languages. Every implementation
prints `120 platforms of 25000 calls: 2099735 answers, checksum
668849013`. The C mirror keeps each video in a fixed 9-byte array and
answers into one buffer; the others allocate a string per video and per
answer.

BENCHTAB
