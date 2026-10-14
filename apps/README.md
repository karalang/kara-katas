# Apps

Two kinds of program live here.

- `prism/`, `veil/`, `cumulus/`: browser apps built to WASM by their own
  `build.sh` and deployed to karac.dev (see `DEPLOY.md`).
- `<kind>/<name>/`: application-shaped programs (services, command-line
  tools, data pipelines, object graphs) written against the v2 compiler.
  `<kind>` is `service`, `cli`, `pipeline` or `graph`. Many do real I/O:
  files on disk, child processes, a TCP server and its client over loopback.

## Layout of a `<kind>/<name>/` app

```
<name>.kara        the program
<name>.orig.kara   first draft, before v2 fixes (the diff is the friction record)
<name>.fixed.kara  the draft after `karac fix`, when `karac fix` was run on it
<name>.py          Python mirror: same algorithm and data, the oracle
expected.out       the mirror's stdout
README.md          what the app does, author errors versus compiler gaps, and
                   each workaround by ledger id (B-...)
app.toml           how the corpus runs it: expect, exit, tags, expected_from,
                   rules, backends, env
```

The README calls the files by their corpus names: `source.kara` is
`<name>.kara`, `source.orig.kara` is `<name>.orig.kara`, and so on.

## How an app reaches the compiler's tests

The kara repo keeps a copy of every app in `corpus/apps/<kind>/<name>/`,
because the corpus is its test suite: the M1/M2 gates and every corpus run
read it at a given compiler commit. The copy is made by

```bash
python3 scripts/corpus/extract.py --katas ../kara-katas --apps-only   # in kara/
```

(a full extract with `--katas` copies the apps too). It writes `source.kara`,
`source.orig.kara`, `source.fixed.kara`, the mirror, `expected.out` and
`notes.md`, and merges `app.toml` into `meta.toml`, keeping the keys the
corpus scripts own (class, bucket, legacy and model fields, notes). A
`source.kara` edited in the corpus since its last copy (classify's
`karac fix`, a migration) is kept and listed; `--overwrite-changed` replaces it.

So: change an app here first, push, then run the extract in kara and commit
the copy there. Compiler gaps an app finds go in the kara ledger
(`docs/bug-ledger.jsonl`) with source `example:<name>`, never worked around
silently: the README names each workaround and the row it waits on.

These apps are not in `scripts/surface-sweep.py` (it skips any directory
with an `app.toml`): their drafts do not compile by design, and their oracle
is the mirror, run by kara's `scripts/corpus/run.py --filter apps`.
