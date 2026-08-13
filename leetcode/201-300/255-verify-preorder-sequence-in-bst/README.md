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
