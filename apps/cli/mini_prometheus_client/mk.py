"""Writes data/script.txt for mini_prometheus_client: the metrics of a small
web service, defined, updated (some updates from four worker tasks at
once), exposed in both text formats and written to a file, with a mistake
for each rule the library checks.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)

SCRIPT = r"""# The metrics of a small web service. Names are full names: a counter's
# `_total` is dropped, a unit is appended, ns_ and sub_ are prepended.

counter http_requests_total labels=method,path,code : HTTP requests\sseen, by method and path.
counter http_requests labels=method : a second counter named the same
gauge http_requests_total : a gauge may take the name the counter dropped
histogram request_latency unit=seconds labels=method buckets=0.005,0.01,0.025,0.05,0.1,0.25,0.5,1,2.5 : Time to first byte.
summary payload labels=route unit=bytes : Request body sizes.
gauge in_flight : Requests being served right now.
gauge queue_depth ns=jobs sub=email : Messages waiting
info build : Build facts.
enum worker_state labels=worker states=starting,idle,busy,draining : What each worker is doing.
counter job:errors labels=queue : Failed jobs by queue (a recording-rule style name).

# Updates.
inc http_requests@GET,/,200
inc http_requests@GET,/,200 2
inc http_requests@POST,/upload,201 1.5
inc http_requests@GET,/missing,404
inc http_requests@GET,/
inc http_requests@GET,/,200,extra
inc http_requests
inc http_requests@GET,/,200 -1
inc http_requests@GET,/,200 ten
inc http_requests@GET,/,200 1 2
inc nosuch@GET 1
set http_requests@GET,/,200 3
set in_flight 3
inc in_flight
dec in_flight 2.5
set http_requests_total 7
set jobs_email_queue_depth 12
inc jobs_email_queue_depth 0.1
inc jobs_email_queue_depth 0.2
observe request_latency_seconds@GET 0.003
observe request_latency_seconds@GET 0.01
observe request_latency_seconds@GET 0.0101
observe request_latency_seconds@GET 0.3
observe request_latency_seconds@GET 7
observe request_latency_seconds@POST 0.75
observe request_latency_seconds 0.2
observe payload_bytes@/upload 2048
observe payload_bytes@/upload 512
observe payload_bytes@/login 96
set build version=1.4.2 commit=0a1b2c3 branch=main
set build note=line\none\stwo quote="yes" path=C:\\tmp
state worker_state@w1 busy
state worker_state@w2 idle
state worker_state@w3 sleeping
state worker_state busy
inc job:errors@mail
inc job:errors@sms 4

# Label values with escapes: a comma, a space, a newline, a backslash, a quote.
inc http_requests@GET,/search?q=a\,b,200
inc http_requests@GET,/two\swords,200
inc http_requests@PUT,line\nbreak,500
inc http_requests@PUT,back\\slash,500
inc http_requests@PUT,"quoted",500
inc http_requests@GET,bad\escape,500

expose
expose openmetrics

# Many updates from four worker tasks at once.
parallel 1000 inc http_requests@GET,/,200
parallel 400 observe request_latency_seconds@GET 0.04
parallel 250 observe payload_bytes@/upload 1024
parallel 64 dec in_flight 0.125
parallel 10 inc http_requests@GET,/,200 -2
parallel 3 state worker_state@w4 busy
parallel 0 inc in_flight
parallel 5 expose

# Names, labels and options the library refuses.
counter 9lives : starts with a digit
counter bad-name : has a dash
gauge ok_name labels=le : le is fine outside a histogram
histogram hist_le labels=le : le is reserved here
summary sum_q labels=quantile : and quantile here
gauge reserved labels=__name : two underscores are reserved
gauge spaced labels=a,b-c : a dash
gauge empty_label labels= : an empty label name
histogram unsorted buckets=1,0.5,2 : out of order
histogram one_bucket buckets=+Inf : only the implied bucket
histogram same_bucket buckets=1,1,2 : equal bounds are sorted
histogram neg_buckets buckets=-1,0,1 : no sum when a bound is negative
histogram bad_bucket buckets=1,two : not a number
histogram big buckets=1000000,1234567,10000000,100000000000,1e+22 : Go-style exponents in le
info build_unit unit=bytes : an info cannot have a unit
enum flag states= : one state, the empty text
enum flag2 : no states
enum job:phase states=queued,running : a colon in the state label
enum mode labels=mode states=a,b : the name is a label too
enum color states=red,green
gauge gauge_opts buckets=1,2 : only a histogram has buckets
gauge twice unit=a unit=b
gauge noeq unit
counter
counter : help but no name
hist undefined_kind
counter c_total : the total is dropped
counter c : and c is taken
gauge c_total : so is c_total
counter cache:hits_total : colon in a counter name

# Odd values.
set ok_name@x NaN
set ok_name@y +Inf
set ok_name@z -Inf
set ok_name@w -0.0
set ok_name@v 1e-7
set ok_name@u 123456789012
inc c NaN
inc c -0.0
observe neg_buckets -2
observe neg_buckets NaN
observe neg_buckets 0.5
observe same_bucket 1
observe big 1234567
observe big 2e20
set reserved 1
inc color
reset c
state color green
state job:phase running
info odd_keys : keys the library does not check
set odd_keys a-b=1 9x=2 __k=3 le=4 a-b=5

# Info labels, overlapping labels, reset, remove, clear, unregister.
info deploy labels=region : Where it runs.
set deploy@eu version=2 region=eu
set deploy@eu version=2 tier=gold
set deploy tier=gold
set deploy@us tier=silver bad
reset http_requests
reset http_requests@GET,/,200
reset in_flight
remove http_requests@GET,/missing,404
remove http_requests@GET
remove http_requests
remove in_flight
remove in_flight@x
clear job:errors
clear in_flight
unregister payload_bytes
unregister payload_bytes
summary payload labels=route unit=bytes : Back, empty.
target service=api region=eu-west\s1
gauge target_info : clashes with the target series
target
gauge target_info : free again
target service=api
unregister target_info
target service=api
expose
expose openmetrics
expose json
write service.prom
write ../escape.prom
write
frobnicate now
"""

with open(os.path.join("data", "script.txt"), "w", encoding="utf-8", newline="") as fh:
    fh.write(SCRIPT)
