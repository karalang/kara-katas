"""Writes data/ for mini_pandas_calendar: the job list and the CSV files
the `due` and `bucket` jobs read.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)


def write(name, text):
    with open(os.path.join("data", name), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


# A help desk's tickets: opened around Thanksgiving, Christmas and New
# Year, some after hours and on weekends.
tickets = [
    ("T-1001", "2026-11-24 16:45:00", "P2"),
    ("T-1002", "2026-11-25 08:05:00", "P1"),
    ("T-1003", "2026-11-25 17:59:00", "P3"),
    ("T-1004", "2026-11-26 10:00:00", "P2"),
    ("T-1005", "2026-11-27 23:30:00", "P1"),
    ("T-1006", "2026-11-28 09:15:00", "P3"),
    ("T-1007", "2026-12-23 15:20:00", "P2"),
    ("T-1008", "2026-12-24 12:00:00", "P1"),
    ("T-1009", "2026-12-31 18:00:00", "P2"),
    ("T-1010", "2027-01-01 07:30:00", "P3"),
    ("T-1011", "2027-01-04 06:59:59", "P1"),
    ("T-1012", "2027-01-15 16:59:00", "P2"),
]
write("tickets.csv", "id,opened,priority\n" + "".join(f"{a},{b},{c}\n" for a, b, c in tickets))

# Invoices with their issue dates, for net-30 and month-end terms.
inv = [
    ("INV-2041", "2026-01-30", 1250.00),
    ("INV-2042", "2026-01-31", 980.50),
    ("INV-2043", "2026-02-27", 4410.00),
    ("INV-2044", "2026-02-28", 75.25),
    ("INV-2045", "2026-05-29", 610.00),
    ("INV-2046", "2026-06-30", 12000.00),
    ("INV-2047", "2026-08-31", 333.33),
    ("INV-2048", "2026-10-30", 870.00),
    ("INV-2049", "2026-11-30", 2290.10),
    ("INV-2050", "2026-12-31", 515.00),
]
write("invoices.csv", "invoice,issued,amount\n" + "".join(f"{a},{b},{c:.2f}\n" for a, b, c in inv))

# A shop's daily takings from July 2025 to December 2026, deterministic.
rows = []
import datetime as _dt
d = _dt.date(2025, 7, 1)
k = 0
while d <= _dt.date(2026, 12, 31):
    if d.weekday() != 6:  # closed on Sundays
        amt = 400 + (k * 37) % 290 + (150 if d.weekday() == 5 else 0)
        if d.month == 12:
            amt += 220
        rows.append(f"{d.isoformat()},{amt}.{(k * 13) % 100:02d},{1 + k % 3}\n")
    k += 1
    d += _dt.timedelta(days=1)
write("sales.csv", "date,amount,till\n" + "".join(rows))

# Trades with settlement on T+1 and T+2 around US market holidays.
trades = [
    ("2026-04-01", "AAPL", 100), ("2026-04-02", "MSFT", 50),
    ("2026-04-03", "AAPL", 25), ("2026-05-22", "NVDA", 10),
    ("2026-06-18", "MSFT", 70), ("2026-07-02", "AAPL", 40),
    ("2026-07-03", "NVDA", 15), ("2026-11-25", "MSFT", 20),
    ("2026-12-24", "AAPL", 60), ("2026-12-31", "NVDA", 5),
]
write("trades.csv", "trade_date,symbol,qty\n" + "".join(f"{a},{b},{c}\n" for a, b, c in trades))

# A payroll run's pay dates as HR typed them.
write("pay.csv", "period,paid\n" + "".join(
    f"{p},{q}\n" for p, q in [
        ("2026-01", "2026-01-15"), ("2026-01", "2026-01-30"),
        ("2026-02", "2026-02-13"), ("2026-02", "2026-02-27"),
        ("2026-05", "2026-05-15"), ("2026-05", "2026-05-29"),
        ("2026-08", "2026-08-14"), ("2026-08", "2026-08-31"),
        ("2026-11", "2026-11-13"), ("2026-11", "2026-11-30"),
    ]))

JOBS = """\
off 2026-11-25T16:30 BusinessHour(3)
off 2026-11-25T16:30 BusinessHour(-3)
off 2026-11-25T08:00 BusinessHour(1)
off 2026-11-27T17:00 BusinessHour(1)
off 2026-11-28T10:00 BusinessHour(2)
off 2026-11-25T16:30 BusinessHour(10)
off 2026-11-25T16:30 BusinessHour(3,start=22:00,end=06:00)
off 2026-11-25T23:30 BusinessHour(2,start=22:00,end=06:00)
off 2026-11-25T12:15 BusinessHour(2,start=[09:00;13:00],end=[12:00;17:00])
off 2026-11-25T16:30 BusinessHour(3,normalize=True)
off 2026-11-25T16:30 BusinessHour(1,offset=td:30min)
off 2026-11-25T16:30 BusinessDay(1,offset=td:2h)
off 2026-11-27T16:45 BusinessHour(1,offset=td:30min)
off 2026-11-25T16:30 CustomBusinessHour(3,cal=us)
off 2026-11-25T16:30 CustomBusinessHour(3,start=10:00,end=18:00,weekmask=1111000)
off 2026-12-24T17:30 CustomBusinessHour(1,cal=us,start=08:00,end=18:00)
off 2026-11-25T16:30 BusinessDay()
off 2026-11-27T16:30 BusinessDay()
off 2026-11-28 BusinessDay()
off 2026-11-28 BusinessDay(-1)
off 2026-11-28 BusinessDay(0)
off 2026-11-25T16:30 BusinessDay(5)
off 2026-11-25T16:30 BusinessDay(-13)
off 2026-11-25 BusinessDay(2,normalize=True)
off 2026-11-25T16:30 BusinessDay(2,normalize=True)
off 2026-11-25T16:30 CustomBusinessDay(cal=us)
off 2026-11-25 CustomBusinessDay(2,cal=nyse)
off 2026-04-02 CustomBusinessDay(1,cal=nyse)
off 2026-04-02 CustomBusinessDay(1,cal=uk)
off 2026-12-24 CustomBusinessDay(1,cal=uk)
off 2026-12-24 CustomBusinessDay(2,holidays=[2026-12-25;2026-12-28])
off 2026-12-24 CustomBusinessDay(1,weekmask=0111110)
off 2026-11-28 CustomBusinessDay(0,cal=us)
off 2026-01-15 MonthEnd()
off 2026-01-31 MonthEnd()
off 2026-01-31 MonthEnd(0)
off 2026-01-31 MonthEnd(-1)
off 2026-02-15 MonthBegin(2)
off 2026-01-30T09:00 BusinessMonthEnd()
off 2026-05-30 BusinessMonthEnd(0)
off 2026-05-30 BusinessMonthEnd(-1)
off 2026-08-01 BusinessMonthBegin()
off 2026-08-03 BusinessMonthBegin(-1)
off 2026-11-02 CustomBusinessMonthEnd(cal=us)
off 2026-12-01 CustomBusinessMonthBegin(cal=us)
off 2026-05-01 CustomBusinessMonthBegin(-1,cal=uk)
off 2026-02-10 SemiMonthEnd()
off 2026-02-15 SemiMonthEnd()
off 2026-02-20 SemiMonthEnd(day_of_month=20)
off 2026-02-28 SemiMonthEnd(-2)
off 2026-02-10 SemiMonthBegin()
off 2026-02-15 SemiMonthBegin(day_of_month=15)
off 2026-02-16 SemiMonthBegin(3,day_of_month=10)
off 2026-11-25 Week()
off 2026-11-25 Week(weekday=4)
off 2026-11-27 Week(weekday=4)
off 2026-11-27 Week(-1,weekday=4)
off 2026-11-25 Week(2,weekday=0)
off 2026-11-25 WeekOfMonth(week=2,weekday=3)
off 2026-11-19 WeekOfMonth(week=2,weekday=3)
off 2026-11-19 WeekOfMonth(-1,week=2,weekday=3)
off 2026-11-25 WeekOfMonth(week=0,weekday=0)
off 2026-11-25 LastWeekOfMonth(weekday=4)
off 2026-11-27 LastWeekOfMonth(weekday=4)
off 2026-11-27 LastWeekOfMonth(-2,weekday=4)
off 2026-05-15 QuarterEnd()
off 2026-05-15 QuarterEnd(startingMonth=2)
off 2026-06-30 QuarterEnd(-1)
off 2026-05-15 QuarterBegin()
off 2026-05-15 QuarterBegin(startingMonth=1)
off 2026-05-15 BQuarterEnd(startingMonth=6)
off 2026-03-31 BQuarterEnd(0,startingMonth=3)
off 2026-05-15 BQuarterBegin(startingMonth=2)
off 2026-05-15 YearEnd()
off 2026-05-15 YearEnd(month=6)
off 2026-12-31 YearEnd(-1)
off 2026-05-15 YearBegin(month=7)
off 2026-05-15 BYearEnd()
off 2026-05-15 BYearEnd(month=10)
off 2026-05-15 BYearBegin()
off 2026-05-15 HalfYearEnd()
off 2026-05-15 HalfYearBegin(startingMonth=4)
off 2026-05-15 BHalfYearEnd()
off 2026-05-15 FY5253(weekday=5,startingMonth=1,variation=last)
off 2026-05-15 FY5253(weekday=5,startingMonth=1,variation=nearest)
off 2026-01-31 FY5253(weekday=5,startingMonth=1,variation=last)
off 2027-01-30 FY5253(-1,weekday=5,startingMonth=1,variation=last)
off 2026-08-29 FY5253(weekday=5,startingMonth=8,variation=nearest)
off 2026-05-15 FY5253Quarter(weekday=5,startingMonth=1,qtr_with_extra_week=4,variation=last)
off 2026-05-15 FY5253Quarter(2,weekday=5,startingMonth=1,qtr_with_extra_week=4,variation=nearest)
off 2026-10-31 FY5253Quarter(-1,weekday=5,startingMonth=1,qtr_with_extra_week=4,variation=last)
off 2026-05-15 Easter()
off 2026-04-05 Easter()
off 2026-04-05 Easter(-1)
off 2026-01-31 DateOffset(months=1)
off 2026-01-31T10:00 DateOffset(months=1,days=-1)
off 2026-11-01 DateOffset(weekday=TH(4))
off 2026-05-31 DateOffset(weekday=MO(-1))
off 2026-11-25 DateOffset(2,months=1)
off 2026-11-25T16:30 DateOffset(hour=9,minute=0)
off 2024-02-29 DateOffset(years=1)
off 2026-11-25T16:30 DateOffset(days=1,normalize=True)
off 2026-11-25 DateOffset(month=13)
off 2026-11-25T16:30 Day(3)
off 2026-11-25T16:30 Hour(36)
off 2026-11-25T16:30 Minute(-90)
off 2026-11-25T16:30 Second(3600)
off 2026-11-25T16:30 Milli(1500)
off 2026-11-25T16:30 Micro(7)
off 2026-11-25T16:30 Nano(5)
off 2026-03-07T12:00@America/New_York Day(1)
off 2026-03-07T12:00@America/New_York Hour(24)
off 2026-03-07T12:00@America/New_York BusinessDay(1)
off 2026-10-31T12:00@America/New_York Week(weekday=6)
off 2026-03-08T01:30@America/New_York Hour(1)
off 2026-01-31T12:00@UTC MonthEnd()
freq 2h30min
freq 1D
freq -2BME
freq Q-JUN
freq QS-NOV
freq W-WED
freq WOM-1MON
freq LWOM-FRI
freq RE-N-DEC-FRI
freq REQ-L-JAN-SAT-4
freq SME-20
freq SMS
freq BYE-MAR
freq BYS
freq C
freq CBME
freq CBMS
freq 1.5h
freq 0.5D
freq 90s
freq 3us
freq 250ms
freq YE-MAR
freq YS
freq bh
freq cbh
freq B
freq h
freq 15min
freq M
freq Q
freq Y
freq A
freq H
freq T
freq S
freq BM
freq Q-FOO
freq W-XYZ
freq 2.5ME
freq 3QE-JUL
freq 0h
range start=2026-01-01 periods=6 freq=BME
range start=2026-01-01 end=2026-12-31 freq=QE-JUN
range start=2026-11-23T09:00 periods=10 freq=bh
range start=2026-11-23 end=2026-12-04 freq=W-FRI
range start=2026-01-01 end=2026-06-30 freq=SMS
range start=2026-01-01 end=2026-06-30 freq=SME
range start=2026-01-01 periods=12 freq=WOM-2TUE
range start=2025-01-01 periods=4 freq=RE-L-JAN-SAT
range start=2025-01-01 periods=8 freq=REQ-N-JAN-SAT-4
range end=2026-12-31 periods=5 freq=LWOM-FRI
range start=2026-03-07T12:00 periods=4 freq=D tz=America/New_York
range start=2026-03-07T12:00 periods=4 freq=24h tz=America/New_York
range start=2026-01-01 end=2026-01-10 freq=2D inclusive=left
range start=2026-01-01 end=2026-01-10 freq=3D inclusive=neither
range start=2026-01-01T10:30 periods=3 freq=D normalize=True
range start=2026-01-01 end=2026-03-01 periods=4
range start=2026-01-01 end=2026-03-01 periods=4 freq=D
range start=2026-01-01 periods=3 freq=M
range start=2026-01-31 periods=4 freq=-1ME
range start=2026-01-01 end=2025-12-01 freq=ME
range start=2026-01-01 periods=0 freq=D
range start=2026-01-01 periods=5 freq=1h30min
brange start=2026-11-20 end=2026-12-04
brange start=2026-11-20 end=2026-12-04 freq=C cal=us
brange start=2026-12-18 end=2027-01-08 freq=C holidays=[2026-12-25;2026-12-28;2027-01-01]
brange start=2026-11-20 end=2026-12-04 freq=C weekmask=1111000
brange start=2026-11-20 end=2026-12-04 holidays=[2026-11-26]
brange start=2026-11-20 periods=5 freq=C cal=nyse
brange start=2026-11-20 end=2026-11-27 freq=CBME cal=us
hol us 2026-01-01 2027-12-31
hol us 2021-06-01 2021-07-10
hol nyse 2026-01-01 2026-12-31
hol nyse 2027-01-01 2028-01-31
hol uk 2026-01-01 2026-12-31
hol uk 2027-01-01 2027-12-31
hol uk 2022-12-20 2023-01-10
hol us 2027-12-25 2028-01-05
hol us 1985-01-01 1986-02-01
per 2026-03 M
per 2026-03-15 Q-JUN
per 2026-03-15 Q-DEC
per 2026-03-15 Y-MAR
per 2026 Y
per 2026-11-25 W
per 2026-11-25 W-SAT
per 2026-11-25 D
per 2026-11-28 B
per 2026-11-25T16:30 h
per 2026-11-25T16:30:15 s
per 2026Q1 Q-JUN
per 2026Q4 Q
per 2024-02 M
per 2026-11-25 BME
per 2026-11-25 Y-FOO
pasfreq 2026-03 M Q-JUN e
pasfreq 2026Q3 Q-JUN M s
pasfreq 2026Q3 Q-JUN M e
pasfreq 2026Q3 Q-JUN D s
pasfreq 2026Q3 Q-JUN D e
pasfreq 2026Q3 Q-JUN Y-JUN e
pasfreq 2026Q3 Q-JUN Q-DEC e
pasfreq 2026 Y-MAR M s
pasfreq 2026 Y-MAR M e
pasfreq 2026-11-25 D W e
pasfreq 2026-11-28 D B e
pasfreq 2026-11-29 D B s
pasfreq 2026-11-29 D B e
pasfreq 2026-11-23/2026-11-29 W h e
pasfreq 2026-11-25 D h s
pasfreq 2026-11-25 D h e
pasfreq 2026-11-25 D s e
padd 2026-03 M 10
padd 2026Q3 Q-JUN 2
padd 2026Q1 Q-JUN -1
padd 2026-11-27 B 1
padd 2026 Y-MAR -3
padd 2026-11-25 W 6
pfmt 2026Q3 Q-JUN FY%F_Q%q
pfmt 2026Q3 Q-JUN %Y-%m-%d
pfmt 2026-03 M %b_%Y
pfmt 2026-11-25T16:30 h %d/%m/%Y_%H:%M
pfmt 2026-11-25 W %Y-W%W_%a
pfmt 2026 Y-MAR %F_%f_%Y_%y
pfmt 2026-11-25 D %j_%A_%B
pdiff 2026-01 2026-11 M
pdiff 2025Q3 2026Q4 Q-JUN
pdiff 2026-11-02 2026-11-30 B
prange start=2025Q3 end=2026Q2 freq=Q-JUN
prange start=2026-01 periods=6 freq=M
prange start=2026-11-23 end=2026-12-06 freq=W
prange start=2026-11-23 end=2026-11-30 freq=B
prange start=2025 end=2027 freq=Y-MAR
prange end=2026-12 periods=4 freq=2M
td 1_days_02:03:04
td 1h30m
td -1_days_+23:59:59.5
td P1DT2H
td 3W
td 1.5us
td 00:00:01.000000001
td 2_days
td -00:30:00
td 1d2h3m4s5ms6us7ns
td 1_day,_10:11:12
td 90_minutes
td 1.25h
td -1.5d
td 3w
td 1y
td 0
td 5
td bogus
td 1_days_25:00:00
td PT36H
td P0DT0H0M0.000001S
td 10000_days
td 106752_days
tdround 1_days_02:03:04.5 h floor
tdround 1_days_02:03:04.5 h ceil
tdround 1_days_02:30:00 h round
tdround 1_days_03:30:00 h round
tdround -1_days_+23:59:59.5 s round
tdround 1_days_02:03:04 D ceil
tdround 1_days_02:03:04 15min floor
tdround 1_days_02:03:04 ME floor
tsadd 2026-03-07T12:00@America/New_York 1_days
tsadd 2026-03-07T12:00@America/New_York 24h
tsadd 2026-11-25T16:30 -3_days_+01:00:00
tsadd 2026-12-31T23:59:59 1s
busday count 2026-11-01 2026-12-01
busday count 2026-11-01 2026-12-01 cal=us
busday count 2026-12-01 2026-11-01
busday count 2026-11-01 2026-12-01 weekmask=1111000
busday count 2026-11-28 2026-11-29
busday offset 2026-11-28 0 roll=forward
busday offset 2026-11-28 0 roll=backward
busday offset 2026-11-28 0 roll=following
busday offset 2026-11-26 1 roll=forward cal=us
busday offset 2026-11-26 -1 roll=backward cal=us
busday offset 2026-11-28 1 roll=modifiedfollowing
busday offset 2026-10-31 0 roll=modifiedfollowing
busday offset 2026-08-01 0 roll=modifiedpreceding
busday offset 2026-11-28 0
busday offset 2026-11-28 0 roll=nat
busday offset 2026-11-28 0 roll=sideways
busday is 2026-11-26
busday is 2026-11-26 cal=us
busday is 2026-11-26 weekmask=1111000
due tickets.csv opened add CustomBusinessHour(4,cal=us,start=08:00,end=18:00)
due tickets.csv opened add BusinessHour(8)
due tickets.csv opened rollforward CustomBusinessHour(cal=us,start=08:00,end=18:00)
due tickets.csv opened on BusinessHour()
due invoices.csv issued add DateOffset(days=30)
due invoices.csv issued add MonthEnd()
due invoices.csv issued add BusinessMonthEnd()
due invoices.csv issued rollforward CustomBusinessDay(cal=us)
due invoices.csv issued add CustomBusinessMonthEnd(cal=us)
due trades.csv trade_date add CustomBusinessDay(1,cal=nyse)
due trades.csv trade_date add CustomBusinessDay(2,cal=nyse)
due trades.csv trade_date sub BusinessDay(1)
due pay.csv paid on SemiMonthEnd()
due pay.csv paid rollforward SemiMonthEnd()
due pay.csv paid add Week(weekday=4)
bucket sales.csv date Q-JUN amount
bucket sales.csv date Y-JUN amount
bucket sales.csv date M amount
bucket sales.csv date W-SAT amount
bucket sales.csv date Q-DEC till
bucket sales.csv date ME amount
bucket sales.csv date RE-L-JAN-SAT amount
"""
write("jobs.txt", JOBS)
