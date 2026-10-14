# 582. Kill Process

You have `n` processes forming a rooted tree structure. You are given
two integer arrays `pid` and `ppid`, where `pid[i]` is the ID of the
`i`-th process and `ppid[i]` is the ID of the `i`-th process's parent
process. Each process has only one parent process but may have multiple
children processes. Only one process has `ppid[i] = 0`, which means this
process has no parent process (the root of the tree). When a process is
killed, all of its children processes will also be killed. Given an
integer `kill` representing the ID of a process you want to kill, return
a list of the IDs of the processes that will be killed. You may return
the answer in any order.

```
pid = [1,3,10,5], ppid = [3,0,5,3], kill = 5  ->  [5,10]
pid = [1], ppid = [0], kill = 1                ->  [1]
```

**Constraints:** `n == pid.length == ppid.length`; `1 <= n <= 5 *
10^4`; `1 <= pid[i] <= 5 * 10^4`; `0 <= ppid[i] <= 5 * 10^4`; only one
process has no parent; all the values of `pid` are unique; `kill` is
guaranteed to be in `pid`.

## Approaches

Every arm is `fn kill_process(pid: Vec[i64], ppid: Vec[i64], kill:
i64) -> Vec[i64]`. The answer may come in any order, so the harness
sorts it before printing.

| file | mechanism |
|---|---|
| `kill_process.kara` ★ | a `Map[i64, Vec[i64]]` from each parent to its children, built with `entry(..).or_insert(..)`, and a `VecDeque` walked breadth first from `kill`; O(n) |
| `kill_process_dfs.kara` | the same map built with `get_mut`, walked by recursion; O(n) |
| `kill_process_sweep.kara` | no index of children: a `Set` of the dead starts with `kill`, and sweeps over the list kill every process whose parent is dead until a sweep kills nothing new; O(n * sweeps) |
| `kill_process_climb.kara` | a `Map` from each process to its parent, and each process climbing from itself towards the root until it meets `kill` or runs out; O(n * depth) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 11 lines: six lists at the edges (the two
examples, the first killed at the root and at a leaf, a chain killed in
the middle, and parents listed after their children), a count and
checksum over 300 random trees of 1 to 30 processes with one killed at
random, and the problem's largest, 50,000 processes: a random tree
killed at the root and at a process partway down, one root with
49,999 children, and a chain of 5,000 killed in the middle. The chain is
kept to 5,000 because the climb arm's cost grows with the depth.
`kill_process.py` mirrors the ★ arm and its output is byte-identical.

The dfs arm does not build today; see Compiler findings. It is kept as
written. A copy outside this directory that adds to a list already in
the map through `children[ppid[i]].push(pid[i])`, after `contains_key`,
in place of `get_mut`, the only change, prints the same output.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: a process dies when it is `kill` or when
its parent dies, its parent found by searching the list and the same
question asked of it. Each arm's answer, sorted, is held to the
properties below on 1,000 random trees of 1 to 10 processes named from
1 to 20, the list shuffled so that parents can come after their
children.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | it holds `kill`, no process twice, and only processes in the list |
| P3 | the list turned round gives the same answer |
| P4 | every process renamed to 100 more gives the answer renamed |
| P5 | the answer is `kill` together with what killing each of its children gives |

Since the dfs arm does not build, the differential does not either:
`karac check` and the MIR backends stop at its copy of that arm. The
copy outside this directory with the workaround in that place prints
`1000 cases, 4 arms, 20000 checks, 0 failures` under `karac __mir-run`
and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the workaround copy of the differential, two to each arm
that change its answers and one to each that does not, each run under
`karac __mir-llvm-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `kill` queued twice | P1 1000, P2 1000, P5 1000 |
| M2 | ★: `kill` itself left out | P1 1000, P2 1000, P5 1000 |
| M3 | dfs: each parent's first child dropped | P1 488, P3 191, P5 488 |
| M4 | dfs: the children killed but not walked | P1 235, P5 235 |
| M5 | sweep: one sweep only | P1 163, P3 235, P5 139 |
| M6 | sweep: `kill` itself left out | P1 1000, P2 1000, P5 1000 |
| M7 | climb: the climb not stopped at `kill` | P1 1000, P2 1000, P5 1000 |
| M8 | climb: one step climbed at most | P1 235, P5 235 |
| E1 | ★: the queue taken from the back | 0 |
| E2 | dfs: each child put first in its list | 0 |
| E3 | sweep: the two tests the other way round | 0 |
| E4 | climb: the root found by its missing parent | 0 |

M4 and M8 give the same wrong answer, `kill` and its children only, so
both fail on the same 235 trees, those where `kill` has a grandchild.
P3 sees only the mutants whose answer depends on the order of the list:
M3 drops whichever child comes first, and M5's one sweep reaches as many
generations as the list's order happens to allow. P4 sees none, since no
arm or mutant reads anything into the names themselves. E1 and E2 change
only the order of the answer, which the harness sorts, and E4 is safe
because the root's parent, 0, is the one value with no entry in the map.

## Verification

The ★, sweep and climb arms print the same output as `kill_process.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. `karac check` passes on those three and the bench program; it
refuses the dfs arm and the differential, and so do both MIR backends
(B-2026-10-12-3). The workaround copy of the dfs arm prints the same
output under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

The frozen legacy backends refuse every arm, the differential and the
bench program under `karac run --interp`, `karac run` and `karac build`,
at type checking: each reads an element of `iter()` as `*k` or `*p`, and
legacy gives the element as an `i64` where v2 gives a reference ("unary
'*' requires 'ref T' ... found 'i64'"). The dfs arm also stops at
`get_mut`, as on every backend. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 random trees once, each of
50,000 processes (the problem's most) numbered 1 to 50,000 in a shuffled
order, each one's parent an earlier one; then 30 times over every tree
is asked to kill one of its processes, the root every fourth time. Every
implementation prints `20 trees of 50000 processes, 30 rounds:
7553605 killed, checksum 347966231`, the Kāra program under `karac
__mir-run` included (93 s).

Each call builds a fresh hash map from parent to children, as the Kāra
arm builds a fresh `Map`: a `HashMap<i64, Vec<i64>>` with the default
hasher and a `VecDeque` in Rust, a map of slices with no size hint and a
slice for the queue in Go, and a `dict` of lists and a `deque` in
Python. C has no hash map, so each call `calloc`s an open-addressing
table of 131,072 slots, each holding a growable array of children,
hashes by a 64-bit multiply and frees it all. Spot timings on a shared
4-core container, three runs each (two for Python; `bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.86 to 1.92 s |
| Rust (`rustc -O`) | 2.00 to 2.31 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.21 to 2.34 s |
| Go | 3.11 to 3.32 s |
| Python | 13.8 to 14.1 s |
| Kāra (`karac build --mir`) | 3.15 to 3.30 s |

The legacy `karac build` refuses this program on the same `*k`. So
`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`f6052c659c`. Under `karac __mir-llvm-run` the program prints the same
line in 19.9 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

The Kāra row is about 1.5 times Rust's and level with Go's. Where the
gap to Rust comes from is not measured.

## Compiler findings

None new. The dfs arm meets kara B-2026-10-12-3 (open): `Map.get_mut`,
which docs/library/collections.md lists as `fn get_mut(mut ref self,
key: K) -> Option[mut ref V]`, does not exist, so `if let Some(kids) =
children.get_mut(ppid[i]) { kids.push(pid[i]); }` is refused by `karac
check` and both MIR backends with "no method 'get_mut' on type 'Map'".
The arm keeps the spec's spelling. The legacy failures above are not
filed because legacy is frozen.
