"""Writes data/: the files the jobs read, each shaped like a real export,
and data/jobs.txt, one job per line. A job is a pipeline of steps
separated by " | "; the first step reads a file and the last one prints
the result, by default as print(df) prints it. oracle.py runs each job on
pandas, mini_pandas_display.kara on its own port.

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

# A lab's assay results: concentrations from parts per trillion to
# millions of units, a missing reading, negative blanks after background
# subtraction, and a flag column.
put("assay.csv", "\n".join([
    "sample,analyte,value,unit,flag",
    "S-001,lead,0.0000000124,g/L,",
    "S-001,nitrate,4.75,mg/L,",
    "S-001,coliform,1250000,CFU/100mL,high",
    "S-002,lead,0.00000035,g/L,",
    "S-002,nitrate,,mg/L,missing",
    "S-002,coliform,0,CFU/100mL,",
    "S-003,lead,-0.0000000008,g/L,blank",
    "S-003,nitrate,12.5,mg/L,",
    "S-003,coliform,38,CFU/100mL,",
    "S-004,lead,0.00000002,g/L,",
    "S-004,nitrate,0.125,mg/L,low",
    "S-004,coliform,3200000000,CFU/100mL,high",
    "",
]))

# A building's sensors as one wide table: a timestamp and 25 sensors, so
# the frame is wider than a line and wider than max_columns.
r = Lcg(7)
head = ["ts"] + [f"s{k:02d}" for k in range(1, 26)]
rows = [",".join(head)]
for h in range(12):
    vals = [f"2026-10-29T{h:02d}:00"]
    for k in range(25):
        v = 18 + r.next(9000) / 1000
        vals.append("" if r.next(40) == 0 else f"{v:.3f}")
    rows.append(",".join(vals))
put("sensors.csv", "\n".join(rows) + "\n")

# A staff list with names in several scripts (pandas measures width in
# code points, so wide characters do not line up), salaries, a remote
# flag and a free-text bio.
put("staff.csv", "\n".join([
    "id,name,dept,salary,start,remote,bio",
    "7,Zoë Martín,Engineering,98000,2019-04-01,True,Backend lead; owns the billing service and on-call rota",
    "12,王芳,Engineering,105500,2021-09-15,False,Data platform",
    "15,Ольга Петрова,Sales,72000,2018-01-08,True,EMEA accounts",
    "21,José Ñúñez,Support,51000,2023-06-19,False,",
    "30,Ana,Sales,68000,2024-02-01,True,New hire; shadowing the West region team until the end of the quarter",
    "31,Mohammed Al-Farsi,Support,53500,2022-11-30,True,Night shift",
    "",
]))

# A department budget: planned amounts in whole currency units, actual
# spend with cents, three years and four quarters.
r = Lcg(99)
rows = ["dept,year,quarter,category,planned,actual"]
for dept in ["Ops", "R&D", "Sales"]:
    for year in [2024, 2025, 2026]:
        for q in ["Q1", "Q2", "Q3", "Q4"]:
            if year == 2026 and q == "Q4":
                continue
            for cat in ["staff", "travel"]:
                planned = (40 + r.next(60)) * 1000 if cat == "staff" else (2 + r.next(8)) * 500
                actual = round(planned * (0.8 + r.next(40000) / 100000), 2)
                rows.append(f"{dept},{year},{q},{cat},{planned},{actual}")
put("budget.csv", "\n".join(rows) + "\n")

# A few rows at the edges of number formatting: zeros, a negative zero,
# values that need all six digits, big integers, and one huge float.
put("edges.csv", "\n".join([
    "name,count,ratio,big,mixed",
    "a,0,0.1,9007199254740993,1.5",
    "b,-3,0.25,123456789012,-0.0",
    "c,12,100.0,-42,0.333333333",
    "d,7,0.1234565,0,12345678.9",
    "",
]))

J = []


def job(*s):
    J.append(" | ".join(s))


# print(df) as pandas prints it outside a terminal: max_rows 60 and
# min_rows 10, max_columns 20, width 80, max_colwidth 50, precision 6.
job("read edges.csv")
job("read assay.csv")
job("read staff.csv")
job("read orders.csv")
job("read sensors.csv")
job("read budget.csv")
job("read orders.csv", "head 8")
job("read orders.csv", "tail 3")
job("read orders.csv", "select order_id,units,gift")
job("read orders.csv", "select region,product", "head 4")
job("read orders.csv", "where units > 100")
job("read orders.csv", "where units > 100", "col units")
job("read orders.csv", "where units > 8", "select order_id,region,revenue")
job("read orders.csv", "where region == 'South'", "where channel == 'store'")
job("read orders.csv", "col nope")
job("read orders.csv", "select units,nope")

# The display options.
job("read orders.csv", "show max_rows=20")
job("read orders.csv", "show max_rows=20 min_rows=4")
job("read orders.csv", "show max_rows=20 min_rows=1")
job("read orders.csv", "show max_rows=20 min_rows=0")
job("read orders.csv", "show max_rows=None")
job("read orders.csv", "select order_id,revenue", "show max_rows=3")
job("read orders.csv", "select order_id,revenue", "show max_rows=1")
job("read orders.csv", "select order_id,revenue", "show max_rows=95")
job("read orders.csv", "select order_id,revenue", "show max_rows=96")
job("read orders.csv", "head 5", "show max_colwidth=20")
job("read orders.csv", "head 5", "show max_colwidth=3")
job("read orders.csv", "head 5", "show max_colwidth=None")
job("read orders.csv", "head 5", "show width=60")
job("read orders.csv", "head 5", "show width=20")
job("read orders.csv", "head 5", "show expand_frame_repr=0")
job("read orders.csv", "head 5", "show precision=2")
job("read orders.csv", "head 5", "show colheader_justify=left")
job("read orders.csv", "head 5", "show show_dimensions=1")
job("read orders.csv", "show show_dimensions=0")
job("read sensors.csv", "show max_columns=6")
job("read sensors.csv", "show max_columns=7")
job("read sensors.csv", "show max_columns=2")
job("read sensors.csv", "show max_columns=1")
job("read sensors.csv", "show max_columns=None width=100")
job("read sensors.csv", "show max_columns=None width=200")
job("read sensors.csv", "show max_columns=8 max_rows=6")
job("read edges.csv", "show colheader_justify=left")
job("read edges.csv", "show colheader_justify=center")
job("read edges.csv", "show show_dimensions=1")
job("read edges.csv", "show precision=2")
job("read edges.csv", "show precision=0")
job("read edges.csv", "show precision=10")

# The float rules: one format per column, trailing zeros trimmed the same
# way down the column, and scientific notation when a value would show
# as zero or a large value makes the column too wide.
job("read assay.csv", "show precision=3")
job("read assay.csv", "where analyte == 'nitrate'")
job("read assay.csv", "where analyte == 'coliform'")
job("read assay.csv", "where analyte == 'lead'")
job("read assay.csv", "where analyte == 'lead'", "mul value 1000000")
job("read assay.csv", "where analyte == 'lead'", "mul value 1000000000")
job("read assay.csv", "where analyte == 'coliform'", "mul value 0.001")
job("read assay.csv", "where analyte == 'coliform'", "where value < 10000000")
job("read assay.csv", "where analyte == 'nitrate'", "show precision=1")
job("read assay.csv", "where analyte == 'nitrate'", "mul value 100000")
job("read assay.csv", "where analyte == 'nitrate'", "mul value 1000000")
job("read assay.csv", "where analyte == 'nitrate'", "mul value 0.00001")
job("read orders.csv", "head 6", "div per_unit revenue units")
job("read orders.csv", "head 6", "div per_unit revenue units", "round 3")
job("read edges.csv", "div r ratio count")
job("read edges.csv", "div r count count")
job("read edges.csv", "round 1")
job("read edges.csv", "round 0")
job("read edges.csv", "mul ratio 3")

# Series: values, an index and a footer with the name, the length when
# truncated and the dtype.
job("read orders.csv", "col revenue")
job("read orders.csv", "col note")
job("read orders.csv", "col gift", "head 4")
job("read orders.csv", "col units", "head 4")
job("read orders.csv", "col discount", "head 7")
job("read orders.csv", "col region", "tail 3")
job("read orders.csv", "col revenue", "show max_rows=4")
job("read orders.csv", "col revenue", "show max_rows=4 min_rows=2")
job("read orders.csv", "col revenue", "show max_rows=1")
job("read orders.csv", "col revenue", "sort asc=0", "head 5")
job("read orders.csv", "counts region")
job("read orders.csv", "counts discount")
job("read orders.csv", "counts product")
job("read orders.csv", "share channel")
job("read orders.csv", "share discount")
job("read staff.csv", "col name")
job("read staff.csv", "col bio", "show max_colwidth=12")
job("read staff.csv", "setidx name", "col salary")

# Indexes: a named index, several levels shown sparsely, numbers in the
# index, and the column index's own name.
job("read staff.csv", "setidx name")
job("read staff.csv", "setidx id", "select name,salary")
job("read edges.csv", "setidx ratio")
job("read edges.csv", "setidx big", "select name,mixed")
job("read budget.csv", "select dept,year,planned", "setidx dept,year", "head 6")
job("read budget.csv", "setidx dept,year,quarter,category", "head 10")
job("read budget.csv", "setidx dept,year,quarter,category", "head 10", "show multi_sparse=0")
job("read budget.csv", "setidx dept,year,quarter,category", "tail 5")
job("read budget.csv", "setidx year,dept", "sortidx", "head 9")
job("read budget.csv", "setidx dept,year", "sortidx asc=0", "select planned", "head 7")
job("read budget.csv", "setidx dept,year,quarter,category")
job("read budget.csv", "setidx dept,year,quarter,category", "show max_rows=8")
job("read budget.csv", "setidx dept,year", "select planned", "reset", "head 3")
job("read orders.csv", "sort by=revenue asc=0", "head 5", "select order_id,revenue")
job("read orders.csv", "sort by=region,revenue asc=1,0", "head 6", "select region,revenue")
job("read orders.csv", "sort by=region,units", "select region,units", "show max_rows=10")

# Grouped results.
job("read orders.csv", "agg region n=units:count,mean=revenue:mean")
job("read orders.csv", "agg region,channel n=units:count,units=units:sum,revenue=revenue:sum")
job("read orders.csv", "agg region,channel n=units:count", "reset")
job("read orders.csv", "agg product top=revenue:max,low=revenue:min,gifts=gift:sum")
job("read orders.csv", "agg channel d=discount:mean,dmax=discount:max")
job("read orders.csv", "size region,channel")
job("read orders.csv", "size region")
job("read orders.csv", "size region,channel", "show max_rows=6")
job("read orders.csv", "size region,channel", "show multi_sparse=0")
job("read orders.csv", "size region,channel", "unstack")
job("read orders.csv", "where units > 7", "size region,product", "unstack")
job("read orders.csv", "agg region,channel units=units:sum", "unstack")
job("read orders.csv", "agg region,channel units=units:sum,rev=revenue:sum", "unstack")
job("read orders.csv", "where units > 7", "agg region,product units=units:sum", "unstack")
job("read orders.csv", "size region,channel", "unstack", "stack")
job("read orders.csv", "agg region,channel units=units:sum,rev=revenue:sum", "unstack", "stack")
job("read orders.csv", "agg region n=units:count,rev=revenue:sum", "stack")
job("read orders.csv", "agg region n=units:count,rev=revenue:sum", "T")
job("read edges.csv", "select name,ratio", "setidx name", "stack")

# pivot_table: a column index with a name, several levels of it, margins.
job("read budget.csv", "pivot index=dept columns=year values=actual agg=sum")
job("read budget.csv", "pivot index=dept columns=year values=planned agg=sum")
job("read budget.csv", "pivot index=dept columns=year values=planned agg=mean")
job("read budget.csv", "pivot index=dept columns=year values=planned agg=count")
job("read budget.csv", "pivot index=dept columns=year values=actual agg=max")
job("read budget.csv", "pivot index=dept,category columns=year values=planned agg=sum margins=1")
job("read budget.csv", "pivot index=dept columns=year values=actual agg=mean margins=1")
job("read budget.csv", "pivot index=dept columns=quarter values=planned,actual agg=sum")
job("read budget.csv", "pivot index=dept columns=category values=actual agg=sum,mean")
job("read budget.csv", "pivot index=year columns=dept values=actual agg=mean", "round 1")
job("read budget.csv", "pivot index=year,quarter columns=dept values=planned agg=sum")
job("read budget.csv", "pivot index=year,quarter columns=dept values=planned agg=sum fill=0")
job("read budget.csv", "where year == 2026", "pivot index=quarter columns=dept values=actual agg=sum")
job("read budget.csv", "pivot index=dept columns=year values=planned agg=sum", "stack")
job("read budget.csv", "pivot index=dept columns=year values=planned agg=sum", "T")
job("read budget.csv", "pivot index=dept columns=year values=planned agg=sum", "reset")
job("read orders.csv", "pivot index=region columns=channel values=revenue agg=sum", "round 0")
job("read orders.csv", "pivot index=product columns=region values=units agg=sum margins=1")

# Transposed frames: every column holds mixed values, so it is printed
# value by value.
job("read edges.csv", "T")
job("read staff.csv", "T")
job("read edges.csv", "describe")
job("read orders.csv", "describe")
job("read orders.csv", "describe", "T")
job("read budget.csv", "describe")
job("read assay.csv", "describe")
job("read staff.csv", "describe")
job("read staff.csv", "select salary,remote", "T")

# to_string: the same engine with its own arguments, and no line width
# unless one is given.
job("read orders.csv", "head 5", "string")
job("read orders.csv", "head 5", "string index=0")
job("read orders.csv", "head 5", "string header=0")
job("read orders.csv", "head 5", "string header=0 index=0")
job("read orders.csv", "head 5", "string float_format=%.1f na_rep=-")
job("read orders.csv", "head 5", "string float_format=%.3e")
job("read orders.csv", "head 5", "string float_format=%08.2f")
job("read orders.csv", "head 5", "string na_rep=\\e")
job("read orders.csv", "head 5", "string col_space=12 justify=left")
job("read orders.csv", "head 5", "string col_space=12 justify=center")
job("read orders.csv", "head 5", "string justify=right")
job("read orders.csv", "head 5", "string line_width=70")
job("read orders.csv", "head 5", "string line_width=0")
job("read orders.csv", "string max_rows=6 show_dimensions=1")
job("read orders.csv", "string max_rows=6 min_rows=2")
job("read orders.csv", "head 5", "string max_cols=4")
job("read orders.csv", "head 5", "string max_cols=4 show_dimensions=truncate")
job("read orders.csv", "head 5", "string decimal=,")
job("read orders.csv", "head 5", "string max_colwidth=10")
job("read assay.csv", "string float_format=%.4g")
job("read assay.csv", "string decimal=,")
job("read budget.csv", "setidx dept,year", "head 5", "string sparsify=0")
job("read budget.csv", "setidx dept,year", "head 5", "string index_names=0")
job("read budget.csv", "pivot index=dept columns=year values=planned agg=sum", "string index_names=0")
job("read budget.csv", "pivot index=dept columns=quarter values=planned,actual agg=sum", "string sparsify=0")
job("read budget.csv", "pivot index=dept columns=quarter values=planned,actual agg=sum", "string line_width=60")
job("read orders.csv", "col revenue", "string max_rows=6")
job("read orders.csv", "col revenue", "head 4", "string name=1 dtype=1")
job("read orders.csv", "col revenue", "head 4", "string index=0")
job("read orders.csv", "col revenue", "head 4", "string header=0 length=1")
job("read orders.csv", "col discount", "head 6", "string na_rep=n/a float_format=%.2f")
job("read orders.csv", "size region,channel", "string")

put("jobs.txt", "\n".join(J) + "\n")
