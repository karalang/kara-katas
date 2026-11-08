"""Writes data/script.txt for mini_multidict: an HTTP request's headers
and query string, a response being assembled and the form it posted,
kept in multidicts, with a mistake for each rule the library checks.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)

SCRIPT = r"""# An HTTP exchange in multidicts. `\s` in a word is a space.

# The query string of GET /search?tag=red&tag=blue&page=2&tag=red&q=it's
new query md tag=red tag=blue page=2 tag=red q=it's
show query
len query
keys query
values query
items query
getone query tag
getall query tag
item query page
get query sort
get query sort relevance
getone query sort
getone query sort relevance
getall query sort
getall query sort []
item query sort
has query tag
has query Tag
hasitem query tag blue
hasitem query tag green
hasvalue query 2
hasvalue query two
todict query
reversed query keys
reversed query values
reversed query items

# Request headers are case-insensitive; each key keeps its spelling.
new req ci Host=example.org Accept=text/html Accept=application/json X-Trace-Id=abc123 accept=*/*
show req
keys req
getall req ACCEPT
getone req x-trace-id
has req HOST
has req host
hasitem req ACCEPT text/html
todict req
reversed req keys
del req accept
show req
del req accept
popone req x-trace-id
popone req x-trace-id gone
popall req nothing
popall req nothing []

# A response, built up and rewritten.
new resp ci Content-Type=text/plain Set-Cookie=a=1
add resp Set-Cookie b=2
add resp set-cookie c=3
add resp Vary Accept
show resp
set resp CONTENT-TYPE text/html;\scharset=utf-8
show resp
set resp Set-Cookie session=xyz
show resp
set resp Cache-Control no-store
setdefault resp Vary Cookie
setdefault resp ETag "v1"
show resp
update resp vary=Accept-Encoding vary=Origin vary=Cookie etag="v2"
show resp
merge resp ETag="v3" Server=kara Server=kara/0.8
show resp
extend resp Link=</a> Link=</b>
show resp
popitem resp
popall resp link
len resp
keys resp

# Updates replace in place: the first match takes the new key and value,
# later items take later matches, the rest of the matches go.
new form md color=red size=m color=green note=hi color=blue
update form color=black
show form
new form2 md color=red size=m color=green note=hi color=blue
update form2 color=black color=white
show form2
new form3 md color=red size=m color=green
update form3 color=black color=white color=gold size=l size=xl
show form3
new form4 md a=1
update form4 b=2 b=3 a=4
show form4
merge form4 a=5 c=6 c=7 b=8
show form4
update form4 from form4
show form4
extend form4 from form4
show form4

# Copies, proxies and conversions between the two kinds.
copy req req2
add req2 Accept text/plain
show req
show req2
proxy view ci req
show view
getall view accept
add req Accept image/png
show view
add view Accept x/y
set view Host other
del view Host
popone view Host
clear view
copy view snapshot
show snapshot
proxy view2 ci view
show view2
proxy loose md req
show loose
copy loose plain
show plain
getall plain accept
getall plain Accept
proxy wrong ci query
proxy wrong2 ci loose
new lowered md from req
getall lowered Accept
new raised ci from query
getall raised TAG
new mixed ci Etag=a ETAG=b
new back md from mixed
show back
keys back
new from_view ci from view
show from_view

# Equality: two multidicts compare entry by entry, by identity and value.
new q1 md a=1 b=2
new q2 md a=1 b=2
new q3 md b=2 a=1
new q4 ci A=1 B=2
eq q1 q2
eq q1 q3
eq q1 q4
eq q4 q1
eq view req
eq req view
eq loose plain
eqdict q1 a=1 b=2
eqdict q1 b=2 a=1
eqdict q1 a=1
eqdict q4 a=1 b=2
eqdict q4 A=1 B=2
new dup md a=1 a=1
eqdict dup a=1
eqdict dup a=1 a=1

# Key and item views as sets.
new tags ci Tag=red tag=blue Size=m
keyset tags and TAG size color
keyset tags rand TAG size color
keyset tags or TAG size color
keyset tags ror TAG size color
keyset tags sub TAG color
keyset tags rsub TAG color
keyset tags xor TAG color
keyset tags disjoint color shape
keyset tags disjoint color SIZE
keyset tags and
keyset tags sub
itemset tags and TAG=blue tag=red size=l
itemset tags rand TAG=blue tag=red size=l
itemset tags or TAG=blue size=l
itemset tags ror TAG=blue size=l
itemset tags sub tag=RED tag=red
itemset tags rsub TAG=blue size=l
itemset tags xor TAG=blue size=l
itemset tags disjoint size=l
itemset tags disjoint SIZE=m
keyset query sub tag
itemset query and tag=red

# Emptying.
popitem form
clear form
show form
popitem form
keys form
todict form

# Mistakes.
new query md
new
new x dict a=1
new x md a
new x md from
new x md from nosuch
new x md from query extra
proxy
proxy x md nosuch
copy query
copy nosuch y
copy query req
show
show nosuch
show query extra
len query extra
keys query extra
reversed query
reversed query sideways
has query
hasitem query tag
item query
get query
get query a b c
set query a
del query
add query a
setdefault query a
popone query
popitem query extra
clear query extra
eq query
eq query nosuch
keyset query
keyset query nand a
itemset query and a
extend query a
update query from
merge query from nosuch
frobnicate query
"""

with open(os.path.join("data", "script.txt"), "w", encoding="utf-8", newline="") as fh:
    fh.write(SCRIPT)
