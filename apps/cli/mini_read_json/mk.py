"""Writes data/: the JSON files the jobs read, each shaped like a file
people hand to pandas' read_json (an issue tracker's API page, an
NDJSON request log, a sensor feed, exports from DataFrame.to_json in
every orient, a table-schema export, a price list with long decimals, a
customer list with zip codes, IDs past 2**63), the broken inputs people
meet (a log with a cut-off line, a file with a byte-order mark,
Python's NaN and Infinity, a latin-1 file), and data/jobs.txt, one job
per line. oracle.py runs each job on pandas' read_json,
mini_read_json.kara on its own port.

Every value is made up; the names, e-mail addresses and IDs are not
real.

Run: python3 -s -P -B mk.py"""
import json
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


# ------------------------------------------------------------ issues.json
# A page of an issue tracker's REST API: a list of records, ISO 8601
# times in UTC, a null closed_at, nested user and label objects.
ISSUES = [
    {"id": 2381001, "number": 412, "title": "Crash on empty config file",
     "state": "closed", "user": {"login": "ana-r", "id": 501},
     "labels": [{"name": "bug"}, {"name": "p1"}], "comments": 7,
     "created_at": "2026-09-14T08:12:44Z", "closed_at": "2026-09-16T17:03:10Z",
     "locked": False},
    {"id": 2381377, "number": 418, "title": "Add --dry-run to sync",
     "state": "open", "user": {"login": "bo-l", "id": 502},
     "labels": [{"name": "enhancement"}], "comments": 2,
     "created_at": "2026-09-21T13:40:02Z", "closed_at": None, "locked": False},
    {"id": 2382950, "number": 431, "title": "Docs: \"retry\" section is out of date",
     "state": "open", "user": {"login": "chidi-o", "id": 503},
     "labels": [], "comments": 0,
     "created_at": "2026-10-02T22:05:51Z", "closed_at": None, "locked": True},
    {"id": 2384114, "number": 437, "title": "Ünïcödé file names fail on Windows",
     "state": "closed", "user": {"login": "dee-p", "id": 504},
     "labels": [{"name": "bug"}, {"name": "windows"}], "comments": 12,
     "created_at": "2026-10-09T06:30:00Z", "closed_at": "2026-10-11T09:45:30Z",
     "locked": False},
]
put("issues.json", json.dumps(ISSUES, indent=2, ensure_ascii=False) + "\n")

# ------------------------------------------------------------ requests.ndjson
# An NDJSON access log: one object per line, epoch milliseconds in
# `timestamp`, a field that only some lines have, a blank line, a
# trailing newline.
REQS = [
    {"timestamp": 1790841600123, "method": "GET", "path": "/api/items", "status": 200, "ms": 12.5},
    {"timestamp": 1790841600480, "method": "POST", "path": "/api/items", "status": 201, "ms": 48.25, "user": "u-17"},
    {"timestamp": 1790841601002, "method": "GET", "path": "/api/items/9", "status": 404, "ms": 3.0},
    {"timestamp": 1790841601777, "method": "DELETE", "path": "/api/items/4", "status": 204, "ms": 20.0, "user": "u-17"},
    {"timestamp": 1790841602350, "method": "GET", "path": "/health", "status": 200, "ms": 0.75},
    {"timestamp": 1790841603901, "method": "PUT", "path": "/api/items/4", "status": 409, "ms": 31.125, "user": "u-23"},
    {"timestamp": 1790841604010, "method": "GET", "path": "/api/items", "status": 500, "ms": 1003.5},
]
lines = [json.dumps(r, separators=(",", ":")) for r in REQS]
lines.insert(4, "")
put("requests.ndjson", "\n".join(lines) + "\n")

# A log whose last line was cut off when the disk filled.
put("cutoff.ndjson", "\n".join(lines[:3]) + '\n{"timestamp":1790841601777,"method":"DEL\n')

# A log with Windows line ends.
put("crlf.ndjson", "\r\n".join(lines[:3]) + "\r\n")

# ------------------------------------------------------------ sensors.ndjson
# A sensor feed: epoch seconds in `time`, readings with nulls, a battery
# flag, one reading that is a string.
SENS = []
for i in range(9):
    SENS.append({
        "time": 1790812800 + 600 * i, "sensor": "s-%d" % (1 + i % 3),
        "temp_c": [21.5, 21.75, None, 22.0, 22.25, 21.0, 20.5, None, 19.75][i],
        "rh": [40, 41, 39, 45, 44, 47, 52, 51, 55][i],
        "low_battery": i in (2, 7),
    })
SENS[5]["rh"] = "ERR"
put("sensors.ndjson", "\n".join(json.dumps(r) for r in SENS) + "\n")

# ------------------------------------------------------------ orients
# What DataFrame.to_json writes in each orient, written out by hand so
# the file does not depend on the writer: split, index, columns,
# values and records.
put("split.json", '{"columns":["sku","name","price","in_stock"],'
    '"index":[0,1,2],"data":[["A-100","Kettle",24.99,true],'
    '["A-101","Toaster",39.5,false],["A-102","Mug, 4 pack",18.0,true]]}\n')
put("split_named.json", '{"columns":["qty","price"],"index":["2026-10-01","2026-10-02","2026-10-05"],'
    '"data":[[3,9.5],[1,24.0],[7,1.25]]}\n')
put("split_bad.json", '{"columns":["a"],"index":[0],"data":[[1]],"name":"x"}\n')
put("split_dup.json", '{"columns":["a","b","a"],"index":[0,1],"data":[[1,2,3],[4,5,6]]}\n')
put("index.json", '{"ber":{"city":"Berlin","country":"DE","pop_k":3755,"founded":1237},'
    '"osl":{"city":"Oslo","country":"NO","pop_k":709,"founded":1048},'
    '"lis":{"city":"Lisbon","country":"PT","pop_k":545}}\n')
put("columns.json", '{"region":{"0":"north","1":"south","2":"east","3":"west"},'
    '"units":{"0":120,"1":95,"2":null,"3":140},'
    '"revenue":{"0":1500.0,"1":1187.5,"2":0.0,"3":1750.25}}\n')
put("columns_dates.json", '{"close":{"1790812800000":101.5,"1790899200000":102.25,"1791158400000":99.75},'
    '"volume":{"1790812800000":1200,"1790899200000":980,"1791158400000":1510}}\n')
put("values.json", '[[1,"north",120.5],[2,"south",null],[3,"east",98.25]]\n')
put("ragged.json", '[[1,"north"],[2,"south",3.5],[3]]\n')
put("records_mixed.json", '[{"a":1,"b":"x"},{"b":"y","c":true},{"a":3,"c":false,"d":null}]\n')

# ------------------------------------------------------------ table.json
# A table-schema export (orient="table"), with a tz-aware time, a
# category and a nullable integer.
put("table.json", json.dumps({
    "schema": {
        "fields": [
            {"name": "order_id", "type": "integer"},
            {"name": "placed", "type": "datetime", "tz": "UTC"},
            {"name": "status", "type": "any", "constraints": {"enum": ["new", "paid", "shipped"]}, "ordered": False},
            {"name": "total", "type": "number"},
            {"name": "gift", "type": "boolean"},
            {"name": "note", "type": "string"},
            {"name": "items", "type": "integer", "extDtype": "Int64"},
        ],
        "primaryKey": ["order_id"],
        "pandas_version": "1.4.0",
    },
    "data": [
        {"order_id": 9001, "placed": "2026-10-03T09:15:00.000Z", "status": "paid", "total": 59.9, "gift": False, "note": "leave at door", "items": 2},
        {"order_id": 9002, "placed": "2026-10-03T11:02:30.500Z", "status": "new", "total": 12.0, "gift": True, "note": None, "items": None},
        {"order_id": 9003, "placed": "2026-10-04T18:45:00.000Z", "status": "shipped", "total": 240.75, "gift": False, "note": "fragile", "items": 5},
    ],
}) + "\n")
put("table_noindex.json", json.dumps({
    "schema": {
        "fields": [
            {"name": "index", "type": "integer"},
            {"name": "day", "type": "datetime"},
            {"name": "kwh", "type": "number"},
        ],
        "primaryKey": ["index"],
        "pandas_version": "1.4.0",
    },
    "data": [
        {"index": 0, "day": "2026-10-01T00:00:00.000", "kwh": 7.5},
        {"index": 1, "day": "2026-10-02T00:00:00.000", "kwh": 6.25},
    ],
}) + "\n")

# ------------------------------------------------------------ series
put("daily.json", '{"2026-10-01":412,"2026-10-02":398,"2026-10-03":455,"2026-10-04":0}\n')
put("series_split.json", '{"name":"visits","index":["mon","tue","wed"],"data":[120,98,143]}\n')
put("series_list.json", '[3.5,null,4.25,1.0]\n')

# ------------------------------------------------------------ numbers
# A price list with long decimals: the default decoder sums digit by
# digit and drops digits past the fifteenth.
put("prices.json", '[{"sku":"P-1","price":0.1,"rate":1.0000000000000002},'
    '{"sku":"P-2","price":3.14159265358979,"rate":0.30000000000000004},'
    '{"sku":"P-3","price":1577.2,"rate":2.5e-3},'
    '{"sku":"P-4","price":12345.678901234567,"rate":6.02214076E23}]\n')
# Customer IDs and zip codes stored as strings, and a column of numbers
# as strings.
put("customers.json", '[{"cust_id":"000123","zip":"02139","phone":"5550142","balance":"120.50","name":"Ana Ruiz"},'
    '{"cust_id":"000124","zip":"10001","phone":"5550199","balance":"-3","name":"Bo Lindgren"},'
    '{"cust_id":"000125","zip":"94105","phone":"5550123","balance":"0","name":"Chidi Okafor"}]\n')
# IDs past what int64 holds.
put("big_ids.json", '[{"id":9223372036854775807,"n":1},{"id":9223372036854775808,"n":2}]\n')
put("too_big.json", '[{"id":18446744073709551616}]\n')
put("too_small.json", '[{"id":-9223372036854775809}]\n')
put("nan.json", '[{"x":NaN,"y":1.5},{"x":Infinity,"y":-Infinity},{"x":2.0,"y":null}]\n')
put("bools.json", '[{"flag":true,"maybe":true},{"flag":false,"maybe":null},{"flag":true,"maybe":false}]\n')

# ------------------------------------------------------------ dates
# Time columns pandas guesses from the name, and ones it does not.
put("dates.json", json.dumps([
    {"date": "2026-10-01", "updated_at": "2026-10-01T09:00:00+02:00", "end_time": 1790841600,
     "timestamp_ms": 1790841600000, "modified": "yesterday", "due": "2026-10-15", "datetime": "2026-10-01 09:30"},
    {"date": "2026-10-02", "updated_at": "2026-10-02T09:00:00+02:00", "end_time": 1790928000,
     "timestamp_ms": 1790928000500, "modified": "last week", "due": "2026-10-16", "datetime": "2026-10-02 18:05"},
]) + "\n")
put("tz_mixed.json", json.dumps([
    {"seen_at": "2026-10-01T09:00:00+02:00"},
    {"seen_at": "2026-10-01T09:00:00-04:00"},
]) + "\n")
# Dates as people write them: US month-first, then a European
# day-first one further down; month names; a date and a full time in
# one column; UTC written two ways; naive and aware times together;
# nanoseconds; a missing date.
put("us_dates.json", '[{"order_date":"10/03/2026","n":1},{"order_date":"10/14/2026","n":2},{"order_date":"11/02/2026","n":3}]\n')
put("eu_dates.json", '[{"date":"10/03/2026","n":1},{"date":"13/03/2026","n":2},{"date":"25/12/2026","n":3}]\n')
put("named_dates.json", '[{"date":"Oct 3, 2026"},{"date":"Oct 14, 2026"},{"date":"Nov 2, 2026"}]\n')
put("long_dates.json", '[{"date":"Saturday, 3 October 2026"},{"date":"Wednesday, 14 October 2026"}]\n')
put("iso_mixed.json", '[{"date":"2026-10-01"},{"date":"2026-10-02T09:30:00"},{"date":"2026-10-03 18:45:10.25"}]\n')
put("utc_two_ways.json", '[{"sent_at":"2026-10-01T09:00:00Z"},{"sent_at":"2026-10-01T11:00:00+02:00"}]\n')
put("utc_offsets.json", '[{"sent_at":"2026-10-01T09:00:00+00:00"},{"sent_at":"2026-10-01T11:00:00+00:00"}]\n')
put("naive_aware.json", '[{"sent_at":"2026-10-01T09:00:00"},{"sent_at":"2026-10-01T09:00:00Z"}]\n')
put("nanos.json", '[{"captured_at":"2026-10-01T09:00:00.123456789Z"},{"captured_at":"2026-10-01T09:00:01Z"}]\n')
put("millis.json", '[{"captured_at":"2026-10-01T09:00:00.5"},{"captured_at":"2026-10-01T09:00:01"}]\n')
put("null_dates.json", '[{"date":"2026-10-01","v":1},{"date":null,"v":2},{"date":"2026-10-03","v":3}]\n')
put("compact_dates.json", '[{"date":"20261001"},{"date":"20261002"}]\n')
put("year_only.json", '[{"date":"2026"},{"date":"2027"}]\n')
put("words.json", '[{"date":"soon"},{"date":"2026-10-01"}]\n')
put("small_epoch.json", '[{"created_at":1000,"n":1},{"created_at":2000,"n":2}]\n')

# ------------------------------------------------------------ text
put("bom.json", b'\xef\xbb\xbf[{"id":1,"name":"Ana"}]\n')
put("latin1.json", '[{"city":"M\xfcnchen","temp":"12\xb0C"}]\n', "latin-1")
put("escapes.json", '[{"s":"tab\\there","t":"\\u00e9t\\u00e9","u":"\\ud83d\\ude00","v":"a\\/b"}]\n')
put("bad_escape.json", '[{"s":"C:\\Users\\ana"}]\n')
put("python_dict.json", "{'a': 1, 'b': 2}\n")
put("trailing.json", '[{"a":1}] [{"a":2}]\n')
put("trailing_comma.json", '[{"a":1},{"a":2},]\n')
put("scalars.json", '{"a":1,"b":2}\n')
put("empty.json", "")
put("empty_list.json", "[]\n")
put("empty_obj.json", "{}\n")

JOBS = [
    # records from an API
    "read issues.json",
    "read issues.json orient=records head=2",
    "read issues.json convert_dates=False head=2",
    "read issues.json keep_default_dates=False head=2",
    "read issues.json convert_dates=closed_at keep_default_dates=False head=2",
    "read issues.json dtype=False head=2",
    "read issues.json dtype=number:float64,comments:float64 head=2",
    "read issues.json dtype=id:str head=2",
    "read issues.json dtype_backend=numpy_nullable head=2",
    "read issues.json orient=split",
    "read issues.json orient=index",
    "read issues.json orient=columns head=2",
    "read issues.json orient=values head=2",
    "read issues.json orient=table",
    "read issues.json orient=sideways head=2",
    "read issues.json typ=series head=2",
    "read issues.json typ=table",
    # NDJSON
    "read requests.ndjson lines=True",
    "read requests.ndjson lines=True convert_dates=False",
    "read requests.ndjson lines=True date_unit=ms",
    "read requests.ndjson lines=True date_unit=s",
    "read requests.ndjson lines=True date_unit=MS",
    "read requests.ndjson lines=True date_unit=d",
    "read requests.ndjson lines=True nrows=3",
    "read requests.ndjson lines=True nrows=5",
    "read requests.ndjson lines=True nrows=0",
    "read requests.ndjson lines=True chunksize=3",
    "read requests.ndjson lines=True chunksize=3 nrows=4",
    "read requests.ndjson lines=True chunksize=0",
    "read requests.ndjson chunksize=3",
    "read requests.ndjson nrows=3",
    "read requests.ndjson",
    "read requests.ndjson lines=True dtype_backend=numpy_nullable",
    "read requests.ndjson lines=True dtype=status:str",
    "read cutoff.ndjson lines=True",
    "read cutoff.ndjson lines=True nrows=3",
    "read cutoff.ndjson lines=True chunksize=2",
    "read crlf.ndjson lines=True",
    "read sensors.ndjson lines=True",
    "read sensors.ndjson lines=True convert_dates=time",
    "read sensors.ndjson lines=True convert_dates=time date_unit=s",
    "read sensors.ndjson lines=True dtype=rh:float64",
    "read sensors.ndjson lines=True dtype_backend=numpy_nullable",
    "read sensors.ndjson lines=True chunksize=4",
    # every orient
    "read split.json orient=split",
    "read split.json orient=split dtype_backend=numpy_nullable",
    "read split.json",
    "read split_named.json orient=split",
    "read split_named.json orient=split convert_axes=False",
    "read split_bad.json orient=split",
    "read split_dup.json orient=split",
    "read index.json orient=index",
    "read index.json",
    "read index.json orient=index dtype=pop_k:float64",
    "read columns.json",
    "read columns.json convert_axes=False",
    "read columns.json orient=index",
    "read columns.json dtype=units:Int64",
    "read columns_dates.json",
    "read columns_dates.json convert_axes=False",
    "read values.json orient=values",
    "read values.json",
    "read ragged.json orient=values",
    "read records_mixed.json",
    "read records_mixed.json dtype_backend=numpy_nullable",
    "read table.json orient=table",
    "read table.json orient=table dtype=total:float64",
    "read table.json orient=table convert_axes=True",
    "read table.json",
    "read table_noindex.json orient=table",
    # Series
    "read daily.json typ=series",
    "read daily.json typ=series convert_axes=False",
    "read daily.json typ=series orient=index",
    "read daily.json",
    "read series_split.json typ=series orient=split",
    "read series_split.json typ=series",
    "read series_list.json typ=series",
    "read series_list.json typ=series orient=values",
    "read series_list.json typ=series dtype_backend=numpy_nullable",
    "read split.json typ=series orient=split",
    # numbers
    "read prices.json",
    "read prices.json precise_float=True",
    "read customers.json",
    "read customers.json dtype=False",
    "read customers.json dtype=cust_id:str,zip:str",
    "read customers.json dtype=str",
    "read customers.json dtype_backend=numpy_nullable",
    "read big_ids.json",
    "read too_big.json",
    "read too_small.json",
    "read nan.json",
    "read bools.json",
    "read bools.json dtype_backend=numpy_nullable",
    # dates
    "read dates.json",
    "read dates.json convert_dates=False",
    "read dates.json convert_dates=due",
    "read dates.json convert_dates=due keep_default_dates=False",
    "read dates.json date_unit=ms",
    "read dates.json dtype=date:str",
    "read tz_mixed.json",
    "read us_dates.json",
    "read us_dates.json convert_dates=order_date",
    "read eu_dates.json",
    "read named_dates.json",
    "read long_dates.json",
    "read iso_mixed.json",
    "read utc_two_ways.json",
    "read utc_offsets.json",
    "read naive_aware.json",
    "read nanos.json",
    "read millis.json",
    "read null_dates.json",
    "read compact_dates.json",
    "read year_only.json",
    "read words.json",
    "read small_epoch.json",
    "read small_epoch.json date_unit=s",
    # text and broken input
    "read bom.json",
    "read bom.json encoding=utf-8-sig",
    "read latin1.json",
    "read latin1.json encoding=latin-1",
    "read latin1.json encoding_errors=replace",
    "read escapes.json",
    "read bad_escape.json",
    "read python_dict.json",
    "read trailing.json",
    "read trailing_comma.json",
    "read scalars.json",
    "read scalars.json typ=series",
    "read scalars.json orient=index",
    "read empty.json",
    "read empty.json lines=True",
    "read empty_list.json",
    "read empty_obj.json",
    "read empty_list.json typ=series",
    "read missing.json",
    "read issues.json orient=table dtype=id:str",
    "read issues.json dtype_backend=arrow",
    "read issues.json engine=simdjson",
    "read issues.json engine=pyarrow",
]
put("jobs.txt", "\n".join(JOBS) + "\n")
