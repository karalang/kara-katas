"""Writes data/: the files the jobs read, each shaped like a real export,
and data/jobs.txt, one job per line. A job is a pipeline of steps
separated by " | "; the first step reads a file and the last one prints
the result, by default as print(df) prints it. oracle.py runs each job on
pandas, mini_pandas_query.kara on its own port.

Run: python3 -s -P -B mk.py"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
shutil.rmtree(DATA, ignore_errors=True)
os.makedirs(DATA)


def put(name, text):
    with open(os.path.join(DATA, name), "w", encoding="utf-8", newline="") as f:
        f.write(text)


class Lcg:
    """A small linear congruential generator, so the files are the same on
    every run without depending on any library's random numbers."""

    def __init__(self, seed):
        self.s = seed

    def next(self, n):
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) % (1 << 64)
        return (self.s >> 33) % n


# A shop's order export: 96 orders over September, four regions, three
# channels, a discount that is sometimes missing, a gift flag and a free
# text note that is usually empty, sometimes long, once holds a tab and
# once a line break inside quotes.
r = Lcg(2026)
regions = ["North", "South", "East", "West"]
channels = ["web", "store", "phone"]
products = [("Kettle", 39.99), ("Toaster", 54.5), ("Blender", 89.0),
            ("Mug set", 18.25), ("Grinder", 129.95), ("Scale", 24.0)]
notes = [
    "", "", "", "", "", "",
    "leave at the back door",
    "customer asked for the invoice to be sent to the accounts payable mailbox instead",
    "gift wrap\tred paper",
    "\"call before\ndelivery\"",
    "repeat customer",
]
rows = ["order_id,date,region,channel,product,units,unit_price,discount,revenue,gift,note"]
for i in range(96):
    day = 1 + i * 30 // 96
    reg = regions[r.next(4)]
    ch = channels[r.next(3)]
    name, price = products[r.next(6)]
    units = 1 + r.next(9)
    d = [0.0, 0.0, 0.05, 0.1, 0.15, None][r.next(6)]
    rev = round(units * price * (1 - (d or 0.0)), 2)
    gift = "True" if r.next(5) == 0 else "False"
    note = notes[r.next(len(notes))]
    rows.append(",".join([
        str(10001 + i), f"2026-09-{day:02d}", reg, ch, name, str(units),
        f"{price}", "" if d is None else str(d), repr(rev), gift, note,
    ]))
put("orders.csv", "\n".join(rows) + "\n")

# A warehouse's stock count, exported with the column titles people
# typed: spaces, a currency sign and brackets, so a query has to quote
# them in backticks. Counts can be zero or negative (shrinkage found at
# the count), a cost is sometimes missing, and so is a bin.
r = Lcg(41)
items = ["hex bolt M6", "hex bolt M8", "washer M6", "wood screw 4x40", "cable tie 200",
         "wall plug 6", "hinge 75mm", "drawer slide", "shelf pin", "door stop",
         "cabinet knob", "corner brace", "tape measure", "utility knife", "glue 250ml",
         "sandpaper 120", "paint brush 2in", "masking tape", "drill bit 6mm", "zip bag"]
rows = ["sku,item name,on hand,reorder at,unit cost (€),last count,active,bin"]
for k, it in enumerate(items):
    on_hand = r.next(60) - 6
    reorder = [5, 10, 20, 25][r.next(4)]
    cost = "" if r.next(7) == 0 else f"{(5 + r.next(4000)) / 100}"
    count = f"2026-10-{1 + r.next(28):02d}"
    active = "False" if r.next(6) == 0 else "True"
    b = "" if r.next(8) == 0 else f"{'ABCD'[r.next(4)]}{1 + r.next(12)}"
    rows.append(f"SKU-{1000 + 7 * k},{it},{on_hand},{reorder},{cost},{count},{active},{b}")
put("inventory.csv", "\n".join(rows) + "\n")

# Hourly readings from four weather stations: temperatures below zero, a
# calm hour (wind 0), dry hours (rain 0) and gaps, for the math
# functions eval supports.
r = Lcg(5)
rows = ["station,hour,temp_c,pressure_hpa,wind_ms,wind_dir_deg,rain_mm"]
for st in ["harbour", "airport", "ridge", "valley"]:
    for h in range(0, 24, 4):
        t = (r.next(300) - 80) / 10
        p = 990 + r.next(400) / 10
        w = 0.0 if r.next(6) == 0 else r.next(180) / 10
        d = r.next(360)
        rain = 0.0 if r.next(3) else r.next(120) / 10
        cells = [st, str(h), f"{t}", f"{p}", f"{w}", str(d), f"{rain}"]
        if r.next(9) == 0:
            cells[2 + r.next(5)] = ""
        rows.append(",".join(cells))
put("readings.csv", "\n".join(rows) + "\n")

# A small ledger of integer pairs for the arithmetic rules: negative
# operands, zero divisors, and a float column beside them.
put("pairs.csv", "\n".join([
    "id,a,b,x",
    "p1,17,5,2.5",
    "p2,-17,5,-2.5",
    "p3,17,-5,0.0",
    "p4,-17,-5,1e-3",
    "p5,0,3,",
    "p6,9,0,4.0",
    "p7,0,0,-0.5",
    "p8,123456789,1000,1e6",
    "",
]))

# A staff list, read with the name as the index.
put("staff.csv", "\n".join([
    "id,name,dept,salary,start,remote,bio",
    "7,Zoë Martín,Engineering,98000,2019-04-01,True,Backend lead; owns the billing service and on-call rota",
    "12,Wang Fang,Engineering,105500,2021-09-15,False,Data platform",
    "15,Olga Petrova,Sales,72000,2018-01-08,True,EMEA accounts",
    "21,José Núñez,Support,51000,2023-06-19,False,",
    "30,Ana,Sales,68000,2024-02-01,True,New hire; shadowing the West region team",
    "31,Mohammed Al-Farsi,Support,53500,2022-11-30,True,Night shift",
    "",
]))

J = []


def job(s):
    J.append(s)


O = "read orders.csv"
I = "read inventory.csv"
R = "read readings.csv"
P = "read pairs.csv"
S = "read staff.csv index=name"

# --- comparisons and boolean logic
job(f"{O} | query units > 7 | head 8")
job(f"{O} | query units >= 8 and region == 'West'")
job(f"{O} | query units >= 8 & region == 'West'")
job(f"{O} | query units == 9 or units == 1 | head 6")
job(f"{O} | query (units == 9)|(units == 1) | head 6")
job(f"{O} | query (units == 9 or units == 1) and channel == 'web'")
job(f"{O} | query not gift and units > 8")
job(f"{O} | query ~gift & (units > 8)")
job(f"{O} | query gift")
job(f"{O} | query gift == True and region != 'North'")
job(f"{O} | query 3 < units <= 4 | head 6")
job(f"{O} | query 3 < units <= 4 < unit_price | head 6")
job(f"{O} | query units > 7 > 3 | head 3")
job(f"{O} | query unit_price > 100 and units >= 5")
job(f"{O} | query revenue < 30")
job(f"{O} | query revenue != revenue")
job(f"{O} | query discount > 0.1")
job(f"{O} | query discount != 0.1 | head 6")
job(f"{O} | query discount == discount and discount < 0.05 | head 6")
job(f"{O} | query 2 * units > revenue / 20 | head 5")
job(f"{O} | query -units < -8")
job(f"{O} | query units * unit_price > 1000")
job(f"{O} | query units // 3 == 2 and units % 2 == 1 | head 5")
job(f"{O} | query units ** 2 > 70 | head 4")
job(f"{O} | query order_id % 10 == 0")
job(f"{O} | query units > 100")
# --- strings and membership
job(f"{O} | query region == 'West' | head 5")
job(f'{O} | query region == "West" and product == "Scale"')
job(f"{O} | query region != 'West' | head 5")
job(f"{O} | query region == ['West', 'East'] and units == 9")
job(f"{O} | query region != ['West', 'East'] and units == 9")
job(f"{O} | query region in ['North', 'South'] and units == 9")
job(f"{O} | query region not in ('North', 'South') and units > 8")
job(f"{O} | query ['North', 'South'] in region and units == 9")
job(f"{O} | query units in [1, 9] and channel == 'phone'")
job(f"{O} | query units == [1, 9] and channel == 'phone'")
job(f"{O} | query 'web' == channel and units > 8")
job(f"{O} | query product > 'S' | head 5")
job(f"{O} | query product <= 'Blender' | head 5")
job(f"{O} | query note == 'repeat customer'")
job(f"{O} | query note != 'repeat customer' and units == 9")
job(f"{O} | query note in ['repeat customer', 'leave at the back door'] and units > 6")
job(f"{O} | query date == '2026-09-30'")
job(f"{O} | query date > '2026-09-27' and region == 'East'")
# --- methods on columns
job(f"{O} | query units > units.mean() and revenue > revenue.median() | head 6")
job(f"{O} | query revenue == revenue.max()")
job(f"{O} | query revenue == revenue.min() or units == units.max() | head 4")
job(f"{O} | query discount.isna() | head 6")
job(f"{O} | query discount.notna() and discount >= 0.15 | head 6")
job(f"{O} | query discount.fillna(0) == 0 and units > 7")
job(f"{O} | query units.between(4, 5) and channel == 'store' | head 6")
job(f"{O} | query units.isin([2, 3]) and product == 'Grinder'")
job(f"{O} | query product.str.startswith('K') and units > 6")
job(f"{O} | query product.str.endswith('er') and units == 9")
job(f"{O} | query note.str.contains('call', regex=False)")
job(f"{O} | query note.str.contains('back') | head 4")
job(f"{O} | query region.str.lower() == 'east' and units == 9")
job(f"{O} | query product.str.upper() == 'MUG SET' and units > 7")
job(f"{O} | query product.str.len() > 6 and units == 9")
job(f"{O} | query note.str.len() > 30")
job(f"{O} | query revenue.round(0) == 109")
job(f"{O} | query (revenue - units * unit_price).abs() > 40")
job(f"{O} | query abs(revenue - units * unit_price) > 40")
# --- locals
job(f"{O} | let lo=3 hi=4 | query units >= @lo and units < @hi and region == 'North'")
job(f"{O} | let regs=['West','North'] | query region in @regs and units == 9")
job(f"{O} | let want='Kettle' | query product == @want and units > 6")
job(f"{O} | let cap=1000.0 | query revenue > @cap * 0.9")
job(f"{O} | let units=100 | query units > @units")
job(f"{O} | let units=8 | query units > @units and @units < 9 | head 4")
job(f"{O} | query units > @limit")
job(f"{O} | query units > limit")
job(f"{O} | let n=2 | query units ** @n == 81 and channel == 'web'")
# --- backticks
job(f"{I} | query `on hand` < `reorder at`")
job(f"{I} | query `on hand` <= 0")
job(f"{I} | query `unit cost (€)` > 30")
job(f"{I} | query `unit cost (€)`.isna()")
job(f"{I} | query active and `on hand` < `reorder at` and bin.notna()")
job(f"{I} | query `item name`.str.contains('bolt') or `item name`.str.startswith('wood')")
job(f"{I} | query bin.str.startswith('A')")
job(f"{I} | query `last count` < '2026-10-08'")
job(f"{I} | eval value = `on hand` * `unit cost (€)` | select sku,value | head 8")
job(f"{I} | eval `to order` = `reorder at` - `on hand` | query `to order` > 0 | head 3")
# --- the index
job(f"{O} | query index < 3")
job(f"{O} | query index % 24 == 0")
job(f"{O} | query index >= 90 and units < 5")
job(f"{O} | query ilevel_0 == 50")
job(f"{O} | setidx order_id | query index > 10093")
job(f"{O} | setidx order_id | query order_id < 10003")
job(f"{O} | setidx region,channel | query region == 'East' and channel == 'phone' and units > 6")
job(f"{O} | setidx region,channel | query ilevel_0 == 'x'")
job(f"{S} | query name == 'Ana'")
job(f"{S} | query index.str.contains('a') and salary > 60000")
job(f"{S} | query dept == 'Sales' or remote == False")
job(f"{S} | query salary > salary.mean()")
job(f"{S} | query bio.isna()")
# --- eval: values
job(f"{O} | eval units * unit_price | head 5")
job(f"{O} | eval revenue / units | head 5")
job(f"{O} | eval units * 2 | head 3")
job(f"{O} | eval units > 5 | head 3")
job(f"{O} | eval -units | head 3")
job(f"{O} | eval +revenue | head 3")
job(f"{O} | eval ~gift | head 3")
job(f"{O} | eval not gift | head 3")
job(f"{O} | eval units + revenue * 2 - 1 | head 3")
job(f"{O} | eval (units + revenue) * 2 | head 3")
job(f"{O} | eval units ** 2 ** 2 | head 3")
job(f"{O} | eval -units ** 2 | head 3")
job(f"{O} | eval (-units) ** 2 | head 3")
job(f"{O} | eval units / 0 | head 2")
job(f"{O} | eval revenue.round(-1) | head 4")
job(f"{O} | eval discount.fillna(0) * revenue | head 4")
job(f"{O} | eval region + '/' + channel | head 4")
job(f"{O} | eval region * 2 | head 2")
job(f"{O} | eval units.sum()")
job(f"{O} | eval units.max() - units.min()")
job(f"{O} | eval 2 + 3 * 4")
job(f"{O} | eval 7 / 2")
job(f"{O} | eval 2 ** 10")
job(f"{O} | eval units.mean()")
job(f"{O} | eval revenue.sum() / units.sum()")
# --- integer arithmetic
job(f"{P} | eval a // b")
job(f"{P} | eval a % b")
job(f"{P} | eval a / b")
job(f"{P} | eval a ** 2")
job(f"{P} | eval b ** a")
job(f"{P} | eval a ** -1")
job(f"{P} | eval a // x")
job(f"{P} | eval a % x")
job(f"{P} | eval x ** 0.5")
job(f"{P} | eval -a // b")
job(f"{P} | eval a // 0")
job(f"{P} | eval a % 0")
job(f"{P} | eval a & b")
job(f"{P} | eval (a > 0) & (b > 0)")
job(f"{P} | eval a > 0 & b > 0")
job(f"{P} | eval a * 100000000000")
job(f"{P} | eval a - b * 3 + 7 // 2")
# --- eval: assignments
job(f"{O} | eval total = units * unit_price | select order_id,units,unit_price,total | head 5")
job(f"{O} | eval gross = units * unit_price ; saved = gross - revenue | select order_id,gross,saved,revenue | head 5")
job(f"{O} | eval units = units * 10 | select order_id,units | head 3")
job(f"{O} | eval big = units > 7 ; half = units / 2 | select order_id,big,half | head 4")
job(f"{O} | eval per = revenue / units ; per = per.round(1) | select per | head 4")
job(f"{O} | eval share = revenue / revenue.sum() | select order_id,share | head 4")
job(f"{O} | eval a = 1 | select order_id,a | head 2")
job(f"{O} | eval units * 2 ; b = 1")
job(f"{O} | query big = units > 7")
job(f"{O} | eval a = units ; units * 2")
# --- math functions
job(f"{R} | eval sqrt(wind_ms) | head 6")
job(f"{R} | eval log(rain_mm) | head 8")
job(f"{R} | eval log10(pressure_hpa) | head 4")
job(f"{R} | eval exp(temp_c / 10) | head 4")
job(f"{R} | eval sin(wind_dir_deg * 3.141592653589793 / 180) | head 6")
job(f"{R} | eval cos(wind_dir_deg * 3.141592653589793 / 180) | head 6")
job(f"{R} | eval arctan2(temp_c, wind_ms) | head 6")
job(f"{R} | eval floor(temp_c) | head 6")
job(f"{R} | eval ceil(temp_c) | head 6")
job(f"{R} | eval abs(temp_c) | head 6")
job(f"{R} | eval log1p(rain_mm) | head 6")
job(f"{R} | eval expm1(rain_mm / 10) | head 6")
job(f"{R} | eval tanh(temp_c / 10) | head 4")
job(f"{R} | eval east = wind_ms * sin(wind_dir_deg * 3.141592653589793 / 180) ; north = wind_ms * cos(wind_dir_deg * 3.141592653589793 / 180) | select station,hour,east,north | head 8")
job(f"{R} | query sqrt(wind_ms) > 3 and station == 'ridge'")
job(f"{R} | query temp_c < 0 and rain_mm > 0")
job(f"{R} | query temp_c != temp_c or pressure_hpa != pressure_hpa or wind_ms != wind_ms")
job(f"{R} | query floor(temp_c) == ceil(temp_c)")
job(f"{R} | eval round(temp_c)")
job(f"{R} | eval sqrt(x=temp_c)")
job(f"{R} | eval hypot(temp_c, wind_ms)")
# --- errors
job(f"{O} | query units ^ 2")
job(f"{O} | query units if gift else revenue")
job(f"{O} | query note is None")
job(f"{O} | query units > 5 and 2")
job(f"{O} | query nope == 1")
job(f"{O} | eval region - 1")
job(f"{O} | query region > 5")
job(f"{O} | query units > 'five'")
job(f"{O} | query @lo < units")
# --- display after query
job(f"{O} | query units == 9 | show max_rows=6")
job(f"{O} | query revenue > 600 | sort by=revenue asc=0 | select order_id,region,revenue")
job(f"{O} | query channel == 'web' and units > 6 | string index=0")
job(f"{O} | query units < 3 | select region,units,revenue | tail 4")

put("jobs.txt", "\n".join(J) + "\n")
