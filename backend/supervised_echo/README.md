# supervised_echo — error-cause branching over std.tcp

A backend-category kata that exercises **phase-8 line-74**: branching on
the *cause* of a network construction failure. It is the consumer that
drove the named `TcpError` variants (`AddrInUse` / `ConnectionRefused` /
`PermissionDenied`) into the compiler — before that work every failure
was `TcpError.Other(-1)`, and the two scenes below could not be written
correctly.

## Scenes

| Scene | Pattern | Cause branched on |
|---|---|---|
| 1. Port picker | bind the first free port in a range, stepping past taken ones | `TcpError.AddrInUse` → try next; `PermissionDenied` → stop |
| 2. Reconnect | retry a connection a bounded number of times while refused | `TcpError.ConnectionRefused` → retry; any other → fatal, give up |

Scene 1 occupies its own base port (18080) first, so the `AddrInUse`
fallback fires deterministically. Scene 2 targets a closed port (19099),
so every attempt is refused and the retry budget is exhausted.

## Running

```bash
# Build karac with the network surface (slices land on karalang/kara main):
#   TcpStream.connect (commit 0ed78d94) + named TcpError variants (c5b3e0f8)
KARAC_AUTO_PAR=0 karac build main.kara
./main
```

`KARAC_AUTO_PAR=0` is needed for **deterministic line ordering** — the
two scenes are independent, so the auto-parallelizer otherwise interleaves
their stdout. This is a feature demo, not an auto-par demo.

Expected output:

```
scene 1: AddrInUse-aware port picker
  occupied 18080; picker starts at 18080
  port 18080 in use — stepping to next
  bound port 18081
scene 2: ConnectionRefused-aware reconnect
  attempt 1: connection refused — retrying
  attempt 2: connection refused — retrying
  attempt 3: connection refused — retrying
  reconnect finished
```

## Kāra features exercised

- **`TcpStream.connect(addr) -> Result[TcpStream, TcpError]`** — the
  plain-TCP client (karac `0ed78d94`). Kāra could previously *accept* a
  TCP connection but not *initiate* one; this kata's scene 2 is the first
  consumer of the client surface.
- **Named `TcpError` construction-cause variants** (karac `c5b3e0f8`) —
  `AddrInUse` / `ConnectionRefused` / `PermissionDenied`, matched by name
  in both scenes. The runtime maps `std::io::ErrorKind` (platform-
  normalized) to a stable code that codegen decodes into the variant, so
  the kata never sees a raw, platform-specific errno number.
- **`Result` destructure with named + wildcard arms** — `match` over
  `Result.Ok` / `Result.Err(TcpError.X)` / `Result.Err(_)`.
- **Module-level effect propagation** — `connect` carries
  `sends(Network) receives(Network)`; `bind` is deliberately effect-free
  (local socket setup).

## Compiler limitations this kata surfaced

Per the kata-as-bug-finder discipline, the issues this workload exposed
(all pre-existing, all tracked on `karalang/kara`):

1. **`return;` in `main` fails codegen** (`ret void` vs main's `i32`
   exit-code ABI). Minimal repro: `fn main() { return; }`. Tracked in
   `phase-7-codegen.md`. Scene 2 uses a `done` flag instead of an early
   `return`.
2. **A network-yielding call (`connect` / `accept` / `read` / …) inside a
   *called* function produces no output** when driven by a plain call
   from `main` — the phase-6 effect-routed state-machine transform makes
   the helper a state machine the caller never drives. Tracked in
   `phase-6-runtime.md`. This is why scene 2's reconnect loop is inlined
   in `main` rather than factored into a `reconnect()` helper (scene 1's
   `pick_port` *can* be a helper only because `bind` is not
   network-yielding). When that lands, scene 2 factors out cleanly.
3. **Auto-par interleaves independent stdout** — the `KARAC_AUTO_PAR=0`
   requirement above; whether `println` should be a sequencing barrier
   under auto-par is a design question noted alongside limitation 2.

Once 1 and 2 land, this kata's natural shape is a `pick_port()` +
`reconnect()` pair of helpers, both with early `return`s.
