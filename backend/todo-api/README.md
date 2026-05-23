# todo-api — CRUD TODO list service

First entry in the **backend-service** kata category — closes axis-1
("Backend service") in `../../PLAN.md`. Status: **v2, full CRUD over
an in-memory store with per-request `Json.stringify`.** Shipped
2026-05-22 after the two karac slices that unblocked the planned
shape (`Vec.new()` at module scope + uppercase-receiver method
dispatch).

## Routes

| Method | Path | Status | Body |
|---|---|---|---|
| GET | `/todos` | 200 | JSON array of all TODOs |
| GET | `/todos/:id` | 200 / 404 | Single TODO, or "not found" |
| POST | `/todos` | 201 / 400 | Created TODO (auto-id), or error |
| PUT | `/todos/:id` | 200 / 400 / 404 | Updated TODO, or error |
| DELETE | `/todos/:id` | 204 / 404 | Empty body on success |
| any | other | 404 | "not found" |
| non-supported method | any | 405 | "method not allowed" |

## Running

```bash
karac build main.kara
./main             # binds 127.0.0.1:8080
curl http://127.0.0.1:8080/todos
curl http://127.0.0.1:8080/todos/2
curl -X POST -d '{"title":"From curl","completed":false}' http://127.0.0.1:8080/todos
curl -X PUT  -d '{"title":"Updated","completed":true}' http://127.0.0.1:8080/todos/1
curl -X DELETE http://127.0.0.1:8080/todos/2
```

## Kāra features exercised

- **Module-level mutable state**: `let mut TODOS: Vec[Todo] = Vec.new();`
  + `let mut NEXT_ID: i64 = 1;` per design.md §1278-1330. Slice-a
  (karac-rust `d92f3da`) wired `Vec.new()` into the const-init
  permitted special forms; the global is emitted as the canonical
  `{ptr null, i64 0, i64 0}` LLVM aggregate and grows on `push`.
- **Uppercase-receiver method dispatch**: `TODOS.push(t)`,
  `TODOS.len()`, `TODOS[i]`, `TODOS[i] = ...`, `TODOS.pop()` all
  dispatch correctly through the typechecker + lowering + codegen
  rewrite shipped karac-rust `f41a62c`. Without that fix, every
  method call against an uppercase global Vec failed with
  `type 'Vec[i64]' is not callable`.
- **`std.http` server**: `Server.serve(addr, handler)` with a
  per-request handler taking `Request` and returning `Response`.
  `req.method()`, `req.path()`, `req.body()` all round-trip through
  the FFI to hyper.
- **`std.json` per-request serialization**: every response body is
  built from a `Json` value tree via `Json.Object` / `Json.Array` /
  `Json.Number` / `Json.String` / `Json.Bool` and rendered with
  `j.stringify()`. Incoming bodies are parsed with `Json.parse(...)`
  and pattern-matched against the variant.
- **Dynamic `:id` extraction**: `String.starts_with` +
  `String.substring` + `i64.parse` + `Option`-match on the result.
- Multi-route dispatch with status-code variation (200, 201, 204,
  400, 404, 405).

## v1 karac gaps the kata surfaced (all fixed)

All four karac codegen gaps the kata bridged with inline
workarounds at Slice 4 ship time have shipped fixes in karac.
The kata is now back to its natural shape — JSON construction
uses `Vec[a, b, c]` literals at variant payload position,
`extract_completed` reads the bool directly, DELETE uses
`Vec.remove(idx)` and preserves order.

| Gap | Fix |
|---|---|
| Enum-payload bool narrowing — `match Json.Bool(b) => b` LLVM verifier rejection | karac `11ca0e1` |
| `Vec.remove(idx)` doesn't shrink the Vec | karac `4de2e8e` |
| `Vec[a, b, c]` literal codegen — `PrefixCollectionLiteral` has no compile arm | karac `540cd8c` |
| Field-receiver method GEP through a `ref T` parameter | karac `32f52d2` |

One small style choice the kata makes: JSON construction lives
inline in each handler rather than factored into a
`todo_to_json(t: ref Todo) -> Json` helper. The helper compiles
clean and works in isolation, but inside the Server-frame handler
context — combined with the `match Json.parse(req.body())` outer
binding and the per-request lifetime — exposes a separate
ownership/drop interaction that crashes the response write. The
shape is narrower than today's known gaps and would file as a
separate follow-up; the inline JSON in each handler is short
enough that the missing helper isn't load-bearing for the kata's
demo value.

## Numbers

- LOC: ~250 (main.kara), up from ~110 in the v1 read-only shape.
- Compile time: <1s on M5 Pro (clean build of just `main.kara`
  against the installed karac).
- Binary size: ~720 KiB.

## Architecture notes

- **State is global, not per-request**: every handler call mutates
  the same `TODOS` Vec under `Server.serve`'s single-threaded
  dispatch (v1 server semantics — no concurrent handlers). Once
  multi-thread serving lands, the binding will need either
  `Mutex[Vec[Todo]]` (per design.md §1326 path (a)) or the
  `public_effects = "inferred"` project flag (path (b)).
- **`NEXT_ID` is monotonically increasing**: deleted ids are NOT
  reused. A POST after `DELETE /todos/2` gets id 4 (the next
  unused), not id 2.
- **Body parsing is two-pass**: the kata calls `Json.parse(req.body())`
  twice per write request — once for `title`, once for `completed`.
  This is a v1 pragma because the v1 JSON enum's `Object` payload
  is a `Vec[(String, Json)]` and the elements move on the first
  extraction. A single-pass extractor lands when the same
  follow-on Vec[Json] codegen lands.

## Comparison targets

Per PLAN.md axis-5, this kata needs Go and Rust comparison
counterparts for the v1 backend-shape compile-time public-quote
number. They land as additive commits — the Kāra side here is
what needs to typecheck against the v1 stdlib surface, which it
now does.
