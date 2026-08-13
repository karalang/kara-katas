# 263. Ugly Number

An **ugly number** is a positive integer whose prime factors are all drawn from
`{2, 3, 5}`. Return whether `n` is ugly.

```
1   ->  true     the empty product
6   ->  true     2 * 3
8   ->  true     2^3
14  ->  false    2 * 7 — the 7 survives
0   ->  false    and this one is where the problem bites
```

**Constraints:** `-2³¹ ≤ n ≤ 2³¹ − 1`.

## Approaches

| file | mechanism | direction |
|---|---|---|
| `ugly_number.kara` ★ | divide out every 2, then 3, then 5; residue must be 1 | destructive, by named primes |
| `ugly_number_gcd.kara` | divide out `gcd(m, 30)` until it reaches 1 | destructive, by their product |
| `ugly_number_enum.kara` | generate the ugly numbers in order and look for `n` | constructive |
| `differential.kara` | exhaustive over a band + 600 scattered probes | — |

## The mechanism

Strip every allowed prime and ask what is left. If the residue is `1` the number
was built entirely from `{2, 3, 5}`; anything else means some other prime
survived. Order does not matter — division is commutative over the
factorisation — and `n = 1` is ugly as the empty product.

That is four lines. The problem is what happens at zero.

## The zero hang

`n ≤ 0` has to be rejected **before** the loop, and not as a definitional
nicety about positivity:

```
0 % 2 == 0    and    0 / 2 == 0
```

so a divide-out loop entered with `n = 0` divides forever. It is not a wrong
answer, it is a **hang** — and the arithmetic is not wrong either, which is why
nothing traps and nothing rescues it.

The striking part is that the trap is not a property of one implementation. The
gcd form shares none of the trial-division form's arithmetic, and fails
identically:

```
gcd(0, 30) == 30    and    0 / 30 == 0
```

Both loops are perfectly correct on every input the guard admits. Both spin
forever on the one input it excludes. The trap is in the problem, not in either
way of writing it.

Negative inputs are a much milder case: they terminate on their own
(`-6 → -3 → -1`, residue `-1 ≠ 1`) and answer false, which is also the right
answer. Only zero hangs.

**This failure mode is demonstrated, not asserted** — but it cannot be
demonstrated the way the others are. A decider that hangs produces no mismatch
to count; it produces no output at all. So it is measured with the one
instrument that fits:

| guard removed from | `is_ugly(0)`, interpreted | compiled |
|---|---|---|
| trial division | no output, killed at 10 s | no output, killed at 10 s |
| gcd peeling | no output, killed at 10 s | no output, killed at 10 s |

## Why three, and why the third goes the other way

The first two both **tear `n` down**. They differ in how they name the primes —
individually, or through their product 30, where `gcd(m, 30)` is exactly "one
copy of each of 2, 3, 5 that `m` still has" — but a mistake in the *idea* (strip
the factors, check the residue) would be shared by both. As the injected-bug
table below shows, that is not hypothetical: forgetting the 5s in either form
misclassifies precisely the same inputs.

The third **builds up** instead. Every ugly number after 1 is 2, 3 or 5 times an
earlier one, so keep a cursor per multiplier into the generated list, take the
smallest candidate, and advance every cursor that produced it — the merge from
[#264](../264-ugly-number-ii/). Stop when the sequence reaches or passes `n`.

This looks expensive and is not. The count of ugly numbers below `N` grows like
`(ln N)³`, so there are only ~1,350 below 2³¹ and ~11,000 below 2⁶³ — a few
thousand steps for *any* `i64` input.

**Overflow is its real hazard, not cost.** A candidate `u[i] * 5` can exceed
`i64` even when `u[i]` is a perfectly good ugly number below `n`. Kāra traps on
signed overflow rather than wrapping, so an unguarded enumerator does not return
a wrong answer — it aborts. The guard costs one comparison:

```kara
if u[i2] <= n / 2i64 { has2 = true; c2 = u[i2] * 2i64; }
```

With floor division, `u[i] <= n / k` holds exactly when `u[i] * k <= n`, so the
candidate is formed only when it fits — and candidates beyond `n` were never
needed anyway, since the search stops at `n`. The guard is free in every sense.

## Generator design

Ugliness is a property of a single integer, not of a structure, so the small
band does not need sampling — it can simply be **checked in full**:

| family | inputs | purpose |
|---|---|---|
| A | every `n` from −100 to 20,000 | settles that range outright |
| B | constructed `2^a·3^b·5^c` near the `i64` ceiling | large trues; exercises the overflow guard |
| C | ★ ugly × one other prime (7, 11, 13, 17, 9973) | the near-misses |
| D | uniform random | false for varied reasons |

**Family C is the one that separates.** A decider that strips 2s, 3s and 5s and
then forgets to ask what is left accepts every one of them; so does one that
checks only "divisible by 2, 3 or 5". Family B alone would catch neither,
because everything in it is genuinely ugly.

Family A runs the constructive generator **in its natural mode** — once over the
band, marking what it produces — rather than re-running it per value. Same
algorithm and same output, applied the way a constructive oracle is meant to be
applied to a contiguous range, and it is what keeps the exhaustive band
affordable under the interpreter. Families B/C/D cannot use a table (their values
are scattered across the whole `i64` range), so the per-value form checks those.

Over the run: **20,701 inputs checked**, 413 ugly, **212 of them in
[−100, 20000]** — a count independently confirmed by a triple loop over the
exponents `2^a·3^b·5^c ≤ 20000`, a fourth method sharing nothing with any of the
three deciders.

**Three failure modes measured, one demonstrated:**

| injected bug | mismatches / 20,701 |
|---|---|
| trial division never strips 5s | **304** |
| `gcd(m, 6)` instead of `gcd(m, 30)` | **304** |
| overflow guard `<` instead of `<=` | **188** |
| `n ≤ 0` guard removed | *no mismatch — it hangs* (above) |

The first two numbers are equal because they are the same mistake reached by two
routes: "forget the 5s" misclassifies exactly one set of inputs, and it does not
matter whether the 5 goes missing from a loop or from a constant. The third is a
different shape entirely — an off-by-one in the overflow guard drops candidates
where `u[i] * k == n` exactly, so it answers *false* for ugly numbers that are
precisely `k` times an earlier one.

## Kāra features exercised

- **`i64.MAX`** as a value, and `v <= limit / f` as the overflow-safe way to ask
  whether a product will fit.
- **Trapping signed arithmetic** — the reason the enumerator's guard is a
  correctness requirement and not a micro-optimisation.
- **`while true` with `return` from the body**, for a loop whose exit condition
  is discovered rather than tested.
- **`Vec[bool]` as a marked table**, alongside `Vec[i64]` as the generated
  sequence.
- **Euclid's algorithm** on `i64` with `%`.

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`; the ★ solver
and the differential match their Python mirrors.

No compiler bugs found. The zero hang is a property of the algorithm, not of
`karac` — the arithmetic it performs is correct at every step.

## Running

```bash
karac run ugly_number.kara
karac run ugly_number_gcd.kara
karac run ugly_number_enum.kara

diff <(karac run ugly_number.kara) <(python3 ugly_number.py) && echo OK
diff <(karac run ugly_number.kara) <(karac run ugly_number_gcd.kara) && echo OK
diff <(karac run ugly_number.kara) <(karac run ugly_number_enum.kara) && echo OK

# exhaustive band + 600 scattered probes, three deciders cross-checked
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in ugly_number ugly_number_gcd ugly_number_enum differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```
