#!/usr/bin/env python3
"""Writes data/: a page of text, an access log, a cache trace and
data/jobs.tsv.

A job is one line of tab-separated fields; the operations in its last
field are separated by "|". A field that starts with "@" names a file in
data/.
"""
import os

os.makedirs("data", exist_ok=True)

TEXT = """\
the quick brown fox jumps over the lazy dog the dog sleeps
a fox is quick and a dog is lazy but the fox is not a dog
over and over the fox jumps and the dog sleeps
"""
LOG = """\
10.0.0.1 GET /index.html 200
10.0.0.2 GET /app.js 200
10.0.0.1 GET /api/items 200
10.0.0.3 POST /api/login 401
10.0.0.2 GET /missing 404
10.0.0.1 GET /api/items 500
10.0.0.4 GET /index.html 200
10.0.0.3 POST /api/login 200
10.0.0.2 GET /old 301
10.0.0.5 GET /missing 404
10.0.0.1 GET /api/report 500
10.0.0.4 GET /app.js 304
"""
TRACE = "a b c a d b e a f a c g b a h c a b".replace(" ", "\n") + "\n"
for name, text in {"page.txt": TEXT, "access.log": LOG, "trace.txt": TRACE}.items():
    with open(os.path.join("data", name), "w") as f:
        f.write(text)

JOBS = r"""
counter	new a b c a b a|repr|most 2|most|most 0|total|get a|get z|elements|update a z z|repr|subtract a a a a|repr|most 2|del z|repr|pos|neg
counter	new @page.txt|most 5|total|get fox|add fox fox cat|sub the the the the the the the the|and fox dog cat|or fox fox fox fox fox|le the|ge the|eq the|ne the
counter	new|repr|most 3|total|pos|update x|subtract x y|repr|pos|neg|elements|le|eq
counter	new b a b a|repr|most|update a|most|subtract b|most
deque	-	append 1|append 2|appendleft 0|extend 3 4|extendleft 9 8|len|get 0|get -1|get 3|set 1 7|rotate 2|rotate -3|count 4|index 4|index 99|remove 4|remove 99|reverse|pop|popleft|insert 2 5|clear|pop|popleft|get 0
deque	3	append 1|append 2|append 3|append 4|appendleft 0|extend 5 6 7 8|extendleft 1 2|insert 1 9|pop|insert 1 9|rotate 1|maxlen|len|clear|maxlen
deque	0	append 1|appendleft 2|extend 3 4|len|insert 0 1|pop
deque	1	append 1|append 2|rotate 5|appendleft 3|pop|pop
deque	-	extend 1 2 3 4 5|rotate 7|rotate -12|rotate 0|reverse|index 5|count 9|set 9 1|get -6|get -5
odict	set a 1|set b 2|set c 3|repr|set a 10|repr|move a last|repr|move c first|repr|get b|get z|del b|repr|del b|keys|popitem last|popitem first|repr|popitem last|popitem first|repr|set z 26|move z first|move q last|repr
lru	3	@trace.txt
lru	1	@trace.txt
lru	8	@trace.txt
lru	0	@trace.txt
chain	verbose=1,port=8080	port=9000,host=example.org	host=localhost,port=80,debug=0	get port|get host|get debug|get user|in verbose|in user|len|keys|repr|set debug 1|keys|repr|del host|del port|keys|repr|pop verbose|pop verbose|child|set port 1|repr|parents|get port|len
chain	-	-	get x|len|keys|set x 1|repr|del x|del x|repr
group	@access.log
tail	3	@access.log
tail	1	@access.log
tail	20	@access.log
tail	0	@access.log
"""
with open("data/jobs.tsv", "w") as f:
    f.write(JOBS.lstrip("\n"))
