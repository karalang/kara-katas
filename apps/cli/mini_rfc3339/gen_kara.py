# Prints the Kara jobs_text() function that holds data/jobs.tsv, for
# mini_rfc3339.kara's data section. No other data files are used.
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


print("// data/jobs.tsv, as mk.py writes it.")
print("fn jobs_text() -> String {")
print("    let mut s = String.new();")
for line in open("data/jobs.tsv", encoding="utf-8").read().splitlines():
    print("    s.push_str(%s);" % lit(line + "\n"))
print("    s")
print("}")
