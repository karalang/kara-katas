"""Writes data/: the files the jobs read, and data/jobs.txt, one mlr run
per line with its arguments separated by tabs.

The files are written out by hand to reach the corners of Miller's
readers (CSV quoting, a byte-order mark, CRLF, ragged rows, duplicate
header names, TSV escapes, DKVP lines with missing keys, whitespace-split
NIDX), its type inference (hex, leading zeros, signs, exponents, a value
past the int64 range) and its writers.

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


# An order export: four regions, four products, a missing quantity, an
# accented customer name (pprint and xtab pad by characters, not bytes).
put("orders.csv", """id,date,region,customer,product,qty,price,status
1001,2026-01-03,east,acme,widget,4,2.50,shipped
1002,2026-01-03,west,globex,gadget,1,19.99,shipped
1003,2026-01-04,east,initech,widget,10,2.50,pending
1004,2026-01-05,north,acme,gizmo,2,7.25,shipped
1005,2026-01-05,west,umbrella,widget,,2.50,cancelled
1006,2026-01-06,east,globex,gizmo,3,7.25,shipped
1007,2026-01-07,south,acme,gadget,2,19.99,returned
1008,2026-01-07,north,initech,doohickey,6,0.75,shipped
1009,2026-01-08,east,umbrella,gadget,1,18.5,shipped
1010,2026-01-09,west,acme,widget,12,2.4,pending
1011,2026-01-10,south,globex,doohickey,25,0.75,shipped
1012,2026-01-10,east,Zoë & co,gizmo,1,7,shipped
1013,2026-01-11,north,umbrella,widget,8,2.50,returned
1014,2026-01-12,south,initech,gadget,3,19.99,shipped
""")

# The customer list the joins read; "hooli" places no orders.
put("customers.csv", """customer,tier,since
acme,gold,2019
globex,silver,2021
initech,gold,2018
hooli,bronze,2024
umbrella,silver,2020
""")

# Readings in every numeric spelling Miller's scanner has an opinion on.
put("sensors.csv", """sensor,reading,unit,note
s1,1.5,C,ok
s1,-0.25,C,ok
s2,+3,C,signed
s2,1e3,C,spike
s3,.5,C,ok
s3,5.,C,ok
s4,0x1F,raw,hex
s4,007,raw,leading zero
s5,,C,missing
s5,n/a,C,text
s6,9223372036854775807,raw,int64 max
s6,10,raw,overflows the sum
s6,1_000,raw,underscore
s7,-12,C,ok
s7,2.5E-2,C,ok
s7,99999999999999999999,raw,past int64
""")

# Quoting: a byte-order mark, CRLF line ends, separators, doubled quotes,
# a field over two lines, a pipe for markdown, a tab for TSV.
put("quoted.csv", "﻿" + "\r\n".join([
    'name,quote,n',
    'plain,hello,1',
    '"comma, inside","say ""hi""",2',
    'multi,"line one',
    'line two",3',
    'pipe,a|b,4',
    'tab,"x\ty",5',
    'empty,,6',
]) + "\r\n")

put("dupes.csv", """a,b,a,a
1,2,3,4
5,6,7,8
""")

# Row 4 is short, row 5 is long: an error without --allow-ragged-csv-input.
put("ragged.csv", """k,x,y
a,1,2
b,3,4
c,5
d,6,7,8
e,9,10
""")

put("regions.tsv", "region\tmanager\ttarget\n"
    "east\tKim\\tLee\t1200\n"
    "west\tSam\\nO'Neil\t900\n"
    "north\tAl\\\\Bo\t700\n"
    "south\tJo\t\n")

put("bad.tsv", "a\tb\tc\n1\t2\t3\n4\t5\n6\t7\t8\n")

put("events.dkvp", """t=1700000000,user=ann,action=login,ms=12
t=1700000060,user=bob,action=view,ms=48,page=home
t=1700000090,user=ann,action=view,ms=33,page=cart
t=1700000120,user=cy,action=login
t=1700000150,user=bob,action=buy,ms=91,page=cart,amount=19.99
t=1700000200,ms=7,user=ann,action=logout
lonely,user=dee,x
""")

put("words.txt", """alpha beta  gamma
  delta	epsilon
zeta eta theta iota

kappa
""")

put("semi.csv", """city;temp;rain
Oslo;-3.5;0.2
Lima;22;0
Pune;31.25;
""")

put("nested.csv", """id,user.name,user.age,tags.1,tags.2,geo.lat,geo.lon,meta,list
1,ann,31,red,blue,59.9,10.7,{},[]
2,bob,,green,,48.8,2.35,{},x
""")

put("visits.csv", """page,user
home,ann
cart,bob
home,ann
home,cy
cart,bob
home,ann
""")

put("scores.csv", """name,q1,q2,q3,q4
ann,7,9,,8
bob,5,6,7,n/a
cy,9,9.5,10,8.5
dee,4,0x10,3,2
""")

put("flows.csv", """host,bytes_in,bytes_out,pkts_in,pkts_out
a,100,250,4,6
b,300,,9,12
c,0,40,0,2
""")

put("tags.csv", """id,tags,attrs
1,red;green;blue,size:L;fit:slim
2,solo,color:red
3,,
""")

put("times.csv", """id,t,ms
1,0,0
2,1500000000,1500000000123
3,1700000000.75,1700000000999
4,-86400,-1000
5,soon,
""")

put("header_only.csv", "a,b,c\n")
put("empty.csv", "")

# ------------------------------------------------------------ jobs
JOBS = []


def job(*argv):
    JOBS.append("\t".join(argv))


O = "data/orders.csv"
S = "data/sensors.csv"
E = "data/events.dkvp"

# Formats.
job("--icsv", "--opprint", "cat", O)
job("--icsv", "--ojson", "head", "-n", "2", O)
job("--icsv", "--ojsonl", "head", "-n", "3", "then", "cut", "-f", "id,customer,price", O)
job("--icsv", "--ojson", "--jvstack", "--no-jlistwrap", "head", "-n", "2", "then", "cut", "-f", "id,qty", O)
job("--icsv", "--ojson", "--no-jvstack", "tail", "-n", "2", O)
job("--icsv", "--oxtab", "head", "-n", "2", O)
job("--icsv", "--oxtab", "--xvright", "head", "-n", "3", "then", "cut", "-f", "id,customer,qty,price", O)
job("--icsv", "--oxtab", "--ops", "colon", "head", "-n", "1", O)
job("--c2p", "--barred", "head", "-n", "4", "then", "cut", "-f", "id,region,qty", O)
job("--c2p", "--right", "head", "-n", "4", "then", "cut", "-f", "id,customer,price", O)
job("--c2p", "--barred", "--right", "head", "-n", "3", "then", "cut", "-f", "id,customer,qty", O)
job("--icsv", "--omd", "cat", "data/quoted.csv")
job("--icsv", "--otsv", "cat", "data/quoted.csv")
job("--icsv", "--ocsv", "cat", "data/quoted.csv")
job("--icsv", "--ojson", "cat", "data/quoted.csv")
job("--icsv", "--ocsv", "--quote-all", "head", "-n", "2", "then", "cut", "-f", "id,customer", O)
job("--icsv", "--odkvp", "head", "-n", "2", O)
job("--icsv", "--onidx", "--ofs", "space", "head", "-n", "3", "then", "cut", "-f", "id,customer,qty", O)
job("--c2t", "head", "-n", "2", O)
job("--c2d", "head", "-n", "2", O)
job("--c2j", "head", "-n", "1", O)
job("--c2n", "head", "-n", "2", O)
job("--c2m", "head", "-n", "2", "then", "cut", "-f", "id,status", O)
job("--icsv", "--opprint", "cat", "data/dupes.csv")
job("--icsv", "--implicit-csv-header", "--ocsv", "head", "-n", "2", O)
job("--icsv", "--headerless-csv-output", "--ocsv", "head", "-n", "2", O)
job("--icsv", "--hi", "--ho", "--ocsv", "tail", "-n", "1", "data/visits.csv")
job("--icsv", "--allow-ragged-csv-input", "--ojson", "cat", "data/ragged.csv")
job("--icsv", "--opprint", "cat", "data/ragged.csv")
job("--icsv", "--opprint", "cat", "data/ragged.csv", "data/visits.csv")
job("--itsv", "--ojson", "cat", "data/regions.tsv")
job("--itsv", "--otsv", "cat", "data/regions.tsv")
job("--itsv", "--opprint", "cat", "data/bad.tsv")
job("--itsv", "--allow-ragged-csv-input", "--ocsv", "cat", "data/bad.tsv")
job("--idkvp", "--ojson", "cat", E)
job("--opprint", "cat", E)
job("--ocsv", "cat", E)
job("--ocsv", "unsparsify", E)
job("--oxtab", "unsparsify", "--fill-with", "-", "then", "head", "-n", "2", E)
job("--inidx", "--ocsv", "cat", "data/words.txt")
job("--inidx", "--ifs", "space", "--ojson", "head", "-n", "2", "data/words.txt")
job("--inidx", "--ifs", "space", "--repifs", "--onidx", "--ofs", "comma", "cat", "data/words.txt")
job("--icsv", "--ifs", "semicolon", "--opprint", "cat", "data/semi.csv")
job("--csv", "--fs", "semicolon", "cat", "data/semi.csv")
job("--icsv", "--ojson", "cat", "data/nested.csv")
job("--icsv", "--ojson", "--no-auto-unflatten", "head", "-n", "1", "data/nested.csv")
job("--icsv", "--ojsonl", "cat", "data/nested.csv")
job("--icsv", "--opprint", "cat", "data/header_only.csv")
job("--icsv", "--ojson", "cat", "data/empty.csv")
job("--icsv", "--ocsv", "cat", O, "data/customers.csv")
job("--icsv", "--opprint", "cat", O, "data/customers.csv")
job("--from", O, "--icsv", "--opprint", "head", "-n", "2", "then", "cut", "-f", "id,qty")
job("--c2p", "cat", "-n", "-g", "region", "then", "head", "-n", "6", O)
job("--c2p", "cat", "-N", "idx", "--filename", "--filenum", "data/visits.csv", "data/customers.csv")

# Types: the sort orders and sums only make sense with Miller's inference.
job("--icsv", "--opprint", "sort", "-nr", "reading", S)
job("--icsv", "--opprint", "sort", "-nf", "reading", S)
job("--icsv", "--opprint", "sort", "-f", "reading", S)
job("--icsv", "--opprint", "sort", "-f", "sensor", "-nr", "reading", S)
job("--icsv", "--ojson", "head", "-n", "8", "then", "cut", "-f", "reading", S)
job("--icsv", "--opprint", "stats1", "-a", "count,sum,mean,min,max", "-f", "reading", "-g", "sensor", S)
job("--icsv", "--opprint", "stats1", "-a", "count,null_count,distinct_count,mode,antimode,minlen,maxlen", "-f", "reading,note", S)
job("--icsv", "--opprint", "stats1", "-a", "min,max,p50", "-f", "reading", S)

# Sorting and selecting.
job("--icsv", "--opprint", "sort", "-f", "region", "-nr", "qty", O)
job("--icsv", "--opprint", "sort", "-nf", "price", "-f", "id", "then", "cut", "-f", "id,product,price", O)
job("--icsv", "--opprint", "sort", "-c", "customer", "then", "cut", "-f", "id,customer", O)
job("--icsv", "--opprint", "sort", "-cr", "customer", "then", "cut", "-f", "id,customer", O)
job("--icsv", "--opprint", "sort", "-r", "status", "-n", "id", "then", "cut", "-f", "id,status", O)
job("--opprint", "sort", "-f", "page", E)
job("--icsv", "--opprint", "head", "-n", "1", "-g", "region", "then", "cut", "-f", "id,region,customer", O)
job("--icsv", "--opprint", "tail", "-n", "2", "-g", "product", "then", "cut", "-f", "id,product", O)
job("--icsv", "--opprint", "tac", "then", "head", "-n", "3", O)
job("--icsv", "--ocsv", "cut", "-o", "-f", "price,id,nosuch", O)
job("--icsv", "--ocsv", "cut", "-x", "-f", "date,status,price", O)
job("--icsv", "--ocsv", "cut", "-r", "-f", "^(i|pr)", O)
job("--icsv", "--ocsv", "cut", "-r", "-f", '"^ID$"i,qty', "then", "head", "-n", "3", O)
job("--icsv", "--ocsv", "cut", "-x", "-r", "-f", "e", "then", "head", "-n", "2", O)
job("--opprint", "having-fields", "--at-least", "ms,page", E)
job("--opprint", "having-fields", "--which-are", "t,user,action", E)
job("--opprint", "having-fields", "--at-most", "t,user,action,ms", E)
job("--opprint", "having-fields", "--any-matching", "^am", E)
job("--opprint", "having-fields", "--all-matching", "^[a-z]+$", E)
job("--opprint", "having-fields", "--none-matching", "^p", E)
job("--icsv", "--opprint", "decimate", "-n", "4", O)
job("--icsv", "--opprint", "decimate", "-n", "2", "-b", "-g", "region", "then", "cut", "-f", "id,region", O)
job("--icsv", "--opprint", "grep", "-i", "ACME", O)
job("--icsv", "--opprint", "grep", "-v", "shipped", O)
job("--icsv", "--opprint", "grep", "-a", "^100[3-5],", O)
job("--icsv", "--opprint", "grep", "region=north", O)

# Counting and grouping.
job("--icsv", "--opprint", "count", O)
job("--icsv", "--opprint", "count", "-g", "region", O)
job("--icsv", "--opprint", "count", "-n", "-g", "customer", O)
job("--icsv", "--opprint", "count", "-o", "orders", "-g", "region,product", O)
job("--icsv", "--opprint", "count-distinct", "-f", "region,status", O)
job("--icsv", "--opprint", "count-distinct", "-n", "-f", "customer", O)
job("--icsv", "--opprint", "count-distinct", "-u", "-f", "region,product", O)
job("--icsv", "--opprint", "count-similar", "-g", "customer", "then", "cut", "-f", "id,customer,count", O)
job("--icsv", "--opprint", "uniq", "-g", "region,status", O)
job("--icsv", "--opprint", "uniq", "-g", "region", "-c", O)
job("--icsv", "--opprint", "uniq", "-g", "region", "-n", O)
job("--icsv", "--opprint", "uniq", "-x", "page", "-c", "data/visits.csv")
job("--icsv", "--opprint", "uniq", "-a", "data/visits.csv")
job("--icsv", "--opprint", "uniq", "-a", "-c", "data/visits.csv")
job("--icsv", "--opprint", "uniq", "-a", "-n", "data/visits.csv")
job("--icsv", "--opprint", "group-by", "region", O)
job("--opprint", "group-like", E)
job("--icsv", "--opprint", "top", "-n", "2", "-f", "price", "-g", "region", O)
job("--icsv", "--opprint", "top", "-n", "3", "-f", "qty", "--min", "-o", "rank", O)
job("--icsv", "--opprint", "top", "-f", "qty,price", O)
job("--icsv", "--opprint", "top", "-n", "1", "-f", "price", "-g", "product", "-a", O)

# Statistics.
job("--icsv", "--opprint", "stats1", "-a", "count,sum,mean,min,max", "-f", "qty,price", "-g", "region", O)
job("--icsv", "--opprint", "stats1", "-a", "p10,p25.2,median,p75,p90", "-f", "qty,price", O)
job("--icsv", "--opprint", "stats1", "-i", "-a", "p25,median,p75", "-f", "qty,price", O)
job("--icsv", "--oxtab", "stats1", "-a", "var,stddev,meaneb,kurtosis,mad", "-f", "qty,price", O)
job("--icsv", "--opprint", "stats1", "-a", "mean,var", "-f", "qty", "-g", "product,region", O)
job("--icsv", "--opprint", "stats1", "-a", "sum,count", "--fr", "^(qty|price)$", "-g", "status", O)
job("--icsv", "--opprint", "stats1", "-a", "max", "--fx", "^(id|qty|price)$", O)
job("--icsv", "--opprint", "stats1", "-a", "first", "-f", "qty", O)
job("--icsv", "--opprint", "stats1", "-f", "qty", O)
job("--icsv", "--opprint", "merge-fields", "-a", "min,max,sum", "-f", "q1,q2,q3,q4", "-o", "all", "data/scores.csv")
job("--icsv", "--opprint", "merge-fields", "-k", "-a", "sum,count,mean", "-r", "^q[12]$", "-o", "h1", "data/scores.csv")
job("--icsv", "--opprint", "merge-fields", "-a", "sum,max", "-c", "_in,_out", "data/flows.csv")
job("--icsv", "--opprint", "merge-fields", "-k", "-a", "sum", "-c", "bytes_,pkts_", "data/flows.csv")
job("--icsv", "--opprint", "merge-fields", "-a", "nope", "-f", "q1", "-o", "x", "data/scores.csv")
job("--icsv", "--opprint", "fraction", "-f", "price", O)
job("--icsv", "--opprint", "fraction", "-f", "price", "-g", "region", "-p", "-c", "then", "cut", "-f", "id,region,price,price_cumulative_percent", O)
job("--icsv", "--opprint", "fraction", "-f", "bytes_in,pkts_out", "data/flows.csv")

# Steps.
job("--icsv", "--opprint", "step", "-a", "delta,shift,from-first,ratio,rsum,rprod,counter", "-f", "q1", "data/scores.csv")
job("--icsv", "--opprint", "step", "-a", "delta,rsum,counter", "-f", "qty", "-g", "region", "then", "cut", "-f", "id,region,qty,qty_delta,qty_rsum,qty_counter", O)
job("--icsv", "--opprint", "step", "-a", "shift_lag,shift_lead", "-f", "price", "then", "cut", "-f", "id,price,price_shift_lag,price_shift_lead", O)
job("--icsv", "--opprint", "step", "-a", "ewma", "-d", "0.1,0.9", "-f", "q1", "data/scores.csv")
job("--icsv", "--opprint", "step", "-a", "ewma", "-d", "0.5", "-o", "half", "-f", "q1,q3", "data/scores.csv")
job("--icsv", "--opprint", "step", "-a", "slwin_1_1,shift_lead", "-f", "price", "-g", "region", "then", "cut", "-r", "-f", "^(id|region|price)", O)
job("--icsv", "--opprint", "step", "-a", "slwin_0_2", "-f", "q2", "data/scores.csv")
job("--icsv", "--opprint", "step", "-a", "median", "-f", "q1", "data/scores.csv")

# Reshaping fields.
job("--icsv", "--opprint", "nest", "--ivar", ";", "-f", "id", "then", "cut", "-f", "region,id", O)
job("--icsv", "--opprint", "nest", "--explode", "--values", "--across-records", "-f", "tags", "--nested-fs", ";", "data/tags.csv")
job("--icsv", "--opprint", "nest", "--explode", "--values", "--across-fields", "-f", "tags", "--nested-fs", "semicolon", "data/tags.csv")
job("--icsv", "--ojson", "nest", "--explode", "--pairs", "--across-records", "-f", "attrs", "--nested-fs", ";", "--nested-ps", ":", "data/tags.csv")
job("--icsv", "--ojson", "nest", "--explode", "--pairs", "--across-fields", "-f", "attrs", "--nested-fs", ";", "--nested-ps", ":", "data/tags.csv")
job("--icsv", "--opprint", "nest", "--evar", ";", "-f", "tags", "then", "nest", "--ivar", "|", "-f", "tags", "data/tags.csv")
job("--icsv", "--opprint", "nest", "--explode", "--values", "--across-fields", "-f", "tags", "then", "nest", "--implode", "--values", "--across-fields", "-f", "tags", "--nested-fs", "+", "data/tags.csv")
job("--icsv", "--ocsv", "reorder", "-f", "status,id", "then", "head", "-n", "2", O)
job("--icsv", "--ocsv", "reorder", "-e", "-f", "id,date", "then", "head", "-n", "2", O)
job("--icsv", "--ocsv", "reorder", "-f", "qty", "-a", "region", "then", "head", "-n", "2", O)
job("--icsv", "--ocsv", "reorder", "-r", "^[pq]", "-b", "id", "then", "head", "-n", "2", O)
job("--icsv", "--ocsv", "reorder", "-r", "^[dp]", "then", "head", "-n", "2", O)
job("--icsv", "--ocsv", "rename", "id,order,qty,quantity", "then", "head", "-n", "2", O)
job("--icsv", "--ocsv", "rename", "qty,price", "then", "head", "-n", "2", O)
job("--icsv", "--ocsv", "rename", "-r", "^(.)r(.*)$,\\2_\\1", "then", "head", "-n", "2", O)
job("--icsv", "--ocsv", "rename", "-g", "-r", "e,E", "then", "head", "-n", "2", O)
job("--icsv", "--ocsv", "rename", "-r", '"^C(.*)"i,client\\1', "then", "head", "-n", "2", O)
job("--icsv", "--ocsv", "label", "a,b,c", "then", "head", "-n", "2", O)
job("--icsv", "--ocsv", "label", "x,y,qty", "then", "head", "-n", "2", O)
job("--icsv", "--ocsv", "label", "a,b,a", O)
job("--opprint", "regularize", E)
job("--ojson", "sort-within-records", "then", "head", "-n", "2", E)
job("--ojson", "sort-within-records", "-r", "then", "tail", "-n", "1", E)
job("--icsv", "--opprint", "template", "-f", "customer,id,missing", O)
job("--icsv", "--opprint", "template", "-f", "id,missing", "--fill-with", "X", "then", "head", "-n", "3", O)
job("--icsv", "--ojson", "template", "-f", "page,user,n", "--fill-with", "", "then", "head", "-n", "1", "data/visits.csv")
job("--icsv", "--opprint", "fill-down", "-f", "qty", "then", "head", "-n", "6", "then", "cut", "-f", "id,qty", "data/orders.csv")
job("--icsv", "--opprint", "fill-down", "-a", "-f", "qty", "then", "head", "-n", "6", "then", "cut", "-f", "id,qty", "data/orders.csv")
job("--icsv", "--opprint", "fill-down", "-f", "q3,q4", "data/scores.csv")
job("--icsv", "--opprint", "fill-down", "--all", "data/tags.csv")
job("--icsv", "--opprint", "fill-empty", O)
job("--icsv", "--ojson", "fill-empty", "-v", "0", "then", "head", "-n", "1", "then", "cut", "-f", "q3", "data/scores.csv")
job("--icsv", "--ojson", "fill-empty", "-S", "-v", "0", "then", "head", "-n", "1", "then", "cut", "-f", "q3", "data/scores.csv")
job("--icsv", "--opprint", "sec2gmt", "t", "data/times.csv")
job("--icsv", "--opprint", "sec2gmt", "-3", "t", "data/times.csv")
job("--icsv", "--opprint", "sec2gmt", "--millis", "-6", "ms", "data/times.csv")
job("--icsv", "--opprint", "sec2gmt", "-1", "t,ms", "data/times.csv")

# Joins.
job("--icsv", "--opprint", "join", "-j", "customer", "-f", "data/customers.csv", "then", "cut", "-f", "id,customer,tier,qty", O)
job("--icsv", "--opprint", "join", "--np", "--ul", "-j", "customer", "-f", "data/customers.csv", O)
job("--icsv", "--opprint", "join", "--np", "--ur", "-j", "customer", "-f", "data/customers.csv", O)
job("--icsv", "--opprint", "join", "--ul", "--ur", "-j", "customer", "--lp", "c_", "--rp", "o_", "-f", "data/customers.csv", "then", "head", "-n", "4", O)
job("--icsv", "--opprint", "join", "-l", "customer", "-r", "customer", "-j", "client", "-f", "data/customers.csv", "then", "cut", "-f", "client,id,tier", O)
job("--icsv", "--opprint", "join", "--lk", "tier", "-j", "customer", "-f", "data/customers.csv", "then", "head", "-n", "3", O)

# Generators and chains.
job("seqgen", "--start", "1", "--stop", "10", "--step", "3")
job("--opprint", "seqgen", "-f", "x", "--start", "5", "--stop", "1", "--step", "-1.5")
job("seqgen", "--start", "1", "--stop", "1", "--step", "0")
job("seqgen", "--start", "1", "--stop", "5", "--step", "0")
job("--ojson", "seqgen", "--start", "0x10", "--stop", "0x13", "then", "step", "-a", "rsum", "-f", "i")
job("-n", "--icsv", "--opprint", "cat", O)
job("--icsv", "--opprint", "sort", "-nr", "qty", "then", "head", "-n", "3", "then", "cut", "-o", "-f", "customer,qty", O)
job("--icsv", "--opprint", "stats1", "-a", "sum", "-f", "qty", "-g", "customer", "then", "sort", "-nr", "qty_sum", O)

# Errors.
job("--icsv", "--bogus", "cat", O)
job("--icsv", "frobnicate", O)
job("--icsv", "cat", "then")
job("--icsv", "head", "-n", "abc", O)
job("--icsv", "--opprint", "step", "-a", "delta", O)
job("--icsv", "--opprint", "seqgen", "--start", "x")
job("--icsv", "--opprint", "grep", "(", O)

put("jobs.txt", "\n".join(JOBS) + "\n")
