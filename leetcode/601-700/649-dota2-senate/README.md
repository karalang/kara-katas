# 649. Dota2 Senate

The senate of Dota2 has senators of two parties, Radiant and Dire, given
as a string of `R` and `D` in the order they vote. Round after round,
each senator still voting either bans one other senator from voting for
the rest of the game or, if every senator still voting is of its own
party, announces victory. Every senator plays as well as it can for its
party. Return the party that wins, `"Radiant"` or `"Dire"`.

```
senate = "RD"   ->  "Radiant"    R bans D, then announces victory
senate = "RDD"  ->  "Dire"       R bans the first D, the second D bans R
```

**Constraints:** 1 to 10,000 senators.

## Approaches

Every arm is `fn predict_party_victory(senate: String) -> String`. Each
plays the strategy every solution rests on: ban the opponent due to vote
soonest, counting on into the next round.

| file | mechanism |
|---|---|
| `dota2_senate.kara` ★ | a `VecDeque` of each party's senators by when they vote; the front two meet, the earlier bans the later and goes to the back `n` places later; O(n) |
| `dota2_senate_bans.kara` | one queue of all the senators and a count of the bans each party owes; a senator whose party owes one is struck out, anyone else adds a ban to the other party's count and goes to the back; O(n) |
| `dota2_senate_rounds.kara` | rounds over the seats, each senator still voting banning the next opponent still voting from its seat on, around to the start; O(n^2) |
| `dota2_senate_rebuild.kara` | the senate rewritten each round as a new `String`, with the bans owed carried from round to round; O(n) per round |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 14 lines: the two LeetCode examples; eight
more (one senator of each party; the second party to vote outnumbering
the first; the first outnumbered three to two but winning, either way
round; outnumbered four to two and losing; parties by turns; and a long
mixed senate), each with its answer; the Radiant wins and a checksum of
the winners of 300 random senates of 1 to 30, each senator Radiant with
a chance from 0 to 100 percent; and three senates of the problem's
largest size, 10,000, at chances of 50, 45 and 55 percent.
`dota2_senate.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which assumes no strategy: the whole game searched, each senator in turn
trying every senator it could ban, of either party, and a party winning
from a position when any of its senator's moves wins, remembered in a
`Map` by who is still voting and whose turn it is. Each of 1,000 cases
has 1 to 9 senators, each Radiant with a chance from 0 to 100 percent.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the parties swapped swap the winner |
| P3 | one more of the winners, voting last, still wins |
| P4 | one more of the winners, voting first, still wins |
| P5 | the losers' last senator taken away, the same party wins |

P3 to P5 are not in the problem. A Python search of every senate of up
to 10 senators, playing the whole game as the definition does, found
none that breaks them, and none where the strategy loses a game that
could be won.

It prints `1000 cases (4930 senators), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the voter sent back without its place in the next round | P1 96, P2 175 |
| M2 | ★: the later of the two senators banning | P1 470, P3 25, P4 236, P5 29 |
| M3 | bans: each Radiant banning two | P1 53, P2 89 |
| M4 | bans: a single ban owed to the Radiant ignored | P1 63, P2 126 |
| M5 | rounds: a senator banning its own party | P1 456, P3 194, P4 82, P5 135 |
| M6 | rounds: the search for an opponent from the first seat | P1 118 |
| M7 | rebuild: the bans owed forgotten each round | P1 118 |
| M8 | rebuild: one Radiant left out paying off every ban owed | P1 17, P2 37 |
| E1 | ★: a tie going to the Radiant | 0 |
| E2 | bans: the Radiant winning when no Dire is left | 0 |
| E3 | rounds: the winner read at the end of the search | 0 |
| E4 | rebuild: a Radiant copied setting the count to 1 | 0 |

P1 kills all eight. P2 sees exactly the four mutants that treat the
parties differently, M1, M3, M4 and M8, each changing only the Radiant's
side; the other four are symmetric, so swapping the parties swaps their
wrong answers too. P3, P4 and P5 see only M2 and M5, the two that change
who is banned, the later senator banning or a senator banning its own
party: neither is best play, so one more winner or one fewer loser no
longer decides the game the way it should. M6 and M7 ban a different
opponent or drop the bans owed at the end of a round, and only P1 sees
them. The four survivors cannot change an answer: no two senators share
a place in the voting order, so `r` and `d` are never equal; the loop
ends when one party has no senator left, so the other has one; the
search ends on the senator searching only when there is no opponent; and
only whether any Radiant was copied matters, not how many.

## Verification

Every arm prints the same output as `dota2_senate.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` for the debug build and `803e7dac6a` for the release build
that runs `check` and `__mir-run`, with runtime archives newer than the
last `runtime/src` change.

The frozen legacy backends refuse every arm and the differential at type
checking: the harness hands `seed`, already a `mut ref` parameter, on
with the `mut` marker design.md asks for, which legacy rejects, and the
bans and rebuild arms read `*b` from `bytes().iter()`, which legacy
types by value. Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 senates of
100,000 senators once, each senator Radiant with a chance from 45 to
55 percent, the chance picked for each senate; then 500 rounds each
predict one senate, picked by the round, counting the Radiant wins and
putting each winner into a checksum. Every implementation prints
`20 senates, 500 rounds: Radiant wins 250, checksum 266594483`, the Kāra
program under `karac __mir-run` included (in 105 s).

Each implementation keeps a queue of indices for each party: Kāra and
Rust a `VecDeque`, C a ring buffer it grows by doubling, Go a slice it
takes from the front and appends to, and Python a `deque`. Spot timings
on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine), each including making the
senates (six runs for the two Kāra builds):

| | time |
|---|---|
| C (`clang -O3`) | 0.78 to 0.80 s |
| Rust (`rustc -O`) | 0.61 to 0.72 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.63 to 0.83 s |
| Go | 1.47 to 1.65 s |
| Python | 5.16 to 5.26 s |
| Kāra (`karac build --mir`) | 1.18 to 1.45 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program: its parameters are still owned rather than borrowed, so handing
`senates[(r * 7) % inputs]` to `predict_party_victory` moves an element
out of a `Vec`. That edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside the kata whose parameter
is `ref String` builds under legacy and takes 0.39 to 0.52 s over six
runs. Under `karac __mir-llvm-run` the program prints the same line in
6.9 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So the v2 build takes about three times as long as legacy, past the
M2 bar of 1.5 times, and twice Rust's time with the same `VecDeque`. The
deque is the cost, and it is open row B-2026-10-13-36: on the v2 backend
`push_back` and `pop_front` are out-of-line runtime calls that wrap with
an integer `%` and copy each element with a `memcpy` call. A program of
nothing but 50 million `pop_front` and `push_back` pairs on a deque of
1,000 `i64` takes 0.53 s built with `--mir` and 0.07 s under legacy
`karac build`. The comparison with C and Rust waits until after M4.

## Compiler findings

None new. The bench's gap to legacy is open row B-2026-10-13-36, filed
from kata 542, and the deque probe above is one more measurement of it.
All four arms, the differential and the bench program pass `karac check`
and run the same on both v2 backends. The legacy refusals above are not
filed because legacy is frozen.
