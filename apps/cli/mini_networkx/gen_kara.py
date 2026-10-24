# Prints the Kara function that holds data/jobs.txt (as mk.py writes it),
# for the end of mini_networkx.kara. Lines are grouped into literals of
# about 2 KB.
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


print()
print("// ------------------------------------------------------------ data")
print("// data/jobs.txt, which main() writes out and reads back.")
print("fn jobs_text() -> String {")
print("    let mut s = String.new();")
chunk = ""
for line in open("data/jobs.txt", encoding="utf-8", newline="\n").read().split("\n")[:-1]:
    chunk += line + "\n"
    if len(chunk) > 2000:
        print("    s.push_str(%s);" % lit(chunk))
        chunk = ""
if chunk:
    print("    s.push_str(%s);" % lit(chunk))
print("    s")
print("}")
