# 340. Longest Substring with At Most K Distinct Characters

Given a string `s` and an integer `k`, return the length of the longest
substring of `s` that contains at most `k` distinct characters.

```
"eceba", k = 2  ->  3    "ece"
"aa",    k = 1  ->  2    "aa"
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `longest_k_distinct.kara` ★ | a sliding window with a count per character in a `Map[char, i64]`: grow on the right, drop from the left while the map holds more than `k` keys | `O(n)`, `O(k)` |
| `longest_k_distinct_array.kara` | the same window over a 128-slot `Vec[i64]` of counts and a counter of the kinds in the window | `O(n)`, `O(1)` |
| `longest_k_distinct_lastpos.kara` | a `Map` of each character's last position; a `(k + 1)`-th character evicts the one seen least recently and the window restarts after its last sighting | `O(n k)`, `O(k)` |
| `longest_k_distinct_nonshrink.kara` | a window that never shrinks: when it holds too many kinds it loses exactly one character on the left, so its final length is the answer | `O(n)`, `O(k)` |
| `longest_k_distinct_brute.kara` | from every start, extend with a `Set` until a `(k + 1)`-th character would join | `O(n w)`, `O(k)` |
| `differential.kara` | the five arms, an independent oracle and eight properties | — |
| `bench/longest_k_distinct.kara` | 400 windows over 20,000-letter strings, by the ★ arm | — |

Every arm prints the same 13 lines: eight hand cases (the two examples, the
empty string, `k = 0`, `k` larger than the string, and three mixed cases) and
a summary of five generated strings, up to 50,000 letters drawn from up to 52.
The five arms' output is byte-identical, and `longest_k_distinct.py` mirrors
the ★ arm.

## Differential

`differential.kara` compares the five arms with an oracle that tries every
substring from the longest down and counts its distinct characters by sorting
them (cubic, and sharing no code with any arm). It runs on the eight hand
cases and 300 generated strings (0 to 40 letters from alphabets of 1 to 6,
`k` from 0 to 7), and checks the properties on each.

| | property |
|---|---|
| P1 | the five arms agree (also on the five large strings the arms print) |
| P2 | they equal the oracle |
| P3 | `k = 0` gives 0, and `k` at least the number of distinct characters gives the length of `s` |
| P4 | the answer never falls as `k` grows |
| P5 | the answer is at most the length of `s` and at least `min(length, k)` |
| P6 | reversing `s` keeps the answer |
| P7 | renaming the characters one-to-one keeps the answer |
| P8 | for `s + t` the answer is at least each part's and at most their sum |

`308 cases checked (answers add up to 4276), 0 failures` under
`karac run --interp`. The differential does not yet build: it copies
`cases[i + 1].0.clone()` out of a `Vec[(String, i64)]`, and codegen lowers
that clone only when the subscript is a name or a literal (B-2026-10-05-2,
the remainder of B-2026-10-04-54; see Compiler findings). The five arms
themselves build and run on every surface.

## Mutation testing

Twelve edits to the copies inside `differential.kara`, each run under
`--interp` with every failure printed rather than the first ten. The mutants
run without the three 50,000-letter strings, because M10 turns the brute arm
quadratic in the string length on the four-letter one.

| # | mutation | outcome | how |
|---|---|---|---|
| M1 | ★: shrinks while the count is at least `k` | **killed** | P1 |
| M2 | ★: window length off by one | **killed** | P1 |
| M3 | ★: never removes a character whose count reaches 0 | **killed** | panics (`unwrap()` on `None`) |
| M4 | array: a new kind is not counted | **killed** | P1 |
| M5 | array: an emptied kind is not uncounted | **killed** | panics (index out of bounds) |
| M6 | last position: the window restarts at the evicted sighting, not after it | **killed** | P1, P6 |
| M7 | last position: evicts the newest character instead | **killed** | P1, P6 |
| M8 | non-shrinking: loses two characters instead of one | **killed** | P1 |
| M9 | non-shrinking: final length off by one | **killed** | P1 |
| M10 | brute: allows `k + 1` kinds | **killed** | P1 |
| M11 | brute: counts the character that broke the run | **killed** | P1 |
| M12 | array: shrinks while the kinds are at least `k` | **killed** | P1 |

P1 catches every non-panicking mutation, because each arm is compared with
the ★ arm's answer first. M3 and M5 never let the window lose a kind, so it
runs off the end of the string before any property is checked.

## Verification

All five arms print the same standard output under `karac run` (LLJIT),
`karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the default
auto-parallelising `karac build`, and that output is byte-identical to
`longest_k_distinct.py`. At `-O0` with `KARAC_AUTO_PAR=0` and
`KARAC_BUF_CACHE=0`, valgrind reports all five clean (`All heap blocks were
freed`, no errors).

The last-position arm walks its `Map` to find the oldest sighting, which is a
walk in per-process hash order; it takes the minimum, so its output does not
depend on that order.

## Benchmarks

`bench/longest_k_distinct.kara` and its four mirrors time the ★ arm as
written: a sliding window with a count per character in a hash map. Eight
pseudo-random strings (20,000 letters each, from alphabets of 4 to 52 letters)
are generated once; round `r` takes string `r % 8` and `k = (r * 7) % 30 + 1`,
for 400 rounds. A rolling hash of every round's answer is the sink. Rust uses
`HashMap<char, i64>` with `entry`, Go a `map[rune]int64`, Python a `dict`, and
C, which has no standard map, a 128-slot open-addressing table with backward
shift deletion.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each (Python: 3), on a 4-core x86-64 Linux container, measured
2026-10-04, karac built from `main` at `4ed27deb7`. Python is its own lane.

| implementation | mean | vs fastest |
|---|---|---|
| c `clang -O3` (hand-written table, no SipHash) | 60.3 ms ± 2.4 | 1.00× |
| c `-march=x86-64-v3` (matched-ISA) | 63.1 ms ± 3.5 | 1.05× |
| rust `-O` | 217.8 ms ± 5.0 | 3.61× |
| rust `-C target-cpu=x86-64-v3` (matched) | 223.3 ms ± 11.9 | 3.70× |
| rust `-O -C overflow-checks=on` (equal-safety) | 224.0 ms ± 5.6 | 3.71× |
| go `go build` | 308.0 ms ± 15.1 | 5.11× |
| **kāra `karac build`** | **496.5 ms ± 30.5** | **8.23×** |
| python 3 | 2044 ms ± 96 | 33.9× |

Kāra is 2.2× equal-safety Rust here, and the reason is the map
(B-2026-10-04-56, since fixed: 1.85×, see Compiler findings). Kāra and Rust both hash with SipHash-1-3, but under
callgrind Kāra's hash alone costs more instructions than Rust's whole run:
26.5M hash calls at 92 instructions each, half of Kāra's total, against about
18.5M hashes in Rust. The counting step `counts.insert(c, counts.get(c)
.unwrap_or(0) + 1)` hashes the same key twice where Rust's `entry` hashes once.
The `entry` spelling in Kāra, `*counts.entry(c).or_insert(0) += 1`, measured
0.38 to 0.43 s, still 1.9× Rust, so the rest is the per-hash cost and the map's
own path. The C table hashes its one-byte key with a single multiply rather
than SipHash, so it is not an equal-hashing comparison.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 121.7 ms ± 3.0 | 15.8 KiB | 1.8 MiB |
| rust | 252.9 ms ± 9.8 | 3888.9 KiB | 2.4 MiB |
| kāra | 369.6 ms ± 10.3 | 350.0 KiB | 2.6 MiB |
| go | — | 2179.4 KiB | 6.4 MiB |
| python | — | — | 8.2 MiB |

`karac build` is 3.0× clang's cold compile and 1.5× rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

The benchmark kernel's sink matches all four language twins and Python
(`sink 141288741`).

## Compiler findings

- **B-2026-10-04-61 (soundness, high): any expression was accepted as an assignment
  target.** Writing the bench, the counting step in Rust's form,
  `counts.entry(c).or_insert(0) += 1`, passed `karac check`, crashed the
  interpreter and failed codegen naming an LLVM type. So did `(a, b) = (b, a)`,
  `a + 1 = 3` and `v.len() = 3`, and compiled, the tuple swap silently did
  nothing (`1 2`, exit 0). Fixed in the kara repo: each is now an error
  (E0287), a call returning `mut ref` gets the missing `*` as a `karac fix`
  edit, and a parenthesized swap is pointed at Kāra's `a, b = b, a`. The place
  form, `*counts.entry(c).or_insert(0) += 1`, was right on both backends all
  along.
- **B-2026-10-04-56 (perf, medium): the ★ arm's `Map[char, i64]` ran 2.2x
  Rust's `HashMap` at equal hashing.** The counting step
  `counts.insert(c, counts.get(c).unwrap_or(0) + 1)` hashed `c` twice where
  Rust's `entry` hashes once, and the hash was half of all instructions. Fixed
  in the kara repo: a mono `Map` operation now takes its key's hash at the call
  site, so the two calls share one. The bench went from 4.68 G to 3.43 G
  instructions and from 498 ms to 399 ms, against 216 ms for Rust with
  overflow checks (2.31x to 1.85x, hyperfine, 30 runs, same session). The rest
  of the gap (the per-hash cost, a second hash in `remove`, the insert's probe)
  is B-2026-10-04-79. The table above was measured before the fix.
- **B-2026-10-04-54 (codegen gap, medium, fixed): `.clone()` on a tuple element reached
  through an index or a `ref` parameter did not build.** Fixed for a name or
  literal subscript (`cases[i].0.clone()` now builds). The differential's
  `cases[i + 1].0.clone()` still fails `karac build` with "Vec/String method
  'clone' is not yet supported in codegen", which is **B-2026-10-05-2 (codegen
  gap, medium, open)**; the differential runs under `--interp` until then.
- **B-2026-10-04-55 (miscompile, medium, open): an assignment through `*` of a user
  function's returned `mut ref` is dropped** on both backends: `*bump(mut x)
  += 5` leaves `x` unchanged. Found probing assignment targets for B-2026-10-04-61;
  the kata does not write through a returned reference.
- **B-2026-10-04-60 (diagnostics, low): a keyword used as a name cascaded, and
  `karac fix` could not repair it.** The first draft named its counter
  `distinct`, a reserved word. Two of its seven uses went unreported,
  `return distinct;` was read as the start of a `distinct type` item, and
  although every message said to write `r#distinct`, `karac fix` applied
  nothing. Fixed in the kara repo: one error per use, each carrying the `r#`
  edit, and the fixed file parses. The kata names the counter `kinds`.
