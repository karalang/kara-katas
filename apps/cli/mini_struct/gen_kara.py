# Prints the Kara functions that hold data/ (as mk.py writes it), for
# mini_struct.kara's data section: the binary files as hex, jobs.txt as text.
import os

def lit(s):
    out = []
    for ch in s:
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\n":
            out.append("\\n")
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'

names = sorted(n for n in os.listdir("data") if n != "jobs.txt")
print("// The input files under data/, each as hex.")
print("fn data_files() -> Vec[(String, String)] {")
print("    let mut v: Vec[(String, String)] = Vec.new();")
for n in names:
    h = open(os.path.join("data", n), "rb").read().hex()
    print("    v.push((%s.to_string(), %s.to_string()));" % (lit(n), lit(h)))
print("    v")
print("}")
print()
print("fn jobs_text() -> String {")
print("    let mut s = String.new();")
for line in open("data/jobs.txt").read().splitlines():
    print("    s.push_str(%s);" % lit(line + "\n"))
print("    s")
print("}")
