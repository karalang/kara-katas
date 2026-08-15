# 255. Verify Preorder Sequence in Binary Search Tree

Given a sequence of **distinct** integers, could it be the preorder traversal of
some BST? No tree is ever built — the question is answerable from the sequence.

```
[5,2,1,3,6] -> true       [5,2,6,1,3] -> false
[1,3,2]     -> true       [2,3,1]     -> false
```

**Constraints:** `1 ≤ preorder.length ≤ 10⁴`; values are distinct and fit in
`i64`.

## Approaches

| file | idea | time | extra space |
|---|---|---|---|
| `verify_preorder.kara` ★ | ancestor stack + rising lower bound | O(n) | O(n) |
| `verify_preorder_inplace.kara` | the input array **is** the stack | O(n) | **O(1)** |
| `verify_preorder_divide.kara` | recursive split with bound flags | O(n²) worst | O(depth) |
| `differential.kara` | 6,000 randomized sequences, all three agree | — | — |

## The mechanism

**Stepping right is irreversible.** Reading a preorder left to right you descend
leftwards while values shrink; the moment a value *rises* above something already
seen, you have entered that node's right subtree — and every remaining value must
exceed it, forever. So carry a lower bound and a stack of ancestors whose right
subtree has not yet been entered:

- a value below the bound is impossible → reject;
- a value above the stack top means we just stepped right, so pop and raise the
  bound (repeatedly — one value can close several levels at once);
- push the value as the newest ancestor.

**The bound only ever rises, and that is the whole proof.** Once raised past a
value, nothing smaller can legally appear again.

**The in-place variant works because the stack is always a prefix of what has
already been read.** So the input can be the stack: `top <= i` holds at every
step, and the overwrite can never clobber an unexamined value. That is the whole
safety argument — and it is why the trick does not generalise to algorithms whose
stack can outgrow the prefix. The cost is that the input is destroyed, which
Kāra makes explicit in the signature (`mut Slice[i64]`) and at the call site.

**The divide-and-conquer file is the differential's reference** because it rests
on nothing but the definition: preorder = root, then the contiguous block below
it, then the block above. The other two rest on an argument about a monotonically
rising bound.

## A sentinel that would have been wrong

The recursive form needs "no bound yet" at the root. Using `i64.MIN` as that
sentinel is the obvious move and it is **incorrect here**: `i64.MIN` is itself a
legal input value, so an unbounded position becomes indistinguishable from one
bounded at the extreme. The file carries `has_min` / `has_max` flags instead —
four more parameters, no ambiguity, and no silent narrowing of the domain.
`[i64.MIN, 5]` is in every solver's tests for exactly this.

(The two stack forms *do* use `i64.MIN` as the initial bound, and are safe doing
so only because their test is strict: `x < lower` accepts a genuine `i64.MIN`.
A `<=` there would reject it.)

## What the differential found: duplicates are out of spec

The first generator drew its uniform-random family without deduplicating. One
case in 6,000 disagreed:

```
[875, 160, 875, 859]     stack=true   inplace=true   divide=false
```

`875` appears twice. The divide-and-conquer rejects it because its bounds are
**exclusive** — a right-subtree value equal to its root is impossible in a BST
with distinct keys. The two stack forms accept it because their tests are strict.
**Neither is wrong**; the input is outside the stated domain, and the problem is
ill-posed on it.

LeetCode specifies distinct integers, so the fix went to the generator, not to
any decider. It is recorded because the divergence is invisible in the code: three
implementations that agree on every valid input can still disagree the moment the
precondition is dropped, and only the one written from the definition notices.

This is the second time in this stretch that a generator wandered out of spec and
the differential caught it — [#252](../252-meeting-rooms/) did the same with
zero-length intervals. Both times the *definitional* implementation was the one
that flagged it.

## Generator design

A uniform random array is almost never a valid preorder — the first out-of-order
value rejects it — so a naive generator tests nothing but the early exit. Three
families instead:

- **valid** (~half) — an actual random BST is built and traversed, so the
  sequence is correct by construction. Without these the accept path is dead
  code.
- **perturbed** — a valid sequence with one pair swapped, so rejection happens
  *late* and stresses the bound logic rather than the first comparison.
- **random** — the uniform draw (distinct), keeping the fast-reject path covered.

Over 6,000 cases: **4,606 accepted, 1,394 rejected, 32,551 elements.**

**Each decider gets its own freshly generated copy.** The in-place variant
destroys its input; sharing one buffer would have the second and third deciders
reading scratch data and agreeing with each other for the wrong reason — a
differential that validates nothing.

## Benchmark

`bench/` builds a random BST over **200,000 distinct keys once**, traverses it to
a **valid** preorder, then runs **250 rounds** of full ancestor-stack
verification. Sink `200000 302714266`, reproduced by all four mirrors.

Two choices keep it measuring the verifier:

- **The sequence must be valid.** A rejecting input returns at the first
  violation, so benching one would time how quickly a counterexample appears —
  a property of the generator, not the algorithm.
- **Keys are inserted shuffled**, giving a random BST of depth ~2·log₂(n).
  Sorted insertion would give a right spine whose preorder is strictly increasing
  and which pops on *every* element — degenerate, exercising the pop loop and
  nothing else.

The kernel is the ★ stack form rather than the in-place variant, which destroys
its input and would need a fresh copy per round — measuring the copy alongside
the algorithm.

### Runtime — sequential lane

Apple M5 Pro (6P+12E), 2026-08-15, `karac 0.1.0-dev.6106+g50267795a`, hyperfine
30 runs, `KARAC_AUTO_PAR=0`, every lane 99% CPU. This is the canonical host —
`bench/results.json`.

| Impl | Mean ± σ | vs Kāra |
|---|---|---|
| C `clang -O3` | 188.6 ± 7.1 ms | 0.93× |
| Rust `-O` | 195.1 ± 6.1 ms | 0.96× |
| **Kāra (codegen)** | **202.9 ± 2.6 ms** | 1.00× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 209.5 ± 2.2 ms | 1.03× |
| Go | 226.1 ± 4.8 ms | 1.11× |

**Kāra sits between wrapping and checked Rust, which is the honest place for it**
— 202.9 ms against 195.1 and 209.5. It leads equal-safety Rust by 3% and trails
C by 8%, and the full spread across five languages is 1.20×. Note that σ here is
1.1–3.8%, against the container's 5–21%: this host actually resolves the lane.

**The container had Kāra first; the M5 has it third, and neither is a change.**
The container's top three (Kāra 437.9, C 446.8, Rust 500.5) sat inside σ of 25–42
ms — the ordering was never real. Here the same three separate cleanly in a
different order. What survives both hosts is the claim the section below makes:
on a `Vec`-push/pop-dominated workload Kāra is level with the systems languages,
within 8% of C in one direction and ahead of equal-safety Rust in the other.

That matters against the sort story elsewhere in this corpus. The ancestor stack
does one push and at most one pop per element, and Kāra tracks C on it — while
[#252](../252-meeting-rooms/) and [#253](../253-meeting-rooms-ii/), which are
sort-dominated, are 3.70× and 2.04× behind Rust on this same host. kara
`B-2026-08-11-28` records the sort residual as an accepted cost; nothing here
suggests a general codegen gap, which is consistent with that row's scope.

### The x86 corroboration run

Container x86-64, `bench/results.container-x86.json` — corroboration only
(BENCHMARKS.md § Hosts).

| lang | mean (ms) | vs Rust |
|---|---|---|
| **Kāra** | **437.9 ± 25.3** | **0.87×** |
| C | 446.8 ± 24.5 | 0.89× |
| Rust | 500.5 ± 42.4 | 1.00× |
| Go | 531.6 ± 112.3 | 1.06× |
| Rust (checked) | 534.2 ± 23.2 | 1.07× |

**Kāra and C are tied there**, not ranked — 437.9 against 446.8 with error bars
that overlap almost entirely. **Go's row is unusable**: σ = 112.3 ms, 21% of its
own mean, an order of magnitude noisier than everything else in that table. Both
observations are why the M5 lane above is the published one.

## What it found: kara `B-2026-08-11-35`

Not a compiler bug — a **tooling** one, and it destroyed source.

The in-place variant takes `mut Slice[i64]`, and its reporting helper forwards
that into an f-string: `println(f"{label} -> {verify_preorder(mut preorder)}")`.
The typechecker correctly reported *"already a mut-ref; drop the `mut` marker"* —
a four-character deletion. `karac fix`, which CLAUDE.md designates as the primary
fix path for machine-applicable diagnostics, printed `applied 1 fix(es)`, exited
0, and turned this file from ~80 lines into 31 with line 1 mangled.

The replacement span for a fix inside an **f-string interpolation** was applied
at the wrong file offset — landing near the top of the file and truncating
mid-token. No backup, no dry-run, success reported.

Minimised to five lines and filed; **fixed upstream in `35d7fec`**, and verified
here against the original repro. The obvious first guess — multi-byte UTF-8
offsets, since this file is full of em-dashes — was **wrong**: ASCII-only files,
files with em-dashes near the site, and files with 30 em-dash comment lines
before it all fixed correctly. The f-string hole was the single distinguishing
factor.

## Kāra features exercised

- **`mut Slice[i64]` as a consumed scratch buffer**, with the mutation announced
  at the signature and marked at the call site.
- **Index-pool BST construction** inside the generator (parallel `val`/`left`/
  `right` vectors), then an iterative preorder walk with an explicit stack.
- **A 7-parameter recursion** carrying paired value/validity flags — the
  alternative to an in-band sentinel.
- **`i64.MIN` written as `-9223372036854775807i64 - 1i64`**, since the literal
  `-9223372036854775808` is the negation of an out-of-range positive.

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`; the two with
mirrors match Python.

No compiler bugs found in the solvers. The one mismatch the differential reported
was checked against the compiler first — interpreter and AOT gave the identical
count and digest — which ruled out codegen before the algorithms were examined.

## Running

```bash
karac run verify_preorder.kara
karac run verify_preorder_inplace.kara
karac run verify_preorder_divide.kara

diff <(karac run verify_preorder.kara) <(python3 verify_preorder.py) && echo OK
diff <(karac run verify_preorder.kara) <(karac run verify_preorder_inplace.kara) && echo OK
diff <(karac run verify_preorder.kara) <(karac run verify_preorder_divide.kara) && echo OK

# 6,000 randomized sequences, three deciders cross-checked, mirrored in Python
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

# run == build, on every program
for f in verify_preorder verify_preorder_inplace verify_preorder_divide differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```
