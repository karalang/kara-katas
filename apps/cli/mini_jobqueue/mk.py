"""Writes data/ for mini_jobqueue: the queues and worker kinds of a small
online shop (mail, payments, webhooks, exports), each file with a few
mistakes, and a day's script of jobs, failures, a crash that tears the
log, recovery and pruning.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)


def put(name, text):
    with open(os.path.join("data", name), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


put("queues.conf", """\
# Queues of the shop's job runner. limit is how many jobs of the queue
# run at once.

queue default limit=2
queue mailers limit=2
queue payments limit=1        # the card processor allows one call at a time
queue webhooks limit=3
queue exports limit=1 paused  # reports wait for the nightly window

queue Mailers limit=2         # names are lower case
queue media limit=0
queue media limit=200
queue media workers=4
queue media
queue mailers limit=5
topic events limit=1
queue
""")

put("workers.conf", """\
# Worker kinds: how long an attempt runs and how it ends.

worker send_email duration=2s
worker send_welcome duration=1 attempts=3
worker charge_card duration=3 attempts=3 fail=1 error=card declined by issuer
worker webhook_deliver duration=1 attempts=4 fail=1,2,3,4 error=HTTP 503 from endpoint
worker generate_report duration=2m timeout=90s attempts=2
worker sync_inventory duration=30s
worker refund duration=5 cancel_on=1
worker resize_image duration=4

worker send-sms duration=1           # names use underscores
worker thumbnail duration=0
worker thumbnail duration=5x
worker thumbnail
worker send_email duration=3
worker export_csv duration=10 fail=1,30
worker export_csv duration=10 cancel_on=0
worker export_csv duration=10 attempts=50
worker export_csv duration=10 retries=3
worker export_csv duration=10 error=
job cleanup duration=1
worker
""")

put("events.txt", """\
# A day at the shop. Times are HH:MM:SS since the runner started.

00:00:00 enqueue mailers send_email to=ana@example.com template=receipt
00:00:00 enqueue mailers send_email to=bo@example.com template=receipt
00:00:00 enqueue mailers send_email to=cy@example.com template=receipt priority=1
00:00:00 enqueue mailers send_email to=di@example.com template=receipt
00:00:01 stats

# A card is declined once and charged on the retry; another goes through.
00:00:10 enqueue payments charge_card order=1001 amount=4999
00:00:10 enqueue payments charge_card order=1002 amount=1250 fail=none
00:00:10 enqueue payments charge_card order=1003 amount=899 fail=1,2,3

# A partner endpoint is down; another answers on the second try.
00:00:20 enqueue webhooks webhook_deliver url=https://partner.example/hook event=order.paid
00:00:20 enqueue webhooks webhook_deliver url=https://crm.example/hook event=order.paid fail=1
00:00:20 enqueue webhooks webhook_deliver url=https://ops.example/hook event=order.paid fail=none

# The welcome mail goes out an hour after signup, once.
00:00:30 enqueue mailers send_welcome user=77 in=1h unique=1h
00:00:31 enqueue mailers send_welcome user=77 in=1h unique=1h
00:00:32 enqueue mailers send_welcome user=78 in=1h unique=1h
00:00:40 jobs retryable
00:01:00 jobs scheduled

# Image work queues up behind the limit; priorities pick the order.
00:02:00 enqueue default sync_inventory warehouse=east
00:02:00 enqueue default resize_image photo=p1 size=large priority=5
00:02:00 enqueue default resize_image photo=p2 size=large priority=5
00:02:00 enqueue default resize_image photo=p3 size=thumb
00:02:00 enqueue default resize_image photo=p4 size=thumb
00:02:05 cancel 13
00:02:06 stats
00:02:10 scale default 3
00:02:15 cancel 13
00:02:20 retry 13

# A refund the worker refuses, retried by hand.
00:03:00 enqueue payments refund order=1001 amount=4999
00:03:30 jobs cancelled
00:03:31 retry 18

# Mistakes an operator makes.
00:04:00 enqueue sms send_email to=ana@example.com
00:04:00 enqueue mailers send_sms to=ana@example.com
00:04:00 enqueue mailers send_email to=ana@example.com priority=10
00:04:00 enqueue mailers send_email to=ana@example.com in=soon
00:04:00 enqueue mailers send_email to=ana@example.com max_attempts=0
00:04:00 enqueue mailers send_email to=ana@example.com fail=0
00:04:00 enqueue mailers send_email to=ana@example.com urgent
00:04:00 enqueue mailers send_email To=ana@example.com
00:04:00 enqueue mailers send_email to=ana@example.com to=bo@example.com
00:04:00 enqueue mailers
00:04:00 pause media
00:04:00 resume mailers
00:04:00 scale mailers 0
00:04:00 cancel abc
00:04:00 cancel 999
00:04:00 cancel 1
00:04:00 retry 2
00:04:00 retry 7
00:04:00 jobs stuck
00:04:00 recover
00:04:00 restart
00:03:59 stats
00:61:00 stats
00:04:00
00:04:00 pause mailers mailers

# The nightly window opens: the report times out, is retried by hand.
00:05:00 enqueue exports generate_report month=2026-10 format=csv
00:05:00 enqueue exports generate_report month=2026-10 format=csv unique=10m
00:05:30 jobs available
00:06:00 resume exports
00:06:00 pause exports
00:12:00 jobs discarded
00:12:00 resume exports
00:12:01 retry 19
00:14:00 retry 19
00:20:00 stats

# Orders keep coming; payments is paused for a processor upgrade.
00:30:00 pause payments
00:30:00 enqueue payments charge_card order=1004 amount=2500
00:30:00 enqueue payments charge_card order=1005 amount=7300 fail=none priority=2 max_attempts=1
00:30:00 enqueue mailers send_email to=ed@example.com template=shipped
00:30:00 enqueue mailers send_email to=fa@example.com template=shipped
00:30:05 resume payments

# The process dies writing a record, and comes back.
00:30:06 crash torn
00:30:30 stats
00:31:00 recover
00:31:01 jobs executing
00:31:01 enqueue default sync_inventory warehouse=west
00:31:05 crash
00:32:00 crash
00:33:00 recover
00:33:00 recover
00:33:01 jobs available
00:33:02 retry 21

# Housekeeping: completed and dead jobs older than 30 minutes go.
01:01:00 jobs scheduled
01:10:00 prune 30m
01:10:00 prune soon
01:10:01 jobs all
01:12:00 enqueue mailers send_email to=ana@example.com template=receipt
01:12:00 enqueue mailers send_email to=bo@example.com template=reminder in=15m
01:12:00 enqueue webhooks webhook_deliver url=https://partner.example/hook event=order.refunded
01:12:30 drain
""")
