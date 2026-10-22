#!/usr/bin/env python3
"""Writes data/jobs.tsv: the job list that both oracle.py and the Kara port
run through more-itertools.

A job is one line of tab-separated fields; field 0 names the function.
Encodings used by the fields:
  - an integer list  "1,2,3"   ("-" or "" is the empty list)
  - several lists    "1,2;3,4" (";"-separated)
  - a plain integer  "3"
  - a bool           "1" / "0"
  - a character run   a bare word; its characters are iterated
  - a nested list    "1,[2,[3,4]],5" for collapse
Only ASCII letters and digits appear in character runs, so every char's
repr is 'x' with no escaping.
"""
import os

os.makedirs("data", exist_ok=True)

JOBS = r"""
chunked	1,2,3,4,5,6	3	0
chunked	1,2,3,4,5	3	0
chunked	1,2,3,4,5,6	3	1
chunked	-	3	0
chunked_even	1,2,3,4,5,6,7	3
chunked_even	1,2,3,4,5,6	3
chunked_even	1,2,3	5
chunked_even	-	3
distribute	3	1,2,3,4,5,6,7
distribute	2	1,2,3,4,5,6
distribute	5	1,2,3
divide	3	1,2,3,4,5,6,7
divide	2	1,2,3,4,5,6
divide	5	1,2,3
sliced	1,2,3,4,5,6,7,8	3
split_at	1,2,3,0,4,5,0,6	-1	0
split_at	1,2,3,0,4,5,0,6	1	0
split_at	1,2,3,0,4,5,0,6	-1	1
split_before	1,2,3,1,2,1	1
split_after	1,2,3,1,2,1	1
split_when	1,2,3,3,2,5,2,4,2	gt
split_when	1,2,3,3,2,5,2,4,2	gt2
split_into	1,2,3,4,5,6	1,2,3
split_into	1,2,3,4	1,2,3,4
split_into	1,2,3,4,5,6	2,3
grouper	1,2,3,4,5,6	3	fill
grouper	1,2,3,4,5	3	fill
grouper	1,2,3,4,5	3	ignore
grouper	1,2,3,4,5,6	3	strict
partition	1,2,3,4,5,6,7,8
bucket	10,21,32,13,24,5,16
windowed	1,2,3,4,5	3	1
windowed	1,2,3,4,5	3	2
windowed	1,2,3,4,5	2	3
windowed	1,2,3	5	1
substrings	abc
substrings_indexes	abc
stagger	0,1,2,3	m101	0
stagger	0,1,2,3,4,5,6,7	024	0
stagger	0,1,2,3	m101	1
windowed_complete	0,1,2,3,4,5,6	3
triplewise	1,2,3,4,5
sliding_window	1,2,3,4,5	3
subslices	abc
count_cycle	1,2,3	2
intersperse	0	1,2,3,4,5	1
intersperse	0	1,2,3,4,5	2
padded	1,2,3	0	6	0
padded	1,2,3	0	4	1
repeat_each	1,2,3	2
repeat_last	1,2,3	6
ncycles	1,2,3	3
mark_ends	1,2,3
mark_ends	7
padnone	1,2,3	5
collapse	1,[2,[3,4],5],6
collapse	[1,[2,[3,[4,[5]]]]]
flatten	1,2;3,4;;5,6,7
interleave	1,2,3;4,5,6;7,8,9
interleave	1,2;3,4,5,6;7
interleave_longest	1,2;3,4,5,6;7
interleave_evenly	1,2,3,4,5;6,7
interleave_evenly	1,2,3;4,5;6,7,8
roundrobin	1,2,3;4;5,6
zip_offset	1,2,3;4,5,6	0,1	0	0
zip_offset	1,2,3;4,5,6	0,1	1	0
dotproduct	1,2,3	4,5,6
convolve	1,2,3	2,1
sort_together	3,1,2;7,8,9	0
sort_together	3,1,2;0,1,0	1
transpose	1,2,3;4,5,6
unzip	1,4;2,5;3,6
reshape	0,1;2,3;4,5	3
ilen	1,2,3,4,5
take	3	1,2,3,4,5
take	9	1,2,3
first	1,2,3	-1
first	-	-1
last	1,2,3	-1
last	-	-1
nth	1,2,3,4	2	-1
nth	1,2,3,4	9	-1
nth_or_last	1,2,3	1
nth_or_last	1,2,3	9
only	5	-1
only	-	-1
only	5,6	-1
one	5
one	-
one	5,6
all_equal	2,2,2
all_equal	2,2,3
all_equal	-
all_unique	1,2,3
all_unique	1,2,2
first_true	2,4,6,7,8	odd
first_true	2,4,6	odd
quantify	1,2,3,4,5,6	even
is_sorted	1,2,2,3	0
is_sorted	1,2,2,3	1
is_sorted	3,2,1	0
minmax	3,1,5,2,4
iequals	1,2,3;1,2,3
iequals	1,2,3;1,3,2
iequals	1,2,3;1,2
map_reduce	10,11,12,13,14,15
exactly_n	1,0,1,0,1	2	nz
exactly_n	1,0,1,0,1	3	nz
run_length_encode	abbcccdddd
run_length_decode	a1b2c3
consecutive_groups	1,10,11,12,20,30,31,32,33,40
locate	0,1,1,0,1	nz
rlocate	0,1,1,0,1	nz
replace	1,1,0,1,1,0,1,1	0	8,9	-1
replace	1,1,0,1,1,0,1,1,0	0	7	2
longest_common_prefix	flower;flow;flight
longest_common_prefix	dog;cat
argminmax	3,1,4,1,5,9,2,6
running_max	1,3,2,5,4,6
running_min	5,3,4,1,2,0
unique_everseen	1,2,2,3,3,3,1
unique_justseen	1,2,2,3,3,3,1
unique_in_window	0,1,0,2,3,0	3
duplicates_everseen	3,3,1,2,2,3
duplicates_justseen	3,3,1,2,2,3
classify_unique	otto
powerset	1,2,3
partitions	abc
set_partitions	abc	-1
set_partitions	abcd	2
circular_shifts	0,1,2,3	1
circular_shifts	0,1,2,3	2
distinct_permutations	1,0,1	-1
distinct_permutations	0,1,2	2
distinct_combinations	0,0,1	2
nth_product	8	0,1;0,1;0,1;0,1
nth_combination	0,1,2,3,4	3	5
nth_permutation	0,1,2,3,4	2	5
gray_product	1,2;3,4
partial_product	1,2;3;4,5,6
sum_of_squares	1,2,3,4
polynomial_eval	1,2,3	2
polynomial_from_roots	1,2,3
polynomial_derivative	3,2,1
matmul	1,2;3,4	5,6;7,8
factor	360
is_prime	97
is_prime	91
sieve	30
totient	36
multinomial	2,1,1
"""

with open("data/jobs.tsv", "w") as f:
    f.write(JOBS.lstrip("\n"))

print("jobs:", len(JOBS.strip().splitlines()))
