#!/usr/bin/env python3
"""Writes data/jobs.tsv: size / length / timespan / number parse-and-format
jobs that both oracle.py and the Kara port run through humanfriendly.

One tab-separated line per job; field 0 names the kind:

  size_fmt   <bytes:int> <binary 0|1> <keep_width 0|1>     format_size
  size_parse <str> <binary 0|1>                            parse_size -> bytes
  len_fmt    <metres:float> <keep_width 0|1>               format_length
  len_parse  <str>                                         parse_length -> metres
  time_fmt   <seconds:int> <detailed 0|1> <max_units:int>  format_timespan
  time_parse <str>                                         parse_timespan -> seconds
  num        <number:int> <decimals:int>                   format_number
  round      <x:float> <keep_width 0|1>                     round_number
  bool       <str>                                         coerce_boolean

A parse job prints the result (bytes as an int; metres/seconds through
num_str) or err=<message>. A format/round job prints the string. A bool job
prints True/False or err=<message>.
"""
import os

os.makedirs("data", exist_ok=True)

JOBS = r"""
size_fmt	0	0	0
size_fmt	1	0	0
size_fmt	5	0	0
size_fmt	999	0	0
size_fmt	1000	0	0
size_fmt	1000	0	1
size_fmt	1024	1	0
size_fmt	1500000000	0	0
size_fmt	4000000000	0	0
size_fmt	1536	1	0
size_fmt	1234567	0	0
size_fmt	2500000	0	0
size_fmt	1073741824	1	0
size_fmt	5000000000000	0	0
size_fmt	2000000000000000	0	0
size_parse	42	0
size_parse	13b	0
size_parse	5 bytes	0
size_parse	1 KB	0
size_parse	1 kilobyte	0
size_parse	1 KiB	0
size_parse	1 KB	1
size_parse	1.5 GB	0
size_parse	1.5 GB	1
size_parse	2 TB	0
size_parse	1 MiB	0
size_parse	3 mebibyte	0
size_parse	1 EB	0
size_parse	nonsense	0
size_parse	1 flooble	0
len_fmt	0	0
len_fmt	1	0
len_fmt	5	0
len_fmt	1000	0
len_fmt	0.004	0
len_fmt	0.153	0
len_fmt	2500	0
len_fmt	1	1
len_parse	42	0
len_parse	1 km	0
len_parse	5mm	0
len_parse	15.3cm	0
len_parse	2 m	0
len_parse	bad	0
time_fmt	0	0	3
time_fmt	1	0	3
time_fmt	5	0	3
time_fmt	60	0	3
time_fmt	3600	0	3
time_fmt	86400	0	3
time_fmt	90	0	3
time_fmt	3661	0	3
time_fmt	31449600	0	3
time_fmt	31622400	0	3
time_fmt	31622640	0	3
time_fmt	31622640	0	2
time_fmt	604800	0	3
time_parse	42	0
time_parse	42s	0
time_parse	1m	0
time_parse	1h	0
time_parse	1d	0
time_parse	90m	0
time_parse	1.5h	0
time_parse	2w	0
time_parse	3 hours	0
time_parse	bogus	0
num	6000000	2
num	1234	2
num	100	2
num	-6000000	2
num	999	2
num	1000000000	0
round	1	0
round	3.14159	0
round	5.001	0
round	1.5	0
round	1	1
round	2.5	0
bool	1
bool	yes
bool	TRUE
bool	on
bool	0
bool	no
bool	false
bool	off
bool	maybe
"""

with open("data/jobs.tsv", "w") as f:
    f.write(JOBS.strip("\n") + "\n")

print("jobs:", len(JOBS.strip().splitlines()))
