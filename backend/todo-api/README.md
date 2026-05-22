# todo-api — read-only TODO list service

First entry in the **backend-service** kata category — closes axis-1
("Backend service") in `../../PLAN.md`. Status: **v1, static
responses + POST echo.** Per-request JSON serialization, write
endpoints, and dynamic `:id` extraction wait on the karac prereqs
listed below.

## What's here

A minimal Kāra HTTP server with fixed responses:

```
GET  /todos      → 200 [{"id":1,"title":"Learn Kāra","completed":false}, ...]
GET  /todos/1    → 200 {"id":1,"title":"Learn Kāra","completed":false}
GET  /todos/2    → 200 {"id":2,"title":"Write a kata","completed":true}
GET  /todos/3    → 200 {"id":3,"title":"Ship slice 1","completed":true}
POST /echo       → 200 <request body verbatim>
GET  /anything   → 404 not found
non-GET non-POST → 405 method not allowed
```

Compile and run:

```bash
karac build main.kara
./main             # binds 127.0.0.1:8080
curl http://127.0.0.1:8080/todos
curl http://127.0.0.1:8080/todos/2
curl -X POST -d '{"x":1}' http://127.0.0.1:8080/echo
```

## What this kata exercises

- `std.http` server `Server.serve(addr, handler)` form (shipped
  2026-05-09)
- `Request.path()` / `Request.method()` / `Request.body()` round-trip
  — `body()` shipped 2026-05-21 as Slice 1 of the backend-kata
  unblock work; `POST /echo` validates the end-to-end body
  round-trip
- String literals with `\"` JSON-escape, multi-route dispatch,
  status-code variation

## What this kata does NOT exercise yet (and why)

The PLAN.md spec for Priority 1 calls for ~500-1000 LOC with full CRUD
(POST/PUT/DELETE) over an in-memory store, per-request JSON
serialization, and dynamic `:id` extraction. Five karac prerequisites
gate that target:

1. **Module-level `let mut` bindings** —
   `karac-rust/docs/implementation_checklist/phase-8-stdlib-floor.md`,
   the entry directly above OnceLock/OnceCell (commit `a9f3815`,
   2026-05-21). Required for the in-memory TODO store across handler
   calls.

2. **String typechecker arms** for `starts_with` / `substring` /
   `parse` —
   `karac-rust/src/typechecker/stdlib_seq.rs:165-168` notes that
   `len`/`contains`/`is_empty` etc. are "runtime-only and not yet
   wired through the typechecker." Required for dynamic `:id`
   extraction (`/todos/:id` where `:id` parses at runtime). v1 here
   enumerates `/todos/1..3` as fixed paths.

3. **`Json.stringify()` codegen dispatch** —
   `phase-8-stdlib-floor.md` line 431 says "runtime crate exposes the
   C-ABI exports for codegen-side wiring (deferred)." Surfaced
   2026-05-21 by this kata's build: `error: codegen failed: codegen:
   no handler for method 'stringify' on variable 'j'`. Workaround:
   static JSON strings baked into source. Required to drop the static
   strings and build responses from `Vec[Todo]` per request.

4. **`match` over a String scrutinee in codegen** — ✓ **shipped
   2026-05-21** as karac-rust commit `b763340`. Originally surfaced
   by this kata's build (panicked at
   `src/codegen/expr_ops.rs:1138` with `Found StructValue but
   expected IntValue`). Root cause was narrower than first framed
   — `compile_pattern_condition` was emitting only a `*const i8`
   for `LiteralPattern::String`, then `compile_binop(scrutinee_struct,
   pointer)` fell into the int path. Fix: build a full String struct
   for the literal pattern, both operands route through the existing
   `compile_string_binop` length-check + `memcmp` path. The route
   dispatcher in `main.kara` now uses the natural `match req.path()
   { ... }` form rather than the per-branch `if req.path() == "..."`
   chain.

5. **`Request.query()` / `.header()`** —
   `phase-7-codegen.md` line 266 calls these "deferred — additive
   when a real consumer needs them." Required for content-type
   negotiation, query-string filtering.

(3) is filed at `phase-8-stdlib-floor.md` (next to the shipped
`std.json` minimal-surface entry); (4) is filed AND shipped at
`phase-7-codegen.md` (commit `b763340`).

When the remaining four prereqs land, this kata grows into the full
PLAN.md Priority 1 spec in-place — the static-response dispatch
becomes the read path of a real CRUD surface, with `Vec[Todo]` +
JSON serialization + path-param extraction.

## Comparison targets

Per PLAN.md axis-5, this kata needs a Go comparison for the v1
backend-shape compile-time public-quote number. Go + Rust counterparts
land as a follow-up commit (additive — the Kāra side here is what
needs to typecheck against the v1 stdlib surface). For now, this
directory only carries `main.kara`.
