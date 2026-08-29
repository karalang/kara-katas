# 297. Serialize and Deserialize Binary Tree

Turn a binary tree into a string, and that string back into the same tree. The
values carry no ordering guarantee and may repeat, so knowing the *multiset* of
values tells you nothing about which tree they came from — the encoding has to
carry the **shape**.

```
      1                 preorder      "1,2,#,#,3,4,#,#,5,#,#"
     / \                level order   "1,2,3,#,#,4,5"
    2   3               parenthesized "1(2)(3(4)(5))"
       / \
      4   5
```

## Approaches

| file | mechanism | shape of the parser |
|---|---|---|
| `codec.kara` ★ | preorder + `#` at every empty slot | recursive descent, one shared cursor |
| `codec_level.kara` | level order, trailing sentinels trimmed | flat loop over a FIFO |
| `codec_paren.kara` | nested parentheses, no sentinel | recursive descent by brace matching |
| `differential.kara` | 900 trees, three arms, five properties | — |
| `bench/treecodec.kara` | 200k-node tree, 24 chained round trips | benchmark lane |
| `codec.py` | mirror of the ★ arm | — |

## The nulls are the problem, not the values

A preorder walk of the values alone is ambiguous: `1,2,3` is three different
trees. What disambiguates it is recording where the children **are not** — every
absent child becomes a `#`, so the traversal is *total* over the 2n+1 positions
of an n-node tree rather than partial over its n values. That is the whole
trick, and it is why the encoded length is proportional to nodes-plus-nulls.

Deserialization then needs one shared, mutable read position across the whole
recursion:

```
token is `#`   ->  this slot is empty, consume one token, return None
otherwise      ->  build a node, then recursively fill left, then right
```

The recursion **order** is doing the work. Because serialize emitted root before
left before right, and deserialize consumes in exactly that order, the cursor
never looks ahead or back — the string is a transcript of the call tree,
replayed. Get the order wrong in either direction and the shape comes back
mirrored with no error raised, which is what makes the round-trip a *property*
worth testing rather than a few spot checks.

## Three encodings that agree on nothing but the tree

The arms differ in traversal order (preorder vs breadth-first), in how absence
is recorded (a sentinel token vs a trimmed row vs a delimiter pair), and in how
parsing is driven (a shared cursor vs a queue vs brace matching). A bug in one
has no route into the others, which is what makes agreement evidence rather
than coincidence.

| arm | how it can be wrong |
|---|---|
| **A** preorder | the cursor desyncs — one token consumed too many or too few |
| **B** level order | a child pushed in the wrong order, or the trailing row mis-trimmed |
| **C** parentheses | the empty pair in `1()(2)` dropped, so a right child moves sides |

C's asymmetry is the sharpest of the three. A node writes `(left)(right)` and an
absent child writes nothing — so a right-only node cannot simply omit the left
pair, or `1()(2)` collapses to `1(2)`:

```
left only    1(2)
right only   1()(2)      the empty pair is LOAD-BEARING
both         1(2)(3)
neither      1
```

That case has no analogue in either other arm, and it is exactly what a
hand-written parser gets wrong while passing every balanced example.

### The strings are never compared

Each arm's encoding is its own — B trims trailing sentinels, so it is not even
canonical against a level-order encoder that emits them. The differential
compares **reconstructed trees**, fingerprinted through A's preorder form.
Comparing encodings across arms would test the formats, not the codecs.

### The five properties

| | what it checks |
|---|---|
| P1 | round-trip identity — `deserialize(serialize(t))` is `t`, per arm |
| P2 | cross-format agreement — all three reconstruct the same tree |
| P3 | serialization is a function of the tree — equal trees, equal strings |
| P4 | structure survives — node count, height, and the in-order sequence |
| P5 | right-only spines, negative values, duplicate values, deep spines |

**P4 is the one that catches a mirrored tree.** P1 and P2 both compare through a
fingerprint that is itself a preorder walk, so an arm that swapped left and
right *consistently in both directions* would round-trip perfectly and agree
with itself. The in-order sequence is what separates them, because mirroring
reverses it.

## Compiler bugs this kata found

| id | what | status |
|---|---|---|
| [`B-2026-08-26-11`](../../../../kara/docs/bug-ledger.md) | design.md's `String` method table documents `push_char`, which does not exist; the working method is `push(c: char)` and has no row | fixed |
| [`B-2026-08-26-12`](../../../../kara/docs/bug-ledger.md) | **heap corruption**: an `if`-expression yielding an `Option[shared]`, passed by value into a function inside a loop that rebinds it, aborts on both compiled backends | fixed (`3454927`) |
| [`B-2026-08-27-34`](../../../../kara/docs/bug-ledger.md) | **silent wrong answer**: 3454927 emits the branch-leaf retain once per *binding*, not per *use*, so the third read of the selected value returns garbage — and the binary exits `0` | fixed (`c56e598`) |
| [`B-2026-08-27-43`](../../../../kara/docs/bug-ledger.md) | the same defect one shape over, split out of `-34`: when the arm hands out an ARM-LOCAL binding its own scope-exit dec cancels the leaf retain, so the *first* read already returns garbage | fixed (`9f62ac6`) |
| [`B-2026-08-26-13`](../../../../kara/docs/bug-ledger.md) | `String.split` has no borrowing form — one allocation and one copy per token | relocated to the roadmap's `StringSlice` item |

### `differential.kara` was the live witness for B-2026-08-27-34

All four arms are now byte-identical on all four surfaces — `karac run
--interp`, `karac run` (JIT), `karac build`, and `KARAC_AUTO_PAR=0 karac build`
— and `codec.kara` matches `codec.py` exactly. The differential printed
`DIFFERENTIAL OK` under the interpreter and aborted on both compiled backends
until `c56e598` and `9f62ac6`; the account below is what it took to get here,
kept because each fix left the kata still wrong in a way that looked like the
one before it.

Property 5 selects between two subtree handles with an `if`-expression and then
consumes the result four times — once for the expected fingerprint and once per
codec arm. **That count is the bug.** The first form of it (`B-2026-08-26-12`,
fixed by `3454927`) taught a value-position branch leaf to retain the
`Option[shared]` it hands out; the retain is emitted once for the *binding* and
not once per *use*, so two reads balance and the third reads through a freed
box. Dropping any one of P5's three arms makes it green, and duplicating one arm
instead of adding a distinct one crashes just the same — which is what shows the
count, not the arms, to be the variable.

Per the corpus rule that a kata must **never route around a compiler gap**, the
differential is not being rephrased. It stays in the shape that finds it. The
minimal form has no loop at all:

```kara
shared struct Node { val: i64 }
fn make(n: i64) -> Option[Node] { return Some(Node { val: n }); }
fn show(t: Option[Node]) -> i64 { match t { None => { return 0; } Some(n) => { return n.val; } } }
fn main() {
    let a = make(1);
    let b = make(2);
    let t = if true { a } else { b };
    println(f"{show(t)} {show(t)} {show(t)}");   // interp: 1 1 1
}                                               // build:  1 1 <garbage>, exit 0
```

The compiled binary **exited 0**. There was no abort and no diagnostic — only a
wrong number that differed run to run. Removing the `if` made it green.

`c56e598` fixed that by registering the consuming binding, so it takes a retain
per use rather than inheriting the leaf's single one. One shape survived it:
when the arm hands out an ARM-LOCAL binding (`if c { let u = make(1); u }`) that
local's own scope-exit dec cancels the leaf retain inside the arm, so the value
escapes owned by nobody and the FIRST read is already garbage. Static
re-derivation could not see it — the arm's name env is reverted before the
consuming `let` classifies its RHS — so `9f62ac6` (`B-2026-08-27-43`) records
the retains at emission instead and matches the leaf against that record.

Notably, linking either form with `-fsanitize=address` runs **clean**, and
structurally so: the sanitizer is linked in, never compiled in, so it sees
allocator faults and cannot see a use-after-free *access* from the
uninstrumented Kāra object. That is why the compiler's ~1200-fixture ASAN corpus
never caught the class, and why the regression tests live in the ordinary E2E
harness instead.

## Benchmarks
<!-- bench-staleness -->
> **Figures in this section are a 2026-08-26 snapshot; the feed was last measured 2026-08-28.** Where the two disagree, [`bench/results.json`](bench/results.json) and the [charts](../../../BENCHMARKS.md) are current; the numbers below are kept because the analysis around them explains *why* the shape is what it is, and that reasoning outlives the milliseconds.
> Comparative claims below ("ahead of C", "leads Rust", ratios) were true of the snapshot and have **not** been re-verified against the current feed — treat them as historical, not as the standing result.

> **Two hosts, both shown.** The headline table is the canonical Apple M5 Pro
> lane, [`bench/results.json`](bench/results.json) — the file
> `scripts/consolidate-bench.sh` feeds into the top-level chart. The second
> table is a shared x86-64 Linux cloud container,
> [`bench/results.container-x86.json`](bench/results.container-x86.json), which
> is where every figure in the analysis was measured. Absolute milliseconds are
> NOT comparable between the two; only the **within-file cross-language ratios**
> are.

Build one balanced 200,000-node tree, then 24 **chained** round trips —
serialize, hash the string, deserialize, repeat on the reconstruction. Chaining
matters: a deserializer that dropped or duplicated a subtree would drift the
string length and move the sink, which serializing the same original 24 times
would not notice. Sink: a polynomial hash over the bytes of every encoded
string, `checksum 397546302`, identical in all five languages.

**Canonical lane — Apple M5 Pro**, [`bench/results.json`](bench/results.json),
30 runs each. This is the feed `scripts/consolidate-bench.sh` publishes:

| lang | mean | vs C |
|---|---:|---:|
| Go | 436.6 ms ± 2.3 | 0.92× |
| C `clang -O3` | 477.0 ms ± 4.0 | 1.00× |
| Rust `-O` | 484.5 ms ± 5.9 | 1.02× |
| Rust `-O -C overflow-checks=on` (equal safety) | 486.0 ms ± 4.6 | 1.02× |
| **Kāra** (codegen, seq) | **841.9 ms ± 12.3** | **1.77×** |

Kāra is **1.77× C**. Note that Go beats C here by 1.09×, which it does not do on
the container — a reminder that the cross-language ordering is a property of the
host as much as of the code.

**Corroborating lane — x86-64 Linux container**,
[`bench/results.container-x86.json`](bench/results.container-x86.json). Every
figure in the analysis below was measured here, so the container table is what
those numbers should be read against:

| | mean | vs C |
|---|---:|---:|
| c (`-O3`) | 1.185 s | 1.00× |
| rust (`-O`) | 1.213 s | 1.02× |
| rust (`-O -C overflow-checks=on`, equal safety) | 1.226 s | 1.03× |
| go | 1.497 s | 1.26× |
| **kara** (codegen, seq) | **2.438 s** | **2.06×** |
| python | 16.770 s | 14.2× |

> **Ratios on the container move with load, so they are cross-checked by
> interleaving.** Alternating the kāra and C binaries 12 times each gives a
> median ratio of **2.08×** (2.43 s / 1.17 s) and a min-of-runs ratio of 1.99×,
> which is what the container table should be read as. An earlier sequential run
> at lower load reported 1.87×; that was measurement, not a code change — the
> kāra binary is byte-identical in size across both, and the bench lane contains
> no branch-leaf `let`, so none of the fixes above could have touched its
> codegen. Every figure below is likewise a median over interleaved runs.
>
> The 2.06× container figure and the 1.77× M5 figure are the same program on two
> hosts, not a disagreement. Absolute milliseconds are not comparable between
> them; only within-file ratios are, and both put the gap in the same place.

### Where the gap goes, measured (container lane)

Ablating the compiled Kāra binary one stage at a time (200k nodes, 24 rounds,
median of 7 interleaved runs):

| stage | time |
|---|---|
| serialize + hash, no deserialize | 0.89 s |
| serialize + deserialize, no hash | 2.16 s |
| all three | 2.45 s |

So **deserialize is ~1.6 s of it** — two thirds of the total, and effectively
the whole gap. It is not the tree building and not the string append.

Narrowed to a micro-benchmark (split a 3.2 MB comma-separated string 24 times):

| | time |
|---|---|
| C, split in place (no copies) | 0.04 s |
| Rust, `split(',').collect::<Vec<&str>>()` (borrowed) | 0.19 s |
| **Kāra, `s.split(",")`** | **0.68 s** |
| Rust, `split(',').map(String::from).collect()` (owned copies) | 1.01 s |

**Kāra's `split` is not slow — it beats Rust's same-semantics version by 1.5×.**
The gap is that `String.split` returns `Vec[String]`: one heap allocation and
one copy per token, with no slice-returning variant to reach for. C splits in
place, Rust and Go hand back views into the original buffer, and those are the
versions the other three arms are running. Python allocates copies as Kāra does
and is 14× slower than C, so this is the cost of the API *shape*, not of the
implementation behind it.

That is `B-2026-08-26-13`, now tracked on the roadmap's `StringSlice` item as
specified v1 behaviour with a v2 successor. It is not worked around here: the
kata keeps the idiomatic `s.split(",")` spelling, which is the whole point of
writing katas.

> The deserializer reads each token as `let tok = ref tokens[i];`. The borrow is
> not an optimisation for the benchmark's sake — since `E_INDEX_MOVE_NON_COPY`
> landed, `tokens[i]` on a non-`Copy` element is a hard error, and `ref` is the
> apt one of the three offered repairs for a read-only use. `karac fix` proposes
> `.clone()`, which also compiles and cost this lane roughly a third of its
> runtime: worth knowing that the machine-applicable fix is not always the right
> one.

### Elsewhere

| | | kara | c | rust | go |
|---|---|---:|---:|---:|---:|
| binary size | M5 | 295.9 KiB | 33.1 KiB | 456.8 KiB | 2451.5 KiB |
| | container | 345.7 KiB | 16.0 KiB | 3868.7 KiB | 2208.1 KiB |
| peak RSS | M5 | 179.9 MiB | 19.8 MiB | 174.4 MiB | 28.6 MiB |
| | container | 67.5 MiB | 14.2 MiB | 25.7 MiB | 25.0 MiB |
| compile (cold) | M5 | 116 ms | 49 ms | 114 ms | — |
| | container | 475 ms | 151 ms | 276 ms | — |

**The two hosts disagree about memory, and only one of them supports the
obvious story.** On the container, Kāra's 67.5 MiB against Rust's 25.7 MiB looks
like exactly what the tokenizer analysis predicts: ~400k owned token `String`s
live during every deserialize. On the M5, Rust sits at 174.4 MiB — within 3% of
Kāra — while C stays at 19.8 MiB, so whatever separates them there is not the
`Vec[String]`. Peak RSS is measured differently enough across the two platforms
(and Rust's allocator returns pages differently under each) that it should not
be read as corroborating the split-allocation finding. **The runtime ablation
and the split micro-benchmark do carry that finding; RSS does not, and this
table previously claimed it did.**

Binary size is the one row that is comparable in shape: Kāra's ~300 KiB sits
between C's tens of kilobytes and Go's ~2.4 MiB on both hosts.

## Running it

```bash
karac run  codec.kara
karac build codec.kara && ./codec
karac run  differential.kara              # agrees on all four surfaces
python3 codec.py
bash bench/bench.sh
```
