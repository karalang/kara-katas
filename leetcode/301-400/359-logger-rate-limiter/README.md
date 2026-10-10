# 359. Logger Rate Limiter

Design a logger that receives a stream of messages with timestamps, in
non-decreasing order, and decides for each whether to print it: a message
prints unless the same message printed in the last 10 seconds, that is at a
time `t'` with `t - 10 < t' <= t`. A refused message does not count as
printed.

```
shouldPrintMessage(1, "foo")   -> true
shouldPrintMessage(2, "bar")   -> true
shouldPrintMessage(3, "foo")   -> false
shouldPrintMessage(8, "bar")   -> false
shouldPrintMessage(10, "foo")  -> false   (10 < 1 + 10)
shouldPrintMessage(11, "foo")  -> true
```

**Constraints:** `0 <= timestamp <= 10^9`; `1 <= message.length <= 30`; at
most `10^4` calls.

## Approaches

| file | mechanism | memory |
|---|---|---|
| `logger.kara` ★ | a `Map` from message to the earliest time it may print again; printing sets it to `t + 10` | every distinct message ever seen |
| `logger_window.kara` | a `VecDeque` of the (time, message) pairs printed in the last 10 seconds and a `Set` of the same messages; expired entries leave both before each answer | the messages of one window |
| `logger_buckets.kara` | ten one-second buckets in a ring, each holding its second and a `Set` of the messages printed in it; a message is refused if a live bucket holds it | the messages of one window |
| `differential.kara` | the map and bucket arms against an oracle that scans the whole printed history, 20,000 checks, five properties | — |

`should_print_message` takes `message: own String` in every arm, because the
arms that print a message keep it.

Every arm prints the same 12 lines: the LeetCode example, ten edge cases (no
calls, one call, exactly ten seconds later, nine seconds later, the same
timestamp twice, refusals that must not reset the clock, independent
messages, the empty message, prefixes, timestamps near `10^9`), and a
checksum over 20,000 random calls. A line shows one `T` or `F` per call.
`logger.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the map and bucket arms, plus an oracle
that keeps every printed (time, message) pair and refuses a call when the
same message printed at a time in `(t - 10, t]`. The test draws 2,000 random
sequences of 0 to 30 calls over one to four messages, with timestamps
advancing by 0 to 6 seconds per call.

| | property |
|---|---|
| P1 | each arm gives the oracle's answer to every call |
| P2 | no arm prints a message twice within 10 seconds |
| P3 | the first call with a given message always prints |
| P4 | shifting every timestamp by the same amount changes no answer |
| P5 | renaming every message the same way changes no answer |

It prints `2000 cases, 20000 checks, 14044 printed, 0 failures` under
`karac run --interp`. The MIR interpreter refuses it and the native builds
abort, for the reasons under Compiler findings, and the window arm is not in
it yet, for the same reason.

## Mutation testing

Nine edits to the copies inside `differential.kara`, each run under
`karac run --interp`. All nine are killed.

| # | mutation | how |
|---|---|---|
| M1 | map: refuses at exactly ten seconds | P1, 937 failures |
| M2 | map: a refusal resets the clock | P1, 1456 failures |
| M3 | map: a 9-second window | P1 and P2, 2076 failures |
| M4 | buckets: looks at only 9 of the 10 buckets | P1, P2 and P4, 2286 failures |
| M5 | buckets: a bucket reused for a new second keeps its old messages | P1, 721 failures |
| M6 | buckets: ignores which second a bucket belongs to | P1, 1600 failures |
| M7 | buckets: an 11-second window | P1, 917 failures |
| M8 | oracle: refuses at exactly ten seconds | P1, 1874 failures |
| M9 | oracle: compares timestamps only | P1, 2724 failures |

## Verification

The map and bucket arms print the same output as `logger.py` under
`karac run --interp` and `karac __mir-run` (the v2 MIR interpreter). The
bucket arm is also byte-identical under LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`. The map arm is not: see below. The window
arm printed the same output with `window.get(0)` in place of
`window.front()`, but as committed it waits for `front` to pass
`karac check`.

The bench program prints `558265 of 1000000 calls printed, checksum 467012428`
under `karac __mir-run`, as do its C, Rust, Go and Python mirrors.

## Benchmarks

Not measured. The legacy native build of the bench program aborts with a
double free (below), so there is no Kāra binary to time yet. The C, Rust, Go
and Python mirrors are written and agree on the checksum.

## Compiler findings

- **Legacy codegen: double free.** The map arm aborts with
  `free(): double free detected` under `karac build` and LLJIT, before it
  prints anything. The trigger is an f-string temporary passed to the
  `own String` parameter and stored with `self.next_ok[message] = ...`;
  the same method called with string literals runs correctly. Legacy codegen
  is frozen for the v2 rewrite (kara, 2026-10-06), so this is noted here and
  not filed.
- **`VecDeque.front` is refused by `karac check`**, as in kata 358. The
  window arm keeps `match self.window.front() { ... }`. Handed to the stdlib
  thread.
- **MIR builder: `if w` on a borrowed bool.** In the differential,
  `for w in want.iter() { if w { ... } }` passes `karac check`, but
  `karac __mir-run` refuses it with
  `invalid MIR: main: bb149[term]: switchInt on ref bool`. Handed to the MIR
  builder thread.
- **The D5 migrator misses a key moved by index-assign.**
  `KARAC_D5_MIGRATE=1 karac fix` adds `own` to a parameter moved by
  `m.insert(k, v)`, but not to one moved by `m[k] = v`, which inserts on a
  missing key. The `own` here was written by hand. Handed to the stdlib
  thread.
