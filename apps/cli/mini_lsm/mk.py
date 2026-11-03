"""Writes data/ for mini_lsm: a product catalog to load and data/jobs.txt,
a session against two stores that writes, reads, flushes, compacts,
crashes, tears and corrupts files, and recovers.

Run from this directory: python3 -s -P -B mk.py"""
import os
import random

os.makedirs("data", exist_ok=True)


def write(name, text):
    with open(os.path.join("data", name), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


rnd = random.Random(20261104)
adjs = ["red", "blue", "steel", "oak", "mini", "pro", "eco", "smart", "dual", "quiet"]
nouns = ["kettle", "lamp", "drill", "chair", "router", "blender", "fan", "desk", "mug", "saw"]
rows = ["sku,name,price,stock"]
skus = rnd.sample(range(1, 10000), 160)
for s in skus:
    name = f"{rnd.choice(adjs)}_{rnd.choice(nouns)}"
    price = f"{rnd.randint(1, 499)}.{rnd.randint(0, 99):02d}"
    rows.append(f"{s:05d},{name},{price},{rnd.randint(0, 250)}")
# Rows the loader must skip.
rows += ["oops", "00042,,1.00,3", "00043,bad name,1.00,3", ""]
write("catalog.csv", "\n".join(rows) + "\n")
some = sorted(skus)

jobs = f"""# A product store: load a catalog, read through every level.
create shop
load shop catalog.csv
stats shop
ls shop
get shop sku:{some[0]:05d}
get shop sku:{some[80]:05d}
get shop sku:{some[159]:05d}
get shop sku:00000
get shop sku:99999
scan shop sku:{some[10]:05d} sku:{some[20]:05d}
scan shop sku: sku:~ 5
# Updates, deletes and a snapshot that pins the old versions.
snap shop before_sale
put shop sku:{some[80]:05d} sale_kettle|9.99|12
del shop sku:{some[81]:05d}
batch shop sku:{some[82]:05d}=boxed_set|59.00|4 -sku:{some[83]:05d} note:sale=on
get shop sku:{some[80]:05d}
get shop sku:{some[80]:05d} @before_sale
get shop sku:{some[81]:05d}
get shop sku:{some[81]:05d} @before_sale
get shop sku:{some[83]:05d}
get shop note:sale
scan shop sku:{some[79]:05d} sku:{some[85]:05d}
scan shop sku:{some[79]:05d} sku:{some[85]:05d} @before_sale
flush shop
stats shop
compact shop
stats shop
get shop sku:{some[80]:05d} @before_sale
get shop sku:{some[81]:05d} @before_sale
release shop before_sale
compact shop
stats shop
get shop sku:{some[81]:05d}
sst shop 16
check shop
# A crash loses the memtable but not the log.
put shop cart:alice sku:{some[3]:05d}x2
put shop cart:bob sku:{some[7]:05d}x1
del shop cart:alice
crash shop
get shop cart:bob
open shop
get shop cart:bob
get shop cart:alice
# A torn write at the end of the log is cut off on recovery.
put shop cart:carol sku:{some[9]:05d}x5
put shop cart:dave sku:{some[11]:05d}x1
crash shop
tear shop 7
open shop
get shop cart:carol
get shop cart:dave
put shop cart:dave sku:{some[11]:05d}x3
get shop cart:dave
# A bad byte in the middle of the log stops replay there.
put shop cart:erin sku:{some[12]:05d}x1
put shop cart:frank sku:{some[13]:05d}x2
put shop cart:gina sku:{some[14]:05d}x4
crash shop
flip shop log 260
open shop
get shop cart:erin
get shop cart:frank
get shop cart:gina
# Bulk writes: flushes, then a compaction when L0 fills up.
putn metrics m:cpu: 0 1
create metrics
putn metrics m:cpu: 60 40
putn metrics m:mem: 60 40
putn metrics m:disk: 60 40
putn metrics m:net: 60 40
stats metrics
get metrics m:mem:00042
get metrics m:net:00059
get metrics m:zzz:00000
scan metrics m:disk:00057 m:mem:00002
putn metrics m:cpu: 30 12
stats metrics
compact metrics
stats metrics
ls metrics
get metrics m:cpu:00007
get metrics m:cpu:00045
scan metrics m:cpu:00027 m:cpu:00033
check metrics
# A flipped byte in a table is caught by its block checksum.
sst metrics 32
flip metrics 32 100
check metrics
get metrics m:cpu:00002
get metrics m:disk:00053
open metrics
# Errors.
get nosuch k
create shop
open nosuch
put shop
get shop
scan shop z a
snap shop
get shop k @nosnap
release shop nosnap
sst shop 9999
flip shop 9999 1
tear shop 100000
batch shop =x
putn shop p: x 4
frobnicate shop
"""
write("jobs.txt", jobs)
