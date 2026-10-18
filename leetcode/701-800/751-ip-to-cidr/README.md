# 751. IP to CIDR

An IPv4 address is a 32-bit number written as four parts of 8 bits each,
`a.b.c.d`. A CIDR block `a.b.c.d/k` is the 2^(32 - k) addresses that
share the first k bits of `a.b.c.d`, which must be the block's first
address. Given a start address `ip` and a count `n`, return the fewest
CIDR blocks that cover exactly the n addresses from `ip` on, in address
order.

```
ip = "255.0.0.7", n = 10
    ->  ["255.0.0.7/32", "255.0.0.8/29", "255.0.0.16/32"]
ip = "117.145.102.62", n = 8
    ->  ["117.145.102.62/31", "117.145.102.64/30", "117.145.102.68/31"]
```

**Constraints:** 1 <= n <= 1,000; `ip` is a valid IPv4 address, and the
range fits below 2^32.

## Approaches

A block of 2^k addresses may start only at a multiple of 2^k, so each
step takes the largest block that starts at the current address and fits
in what is left; the arms differ in how they find that block and in how
they read and write the address.

| file | mechanism |
|---|---|
| `ip_to_cidr.kara` ★ | the largest block that may start at x is x's lowest set bit, `x & -x`; halve it until it fits, write it, move past it; O(32 x blocks) |
| `ip_to_cidr_trailing.kara` | count the zeros at the bottom of x and lower the count until the block fits; the address is read through `collect()` into a `Vec[Str]` and written with shifts and masks |
| `ip_to_cidr_tree.kara` | split the whole address space like a segment tree, writing every block that lies inside the range and halving every block that only overlaps it, the lower half first; the address is read character by character |
| `ip_to_cidr_prefixes.kara` | at each step try the prefix lengths from /0 to /32 and take the first whose block starts at x and fits; the parts are joined with `join` |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 11 lines: the two LeetCode examples; one
address and a thousand from 0.0.0.0; the last address; a thousand
addresses ending at the very end of the address space; 256 addresses
from an unaligned start and from an aligned one; one address; two
addresses across a boundary of the third part; and 300 random ranges of
1 to 1,000 addresses, with the number of blocks and a checksum of their
text. `ip_to_cidr.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which starts from one /32 block for each address and merges two
neighbouring blocks of one size into one of twice the size whenever the
first starts on a multiple of that size, until no two merge.
3,000 random ranges are checked, each of 1 to 300 addresses from a start
whose first part is at most 250 and whose lowest 0 to 12 bits are
cleared, so that large aligned blocks occur; their answers hold
14,258 blocks in all.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | read back, the blocks each start on a multiple of their size, follow one another from the start, and hold n addresses |
| P3 | the range moved up by 1,024, 2,048 or 3,072 addresses, more than any block here holds, gives the same blocks moved up |
| P4 | the range mirrored through the address space, each address a turned into 2^32 - 1 - a, gives the same prefixes in reverse order |

It prints `3000 ranges (14258 blocks in all), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the prefix one bit too short | P1 3000, P2 3000 |
| M2 | ★: a block one address too big kept | P1 1523, P2 1523, P4 1579 |
| M3 | ★: the address read in base 255 | P1 3000, P2 3000, P3 3000, P4 2989 |
| M4 | trailing: no block bigger than 16 addresses | P1 2612 |
| M5 | trailing: twice the block taken off what is left | P1 2939, P2 2939, P4 2914 |
| M6 | trailing: the third part written from the wrong bits | P1 2984, P2 2984, P3 3000 |
| M7 | tree: the upper half tried first | P1 2939, P2 2939 |
| M8 | tree: the address's digits read in base 16 | P1 3000, P2 3000, P3 856, P4 2291 |
| M9 | tree: the second part written modulo 255 | P1 2987, P2 2987 |
| M10 | prefixes: a block not checked to start on its size | P1 1254, P2 1254, P4 2917 |
| M11 | prefixes: the last two parts written in the wrong order | P1 2999, P2 2999, P3 3000 |
| M12 | prefixes: no block bigger than /26 | P1 1416 |
| E1 | ★: a bigger first size for address 0 | 0 |
| E2 | trailing: the zeros counted on to 33 | 0 |
| E3 | tree: the search started from a block of 2^33 | 0 |

P1 kills all twelve. P2, which reads the blocks back and checks that
they tile the range, sees every edit that writes a wrong block or a
wrong address, except M4 and M12: these only cap the block size, so the
range is still tiled exactly, by more and smaller blocks than it needs,
and only the definition sees that. P3 sees the edits that misread or
miswrite an address in a way that moving it changes: M3, M6, M8 and
M11. P4 sees the edits that get block sizes wrong in a way that is not
symmetric, M2, M3, M5, M8 and M10. M1 makes every prefix one bit short
in the same way, so the mirrored list agrees. M7 writes the right
blocks, last first: P2 sees it, since the blocks no longer follow one
another from the start, and P4 cannot, since the mirrored answer is
reversed in the same way. E1 starts address 0's block larger and halves
it anyway; E2 counts zeros on to 33 and lowers the count anyway;
E3 starts the split from a block of 2^33, which only overlaps the range
and is halved at once.

## Verification

Every arm prints the same output as `ip_to_cidr.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`1a5c083e3a`, whose last compiler change is `4655692faa`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse every program here at type checking.
The ★, tree and prefixes arms stop at the harness's `*` over a string's
`bytes().iter()` (`*ch`), since legacy gives those by value where
v2 gives references; the trailing arm and the differential at
`collect()` after `split`, which legacy's `split` does not need, as it
already returns a `Vec`; and the bench program at `pool[q % 1000]`
passed to the arm, which legacy takes as a move out of the vector where
v2 lends it. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes a pool
of 1,000 random addresses as text once, and for each of 500,000 queries
takes the next address from the pool and a random count from 1 to
1,000 and finds the blocks, adding up how many there are and a checksum
of their lengths. Every implementation prints `500000 ranges:
4261274 blocks in all, checksum 567855528`, the Kāra program under
`karac __mir-run` included (in 28 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.72 to 0.81 s |
| Rust (`rustc -O`) | 0.89 to 1.06 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.96 to 1.06 s |
| Go | 1.66 to 1.78 s |
| Python | 4.3 s |
| Kāra (`karac build --mir`) | 0.64 to 0.70 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 6.5 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So at the medians of the interleaved runs the v2 build is the fastest of
the compiled programs at 0.66 s, ahead of C (0.73), Rust (1.01, or
1.00 under overflow checks) and Go (1.69). The work is mostly writing
the blocks as text, and the C, Rust and Go programs do it with their
general formatting routines (`snprintf`, `format!`, `fmt.Sprintf`):
under valgrind's cachegrind v2 runs 7.6 billion instructions against C's
9.2 billion and Rust's 13.1 billion. The legacy backends refuse the
program. To have a legacy time at all, the bench was copied for legacy
alone with `pool[q % 1000].clone()` passed to the arm: the legacy build
of that copy ran 0.73 to 0.82 s, a median of 0.75 s in the interleaved
runs, so v2 takes about nine tenths of legacy's time, inside M2's limit
of twice legacy. That copy is a measurement only and is not in the kata,
and new katas' benches are outside M2's frozen set in any case. The
comparison with C and Rust waits until after M4.

## Compiler findings

None new.
