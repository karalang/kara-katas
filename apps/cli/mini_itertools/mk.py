#!/usr/bin/env python3
"""Writes data/: a sales ledger in CSV and data/jobs.tsv.

A job is one line of tab-separated fields. A list of integers is written
"1,2,3" ("-" or an empty field is the empty list); several lists are
separated by ";". A field that starts with "@" names a file in data/.
"""
import os

os.makedirs("data", exist_ok=True)

SALES = """\
month,region,product,units,price,promo
2026-01,north,kettle,12,30,0
2026-01,south,kettle,7,30,1
2026-01,north,toaster,5,45,0
2026-02,east,kettle,9,28,1
2026-02,north,blender,3,80,0
2026-02,south,toaster,11,45,0
2026-03,south,kettle,4,30,0
2026-03,east,blender,6,75,1
2026-03,east,toaster,2,45,0
2026-03,north,kettle,15,29,1
2026-04,west,blender,8,78,0
2026-04,south,blender,1,80,0
2026-04,north,toaster,6,44,1
"""
with open("data/sales.csv", "w") as f:
    f.write(SALES)

JOBS = r"""
count	10	3	5
count	-2	-5	4
count	7	0	3
cycle	1,2,3	8
cycle	-	5
cycle	4	3
repeat	9	4
repeat	9	0
accumulate	1,2,3,4,5	add	-
accumulate	1,2,3,4,5	mul	-
accumulate	3,1,4,1,5,9,2,6	max	-
accumulate	3,1,4,1,5,9,2,6	min	-
accumulate	1,2,3	add	100
accumulate	-	add	-
accumulate	-	add	7
batched	1,2,3,4,5,6,7	3
batched	1,2,3	3
batched	1,2,3	5
batched	-	2
chain	1,2;3;;4,5,6
chain	;;
compress	1,2,3,4,5,6	1,0,1,0,1,1
compress	1,2,3	1,1,1,1,1
compress	1,2,3,4	0,1
dropwhile	1,4,6,4,1	5
takewhile	1,4,6,4,1	5
dropwhile	7,8	5
takewhile	7,8	5
filterfalse	1,2,3,4,5,6,7	odd
groupby	1,1,2,3,3,3,1,1	same
groupby	1,3,5,2,4,7,9,8	parity
groupby	-	same
islice	0,1,2,3,4,5,6,7,8,9	2	8	2
islice	0,1,2,3,4,5,6,7,8,9	0	-	3
islice	0,1,2,3,4,5,6,7,8,9	7	3	1
islice	0,1,2,3,4,5,6,7,8,9	5	50	1
islice	0,1,2	0	0	1
pairwise	1,2,4,7,11
pairwise	5
pairwise	-
zip_longest	1,2,3,4	10,20	0
zip_longest	-	10,20	-1
product	1,2;3,4	1
product	0,1	3
product	1,2;-;3	1
product	-	0
permutations	1,2,3	-
permutations	1,2,3,4	2
permutations	1,2,3	0
permutations	1,2	3
combinations	1,2,3,4,5	3
combinations	1,2,3	0
combinations	1,2	3
combinations	3,1,2	2
cwr	1,2,3	2
cwr	1,2	3
cwr	-	2
cwr	-	0
report	@sales.csv
"""
with open("data/jobs.tsv", "w") as f:
    f.write(JOBS.lstrip("\n"))
