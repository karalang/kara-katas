"""Writes data/: the CSV files the jobs read, and data/jobs.txt, one job per
line. A job is a pipeline of steps separated by " | "; the first step reads
a file. oracle.py runs each job on pandas, mini_pandas.kara on its own port.

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


# A shop's order export: a missing quantity, missing discounts, a price
# with more digits than a float holds exactly, an accented customer.
put("orders.csv", """order_id,date,region,customer,product,qty,unit_price,discount,status
1001,2026-03-02,east,acme,widget,4,2.99,0.1,shipped
1002,2026-03-02,west,globex,gadget,1,19.5,,shipped
1003,2026-03-03,east,initech,widget,10,2.99,0.15,pending
1004,2026-03-04,north,acme,gizmo,2,7.25,,shipped
1005,2026-03-04,west,umbrella,widget,,2.99,,cancelled
1006,2026-03-05,east,globex,gizmo,3,7.25,0.05,shipped
1007,2026-03-06,south,acme,gadget,2,19.5,,returned
1008,2026-03-06,north,initech,doohickey,6,0.75,0.2,shipped
1009,2026-03-07,east,umbrella,gadget,1,18.25,,shipped
1010,2026-03-08,west,acme,widget,12,2.79,0.1,pending
1011,2026-03-09,south,globex,doohickey,25,0.75,0.25,shipped
1012,2026-03-09,east,Zoë & Co,gizmo,1,7.0,,shipped
1013,2026-03-10,north,umbrella,widget,8,2.99,0.1,returned
1014,2026-03-11,south,initech,gadget,3,19.5,0.05,shipped
1015,2026-03-11,west,hooli,gizmo,5,7.25,,shipped
1016,2026-03-12,east,acme,doohickey,40,0.7,0.3,shipped
1017,2026-03-13,north,globex,widget,7,2.99,,pending
1018,2026-03-13,south,umbrella,gizmo,2,7.25,0.1,shipped
1019,2026-03-14,east,initech,gadget,,19.5,,cancelled
1020,2026-03-15,west,acme,gadget,4,18.25,0.05,shipped
""")

# The CRM's customer table: "hooli" appears twice (a data-quality bug the
# merges then multiply), "wayne" has no orders, and Zoë & Co is missing.
put("customers.csv", """customer,segment,country,since
acme,enterprise,US,2019
globex,smb,DE,2021
initech,enterprise,US,2018
umbrella,smb,UK,2020
hooli,startup,US,2024
hooli,startup,US,2025
wayne,enterprise,US,2017
""")

# Returns: one refers to an order that does not exist.
put("returns.csv", """order_id,reason,refund
1007,damaged,39.0
1013,wrong item,23.92
1020,late,
1099,unknown,5.5
""")

# The next quarter's export, with a column the first one lacks.
put("orders_q2.csv", """order_id,date,region,customer,product,qty,unit_price,discount,status,channel
2001,2026-04-01,east,acme,widget,3,2.99,,shipped,web
2002,2026-04-01,west,wayne,gizmo,9,7.25,0.1,shipped,phone
2003,2026-04-02,south,globex,gadget,1,19.5,,pending,web
""")

# Three sensors over eight days, a reading lost here and there.
put("readings.csv", """sensor,day,temp,humidity
s1,1,20.5,40
s1,2,21.0,42
s1,3,,41
s1,4,22.25,45
s1,5,21.75,44
s1,6,23.5,47
s1,7,24.0,
s1,8,22.5,43
s2,1,18.0,55
s2,2,18.5,57
s2,3,19.25,56
s2,4,19.25,58
s2,5,19.25,60
s2,6,20.0,59
s2,7,,61
s2,8,21.5,62
s3,1,-2.5,80
s3,2,-1.0,82
s3,3,0.5,81
s3,4,-0.5,79
s3,5,1.5,78
s3,6,3.0,77
s3,7,2.5,76
s3,8,4.0,75
""")

# Staff: salary ties for the ranks, a duplicated row, a missing manager.
put("staff.csv", """name,dept,salary,start,manager
ana,eng,120000,2019,
ben,eng,95000,2021,ana
chen,eng,95000,2022,ana
dara,ops,70000,2020,eli
eli,ops,88000,2016,
fay,sales,64000,2023,gus
gus,sales,91000,2015,
hal,eng,135000,2014,
ida,ops,70000,2022,eli
ben,eng,95000,2021,ana
jo,sales,58000,2024,gus
""")

# A survey on a 1-5 scale; respondents skip questions.
put("survey.csv", """respondent,team,q1,q2,q3,q4
r1,red,5,4,4,3
r2,red,3,,4,2
r3,blue,4,4,5,5
r4,blue,2,3,,1
r5,green,5,5,5,4
r6,red,1,2,3,
r7,green,4,3,4,4
""")

# An access log, tab-separated.
put("web.tsv", "ts\tpath\tstatus\tbytes\tms\n" + "".join(
    "\t".join(r) + "\n" for r in [
        ("09:00:01", "/", "200", "5120", "12.5"),
        ("09:00:02", "/api/orders", "200", "830", "48.25"),
        ("09:00:02", "/api/orders", "500", "120", "1203.0"),
        ("09:00:03", "/static/app.js", "200", "88123", "3.0"),
        ("09:00:05", "/api/users", "404", "64", "7.75"),
        ("09:00:06", "/api/orders", "200", "910", "52.5"),
        ("09:00:08", "/", "304", "0", "1.25"),
        ("09:00:09", "/API/Orders", "200", "850", "49.0"),
        ("09:00:11", "/static/app.css", "200", "20480", "2.5"),
        ("09:00:12", "/api/orders", "503", "0", "3001.5"),
        ("09:00:12", "/api/users", "200", "1500", "22.0"),
        ("09:00:14", "/health", "200", "2", "0.5"),
    ]))

# A European export: semicolons, and "-" for a missing value.
put("semi.csv", """city;temp;rain
Berlin;12.5;-
Paris;14;2.5
Madrid;-;0
Rome;18.25;1
""")

# Every spelling read_csv has an opinion on, one column each.
put("types.csv", "\n".join([
    'ints,lead,signs,floats,exps,bools,yesno,mixed,gaps,quoted',
    '1,007,+3,1.5,1e3,True,yes,10,1,"a, b"',
    '2,010,-4,.5,2.5E-2,False,no,x,,"say ""hi"""',
    '3,000,+0,5.,inf,TRUE,yes,30,3,plain',
    '4,100,-0,-0.0,-inf,false,no,40,4,',
]) + "\n")

# An empty data set: a header and no rows.
put("header_only.csv", "a,b,c\n")

# ------------------------------------------------------------ jobs
JOBS = []


def job(*steps):
    JOBS.append(" | ".join(steps))


O = "read orders.csv"
S = "read staff.csv"
R = "read readings.csv"
W = "read web.tsv sep=tab"

# Reading and types.
job("read types.csv | dtypes")
job("read types.csv")
job("read orders.csv | dtypes")
job("read semi.csv sep=; na=-")
job("read semi.csv sep=; na=- | dtypes")
job("read semi.csv sep=;")
job("read customers.csv usecols=customer,since")
job("read survey.csv header=none | head 3")
job("read header_only.csv | dtypes")
job("read header_only.csv")
job("read types.csv dtype=lead:str,ints:float | select ints,lead")
job("read types.csv keep_default_na=0 na=yes | select yesno,gaps")
job("read missing.csv")
job(W + " | dtypes")

# Selecting and filtering.
job(O + " | head 3")
job(O + " | tail 2")
job(O + " | select order_id,customer,qty | head 4")
job(O + " | drop date,discount,status | head 3")
job(O + " | rename unit_price:price,qty:units | head 2")
job(O + " | where qty > 5 | select order_id,qty")
job(O + " | where qty <= 2 | select order_id,qty")
job(O + " | where region == 'east' | select order_id,customer")
job(O + " | where status != 'shipped' | select order_id,status")
job(O + " | where unit_price >= 7.25 | where qty < 4 | select order_id,product,qty")
job(O + " | isna qty | select order_id,status")
job(O + " | notna discount | select order_id,discount")
job(O + " | isin product gizmo,gadget | select order_id,product")
job(O + " | isin qty 1,2,40 | select order_id,qty")
job(O + " | contains customer co case=0 | select order_id,customer")
job(O + " | contains customer Co | select customer")
job(W + " | contains path /api | select path,status")
job(W + " | contains path orders case=0 | select path")
job(W + " | startswith path /static | select path,bytes")
job(W + " | where status >= 500 | select ts,path,ms")
job(W + " | between ms 2.5 49.0 | select path,ms")
job(O + " | where qty > @discount | select order_id")
job(O + " | select nope")
job(O + " | where nope > 1")

# New columns.
job(O + " | assign total = qty * unit_price | select order_id,qty,unit_price,total")
job(O + " | assign net = unit_price - discount | select order_id,unit_price,discount,net")
job(O + " | assign half = qty / 2 | select order_id,qty,half | head 6")
job(O + " | assign big = qty + 1000 | assign ratio = big / qty | select order_id,big,ratio | head 5")
job(O + " | assign t = qty * unit_price | round t 1 | select order_id,t")
job(O + " | assign t = qty * unit_price | round t 0 | select order_id,t | head 6")
job(R + " | round temp 0 | select sensor,day,temp | head 8")
job(O + " | upper region | lower customer | select region,customer | head 4")
job(O + " | len customer clen | select customer,clen | head 5")
job(W + " | strip path | lower path | counts path")
job(O + " | astype qty str | select qty | head 6")
job(O + " | fillna qty 0 | astype qty int | select order_id,qty")
job(O + " | astype order_id float | select order_id | head 3")
job(R + " | clip temp 0 22 | select sensor,day,temp")
job(R + " | abs temp | where sensor == 's3' | select day,temp")

# Missing values.
job(O + " | fillna discount 0 | select order_id,discount | head 6")
job(O + " | fillna qty 1 | select order_id,qty | head 6")
job(O + " | dropna | select order_id")
job(O + " | dropna subset=qty | select order_id,qty")
job("read survey.csv | dropna")
job("read survey.csv | dropna how=all")
job("read survey.csv | dropna subset=q2,q3")
job(R + " | ffill temp | select sensor,day,temp")
job(R + " | bfill humidity | select sensor,day,humidity")
job("read semi.csv sep=; na=- | fillna temp 0 | fillna rain 0")

# Sorting and duplicates.
job(O + " | sort qty | select order_id,qty")
job(O + " | sort qty asc=0 | select order_id,qty")
job(O + " | sort qty na=first | select order_id,qty | head 4")
job(O + " | sort region,qty asc=1,0 | select region,order_id,qty")
job(O + " | sort customer,unit_price | select customer,unit_price,order_id")
job(O + " | sort status asc=0 | select order_id,status")
job(S + " | sort salary,name asc=0,1")
job(S + " | dedup")
job(S + " | dedup subset=dept | select name,dept")
job(S + " | dedup subset=dept keep=last | select name,dept")
job(S + " | dedup subset=salary keep=false | select name,salary")
job(S + " | sort start | dedup subset=dept | select dept,name,start")

# Grouping.
job(O + " | agg region qty:sum,unit_price:mean")
job(O + " | agg region qty:count,qty:size,order_id:count")
job(O + " | agg product qty:min,qty:max,unit_price:median")
job(O + " | agg customer qty:mean,qty:std,qty:var")
job(O + " | agg region,product qty:sum")
job(O + " | agg status customer:nunique,customer:first,customer:last")
job(O + " | agg region customer:min,customer:max")
job(O + " | agg region discount:sum,discount:mean,discount:count")
job(O + " | assign total = qty * unit_price | agg customer total:sum | sort total_sum asc=0")
job(O + " | assign total = qty * unit_price | agg region,status total:sum,total:mean")
job(O + " | size region")
job(O + " | size region,status")
job(S + " | agg dept salary:mean,salary:median,salary:std,name:count")
job(S + " | agg dept manager:first,manager:count,manager:nunique")
job(R + " | agg sensor temp:mean,temp:min,temp:max,temp:std,humidity:median")
job(R + " | agg sensor temp:sum,temp:var")
job("read survey.csv | agg team q1:mean,q2:mean,q3:mean,q4:mean")
job(W + " | agg path ms:mean,bytes:sum,status:max")
job(O + " | agg region nope:sum")
job(O + " | agg region qty:bogus")
job(O + " | transform region qty sum region_qty | select order_id,region,qty,region_qty")
job(O + " | transform product unit_price mean avg_price | select order_id,product,unit_price,avg_price")
job(O + " | transform customer order_id count n | select customer,n | head 8")
job(S + " | transform dept salary max top | assign gap = top - salary | select name,dept,salary,gap")
job(S + " | transform dept salary min floor | select name,floor")
job(R + " | gcumsum sensor temp cum | select sensor,day,temp,cum")
job(R + " | gshift sensor temp 1 prev | select sensor,day,temp,prev")
job(R + " | gshift sensor temp -1 next | select sensor,day,next | head 9")
job(R + " | gdiff sensor temp delta | select sensor,day,delta")

# Merging and concatenating.
job(O + " | merge customers.csv on=customer | select order_id,customer,segment,country")
job(O + " | merge customers.csv on=customer how=left | select order_id,customer,segment")
job(O + " | merge customers.csv on=customer how=right | select order_id,customer,since")
job(O + " | merge customers.csv on=customer how=outer | select order_id,customer,segment")
job(O + " | merge returns.csv on=order_id | select order_id,customer,reason,refund")
job(O + " | merge returns.csv on=order_id how=outer | select order_id,status,reason,refund")
job(O + " | merge returns.csv on=order_id how=left | where status == 'returned' | select order_id,reason")
job(O + " | select order_id,customer | merge customers.csv left_on=customer right_on=customer how=inner | head 4")
job("read staff.csv | dedup | merge staff.csv left_on=manager right_on=name suffixes=,_mgr | select name,manager,salary,salary_mgr")
job("read customers.csv | merge customers.csv on=country | select customer_x,customer_y | head 6")
job(O + " | concat orders_q2.csv | select order_id,qty,channel | tail 5")
job(O + " | concat orders_q2.csv | dtypes")
job("read orders_q2.csv | concat returns.csv | select order_id,qty,reason")
job(O + " | merge nope.csv on=customer")
job(O + " | merge customers.csv on=nope")

# Reshaping.
job(O + " | pivot index=region columns=product values=qty agg=sum")
job(O + " | pivot index=region columns=product values=qty agg=sum fill=0")
job(O + " | pivot index=customer columns=status values=order_id agg=count fill=0")
job(O + " | pivot index=product columns=region values=unit_price agg=mean")
job(R + " | pivot index=day columns=sensor values=temp agg=mean")
job("read survey.csv | melt id=respondent vars=q1,q2")
job("read survey.csv | melt id=respondent,team | head 10")
job("read survey.csv | melt id=respondent vars=q1,q2,q3,q4 var=question value=score | dropna | agg question score:mean,score:count")
job("read survey.csv | melt id=team vars=q1,q3 | pivot index=team columns=variable values=value agg=max")
job(O + " | crosstab region status")
job(S + " | crosstab dept start")

# Windows.
job(R + " | where sensor == 's1' | rolling temp 3 mean avg | select day,temp,avg")
job(R + " | where sensor == 's1' | rolling temp 3 mean avg min=1 | select day,temp,avg")
job(R + " | where sensor == 's2' | rolling temp 3 sum tot min=2 | select day,temp,tot")
job(R + " | where sensor == 's3' | rolling temp 2 mean avg | select day,temp,avg")
job(R + " | where sensor == 's2' | rolling humidity 4 max hi | rolling humidity 4 min lo | select day,humidity,hi,lo")
job(R + " | where sensor == 's1' | rolling humidity 3 count n | select day,humidity,n")
job(R + " | where sensor == 's1' | cumsum temp cum | cummax temp peak | select day,temp,cum,peak")
job(R + " | where sensor == 's1' | shift temp 2 lag | select day,temp,lag")
job(R + " | where sensor == 's2' | diff temp d | pct temp p | select day,temp,d,p")
job(O + " | cumsum qty running | select order_id,qty,running")

# Ranks and counts.
job(S + " | rank salary r | select name,salary,r")
job(S + " | rank salary r method=min desc | select name,salary,r")
job(S + " | rank salary r method=dense desc | select name,salary,r")
job(S + " | rank salary r method=first | select name,salary,r")
job(S + " | rank salary r method=max | select name,salary,r")
job(O + " | rank qty r | select order_id,qty,r")
job(O + " | rank customer r method=dense | select customer,r | head 6")
job(O + " | counts region")
job(O + " | counts product norm")
job(O + " | counts qty")
job(S + " | counts dept")
job(W + " | counts status")
job(O + " | counts nope")

# Summaries.
job(O + " | describe")
job(R + " | describe")
job(S + " | describe")
job(W + " | select status,ms | describe")
job(O + " | quantile qty,unit_price 0.1,0.5,0.9")
job(R + " | quantile temp 0.25,0.75")

put("jobs.txt", "\n".join(JOBS) + "\n")
print(len(JOBS), "jobs")
