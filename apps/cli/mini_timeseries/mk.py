"""Writes data/: the CSV files the jobs read, and data/jobs.txt, one job per
line. A job is a pipeline of steps separated by " | "; the first step reads
a file (or builds a date range). oracle.py runs each job on pandas,
mini_timeseries.kara on its own port.

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
    """A small deterministic generator, so the data never changes."""

    def __init__(self, seed):
        self.s = seed

    def next(self):
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) % (1 << 64)
        return self.s >> 33

    def below(self, n):
        return self.next() % n


def two(n):
    return "%02d" % n


# Host metrics from a monitoring agent, in UTC with a trailing Z: three
# hosts sampled about every 20 minutes from Saturday evening to Monday
# morning, across the night the US clocks go forward (2026-03-08 07:00Z).
# A few samples are lost, and a few report no CPU figure.
r = Lcg(7)
rows = ["ts,host,cpu,mem,req"]
for host, base in (("web1", 30), ("web2", 45), ("db1", 60)):
    t = 20 * 60  # minutes after 2026-03-07 00:00Z
    while t < (2 * 24 + 6) * 60:
        if r.below(13) != 0:
            day, rest = divmod(t, 24 * 60)
            h, m = divmod(rest, 60)
            sec = r.below(60)
            cpu = "" if r.below(17) == 0 else "%d.%d" % (base + r.below(40) - 15, r.below(10))
            mem = 2000 + base * 10 + r.below(500)
            req = r.below(400) if host != "db1" else r.below(40)
            rows.append("2026-03-%sT%s:%s:%sZ,%s,%s,%d,%d" % (two(7 + day), two(h), two(m), two(sec), host, cpu, mem, req))
        t += 20 + r.below(3) - 1
put("metrics.csv", "\n".join(rows) + "\n")

# Trades on two symbols in the first 45 minutes of a session, to the
# millisecond, local exchange time with no zone.
r = Lcg(11)
rows = ["ts,sym,price,qty"]
px = {"KRA": 101.25, "MND": 47.5}
ms = (9 * 3600 + 30 * 60) * 1000
while ms < (10 * 3600 + 15 * 60) * 1000:
    sym = "KRA" if r.below(3) else "MND"
    px[sym] = round(px[sym] + (r.below(41) - 20) / 100, 2)
    qty = (r.below(20) + 1) * 10
    s, frac = divmod(ms, 1000)
    h, rest = divmod(s, 3600)
    m, sec = divmod(rest, 60)
    rows.append("2026-03-02 %s:%s:%s.%03d,%s,%.2f,%d" % (two(h), two(m), two(sec), frac, sym, px[sym], qty))
    ms += r.below(90000) + 250
put("trades.csv", "\n".join(rows) + "\n")

# A shop's daily takings in two stores over the first four months of a
# leap year; the stores close on some days, and one day's figure is lost.
r = Lcg(5)
rows = ["date,store,amount"]
mdays = [31, 29, 31, 30]
for store in ("north", "south"):
    for mo in range(4):
        for d in range(1, mdays[mo] + 1):
            if r.below(9) == 0:
                continue
            amt = "" if (store, mo, d) == ("south", 1, 14) else "%d.%02d" % (200 + r.below(900), r.below(100))
            rows.append("2024-%s-%s,%s,%s" % (two(mo + 1), two(d), store, amt))
put("sales.csv", "\n".join(rows) + "\n")

# Support tickets with Unix-time creation and close stamps; open ones
# have no close stamp.
r = Lcg(3)
rows = ["id,created,closed,prio"]
t = 1772323200  # 2026-03-01 00:00:00Z
for i in range(40):
    t += r.below(20000) + 600
    closed = "" if r.below(6) == 0 else str(t + r.below(200000) + 60)
    rows.append("%d,%d,%s,%s" % (5000 + i, t, closed, "P%d" % (r.below(3) + 1)))
put("tickets.csv", "\n".join(rows) + "\n")

# A US-style export: month/day/year with a 12-hour clock... and two cells
# that are not dates at all.
put("visits.csv", """visit,when,clinic
1,03/01/2026 08:15,east
2,03/01/2026 09:40,west
3,03/02/2026 13:05,east
4,03/04/2026 16:30,east
5,13/45/2026 10:00,west
6,03/09/2026 07:55,west
7,03/09/2026 18:20,east
8,03/10/2026 12:00,west
9,,east
10,03/15/2026 23:59,west
11,03/16/2026 00:01,east
12,03/31/2026 11:11,west
""")

# Meter readings at irregular moments: a cumulative register, to be put
# on a regular grid and differenced.
put("meter.csv", """at,kwh
2026-01-30 22:10:00,15000.5
2026-01-31 23:50:00,15012.25
2026-02-02 06:30:00,15030.0
2026-02-05 12:00:00,15071.75
2026-02-06 00:00:00,15078.0
2026-02-10 09:45:00,15130.5
2026-02-28 18:00:00,15333.25
2026-03-01 00:00:00,15336.0
""")

# ------------------------------------------------------------ jobs
JOBS = []


def job(*steps):
    JOBS.append(" | ".join(steps))


M = "read metrics.csv dates=ts"
T = "read trades.csv dates=ts"
S = "read sales.csv dates=date"
K = "read tickets.csv dates=created,closed unit=s"
V = "read visits.csv dates=when format=%m/%d/%Y_%H:%M coerce"
E = "read meter.csv dates=at"

# Reading and parsing.
job(M + " | dtypes")
job(M + " | head 4")
job(T + " | dtypes")
job(T + " | head 3")
job(S + " | head 3")
job(S + " | dtypes")
job(K + " | head 4")
job(K + " | dtypes")
job(V)
job(V + " | dtypes")
job("read visits.csv dates=when format=%m/%d/%Y_%H:%M")
job("read meter.csv | dtypes")
job(E)

# Date parts.
job(S + " | dt date year y | dt date month m | dt date day d | head 4")
job(S + " | dt date dayofweek dow | dt date day_name name | head 7")
job(S + " | dt date quarter q | dt date dayofyear doy | dt date is_month_end me | where me == True")
job(S + " | dt date week w | dt date is_month_start ms | head 9")
job(S + " | dt date month_name mn | agg mn amount:sum | sort amount_sum asc=0")
job(M + " | dt ts hour h | dt ts minute mi | dt ts second s | head 5")
job(T + " | dt ts microsecond us | head 4")
job(V + " | dt when hour h | dt when dayofweek dow | select visit,when,h,dow")

# Rounding and formatting.
job(M + " | floor ts h t | select ts,t | head 5")
job(M + " | ceil ts 15min t | select ts,t | head 5")
job(M + " | dtround ts h t | select ts,t | head 6")
job(T + " | floor ts s t | dtround ts min r | select ts,t,r | head 5")
job(S + " | strftime date %Y-%m m | agg m amount:sum,amount:count")
job(S + " | strftime date %d/%m/%Y f | strftime date %a_%b_%d f2 | strftime date %j doy | head 3")
job(M + " | strftime ts %Y-%m-%dT%H:%M h | head 3")
job(S + " | normalize date d | head 2")
job(M + " | normalize ts d | agg host,d cpu:mean,req:sum")

# Filtering by time.
job(M + " | where ts >= '2026-03-08_06:00' | where ts < '2026-03-08_08:00' | where host == 'web1' | select ts,cpu")
job(S + " | where date > '2024-02-27' | where date <= '2024-03-02' | select date,store,amount")
job(K + " | isna closed | select id,created")
job(V + " | isna when | select visit,clinic")
job(T + " | between_time ts 09:40 09:45 | select ts,sym,price")
job(M + " | between_time ts 23:50 00:10 | where host == 'db1' | select ts,mem")

# Durations.
job(K + " | sub closed created took | select id,took | head 6")
job(K + " | sub closed created took | secs took s | agg prio s:mean,s:max,s:count")
job(K + " | tdiff created gap | select id,created,gap | head 5")
job(K + " | sub closed created took | where took > '2_days' | select id,took")
job(E + " | tdiff at gap | secs gap s")

# Resampling.
job(T + " | resample ts 5min price:last,qty:sum")
job(T + " | resample ts 5min price:mean,price:count,qty:max")
job(T + " | where sym == 'KRA' | resample ts 10min price:first,price:min,price:max,price:last")
job(T + " | where sym == 'MND' | ohlc ts 15min price")
job(T + " | assign value = price * qty | resample ts 15min value:sum,qty:sum | assign vwap = value_sum / qty_sum | round vwap 4")
job(T + " | resample ts 15min price:median,price:std,qty:mean by=sym")
job(T + " | resample ts 10min qty:sum by=sym")
job(M + " | where host == 'web2' | resample ts 3h cpu:mean,req:sum,mem:max")
job(M + " | resample ts 6h req:sum,cpu:count by=host")
job(M + " | resample ts 6h cpu:mean closed=right label=right by=host | round cpu_mean 3")
job(M + " | resample ts 4h req:sum origin=epoch | head 5")
job(M + " | resample ts 4h req:sum offset=1h | head 5")
job(S + " | where store == 'north' | resample date W amount:sum,amount:count")
job(S + " | resample date W-MON amount:sum by=store | head 8")
job(S + " | resample date ME amount:sum,amount:mean by=store | round amount_mean 2")
job(S + " | resample date MS amount:sum,amount:max")
job(S + " | resample date QE amount:sum,amount:count by=store")
job(S + " | resample date YE amount:sum")
job(S + " | resample date 10D amount:sum | head 6")
job(S + " | where store == 'south' | resample date 2W amount:sum")
job(S + " | where store == 'south' | resample date SME amount:sum")
job(K + " | resample created D id:count,prio:first | head 8")
job(K + " | resample closed 12h id:count")
job(V + " | resample when D visit:count")
job(E + " | resample at D kwh:last | head 6")
job(E + " | resample at ME kwh:min,kwh:max")

# Regular grids.
job(E + " | asfreq at D | head 6")
job(E + " | asfreq at D ffill | head 8")
job(E + " | asfreq at D bfill | tail 3")
job(E + " | floor at D day | asfreq day D | head 4")
job(E + " | asfreq at 12h | head 4")
job(S + " | where store == 'north' | asfreq date D | isna amount | select date,store")
job("range 2026-03-01 2026-03-03 8h | dt t day_name name")
job("range 2024-01-31 2024-06-30 ME")
job("range 2024-02-26 2024-03-04 D | dt t week w | dt t dayofweek dow")
job("range 2026-01-01 2026-12-31 QS")
job("range 2026-03-07 2026-03-21 W-SAT")

# Time windows.
job(T + " | where sym == 'KRA' | trolling ts 2min price mean avg | round avg 4 | head 10")
job(T + " | trolling ts 5min qty sum vol | select ts,qty,vol | head 10")
job(T + " | trolling ts 90s qty count n | select ts,n | head 8")
job(M + " | where host == 'db1' | trolling ts 1h cpu max peak | select ts,cpu,peak | head 8")
job(S + " | where store == 'north' | trolling date 7D amount sum wk | round wk 2 | head 10")
job(S + " | where store == 'south' | trolling date 3D amount mean avg | round avg 2 | head 12")

# Time zones.
job(M + " | tz ts convert America/New_York | head 3")
job(M + " | tz ts convert America/New_York | where host == 'web1' | where ts >= '2026-03-08_00:40-05:00' | head 6")
job(M + " | tz ts convert America/New_York | dt ts hour h | where host == 'web2' | agg h req:sum | head 8")
job(M + " | tz ts convert America/New_York | resample ts D req:sum,cpu:count")
job(M + " | tz ts convert America/New_York | resample ts 6h req:sum | head 6")
job(M + " | tz ts convert America/New_York | normalize ts d | agg d req:sum")
job(M + " | tz ts convert UTC | head 2")
job(T + " | tz ts localize America/New_York | tz ts convert UTC | head 3")
job(V + " | tz when localize America/New_York | select visit,when | head 8")
job(M + " | tz ts convert America/New_York | strftime ts %Y-%m-%d_%H:%M_%Z f | select f | head 2")
job("range 2026-03-07 2026-03-10 D tz=America/New_York")
job("range 2026-11-01 2026-11-02 6h tz=America/New_York")

# Errors.
job(M + " | resample ts 1fortnight req:sum")
job(M + " | resample host h req:sum")
job(S + " | dt amount year y")
job("read sales.csv dates=nope")
job(M + " | tz ts localize America/New_York")

put("jobs.txt", "\n".join(JOBS) + "\n")
