# 1117. Building H2O

There are two kinds of threads: `oxygen` and `hydrogen`. Your goal is
to group these threads to form water molecules.

There is a barrier where each thread has to wait until a complete
molecule can be formed. Hydrogen and oxygen threads will be given
`releaseHydrogen` and `releaseOxygen` methods respectively, which will
allow them to pass the barrier. These threads should pass the barrier
in groups of three, and they must immediately bond with each other to
form a water molecule. You must guarantee that all the threads from one
molecule bond before any other threads from the next molecule do.

In other words:

- If an oxygen thread arrives at the barrier when no hydrogen threads
  are present, it must wait for two hydrogen threads.
- If a hydrogen thread arrives at the barrier when no other threads are
  present, it must wait for an oxygen thread and another hydrogen
  thread.

We do not have to worry about matching the threads up explicitly; the
threads do not necessarily know which other threads they are paired up
with. The key is that threads pass the barriers in complete sets; thus,
if we examine the sequence of threads that bind and divide them into
groups of three, each group should contain one oxygen and two hydrogen
threads.

Write synchronization code for oxygen and hydrogen molecules that
enforces these constraints.

```
water = "HOH"      ->  "HHO"      ("HOH" and "OHH" are also valid)
water = "OOHHHH"   ->  "HHOHHO"   (any order within each three)
```

**Constraints:** `3 * n == water.length`; `1 <= n <= 20`;
`water[i]` is either `'H'` or `'O'`; there will be exactly `2 * n`
`'H'` in `water`.

The arms are a `sync struct H2o` with `fn new() -> H2o`, `fn
hydrogen(self, release_hydrogen: Fn())` and `fn oxygen(self,
release_oxygen: Fn())`. A struct is named in PascalCase, and `karac`
refuses `H2O`, an all-capitals name it reads as a constant's, with no
fix to rename it (B-2026-11-11-35). LeetCode's threads are a `TaskGroup`
with a task per atom, started in the water's order, and the releases go
to a log behind a `Mutex`. An answer is right when every three atoms of
the log are two hydrogens and an oxygen, so the arms print counts, not
logs.

## Approaches

| file | mechanism |
|---|---|
| `building_h2o.kara` ★ | each oxygen building its molecule: a hydrogen hands a one-shot channel to the oxygens and waits on it; an oxygen takes the bonding lock, receives two hydrogens, releases itself, sends each a channel to say it is out on, and waits for both before it gives the lock up |
| `building_h2o_semaphore.kara` | semaphores and a barrier, as the Python solutions write it with `threading.Semaphore(2)`, `Semaphore(1)` and `Barrier(3)`: two hydrogens and an oxygen pass the semaphores, meet at the barrier, release themselves and only then give their permits back. The semaphores are the standard library's; it has no barrier, so the barrier is a count under a lock |
| `building_h2o_waitlist.kara` | a condition variable built from a `Mutex` and channels: the atoms let into the molecule being built and the ones out of it under the lock, an atom getting in while its element has room, and the third out emptying the molecule and waking every waiter |
| `building_h2o_polling.kara` | the same molecule under a lock, and an atom with no room for its element sleeping for no time at all between looks |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 6 lines: for four waters (LeetCode's two
examples, the hydrogens first, and three molecules), the atoms
released and how many of the molecules came out whole, then over 2000
waters of up to 12 molecules, their atoms in a random order, the atoms
released and how many waters had every molecule whole (`2000 random
waters of up to 12 molecules: 39348 atoms, 2000 with every molecule
whole`), and LeetCode's largest, 20 molecules with every oxygen first.
`building_h2o.py` mirrors the ★ arm with a thread per atom and one-slot
`queue.Queue`s, and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. Each release
function checks, under the log's lock, that the molecule being built
has room for its element, and counts one that finds none. It checks 600
problems of up to 8 molecules, six of them of LeetCode's largest, 20:
the atoms shuffled, a second order of the same atoms, a second water of
up to 8 molecules with the two waters' atoms interleaved, and busy work
of up to 2000 steps for each of the first one to five releases, all
drawn at random before any arm runs.

| | property |
|---|---|
| P1 | the statement read literally: every three atoms of the log are two hydrogens and an oxygen |
| P2 | by a second reading, each atom: its molecule had room for its element when it was released |
| P3 | the same atoms started in another order give whole molecules |
| P4 | with busy work before the first releases, every molecule whole and no atom found no room |
| P5 | two waters at once on two `H2o`s, their atoms interleaved, both whole and no atom found no room |
| P6 | the water twice over on one `H2o`, the second time reordered, gives twice the molecules, whole |

All 14,400 checks pass on every arm: `600 problems: checksum 177651007,
14400 checks over 4 arms: 0 failures`. A Python reading of the same
problems, counting each water's atoms and hydrogens for each arm, gives
the same checksum.

## Mutation testing

Twenty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All twenty are caught
natively, and fourteen under the interpreter too.

| # | mutation | `__mir-run` | `__mir-llvm-run` |
|---|---|---|---|
| M1 | ★: an oxygen released before it takes its hydrogens | P1 531, P2 531, P3 531, P4 531, P5 596, P6 600 | P1 530, P2 530, P3 530, P4 531, P5 596, P6 599 |
| M2 | ★: a hydrogen released before its oxygen calls it | P1 144, P2 144, P3 139, P4 144, P5 240, P6 167 | P1 155, P2 155, P3 146, P4 174, P5 256, P6 192 |
| M3 | ★: an oxygen not waiting for its hydrogens to be out | P1 196, P2 196, P3 175, P4 196, P5 305, P6 337 | P1 208, P2 208, P3 214, P4 220, P5 316, P6 338 |
| M4 | ★: the bonding lock given up at once | P1 446, P2 446, P3 443, P4 446, P5 560, P6 554 | P1 449, P2 449, P3 447, P4 458, P5 559, P6 554 |
| M5 | ★: a hydrogen released twice | P1 600, P2 531, P3 600, P4 600, P5 600, P6 600 | P1 600, P2 531, P3 600, P4 600, P5 600, P6 600 |
| M6 | semaphore: a hydrogen released before the barrier | P1 502, P2 502, P3 493, P4 502, P5 586, P6 579 | P1 461, P2 461, P3 460, P4 493, P5 574, P6 559 |
| M7 | semaphore: an oxygen released before the barrier | P1 373, P2 373, P3 361, P4 373, P5 498, P6 497 | P1 442, P2 442, P3 463, P4 469, P5 557, P6 539 |
| M8 | semaphore: a hydrogen gives back its permit before it is released | none | P1 29, P2 29, P3 23, P4 47, P5 45, P6 64; 291 to 317 in four more runs |
| M9 | semaphore: an oxygen gives back its permit before it is released | none | P1 22, P2 22, P3 21, P4 37, P5 38, P6 54; 234 to 257 in four more runs |
| M10 | semaphore: a hydrogen released twice | P1 600, P2 554, P3 600, P4 600, P5 600, P6 600 | P1 600, P2 559, P3 600, P4 600, P5 600, P6 600 |
| M11 | waitlist: a hydrogen leaves before it is released | none | P1 2, P2 2, P3 1, P4 12, P5 4, P6 2; 245 to 316 in four more runs |
| M12 | waitlist: an oxygen leaves before it is released | none | P3 1, P4 4, P6 1; 120 to 286 in four more runs |
| M13 | waitlist: a hydrogen released before it enters | P1 374, P2 374, P3 386, P4 374, P5 517, P6 467 | P1 378, P2 378, P3 387, P4 377, P5 520, P6 468 |
| M14 | waitlist: an oxygen released before it enters | P1 374, P2 374, P3 374, P4 374, P5 521, P6 454 | P1 384, P2 384, P3 391, P4 392, P5 527, P6 472 |
| M15 | waitlist: an oxygen released twice | P1 600, P2 579, P3 600, P4 600, P5 600, P6 600 | P1 600, P2 579, P3 600, P4 600, P5 600, P6 600 |
| M16 | polling: a hydrogen released before it enters | P1 374, P2 374, P3 386, P4 374, P5 517, P6 467 | P1 375, P2 375, P3 387, P4 375, P5 517, P6 467 |
| M17 | polling: an oxygen released before it enters | P1 374, P2 374, P3 374, P4 374, P5 521, P6 454 | P1 381, P2 381, P3 380, P4 381, P5 524, P6 461 |
| M18 | polling: a hydrogen leaves before it is released | none | P4 9, P5 1; 296 to 427 in four more runs |
| M19 | polling: an oxygen leaves before it is released | none | P1 12, P2 12, P3 7, P4 63, P5 21, P6 22; 316 to 388 in four more runs |
| M20 | polling: a hydrogen released twice | P1 600, P2 552, P3 600, P4 600, P5 600, P6 600 | P1 600, P2 559, P3 600, P4 600, P5 600, P6 600 |

The six the interpreter misses each let an atom leave, or give back its
place, just before it is released rather than just after: a permit given
back (M8, M9), or the molecule left (M11, M12, M18, M19). The
interpreter runs one task at a time and switches only where a task
waits, and giving back a permit or a place is not a wait, so the atom is
still released before the next one runs. Natively the tasks run at once
on every core, and the next molecule's atoms are sometimes released into
this one. How often depends on how busy the machine is: in the mutation
run, three programs at a time, each of the six failed between 6 and 237
checks; run four more times each, one program at a time, every one of
them failed every time, between 120 and 427 checks.

The other fourteen fill a molecule wrongly whatever the schedule, and
fail on both lanes, natively with counts that move with the schedule.

## Verification

Every arm prints the same output as `building_h2o.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file, and `karac fix` has nothing to apply.

The kata found four gaps, all of them fixed. LeetCode names the class
`H2O`, which `karac` refuses as a constant's name, suggesting `H2o` with
no fix to rename the declaration and its uses (B-2026-11-11-35, fixed in
cc0bc927f2): `karac fix` now renames them, and every arm written with
`H2O` comes out as it is here. The harness builds each water with
`String.from_iter(atoms.iter())` over a `Vec[char]`, whose items are
`ref char`: the error named `.cloned()` but offered no edit, because a
call through a type's name never recorded where its arguments end
(B-2026-11-11-36); `karac fix` now adds the `.cloned()` in every arm.
The polling arm empties its molecule under the lock with `g.value =
Molecule { .. }`, a plain `=` on the guard's `mut ref` field: `karac
fix` asked for `let mut g` and the assignment then wrote through the
guard, where a `mut ref` local's `r = v` is refused with the `*r = v`
fix (B-2026-11-11-37); it now gets `*g.value = ..` and `let g` stays.
And that arm, like 1114's, waits with `sleep(Duration.ms(0))`, which
never let another task run before B-2026-11-11-32. The semaphore arm,
like kata 1115's, built its semaphores from channels until
`Semaphore.acquire` waited for another task's `release`
(B-2026-11-11-34, found by kata 1115, fixed in c47fd80f23), and now uses
the standard library's. Every arm was written as Kāra.

## Benchmarks

The bench runs the ★ arm on 500 waters of LeetCode's largest, 20
molecules, each with its atoms in a shuffled order, and prints `500 runs
of 20 molecules: 500 with every molecule whole, checksum 306444059`.
Each language starts a thread or task per atom, 60 for every run. A
hydrogen hands the oxygens something to wait on and waits on it: in C
the semaphore it waits on, put in a ring of two guarded by a mutex and
two counting semaphores, in Kāra and Go a one-shot channel, in Rust a
one-shot `sync_channel`, and in Python a one-slot queue. An oxygen takes
the bonding lock, takes two hydrogens, releases itself, tells each
hydrogen to go and waits until both are out.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python (user is the median CPU
time in user mode, summed over the threads), with karac `3402c1954a` on
LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median | user |
|---|---|---|---|
| Go | 0.051 to 0.068 s | 0.061 s | 0.085 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.129 to 1.479 s | 1.313 s | 4.627 s |
| C (`clang -O3 -march=x86-64-v3`) | 1.294 to 1.613 s | 1.348 s | 0.258 s |
| C (`clang -O3`) | 1.288 to 1.439 s | 1.350 s | 0.251 s |
| Kāra (`karac build`) | 1.172 to 1.558 s | 1.376 s | 4.863 s |
| Rust (`rustc -O`) | 2.555 to 3.256 s | 2.764 s | 0.791 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.621 to 3.093 s | 2.764 s | 0.783 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 2.677 to 3.033 s | 2.791 s | 0.808 s |
| Python | 6.559 s | | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is level with C and about 2x faster than Rust, each of which
starts 60 OS threads for every one of the 500 runs. Kāra's tasks run on
a pool of workers, so a hand-off from one method to the next is a switch
within the pool, where a hand-off between C's or Rust's OS threads goes
through the kernel; little of their wall time is user time. Go's
goroutines hand off within its own scheduler too, and Go takes about a
twentieth of Kāra's time. Kāra's user time is about 3.5x its wall time:
its workers stay busy between hand-offs. An idle program's workers do
sleep (a task waiting two seconds on a channel used 0.05 s of CPU), so
this is presumably a short spin before a worker parks; it was not traced
further. Python takes about 5x Kāra's time.
