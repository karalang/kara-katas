"""Writes data/: the JSON, JSON-lines and CSV files the jobs read, and
data/jobs.txt, one job per line. A job is a pipeline of steps separated by
" | "; the first step reads a file. oracle.py runs each job on pandas,
mini_pandas_json.kara on its own port.

Run: python3 -s -P -B mk.py"""
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
shutil.rmtree(DATA, ignore_errors=True)
os.makedirs(DATA)


def put(name, text):
    with open(os.path.join(DATA, name), "w", encoding="utf-8", newline="") as f:
        f.write(text)


def item(sku, qty, price, tags, **more):
    d = {"sku": sku, "qty": qty, "price": price, "tags": tags}
    d.update(more)
    return d


# An online shop's order export, as its API returns it: a customer object
# with a nested address, a list of line items (some with an options
# object), a coupon that is usually null, a gift flag only some orders
# carry, and returns on two orders. One customer has no address, one
# order has no items and one has `null` for them.
ORDERS = [
    {"id": 5001, "placed": "2026-04-01", "status": "shipped", "total": 37.5,
     "customer": {"id": "c-17", "name": "Ada Okafor", "tier": "gold",
                  "address": {"city": "Lagos", "country": "NG"}},
     "items": [item("TEA-01", 2, 10.0, ["tea", "organic"]),
               item("MUG-02", 1, 17.5, [], options={"color": "blue"})],
     "coupon": None, "gift": True},
    {"id": 5002, "placed": "2026-04-01", "status": "pending", "total": 64,
     "customer": {"id": "c-03", "name": "Bruno Lima", "tier": "silver",
                  "address": {"city": "Porto", "country": "PT"}},
     "items": [item("BEAN-05", 4, 16.0, ["coffee"], options={"grind": "fine", "size": "1kg"})],
     "coupon": "SPRING10"},
    {"id": 5003, "placed": "2026-04-02", "status": "shipped", "total": 12.75,
     "customer": {"id": "c-22", "name": "Seán O'Brien", "tier": "bronze",
                  "address": {"city": "Cork", "country": "IE"}},
     "items": [item("TEA-07", 3, 4.25, ["tea", "sample"])],
     "coupon": None, "gift": False},
    {"id": 5004, "placed": "2026-04-02", "status": "cancelled", "total": 0,
     "customer": {"id": "c-17", "name": "Ada Okafor", "tier": "gold",
                  "address": {"city": "Lagos", "country": "NG"}},
     "items": [], "coupon": None},
    {"id": 5005, "placed": "2026-04-03", "status": "shipped", "total": 88.4,
     "customer": {"id": "c-41", "name": "Mei Tanaka", "tier": "gold"},
     "items": [item("MUG-02", 2, 17.5, ["gift"], options={"color": "red"}),
               item("TEA-01", 1, 10.0, ["tea", "organic"]),
               item("KETTLE-1", 1, 43.4, ["hardware", "sale"])],
     "coupon": "WELCOME", "gift": True,
     "returns": [{"sku": "KETTLE-1", "reason": "damaged", "refund": 43.4}]},
    {"id": 5006, "placed": "2026-04-04", "status": "shipped", "total": 32,
     "customer": {"id": "c-03", "name": "Bruno Lima", "tier": "silver",
                  "address": {"city": "Porto", "country": "PT"}},
     "items": [item("BEAN-05", 2, 16.0, ["coffee"], options={"grind": "whole", "size": "1kg"})],
     "coupon": None},
    {"id": 5007, "placed": "2026-04-05", "status": "pending", "total": 21.0,
     "customer": {"id": "c-58", "name": 'Zoë "Z" Adler', "tier": "bronze",
                  "address": {"city": "Graz", "country": "AT"}},
     "items": None, "coupon": None},
    {"id": 5008, "placed": "2026-04-05", "status": "shipped", "total": 51.25,
     "customer": {"id": "c-22", "name": "Seán O'Brien", "tier": "bronze",
                  "address": {"city": "Cork", "country": "IE"}},
     "items": [item("TEA-07", 5, 4.25, ["tea"]),
               item("BEAN-09", 1, 30.0, ["coffee", "sale"], options={"grind": "fine", "size": "500g"})],
     "coupon": "SPRING10", "gift": False,
     "returns": [{"sku": "TEA-07", "reason": "wrong item", "refund": 8.5},
                 {"sku": "BEAN-09", "reason": "stale", "refund": 30.0}]},
    {"id": 5009, "placed": "2026-04-06", "status": "shipped", "total": 10,
     "customer": {"id": "c-41", "name": "Mei Tanaka", "tier": "gold"},
     "items": [item("TEA-01", 1, 10.0, ["tea", "organic"])],
     "coupon": None},
    {"id": 5010, "placed": "2026-04-07", "status": "returned", "total": 43.4,
     "customer": {"id": "c-17", "name": "Ada Okafor", "tier": "gold",
                  "address": {"city": "Abuja", "country": "NG"}},
     "items": [item("KETTLE-1", 1, 43.4, ["hardware"])],
     "coupon": None, "gift": True},
]
put("orders.json", json.dumps(ORDERS, indent=2, ensure_ascii=False) + "\n")

# One store's order, alone: json_normalize of a dict.
put("order.json", json.dumps(ORDERS[4], ensure_ascii=False) + "\n")

# Webhook events as JSON lines: a user object (null on one anonymous
# event), event-specific properties, and a session object only some
# carry, nested two levels down.
EVENTS = [
    {"event": "page_view", "user": {"id": 7, "plan": "free"}, "props": {"path": "/pricing", "ms": 1840}},
    {"event": "signup", "user": {"id": 9, "plan": "pro", "referrer": "ads"}, "props": {"method": "google"}},
    {"event": "page_view", "user": {"id": 9, "plan": "pro"}, "props": {"path": "/docs", "ms": 420},
     "session": {"id": "s-1", "device": {"os": "ios", "app": "4.2"}}},
    {"event": "purchase", "user": {"id": 7, "plan": "pro"}, "props": {"amount": 49.0, "items": ["pro-annual"]}},
    {"event": "page_view", "user": None, "props": {"path": "/", "ms": 95}},
    {"event": "page_view", "user": {"id": 12, "plan": "free"}, "props": {"path": "/pricing", "ms": 2210},
     "session": {"id": "s-2", "device": {"os": "android", "app": "4.1"}}},
    {"event": "purchase", "user": {"id": 12, "plan": "team"}, "props": {"amount": 120, "items": ["team-monthly", "seats-5"]}},
    {"event": "page_view", "user": {"id": 7, "plan": "pro"}, "props": {"path": "/docs", "ms": None}},
    {"event": "refund", "user": {"id": 7, "plan": "free"}, "props": {"amount": -49.0, "reason": "changed mind"}},
    {"event": "signup", "user": {"id": 15, "plan": "free", "referrer": "friend"}, "props": {"method": "email"},
     "session": {"id": "s-3", "device": {"os": "web"}}},
    {"event": "page_view", "user": {"id": 15, "plan": "free"}, "props": {"path": "/blog/launch", "ms": 3105}},
    {"event": "purchase", "user": {"id": 9, "plan": "pro"}, "props": {"amount": 9.99, "items": []}},
]
put("events.jsonl", "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in EVENTS))

# A developer survey: multi-select answers joined by ';' (one skipped),
# an answer outside the scale, ages on the bin edges, incomes with ties.
put("survey.csv", """respondent,age,country,langs,satisfaction,income,hours
1,34,DE,python;rust,high,72000,6.5
2,19,US,javascript,medium,31000,
3,18,US,python;javascript;go,low,28000,9.0
4,45,IN,java,high,95000,7.5
5,65,UK,python,medium,60000,4.0
6,27,IN,rust;go,very high,54000,8.0
7,52,DE,,low,88000,
8,23,BR,javascript;python,medium,31000,5.5
9,38,US,go,high,120000,10.0
10,61,UK,java;python,low,67000,3.0
11,30,BR,python;rust;go,medium,49000,6.0
12,71,US,python,high,45000,2.5
""")

# A temperature sensor with dropped readings, two at the start.
put("sensor.csv", """minute,temp
0,
1,
2,20.5
3,21.0
4,
5,
6,22.75
7,23.0
8,
9,21.4
10,
""")

JOBS = []


def job(*steps):
    JOBS.append(" | ".join(steps))


O = "json orders.json"
E = "jsonl events.jsonl"
S = "read survey.csv"

# Flattening: json_normalize with its defaults, a separator, a depth limit,
# a single object, and JSON lines.
job(O + " | dtypes")
job(O + " | select id,status,total,customer.name,customer.address.city,coupon,gift")
job(O + " | select id,items | head 3")
job(O + " sep=_ | select id,customer_id,customer_address_country | head 4")
job(O + " max_level=1 | select id,customer.name,customer.address | head 4")
job(O + " max_level=0 | select id,customer | head 2")
job(O + " | select id,returns")
job("json order.json | dtypes")
job("json order.json record_path=items meta=id")
job(E + " | dtypes")
job(E + " | select event,user.id,user.plan,props.path,props.ms")
job(E + " | select event,user,user.id | head 6")
job(E + " | where event == 'purchase' | select user.id,props.amount,props.items")
job(E + " | select event,session.device.os,session.device.app")
job(E + " max_level=1 | select event,session.id,session.device | head 4")

# Records: one row per element of a list, with fields from the parents.
job(O + " record_path=items | dtypes")
job(O + " record_path=items")
job(O + " record_path=items meta=id,status")
job(O + " record_path=items meta=id,customer.name,customer.tier | select id,customer.name,customer.tier,sku,qty")
job(O + " record_path=items meta=id record_prefix=item. | head 4")
job(O + " record_path=items meta=id,customer.id meta_prefix=order. | select order.id,order.customer.id,sku | head 4")
job(O + " record_path=items meta=id sep=_ | select id,sku,options_color,options_grind")
job(O + " record_path=items,tags meta=id")
job("json order.json record_path=items,tags meta=id record_prefix=tag_")
job(O + " record_path=items meta=id,customer.address.city")
job(O + " record_path=items meta=id,customer.address.city errors=ignore | select id,sku,customer.address.city")
job(O + " record_path=returns meta=id")
job(O + " record_path=items meta=id,sku errors=ignore")
job(E + " record_path=props.items meta=event")

# Lists in cells: length, explode, and splitting delimited strings.
job(O + " | len items n_items | select id,n_items")
job(O + " | explode items | select id,items | head 5")
job(O + " record_path=items meta=id | explode tags | select id,sku,tags")
job(O + " record_path=items meta=id | explode tags | counts tags")
job(O + " record_path=items meta=id | explode tags | agg tags qty:sum,id:nunique")
job(S + " | split langs ; | select respondent,langs | head 4")
job(S + " | split langs ; | explode langs | counts langs")
job(S + " | split langs ; | len langs n | select respondent,n")
job(S + " | split langs ; | explode langs | agg langs income:mean,age:max")
job(S + " | splitx langs ; first,second,third | select respondent,first,second,third")
job(S + " | splitx langs ; first,rest | select respondent,first,rest")

# Indicator columns.
job(S + " | dummies langs ; | drop age,country,satisfaction,income,hours")
job(S + " | getdummies country | select respondent,country_BR,country_DE,country_IN,country_UK,country_US")
job(S + " | getdummies satisfaction prefix=sat | drop age,country,langs,income,hours")
job(O + " | getdummies status | dtypes")

# Binning.
job(S + " | cut age 0,18,35,50,120 band | select respondent,age,band")
job(S + " | cut age 0,18,35,50,120 band lowest=1 | select respondent,age,band")
job(S + " | cut age 18,30,50,65 band right=0 | select respondent,age,band")
job(S + " | cut age 0,18,35,65,120 band labels=minor,young,adult,senior | select respondent,age,band")
job(S + " | cut age 3 band | select respondent,age,band")
job(S + " | cut age 4 band right=0 | select respondent,age,band")
job(S + " | cut hours 4 band | select respondent,hours,band")
job(S + " | cut income 3 band | counts band")
job(S + " | cut age 0,18,35,50,120 band | agg band income:mean,respondent:count")
job(S + " | cut age 0,18,35,50,120 band | counts band")
job(S + " | cut age 0,18,35,50,120 band | dtypes")
job(S + " | cut age 50,18,35 band")
job(S + " | qcut income 4 q | select respondent,income,q")
job(S + " | qcut income 3 q | select respondent,income,q")
job(S + " | qcut income 10 q | counts q")
job(S + " | qcut income 0,0.1,0.5,0.9,1 q | select respondent,income,q")
job(S + " | qcut hours 4 q labels=light,typical,busy,heavy | select respondent,hours,q")
job(S + " | qcut age 2 half | agg half age:min,age:max,income:median")
job(S + " | cut income 0,40000,80000,200000 band labels=low,mid,high | sort band,income | select respondent,income,band")

# Categoricals.
job(S + " | cat satisfaction low,medium,high | dtypes")
job(S + " | cat satisfaction low,medium,high | select respondent,satisfaction")
job(S + " | cat satisfaction low,medium,high ordered=1 | sort satisfaction | select respondent,satisfaction")
job(S + " | cat satisfaction low,medium,high ordered=1 | sort satisfaction asc=0 | select respondent,satisfaction")
job(S + " | cat satisfaction low,medium,high ordered=1 | where satisfaction >= 'medium' | select respondent,satisfaction")
job(S + " | cat satisfaction low,medium,high | where satisfaction == 'high' | select respondent,satisfaction")
job(S + " | cat satisfaction low,medium,high | where satisfaction > 'low'")
job(S + " | cat satisfaction low,medium,high,very_high | counts satisfaction")
job(S + " | cat satisfaction high,medium,low ordered=1 | agg satisfaction income:mean,age:count")
job(S + " | cat country US,UK,DE | counts country")
job(S + " | cat satisfaction low,medium,high ordered=1 | dedup satisfaction | sort satisfaction")

# Picking, filling and numbering rows.
job(S + " | nlargest 3 income | select respondent,income")
job(S + " | nsmallest 4 income | select respondent,income")
job(S + " | nlargest 3 hours | select respondent,hours")
job(O + " record_path=items meta=id | nlargest 4 price | select id,sku,price")
job("read sensor.csv | interpolate temp")
job("read sensor.csv | interpolate temp | round temp 3")
job(S + " | interpolate hours | select respondent,hours")
job(S + " | cumcount n by=country | select respondent,country,n")
job(S + " | ngroup g by=country | select respondent,country,g")
job(O + " record_path=items meta=id | cumcount line by=id | select id,line,sku")
job(S + " | replace country UK GB | counts country")
job(O + " | replace status returned refunded | select id,status")

# Errors.
job("json nope.json")
job(O + " record_path=items meta=id,sku")
job(S + " | cut age 0,18,18,65 band")
job(S + " | qcut country 4 q")
job(S + " | explode nope")

put("jobs.txt", "\n".join(JOBS) + "\n")
print(len(JOBS), "jobs")
