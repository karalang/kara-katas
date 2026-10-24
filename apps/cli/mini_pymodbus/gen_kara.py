# Prints the Kara function that holds data/jobs.txt (as mk.py writes it),
# for the end of mini_pymodbus.kara.
def lit(s):
    out = []
    for ch in s:
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "{":
            out.append("{")
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'

print()
print("// ------------------------------------------------------------ data")
print("// data/jobs.txt, which main() writes out and reads back.")
print("fn jobs_text() -> String {")
print("    let mut s = String.new();")
for line in open("data/jobs.txt", encoding="utf-8").read().split("\n")[:-1]:
    print("    s.push_str(%s);" % lit(line + "\\n").replace("\\\\n\"", "\\n\""))
print("    s")
print("}")
