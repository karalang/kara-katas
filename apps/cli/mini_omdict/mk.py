#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_omdict: a scripted sequence of operations on
one evolving omdict (ordered multivalue dictionary), one op per line
(tab-separated):

    a  \t <k> \t <v>       add (append a value for k)
    al \t <k> \t <csv>     addlist (comma-separated values)
    s  \t <k> \t <v>       set (replace all of k's values with one)
    sl \t <k> \t <csv>     setlist (replace in place, append extras, drop surplus; empty csv deletes k)
    g  \t <k>              get           -> <v> | miss
    gl \t <k>              getlist       -> [v, ...] | []
    p  \t <k>              pop           -> <first v> | miss   (removes every value of k)
    pl \t <k>              poplist       -> [v, ...] | miss
    pv \t <k>              popvalue last -> <v> | miss
    pf \t <k>              popvalue first-> <v> | miss
    h  \t <k>              has_key       -> yes | no
    l                      size (total items, duplicates counted)
    ks                     keys()      (unique, first-insertion order)
    vs                     values()    (first value per unique key)
    it                     items()     ([(k v), ...] per unique key)
    ai                     allitems()  (every (k, v) in insertion order)
    ak                     allkeys()   av   allvalues()
    rv                     reverse()   -> the reversed allitems()

Every mutation prints the resulting allitems(), so set/setlist's in-place
replace + append + drop and reverse's order are directly visible. Keys are
lowercase ASCII; values are small ints. `oracle.py` replays the sequence
against the vendored orderedmultidict.omdict.
"""
import os

ops = []


def ai():
    ops.append(("ai",))


# Build multi-valued keys; addlist; snapshot views.
for k, v in [("a", 1), ("a", 11), ("a", 111), ("b", 2), ("c", 3), ("b", 22)]:
    ops.append(("a", k, v))
ai()
ops.append(("al", "c", "33,333"))
ops.append(("al", "d", "4"))
ai()
ops.append(("ks",))
ops.append(("vs",))
ops.append(("it",))
ops.append(("ak",))
ops.append(("av",))
ops.append(("l",))

# Point queries: present, multi, absent.
for k in ["a", "b", "c", "d", "z"]:
    ops.append(("g", k))
    ops.append(("gl", k))
    ops.append(("h", k))

# set: replace all of a key's values with one (in place at first position).
ops.append(("s", "a", 9))
ai()
# setlist: in-place replace + append extras.
ops.append(("sl", "b", "20,200,2000"))
ai()
# setlist: surplus existing dropped.
ops.append(("sl", "c", "30"))
ai()
# setlist on a new key: all values appended.
ops.append(("sl", "e", "5,55"))
ai()
# setlist empty: deletes the key.
ops.append(("sl", "d", ""))
ai()
ops.append(("ks",))
ops.append(("l",))

# reverse: item order flips, but keys() order is preserved and values() take
# the new firsts.
ops.append(("rv",))
ops.append(("ks",))
ops.append(("vs",))
ops.append(("it",))
ops.append(("gl", "b"))

# popvalue: last then first, shrinking a multi-valued key.
ops.append(("pv", "b"))
ai()
ops.append(("pf", "b"))
ai()
ops.append(("gl", "b"))

# pop / poplist: remove every value of a key.
ops.append(("pl", "a"))
ai()
ops.append(("p", "e"))
ai()
ops.append(("p", "z"))
ops.append(("pl", "z"))

# popvalue down to empty removes the key from keys().
ops.append(("pv", "c"))
ops.append(("ks",))
ops.append(("pv", "c"))
ops.append(("ks",))
ops.append(("h", "c"))
ai()
ops.append(("l",))

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for op in ops:
        fh.write("\t".join(str(x) for x in op) + "\n")
