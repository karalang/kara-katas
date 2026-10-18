#!/usr/bin/env python3
"""Writes data/ for mini_fractions: a recipe, a shared bill, the jobs."""
import os

os.makedirs("data", exist_ok=True)

# quantity	unit	ingredient (quantities as cooks write them)
RECIPE = """\
1 1/2	cup	flour
3 1/2	tsp	baking powder
1/4	tsp	salt
1	tbsp	sugar
1 1/4	cup	milk
1	-	egg
3	tbsp	butter, melted
"""

# A dinner bill: item, price in cents, who shared it (comma-separated).
BILL = """\
pizza	2399	ana,ben,cy
salad	1150	ana,dee
wine	3400	ana,ben,cy,dee
soda	325	cy
dessert	995	ben,cy,dee
"""

JOBS = [
    "new\t3/4", "new\t-35/4", "new\t10/-8", "new\t314", "new\t3.1415",
    "new\t-47e-2", "new\t1.5E3", "new\t  7/14  ", "new\t1_000/3",
    "new\t.5", "new\t2.", "new\t+0.125", "new\t1/0", "new\tabc",
    "new\t1/", "new\t1 / 2", "new\t/2", "new\t1e", "new\t-0",
    "pair\t10\t-8", "pair\t0\t5", "pair\t-6\t-4", "pair\t3\t0",
    "op\t1/2\t+\t1/3", "op\t1/2\t-\t5/6", "op\t3/4\t*\t2/9", "op\t3/4\t/\t9/8",
    "op\t7/2\t//\t2/3", "op\t-7/2\t//\t2/3", "op\t7/2\t%\t2/3", "op\t-7/2\t%\t2/3",
    "op\t7/2\tdivmod\t-2/3", "op\t2/3\t**\t3", "op\t2/3\t**\t-2", "op\t-2/3\t**\t-3",
    "op\t0\t**\t-1", "op\t5\t/\t0", "op\t1/3\t<\t1/2", "op\t2/4\t==\t1/2",
    "op\t-1/3\t>=\t-1/2", "op\t5/7\t!=\t5/7",
    "limit\t3.141592653589793\t10", "limit\t3.141592653589793\t100",
    "limit\t3.141592653589793\t1000000", "limit\t4321/8765\t10000",
    "limit\t1/2\t1", "limit\t3/2\t1", "limit\t-1.414213562\t50", "limit\t1/3\t0",
    "round\t7/2\t-", "round\t5/2\t-", "round\t-5/2\t-", "round\t2/3\t2",
    "round\t1234567/1000\t-2", "round\t1/8\t2", "round\t-1/8\t2",
    "ints\t7/2", "ints\t-7/2", "ints\t4", "ints\t-1/3",
    "format\t3/4\t", "format\t3/4\t>10", "format\t-3/4\t*<10", "format\t3/4\t^9",
    "format\t-3/4\t=+10", "format\t4\t#", "format\t1234567/10\t,", "format\t-1234567\t_",
    "format\t3/4\t+", "format\t3/4\t.2f", "format\t2/3\t.4f", "format\t-1/8\t.2f",
    "format\t5/2\t.0f", "format\t1/2\tq",
    "recipe\t@recipe.tsv\t2", "recipe\t@recipe.tsv\t1/2", "recipe\t@recipe.tsv\t2/3",
    "bill\t@bill.tsv\t18",
    "convert\t12\tin\tmm", "convert\t100\tmm\tin", "convert\t1/3\tcup\tml", "convert\t5\tmi\tkm",
]

with open("data/recipe.tsv", "w") as f:
    f.write(RECIPE)
with open("data/bill.tsv", "w") as f:
    f.write(BILL)
with open("data/jobs.tsv", "w") as f:
    f.write("\n".join(JOBS) + "\n")
