"""Writes data/: the CSV files the jobs read, and data/jobs.txt, one job
per line. A job is a pipeline of steps separated by " | "; the first step
reads a file. oracle.py runs each job on pandas, mini_pandas_clean.kara on
its own port.

Run: python3 -s -P -B mk.py"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
shutil.rmtree(DATA, ignore_errors=True)
os.makedirs(DATA)


def put(name, rows):
    text = "\n".join(",".join(r) for r in rows) + "\n"
    with open(os.path.join(DATA, name), "w", encoding="utf-8", newline="") as f:
        f.write(text)


# A CRM's contact export, as a sales team keeps it: names typed every
# way, emails with stray spaces, capitals and a mailto: prefix, phone
# numbers in four formats, zip codes that a spreadsheet stripped of their
# leading zeros, a signup fee typed by hand ("N/A", "1,200", "free", an
# exponent, a blank), and the same person entered twice.
put("contacts.csv", [
    ["id", "name", "email", "phone", "zip", "country", "plan", "fee", "visits", "referrer"],
    ["101", "  alice SMITH ", "Alice@Example.com", "(415) 555-0101", "94107", "US", "pro", "12.50", "3", "ads"],
    ["102", "BOB o'neil", " bob@example.org", "415.555.0102", "2134", "US", "free", "0", "11", ""],
    ["103", "carol-ann lee", "mailto:carol@example.net", "+1 415 555 0103", "501", "US", "team", '"1,200"', "7", "partner"],
    ["104", "3rd street deli", "orders@3rdstreet.example", "4155550104", "10001-4356", "US", "pro", " 35 ", "0", "ads"],
    ["105", "dr. zoë ADLER", "zoe@example.de", "+49 30 5550105", "10115", "DE", "team", "N/A", "21", "conference"],
    ["106", "Seán O'Brien", "sean@example.ie", "+353 1 555 0106", "D02", "IE", "pro", "free", "5", "ads"],
    ["107", "ALICE SMITH", "alice@example.com ", "(415) 555-0101", "94107", "US", "pro", "12.5", "4", "ads"],
    ["108", "mei-ling wu", "mei@example.sg", "+65 5550 0108", "18956", "SG", "free", "", "2", "search"],
    ["109", "o'hara & sons", "Info@OHara.example", "415-555-0109", "601", "US", "team", "1e3", "9", "partner"],
    ["110", "  ", "nobody@example.com", "", "", "US", "free", "-0", "1", ""],
    ["111", "JOSÉ  núñez", "jose@example.mx", "+52 55 5550 0111", "06700", "MX", "pro", "49.99", "14", "search"],
    ["112", "bob o'neil", "BOB@example.org", "415.555.0102", "2134", "US", "free", "0.0", "12", "ads"],
])

# The same data, where every fee is a clean number or a gap, and every
# count a whole number.
put("fees.csv", [
    ["id", "fee", "visits", "credits"],
    ["101", "12.50", "3", "10"],
    ["102", "0", "11", "-4"],
    ["103", "1200", "7", "250"],
    ["104", " 35 ", "0", "0"],
    ["105", "", "21", "75"],
    ["106", "+5", "5", "15"],
    ["107", "12.5", "4", "10"],
])

# A shop's catalog and a vendor's price feed for it. The feed lists some
# of the shop's products, one new one, a price it does not know (blank)
# and a name in its own spelling.
put("catalog.csv", [
    ["sku", "name", "price", "stock", "color"],
    ["k3", "Desk lamp", "39.0", "12", "black"],
    ["k1", "Mug", "", "40", ""],
    ["k5", "Notebook", "4.5", "200", "red"],
    ["k2", "Kettle", "24.0", "7", "white"],
])
put("vendor.csv", [
    ["sku", "name", "price", "weight"],
    ["k1", "Ceramic mug", "8.0", "0.35"],
    ["k4", "Teapot", "31.5", "0.9"],
    ["k2", "Electric kettle", "", "1.2"],
    ["k5", "Notebook A5", "4.25", ""],
])

# A morning of trades and quotes on two tickers, times in milliseconds
# after the open. Quotes arrive at their own times, some at the same
# millisecond as a trade.
put("trades.csv", [
    ["ms", "ticker", "qty", "price"],
    ["100", "ACME", "200", "51.10"],
    ["130", "GLOB", "50", "720.0"],
    ["150", "ACME", "100", "51.12"],
    ["150", "GLOB", "25", "720.5"],
    ["205", "ACME", "300", "51.08"],
    ["260", "GLOB", "10", "721.25"],
    ["400", "ACME", "75", "51.30"],
])
put("quotes.csv", [
    ["ms", "ticker", "bid", "ask", "venue"],
    ["90", "ACME", "51.05", "51.11", "X"],
    ["120", "GLOB", "719.5", "720.5", "Y"],
    ["150", "ACME", "51.09", "51.13", "X"],
    ["155", "ACME", "51.10", "51.14", "Z"],
    ["200", "GLOB", "720.0", "721.0", "Y"],
    ["210", "ACME", "51.04", "51.09", "Y"],
    ["390", "GLOB", "721.0", "721.5", "X"],
])
# The same trades out of time order, and quotes with float times.
put("trades_late.csv", [
    ["ms", "ticker", "qty", "price"],
    ["150", "ACME", "100", "51.12"],
    ["100", "ACME", "200", "51.10"],
])
put("quotes_f.csv", [
    ["ms", "ticker", "bid", "ask", "venue"],
    ["90.0", "ACME", "51.05", "51.11", "X"],
    ["150.5", "ACME", "51.09", "51.13", "X"],
])

# Daily closes for three tickers, with days the feed missed.
CLOSES = {
    "ACME": ["51.2", "51.9", "", "52.4", "50.8", "", "", "53.1", "53.0", "52.2"],
    "GLOB": ["720", "722.5", "719", "", "725.25", "731", "728", "", "735.5", "741"],
    "FLAT": ["10", "10", "10", "10", "", "10", "10", "10", "10", "10"],
}
rows = [["day", "ticker", "close", "volume"]]
for d in range(10):
    for k, (t, cs) in enumerate(CLOSES.items()):
        rows.append([str(d + 1), t, cs[d], str(1000 + 37 * d + 15 * (k + 1) * (d % 3))])
put("closes.csv", rows)

# Measurements at the ends of the float range, as a physics export writes
# them, with the same numbers as text (`raw`), some with more digits than
# a double holds.
put("sci.csv", [
    ["name", "x", "raw"],
    ["avogadro", "6.02214076e23", "6.02214076e23"],
    ["planck", "6.62607015e-34", "6.62607015E-34"],
    ["tiny", "1e-20", "0.00000000000000000001"],
    ["edge", "1e-15", "1e-15"],
    ["below", "9.9e-16", "9.9e-16"],
    ["big", "1.5e17", "150000000000000000"],
    ["e16", "1e16", "1e16"],
    ["under", "9999999999999998", "9999999999999998"],
    ["long", "0.12345678901234568", "0.1234567890123456789"],
    ["imax", "9.223372036854776e18", "9223372036854775807"],
    ["odd", "315667262066627.0", "31566.726206662698e10"],
    ["inf", "inf", "-Infinity"],
    ["half", "2.5", "2.5"],
    ["neg", "-0.125", " -0.125 "],
])

JOBS = []


def job(s):
    JOBS.append(s)


C = "read contacts.csv dtype=zip:str"

# The raw export, and what read_csv made of it.
job(C + " | dtypes")
job(C + " | select id,name,fee,zip")

# Text columns: case, whitespace, padding, slicing, replacing.
job(C + " | str name strip as=n1 | str n1 title as=n2 | select id,name,n2")
job(C + " | str name capitalize as=cap | str name swapcase as=swap | select id,cap,swap")
job(C + " | str name lower | str name strip | str name title | select id,name")
job(C + " | str email strip | str email lower | str email removeprefix mailto: | select id,email")
job(C + " | str email find @ as=at | str email count e as=es | select id,email,at,es")
job(C + " | str zip zfill 5 | select id,zip")
job(C + " | str zip slice 0 5 | str zip zfill 5 | select id,zip,country")
job(C + " | str phone replace ( \\e | str phone replace ) \\e | str phone replace - \\e | str phone replace . \\e | str phone replace \\s \\e | select id,phone")
job(C + " | str phone slice -4 as=last4 | select id,phone,last4")
job(C + " | str phone slice 1 4 as=s | select id,s")
job(C + " | str plan pad 6 as=a | str plan pad 6 side=right fill=. as=b | str plan pad 7 side=both fill=* as=c | select plan,a,b,c")
job(C + " | str plan upper | str plan len as=n | select id,plan,n")
job(C + " | str country removesuffix E | select id,country")
job(C + " | cat name country sep=/ as=nc | select id,nc")
job(C + " | cat plan referrer sep=- as=pr | select id,pr")
job(C + " | cat plan referrer sep=- na=none as=pr | select id,pr")
job(C + " | str id upper")

# Text to numbers.
job(C + " | numeric fee coerce | select id,fee")
job(C + " | numeric fee coerce | dtypes")
job(C + " | numeric fee")
job(C + " | numeric visits | dtypes")
job(C + " | numeric zip coerce | select id,zip")
job(C + " | numeric phone coerce | select id,phone")
job(C + " | str fee replace , \\e | numeric fee coerce | select id,fee")
job(C + " | str fee replace , \\e | numeric fee coerce | agg plan fee:sum,fee:mean,fee:count")
job("read fees.csv dtype=fee:str | numeric fee | dtypes")
job("read fees.csv dtype=fee:str | numeric fee | select id,fee")
job("read fees.csv dtype=credits:str | numeric credits | dtypes")
job("read fees.csv dtype=fee:str,credits:str | numeric fee coerce as=f | numeric credits as=c | select id,f,c")

# Duplicates as flags.
job(C + " | str email strip | str email lower | duplicated subset=email as=dup | select id,email,dup")
job(C + " | str email strip | str email lower | duplicated subset=email keep=last as=dup | select id,email,dup")
job(C + " | str email strip | str email lower | duplicated subset=email keep=false as=dup | select id,email,dup")
job(C + " | duplicated subset=phone,zip as=dup | select id,phone,zip,dup")
job(C + " | duplicated as=dup | select id,dup")
job(C + " | str email strip | str email lower | duplicated subset=email as=dup | where dup == False | select id,email")
job(C + " | duplicated subset=phone keep=false as=dup | where dup == True | select id,phone")

# Replacing values by a condition.
job(C + " | mask visits > 10 other=10 | select id,visits")
job(C + " | mask visits > 10 | select id,visits")
job(C + " | keep visits >= 5 other=0 | select id,visits")
job(C + " | keep visits >= 5 other=0.5 | select id,visits")
job(C + " | mask plan == 'free' other='trial' | select id,plan")
job(C + " | numeric fee coerce | keep fee < 100 | select id,fee")
job(C + " | numeric fee coerce | mask fee > 100 other=100 | select id,fee")

# Two sources for one table.
job("read catalog.csv | combine vendor.csv on=sku")
job("read catalog.csv | combine vendor.csv on=sku | dtypes")
job("read vendor.csv | combine catalog.csv on=sku")
job("read catalog.csv | update vendor.csv on=sku")
job("read catalog.csv | update vendor.csv on=sku | dtypes")
job("read vendor.csv | update catalog.csv on=sku")

# The quote in force at each trade.
T = "read trades.csv"
job(T + " | asof quotes.csv on=ms")
job(T + " | asof quotes.csv on=ms by=ticker")
job(T + " | asof quotes.csv on=ms by=ticker | dtypes")
job(T + " | asof quotes.csv on=ms by=ticker direction=forward")
job(T + " | asof quotes.csv on=ms by=ticker direction=nearest")
job(T + " | asof quotes.csv on=ms by=ticker tolerance=10")
job(T + " | asof quotes.csv on=ms by=ticker exact=0")
job(T + " | asof quotes.csv on=ms by=ticker direction=forward exact=0 tolerance=20")
job(T + " | asof quotes.csv on=ms by=ticker | agg ticker qty:sum,bid:mean,ask:max")
job("read quotes.csv | asof trades.csv on=ms by=ticker")
job("read trades_late.csv | asof quotes.csv on=ms")
job("read quotes.csv | asof trades_late.csv on=ms")
job(T + " | asof quotes_f.csv on=ms")
job(T + " | asof quotes.csv on=ms tolerance=-5")

# Exponentially weighted windows.
D = "read closes.csv"
job(D + " | where ticker == 'ACME' | ewm close mean span=3 as=ema | select day,close,ema")
job(D + " | where ticker == 'ACME' | ewm close mean span=3 adjust=0 as=ema | select day,close,ema")
job(D + " | where ticker == 'ACME' | ewm close mean span=3 ignore_na=1 as=ema | select day,close,ema")
job(D + " | where ticker == 'ACME' | ewm close mean span=3 adjust=0 ignore_na=1 as=ema | select day,close,ema")
job(D + " | where ticker == 'ACME' | ewm close mean com=1 adjust=0 as=ema | select day,close,ema")
job(D + " | where ticker == 'ACME' | ewm close mean alpha=0.3 minp=3 as=ema | select day,close,ema")
job(D + " | where ticker == 'GLOB' | ewm close mean halflife=2 as=ema | select day,close,ema")
job(D + " | where ticker == 'GLOB' | ewm close std span=4 as=sd | ewm close var span=4 as=v | select day,close,sd,v")
job(D + " | where ticker == 'GLOB' | ewm close std span=4 bias=1 as=sd | select day,close,sd")
job(D + " | where ticker == 'ACME' | ewm close var com=2 adjust=0 as=v | select day,close,v")
job(D + " | where ticker == 'FLAT' | ewm close mean span=5 as=ema | ewm close std span=5 as=sd | select day,close,ema,sd")
job(D + " | ewm close mean span=3 by=ticker as=ema | select day,ticker,close,ema")
job(D + " | ewm volume mean alpha=0.5 by=ticker as=ev | where day > 7 | select day,ticker,ev")
job(D + " | ewm close mean span=0.5 as=ema")
job(D + " | ewm close mean alpha=1.5 as=ema")
job(D + " | ewm ticker mean span=3 as=ema")

# Writing JSON.
job(C + " | select id,name,fee,visits | head 4 | json records")
job(C + " | select id,name,fee,visits | head 4 | json records ascii=0")
job(C + " | select id,name,email | tail 3 | json split")
job(C + " | select id,name,visits | head 3 | json index")
job(C + " | select id,country,visits | head 3 | json columns")
job(C + " | select id,phone,referrer | head 3 | json values")
job(C + " | select id,plan,visits | head 3 | json table")
job(C + " | select id,name,zip | head 3 | json records lines=1")
job(T + " | asof quotes.csv on=ms by=ticker | json records")
job(T + " | asof quotes.csv on=ms by=ticker | json records precision=2")
job(T + " | asof quotes.csv on=ms by=ticker | json values precision=0")
job(D + " | where ticker == 'ACME' | ewm close mean span=3 as=ema | select day,ema | json split")
job(D + " | where ticker == 'GLOB' | ewm close std span=4 as=sd | select day,sd | json records precision=15")
job("read fees.csv dtype=fee:str | numeric fee | select id,fee,credits | json table")
job(C + " | numeric fee coerce | select id,fee | json records")
job(C + " | str fee replace , \\e | numeric fee coerce | agg plan fee:mean,visits:sum | json table")
job("read catalog.csv | combine vendor.csv on=sku | json records")
job("read catalog.csv | update vendor.csv on=sku | json columns")
job(C + " | cat name country sep=/ as=nc | select id,nc | head 3 | json records")
job("read sci.csv")
job("read sci.csv | json values")
job("read sci.csv | json values precision=3")
job("read sci.csv | json values precision=0")
job("read sci.csv | json records precision=15")
job("read sci.csv | numeric raw | select name,x,raw")
job("read sci.csv | numeric raw | json values precision=15")
job("read sci.csv | where name != 'inf' | numeric raw | agg name x:sum,raw:sum | json split")

put("jobs.txt", [[j] for j in JOBS])
print(len(JOBS), "jobs")
