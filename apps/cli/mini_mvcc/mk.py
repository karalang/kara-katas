"""Writes data/ for mini_mvcc: six scripted sessions of interleaved
transactions, and one with mistakes in it.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)

SESSIONS = {
    "1_bank.mvcc": """# Two transfers race on the same account. Under read committed the
# later writer wins and a deposit is lost; under snapshot isolation the
# second writer aborts and retries.
begin setup
setup put acct:alice 100
setup put acct:bob 50
setup commit
begin t1 rc
begin t2 rc
t1 add acct:alice -30
t1 add acct:bob 30
t2 add acct:alice 20
t1 commit
t2 commit
begin audit
audit scan acct:
audit sum acct:
audit commit
begin fix
fix put acct:alice 90
fix commit
begin t3 si
begin t4 si
t3 add acct:alice -30
t3 add acct:bob 30
t4 add acct:alice 20
t3 commit
t4 commit
t4 get acct:alice
begin t4 si
t4 add acct:alice 20
t4 commit
begin audit
audit scan acct:
audit sum acct:
audit get acct:carol
audit commit
dump
""",
    "2_oncall.mvcc": """# Two doctors on call each check that someone else is on call, then
# go off. Snapshot isolation lets both commit (write skew); serializable
# aborts the second, whose reads the first one's write made stale.
begin setup
setup put oncall:alice yes
setup put oncall:bob yes
setup commit
begin a si
begin b si
a scan oncall:
b scan oncall:
a put oncall:alice no
b put oncall:bob no
a commit
b commit
begin check
check scan oncall:
check commit
begin fix
fix put oncall:alice yes
fix put oncall:bob yes
fix commit
begin a ser
begin b ser
a get oncall:alice
a get oncall:bob
b get oncall:alice
b get oncall:bob
a put oncall:alice no
b put oncall:bob no
a commit
b commit
# A scan whose range gains a key before the scanner commits.
begin r ser
begin w si
r scan oncall:
w put oncall:carol yes
w commit
r put shift:count 2
r commit
# A read-only transaction saw one snapshot, so it commits unchecked.
begin ro ser
begin w2 si
ro scan oncall:
w2 put oncall:alice yes
w2 commit
ro get oncall:alice
ro commit
begin check
check scan oncall:
check scan shift:
check commit
""",
    "3_reads.mvcc": """# What a transaction sees: read committed re-reads the latest commit at
# every statement, a snapshot does not move, and a transaction always
# sees its own writes.
begin setup
setup put cfg:mode fast
setup put cfg:retries 3
setup put user:1 ann
setup commit
begin rc1 rc
begin si1 si
rc1 get cfg:mode
si1 get cfg:mode
begin w
w put cfg:mode safe
w del cfg:retries
w put cfg:timeout 30
w commit
rc1 get cfg:mode
si1 get cfg:mode
rc1 scan cfg:
si1 scan cfg:
si1 put cfg:mode slow
si1 del cfg:timeout
si1 put cfg:level 2
si1 scan cfg:
si1 get cfg:mode
si1 commit
si1 get cfg:mode
rc1 put cfg:retries 5
rc1 commit
begin r
r scan cfg:
r get user:1
r get user:2
r del user:1
r get user:1
r scan user:
r add user:1 1
r abort
begin r2
r2 get user:1
r2 add user:1 1
r2 get user:1
begin r3
r3 get user:1
r3 commit
dump
""",
    "4_vacuum.mvcc": """# Old versions stay while a snapshot that can see them is open; vacuum
# removes the rest. A read committed transaction holds nothing back.
begin s
s put page:home v1
s put page:about v1
s put tmp:x 1
s commit
begin long si
begin e1
e1 put page:home v2
e1 commit
begin e2
e2 put page:home v3
e2 del tmp:x
e2 commit
begin e3
e3 put page:home v4
e3 put page:about v2
e3 commit
begin watcher rc
dump
vacuum
long get page:home
long scan page:
long scan tmp:
long commit
vacuum
dump
begin e4
e4 del page:about
e4 commit
watcher scan page:
vacuum
dump
watcher commit
""",
    "5_crash.mvcc": """# Every commit is appended to a write-ahead log. A crash loses what was
# in memory and the open transactions; recover replays the log. A torn
# write at the end of the log is dropped, and a checkpoint writes a
# snapshot and empties the log.
begin a
a put order:1 new
a put order:2 new
a commit
begin b
b put order:1 paid
b commit
begin c
c put order:3 new
begin d ser
d get order:1
crash
d get order:1
recover
begin e
e scan order:
e put order:2 shipped
e commit
crash
tear 9
recover
begin f
f scan order:
f put order:4 new
f del order:1
f commit
vacuum
checkpoint
begin g
g put order:1 refunded
g commit
crash
recover
begin h
h scan order:
h commit
dump
recover
tear 3
crash
crash
recover
""",
    "7_bad.mvcc": """# Mistakes the loader reports.
begin t1 snapshot
t9 get x
t1 put x
t1 put x -
t1 add x lots
tear -3
vacuum now
launch
t1 frobnicate x
begin
""",
}


# A bank of ten accounts under load: rounds of three overlapping
# transfers at mixed isolation levels, committed in a shuffled order,
# with an audit, vacuum and finally a crash and recovery.
def load():
    seed = 20261103

    def rnd(n):
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return (seed // 65536) % n

    accts = [f"acct:{i:02d}" for i in range(10)]
    out = ["# Ten accounts, 24 rounds of three overlapping transfers at mixed",
           "# isolation levels. Snapshot and serializable transfers keep the",
           "# total; a read committed one can lose another's update.",
           "begin setup"]
    out += [f"setup put {a} 100" for a in accts]
    out.append("setup commit")
    levels = ["si", "ser", "rc", "si", "ser"]
    n = 0
    for rd in range(24):
        names = []
        for k in range(3):
            n += 1
            t = f"x{n}"
            names.append(t)
            out.append(f"begin {t} {levels[rnd(len(levels))]}")
        for t in names:
            a = accts[rnd(10)]
            b = accts[rnd(10)]
            while b == a:
                b = accts[rnd(10)]
            amt = 1 + rnd(40)
            out.append(f"{t} add {a} -{amt}")
            out.append(f"{t} add {b} {amt}")
        order = names[:]
        for i in range(len(order) - 1, 0, -1):
            j = rnd(i + 1)
            order[i], order[j] = order[j], order[i]
        for t in order:
            out.append(f"{t} commit")
        if rd % 6 == 5:
            out.append("begin audit si")
            out.append("audit sum acct:")
            out.append("audit commit")
            out.append("vacuum")
    out += ["begin audit", "audit scan acct:", "audit sum acct:", "audit commit",
            "checkpoint", "begin late", "late add acct:00 5", "late add acct:09 -5",
            "late commit", "crash", "recover", "begin audit", "audit sum acct:",
            "audit commit"]
    return "\n".join(out) + "\n"


SESSIONS["6_load.mvcc"] = load()

for name, text in SESSIONS.items():
    with open(os.path.join("data", name), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
