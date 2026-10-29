"""Writes data/: the files the jobs read, each one the way some real
system exports it, and data/jobs.txt, one job per line. A job is a
pipeline of steps separated by " | "; the first step reads a file.
oracle.py runs each job on pandas, mini_pandas_io.kara on its own port.

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


# A German bank's account statement export: three lines of account
# details above the header, `;` between fields, `,` for the decimal
# point and `.` between thousands, dates as dd.mm.yyyy, a purpose field
# that holds a `;` inside quotes, and a blank line at the end. The
# account number is a made-up one.
put("statement.csv", "\n".join([
    "Kontoauszug;Girokonto",
    "IBAN;DE00 0000 0000 0000 0000 00",
    "Zeitraum;01.09.2026 - 30.09.2026",
    "Buchungstag;Valuta;Empfänger;Verwendungszweck;Betrag;Saldo;Währung",
    "01.09.2026;01.09.2026;Stadtwerke Musterstadt;\"Abschlag Strom; Gas\";-142,50;2.857,50;EUR",
    "01.09.2026;01.09.2026;Arbeitgeber GmbH;Gehalt 09/2026;3.250,00;6.107,50;EUR",
    "02.09.2026;02.09.2026;Vermieterin K.;Miete September;-1.180,00;4.927,50;EUR",
    "05.09.2026;04.09.2026;Supermarkt 0815;Kartenzahlung;-63,17;4.864,33;EUR",
    "09.09.2026;09.09.2026;Versicherung AG;\"Beitrag \"\"Hausrat\"\"\";-12,90;4.851,43;EUR",
    "15.09.2026;15.09.2026;Bargeld;Geldautomat;-200;4.651,43;EUR",
    "21.09.2026;22.09.2026;Online-Shop;Rücksendung;+49,99;4.701,42;EUR",
    "30.09.2026;30.09.2026;Bank;Kontoführung;-4,95;4.696,47;EUR",
    "",
    "",
]))

# A mainframe extract: `|` between fields, no header row, comment lines
# from the job that wrote it, fields padded with spaces, account ids with
# leading zeros, -9999 and "n.a." for missing values, and a product name
# with a `#` in it, which a comment character cuts short.
put("legacy.dat", "\n".join([
    "# EXTRACT ACCTMAST  RUN 2026-10-29 02:00",
    "# FIELDS: ACCT|NAME|REGION|BALANCE|LIMIT|OPENED",
    "000123|ACME CORP           |WEST |   15000.00|  50000|19980312",
    "000124|  BLUE RIVER LLC    |EAST |    -250.75|  -9999|20010704",
    "000125|WIDGETS #2 SUPPLY   |WEST |       n.a.|  10000|20150101",
    "000126|CEDAR & PINE        |NORTH|     980.10|  25000|20200229",
    "# 4 RECORDS",
    "000127|DELTA FREIGHT       |-9999|    1234.5 |   7500|20221111",
    "",
]))

# A building's sensor log as tab-separated values: three devices
# reporting every 15 minutes, interleaved, with readings the network
# dropped (blank), the device's own "no reading" value (-9999) and an
# error code.
rows = ["device\tts\ttemp_c\thumidity\tstatus"]
temps = {
    "lobby": ["21.5", "21.7", "", "", "22.4", "22.1", "-9999", "21.9"],
    "roof": ["14.2", "", "13.8", "13.1", "", "", "", "12.4"],
    "server": ["24.0", "24.6", "25.9", "ERR", "27.3", "26.8", "25.5", "24.9"],
}
hums = {
    "lobby": ["40", "41", "41", "", "43", "42", "42", "40"],
    "roof": ["71", "", "74", "78", "79", "", "81", "83"],
    "server": ["30", "30", "29", "29", "", "28", "28", "29"],
}
for k in range(8):
    ts = "2026-10-29T%02d:%02d" % (8 + (k * 15) // 60, (k * 15) % 60)
    for d in ["lobby", "roof", "server"]:
        st = "ok" if temps[d][k] not in ("", "-9999", "ERR") else ("" if temps[d][k] == "" else "fault")
        rows.append("\t".join([d, ts, temps[d][k], hums[d][k], st]))
put("sensors.tsv", "\n".join(rows) + "\n")

# A shop's product feed: titles and descriptions with commas, quotes and
# a line break inside quotes; one row where a title's comma was not
# quoted (one field too many) and one row cut short.
put("feed.csv", "\n".join([
    "sku,title,description,price,stock,tags",
    "M-24,\"Monitor 24\"\", IPS\",\"Matte, 75 Hz\",149.00,12,office",
    "K-01,Keyboard,\"Mechanical\nbrown switches\",89.5,0,\"office,gaming\"",
    "C-10,Cable, USB-C,2 m braided,9.99,140,",
    "H-07,\"Headset \"\"Pro\"\"\",Closed back,59,8,gaming",
    "D-02,Dock,,129.00",
    "W-33,Webcam,1080p,45.25,31,office",
]) + "\n")

# The same feed from a system that escapes quotes with a backslash
# instead of doubling them.
put("feed_esc.csv", "\n".join([
    "sku,title,price",
    "M-24,\"Monitor 24\\\", IPS\",149.00",
    "H-07,\"Headset \\\"Pro\\\"\",59",
    "B-12,Bag\\, padded,24.50",
]) + "\n")

# A survey tool's export: yes/no answers in three spellings, booleans in
# any case, a question exported twice under one name, an unnamed column,
# blank lines and a line of spaces between respondents.
put("survey.csv", "\n".join([
    "respondent,consent,q1,q1,,score,newsletter,active",
    "r01,Yes,4,5,a,8.5,Y,TRUE",
    "r02,No,3,3,,7,N,false",
    "",
    "r03,Yes,5,4,b,,Y,True",
    "   ",
    "r04,yes,2,2,c,9,N,tRuE",
    "r05,No,,1,,6.5,Y,FALSE",
]) + "\n")

# A report a tool printed with columns lined up by spaces.
put("report.txt", "\n".join([
    "  host        cpu   mem_mb   uptime_d  state",
    "  web-01      12.5    2048      41      up",
    "  web-02       7.0    2048      41      up",
    "    db-01     55.25   16384    210      up",
    "  cache-01     0.5     512       3      degraded",
    "",
    "   ",
]) + "\n")

# Excel's "CSV UTF-8" on Windows: a byte-order mark and CRLF line ends.
put("windows.csv", "﻿id,name,amount,paid\r\n1,Zoë,3.50,TRUE\r\n2,Łukasz,12,FALSE\r\n3,Ana,,TRUE\r\n")

# Excel for Mac's older "CSV (Macintosh)": lines end with a bare CR.
put("mac.csv", "id,city,visits\r1,Lyon,4\r2,Kraków,7\r3,Porto,\r")

# Ids and counts at the edges of 64-bit integers, with numbers quoted,
# padded with spaces, signed, written with thousands separators and in
# exponent form.
put("ids.csv", "\n".join([
    "event_id,user_id,signed,count,amount,code",
    "18446744073709551615,9223372036854775807,-9223372036854775808,\"1,234\", 42 ,007",
    "1,1,+7,\"12,000,000\",1e3,010",
    "9223372036854775808,2,0,5,  -0.5,099",
]) + "\n")
put("ids_neg.csv", "event_id,user\n18446744073709551615,a\n-2,b\n")
put("ids_big.csv", "event_id,user\n18446744073709551616,a\n2,b\n")

# A file that ends inside an open quote, as a cut-off download does.
put("truncated.csv", "id,note\n1,fine\n2,\"cut off here\n")

J = []
def job(*s):
    J.append(" | ".join(s))

# --- reading: the bank statement
job("read statement.csv")
job("read statement.csv sep=;")
job("read statement.csv sep=; skiprows=3")
job("read statement.csv sep=; skiprows=3 | dtypes")
job("read statement.csv sep=; skiprows=3 decimal=,")
job("read statement.csv sep=; skiprows=3 decimal=, | dtypes")
job("read statement.csv sep=; skiprows=3 decimal=, thousands=.")
job("read statement.csv sep=; skiprows=3 decimal=, thousands=. | dtypes")
job("read statement.csv sep=; skiprows=3 decimal=, thousands=. usecols=Buchungstag,Betrag,Saldo")
job("read statement.csv sep=; skiprows=3 decimal=, thousands=. | cumsum Betrag as=laufend | select Buchungstag,Betrag,Saldo,laufend")
job("read statement.csv sep=; skiprows=3 decimal=, thousands=. | where Betrag < 0 | agg Währung n=Betrag:count,ausgaben=Betrag:sum")
job("read statement.csv sep=; skiprows=3 decimal=, thousands=. nrows=3")
job("read statement.csv sep=; skiplines=0,1,2,5")
job("read statement.csv sep=; skiprows=3 decimal=, thousands=. | write sep=, decimal=.")
job("read statement.csv sep=; skiprows=3 decimal=, thousands=. | write sep=; decimal=, float=%.2f")
job("read statement.csv sep=; skiprows=3 decimal=, thousands=. | write quoting=1")
job("read statement.csv sep=; skiprows=3 decimal=, thousands=. | write quoting=2 float=%.2f")

# --- reading: the mainframe extract
job("read legacy.dat sep=| header=none")
job("read legacy.dat sep=| header=none comment=#")
job("read legacy.dat sep=| header=none comment=# names=acct,name,region,balance,limit,opened")
job("read legacy.dat sep=| header=none comment=# names=acct,name,region,balance,limit,opened | dtypes")
job("read legacy.dat sep=| header=none comment=# names=acct,name,region,balance,limit,opened dtype=acct:str na=-9999,n.a.")
job("read legacy.dat sep=| header=none comment=# names=acct,name,region,balance,limit,opened dtype=acct:str na=-9999,n.a. | dtypes")
job("read legacy.dat sep=| header=none comment=# names=acct,name,region,balance,limit,opened dtype=acct:str,opened:str na=-9999,n.a. skipinitialspace=1 | strip name | strip region")
job("read legacy.dat sep=| header=none comment=# names=acct,name,region,balance,limit,opened dtype=acct:str na=-9999,n.a. | fillna balance 0 | fillna limit 0 | write float=%.2f")
job("read legacy.dat sep=| header=none comment=# names=acct,name,region,balance,limit,opened dtype=acct:str na=-9999,n.a. keep_default_na=0")
job("read legacy.dat sep=| header=none comment=# names=acct,name,region,balance dtype=acct:str")
job("read legacy.dat sep=| header=none comment=# names=acct,name,region,balance,limit,opened dtype=balance:float")
job("read legacy.dat sep=| header=none comment=# names=acct,name,region,balance,limit,opened dtype=limit:int64")
job("read legacy.dat sep=| header=none comment=# names=acct,name,region,balance,limit,opened dtype=acct:str na=-9999,n.a. | dropna")
job("read legacy.dat sep=| header=none comment=# names=acct,name,region,balance,limit,opened dtype=acct:str na=-9999,n.a. | dropna subset=balance")
job("read legacy.dat sep=| header=none comment=# names=acct,name,region,balance,limit,opened dtype=acct:str na=-9999,n.a. | dropna thresh=6")

# --- the sensor log
job("read sensors.tsv sep=\\t")
job("read sensors.tsv sep=\\t | dtypes")
job("read sensors.tsv sep=\\t na=-9999,ERR")
job("read sensors.tsv sep=\\t na=-9999,ERR | dtypes")
job("read sensors.tsv sep=\\t na=-9999,ERR | ffill temp_c")
job("read sensors.tsv sep=\\t na=-9999,ERR | ffill temp_c by=device")
job("read sensors.tsv sep=\\t na=-9999,ERR | ffill temp_c by=device limit=1")
job("read sensors.tsv sep=\\t na=-9999,ERR | bfill temp_c by=device")
job("read sensors.tsv sep=\\t na=-9999,ERR | bfill humidity limit=1")
job("read sensors.tsv sep=\\t na=-9999,ERR | where device == 'roof' | ffill temp_c | diff temp_c as=change")
job("read sensors.tsv sep=\\t na=-9999,ERR | where device == 'server' | diff temp_c as=d1 | diff temp_c periods=2 as=d2")
job("read sensors.tsv sep=\\t na=-9999,ERR | where device == 'server' | pct_change temp_c as=pct")
job("read sensors.tsv sep=\\t na=-9999,ERR | where device == 'lobby' | shift temp_c 1 as=prev | shift temp_c -1 as=next")
job("read sensors.tsv sep=\\t na=-9999,ERR | where device == 'lobby' | shift humidity 2 as=lag2")
job("read sensors.tsv sep=\\t na=-9999,ERR | where device == 'roof' | cumsum humidity as=cs | cummax humidity as=cmax | cummin humidity as=cmin")
job("read sensors.tsv sep=\\t na=-9999,ERR | where device == 'roof' | cumprod humidity as=cp")
job("read sensors.tsv sep=\\t na=-9999,ERR | clip temp_c lower=15 upper=25")
job("read sensors.tsv sep=\\t na=-9999,ERR | clip humidity upper=75 | where device == 'roof'")
job("read sensors.tsv sep=\\t na=-9999,ERR | round temp_c 0 | where device == 'lobby'")
job("read sensors.tsv sep=\\t na=-9999,ERR | ffill temp_c by=device | agg device n=temp_c:count,mean=temp_c:mean,max=temp_c:max")
job("read sensors.tsv sep=\\t na=-9999,ERR | dropna how=all subset=temp_c,humidity")
job("read sensors.tsv sep=\\t na=-9999,ERR | dropna subset=temp_c,humidity")
job("read sensors.tsv sep=\\t na=-9999,ERR | fillna status 'missing' | agg status n=device:count")
job("read sensors.tsv sep=\\t na=-9999,ERR | astype humidity int64")
job("read sensors.tsv sep=\\t na=-9999,ERR | where device == 'server' | astype humidity str")
job("read sensors.tsv sep=\\t na=-9999,ERR | where device == 'server' | astype temp_c str | dtypes")
job("read sensors.tsv sep=\\t | replace temp_c '-9999' 'none' | replace temp_c 'ERR' 'none' | where device == 'lobby'")
job("read sensors.tsv sep=\\t na=-9999,ERR | replace humidity 41 40 | where device == 'lobby'")
job("read sensors.tsv sep=\\t na=-9999,ERR | where device == 'roof' | write na=NULL")
job("read sensors.tsv sep=\\t na=-9999,ERR | where device == 'roof' | write sep=\\t float=%.1f")
job("read sensors.tsv sep=\\t na=-9999,ERR | where device == 'lobby' | write float=%.3e")
job("read sensors.tsv sep=\\t na=-9999,ERR | where device == 'lobby' | write float=%.3g")

# --- the product feed
job("read feed.csv")
job("read feed.csv on_bad_lines=skip")
job("read feed.csv on_bad_lines=warn")
job("read feed.csv on_bad_lines=skip | dtypes")
job("read feed.csv usecols=sku,price")
job("read feed.csv on_bad_lines=skip | write quoting=1")
job("read feed.csv on_bad_lines=skip | write quoting=2")
job("read feed.csv on_bad_lines=skip | write quoting=3")
job("read feed.csv on_bad_lines=skip | write quoting=3 escapechar=\\")
job("read feed.csv on_bad_lines=skip | write quoting=4")
job("read feed.csv on_bad_lines=skip | write quoting=5")
job("read feed.csv on_bad_lines=skip | write escapechar=\\ doublequote=0")
job("read feed.csv on_bad_lines=skip | write quotechar='")
job("read feed.csv on_bad_lines=skip | write sep=|")
job("read feed.csv on_bad_lines=skip | write sep=; header=0 columns=price,sku")
job("read feed.csv on_bad_lines=skip quoting=3")
job("read feed_esc.csv")
job("read feed_esc.csv escapechar=\\")
job("read feed_esc.csv escapechar=\\ doublequote=0")
job("read feed_esc.csv escapechar=\\ doublequote=0 | write escapechar=\\ doublequote=0")
job("read feed_esc.csv quotechar='")

# --- the survey
job("read survey.csv")
job("read survey.csv | dtypes")
job("read survey.csv true=Yes,yes,Y false=No,N")
job("read survey.csv true=Yes,yes,Y false=No,N | dtypes")
job("read survey.csv true=Yes,Y false=No,N | dtypes")
job("read survey.csv skip_blank_lines=0")
job("read survey.csv skip_blank_lines=0 | dtypes")
job("read survey.csv | rename q1:q1_first,q1.1:q1_second,Unnamed:\\s4:group")
job("read survey.csv | rename q1:q1_first,q1.1:q1_second | dedup subset=q1_first,q1_second")
job("read survey.csv | dedup subset=consent")
job("read survey.csv | dedup subset=consent keep=last")
job("read survey.csv | dedup subset=consent keep=False")
job("read survey.csv | fillna q1 0 | astype q1 int64 | dtypes")
job("read survey.csv true=Yes,yes,Y false=No,N | write quoting=2")

# --- lined-up columns, Windows and old Mac line ends
job("read report.txt sep=ws")
job("read report.txt sep=ws | dtypes")
job("read report.txt sep=ws | write float=%.2f sep=\\t")
job("read report.txt")
job("read windows.csv")
job("read windows.csv | dtypes")
job("read mac.csv")
job("read mac.csv | dtypes")

# --- integers at the edges
job("read ids.csv")
job("read ids.csv | dtypes")
job("read ids.csv thousands=,")
job("read ids.csv thousands=, | dtypes")
job("read ids.csv thousands=, dtype=code:str | dtypes")
job("read ids_neg.csv | dtypes")
job("read ids_big.csv | dtypes")
job("read ids_big.csv")

# --- errors a pipeline has to report
job("read truncated.csv")
job("read missing.csv")
job("read feed.csv usecols=sku,weight")
job("read sensors.tsv sep=\\t na=-9999,ERR | astype temp_c int64")
job("read sensors.tsv sep=\\t | astype temp_c float64")

with open(os.path.join(DATA, "jobs.txt"), "w", encoding="utf-8", newline="") as f:
    f.write("\n".join(J) + "\n")
print(len(J), "jobs")
