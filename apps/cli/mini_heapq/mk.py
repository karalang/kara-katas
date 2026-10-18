#!/usr/bin/env python3
"""Writes data/: a road map, four web-server logs, a scheduler script and
data/jobs.tsv.

A job is one line of tab-separated fields. A field that starts with "@"
names a file in data/.
"""
import os

os.makedirs("data/logs", exist_ok=True)

ROADS = """\
# from	to	minutes (roads run both ways)
Aston	Brook	7
Aston	Carlow	9
Aston	Fenwick	14
Brook	Carlow	10
Brook	Dunmore	15
Carlow	Dunmore	11
Carlow	Fenwick	2
Dunmore	Ely	6
Ely	Fenwick	9
Fenwick	Glen	12
Ely	Glen	8
Glen	Harrow	5
Harrow	Ivy	4
Glen	Ivy	9
Ivy	Jura	3
Harrow	Jura	7
Kells	Lisle	2
Jura	Mallow	6
Ivy	Mallow	9
Mallow	Nore	1
Jura	Nore	7
"""
with open("data/roads.tsv", "w") as f:
    f.write(ROADS)

LOGS = {
    "web1.log": [
        "09:00:01 web1 GET /index.html 200 5120 12",
        "09:00:03 web1 GET /app.js 200 88211 40",
        "09:00:03 web1 GET /style.css 200 9100 8",
        "09:00:07 web1 POST /api/login 401 310 95",
        "09:00:12 web1 GET /api/items 200 20480 130",
        "09:00:15 web1 GET /missing 404 210 3",
        "09:00:21 web1 GET /api/items?page=2 200 20480 128",
    ],
    "web2.log": [
        "09:00:00 web2 GET /health 200 2 1",
        "09:00:03 web2 GET /index.html 200 5120 15",
        "09:00:05 web2 POST /api/login 200 512 210",
        "09:00:12 web2 GET /api/report 500 1024 2900",
        "09:00:12 web2 GET /health 200 2 1",
        "09:00:30 web2 GET /download/big.iso 200 734003200 15400",
    ],
    "web3.log": [
        "09:00:02 web3 GET /favicon.ico 304 0 2",
        "09:00:03 web3 GET /app.js 200 88211 44",
        "09:00:09 web3 PUT /api/items/7 204 0 77",
        "09:00:21 web3 DELETE /api/items/9 403 120 6",
    ],
    "empty.log": [],
}
for name, lines in LOGS.items():
    with open(os.path.join("data/logs", name), "w") as f:
        f.write("".join(l + "\n" for l in lines))

SCHED = """\
# time	priority	kind	name	[args]
#   once: run once
#   repeat N EVERY: run, then enter itself again EVERY later, N runs in all
#   later NAME DELAY: run, then enter NAME DELAY later (sched.enter)
#   cancel NAME: run, then cancel the queued event NAME
0	2	once	boot
5	1	repeat	heartbeat	4	10
5	0	once	migrate
12	1	once	backup
12	1	once	rotate
12	0	once	flush
30	5	once	report
25	3	cancel	stop-report	report
40	1	later	compact	cleanup	7
26	1	cancel	cancel-ghost	ghost
44	9	once	late
"""
with open("data/sched.txt", "w") as f:
    f.write(SCHED)

JOBS = r"""
heap	5,3,8,1,9,2	push 4|pop|pop|pushpop 0|pushpop 10|replace 6|push 1|push 1|pop|pop|pop
heap	-	pop|replace 3|push 7|push 2|push 9|push 2|pop|pushpop 2|pop|pop|pop|pop
heap	9,8,7,6,5,4,3,2,1,0	pop|pop|replace 11|push -1|pop
heap	4,4,4,1,1	pop|pop|pop|pop|pop|pop
nlargest	3	-	5,1,9,3,9,7,2
nlargest	1	-	5,1,9,3,9,7,2
nlargest	0	-	5,1,9
nlargest	10	-	5,1,9
nlargest	-2	-	5,1,9
nlargest	1	-	
nsmallest	3	-	5,1,9,3,1,7,2
nsmallest	1	-	5,1,9,3,1,7,2
nsmallest	9	-	5,1,9
nlargest	3	bytes	@logs
nlargest	4	ms	@logs
nlargest	2	path	@logs
nsmallest	3	ms	@logs
nsmallest	4	status	@logs
nlargest	20	ms	@logs
nsmallest	1	bytes	@logs
merge	-	1,3,5,7;0,2,4,8;5,10,15,20;;25
merge	-	;;
merge	-	2,2;1,2;2
merge	time	web1.log;web2.log;web3.log;empty.log
merge	host	web2.log;web1.log
merge	-	web3.log;web1.log
bisect	left	1,2,4,4,4,8	4
bisect	right	1,2,4,4,4,8	4
bisect	left	1,2,4,4,4,8	0
bisect	right	1,2,4,4,4,8	9
bisect	left	-	3
insort	-	5,1,4,1,5,9,2,6,5,3
insort	10,20,30	25,5,35,20
grade	33,99,77,70,89,90,100,59,60
buckets	5,10,50,100,500,1000,5000	@logs
buckets	1	@logs
route	Aston	Nore
route	Aston	Glen
route	Nore	Aston
route	Carlow	Carlow
route	Brook	Ivy
route	Aston	Lisle
route	Kells	Lisle
route	Aston	Atlantis
sched	@sched.txt
"""
with open("data/jobs.tsv", "w") as f:
    f.write(JOBS.lstrip("\n"))
