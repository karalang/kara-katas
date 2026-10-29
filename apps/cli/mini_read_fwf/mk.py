"""Writes data/: the fixed-width files the jobs read, each shaped like a
file people meet (a weather-station inventory in the GHCN layout, a
mainframe payroll export with header and trailer records, the output of
kubectl, df and docker, a DataFrame printed with to_string, a bank
ledger in ISO-8859-1, a sensor log with comments and CRLF line ends, a
register padded with underscores, a file with a byte-order mark), the
broken inputs people meet, and data/jobs.txt, one job per line.
oracle.py runs each job on pandas' read_fwf, mini_read_fwf.kara on its
own port.

Every value is made up; the account numbers are not real.

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


# ------------------------------------------------------------ stations.txt
# The GHCN-Daily station inventory layout: ID 1-11, latitude 13-20,
# longitude 22-30, elevation 32-37 (-999.9 when unknown), state 39-40,
# name 42-71, GSN flag 73-75, HCN/CRN flag 77-79, WMO id 81-85, with
# no header. Names hold spaces, most flags and many WMO ids are blank.
STATIONS = [
    ("USW00014819", 41.7861, -87.7522, 186.5, "IL", "CHICAGO MIDWAY AP", "", "", "72534"),
    ("USW00094846", 41.9950, -87.9336, 201.8, "IL", "CHICAGO OHARE INTL AP", "", "", "72530"),
    ("USC00111577", 41.7372, -87.7775, 189.0, "IL", "CHICAGO MIDWAY 3 SW", "", "HCN", ""),
    ("USC00116610", 41.0181, -88.0472, -999.9, "IL", "PEOTONE", "", "HCN", ""),
    ("USW00023174", 33.9381, -118.3889, 29.6, "CA", "LOS ANGELES INTL AP", "", "", "72295"),
    ("USW00023188", 32.7336, -117.1831, 4.6, "CA", "SAN DIEGO LINDBERGH FLD", "GSN", "", "72290"),
    ("USC00045114", 37.4806, -119.9772, 640.1, "CA", "MARIPOSA RS", "", "", ""),
    ("USS0020H13S", 39.3200, -120.3700, 2133.6, "CA", "INDEPENDENCE LAKE", "", "", ""),
    ("USW00094728", 40.7789, -73.9692, 39.6, "NY", "NEW YORK CNTRL PK TWR", "", "HCN", "72506"),
    ("USW00014732", 40.7794, -73.8803, 3.4, "NY", "NEW YORK LAGUARDIA AP", "", "", "72503"),
    ("USC00300183", 42.7667, -78.6167, 274.3, "NY", "AURORA", "", "", ""),
    ("USW00012839", 25.7881, -80.3169, 8.8, "FL", "MIAMI INTL AP", "GSN", "", "72202"),
    ("USW00012921", 29.5442, -98.4839, 241.7, "TX", "SAN ANTONIO INTL AP", "", "", "72253"),
    ("USC00415196", 30.2844, -97.7347, 172.2, "TX", "AUSTIN CAMP MABRY", "", "HCN", ""),
    ("USW00024233", 47.4444, -122.3139, 112.8, "WA", "SEATTLE TACOMA INTL AP", "GSN", "", "72793"),
    ("USR0000WTRO", 48.4500, -120.1667, 1219.2, "WA", "TWISP RAWS", "", "", ""),
    ("USW00026451", 61.1689, -150.0278, 36.6, "AK", "ANCHORAGE INTL AP", "GSN", "", "70273"),
    ("CA001108395", 49.1950, -123.1814, 4.3, "BC", "VANCOUVER INTL A", "", "", "71892"),
    ("CA006158355", 43.6772, -79.6306, 173.4, "ON", "TORONTO INTL A", "", "", "71624"),
    ("MXN00009048", 19.4000, -99.1833, 2303.0, "", "TACUBAYA CENTRAL D.F.", "GSN", "", "76680"),
    ("GME00127786", 52.4631, 13.3017, 51.0, "", "BERLIN-DAHLEM", "GSN", "", "10381"),
    ("FRE00106207", 48.8167, 2.3333, 75.0, "", "PARIS/LE BOURGET", "", "", "07150"),
    ("UK000056225", 51.4780, -0.4610, 25.0, "", "HEATHROW", "", "", "03772"),
    ("ASN00066062", -33.8607, 151.2050, 39.0, "", "SYDNEY (OBSERVATORY HILL)", "GSN", "", "94768"),
    ("JA000047662", 35.6830, 139.7670, 36.0, "", "TOKYO", "GSN", "", "47662"),
    ("SF000068816", -33.9670, 18.6000, 46.0, "", "CAPE TOWN INTL", "GSN", "", "68816"),
    ("AYM00089606", -66.2830, 110.5170, -999.9, "", "CASEY", "", "", "89611"),
]


def station(r):
    sid, lat, lon, elev, st, name, gsn, hcn, wmo = r
    return f"{sid:11} {lat:8.4f} {lon:9.4f} {elev:6.1f} {st:2} {name:30} {gsn:3} {hcn:3} {wmo:5}"


put("stations.txt", "".join(station(r) + "\n" for r in STATIONS))

# ------------------------------------------------------------ payroll.dat
# A mainframe export: one header record, detail records, one trailer
# record. Detail layout (widths 1, 6, 15, 12, 4, 8, 9, 1): record type,
# zero-padded employee number, last name, first name, department, hire
# date as YYYYMMDD, salary in cents (zero-padded), status (A, L, T).
PAY = [
    (17, "OKONKWO", "ADAEZE", "FIN", "20120305", 9875000, "A"),
    (42, "LINDQVIST", "MAJA", "ENG", "20150914", 12450000, "A"),
    (108, "HERNANDEZ", "JOSE LUIS", "ENG", "20180102", 11800050, "L"),
    (215, "NAKAMURA", "KENJI", "OPS", "20190617", 6420000, "A"),
    (377, "O'BRIEN", "SIOBHAN", "HR", "20200810", 7100000, "T"),
    (512, "DUBOIS", "CAMILLE", "FIN", "20210201", 8350075, "A"),
    (640, "MBEKI", "THABO", "OPS", "20220711", 5980000, "A"),
    (733, "KOWALSKI", "PIOTR", "ENG", "20230320", 10500000, "A"),
    (901, "SINGH", "HARPREET", "SALE", "20240115", 6875000, "A"),
    (1024, "ROSSI", "GIULIA", "SALE", "20250506", 7210000, "L"),
]


def pay(r):
    emp, last, first, dept, hired, cents, st = r
    return f"D{emp:06d}{last:15}{first:12}{dept:4}{hired}{cents:09d}{st}"


put(
    "payroll.dat",
    "H20261031PAYROLL EXPORT V2 ACME CORP\n"
    + "".join(pay(r) + "\n" for r in PAY)
    + f"T{len(PAY):06d}{sum(r[5] for r in PAY):015d}\n",
)

# ------------------------------------------------------------ pods.txt
# `kubectl get pods`: a header row, columns padded to the widest value
# with three spaces between, and RESTARTS cells such as `12 (4m ago)`.
put(
    "pods.txt",
    """NAME                                READY   STATUS             RESTARTS       AGE
api-gateway-7d9f8b6c4-2xkqp         1/1     Running            0              3d4h
api-gateway-7d9f8b6c4-9wzlm         1/1     Running            1 (2d ago)     3d4h
billing-worker-5c6b7d8e9-abcde      0/1     CrashLoopBackOff   12 (4m ago)    61m
billing-worker-5c6b7d8e9-fghij      1/1     Running            0              61m
nightly-report-28911340-x7k2p       0/1     Completed          0              7h
postgres-0                          2/2     Running            0              14d
redis-6f8d9c7b5-q4r8t               1/1     Running            3 (5d12h ago)  14d
search-indexer-84c7f6d9b-tt2mn      0/1     Pending            0              8s
""",
)

# ------------------------------------------------------------ df.txt
# `df -h`: the last header is two words, `Mounted on`.
put(
    "df.txt",
    """Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p2  468G  201G  244G  46% /
tmpfs           7.8G  1.2M  7.8G   1% /dev/shm
/dev/nvme0n1p1  511M  6.1M  505M   2% /boot/efi
/dev/sda1       3.6T  2.9T  540G  85% /mnt/backup
nas:/export     11T   8.4T  2.1T  81% /mnt/nas
""",
)

# ------------------------------------------------------------ docker.txt
# `docker ps`: values with single spaces inside (`2 hours ago`), a quoted
# command cut with an ellipsis, and an empty PORTS cell.
put(
    "docker.txt",
    """CONTAINER ID   IMAGE                COMMAND                  CREATED        STATUS                    PORTS                    NAMES
3f2a9c1d7e4b   nginx:1.27-alpine    "/docker-entrypoint.…"   2 hours ago    Up 2 hours                0.0.0.0:8080->80/tcp     web
a81c55e0b9f3   postgres:16          "docker-entrypoint.s…"   3 days ago     Up 3 days (healthy)       5432/tcp                 db
5be7d042c6a1   redis:7.4            "docker-entrypoint.s…"   3 days ago     Up 3 days                 6379/tcp                 cache
c09e1f3a2d88   acme/worker:2.3.1    "python -m worker"       45 minutes ago Exited (1) 40 minutes ago                          worker
""",
)

# ------------------------------------------------------------ frame.txt
# A DataFrame printed with to_string() and pasted into a file: the index
# column has no header, NaN is spelled out, numbers are right-aligned.
put(
    "frame.txt",
    """         city  temp_c  rain_mm  stations
0        Oslo   -3.50      NaN         4
1   Reykjavík    1.25     12.0         2
2    Helsinki   -7.00      0.4         6
3   Stockholm   -1.00      3.2         5
4  Copenhagen    2.50      NaN         3
5      Tromsø  -11.75      8.1         1
""",
)

# ------------------------------------------------------------ ledger.txt
# A bank ledger in ISO-8859-1 with German numbers (1.234,56) and a
# minus sign after the amount on some rows: printed by a COBOL report
# writer, so the column titles are underlined with dashes.
LEDGER = [
    ("01.10.2026", "Gehalt Oktober", "3.250,00", "EUR"),
    ("02.10.2026", "Miete Wohnung Köln", "-1.180,00", "EUR"),
    ("05.10.2026", "Café Müller", "-12,40", "EUR"),
    ("07.10.2026", "Überweisung Sparkonto", "-500,00", "EUR"),
    ("12.10.2026", "Rückerstattung Hôtel Zürich", "86,15", "CHF"),
    ("15.10.2026", "Bäckerei Groß", "-7,95", "EUR"),
    ("20.10.2026", "Strom (Abschlag)", "-74,00", "EUR"),
    ("28.10.2026", "Zinsen", "0,83", "EUR"),
]
ledger = "Datum       Buchungstext                    Betrag     Währung\n"
ledger += "----------  ------------------------------  ---------  -------\n"
for d, t, b, c in LEDGER:
    ledger += f"{d:10}  {t:30}  {b:>9}  {c:7}\n"
put("ledger.txt", ledger, "latin-1")

# ------------------------------------------------------------ sensors.log
# A logger's export: CRLF line ends, comment lines and trailing comments,
# blank lines, -9999 and ERR for a failed reading, and a timestamp with
# a space inside it. The last rows have wider values than the first.
SENS = [
    ("2026-10-29 06:00", "T-101", "4.2", "81", "1013.2"),
    ("2026-10-29 06:10", "T-101", "4.1", "82", "1013.1"),
    ("2026-10-29 06:20", "T-102", "-9999", "80", "1013.0"),
    ("2026-10-29 06:30", "T-102", "3.8", "ERR", "1012.8"),
    ("2026-10-29 06:40", "T-101", "3.6", "84", "1012.7"),
    ("2026-10-29 06:50", "T-103", "3.5", "85", "1012.5"),
    ("2026-10-29 07:00", "T-103", "3.9", "83", "1012.6"),
    ("2026-10-29 07:10", "T-101", "4.4", "79", "1012.9"),
    ("2026-10-29 07:20", "T-1044", "-12.75", "100", "998.25"),
    ("2026-10-29 07:30", "T-1044", "-13.5", "100", "997.5"),
]
log = "# station export v3\r\n# fields: time sensor temp_c rh_pct hpa\r\n"
log += "time              sensor  temp_c  rh_pct  hpa\r\n"
for k, (t, s, temp, rh, hpa) in enumerate(SENS):
    if k == 4:
        log += "\r\n# logger restarted\r\n"
    note = "   # gust" if k == 6 else ""
    log += f"{t:16}  {s:6}  {temp:>6}  {rh:>6}  {hpa:>6}{note}\r\n"
log += "\r\n"
put("sensors.log", log)

# ------------------------------------------------------------ register.txt
# A register padded with underscores instead of spaces, with spaces
# inside values.
REG = [
    ("A-1", "Ana María López", "Valencia", "1,200"),
    ("A-2", "Bob Smith", "Leeds", "950"),
    ("B-1", "Chen Wei", "Shenzhen", "2,075"),
    ("B-2", "Dagny Ødegaard", "Bergen", ""),
]
reg = "code__name_________________city________amount\n"
for c, n, ci, a in REG:
    reg += f"{c:_<6}{n:_<21}{ci:_<12}{a:_>6}\n"
put("register.txt", reg)

# ------------------------------------------------------------ bom.txt
# A Windows export: a UTF-8 byte-order mark before the header.
put(
    "bom.txt",
    "﻿sku     qty  price\nAB-100    3  19.99\nAB-101   12   4.50\nCD-200    1 120.00\n",
)

# ------------------------------------------------------------ named.txt
# A DataFrame with a named index printed with to_string(): the index
# name sits on a row of its own under the column names.
put(
    "named.txt",
    """           temp_c  stations
city                       
Oslo        -3.50         4
Reykjavík    1.25         2
Helsinki    -7.00         6
""",
)

# ------------------------------------------------------------ grouped.txt
# A frame with a two-level index printed with to_string(): a repeated
# outer label is left blank.
put(
    "grouped.txt",
    """                temp
country city        
NO      Oslo    1.50
        Bergen  2.00
SE      Lund     NaN
        Malmö   4.25
""",
)

# ------------------------------------------------------------ mac.txt
# Classic Mac OS line ends: a bare carriage return.
put("mac.txt", "id  qty  item\r1     5  bolt\r2    12  nut\r3     7  washer\r")

# ------------------------------------------------------------ invoice.txt
# An invoice exported in windows-1252: a euro sign, curly quotes and an
# en dash in the header and the cells.
INV = [
    ("A-100", "\u201cDeluxe\u201d kettle", "49,90 \u20ac"),
    ("A-101", "Mug \u2013 set of 4", "18,00 \u20ac"),
    ("B-200", "Tea (loose, 250 g)", "7,25 \u20ac"),
]
inv = "Code   \u201cItem\u201d                   Price\n"
for c, i, pr in INV:
    inv += f"{c:7}{i:25}{pr:>9}\n"
put("invoice.txt", inv, "cp1252")

# ------------------------------------------------------------ broken input
put("empty.txt", "")
put("blank.txt", "\n   \n\n")

STA = (
    "colspecs=0:11,12:20,21:30,31:37,38:40,41:71,72:75,76:79,80:85 header=None "
    "names=id,lat,lon,elev,state,name,gsn,hcn,wmo"
)
PAYW = "widths=1,6,15,12,4,8,9,1 header=None names=rec,emp,last,first,dept,hired,salary,status"
JOBS = [
    # stations: the published layout, then what people try first
    f"read stations.txt {STA} head=6",
    f"read stations.txt {STA} dtype=wmo:str,hcn:str na_values=elev:-999.9 head=6",
    f"read stations.txt {STA} keep_default_na=False dtype=str head=4",
    f"read stations.txt {STA} usecols=id,name,elev index_col=id head=8",
    f"read stations.txt {STA} usecols=0,5 head=3",
    "read stations.txt header=None head=6",
    "read stations.txt header=None infer_nrows=3 head=6",
    "read stations.txt colspecs=:11,41:71 header=None names=id,name head=4",
    "read stations.txt colspecs=:11,41: header=None names=id,rest head=4",
    "read stations.txt widths=11,9,10,7,3,31,4,4,6 header=None head=3",
    "read stations.txt widths=11,9,10 header=None names=id,lat,lon nrows=4",
    f"read stations.txt {STA} skiprows=0,1,2 nrows=3",
    f"read stations.txt {STA} skiprows=20",
    f"read stations.txt {STA} chunksize=10 usecols=id,state",
    f"read stations.txt {STA} nrows=12 chunksize=5 usecols=id,elev",
    f"read stations.txt {STA} index_col=4,0 usecols=id,state,lat head=5",
    # payroll: header and trailer records
    f"read payroll.dat {PAYW}",
    f"read payroll.dat {PAYW} skiprows=1 skipfooter=1",
    f"read payroll.dat {PAYW} skiprows=1 skipfooter=1 dtype=emp:str,hired:str index_col=emp",
    f"read payroll.dat {PAYW} skiprows=1 skipfooter=1 usecols=emp,last,salary dtype=emp:str",
    f"read payroll.dat {PAYW} skiprows=1 skipfooter=1 dtype=salary:float64,dept:category",
    f"read payroll.dat {PAYW} skiprows=1 skipfooter=1 dtype=status:bool",
    f"read payroll.dat {PAYW} skiprows=1 skipfooter=1 dtype=emp:Int64,salary:Float64,last:string",
    f"read payroll.dat {PAYW} skiprows=1 skipfooter=1 dtype_backend=numpy_nullable",
    f"read payroll.dat {PAYW} skiprows=1 skipfooter=1 dtype=last:int64",
    f"read payroll.dat {PAYW} skiprows=1 nrows=3",
    f"read payroll.dat {PAYW} skiprows=1 skipfooter=1 nrows=3",
    f"read payroll.dat {PAYW} skiprows=1 skipfooter=1 chunksize=4",
    f"read payroll.dat widths=1,6,15 header=None names=rec,emp,last,first",
    f"read payroll.dat widths=1,6,15 header=None names=rec,emp",
    f"read payroll.dat widths=1,6,15 header=None names=emp,last index_col=0",
    f"read payroll.dat widths=1,6,15 colspecs=0:1 header=None",
    "read payroll.dat colspecs=None",
    # command output with a header row
    "read pods.txt",
    "read pods.txt colspecs=0:36,36:44,44:63,63:78,78:",
    "read pods.txt colspecs=0:36,36:44,44:63,63:78,78: usecols=NAME,STATUS,RESTARTS",
    "read pods.txt colspecs=0:36,36:44,44:63,63:78,78: index_col=NAME usecols=NAME,READY",
    "read pods.txt colspecs=0:36,36:44,44:63,63:78,78: usecols=NAME,UPTIME",
    "read pods.txt colspecs=0:36,36:44,44:63,63:78,78: usecols=0,7",
    "read df.txt",
    "read df.txt colspecs=0:15,15:21,21:27,27:33,33:38,38:",
    "read df.txt colspecs=0:15,15:21,21:27,27:33,33:38,38: na_values=11T",
    "read docker.txt",
    "read docker.txt colspecs=0:15,15:36,36:61,61:76,76:102,102:127,127:",
    "read docker.txt colspecs=0:15,15:36,36:61,61:76,76:102,102:127,127: keep_default_na=False usecols=NAMES,PORTS",
    # a printed DataFrame read back
    "read frame.txt",
    "read frame.txt index_col=0",
    "read frame.txt index_col=1",
    "read frame.txt index_col=0 dtype=stations:float64 na_values=Oslo",
    "read frame.txt index_col=0 usecols=city,rain_mm",
    "read frame.txt header=1 head=2",
    "read frame.txt header=0,1 index_col=0",
    "read frame.txt header=9",
    "read frame.txt names=a,b,c,d,e",
    "read frame.txt names=idx,city,temp,rain,n skiprows=1",
    "read frame.txt names=city,temp,rain,n skiprows=1",
    "read frame.txt names=a,b,c skiprows=1",
    "read frame.txt index_col=7",
    # the ledger in ISO-8859-1
    "read ledger.txt",
    "read ledger.txt encoding=latin-1",
    "read ledger.txt encoding=latin-1 skiprows=1",
    "read ledger.txt encoding=latin-1 skiprows=[1] decimal=, thousands=.",
    "read ledger.txt encoding=cp1252 skiprows=[1] decimal=, thousands=. dtype_backend=numpy_nullable",
    "read ledger.txt encoding=iso-8859-1 skiprows=[1] thousands=. usecols=Datum,Betrag",
    "read ledger.txt encoding=latin-1 skiprows=[1] decimal=,, thousands=.",
    "read ledger.txt encoding=ebcdic",
    # the sensor log
    "read sensors.log",
    "read sensors.log comment=#",
    "read sensors.log comment=# na_values=-9999,ERR",
    "read sensors.log comment=# na_values=-9999,ERR infer_nrows=5",
    "read sensors.log comment=# colspecs=0:16,18:24,26:32,34:40,42:48 na_values=-9999,ERR",
    "read sensors.log comment=# colspecs=0:16,18:24,26:32,34:40,42:48 skip_blank_lines=False",
    "read sensors.log comment=# colspecs=0:16,18:24,26:32,34:40,42:48 chunksize=4",
    "read sensors.log comment=# colspecs=0:16,18:24,26:32,34:40,42:48 nrows=5 skiprows=4,8",
    "read sensors.log skiprows=0,1 colspecs=0:16,18:24,26:32,34:40,42:48",
    "read sensors.log skiprows=2 comment=# header=None colspecs=0:16,18:24,26:32,34:40,42:48",
    "read sensors.log comment=# colspecs=0:16,18:24,26:32,34:40,42:48 na_filter=False",
    "read sensors.log comment=# colspecs=0:16,18:24,26:32,34:40,42:48 dtype=hpa:int64",
    "read sensors.log comment=# colspecs=0:16,18:24,26:32,34:40,42:48 na_values=-9999,ERR dtype=rh_pct:int64",
    # the underscore register
    "read register.txt",
    "read register.txt delimiter=_",
    "read register.txt delimiter=_ thousands=,",
    "read register.txt delimiter=_ thousands=, dtype_backend=numpy_nullable",
    "read register.txt delimiter=_ colspecs=0:6,6:27,27:39,39:45 thousands=,",
    "read register.txt delimiter=_, thousands=,",
    # the byte-order mark
    "read bom.txt",
    "read bom.txt colspecs=0:6,6:12,12:19",
    "read bom.txt colspecs=0:6,6:12,12:19 encoding=utf-8-sig",
    "read bom.txt header=None",
    # printed frames with a named index
    "read named.txt",
    "read named.txt index_col=0",
    "read named.txt header=0,1 index_col=0",
    "read grouped.txt",
    "read grouped.txt header=0,1",
    "read grouped.txt header=0,1 index_col=0,1",
    "read grouped.txt skiprows=[1] index_col=0,1",
    # old line ends, and a windows-1252 invoice
    "read mac.txt",
    "read mac.txt header=None",
    "read invoice.txt",
    "read invoice.txt encoding=cp1252",
    "read invoice.txt encoding=windows-1252 decimal=,",
    "read invoice.txt encoding=latin-1",
    "read invoice.txt encoding=ascii",
    # more of the reader's options
    "read pods.txt names=a,b,c,d,e header=0",
    "read pods.txt names=a,b,c header=0",
    "read stations.txt header=None usecols=0,4 nrows=3",
    f"read stations.txt {STA} na_values=state:IL|CA,wmo:72530 keep_default_na=False head=5",
    f"read stations.txt {STA} dtype=str index_col=0 head=3",
    f"read stations.txt {STA} skiprows=30",
    f"read stations.txt {STA} chunksize=4 nrows=10 index_col=id usecols=id,lat",
    "read stations.txt colspecs=0:5,3:8,100:120 header=None nrows=2",
    "read ledger.txt encoding=latin-1 skiprows=[1] thousands=. decimal=, dtype=Datum:str",
    "read register.txt delimiter=_ dtype=amount:float64",
    "read register.txt delimiter=_ names=code,name,city,amount",
    "read df.txt usecols=0,5 header=None",
    "read frame.txt index_col=0 chunksize=4",
    "read frame.txt header=0,1 index_col=0 nrows=2",
    "read frame.txt index_col=city",
    "read frame.txt index_col=nope",
    "read frame.txt dtype=city:category,stations:Float64 index_col=0",
    # broken input
    "read empty.txt",
    "read empty.txt colspecs=0:5,5:9",
    "read empty.txt colspecs=0:5,5:9 names=a,b",
    "read blank.txt",
    "read blank.txt colspecs=0:5",
    "read blank.txt colspecs=0:5 names=a",
    "read missing.txt",
    "read stations.txt infer_nrows=0",
]
with open(os.path.join(DATA, "jobs.txt"), "w", encoding="utf-8") as f:
    for j in JOBS:
        f.write(j + "\n")
