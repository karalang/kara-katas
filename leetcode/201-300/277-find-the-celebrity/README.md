# 277. Find the Celebrity

`n` people. A **celebrity** is known by everyone else and knows nobody. There is
at most one. The only thing you may ask is `knows(a, b)`. Return the celebrity's
index, or `-1` — in as few questions as possible.

```
knows = [[0,1,0],      ->  1     person 1 knows nobody, 0 and 2 know them
         [0,0,0],
         [0,1,0]]

knows = [[0,1,0],      -> -1     person 1 knows 2, so nobody qualifies
         [0,0,1],
         [0,1,0]]
```

## Approaches

| file | mechanism | questions |
|---|---|---|
| `find_celebrity.kara` ★ | linear elimination, then verify | ≤ 3(n−1) |
| `find_celebrity_stack.kara` | the same elimination on a stack | ≤ 3(n−1) |
| `find_celebrity_brute.kara` | ask the definition of everyone | O(n²) |
| `differential.kara` | every relation on n ≤ 4, plus planted larger ones | — |

## One question eliminates one person

That is the whole problem, and it is worth stating before any code:

```
knows(a, b) == true   ->  A is not the celebrity   (celebrities know nobody)
knows(a, b) == false  ->  B is not the celebrity   (everyone knows the celebrity)
```

Either answer removes exactly one candidate, never zero. So `n−1` questions
reduce `n` people to one survivor, and nothing can beat that — each call has two
outcomes and each outcome kills one person.

The ★ solver keeps a running `cand` and walks once. The stack solver puts
everyone on a stack and pops two at a time. **They ask the same `n−1`
questions**, because the bound is a property of the problem rather than of the
bookkeeping — which is why it's worth having both.

## The survivor is not yet an answer

This is the half that gets skipped. The scan proves *nobody except `cand` can be
the celebrity*. It does **not** prove `cand` is one — a graph where nobody
qualifies still leaves a survivor. So phase 2 asks, for every other `j`, whether
`cand` knows `j` (must be no) and whether `j` knows `cand` (must be yes).

That costs up to `2(n−1)` more, for **≤ 3(n−1)** total.

## The question count is a second oracle

A solver can be perfectly correct and still ask O(n²) questions — which is
exactly what the problem forbids, and no amount of answer-checking would notice.
So the harness checks the count on every case, not just the answer. The brute
force is in there partly as the definition and partly as the demonstration: it
agrees on every answer and blows the bound constantly.

```
cases 4765
of which EVERY relation on n<=4 4165
cases that actually contain a celebrity 571
worst question count: scan 24, stack 24 (bound at n=9 is 24)
brute force exceeded the bound by up to 15 questions
bound violations by the elimination solvers 0
digest 77630549
the two elimination solvers disagreeing with EACH OTHER 0
either of them disagreeing with the DEFINITION 0
```

Both solvers reach exactly 24 at n=9 and neither exceeds it — the bound is
tight, not slack.

## Two things the generator has to get right

**Enumerate every relation, not a sample.** A knows-matrix has `n²−n`
off-diagonal entries, so there are `2^(n²−n)` of them — 4096 at n=4 — and the
harness walks all of them as a bitmask. This is the strongest arm, because the
space is dominated by the case that breaks survivor-based solvers: only **571 of
4765** cases contain a celebrity at all. A solver that returns its survivor
without verifying is right on the rare positive cases and wrong on almost
everything else.

**And plant one at larger n.** In a uniform random matrix the chance that a given
person is a celebrity is `2^-(2n-2)` — under one in sixty thousand by n=9. Sample
randomly and the positive path essentially never runs. So half the larger cases
get a celebrity planted at a rotating index. Testing only uniform matrices would
look thorough and cover half the problem.

## What the injected bugs did

| injection | scan vs stack | vs the definition |
|---|---:|---:|
| scan: skip phase 2 entirely | 4194 | 4194 |
| scan: phase 2 checks only `knows(cand, j)` | 1045 | 1045 |
| scan: elimination keeps the wrong survivor | 570 | 570 |
| stack: push back the eliminated one | 570 | 570 |
| **brute force: a celebrity may know one person** | **0** | **1585** |
| **both elimination solvers skip verification** | **3674** | **4194** |

The last two rows are why all three exist.

Breaking the **oracle** is invisible between the elimination solvers — they agree
with each other perfectly, 0 disagreements — and shows up only against them.

Breaking **both** elimination solvers the same way is caught between them 3674
times, which is more than it looks like it should be: the scan and the stack pick
*different* survivors, so two identically-broken solvers still mostly disagree.
But `4194 − 3674 = 520` cases have them agreeing with each other and both wrong.
Those 520 are visible only to the definition.

## A compiler bug this kata found

`B-2026-08-16-1` — **auto-par forks two independent `let`s and then codegen
cannot see their bindings.** Two locals initialized from calls returning a heap
collection, gathered into a collection literal, fail the *default* build:

```
let a: Vec[i64] = mk(1i64);
let b: Vec[i64] = mk(2i64);
let c: Vec[Vec[i64]] = [a, b];     // error: codegen failed: Undefined variable 'a'
```

The grouping is correct — the calls really are independent, and
`--concurrency-report` says so. The bindings just aren't visible to the
continuation that consumes them. It needs all three of: two or more bindings from
*calls* (one is never forked), the calls returning a *heap collection* (scalars
compile fine), and consumption as *elements of a collection literal* (`push`,
tuples and `.len()` arithmetic all work).

**Three of this kata's four programs currently fail two of their four surfaces**
because of it — they build their case tables exactly that way. Filed **high**:
it is on the default path for an ordinary construct, and both workarounds require
already knowing the bug exists.

| | `--interp` | JIT | `build` | `AUTO_PAR=0 build` |
|---|---|---|---|---|
| `find_celebrity.kara` | ✅ | ❌ | ❌ | ✅ |
| `find_celebrity_stack.kara` | ✅ | ❌ | ❌ | ✅ |
| `find_celebrity_brute.kara` | ✅ | ❌ | ❌ | ✅ |
| `differential.kara` | ✅ | ✅ | ✅ | ✅ |

The solvers are **left in their natural form**. Rewriting the case table as five
`push` calls would hide the bug, which is the one thing a kata must not do. The
differential builds its matrices from a bitmask rather than a literal table, so
it never hits the shape and the kata's actual verification is unaffected.

## Kāra features exercised

- **`mut ref i64`** threaded through a helper as the question counter — the
  same accumulator idiom as [#250](../250-count-univalue-subtrees/).
- **`Vec[Vec[bool]]`** as an adjacency matrix, indexed twice.
- **`Option[i64]` from `Vec.pop()`**, unwrapped under a `len() > 1` guard that
  makes `None` unreachable — stated rather than hidden behind a dead `match` arm.
- **Nested collection literals** — which is where the compiler bug lives.

## Running

```bash
karac run --interp find_celebrity.kara
karac run --interp find_celebrity_stack.kara
karac run --interp find_celebrity_brute.kara

# 4765 cases, 4165 of them every relation on n <= 4
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

# the solvers need auto-par off until B-2026-08-16-1 is fixed
for f in find_celebrity find_celebrity_stack find_celebrity_brute; do
    KARAC_AUTO_PAR=0 karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```
