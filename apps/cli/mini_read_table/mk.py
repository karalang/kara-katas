"""Writes data/: the delimited text files the jobs read, each shaped like
a file people meet that read_csv's C engine cannot read and its python
engine can (ratings with a two-character separator, `ls -l` and
`vmstat` output split on runs of spaces, a psql result and a Markdown
table split on pipes, a MySQL tab export with backslash escapes, a
European export whose separator has to be sniffed, a survey with spaces
after the commas, ragged rows, a claims file with inch marks), the
broken inputs people meet, and data/jobs.txt, one job per line.
oracle.py runs each job on pandas' read_csv with engine="python",
mini_read_table.kara on its own port.

Every value is made up; the names, titles and account numbers are not
real.

Run: python3 -s -P -B mk.py"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
shutil.rmtree(DATA, ignore_errors=True)
os.makedirs(DATA)


def put(name, data, encoding="utf-8"):
    if isinstance(data, str):
        data = data.encode(encoding)
    with open(os.path.join(DATA, name), "wb") as f:
        f.write(data)


# ------------------------------------------------------------ ratings.dat
# The MovieLens .dat layout: UserID::MovieID::Rating::Timestamp, no
# header, which is why people meet sep="::" and engine="python".
RATINGS = [
    (1, 1193, 5, 978300760), (1, 661, 3, 978302109), (1, 914, 3, 978301968),
    (1, 3408, 4, 978300275), (1, 2355, 5, 978824291), (2, 1357, 5, 978298709),
    (2, 3068, 4, 978299000), (2, 1537, 4, 978299620), (2, 647, 3, 978299351),
    (3, 3421, 4, 978298147), (3, 1641, 2, 978298430), (3, 648, 3, 978297867),
    (4, 3468, 5, 978294008), (4, 1210, 3, 978293924), (5, 2717, 1, 978242084),
    (5, 1193, 4, 978244568), (5, 661, 2, 978246576), (6, 914, 5, 978236567),
]
put("ratings.dat", "".join(f"{u}::{m}::{r}::{t}\n" for u, m, r, t in RATINGS))

# movies.dat: MovieID::Title::Genres in ISO-8859-1, genres joined by |.
MOVIES = [
    (661, "Giant Peach Express (1996)", "Animation|Children's|Musical"),
    (914, "Mon Café à Montréal (1964)", "Musical|Romance"),
    (1193, "Over the Nest (1975)", "Drama"),
    (1210, "Return of the Starfarer: Part VI (1983)", "Action|Adventure|Sci-Fi"),
    (1357, "Brillant (1996)", "Drama|Romance"),
    (1537, "Shall We Dance? (1996)", "Comedy"),
    (2355, "A Bug's Day (1998)", "Animation|Children's|Comedy"),
    (3408, "Erin's Case (2000)", "Drama"),
    (3421, "Animal Haus (1978)", "Comedy"),
    (3468, "Der Hustler (1961)", "Drama"),
]
put("movies.dat", "".join(f"{m}::{t}::{g}\n" for m, t, g in MOVIES), "latin-1")

# ------------------------------------------------------------ ls.txt
# `ls -l` output: a "total" line, then nine whitespace-separated
# columns, except that a file name with spaces in it makes more.
LS = """total 48
-rw-r--r--  1 dana staff  4210 Oct 27 09:14 budget.xlsx
-rw-r--r--  1 dana staff 18733 Oct 28 17:02 report.pdf
drwxr-xr-x  5 dana staff   160 Oct 29 08:30 photos
-rwxr-xr-x  1 dana staff   912 Sep  3  2025 backup.sh
-rw-r--r--  1 dana staff  1534 Oct 29 10:41 notes for monday.txt
lrwxr-xr-x  1 dana staff    11 Oct 12 12:00 latest -> report.pdf
-rw-------  1 dana staff   220 Oct 29 11:05 .env
"""
put("ls.txt", LS)

# vmstat: a group-title line, then the column names, then the samples.
VMSTAT = """procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 2  0      0 812344 102400 2938112    0    0     5    21  310  622  7  2 90  1  0
 1  0      0 811920 102400 2938220    0    0     0    48  402  811 12  3 84  1  0
 4  1    256 790112 102404 2939004    0   12   188   960 1210 2904 41  9 38 12  0
 0  0    256 805776 102404 2939100    0    0     0     8  288  590  3  1 96  0  0
"""
put("vmstat.txt", VMSTAT)

# ------------------------------------------------------------ psql.txt
PSQL = """ id |    name     |   city    | balance  | active
----+-------------+-----------+----------+--------
  1 | Ana Ruiz    | Valencia  |  1200.50 | t
  2 | Bo Lindgren | Malmö     |     0.00 | f
  3 | Chidi Okafor| Lagos     | -340.25  | t
  4 | Dee Park    |           |   88.10  |
(4 rows)

"""
put("psql.txt", PSQL)

# A Markdown table pasted from a README.
MD = """| Service | Port | Owner     | SLO    |
|---------|------|-----------|--------|
| api     | 8080 | platform  | 99.9%  |
| billing | 9000 | payments  | 99.95% |
| search  | 9200 | discovery |        |
"""
put("services.md", MD)

# ------------------------------------------------------------ mysql.tsv
# SELECT ... INTO OUTFILE: tabs between fields, \N for NULL, and a
# backslash before a tab, newline or backslash inside a field.
MYSQL = (
    "1\tAna Ruiz\tana@example.com\t\\N\t2026-01-04\n"
    "2\tBo Lindgren\tbo@example.com\tPrefers email\\tno calls\t2026-02-11\n"
    "3\tChidi Okafor\t\\N\tLine one\\\nline two\t2026-03-09\n"
    "4\tDee Park\tdee@example.com\tC:\\\\Users\\\\dee\t\\N\n"
)
put("mysql.tsv", MYSQL)

# ------------------------------------------------------------ umsatz.csv
# A German export: semicolons, decimal commas, dots for thousands, and
# a column name with a comma in it, so the sniffer picks the comma.
UMSATZ = """Datum;Kunde;Ort;Umsatz, netto;MwSt
03.10.2026;Bäckerei Groß;Köln;1.250,00;237,50
07.10.2026;Café Müller;Bonn;89,90;17,08
12.10.2026;Hôtel Zürich;Zürich;12.400,00;0,00
"""
put("umsatz.csv", UMSATZ, "cp1252")

ORDERS = """Bestellung;Datum;Betrag;Land
A-1001;01.10.2026;1.199,00;DE
A-1002;02.10.2026;49,95;AT
A-1003;02.10.2026;12.000,50;CH
"""
put("orders.csv", ORDERS)

# ------------------------------------------------------------ survey.csv
SURVEY = """id, name, likes_python, team, score
1, 'Ana', yes, 'Data, Platform', 4.5
2, 'Bo', no, Web, 3
3, 'Chidi', Y, 'Infra', 5
4, 'Dee', N, , 2.5
"""
put("survey.csv", SURVEY)

# ------------------------------------------------------------ feedback.csv
# A form export whose free-text field was not quoted, so a comma in it
# makes a row too long, plus a row with a broken quote.
FEEDBACK = """ts,user,rating,comment
2026-10-01 09:12,ana,5,Great
2026-10-01 10:40,bo,3,Slow, but works
2026-10-02 14:03,chidi,4,"Fine"
2026-10-02 16:30,dee,2,"Crashed" twice
2026-10-03 08:05,eli,5,Love it
"""
put("feedback.csv", FEEDBACK)

FEEDBACK2 = """ts,user,rating,comment
2026-10-01 09:12,ana,5,Great
2026-10-01 10:40,bo,3,Slow, but works
2026-10-03 08:05,eli,5,Love it
2026-10-04 11:20,fay,1,No, no, no
"""
put("feedback2.csv", FEEDBACK2)

# ------------------------------------------------------------ claims.txt
# A pipe-delimited claims extract: inch marks in item names, and one
# name that starts with a quote.
CLAIMS = '''claim|member|item|amount
C-01|M-100|27" monitor|229.00
C-02|M-101|USB-C hub|39.90
C-03|M-102|"Pro" keyboard|119.00
C-04|M-103|Desk lamp 12"|24.50
'''
put("claims.txt", CLAIMS)

# ------------------------------------------------------------ others
TRAIL = """sku,qty,price
P-1,3,9.99,
P-2,1,24.00,
P-3,12,1.25,
"""
put("trailing.csv", TRAIL)

ROLES = """role,openings,notes
C# developer,3,remote
"F# engineer, senior",1,# urgent
Python developer,2,office
# end of list
"""
put("roles.csv", ROLES)

MIXED = """name ,qty;price
bolt , 120;0.05
nut ,300 ; 0.02
washer, 75;0.01
"""
put("mixed.csv", MIXED)

TSV = "city\tcountry\tpop_k\nOslo\tNorway\t709\nBergen\tNorway\t291\nAarhus\tDenmark\t285\n"
put("cities.tsv", TSV)

QUOTED = ('id,label,text\r\n1,a,"He said ""hi"""\r\n2,b,"two\r\nlines"\r\n'
          '3,c,plain\r\n')
put("quoted.csv", QUOTED)

SEMI = "id;name;note\n1;Ana;'x;y'\n2;Bo;'it''s'\n"
put("single.csv", SEMI)

WIN = "code,item,price\nA1,\x93Deluxe\x94 kettle,49.90\nA2,Mug \x96 4 pack,18.00\n"
put("win.csv", WIN.encode("latin-1"))

put("nul.csv", b"a,b\n1,x\x00y\n2,z\n")
put("empty.csv", b"")
put("blank.csv", b"\n\n\n")
put("onecol.txt", "alpha\nbeta\ngamma\n")
put("bom.csv", "﻿id;name\n1;Ana\n2;Bo\n")
put("eof.csv", 'a,b\n1,"open\n')
put("cr.csv", "a,b\r1,2\r3,4\r")

# ------------------------------------------------------------ jobs
SP = "{sp}"
JOBS = [
    # ratings and movies
    "read ratings.dat sep=:: header=None names=user,movie,rating,ts",
    "read ratings.dat sep=:: header=None names=user,movie,rating,ts usecols=user,rating nrows=6",
    "read ratings.dat sep=:: header=None names=user,movie,rating,ts index_col=0,1 head=4",
    "read ratings.dat sep=:: header=None names=user,movie,rating,ts chunksize=7",
    "read ratings.dat sep=:: header=None names=user,movie,rating,ts dtype=rating:float64,user:str head=3",
    "read ratings.dat sep=:: header=None names=user,movie,rating,ts dtype_backend=numpy_nullable head=3",
    "read ratings.dat sep=:: header=None",
    "read ratings.dat sep=:: head=3",
    "read ratings.dat sep=: header=None head=2",
    "read movies.dat sep=:: header=None names=movie,title,genres",
    "read movies.dat sep=:: header=None names=movie,title,genres encoding=latin-1",
    "read movies.dat sep=:: header=None names=movie,title,genres encoding=latin-1 index_col=movie usecols=movie,genres",
    "read movies.dat sep=:: header=None names=movie,title,genres encoding_errors=replace",
    "read movies.dat sep=:: header=None names=movie,title,genres encoding_errors=ignore head=3",
    "read movies.dat sep=:: header=None names=movie,title,genres encoding_errors=backslashreplace head=3",
    "read movies.dat sep=[:|] header=None encoding=latin-1",
    # whitespace-separated command output
    "read ls.txt sep=\\s+ skiprows=1 header=None",
    "read ls.txt sep=\\s+ skiprows=1 header=None on_bad_lines=warn",
    "read ls.txt sep=\\s+ skiprows=1 header=None on_bad_lines=skip names=mode,links,owner,group,size,month,day,time,name",
    "read ls.txt sep=\\s+ skiprows=1 header=None usecols=4,8",
    "read ls.txt sep=\\s+ header=None on_bad_lines=skip",
    "read ls.txt sep=" + SP + " skiprows=1 header=None",
    "read vmstat.txt sep=\\s+ skiprows=1",
    "read vmstat.txt sep=\\s+ header=1 usecols=r,b,free,us,sy,id,wa",
    "read vmstat.txt sep=\\s+ header=0,1",
    "read vmstat.txt sep=\\s+",
    # pipes
    "read psql.txt sep=\\s*\\|\\s* skiprows=[1] skipfooter=2",
    "read psql.txt sep=\\s*\\|\\s* skiprows=[1] skipfooter=2 true_values=t false_values=f",
    "read psql.txt sep=\\s*\\|\\s* skiprows=[1] skipfooter=2 true_values=t false_values=f dtype_backend=numpy_nullable",
    "read psql.txt sep=\\s*\\|\\s* skiprows=[1] skipfooter=2 index_col=id",
    "read psql.txt sep=| skiprows=[1] skipfooter=2",
    "read psql.txt sep=\\s*\\|\\s* skiprows=[1]",
    "read psql.txt sep=\\s*\\|\\s* skiprows=[1] nrows=4",
    "read psql.txt sep=\\s*\\|\\s* skiprows=[1] skipfooter=2 nrows=4",
    "read services.md sep=\\s*\\|\\s* skiprows=[1]",
    "read services.md sep=\\s*\\|\\s* skiprows=[1] usecols=Service,Port,SLO",
    "read services.md sep=| skiprows=[1] skipinitialspace=True",
    # MySQL tab export
    "read mysql.tsv sep={tab} header=None names=id,name,email,note,since",
    "read mysql.tsv sep={tab} header=None names=id,name,email,note,since escapechar=\\ na_values=\\N",
    "read mysql.tsv sep={tab} header=None names=id,name,email,note,since escapechar=\\ na_values=\\N quoting=3",
    "read mysql.tsv fn=table header=None escapechar=\\ na_values=\\N keep_default_na=False",
    "read mysql.tsv sep={tab} header=None escapechar=\\ quoting=3 na_filter=False",
    # sniffing
    "read orders.csv sep=None",
    "read orders.csv sep=None decimal=, thousands=.",
    "read orders.csv sep=None decimal=, thousands=. dtype=Datum:str",
    "read umsatz.csv sep=None encoding=cp1252",
    "read umsatz.csv sep=; encoding=cp1252 decimal=, thousands=.",
    "read umsatz.csv sep=; encoding=cp1252 decimal=, thousands=. dtype=Datum:str",
    "read umsatz.csv sep=;",
    "read cities.tsv sep=None",
    "read survey.csv sep=None",
    "read ls.txt sep=None skiprows=1 header=None",
    "read onecol.txt sep=None",
    "read bom.csv sep=None",
    "read bom.csv sep=;",
    "read roles.csv sep=None comment=#",
    "read services.md sep=None",
    # survey with spaces and single quotes
    "read survey.csv",
    "read survey.csv skipinitialspace=True",
    "read survey.csv skipinitialspace=True quotechar='",
    "read survey.csv skipinitialspace=True quotechar=' true_values=yes,Y false_values=no,N",
    "read survey.csv skipinitialspace=True quotechar=' true_values=yes,Y false_values=no,N dtype_backend=numpy_nullable",
    "read survey.csv skipinitialspace=True quotechar=' true_values=yes false_values=no",
    "read survey.csv skipinitialspace=True quotechar=' dtype=likes_python:bool",
    "read survey.csv skipinitialspace=True quotechar=' index_col=0 usecols=id,team",
    "read survey.csv sep=\\s*,\\s* quotechar='",
    # ragged and broken rows
    "read feedback.csv",
    "read feedback.csv on_bad_lines=warn",
    "read feedback.csv on_bad_lines=skip",
    "read feedback2.csv",
    "read feedback2.csv on_bad_lines=warn",
    "read feedback2.csv on_bad_lines=skip usecols=user,rating",
    "read feedback2.csv on_bad_lines=warn index_col=False",
    "read feedback2.csv on_bad_lines=warn skipfooter=1",
    "read feedback.csv on_bad_lines=skip skipfooter=1",
    "read feedback2.csv on_bad_lines=warn chunksize=2",
    "read feedback2.csv on_bad_lines=warn names=ts,user,rating,comment,more header=0",
    # claims with inch marks
    "read claims.txt sep=|",
    "read claims.txt sep=| on_bad_lines=warn",
    "read claims.txt sep=| quoting=3",
    "read claims.txt sep=| quoting=3 index_col=claim",
    "read claims.txt sep=| quotechar=~",
    "read claims.txt sep=| doublequote=False escapechar=\\",
    # trailing separators, comments, mixed separators
    "read trailing.csv",
    "read trailing.csv index_col=False",
    "read trailing.csv index_col=False usecols=sku,price",
    "read trailing.csv header=None",
    "read roles.csv",
    "read roles.csv comment=#",
    "read roles.csv comment=# skip_blank_lines=False",
    "read mixed.csv sep=[;,]",
    "read mixed.csv sep=\\s*[;,]\\s*",
    "read mixed.csv sep=(;|,)",
    "read mixed.csv sep=,",
    # tabs, quotes, line ends
    "read cities.tsv fn=table",
    "read cities.tsv dialect=excel-tab",
    "read cities.tsv dialect=excel-tab sep=,",
    "read cities.tsv dialect=excel-tab sep=;",
    "read survey.csv dialect=unix skipinitialspace=True",
    "read cities.tsv sep={tab} index_col=0 dtype=pop_k:Int64",
    "read quoted.csv",
    "read quoted.csv quoting=3",
    "read quoted.csv skiprows=[2]",
    "read quoted.csv skiprows=1 header=None",
    "read quoted.csv sep=, doublequote=False",
    "read single.csv sep=; quotechar='",
    "read single.csv sep=; quotechar=' doublequote=False",
    "read cr.csv",
    "read cr.csv sep=,",
    # encodings
    "read win.csv",
    "read win.csv encoding=cp1252",
    "read win.csv encoding_errors=replace",
    "read win.csv encoding_errors=ignore",
    "read win.csv encoding_errors=backslashreplace",
    "read win.csv encoding=ascii encoding_errors=replace",
    "read win.csv encoding=latin-1",
    "read umsatz.csv encoding=utf-8 encoding_errors=replace sep=;",
    # errors and edge cases
    "read nul.csv usecols=a",
    "read nul.csv usecols=a sep=None",
    "read eof.csv",
    "read eof.csv on_bad_lines=skip",
    "read empty.csv",
    "read empty.csv sep=None",
    "read empty.csv names=a,b",
    "read blank.csv",
    "read blank.csv sep=None",
    "read missing.csv",
    "read ratings.dat sep=:: header=None names=a,b,a,c",
    "read ratings.dat sep=:: header=None on_bad_lines=maybe",
    "read ratings.dat sep=:: header=None quoting=7",
    "read cities.tsv sep={tab} quoting=7",
    "read cities.tsv sep={tab} escapechar=ab",
    "read cities.tsv sep={tab} quotechar=~~",
    "read ratings.dat sep=::( header=None",
    "read ratings.dat sep=[:: header=None",
    "read ratings.dat sep=:: header=None delimiter=,",
    "read ratings.dat sep=:: header=None encoding_errors=loud",
    "read ratings.dat sep=:: header=None index_col=True",
    "read ratings.dat sep=:: header=None usecols=0,9",
    "read survey.csv quotechar='' ",
    "read survey.csv sep=,, header=None",
    "read survey.csv dialect=fancy",
]
with open(os.path.join(DATA, "jobs.txt"), "w", encoding="utf-8") as f:
    for j in JOBS:
        f.write(j.strip() + "\n")
