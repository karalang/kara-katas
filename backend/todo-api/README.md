# todo-api — read-only TODO list service

First entry in the **backend-service** kata category — closes axis-1
("Backend service") in `../../PLAN.md`. Status: **v1, dynamic `:id`
routing + POST echo.** One karac codegen prereq (`Json.stringify`
codegen-side wiring) remains before this kata reaches the full
PLAN.md Priority 1 spec.

## What's here

A minimal Kāra HTTP server with dynamic path-param extraction:

```
GET  /todos       → 200 [{"id":1,"title":"Learn Kāra","completed":false}, ...]
GET  /todos/1     → 200 {"id":1,"title":"Learn Kāra","completed":false}
GET  /todos/2     → 200 {"id":2,"title":"Write a kata","completed":true}
GET  /todos/3     → 200 {"id":3,"title":"Ship slice 1","completed":true}
GET  /todos/42    → 404 not found  (any unknown integer id)
GET  /todos/abc   → 404 not found  (any non-integer suffix)
POST /echo        → 200 <request body verbatim>
GET  /anything    → 404 not found
non-GET non-POST  → 405 method not allowed
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
- `Request.path()` / `Request.method()` / `Request.body()`
  round-trips — `body()` shipped 2026-05-21 as Slice 1 of the
  backend-kata unblock work; `POST /echo` validates the end-to-end
  body round-trip
- `match` over String scrutinee (shipped 2026-05-21)
- `String.starts_with` + `String.substring` + `i64.parse` —
  dynamic `:id` extraction (all shipped 2026-05-21)
- String literals with `\"` JSON-escape, multi-route dispatch,
  status-code variation, `Option[i64]` pattern-match destructuring

## What this kata does NOT exercise yet (and why)

The PLAN.md spec for Priority 1 calls for ~500-1000 LOC with full
CRUD (POST/PUT/DELETE) over an in-memory store and per-request JSON
serialization from `Vec[Todo]`. Two karac prerequisites remain:

1. **Module-level `let mut` bindings** —
   `karac-rust/docs/implementation_checklist/phase-8-stdlib-floor.md`,
   the entry directly above OnceLock/OnceCell (commit `a9f3815`,
   2026-05-21). Required for the in-memory TODO store across handler
   calls. Without it, write endpoints (POST/PUT/DELETE) would have
   nowhere to persist their changes.

2. **`Json.stringify()` codegen dispatch** —
   `phase-8-stdlib-floor.md` next to the shipped `std.json`
   minimal-surface entry. Required to drop the static JSON strings
   and build responses from `Vec[Todo]` per request via
   `Json.Array([...]).stringify()`.

(The earlier four gaps — `String == String` ownership rule, match
over String scrutinee, String typechecker arms, and `Request.body()`
— are all shipped.)

When the remaining two prereqs land, this kata grows into the full
PLAN.md Priority 1 spec in-place — the static-response dispatch
becomes the read path of a real CRUD surface, with `Vec[Todo]` +
JSON serialization. The current dispatcher already does dynamic
`:id` extraction, so the routing layer is already final-shape.

## Comparison targets

Per PLAN.md axis-5, this kata needs a Go comparison for the v1
backend-shape compile-time public-quote number. Go + Rust
counterparts land as a follow-up commit (additive — the Kāra side
here is what needs to typecheck against the v1 stdlib surface). For
now, this directory only carries `main.kara`.
