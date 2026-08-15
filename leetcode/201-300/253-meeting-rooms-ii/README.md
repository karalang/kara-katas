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

## Benchmark

`bench/` builds **150,000 heavily-overlapping intervals once and shuffles them**,
then runs **25 rounds** of sort + min-heap room counting. Starts advance ~1 per
meeting while durations reach 60, so roughly 30 meetings are live at any instant
and the heap stays deep — a packed non-overlapping set would pin the heap at
size 1 and measure only the sort. Sink `819998103`, reproduced exactly by the C,
Rust, Go and Python mirrors, each hand-rolling the same heap rather than calling
`BinaryHeap` / `container/heap`.

### Runtime — sequential lane

Apple M5 Pro (6P+12E), 2026-08-15, `karac 0.1.0-dev.6106+g50267795a`, hyperfine
30 runs, `KARAC_AUTO_PAR=0`, every lane 99% CPU. This is the canonical host —
`bench/results.json`.

| Impl | Mean ± σ | vs Kāra |
|---|---|---|
| Rust `-O -C overflow-checks=on` (equal-safety) | 119.7 ± 0.6 ms | 0.49× |
| Rust `-O` | 121.3 ± 1.1 ms | 0.50× |
| **Kāra (codegen)** | **244.7 ± 0.9 ms** | 1.00× |
| C `clang -O3` (`qsort`) | 264.9 ± 1.3 ms | 1.08× |
| Go (`sort.Slice`) | 455.2 ± 5.7 ms | 1.86× |

**This is the cleanest measurement in the block** — σ is 0.4% on the Kāra row and
0.5% on Rust's. **Kāra is 2.04× behind equal-safety Rust**, against 1.62× on the
container. Together with [#252](../252-meeting-rooms/)'s 3.70×, the M5 confirms
the gap this kata deferred rather than dissolving it.

The relationship the container found survives, and it is the useful part: #253
*adds* a hand-rolled heap on top of #252's sort-and-scan and comes out relatively
**better** (2.04× vs 3.70×). Extra non-sort work at parity dilutes the ratio,
which is what you would expect if the sort — and only the sort — is the deficit.

### The x86 corroboration run

Container x86-64, `bench/results.container-x86.json` — corroboration only
(BENCHMARKS.md § Hosts).

| lang | mean (ms) | vs Rust |
|---|---|---|
| Rust | 370.5 ± 16.9 | 1.00× |
| **Kāra** | **598.6 ± 18.0** | **1.62×** |
| C | 885.2 ± 10.7 | 2.39× |
| Go | 1121.0 ± 18.9 | 3.03× |

As in [#252](../252-meeting-rooms/), **the C and Go rows are about their sorts,
not their languages**: C uses `qsort`, whose function-pointer comparator cannot
be inlined, and Go's `sort.Slice` pays reflection-based swaps. Neither row should
be read as a language comparison.

### This lane found a Kāra perf gap — kara `B-2026-08-10-9`

Kāra at 1.62× Rust here, and 1.89× on #252, are both sort-dominated. Isolating
the sort — 150k pairs, 25 rounds, clone and `sort_by` only, no heap and no
scan — gives **0.34 s against Rust's 0.16 s, a 2.1× gap**.

That the isolated ratio is *larger* than either kata's is itself the evidence:
each kata carries non-sort work that runs at parity, diluting the ratio. And it
is not the heap — #253 *adds* a hand-rolled heap on top of #252's sort-and-scan
and comes out relatively **better** (1.62× vs 1.89×).

**Settled on the Apple-silicon host, 2026-08-15 — the observation is now a
confirmed result.** It was filed with a single-host caveat because every number
came from one x86 shared container. The M5 lane above removes that caveat: the
gap reproduces on a second, very different host and is **larger** there (this
kata 1.62× → 2.04×, #252 1.89× → 3.70×), on measurements with σ under 1%.
`B-2026-08-10-9` should be read as confirmed rather than provisional.

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
