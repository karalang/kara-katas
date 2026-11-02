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
| `min_meeting_rooms.kara` ★ | min-heap of end times | `PriorityQueue[i64]`, `peek() <= start` |
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

The canonical M5 table is generated from `bench/results.json` — see
[§ Benchmarks](#benchmarks) below.

> **The gap this kata deferred to Apple silicon is essentially closed.** It was
> filed at **2.04× behind equal-safety Rust** (against 1.62× on the container)
> and, with [#252](../252-meeting-rooms/)'s 3.70×, raised kara
> `B-2026-08-15-30`. Five compiler changes later it is **1.10×**:
> `B-2026-08-15-30` routed shuffled input to the stable quicksort it was never
> reaching, `B-2026-08-16-3` replaced the partition's leaf merge with a stable
> insertion sort, and `B-2026-08-16-9` contributed three — multiply-shift pivot
> reduction, a `vectorize.enable` hint on a counting pass LLVM's cost model was
> *declining* rather than refusing, and unswitching the scatter so its
> comparison stays in flags instead of being materialised into registers, 15
> instructions per element down to 9. Kāra here went **244.7 ms → 134.2 ms**
> while Rust, C and Go all held still.

**2026-11-02, v2/MIR backend (`karac 0.8.0-dev.14215+g96fca5370`): the gap
reopened, to 1.28×.** The blockquote above is the 2026-08-17 legacy-backend
state. On the MIR backend Kāra/Rust went 1.09× → 1.33× (karac g6697158fa) →
**1.28×** (Kāra/C 0.48× → 0.59× → 0.57×, Kāra/Go 0.29× → 0.35× → 0.34×). The last
step is under 10%, so flat; overall that is a ~1.2× loss against every comparator,
so it is the compiler, not the machine. The benchmark, which shares its
sort-by-start step with [#252](../252-meeting-rooms/), runs 1.18× legacy dd86e3955's
instructions and 1.21× its cycles; filed as [`B-2026-11-02-7`](../../../../kara/docs/bugs-v2.md) (perf, open).

The relationship the container found survives, and it is still the useful part:
#253 *adds* a hand-rolled heap on top of #252's sort-and-scan and comes out
relatively **better** — 1.10× against #252's 1.29×, as it was 2.04× against
3.70× before, and as it is 1.28× against 1.52× on the MIR backend (2026-11-02). Extra non-sort work at parity dilutes the ratio, which is exactly
what you expect if the sort, and only the sort, is the deficit. That the
relationship held through a 2.9× improvement in the sort is the strongest form
of that evidence. (2026-11-02 note: that reads the ratio to Rust. Against legacy
the excess runs the other way, 1.21× cycles here to #252's 1.17×, so dilution does
not describe the MIR regression itself.)

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

### This lane found a Kāra perf gap — and it is now mostly closed

**The x86 numbers in this section are pre-fix** — what the lane originally
reported, and what `B-2026-08-10-9` was filed from. They were never re-measured
on that host, so read them as the history that flagged the gap, not as a current
claim.

The chain, because four ledger rows are easy to conflate:

| row | what it was | outcome |
|---|---|---|
| `B-2026-08-10-9` | fixed-32-run merge sort, non-adaptive | **fixed** (`50a50e8`) |
| `B-2026-08-11-28` | its shuffled-uniform residual, ~1.6× on x86 | closed **`wontfix`** |
| `B-2026-08-15-30` | that residual on the M5 — 2.04× here, 3.70× on #252 | **fixed** (`93ea7a86`) |
| `B-2026-08-16-3` | the 1.80× left after routing | **fixed** (`012645a5`) |
| `B-2026-08-16-9` | the 1.61× left after the leaf | **open** |
| `B-2026-11-02-7` | MIR-backend sort-by-start regression, 1.28× here / 1.52× on #252 (2026-11-02) | **open** |

This kata and [#252](../252-meeting-rooms/) both shuffle their input, so both
land on the shuffled-uniform residual rather than the ordered-input case
`B-2026-08-10-9` addressed. That is why they were the katas that reopened a
`wontfix`: the disposition had been reached entirely on a shared x86 container,
and on the canonical host the gap was materially wider than the number it was
argued from. Re-deciding it on this host was worth 1.7× on the sort.

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

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`819998103`). Workload: build 150k overlapping intervals once and shuffle, then 25 rounds of sort + min-heap room counting; sink = accumulated peak-room checksum.

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-11-02 (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`; `karac 0.8.0-dev.14215+g96fca5370`, v2/MIR backend):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O -C overflow-checks=on` (equal-safety) | 137.5 ms | 0.77× |
| Rust `-O` | 139.3 ms | 0.78× |
| **Kāra (codegen)** | 178.8 ms | 1.00× |
| C `clang -O3` | 313.1 ms | 1.75× |
| Go | 527.4 ms | 2.95× |

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`, karac g96fca5370); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

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

## Bug ledger

**Surfaced [`B-2026-11-02-7`](../../../../kara/docs/bugs-v2.md)** (perf, open). On the v2/MIR backend the
benchmark runs 1.18× legacy dd86e3955's instructions and 1.21× its cycles,
taking Kāra/Rust from 1.09× (legacy, 2026-08-17) to 1.28× (2026-11-02, karac
g96fca5370; 1.33× on g6697158fa); the row's subject is its sort-by-start step. Shared with [#252](../252-meeting-rooms/), which sorts the same way.
