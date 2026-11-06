"""Writes data/ for mini_logbroker: the topics of a small online shop's
event broker (orders, payments, clicks, customer profiles, an audit
trail), with a few mistakes, and a day's script of producers, consumer
groups, retention and compaction runs, and two crashes.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)


def put(name, text):
    with open(os.path.join("data", name), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


put("topics.conf", """\
# Topics of the shop's event broker. Sizes are small so that segments
# roll, and retention and compaction have something to do, within a day.

topic orders partitions=3 segment_bytes=400 retention=1h
topic payments partitions=2 segment_bytes=300 retention_bytes=200
topic clicks partitions=4 segment_bytes=256 retention=20m
topic profiles partitions=2 segment_bytes=360 cleanup=compact delete_retention=10m
topic audit partitions=1        # the auditors keep everything
topic shipments partitions=2 cleanup=compact

topic Orders partitions=2       # names are lower case
topic orders partitions=1
topic __internal partitions=1
topic inventory
topic inventory partitions=0
topic inventory partitions=4 segment_bytes=32
topic inventory partitions=4 retention=10x
topic inventory partitions=4 retention=0s
topic inventory partitions=4 cleanup=archive
topic inventory partitions=4 replicas=3
topic inventory partitions=4 partitions=2
topic inventory partitions=4 cleanup=compact retention=1h
topic inventory partitions=4 retention
topik shipments partitions=2
topic
""")

put("script.txt", """\
# A day at the shop's event broker. Times are HH:MM:SS.

08:00:00 describe orders
08:00:00 describe profiles

# Orders are keyed by order id, so an order's events stay in order.
08:00:05 produce orders ord-1001 {"event":"created","sku":"tea-01","qty":2}
08:00:06 produce orders ord-1002 {"event":"created","sku":"mug-07","qty":1}
08:00:07 produce orders ord-1003 {"event":"created","sku":"tea-02","qty":6}
08:00:08 produce orders ord-1001 {"event":"paid","amount":"18.40"}
08:00:09 produce orders ord-1004 {"event":"created","sku":"pot-03","qty":1}
08:00:10 produce orders ord-1002 {"event":"paid","amount":"12.00"}
08:00:11 produce orders:1 - {"event":"heartbeat","from":"checkout-2"}
08:00:12 produce orders ord-1005 {"event":"created","sku":"tea-01","qty":1}
08:00:13 produce orders ord-1003 {"event":"cancelled","reason":"out of stock"}
08:00:14 produce orders ord-1006 {"event":"created","sku":"cup-11","qty":4}

08:00:20 produce payments ord-1001 card ok 18.40 EUR
08:00:21 produce payments ord-1002 card ok 12.00 EUR
08:00:22 produce payments ord-1004 paypal pending 31.90 EUR
08:00:23 produce payments ord-1004 paypal ok 31.90 EUR

# Clicks carry no key and go round-robin over the partitions.
08:00:30 batch clicks 9 0 view:/products/
08:00:31 produce clicks - view:/cart

# Profiles are compacted: the latest value per customer is what counts.
08:00:40 produce profiles cust-17 {"name":"Ana","city":"Porto"}
08:00:41 produce profiles cust-23 {"name":"Bo","city":"Malmo"}
08:00:42 produce profiles cust-31 {"name":"Cy","city":"Lyon"}
08:00:43 produce profiles cust-17 {"name":"Ana","city":"Lisbon"}
08:00:44 produce profiles cust-42 {"name":"Di","city":"Ghent"}

08:00:50 produce audit - login admin from 10.0.0.7
08:00:51 produce audit - price change tea-01 9.20 to 9.40

# Mistakes a producer makes.
08:00:55 produce profiles - {"name":"nobody"}
08:00:55 produce invoices inv-1 draft
08:00:55 produce orders:7 ord-1007 {"event":"created"}
08:00:55 produce orders:x ord-1007 {"event":"created"}
08:00:55 produce __consumer_offsets k v
08:00:55 produce orders ord-1007
08:00:55 batch clicks 0 0 view:
08:00:55 batch clicks:1 3 0 view:
08:00:55 deliver orders ord-1007

08:01:00 fetch orders:0 0
08:01:00 fetch orders:1 1 2
08:01:00 fetch orders:2 99
08:01:00 fetch orders 0
08:01:00 describe orders

# The billing service reads orders and payments with two consumers.
08:02:00 join billing bill-a orders,payments
08:02:00 join billing bill-b orders
08:02:01 poll billing bill-a 4
08:02:02 commit billing bill-a
08:02:03 poll billing bill-b
08:02:04 poll billing bill-a 10
08:02:05 commit billing bill-b
# bill-a crashes before it commits its second poll; its partitions move.
08:02:10 leave billing bill-a
08:02:11 poll billing bill-b 20
08:02:12 commit billing bill-b
08:02:13 lag billing
08:02:14 join billing bill-a orders,payments reset=latest
08:02:14 join billing bill-b orders
08:02:14 join billing bill-c orders,invoices
08:02:14 poll billing bill-z
08:02:14 commit nosuch bill-a

# Analytics only cares about clicks from now on.
08:03:00 join analytics an-1 clicks reset=latest
08:03:01 poll analytics an-1
08:03:02 batch clicks 6 0 view:/search?q=tea&page=
08:03:03 poll analytics an-1 4
08:03:04 commit analytics an-1
08:03:05 poll analytics an-1 4
08:03:06 commit analytics an-1

08:04:00 join profile_cache pc-1 profiles
08:04:01 poll profile_cache pc-1 20
08:04:02 commit profile_cache pc-1

# Profiles change during the morning; one customer closes the account.
08:20:00 produce profiles cust-23 {"name":"Bo","city":"Oslo"}
08:20:01 produce profiles cust-31 null
08:20:02 produce profiles cust-17 {"name":"Ana","city":"Lisbon","vip":true}
08:20:03 produce profiles cust-55 {"name":"Ed","city":"Bern"}
08:20:04 produce profiles cust-42 {"name":"Di","city":"Antwerp"}
08:20:05 produce profiles cust-23 {"name":"Bo","city":"Bergen"}
08:20:06 produce profiles cust-61 {"name":"Flo","city":"Graz"}
08:20:07 produce profiles cust-55 {"name":"Ed","city":"Basel"}
08:20:08 describe profiles
08:20:10 compact
08:20:11 describe profiles
08:20:12 fetch profiles:0 0 20
08:20:12 fetch profiles:1 0 20

08:25:00 batch clicks 12 0 view:/products/tea-0
08:25:01 batch payments 8 3 settle-
08:25:02 describe payments
08:25:03 retention
08:25:04 describe payments
08:25:05 describe clicks

08:30:00 poll analytics an-1 30
08:30:01 commit analytics an-1
08:30:02 poll profile_cache pc-1 20
08:30:03 commit profile_cache pc-1

# Ten minutes later the tombstone for cust-31 can go.
08:31:00 compact
08:31:01 fetch profiles:0 0 20
08:31:01 fetch profiles:1 0 20

# Lunch rush.
09:10:00 batch orders 14 5 rush-
09:10:01 batch clicks 10 0 view:/checkout/step-
09:10:02 poll billing bill-b 8
09:10:03 commit billing bill-b
09:10:04 retention
09:10:05 describe clicks

# The broker host loses power while a record is half written.
09:15:00 produce orders ord-1101 {"event":"created","sku":"tea-09","qty":3}
09:15:01 crash orders:9:30
09:15:01 crash orders:0:999999
09:15:01 crash orders:0:30
09:15:02 produce orders ord-1102 {"event":"created"}
09:15:03 poll billing bill-b
09:15:04 restart
09:15:05 restart
09:15:06 describe orders
09:15:07 lag billing
09:15:08 poll billing bill-b
09:15:09 join billing bill-b orders
09:15:10 poll billing bill-b 30
09:15:11 commit billing bill-b
09:15:12 join analytics an-2 clicks
09:15:13 poll analytics an-2 40

# Old orders age out; billing's committed offsets now point before the log.
10:20:00 produce orders ord-1201 {"event":"created","sku":"mug-02","qty":1}
10:20:01 produce orders ord-1202 {"event":"created","sku":"tea-05","qty":2}
10:20:02 produce orders ord-1203 {"event":"created","sku":"pot-01","qty":1}
10:20:03 retention
10:20:04 describe orders
10:20:05 leave billing bill-b
10:20:06 join billing bill-d orders,payments
10:20:07 poll billing bill-d 20
10:20:08 commit billing bill-d
10:20:09 lag billing

# Analytics is retired; its offsets become tombstones and compaction drops them.
10:30:00 leave analytics an-2
10:30:01 delete-group analytics
10:30:01 delete-group billing
10:30:02 lag analytics
10:30:03 compact
10:30:04 describe __consumer_offsets

# A clean restart in the evening keeps everything.
18:00:00 crash
18:00:01 restart
18:00:02 lag billing
18:00:03 lag profile_cache
18:00:04 produce audit - logout admin
18:00:05 fetch audit:0 0
17:00:00 describe audit
18:00:06 retention now
18:00:06 compact now
18:00:06 describe
18:00:06 flush
18:0:07 describe audit
""")
