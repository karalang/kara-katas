"""Writes data/ for mini_rq: a script for a small job queue with three
priority queues, a pool of workers, dependencies, retries with and without
backoff, timeouts, scheduled jobs, cancelling, requeueing and expiring
results, with a few mistakes.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)


def put(name, text):
    with open(os.path.join("data", name), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


put("script.txt", """\
# Queues are listed by priority: a round takes the high jobs first.
queue high
queue default
queue low

enqueue default add1 add 2 3
enqueue default fib30 fib 30
enqueue low count words the quick brown fox jumps ttl=50
enqueue high page echo wake up the oncall
enqueue default report echo report ready depends_on=add1,fib30
enqueue default flaky1 flaky 3 retry=3
enqueue default flaky2 flaky 4 retry=2 backoff=10,30
enqueue default slow1 slow 200 timeout=120
enqueue default slow2 slow 60
enqueue low cleanup echo cleanup done depends_on=slow1,report
enqueue default first echo jump the line at_front
enqueue low sieve primes 200000
enqueue low big primes 2000000
enqueue default bigfib fib 91 retry=1
enqueue default oops boom
@ status
@ job report
work
@ registries
@ job flaky2
tick 10
work
@ job flaky2
tick 30
work
@ job cleanup
requeue slow1
cancel slow1
enqueue default slow3 slow 100 timeout=150
enqueue_in 60 default later echo from the future
enqueue_in 30 high soon add 40 2
@ registries
tick 29
@ status
tick 1
work
tick 30
work
requeue fib30
requeue big
work
@ job big
tick 400
@ job add1
@ job oops
cancel cleanup
@ registries

# Mistakes, each reported and skipped.
queue high
queue Bad-Name
queue
enqueue nowhere j1 echo hi
enqueue default add1 echo again
enqueue default j-2 echo hi
enqueue default j3 sing la la
enqueue default j4 add 1
enqueue default j5 add 1 two
enqueue default j6 fib
enqueue default j7 boom extra
enqueue default j8 echo hi retry=10
enqueue default j9 echo hi backoff=5
enqueue default j10 echo hi retry=1 backoff=5,x
enqueue default j11 echo hi depends_on=ghost
enqueue default j12 echo hi depends_on=add1,add1
enqueue default j13 echo hi colour=red
enqueue default j14 echo hi retry=1 retry=2
enqueue default j15 echo hi timeout=0
enqueue default
enqueue_in soon default j16 echo hi
enqueue_in 5 default j17 echo hi depends_on=add1
cancel ghost
cancel add1
requeue page
tick
tick -5
frobnicate
@
@ job
@ job ghost
@ frob
work
""")
