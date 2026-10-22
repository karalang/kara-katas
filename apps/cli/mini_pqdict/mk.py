#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_pqdict (tab-separated: op then arg).

A stream of indexed-priority-queue sessions. Each `new` starts a fresh queue
(min = smallest value is highest priority, max = largest); the ops that follow
act on it:

  new <min|max>     start a new queue
  set <key> <val>   __setitem__: add key, or update its priority if present
  add <key> <val>   additem: add; ERR if key already present
  upd <key> <val>   updateitem: change priority; ERR if key absent
  del <key>         remove key; ERR if absent
  pop               remove & print the highest-priority item ("key val"); ERR if empty
  top               print the highest-priority item without removing; ERR if empty
  get <key>         print key's priority value; ERR if absent
  has <key>         print yes/no
  len               print the item count
  pushpop <k> <v>   insert then pop the top in one step ("key val"); ERR if key present
  swap <k1> <k2>    swap_priority: exchange the priorities of two keys; ERR if either absent
  rekey <old> <new> replace_key: rename a key in place; ERR if old absent or new present
  drain             pop every item in priority order, print "key:val" space-joined

Only the printing ops emit a line. mk.py writes only literal inputs (no library
import); oracle.py replays every job against the vendored `pqdict` library.
Keys and values are ASCII. See README.md."""
import os

os.makedirs("data", exist_ok=True)

SESSIONS = [
    # min-pq used as a Dijkstra frontier: insert, decrease-key, pop in order
    ("min",
     [("set", "a", 10), ("set", "b", 5), ("set", "c", 8), ("set", "d", 20),
      ("top",), ("len",), ("upd", "d", 3), ("top",), ("set", "b", 1),
      ("pop",), ("pop",), ("get", "c"), ("has", "b"), ("has", "z"),
      ("set", "e", 4), ("set", "f", 4), ("set", "g", 4), ("drain",)]),
    # max-pq task scheduler: higher value runs first; pushpop and swap
    ("max",
     [("add", "low", 1), ("add", "mid", 5), ("add", "high", 9),
      ("top",), ("pushpop", "urgent", 10), ("pushpop", "trivial", 0),
      ("top",), ("swap", "low", "mid"), ("get", "low"), ("get", "mid"),
      ("len",), ("drain",)]),
    # errors and recovery on an empty / small queue
    ("min",
     [("pop",), ("top",), ("get", "x"), ("del", "x"), ("upd", "x", 1),
      ("add", "x", 7), ("add", "x", 9), ("has", "x"), ("set", "x", 2),
      ("get", "x"), ("pushpop", "x", 0), ("len",), ("pop",), ("pop",)]),
    # rekey / swap edge cases and ties
    ("min",
     [("set", "p", 3), ("set", "q", 3), ("set", "r", 3), ("set", "s", 1),
      ("rekey", "p", "p2"), ("has", "p"), ("has", "p2"), ("get", "p2"),
      ("rekey", "q", "r"), ("rekey", "zz", "yy"), ("swap", "s", "p2"),
      ("get", "s"), ("get", "p2"), ("drain",)]),
    # a longer min session: repeated updates to the same key, interleaved pops
    ("min",
     [("set", "n0", 50), ("set", "n1", 40), ("set", "n2", 30), ("set", "n3", 20),
      ("set", "n4", 10), ("upd", "n0", 5), ("upd", "n1", 45), ("pop",),
      ("upd", "n2", 2), ("pop",), ("set", "n5", 1), ("pop",), ("pop",),
      ("len",), ("pop",), ("pop",), ("pop",)]),
    # single-element and immediate drain
    ("max",
     [("set", "only", 42), ("top",), ("len",), ("drain",), ("drain",),
      ("set", "a", 1), ("set", "b", 2), ("del", "a"), ("drain",)]),
]

lines = []
for mode, ops in SESSIONS:
    lines.append("new\t%s" % mode)
    for op in ops:
        if len(op) == 1:
            lines.append(op[0])
        elif len(op) == 2:
            lines.append("%s\t%s" % (op[0], op[1]))
        else:
            lines.append("%s\t%s %s" % (op[0], op[1], op[2]))

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
