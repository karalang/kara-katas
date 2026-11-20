# 1279. Traffic Light Controlled Intersection

There is an intersection of two roads. First road is road A where cars
travel from North to South in direction 1 and from South to North in
direction 2. Second road is road B where cars travel from West to East in
direction 3 and from East to West in direction 4.

There is a traffic light located on each road before the intersection. A
traffic light can either be green or red.

- **Green** means cars can cross the intersection in both directions of
  the road.
- **Red** means cars in both directions cannot cross the intersection and
  must wait until the light turns green.

The traffic lights cannot be green on both roads at the same time. That
means when the light is green on road A, it is red on road B and when the
light is green on road B, it is red on road A.

Initially, the traffic light is green on road A and red on road B. When
the light is green on one road, all cars can cross the intersection in
both directions until the light becomes green on the other road. No two
cars traveling on different roads should cross at the same time.

Design a deadlock-free traffic light controlled system at this
intersection.

Implement the function `void carArrived(carId, roadId, direction,
turnGreen, crossCar)` where:

- `carId` is the id of the car that arrived.
- `roadId` is the id of the road that the car travels on.
- `direction` is the direction of the car.
- `turnGreen` is a function you can call to turn the traffic light to
  green on the current road.
- `crossCar` is a function you can call to let the current car cross the
  intersection.

Your answer is considered correct if it avoids cars deadlock in the
intersection. Turning the light green on a road when it was already green
is considered a wrong answer.

```
cars = [1,3,5,2,4], directions = [2,1,2,4,3], arrivalTimes = [10,20,30,40,50]
  ->  ["Car 1 Has Passed Road A In Direction 2",
       "Car 3 Has Passed Road A In Direction 1",
       "Car 5 Has Passed Road A In Direction 2",
       "Traffic Light On Road B Is Green",
       "Car 2 Has Passed Road B In Direction 4",
       "Car 4 Has Passed Road B In Direction 3"]
cars = [1,2,3,4,5], directions = [2,4,3,3,1], arrivalTimes = [10,20,30,40,40]
  ->  ["Car 1 Has Passed Road A In Direction 2",
       "Traffic Light On Road B Is Green",
       "Car 2 Has Passed Road B In Direction 4",
       "Car 3 Has Passed Road B In Direction 3",
       "Traffic Light On Road A Is Green",
       "Car 5 Has Passed Road A In Direction 1",
       "Traffic Light On Road B Is Green",
       "Car 4 Has Passed Road B In Direction 3"]
```

In the second, car 4 crossing before the light turns green on road A for
car 5 is also accepted.

**Constraints:** `1 <= cars.length <= 20`; `cars.length =
directions.length`; `cars.length = arrivalTimes.length`; all values of
`cars` are unique; `1 <= directions[i] <= 4`; `arrivalTimes` is
non-decreasing.

The arms are a `sync struct TrafficLight` with `fn new()` and `fn
car_arrived(self, car_id: i64, road_id: i64, direction: i64, turn_green:
Fn(), cross_car: Fn())`, road A being 1 and road B 2. LeetCode's threads
are a `TaskGroup` with a task for each car, started in order of arrival,
cars arriving together in a random order; the arrival times order the
tasks' starts and are not waited out. Each callback logs what happens
behind a `Mutex`: the light turning green on a road, and a car entering
the intersection and leaving it, with a yield between, so cars interleave
on the MIR interpreter, which switches tasks only when one waits or
yields. Since a run may cross the cars in any valid order, every harness
judges the log rather than printing it. LeetCode has no Rust signature for
its concurrency problems, so there is no solution arm.

## Approaches

| file | mechanism |
|---|---|
| `traffic_light.kara` ★ | the road whose light is green in a `Mutex`, held while a car turns its light green if it must and crosses: one car is inside at a time |
| `traffic_light_switch.kara` | a light switch, cars on the green road crossing together: the first car of a road to come in takes the intersection, a `Semaphore` of one permit, and turns its light green if it is red, and the last of that road to leave gives it back; each road's count of cars inside in its own `Mutex`, held by the first car until the light is right |
| `traffic_light_channel.kara` | a token: a `channel(1)` holding the road whose light is green while no car is inside; a car receives it, turns its light if the token names the other road, crosses, and sends its road back |
| `traffic_light_spin.kara` | spinning, with no lock: an `Atomic[bool]` marks the intersection busy, taken by `compare_exchange(false, true)` with a yield between tries, and the green road an `Atomic[i64]` changed by `swap` |
| `traffic_light_queue.kara` | a queue of turns: a car takes a ticket from an `Atomic` counter and waits, yielding, until the ticket being served is its own, kept with the green road in a `Mutex[(i64, i64)]`; cars cross in the order they took tickets |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples judged (`5 and
5 cars crossed, valid true true`); 1000 random problems of 1 to 20 cars on
random roads arriving at times 0 to 9 (`1000 random problems: 10514 cars
crossed, 1000 valid`); and the constraints' top, 20 cars arriving together
all on road A, all on road B and on both (`valid true true true`). The
judge is the statement read literally: the light starts green on road A
and turns green only on a road where it is red, a car enters only on its
road's green and never while a car of the other road is inside, and every
car enters once and leaves once. A deadlock would end the run with the
runtime's deadlock report, and none did. `traffic_light.py` mirrors the ★
arm with a thread for each car and a `threading.Lock`, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac build`, five runs in five of each compiled binary,
and under the AddressSanitizer build.

The Mend loop: all five arms checked clean as first written. No gap was
met.

## Differential

`differential.kara` holds copies of the five arms, each with the harness's
run, and the judge. It draws 300 problems of 1 to 20 cars on random roads
and runs each arm on each three times: in arrival order, in reverse, and
with every car moved to the other road.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | two crossing events for each car, and no more light changes than cars |
| P3 | every light change followed by a car of that road entering before the next change |
| P4 | at most two light changes for each car on road B |
| P5 | the tasks started in reverse, the statement read literally |
| P6 | every car moved to the other road, the statement read literally |

All 9,000 checks pass on every arm: `300 problems: 16655 crossings, 9000
checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac run`,
`karac build` and the AddressSanitizer build.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`. The interpreter runs one task at a time and
switches at a wait or a yield, so its counts are the same on every run;
compiled, the tasks run on every core, and a run's counts move by a few
from one run to the next.

| # | mutation | failures by property, `__mir-run` | `karac run` |
|---|---|---|---|
| S1 | ★: the light never recorded as changed | P1 270, P5 276, P6 279 | P1 267, P5 272, P6 275 |
| S2 | ★: the lock let go before the car crosses | P1 272, P5 272, P6 272 | P1 272, P3 32, P5 272, P6 268 |
| W1 | switch: the light never recorded as changed | P1 134, P5 141, P6 138 | P1 143, P5 146, P6 143 |
| W2 | switch: road A's cars never taking the intersection | P1 272, P5 272, P6 272 | P1 263, P5 264, P6 267 |
| C1 | channel: the token sent back with the road it came with | P1 270, P5 276, P6 279 | P1 269, P5 272, P6 281 |
| C2 | channel: the light never turned | P1 287, P5 287, P6 285 | P1 287, P5 287, P6 285 |
| T1 | spin: the light never recorded as changed | P1 270, P5 276, P6 279 | P1 270, P5 275, P6 279 |
| T2 | spin: the intersection marked free before the car crosses | P1 272, P5 272, P6 272 | P1 269, P3 76, P5 268, P6 265 |
| Q1 | queue: the light never recorded as changed | P1 270, P5 276, P6 279 | P1 270, P5 276, P6 279 |
| Q2 | queue: the light compared with the car's direction, not its road | P1 281, P4 35, P5 281, P6 284 | P1 281, P4 35, P5 281, P6 284 |

All ten are caught, every one by P1, the statement read literally, and by
P5 and P6, the same judge on the reversed start and on the swapped roads.
The four that never record the light's change (S1, W1, T1, Q1) and the
channel's stale token (C1) turn a light green that already is, and C2,
which never turns it, lets a car cross on red. The three that let cars of
both roads inside together (S2 and T2, crossing outside the lock, and W2,
road A never taking the intersection) need two cars inside at once, which
the yield inside a crossing gives on the interpreter and the cores give
compiled; compiled, S2 and T2 also leave a light change with no car of
its road following it before the next (P3). Q2, the light compared with a
direction, turns the light more often than there are cars on road B to
need it (P4). P2, the event counts, catches none: every edit still
crosses each car once.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (the green road behind a `Mutex`, held while a car turns its light
and crosses) over 2000 runs of 20 cars, a task for each car, on random
roads and started in a random order; each run's log judged by the
statement read literally. Every program prints `2000 runs of 20 cars:
40000 cars crossed, 2000 valid`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.568 to 0.618 s | 0.591 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.555 to 0.632 s | 0.600 s |
| Rust (`rustc -O`) | 1.086 to 1.400 s | 1.194 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.148 to 1.345 s | 1.245 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 1.088 to 1.331 s | 1.200 s |
| C (`clang -O3`) | 1.218 to 1.353 s | 1.267 s |
| C (`clang -O3 -march=x86-64-v3`) | 1.174 to 1.296 s | 1.261 s |
| Go | 0.024 to 0.039 s | 0.031 s |
| Python | 4.506 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on takes about 2.1x Kāra's time. C
takes about 2.1x Kāra's time; Kāra takes about 19.4x Go's time (0.600 s
against 0.031 s). Python takes about 8x Kāra's time. No profile was
taken.
