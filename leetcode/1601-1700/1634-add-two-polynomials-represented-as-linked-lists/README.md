# 1634. Add Two Polynomials Represented as Linked Lists

A polynomial linked list is a special type of linked list where every
node represents a term in a polynomial expression.

Each node has three attributes:

- `coefficient`: an integer representing the number multiplier of the
  term. The coefficient of the term `9x^4` is `9`.
- `power`: an integer representing the exponent. The power of the term
  `9x^4` is `4`.
- `next`: a pointer to the next node in the list, or `null` if it is the
  last node of the list.

The polynomial linked list must be in its standard form: the polynomial
must be in **strictly** descending order by its `power` value. Also,
terms with a `coefficient` of `0` are omitted.

Given two polynomial linked list heads, `poly1` and `poly2`, add the
polynomials together and return *the head of the sum of the
polynomials*.

**`PolyNode` format:** the input and output format is a list of `n`
nodes, each node represented as its `[coefficient, power]`. For example,
the polynomial `5x^3 + 4x - 7` is represented as
`[[5,3],[4,1],[-7,0]]`.

```
poly1 = [[1,1]], poly2 = [[1,0]]                              ->  [[1,1],[1,0]]
poly1 = [[2,2],[4,1],[3,0]], poly2 = [[3,2],[-4,1],[-1,0]]    ->  [[5,2],[2,0]]
poly1 = [[1,2]], poly2 = [[-1,2]]                             ->  []
```

**Constraints:** `0 <= n <= 10^4`; `-10^9 <= PolyNode.coefficient <= 10^9`;
`PolyNode.coefficient != 0`; `0 <= PolyNode.power <= 10^9`;
`PolyNode.power > PolyNode.next.power`.

## Approaches

| file | mechanism |
|---|---|
| `poly.kara` ★ | both lists merged in one walk, as two sorted lists merge: a `match` on the pair of heads takes the higher power, or both heads' sum for equal powers, and a nonzero term hangs off a dummy head through a tail handle. The list is a `shared struct PolyNode` with a `mut next`. O(m + n) |
| `poly_recursive.kara` | recursion: the sum is the higher leading term followed by the sum of what is left, or for equal powers their nonzero sum followed by the sum of both tails; an or-pattern `(None, rest) \| (rest, None)` returns the other side. O(m + n) calls |
| `poly_map.kara` | every term of both lists added into a `SortedMap` from power to coefficient, then each nonzero term pushed onto the front of a new list, lowest power first, so the highest ends first. O((m + n) log(m + n)) |
| `differential.kara` | the three arms against the statement read literally, six properties |

LeetCode offers no Rust template for this problem, so there is no
Rust-template arm.

Every arm prints the same 9 lines: LeetCode's three examples, two empty
lists, one empty list, and terms that cancel in the middle; then the
terms counted, the coefficients summed and a checksum for 3000 random
pairs of up to 5 terms with powers below 8 and coefficients -3 to 3, 300
of up to 50 terms below 100 with coefficients -1000 to 1000, and 5 of up
to 5000 terms below 10000 with coefficients -5 to 5. `poly.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the three arms and the statement read
literally: a polynomial is its coefficient at each power, so the sum is
the two added power by power in an array, written out from the highest
power down with every zero left out. It checks 3000 random pairs of up
to six terms with powers below 8, every other pair with coefficients 1
and -1, so terms cancel often, the rest -3 to 3, each pair with a third
polynomial for P4. Every pair is drawn before any arm answers.

| | property |
|---|---|
| P1 | the sum is the statement read literally |
| P2 | adding the other way round gives the same sum |
| P3 | adding the second's negation to the sum gives back the first |
| P4 | adding a third polynomial is the same grouped either way |
| P5 | the sum's powers fall strictly, no coefficient is 0, and its coefficients total the two inputs' totals |
| P6 | each arm agrees with at least one of the other two |

The differential prints `3000 problems: checksum 393229330, 54000 checks
over 3 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, three or four to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. A zero sum kept only at power 0 (M2,
M7) is the hardest to catch: only 124 sums show it to P1, and P3, which
adds a negation and so cancels every term, sees it 722 times.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the lower power taken first when the powers differ | P1 2753, P3 247, P4 296, P5 2753, P6 2753 |
| M2 | ★: a sum of 0 kept at power 0 | P1 124, P3 722, P5 124, P6 124 |
| M3 | ★: equal powers move on in the first list only | P1 2107, P2 1624, P3 2888, P4 616, P5 2064, P6 2107 |
| M4 | ★: the tail never moves on | P1 2952, P3 2866, P4 294, P5 2536, P6 2952 |
| M5 | recursive: an empty side makes the sum empty | P1 2334, P3 1516, P4 415, P5 2109, P6 2334 |
| M6 | recursive: the higher leading term drops the other list's head | P1 2206, P2 2753, P4 1068, P5 1939, P6 2206 |
| M7 | recursive: a sum of 0 kept at power 0 | P1 124, P3 722, P5 124, P6 124 |
| M8 | map: a term's coefficient replaces the sum so far | P1 2107, P2 1624, P3 2888, P5 1873, P6 2107 |
| M9 | map: negative coefficients left out | P1 2786, P3 2841, P4 1750, P5 2786, P6 2786 |
| M10 | map: powers walked highest first, so the list ends lowest first | P1 2952, P3 2605, P5 2952, P6 2952 |

## Benchmarks

The bench draws 10 random pairs of polynomials with powers below 400000,
each power present at even odds with a coefficient from -3 to 3 but not
0, all of them first as terms; then it builds each pair into two linked
lists of about 200000 nodes, adds them by the ★ arm in all five
languages, and walks the sum. The lists are Kāra's counted `shared
struct`, Rust's `Option<Box<PolyNode>>` with a `&mut` tail, Go's and
Python's pointers, and C's `malloc`'d nodes, freed as they are walked.
Every implementation prints `10 pairs of up to 400000 terms: 2838755
terms, checksum 801661489`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ee08f070a` on LLVM 22:

| | median |
|---|---|
| Kāra (`karac build`) | 0.263 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.272 s |
| Rust (`rustc -O`) | 0.354 s |
| C (`clang -O3`) | 0.369 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.402 s |
| Go | 0.598 s |
| Python | 8.1 s |

The sequential Kāra build is 23% faster than Rust and 32% faster than
Rust with overflow checks on, the equal-safety comparison
(BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.292 s and
0.341 s on one run).

## Verification

All three arms print the same output as `poly.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `336218278`.

## Writing it

The ★ arm first declared its two cursors Rust's way,
`let (mut a, mut b) = (poly1, poly2);`, and `karac fix` moved the `mut`
before the pattern, `let mut (a, b) = ..`, which makes every binding
mutable. The `match (a, b)` with guards on the heads' powers, the `break`
in its `(None, None)` arm, and the tail handle that is both hung off the
list and moved on (`tail.next = Some(node); tail = node;`) checked clean:
a `shared struct` value is a counted handle, so `node` is still there
after the list takes it.

The recursive arm checked clean as first written, its or-pattern binding
`rest` on either side included.

The map arm walks both lists with `for poly in [poly1, poly2]`, and an
element of a `for` is a borrow, so `let mut node = poly` bound `node` to
one; `node = n.next` was then refused for moving a value into a borrow
(core semantics §3.7), and `karac fix` wrote `node = ref n.next`, which
borrows the next node in turn. The same walk over a parameter,
`let mut node = poly` in the harness's `to_terms`, binds a value and
takes `node = n.next` as it is.
