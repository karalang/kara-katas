# 253. Meeting Rooms II

How many conference rooms does it take to hold every meeting? The answer is the
maximum number ever in progress at once.

```
[[0,30],[5,10],[15,20]]  -> 2      [[7,10],[2,4]]           -> 1
[[1,5],[5,10]]           -> 1      [[1,4],[2,5],[3,6]]      -> 3
```

**Constraints:** `0 ≤ intervals.length ≤ 10⁴`; `0 ≤ start < end ≤ 10⁶`.

The follow-up to [#252](../252-meeting-rooms/), and literally so: that kata's
sweep counts concurrent meetings and stops the moment the count reaches 2. This
one runs the same counter to the end and reports its peak.

## Approaches

| file | state | encodes the touching rule as |
|---|---|---|
| `min_meeting_rooms.kara` ★ | min-heap of end times | `heap[0] <= start` |
| `min_meeting_rooms_sweep.kara` | two sorted coordinate lists | `ends[j] <= starts[k]` |
| `min_meeting_rooms_events.kara` | `(time, ±1)` event list | a **sort tie-break** |
| `differential.kara` | 1,500 randomized inputs, all three agree | — |

## The mechanism

**Only one question is ever asked of the occupied rooms:** has the
earliest-finishing meeting freed up yet? That is why the heap is keyed on *end*
time and why the sweep can throw the pairing away entirely — which meeting frees
a room never matters, only how many are running.

**Touching does not need a second room.** A meeting ending exactly as the next
begins releases its room in time, so every file uses `<=` rather than `<`. The
heap and the sweep say that in an operator. The event list says it in a sort
order, and that difference is the whole reason the third file is here.

## The tie-break, and why it fails quietly

`min_meeting_rooms_events.kara` sorts `(time, delta)` pairs lexicographically, so
at a shared timestamp `-1` sorts before `+1` and a room is released before the
next meeting claims one. Drop the tie-break to compare only the timestamp and
**nothing fails loudly**. The sort is stable, so the answer then depends on the
order events happened to be *pushed*, which depends on the input order:

| input | push order at the shared time | correct | timestamp-only |
|---|---|---|---|
| `[[1,5],[5,10]]` | `(5,-1)` before `(5,+1)` | 1 | 1 ✅ |
| `[[9,10],[4,9],[4,17]]` | `(9,+1)` before `(9,-1)` | 2 | **3** ❌ |

So the obvious touching test passes and an apparently unrelated case breaks —
and the second one is LeetCode's own follow-up example, which is a fair warning
about how easily this ships.

**Measured, not reasoned about.** My first draft of that file's comment claimed
`[[1,5],[5,10]]` was where a timestamp-only comparator diverges. Building the
broken variant showed it survives there; the comment now names the case that
actually fails.

## Does the differential catch it?

A cross-check is only worth what it detects, so the harness was tested against
the bug it exists to find. With the tie-break removed from `count_events`:

```
mismatches 187        (of 1,500 cases — 12.5%)
```

and with it restored, `0`. The generator earns that by drawing times from a
**deliberately small pool** (coordinates `0..23`, up to 10 meetings): coincident
endpoints are the only shape the three counters can differ on, and a wide draw
produces them too rarely to test anything. Census over 1,500 cases: **763 contain
an end coinciding with a start** — 51%, by construction rather than luck.

## Kāra features exercised

- **A hand-rolled binary min-heap over `Vec[i64]`** — push/sift-up and
  pop/swap-last/sift-down. Kāra has no standard-library heap; this is the same
  shape [#23](../../1-100/23-merge-k-sorted-lists/)'s `heap.kara` uses over
  shared-struct handles, but with plain `i64` keys, so it carries **no refcount
  traffic** — a deliberately different surface from #23's.
- **A comparator with a conditional** — `if a.0 != b.0 { a.0.cmp(b.0) } else { a.1.cmp(b.1) }`,
  a step up from #56/#252's single-key `sort_by`.
- **`while true { … break }`** as the sift-down loop form.
- **`Vec[i64].sort()`** beside `Vec[(i64,i64)].sort_by(…)` — two sort surfaces in
  one kata.

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`; the two with
mirrors match Python.

No compiler bugs found. The heap, the conditional comparator and the two sort
surfaces are all constructs earlier katas have already driven bugs out of, so
this is a clean run over known ground rather than new.

## Running

```bash
karac run min_meeting_rooms.kara
karac run min_meeting_rooms_sweep.kara
karac run min_meeting_rooms_events.kara

diff <(karac run min_meeting_rooms.kara) <(python3 min_meeting_rooms.py) && echo OK
diff <(karac run min_meeting_rooms.kara) <(karac run min_meeting_rooms_sweep.kara) && echo OK
diff <(karac run min_meeting_rooms.kara) <(karac run min_meeting_rooms_events.kara) && echo OK

# 1,500 randomized inputs, three counters cross-checked, mirrored in Python
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

# run == build, on every program
for f in min_meeting_rooms min_meeting_rooms_sweep min_meeting_rooms_events differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```
