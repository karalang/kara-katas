# 273. Integer to English Words

Convert a non-negative integer to its English words spelling.

```
0           -> Zero
123         -> One Hundred Twenty Three
1000010     -> One Million Ten
12345       -> Twelve Thousand Three Hundred Forty Five
2147483647  -> Two Billion One Hundred Forty Seven Million
               Four Hundred Eighty Three Thousand Six Hundred Forty Seven
```

**Constraints:** `0 ≤ num ≤ 2³¹ − 1`.

## Approaches

| file | mechanism | cost |
|---|---|---|
| `int_to_words.kara` ★ | split into three-digit groups, name each, tag with a scale | O(digits) |
| `int_to_words_places.kara` | walk the decimal digits, decide each from its position | O(digits) |
| `int_to_words_table.kara` | precompute all 1,000 groups bottom-up, then look up | O(1) after O(1000) |
| `differential.kara` | 50,032 probes, three solvers plus a shape oracle | — |
| `bench/spell.kara` | the ★ chunker as a benchmark kernel — seq and par lanes | — |

## English numerals are periodic with period 1000

Every group of three digits is spelled by the same rules and then labelled
Thousand / Million / Billion, so the whole problem is one function over `1..999`
plus a loop. The ★ solver peels `n % 1000` off the right; the recursion inside a
group is only two levels deep.

Three things go wrong, and none of them are the arithmetic.

**A zero group emits nothing.** `1000000` is "One Million", not "One Million Zero
Thousand Zero" — but `0` itself is "Zero". The empty string is the natural return
for a zero group, which forces the whole-number case to be special-cased *before*
the loop rather than inside it.

**Ten through nineteen are not compositional.** "Fifteen" is not "Ten Five", so
`10..19` needs its own table and the tens digit cannot be handled uniformly.

**The join is where the bugs actually live.** Every piece is separated by exactly
one space, none leading and none trailing, and each piece may itself be empty.

## Three joins, on purpose

Since all three solvers are doing the same joining job, they would happily share
a joining bug. So each does it differently:

| solver | join |
|---|---|
| ★ chunker | prepend — `out = piece + " " + out` |
| positional walk | collect into a `Vec[String]`, join once at the end |
| table | append with a leading-space guard |

## The positional walk is where the teens bite

That solver never splits the number at all: it renders `n` as decimal text and
decides each digit from its position — `p % 3` gives the place inside the group,
`p / 3` gives the scale. Every digit is a pure function of its own value and its
own index.

Except a `1` in the tens place, which **binds to the next digit**. So the loop is
not a per-digit map: it carries one lookahead, and consuming the units digit early
is also what ends the group, so the scale word has to be emitted from two places
in the loop rather than from the `place == 0` arm alone. That coupling is the
entire difficulty of writing it this way, and it is the rule a positional scheme
cannot express.

## The table solver reads its own table while writing it

`g[837] = g[8] + " Hundred " + g[37]` — the two-digit half of every three-digit
name is read back out of the table that is still being filled. It is the exact
inverse of the ★ solver's top-down recursion, and it makes the query O(1).

It also carries **a different transcription of the lexicon** — array literals
where the other two use an `if`-chain. That is what lets the harness catch a typo
in the twenty-eight words; the other two share theirs and could only agree on
"Fourty".

## A fourth check that computes nothing

Agreement between solvers cannot catch a mistake all three make — and all three
are joining words with spaces. So every produced string also goes through a
**shape oracle**: split on a single space, require that no token is empty and
every token is in the vocabulary. An empty token is *exactly* a leading space, a
trailing space or a doubled space, so one condition covers all three, and the
check holds no opinion about which number was being spelled.

```
cases 50032
numbers with a ZERO GROUP below a nonzero one 11191
numbers ending in a teen 4262
longest spelling, bytes 110
shape violations 0
digest 333427260
mismatches 0
```

Uniform draws over `0 .. 2³¹−1` almost never produce a zero group — each group is
zero with probability 1/1000, so 20,000 draws yielded 91. They are therefore
constructed: four groups, each independently zeroed a third of the time. Same
discipline as #270's constructed midpoints.

## Benchmark

`bench/` draws **200,000 integers** spanning the whole range once, then spells
every one of them with the ★ chunker **5 times** — 1,000,000 spellings. Sink
`989861056`, reproduced by **eight** builds: Kāra seq and auto-par, C seq and
pthreads, Rust seq and rayon, Go seq and goroutines, plus Python.

**The sink is order-invariant, and it had to become so for the parallel lane to
exist.** A running `sink = sink * 131 + byte` over the concatenation of every
spelling depends on the order they arrive in, so it cannot be checked against a
result assembled by workers. Each spelling is now hashed on its own —
order-dependent *within* an item, which is what keeps it a strong checksum — and
the item hashes are summed, which is order-invariant across items. The count is
printed beside it, because a sum alone cannot tell 1,000,000 items from 999,999.

**This is the corpus's owned-string-construction lane.** Per spelling the work is
three or four `a + b` concatenations of short strings, each allocating and
copying. #271 copies bytes in *bulk* through hoisted buffers and measures memcpy;
#266 *scans* bytes without producing any. This one produces, and nothing can be
hoisted — each step's output is the next step's input.

The algorithm **prepends**, and that is preserved in all five mirrors.
`out = piece + " " + out` cannot reuse the left buffer in any language, so every
mirror allocates and copies at every step. An append-based rewrite would let
Rust, Go and Kāra amortize into one growing buffer while C still copied — four
growth strategies rather than one algorithm, which is #267's phantom in a new
costume. C has no owned string type, so one is built explicitly: a malloc'd
buffer that its holder frees, with `join` extending the left operand by `realloc`
exactly as an owned-string `+` does.

### Two lanes, compared within themselves

**Cross-lane rows are not drawn.** "Auto-par Kāra vs single-threaded Rust"
conflates compiler quality with whether the comparator opted into parallelism,
and would let a parallel win mask a per-core regression. Each lane is compared
against its own kind.

#### Sequential lane — Apple M5 Pro, per-core, `KARAC_AUTO_PAR=0`

2026-08-15, `karac 0.1.0-dev.6106+g50267795a`, hyperfine 30 runs. The canonical
host — `bench/results.json`.

| Impl | Mean ± σ | vs Kāra |
|---|---|---|
| Go ‡ | 504.7 ± 8.7 ms | 0.66× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 747.1 ± 31.7 ms | 0.98× |
| Rust `-O` | 751.5 ± 34.7 ms | 0.99× |
| **Kāra (codegen)** | **762.7 ± 13.7 ms** | 1.00× |
| C `clang -O3` | 951.7 ± 27.1 ms | 1.25× |

‡ Go runs at **107.6% CPU** (514 ms user against 504.7 wall) — its concurrent
collector, on a lane where every other row is at 99.7%. Its wall-clock lead is
not entirely a per-core result.

**Kāra is ahead of C by 1.25× and level with both Rust builds** (within 2%, on σ
of 1.8–4.6%). The container had Kāra and C tied at 1.002×; on this host Kāra
pulls clear of C while staying pinned to Rust. That is the M5's cheaper allocator
rewarding the owned-string implementations — Kāra, Rust and Go all manage their
own string buffers, while the C mirror's explicit `malloc`/`realloc` join does
not benefit as much.

The finding the lane was built for survives and strengthens: **on a workload that
is nothing but string allocation, Kāra is not behind the systems languages.**

#### Parallel lane — Apple M5 Pro, 14 cores (6P+12E)

| Impl | Mean ± σ | user (ms) | CPU% | vs Kāra |
|---|---|---|---|---|
| Rust (rayon `par_iter`) | 137.7 ± 13.5 ms | 2349 | 1714% | 0.80× |
| Go (goroutines) | 157.9 ± 2.1 ms | 736 | 616% | 0.92× |
| **Kāra (`#[par_order_free]`)** | **172.2 ± 8.6 ms** | 2850 | 1661% | 1.00× |
| C (pthreads — metal floor) | 215.6 ± 15.4 ms | 3651 | 1698% | 1.25× |

**Kāra beats the C pthreads floor by 1.25× and trails rayon by the same factor.**
Its seq→par ratio is 762.7 → 172.2 ms, **4.43× on 14 cores** — much lower
efficiency than the container's 3.61× on 4, and the user-time column says why:
2850 ms of CPU against the sequential lane's 757 ms is **3.8× the total work** for
a 4.4× wall-clock gain. The auto-par lowering is paying real overhead at this
grain, where on 4 cores it paid ~4%.

**Go's row is the one to look at.** It reaches 157.9 ms on **736 ms of CPU** —
under a quarter of Kāra's and a fifth of C's — so on a throughput-per-core basis
it wins this lane outright. Rayon's 41.5% σ problem from the container does not
reproduce here (13.5 ms on 137.7, 9.8%).

> **Cross-lane caveat.** Parallel rows use 14 cores against the sequential lane's
> 1 and are **not comparable** to them. CPU% makes it unambiguous (seq ~99.7%,
> par 616–1714%).

#### The x86 corroboration run — sequential lane

| lang | mean (ms) | σ |
|---|---|---|
| C | 903.4 ± 11.4 | 1.3% |
| **Kāra** | **905.2 ± 8.8** | 1.0% |
| C (`-march=x86-64-v3`) | 910.6 ± 16.4 | 1.8% |
| Rust (checked + `target-cpu=v3`) | 920.5 ± 22.3 | 2.4% |
| Rust (checked, equal-safety) | 939.6 ± 8.5 | 0.9% |
| Rust | 955.4 ± 12.5 | 1.3% |
| Go | 1068.9 ± 20.4 | 1.9% |

On that host **Kāra is second, 1.002× behind C** — inside noise — and ahead of
both Rust builds and Go. On a lane that is nothing but string allocation, that is
a good result, and a narrow one, which is why it was probed rather than
celebrated.

#### The x86 corroboration run — parallel lane, 4 cores

| lang | mean (ms) | σ | user (ms) |
|---|---|---|---|
| C (pthreads — metal floor) | 247.3 ± 7.4 | 3.0% | 953 |
| **Kāra (`#[par_order_free]`)** | **251.0 ± 7.1** | 2.8% | 935 |
| Rust (rayon `par_iter`) | 368.0 ± 152.8 | **41.5%** | 1167 |
| Go (goroutines) | 486.6 ± 17.6 | 3.6% | 1280 |

**Kāra is 1.5% behind hand-written pthreads** — inside noise of the metal floor —
and its own seq→par ratio is **905.2 → 251.0 ms, a 3.61× speedup on 4 cores**,
about 90% efficiency. The user-time column is what makes that claim checkable:
935 ms of CPU against the sequential lane's 899 ms means the auto-par lowering
adds ~4% of total work, not that it found a shortcut.

**Rayon's σ is 41.5%, and that is reproducible** (a second 30-run measurement
gave 403.1 ± 125.9 ms), so its mean should not be ranked precisely against the
others. The user-time column says why: 1167 ms against C's 953 is ~22% more total
CPU. Spelling one integer is roughly a microsecond, and at that grain rayon's
dynamic work-stealing costs more than it recovers, in both mean and variance.
The three lanes that partition statically — Kāra's collect lowering, C's
contiguous slices, Go's — do not pay it. This is a scheduling-strategy
difference, not a language one; rayon is built for coarser items than this.

### The probe: Kāra's `+` never reuses the left buffer

Appending and prepending cost Kāra **the same**, which is the measurement:

| | append `s = s + lit` | prepend `s = lit + s` |
|---|---:|---:|
| Kāra | 52.4 ms | 53.2 ms |
| `rustc -O` | **3.0 ms** | 93.2 ms |

Nobody can reuse a buffer when prepending, so 93.2 ms is what the work costs when
it must be done and 3.0 ms is what it costs when it need not. Kāra pays the
prepend price for both. This lane prepends, so the missing optimization would not
have applied here — Kāra's second place is honest, and it does not generalize.

Three findings came out of that probe, all filed:

| spelling | 20,000 appends | peak RSS | |
|---|---:|---:|---|
| `s.push_str(x)` | 2.5 ms | 2,476 KB | matches Rust |
| `s = s + x` | 53.4 ms | 2,804 KB | **21×** — [`B-2026-08-14-23`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.md) |
| `s += x` | 6.1 s | **1,565,032 KB** | leaks every buffer — [`B-2026-08-14-22`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.md) |

1.5 GB of RSS for a 160 KB string is exactly `sum(8i, i=1..20000)` — every
intermediate, never freed. And through a `mut ref String` parameter the same
operator **silently drops the append**, so the caller sees an empty string while
the interpreter is correct ([`B-2026-08-14-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.md)).

The fast path already exists — `push_str` matches Rust. One change closes all
three: lower `s += x`, and `s = s + x` where the target is the left operand, to
that in-place append. Full write-up in [`bench/probe/`](bench/probe/). All three
were fixed the same day (`e6605e9`, `69abc03`, `645bc75`), and fixing them
surfaced a fourth — `s.push_str(s)`, a self-append on a heap string that must
grow, was a use-after-free (`B-2026-08-15-2`). Routing every spelling onto one
fast path inherits whatever that path got wrong.

### Why this kata has the corpus's first parallel string lane

Every one of the 37 existing par lanes is numeric or byte-scanning, and none is
newer than [#204](../../101-200/204-count-primes/). This is the first where each
parallel branch **allocates, grows and publishes a `String` per iteration**.

That is deliberate. `B-2026-08-14-28`'s fix note records that the par-branch
join's publish-time suppression scan carries one arm per cleanup kind —
`RcDec`, `RcDecOption`, `FreeInlineOptionPayload`, `FreeInlineOptionMapPayload`,
`FreeInlineResultPayload`, then a transfer loop for Map / File / Enum / Struct /
UserDrop / Soa / Column / DataFrame / Tensor — and that *"every one of those arms
exists because this exact failure was found once before at a different shape."*
That is a list discovered one entry at a time by whatever happened to wander in.
Both of the highest-severity bugs found in the corpus on 2026-08-14
(`B-2026-08-14-27`, `-28`) were par-branch join defects found by **sequential**
katas that happened to contain three independent `let`s.

A par branch that produces a heap value is therefore the highest-yield place to
point a lane. This one found nothing — the auto-par String collect is correct on
all eight builds — which is worth recording as a negative result rather than
leaving the surface untested.

## Kāra features exercised

- **`String` `+` concatenation** in three joining styles, and `Vec[String]`
  `push` / index / `join`.
- **`Set[String]`** as the shape oracle's vocabulary.
- **`String.split(" ")`** returning `Vec[String]`, including the empty-token case
  that the oracle turns on.
- **`f"{n}"`** as the integer-to-decimal-text conversion the positional walk
  drives off, and **`.bytes()`** to walk it.
- **A `Vec[String]` read at an index it is still being appended to** — the table
  solver's `g[837] = g[8] + " Hundred " + g[37]`.

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`; the ★ solver
and the differential match their Python mirrors. Both bench kernels — `spell.kara`
(auto-par) and `spell_seq.kara` — agree with each other, with the six non-Kāra
builds and with Python; they are checked across all four surfaces at reduced
size, the full 1,000,000-spelling size being out of reach for the tree-walk
interpreter.

The solvers found no compiler bug. **The bench probe found three**, all in the
same `String` append lowering: `B-2026-08-14-21` (silent wrong answer through a
`mut ref` parameter, high), `B-2026-08-14-22` (a leak of every intermediate
buffer, high) and `B-2026-08-14-23` (the missing left-buffer reuse, medium).

## Running

```bash
karac run int_to_words.kara
karac run int_to_words_places.kara
karac run int_to_words_table.kara

diff <(karac run int_to_words.kara) <(python3 int_to_words.py) && echo OK

# 50,032 probes, three solvers plus the shape oracle
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in int_to_words int_to_words_places int_to_words_table differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done

# cross-language benchmark (needs hyperfine, rustc, clang, go)
bash bench/bench.sh
```
