# Prints the Kara functions that hold the files mk.py writes under data/,
# for the end of mini_cantools.kara. Lines are grouped into literals of
# about 2 KB.
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


def body(path):
    text = open(path, encoding="utf-8", newline="\n").read()
    lines = []
    chunk = ""
    for line in text.split("\n")[:-1]:
        chunk += line + "\n"
        if len(chunk) > 2000:
            lines.append("    s.push_str(%s);" % lit(chunk))
            chunk = ""
    if chunk:
        lines.append("    s.push_str(%s);" % lit(chunk))
    return lines


def emit(fn, path):
    print()
    print(f"// {path}, which run() writes out and reads back.")
    print(f"fn {fn}() -> String {{")
    print("    let mut s = String.new();")
    for line in body(path):
        print(line)
    print("    s")
    print("}")


print()
print("// ------------------------------------------------------------ data")
emit("vehicle_dbc", "data/vehicle.dbc")
emit("jobs_text", "data/jobs.txt")
emit("drive_log", "data/drive.log")
print()
print("// data/bad_*.dbc, in file name order.")
print("fn broken_files() -> Vec[(String, String)] {")
print("    let mut out: Vec[(String, String)] = Vec.new();")
for name in sorted(n for n in os.listdir("data") if n.startswith("bad_")):
    text = open(os.path.join("data", name), encoding="utf-8", newline="\n").read()
    print(f"    out.push((\"{name}\".to_string(), {lit(text)}.to_string()));")
print("    out")
print("}")
