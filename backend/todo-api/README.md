# todo-api — read-only TODO list service

First entry in the **backend-service** kata category — closes axis-1
("Backend service") in `../../PLAN.md`. Status: **v1, dynamic `:id`
routing + POST echo.** One karac codegen prereq (`Json.stringify`
codegen-side wiring) remains before this kata reaches the full
PLAN.md Priority 1 spec.

## Routes

| Method | Path | Response |
|---|---|---|
| GET | `/todos` | 200, JSON array of all TODOs |
| GET | `/todos/:id` | 200 single TODO, or 404 for unknown / non-integer id |
| POST | `/echo` | 200, request body verbatim |
| any | other | 404 |
| non-GET non-POST | any | 405 |

## Running

```bash
karac build main.kara
./main             # binds 127.0.0.1:8080
curl http://127.0.0.1:8080/todos
curl http://127.0.0.1:8080/todos/2
curl -X POST -d '{"x":1}' http://127.0.0.1:8080/echo
```

## Kāra features exercised

- `std.http` `Server.serve(addr, handler)` with `Request.path()` / `method()` / `body()` round-trips.
- `match` over String scrutinee.
- Dynamic `:id` extraction via `String.starts_with` + `String.substring` + `i64.parse`.
- `Option[i64]` pattern-match destructuring, multi-route dispatch with status-code variation.

## What this kata does NOT exercise yet (and why)

The PLAN.md spec for Priority 1 calls for ~500–1000 LOC with full
CRUD (POST/PUT/DELETE) over an in-memory store and per-request JSON
serialization from `Vec[Todo]`. Two karac prerequisites remain:

1. **Module-level `let mut` bindings** —
   `karac-rust/docs/implementation_checklist/phase-8-stdlib-floor.md`,
   the entry directly above OnceLock/OnceCell. Required for the
   in-memory TODO store across handler calls; without it, write
   endpoints have nowhere to persist.

2. **`Json.stringify()` codegen dispatch** —
   `phase-8-stdlib-floor.md` next to the shipped `std.json`
   minimal-surface entry. Required to drop the static JSON strings
   and build responses from `Vec[Todo]` per request.

When both land, this kata grows into the full PLAN.md Priority 1
spec in-place — the static-response dispatch becomes the read path
of a real CRUD surface. The current dispatcher already does dynamic
`:id` extraction, so the routing layer is already final-shape.

## Comparison targets

Per PLAN.md axis-5, this kata needs a Go comparison for the v1
backend-shape compile-time public-quote number. Go + Rust
counterparts land as a follow-up commit (additive — the Kāra side
here is what needs to typecheck against the v1 stdlib surface).
