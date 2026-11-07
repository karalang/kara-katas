"""Writes data/ for mini_blinker: the wiring of a small shop's event bus
(signals, plugins and who listens to what), its stock list, and a day of
events with a few control commands and mistakes.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)


def put(name, text):
    with open(os.path.join("data", name), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


put("wiring.conf", """\
# The shop's event bus. Signals first, then plugins, then connections,
# which deliver in the order they are listed.

signal order_placed
signal order_cancelled
signal order_shipped
signal payment_received
signal stock_low
signal refund_issued

plugin inventory inventory low=stock_low
plugin mailer mailer from=shop@example.test
plugin audit audit file=audit.log
plugin fraud fraud limit=500.00
plugin loyalty loyalty rate=10

connect audit *
connect inventory order_placed
connect inventory order_cancelled
connect mailer order_placed sender=checkout
connect mailer order_shipped
connect mailer stock_low
connect inventory stock_low     # inventory sends it, so it is busy
connect fraud payment_received
connect loyalty order_placed weak
connect metrics *

# Mistakes, each reported and skipped.
signal Order_Placed
signal order_placed
plugin mailer mailer
plugin courier courier
plugin fraud2 fraud limit=lots
plugin loyalty2 loyalty
plugin inventory2 inventory low=no_such_signal
connect mailer order_placed
connect ghost order_placed
connect fraud refunds
connect metrics order_placed weak
connect fraud payment_received bogus
connect
frobnicate
""")

put("stock.csv", """\
sku,qty,reorder
tea-01,12,4
mug-07,3,2
pot-03,5,1
tea-02,8,3
cup-11,0,2
kettle,two,1
spoon-4,9
""")

put("events.log", """\
# time sender signal fields...
09:00:01 checkout order_placed order=1001 customer=ana sku=tea-01 qty=2 total=18.40
09:00:05 checkout order_placed order=1002 customer=ben sku=mug-07 qty=1 total=12.00
09:00:09 phone order_placed order=1003 customer=cy sku=tea-01 qty=6 total=55.20
09:00:12 checkout payment_received order=1001 amount=18.40
09:00:15 checkout payment_received order=1003 amount=812.00
09:00:20 @ status
09:00:30 checkout order_placed order=1004 customer=ana sku=tea-01 qty=1 total=9.20
09:00:31 checkout order_placed order=1005 customer=dee sku=cup-11 qty=1 total=4.00
09:00:32 checkout order_placed order=1006 customer=ed sku=vase-9 qty=1 total=30.00
09:00:40 warehouse order_shipped order=1001 customer=ana
09:00:45 checkout order_cancelled order=1003 customer=cy sku=tea-01 qty=6
09:01:00 @ temp order_placed 2
09:01:05 checkout order_placed order=1007 customer=fay sku=pot-03 qty=4 total=88.00
09:01:06 @ mute order_shipped
09:01:07 warehouse order_shipped order=1002 customer=ben
09:01:08 @ unmute order_shipped
09:01:10 checkout order_placed order=1008 customer=ben sku=tea-02 qty=6 total=41.40
09:01:15 checkout order_placed order=1009 customer=ana sku=tea-02 qty=1 total=6.90
09:01:20 @ drop loyalty
09:01:25 checkout order_placed order=1010 customer=gus sku=mug-07 qty=2 total=24.00
09:01:30 @ disconnect mailer order_shipped
09:01:31 warehouse order_shipped order=1007 customer=fay
09:01:32 @ disconnect mailer order_shipped
09:01:40 accounts refund_issued order=1003 amount=55.20
09:01:45 checkout order_placed order=1011 customer=hal sku=tea-01 qty=x total=1.00
09:01:46 checkout order_placed order=1012 customer=ivy qty=1 total=3.00
09:01:50 checkout payment_received order=1010 amount=24.00
09:01:55 @ status
09:02:00 @ drop audit
09:02:05 warehouse order_shipped order=1008 customer=ben
09:02:10 checkout order_placed order=1013 customer=jo sku=pot-03 qty=1 total=22.00

# Mistakes.
09:02:20 checkout order_exploded order=1
9:02:21 checkout order_placed order=1014
09:02:22 checkout order_placed order 1014
09:02:23 @ mute nothing
09:02:24 @ temp order_placed 0
09:02:25 @ drop loyalty
09:02:26 @ dance
09:02:27 checkout
""")
