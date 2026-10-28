"""Writes data/: the CSV files the jobs read, and data/jobs.txt, one xsv
run per line with its arguments separated by tabs (a literal backslash-t
in an argument is the two characters xsv's --delimiter takes for a tab).

The order export is generated with a small LCG, so the file is the same on
every run; the other files are written out by hand to reach the corners of
xsv's reader, writer, selection syntax and type inference.

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


# ------------------------------------------------------------ orders.csv
seed = 20261028


def rnd(n):
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return (seed >> 8) % n


def q(field):
    if any(c in field for c in ',"\n\r'):
        return '"' + field.replace('"', '""') + '"'
    return field


REGIONS = ["north", "south", "east", "west"]
CUSTOMERS = ["Smith, Jane", "Bob Ng", 'Ana "Ace" Ruiz', "Ünal Çelik",
             "Lee", "Chen Wei", "Priya Nair", "Omar Haddad"]
PRODUCTS = [("widget", "2.5"), ("gadget", "19.99"), ("Widget, large", "7"),
            ("cable 2m", "3.75"), ("hub", "24")]
STATUS = ["shipped", "shipped", "shipped", "pending", "returned", "cancelled"]
WEIGHTS = ["1.250", "0.5", "12", "3e-1", "2.75", "0.125", "4"]

rows = ["order_id,date,region,customer,product,qty,unit_price,discount,"
        "status,rating,weight_kg"]
for i in range(60):
    region = REGIONS[rnd(4)]
    if i in (7, 33):
        region = " " + region
    if i == 41:
        region = ""
    product, price = PRODUCTS[rnd(5)]
    qty = "" if rnd(12) == 0 else str(1 + rnd(40))
    discount = ["", "", "", "", "0.1", "0.05", "0.15"][rnd(7)]
    rating = "" if rnd(9) == 0 else str(1 + rnd(5))
    if i == 47:
        rating = "n/a"
    row = [str(1001 + i), "2026-09-%02d" % (1 + rnd(30)), region,
           CUSTOMERS[rnd(8)], product, qty, price, discount,
           STATUS[rnd(6)], rating, WEIGHTS[rnd(7)]]
    rows.append(",".join(q(f) for f in row))
put("orders.csv", "\n".join(rows) + "\n")

# ------------------------------------------------------------ the rest
put("customers.csv",
    "customer,segment,country\n"
    "\"smith, jane\",retail,UK\n"
    " Bob Ng ,wholesale,SG\n"
    "\"Ana \"\"Ace\"\" Ruiz\",retail,MX\n"
    "Ünal Çelik,retail,TR\n"
    "Chen Wei,wholesale,CN\n"
    "Chen Wei,partner,CN\n"
    "Dana Scully,retail,US\n"
    ",unknown,\n")

put("customers2.csv",
    "customer,segment,country\n"
    "Priya Nair,partner,IN\n"
    "Omar Haddad,retail,JO\n")

put("regions.tsv",
    "region\tmanager\tquarterly_target\n"
    "north\tM. Okafor\t12000\n"
    "south\tR. Silva\t9500.5\n"
    "east\tK. Tanaka\t\n"
    "central\tA. Novak\t7000\n")

put("sensors.csv",
    "id,reading,counter,flag,label\n"
    "s1,-0.5,9007199254740993,true,12\n"
    "s2,.5,-42,false, 12\n"
    "s3,1.,+15,,alpha\n"
    "s4,+7,99999999999999999999,true,beta\n"
    "s5,1e3,0,false,gamma\n"
    "s6,2.5E-2,17,,12\n"
    "s7,-12.75,-3,true,\n"
    "s8,,8,false,delta\n"
    "s9,0.1,8,true,beta\n"
    "s10,0.2,,false,beta\n"
    "s11,1e21,5,,alpha\n"
    "s12,0.00001,5,true,epsilon\n")

put("quoted.csv",
    "id,text,note\r\n"
    "1,\"Hello, world\",\"said \"\"hi\"\"\"\r\n"
    "\r\n"
    "2,\"multi\nline\",plain\r\n"
    "3,\"ab\"cd,x\r\n"
    "4,,\r\n"
    "5,semi;colon,\"tab\there\"\r\n")

put("dupes.csv",
    "name,age,name\n"
    "ada,36,lovelace\n"
    "alan,41,turing\n"
    "grace,85,hopper\n")

put("ragged.csv",
    "a,b,c\n"
    "1,2\n"
    "3,4,5,6\n"
    "7,,,\n"
    "8\n")

put("empty.csv", "x,y,z\n")
put("blank.csv", "")

# ------------------------------------------------------------ jobs
JOBS = []


def job(*argv):
    JOBS.append("\t".join(argv))


O, C, R, S = "data/orders.csv", "data/customers.csv", "data/regions.tsv", "data/sensors.csv"
Q, D, G = "data/quoted.csv", "data/dupes.csv", "data/ragged.csv"

job("count", O)
job("count", "-n", O)
job("count", "data/empty.csv")
job("count", "data/blank.csv")
job("count", Q)
job("count", G)

job("headers", O)
job("headers", R)
job("headers", "-j", C)
job("headers", O, C)
job("headers", "--intersect", R, O)

job("select", "1,3-5", S)
job("select", "label-id", S)
job("select", "!counter-flag", S)
job("select", "3-", R)
job("select", "!-2", R)
job("select", "-", D)
job("select", "name[1],age,name", D)
job("select", "-n", "2,1", R)
job("select", "\"text\",id", Q)
job("select", "nope", O)
job("select", "9", R)
job("select", "name[2]", D)
job("select", "-n", "name", D)
job("select", "a-b-c", D)

job("slice", "-s", "2", "-e", "5", O)
job("slice", "-i", "0", S)
job("slice", "-s", "57", O)
job("slice", "-s", "10", "-l", "3", O)
job("slice", "-n", "-l", "2", R)
job("slice", "-s", "5", "-e", "2", O)
job("slice", "-e", "3", "-l", "2", O)

job("search", "-s", "region", "^(north|east)$", O)
job("search", "-i", "SMITH", O)
job("search", "-v", "-s", "status,rating", "^(shipped|[1-4])$", O)
job("search", "-s", "2", "^-?[0-9]+\\.[0-9]+$", S)
job("search", "-n", "a", D)

job("sort", "-s", "customer", C)
job("sort", "-N", "-s", "qty", O)
job("sort", "-R", "-N", "-s", "unit_price,order_id", O)
job("sort", "-N", "-s", "reading", S)
job("sort", "-n", R)
job("sort", "-R", D)

job("frequency", O)
job("frequency", "-s", "region,status", "--asc", O)
job("frequency", "-s", "rating", "-l", "0", "--no-nulls", O)
job("frequency", "-j", "4", "-s", "product,customer", "-l", "3", O)
job("frequency", "-n", "-s", "1", R)

job("stats", O)
job("stats", "--everything", O)
job("stats", "--everything", "--nulls", "-s", "qty,discount,rating", O)
job("stats", "--everything", S)
job("stats", "-j", "4", "--everything", O)
job("stats", "--median", "--mode", "-s", "reading,counter", "-j", "3", S)
job("stats", "--cardinality", "data/empty.csv")
job("stats", "-n", R)
job("stats", G)

job("join", "customer", O, "customer", C)
job("join", "--left", "customer", C, "customer", O)
job("join", "--right", "region", R, "region", O)
job("join", "--full", "customer", C, "customer", "data/customers2.csv")
job("join", "--no-case", "customer", O, "customer", C)
job("join", "1", C, "1", C)
job("join", "--nulls", "1", C, "1", C)
job("join", "--cross", "region", R, "name", D)
job("join", "1,2", C, "1", R)
job("join", "--left", "--full", "1", C, "1", R)

job("fixlengths", G)
job("fixlengths", "-l", "2", G)
job("fixlengths", "-l", "0", G)

job("flatten", R)
job("flatten", "-c", "6", D)
job("flatten", "-s", "", "-n", D)

job("table", R)
job("table", "-w", "6", "-p", "1", C)
job("table", "-c", "5", S)

job("fmt", "-t", ";", Q)
job("fmt", "--quote-always", R)
job("fmt", "--crlf", D)
job("fmt", "--ascii", D)
job("fmt", "-t", "\\t", Q)
job("fmt", "--escape", "\\", "--quote", "'", Q)

job("cat", "rows", C, "data/customers2.csv")
job("cat", "rows", "-n", R, C)
job("cat", "rows", C, S)
job("cat", "columns", R, D)
job("cat", "columns", "--pad", R, "data/customers2.csv")

put("jobs.txt", "\n".join(JOBS) + "\n")
