#!/usr/bin/env python3
"""Writes data/jobs.tsv: operations on an HTTP/2 priority tree that both
oracle.py and the Kara port run through the `priority` library.

A job is one tab-separated line; field 0 names the kind. State persists from
one line to the next until the next `tree` line resets it.

  tree    <max_streams>                 start a fresh PriorityTree
  insert  <id> <depends_on|-> <weight> <excl 0|1>   insert_stream
  reprio  <id> <depends_on|-> <weight> <excl 0|1>   reprioritize
  remove  <id>                          remove_stream
  block   <id>                          block
  unblock <id>                          unblock
  sched   <count>                       pull `count` stream ids from next()

A mutation prints `ok` or `err=<message>`; a `sched` prints the list of ids
pulled (and, if the tree deadlocks, the DeadlockError message).
"""
import os

os.makedirs("data", exist_ok=True)

JOBS = r"""
tree	1000
insert	1	-	16	0
insert	3	-	16	0
insert	5	-	16	0
sched	9
tree	1000
insert	1	-	32	0
insert	2	-	16	0
insert	3	-	8	0
sched	14
tree	1000
insert	1	-	16	0
insert	3	1	16	0
insert	5	1	16	0
block	1
sched	8
unblock	1
sched	4
tree	1000
insert	1	-	16	0
insert	3	-	16	0
insert	5	1	16	1
sched	6
tree	1000
insert	1	-	16	0
insert	3	-	16	0
insert	5	-	16	0
reprio	5	1	16	1
sched	6
tree	1000
insert	1	-	16	0
insert	3	1	16	0
insert	5	3	16	0
remove	3
sched	6
tree	1000
insert	1	-	200	0
insert	3	-	100	0
reprio	1	3	64	0
sched	10
tree	1000
insert	1	-	16	0
insert	1	-	16	0
tree	1000
reprio	9	-	16	0
tree	1000
remove	9
tree	1000
block	9
tree	1000
reprio	0	-	16	0
tree	1000
remove	0
tree	1000
block	0
tree	1000
insert	1	1	16	0
tree	1000
insert	1	-	0	0
tree	1000
insert	1	-	257	0
tree	2
insert	1	-	16	0
insert	3	-	16	0
tree	1000
insert	1	-	16	0
insert	3	-	16	0
block	1
block	3
sched	3
tree	1000
insert	7	4	16	0
sched	4
"""

with open("data/jobs.tsv", "w") as f:
    f.write(JOBS.lstrip("\n"))

print("jobs:", len(JOBS.strip().splitlines()))
