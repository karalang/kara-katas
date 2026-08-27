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
| [`B-2026-08-27-34`](../../../../kara/docs/bug-ledger.md) | **silent wrong answer**: 3454927 emits the branch-leaf retain once per *binding*, not per *use*, so the third read of the selected value returns garbage — and the binary exits `0` | open |
| [`B-2026-08-26-13`](../../../../kara/docs/bug-ledger.md) | `String.split` has no borrowing form — one allocation and one copy per token | relocated to the roadmap's `StringSlice` item |

### `differential.kara` is the live witness for B-2026-08-27-34

The three codec arms are byte-identical on all four surfaces — `karac run
--interp`, `karac run` (JIT), `karac build`, and `KARAC_AUTO_PAR=0 karac build`.
`differential.kara` is not: it prints `DIFFERENTIAL OK` under the interpreter and
aborts on both compiled backends.

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

The compiled binary **exits 0**. There is no abort and no diagnostic — only a
wrong number that differs run to run. Removing the `if` makes it green.

Notably, linking either form with `-fsanitize=address` runs **clean**, and
structurally so: the sanitizer is linked in, never compiled in, so it sees
allocator faults and cannot see a use-after-free *access* from the
uninstrumented Kāra object. That is why the compiler's ~1200-fixture ASAN corpus
never caught the class, and why the regression tests live in the ordinary E2E
harness instead.

## Benchmarks

Build one balanced 200,000-node tree, then 24 **chained** round trips —
serialize, hash the string, deserialize, repeat on the reconstruction. Chaining
matters: a deserializer that dropped or duplicated a subtree would drift the
string length and move the sink, which serializing the same original 24 times
would not notice. Sink: a polynomial hash over the bytes of every encoded
string, `checksum 397546302`, identical in all five languages.

Container x86-64, `results.container-x86.json`. See `../../../../BENCHMARKS.md`
for methodology and caveats.

| | mean | vs C |
|---|---|---|
| c (`-O3`) | 0.890 s | 1.00× |
| rust (`-O`) | 0.914 s | 1.03× |
| rust (`-O -C overflow-checks=on`, equal safety) | 0.919 s | 1.03× |
| go | 1.172 s | 1.32× |
| **kara** (codegen, seq) | **1.667 s** | **1.87×** |
| python | 11.176 s | 12.6× |

### Where the 1.9× goes, measured

Ablating the compiled Kāra binary one stage at a time (200k nodes, 24 rounds,
best of three):

| stage | time |
|---|---|
| serialize + hash, no deserialize | 0.66 s |
| serialize + deserialize, no hash | 1.32 s |
| all three | 1.64 s |

So **deserialize is ~1.0 s of it** — the majority, and effectively the whole
gap. It is not the tree building and not the string append.

Narrowed to a micro-benchmark (split a 3.2 MB comma-separated string 24 times):

| | time |
|---|---|
| C, split in place (no copies) | 0.02 s |
| Rust, `split(',').collect::<Vec<&str>>()` (borrowed) | 0.11 s |
| **Kāra, `s.split(",")`** | **0.47 s** |
| Rust, `split(',').map(String::from).collect()` (owned copies) | 0.71 s |

**Kāra's `split` is not slow — it beats Rust's same-semantics version by 1.5×.**
The gap is that `String.split` returns `Vec[String]`: one heap allocation and
one copy per token, with no slice-returning variant to reach for. C splits in
place, Rust and Go hand back views into the original buffer, and those are the
versions the other three arms are running. Python allocates copies as Kāra does
and is 12.6× slower than C, so this is the cost of the API *shape*, not of the
implementation behind it.

That is `B-2026-08-26-13`, now tracked on the roadmap's `StringSlice` item as
specified v1 behaviour with a v2 successor. It is not worked around here: the
kata keeps the idiomatic `s.split(",")` spelling, which is the whole point of
writing katas.

> The deserializer reads each token as `let tok = ref tokens[i];`. The
> borrow is not an optimisation for the benchmark's sake — since
> `E_INDEX_MOVE_NON_COPY` landed, `tokens[i]` on a non-`Copy` element is a hard
> error, and `ref` is the apt one of the three offered repairs for a read-only
> use. `karac fix` proposes `.clone()`, which also compiles and cost this lane
> 0.9 s: worth knowing that the machine-applicable fix is not always the right
> one.

### Elsewhere

| | kara | c | rust | go |
|---|---|---|---|---|
| binary size | 345.7 KiB | 16.0 KiB | 3868.7 KiB | 2208.1 KiB |
| peak RSS | 67.5 MiB | 14.3 MiB | 25.7 MiB | 24.3 MiB |
| compile (cold) | 350 ms | 124 ms | 230 ms | — |

Peak RSS tracks the same story: an owned `Vec[String]` of ~400k tokens is live
during every deserialize.

## Running it

```bash
karac run  codec.kara
karac build codec.kara && ./codec
karac run  --interp differential.kara     # compiled backends abort: B-2026-08-27-34
python3 codec.py
bash bench/bench.sh
```
