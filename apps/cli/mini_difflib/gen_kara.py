# Prints the Kara function that holds data/ (as mk.py writes it), for
# mini_difflib.kara's data section.
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
        elif ch == "\t":
            out.append("\\t")
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'

print("// Each input file's name under data/, and its text.")
print("fn data_files() -> Vec[(String, String)] {")
print("    let mut v: Vec[(String, String)] = Vec.new();")
for n in sorted(os.listdir("data")):
    text = open(os.path.join("data", n), newline="").read()
    print("    let mut s = String.new();")
    for line in text.splitlines(keepends=True):
        print("    s.push_str(%s);" % lit(line))
    print("    v.push((%s.to_string(), s));" % lit(n))
print("    v")
print("}")
