# parallel-or-not

**Question:** in this function, which calls can run concurrently?

```kara
pub fn handle_request()
    with writes(Db) writes(Cache) writes(Log)
{
    persist_order();   // 0
    warm_cache();      // 1
    emit_audit();      // 2
    update_ledger();   // 3
}
```

Four calls. The honest answer is **0, 1, and 2 can run in parallel; 3 cannot** — `update_ledger` and `persist_order` both `writes(Db)`, so they touch the same resource and must stay ordered. Run the other three concurrently and you keep correctness; run all four and you race the database.

Nothing in `handle_request` tells you that. Nothing in the *names* tells you that. The conflict lives in the `writes(Db)` annotation on two functions defined further down the file — and in a real codebase, those annotations are spread across modules, behind trait impls, and transitively inferred. This single file is the *minimal* version of a question that gets harder, not easier, at scale.

## Two ways to answer it

**Inference** — read the source and reason it out. This is what a human reviewer does, and what an LLM does when you ask it. It works on small examples and degrades as the effect graph grows; it's probabilistic (it can be confidently wrong) and non-reproducible (re-ask and you may get a different grouping). You cannot put "the model thought these were independent" in a CI gate.

**Deduction** — ask the compiler, which already resolved the full effect-conflict graph in order to typecheck the program:

```console
$ karac query concurrency main.kara.handle_request
{"function":"handle_request","total_statements":4,
 "parallel_groups":[{"statements":[0,1,2],
   "reason":"independent effects on different resources"}]}
```

Statements `[0,1,2]` group; `3` is excluded. Sound, total, and byte-identical every time you run it. This isn't the compiler *guessing better than the LLM* — it's the compiler returning a fact it had to compute anyway, versus an inference that has to be reconstructed and trusted.

The exclusion is visible in the effect surface the grouping is derived from:

```console
$ karac query effects main.kara.persist_order
{"function":"persist_order","inferred_effects":[{"verb":"writes","resource":"Db"}], ...}

$ karac query effects main.kara.update_ledger
{"function":"update_ledger","inferred_effects":[{"verb":"writes","resource":"Db"}], ...}
```

Same resource, `Db` — so statements 0 and 3 carry a conflict edge and never share a group.

## A second axis — shared *values*, not just shared resources

A hidden effect conflict is one reason two statements can't parallelize. There's a second, and the compiler accounts for both: an ordinary **data dependency**. The concurrency graph is the *union* of an effect-conflict graph and a dataflow-dependency graph (read-after-write, write-after-read, and write-write over local bindings). A pair serializes if *either* graph says so.

`dataflow.kara` isolates this axis. All three stages write **fully disjoint** resources (`Db`, `Cache`, `Log`), so on effects alone all three would group. The only variable is whether one statement reads a value another produced:

```kara
pub fn handle()        // stmt 1 READS r
    with writes(Db) writes(Cache) writes(Log)
{
    let r = stage_a();   // 0: defines r, writes Db
    stage_b(r);          // 1: reads r,   writes Cache
    stage_c();           // 2:            writes Log
}

pub fn handle_indep()  // identical effects, stmt 1 ignores r
{
    let r = stage_a();   // 0
    stage_b(0);          // 1: no read of r
    stage_c();           // 2
}
```

```console
$ karac query concurrency dataflow.kara.handle
{... "parallel_groups":[{"statements":[1,2], ...}]}      # stmt 0 excluded

$ karac query concurrency dataflow.kara.handle_indep
{... "parallel_groups":[{"statements":[0,1,2], ...}]}    # all three group
```

The effects are **byte-identical** between the two functions — `query effects` returns the same three `writes` for both. The only difference is the read of `r`, and it flips the grouping from `[0,1,2]` to `[1,2]`. Statement 0's `Db` write conflicts with nothing; the *sole* reason it's pulled out is the read-after-write dependency. That's the dataflow axis, demonstrably independent of effects. (Same contiguous-greedy mechanism as before: stmt 0 becomes a singleton because the next statement depends on it, then 1 seeds a fresh group with 2.)

So the full claim is: **the parallel grouping is sound against both shared resources and shared values, simultaneously** — and an inference-only reader has to track both graphs at once to match it.

> One current limitation, stated plainly: the `reason` string reads `"independent effects on different resources"` even when a value dependency (not an effect) was the operative cause of an exclusion. It describes why the *grouped* statements belong together, but the query does not yet attribute *which axis* excluded a given statement. Richer per-statement attribution is tracked as a follow-up in the compiler's `phase-5-diagnostics` checklist.

## Why this is the interesting shape for agent tooling

An agent doing autonomous code work is good at inference and bad at *certainty*. Pairing it with a deterministic, sound oracle covers exactly that weakness: the agent proposes a parallelization or a refactor, and `query concurrency` *proves* whether it's race-free — the same way a type checker proves a type, instead of "the reviewer will probably catch it." The result is reproducible, so it can live in a pipeline and be regression-tested; an LLM's reading cannot.

Scope honesty: this oracle helps an agent operating *on* existing Kāra — analyze, verify, refactor. It does not help the agent *write* Kāra in the first place (a young language has little training data). And the premise that ground-truth semantics beat a good-enough guess is a bet about how agents will work — this kata exists to make that bet concrete and falsifiable, not to assert it. If the contrast feels thin to you here, that's a real signal.

## Reproduce

```console
$ karac check main.kara
All checks passed.

$ karac build main.kara && ./main
done

$ karac query concurrency main.kara.handle_request
```

Then change the annotations and watch the answer move deterministically:

- Give `update_ledger` its own distinct resource instead of `Db` (e.g. a new `effect resource Mq: Store;`) and statement 3 joins the group — `parallel_groups` becomes `[0,1,2,3]`. The conflict is gone, so all four run concurrently.
- Make *every* stage `writes(Db)` and `parallel_groups` becomes `[]` — fully sequential, because now everything conflicts with everything.

The grouping tracks the effect graph exactly. (Both results above are what `karac query concurrency` actually returns on those edits — verified, not predicted.)

---

*The narrative framing for any launch/marketing use of this kata is intentionally left for the language author to write; this README is the verified technical demonstration only.*
