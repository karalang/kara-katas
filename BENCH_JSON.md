# kara-katas — consolidated bench JSON

Machine-readable companion to [`BENCH.md`](BENCH.md). Where `BENCH.md` defines
*how* each kata measures, this defines the *data format* those measurements are
serialized into, so a dashboard (or any tool) can read the whole corpus's
numbers from one file instead of scraping per-kata README tables.

Three layers:

1. **Per-kata `leetcode/<group>/<kata>/bench/results.json`** — emitted by that
   kata's `bench.sh` via [`scripts/bench-lib.sh`](scripts/bench-lib.sh). One file
   per kata, written on every bench run, holding that kata's six metrics.
2. **Top-level `bench-results.json`** — produced by
   [`scripts/consolidate-bench.sh`](scripts/consolidate-bench.sh), which globs
   every per-kata file and merges them. **This is the single feed a dashboard
   reads.**
3. **`BENCH_JSON.md`** (this doc) — the schema contract. `schema_version` is
   bumped here whenever the shape changes.

Current `schema_version`: **1**.

## The six metrics → where they live

| # | Metric | JSON location | Keyed by |
|---|---|---|---|
| 1 | Runtime — seq lane | `measurements[].runtime` (rows with `lane:"seq"`) | lang, approach, lane, mode |
| 2 | Runtime — auto-par | `measurements[].runtime` (rows with `lane:"par"`) | lang, approach, lane, mode |
| 3 | Compile elapsed (cold) | `compile[].elapsed` | lang, approach, mode |
| 4 | Binary size | `measurements[].binary_bytes` | lang, approach, lane, mode |
| 5 | Runtime peak memory | `measurements[].runtime_peak_rss_bytes` | lang, approach, lane, mode |
| 6 | Compile peak memory (cold) | `compile[].compile_peak_rss_bytes` | lang, approach, mode |

Metrics 1, 2, 4, 5 are **runtime-artifact** properties — they vary with lane
(seq vs par) and mode (codegen vs interp), so they share the `measurements[]`
array. Metrics 3 and 6 are **compile** properties — lane-agnostic (you don't
compile a "par binary" differently), so they live in `compile[]`.

## Vocabulary

These string enums are what the dashboard groups/filters on. Keep them exact.

- **`lang`**: `kara` · `rust` · `c` · `go` · `python`
- **`approach`**: the algorithm variant slug, e.g. `brute_force`, `hash_map`,
  `count`. A kata with one approach uses one value throughout.
- **`lane`**: `seq` (single-threaded codegen quality) · `par` (parallel-runtime
  quality). Cross-lane comparisons are not meaningful — see `BENCH.md § Lanes`.
- **`mode`**: `codegen` (karac `build`) · `interp` (karac `run`) · `native`
  (rustc/clang/go compiled output). `rust+rayon` is `lang:"rust", lane:"par"`;
  Go goroutines is `lang:"go", lane:"par", mode:"native"`.

## Per-kata schema (`results.json`)

```json
{
  "schema_version": 1,
  "kata": {
    "id": "204",
    "slug": "count-primes",
    "group": "201-300",
    "title": "Count Primes",
    "workload": "N=10^7 list primes",
    "sink": "(664579, 3203324994356)"
  },
  "env": {
    "host": "Apple M5 Pro",
    "cores": "6P+12E",
    "os": "Darwin 25.4.0",
    "karac": "karac 0.1.0",
    "rustc": "rustc 1.95.0 (...)",
    "clang": "Apple clang version 21.0.0 (...)",
    "go": "go version go1.26.3 darwin/arm64",
    "hyperfine": "hyperfine 1.20.0",
    "measured_at": "2026-05-30T00:00:00Z"
  },
  "measurements": [
    {
      "lang": "kara",
      "approach": "count",
      "lane": "par",
      "mode": "codegen",
      "runtime": {
        "mean_ms": 48.2,
        "stddev_ms": 3.3,
        "median_ms": 47.9,
        "min_ms": 44.1,
        "max_ms": 55.0,
        "user_ms": 551.6,
        "system_ms": 12.0,
        "cpu_pct": 1169.5,
        "runs": 10
      },
      "binary_bytes": 302827,
      "runtime_peak_rss_bytes": 24222924
    }
  ],
  "compile": [
    {
      "lang": "kara",
      "approach": "count",
      "mode": "codegen",
      "elapsed": {
        "mean_ms": 58.7,
        "stddev_ms": 1.3,
        "median_ms": 58.5,
        "min_ms": 56.9,
        "max_ms": 61.2,
        "user_ms": 40.1,
        "system_ms": 16.0,
        "cpu_pct": 95.4,
        "runs": 10
      },
      "compile_peak_rss_bytes": 9646899
    }
  ]
}
```

Notes on field semantics:

- **All times are milliseconds** (`*_ms`). hyperfine reports seconds; the
  emitter converts. Memory and size are **bytes** (`*_bytes`) — the dashboard
  formats KiB/MiB at display time, never the source.
- **`cpu_pct`** is derived: `(user + system) / mean * 100`. ~95–100% means
  single-core; substantially higher means the run went multi-core (the auto-par
  tell from `BENCH.md § Implicit auto-par`).
- **`runtime` / `elapsed` may be `null`** when a comparator was measured for
  size/memory but excluded from the timed hyperfine run (or vice versa). A
  dashboard must tolerate nulls per field rather than assuming every cell is
  populated.
- **`binary_bytes` / `runtime_peak_rss_bytes` may be `null`** for the same
  reason (e.g. an interp row has no binary).

## Top-level schema (`bench-results.json`)

```json
{
  "schema_version": 1,
  "generated_at": "2026-05-30T00:00:00Z",
  "kata_count": 33,
  "katas": [ /* each per-kata results.json verbatim, sorted by numeric id */ ]
}
```

## How a `bench.sh` emits it

A kata's `bench.sh` sources the library and wraps its measurements; structure
is declared once, at the measurement, so labels never have to be parsed back.
See the worked example in
[`leetcode/201-300/204-count-primes/bench/bench.sh`](leetcode/201-300/204-count-primes/bench/bench.sh)
and the API header in [`scripts/bench-lib.sh`](scripts/bench-lib.sh).

Set `BENCH_JSON=0` in the environment to run a `bench.sh` with emission
disabled (every `bench_*` call becomes a no-op) — useful on a box without
`python3`, or when you only want the human-readable console output.

## Regenerating the feed

```bash
# one kata
( cd leetcode/201-300/204-count-primes/bench && ./bench.sh )   # writes results.json

# whole corpus → bench-results.json
./scripts/consolidate-bench.sh
```

The consolidator logs (to stderr) any kata that has a `bench.sh` but no
`results.json` yet, so partial coverage is never mistaken for full coverage.

## Migrating a kata's bench.sh

Mechanical, following kata #204's `bench/bench.sh`:

1. After the `require` block, add the `jq`/`python3` requires (guarded on
   `BENCH_JSON`), set `ROOT="$(cd ../../../.. && pwd)"`, and
   `. "$ROOT/scripts/bench-lib.sh"`. The `../../../..` is from `bench/` up to
   the repo root (`bench → <kata> → <group> → leetcode → root`).
2. After the sink check, call `bench_begin id=… slug=… group=… title=…
   workload=… sink=…`.
3. Replace the runtime `hyperfine` block with `rt_begin` / one `rt_cmd` per
   comparator (declaring `--lang/--approach/--lane/--mode/--name/--cmd`) /
   `rt_end`. The `--name` must match the old `--command-name` verbatim.
4. Replace the compile-elapsed `hyperfine` block with `ce_begin` / `ce_cmd`
   (carries `--prepare`) / `ce_end`.
5. Replace the binary-size loop with `size_put` calls, the runtime-memory
   `print_mem` calls with `mem_put`, and the compile-memory ones with
   `cmem_put`.
6. End with `bench_emit`.

## Migration status

The JSON pipeline landed 2026-05-30. Kata #204 is the migrated reference. The
remaining katas still emit only their README tables until their `bench.sh` is
migrated and re-run. **The live source of truth for what's left is the
consolidator**: `./scripts/consolidate-bench.sh` logs (to stderr) every kata
that has a `bench.sh` but no `results.json` yet, so the pending list never goes
stale against a hand-maintained checklist here.
