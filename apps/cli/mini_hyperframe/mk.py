#!/usr/bin/env python3
"""Writes data/jobs.tsv: the HTTP/2 frames that both oracle.py and the Kara
port build and parse through hyperframe.

A job is one tab-separated line; field 0 names the kind.

build jobs construct a frame, serialize it, and re-parse the bytes:
  build data         <sid> <flags> <datahex> <pad>
  build headers      <sid> <flags> <depends_on> <weight> <excl> <datahex> <pad>
  build priority     <sid> <flags> <depends_on> <weight> <excl>
  build rststream    <sid> <flags> <error_code>
  build settings     <sid> <flags> <k:v;k:v | ->
  build pushpromise  <sid> <flags> <promised> <datahex> <pad>
  build ping         <sid> <flags> <opaquehex>
  build goaway       <sid> <flags> <last> <error_code> <addhex>
  build windowupdate <sid> <flags> <increment>
  build continuation <sid> <flags> <datahex>
  build altsvc       <sid> <flags> <originhex> <fieldhex>
flags is a comma list of flag names or '-'. A hex field of '-' is empty.

  parse <hex> <strict 0|1>   parse a 9-byte header + body from raw hex bytes
"""
import os

os.makedirs("data", exist_ok=True)

JOBS = r"""
build	data	1	-	-	0
build	data	1	END_STREAM	48656c6c6f	0
build	data	1	PADDED	48656c6c6f	4
build	data	1	END_STREAM,PADDED	deadbeef	2
build	data	3	-	00010203040506070809	0
build	headers	1	-	0	0	0	-	0
build	headers	1	END_STREAM,END_HEADERS	0	0	0	828487	0
build	headers	1	END_HEADERS,PRIORITY	20	16	0	828487	0
build	headers	1	PRIORITY	5	200	1	4188	0
build	headers	1	END_HEADERS,PADDED	0	0	0	828487	5
build	priority	1	-	0	0	0
build	priority	3	-	1	200	1
build	priority	5	-	2147483647	255	0
build	rststream	1	-	0
build	rststream	1	-	8
build	rststream	3	-	4294967295
build	settings	0	-	-
build	settings	0	-	1:4096
build	settings	0	-	1:4096;3:100;4:65535
build	settings	0	-	2:1;5:16384;6:1000000
build	settings	0	ACK	-
build	pushpromise	1	END_HEADERS	2	828487	0
build	pushpromise	1	END_HEADERS,PADDED	4	828487	3
build	pushpromise	3	-	6	-	0
build	ping	0	-	-
build	ping	0	-	0001020304050607
build	ping	0	ACK	cafe
build	goaway	0	-	0	0	-
build	goaway	0	-	5	8	6465627567
build	goaway	0	-	2147483647	4294967295	-
build	windowupdate	0	-	1
build	windowupdate	1	-	65535
build	windowupdate	0	-	2147483647
build	continuation	1	-	-
build	continuation	1	END_HEADERS	828487
build	altsvc	1	-	-	68323d223a3434332229
build	altsvc	0	-	6578616d706c652e636f6d	68323d223a34343322
build	ping	0	-	00ff6162630a0927
build	goaway	0	-	1	1	0d0a09
build	altsvc	0	-	27717569636b27	6162
parse	00000500010000000148656c6c6f	0
parse	000003010400000001828487	0
parse	0000080124000000038000000110828487	0
parse	00000502000000000100000002c8	0
parse	00000403000000000100000008	0
parse	00001204000000000000010000100000030000006400040000ffff	0
parse	000000040100000000	0
parse	00000705040000000100000002828487	0
parse	0000080600000000000001020304050607	0
parse	000008060100000000cafe000000000000	0
parse	00000d07000000000000000005000000086465627567	0
parse	0000040800000000000000ffff	0
parse	000003090400000001828487	0
parse	0000160a0000000000000b6578616d706c652e636f6d68323d223a34343322	0
parse	000006000800000001034869000000	0
parse	000008050c000000010200000004820000	0
parse	000000000000000000	0
parse	000000040000000001	0
parse	000006020000000001000000000000	0
parse	000003030000000001000000	0
parse	00000408000000000100000000	0
parse	00000405040000000100000003	0
parse	0000031f0500000001deadbe	0
parse	0000031f0500000001deadbe	1
parse	000000	0
parse	00000406000000000000000000	0
"""

with open("data/jobs.tsv", "w") as f:
    f.write(JOBS.lstrip("\n"))

print("jobs:", len(JOBS.strip().splitlines()))
