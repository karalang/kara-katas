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

## Known v1 karac gaps (worked around inline)

Two karac codegen surfaces still have v1 gaps that this kata bridges
with inline workarounds; each is filed as a follow-on slice in
`karac-rust/docs/implementation_checklist/phase-8-stdlib-floor.md`.
The kata's response shapes are correct end-to-end; the implementation
style is uglier than it would be once the underlying gaps land.

Two earlier gaps in this list have shipped and the kata is back to
the natural shape for those — see the "Resolved" subsection below.

1. **`Vec[a, b, c]` literal codegen — `PrefixCollectionLiteral` has
   no compile arm.** `Json.Array(Vec[a, b])` parses, the binary
   builds, but the literal evaluates to a null Vec at runtime
   (codegen's `compile_expr` falls through to `i64 0` for
   `PrefixCollectionLiteral`). Workaround: explicit `Vec.new() +
   .push(...)` wherever a Vec value is needed at expression
   position. Affects every use site, not just enum-variant
   payloads; the standalone `let xs: Vec[i64] = Vec[1, 2, 3];`
   form is also broken.
2. **Helper-function `Json` construction silently fails when
   chaining `ref Todo` + `t.title.clone()` into a variant payload.**
   The minimal `fn build() -> Json { Json.Array(items) }` shape
   works; the failure mode is the specific shape that takes
   `t: ref Todo`, calls `t.title.clone()` through the ref, and
   embeds the clone in a Json variant payload returned to the
   caller. The kata's response handlers build their Json inline
   rather than extracting `todo_to_json(t)` helpers — the inline
   form is verified correct.

### Resolved

These were on the gap list at Slice 4 ship time and have since
been fixed in karac:

- **`match Json.Bool(b) => b` LLVM-verifier rejection** — fixed
  karac `11ca0e1`. The bool-narrowing trunc is now inserted at
  pattern reconstruction time, so `extract_completed` returns
  the bool directly without the prior `as i64` / `!= 0i64`
  cast workaround.
- **`Vec.remove(idx)` doesn't shrink the Vec** — fixed karac
  `4de2e8e`. DELETE now uses `TODOS.remove(idx)` directly and
  preserves element order across deletes (replacing the prior
  swap-with-last + `pop()` workaround that scrambled order).

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
