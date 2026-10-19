# Prints the Kara functions that hold mk.FILES and mk.JOBS, for
# mini_distro.kara's data section.
import mk


def lit(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t") + '"'


files = [("roots/" + p, t) for p, t in mk.FILES.items() if t is not None]
files.append(("jobs.tsv", mk.JOBS.lstrip("\n")))
dirs = ["data/roots/" + p for p, t in mk.FILES.items() if t is None]

for i, (name, text) in enumerate(files):
    print("fn file_%d() -> String {" % i)
    lines = text.split("\n")
    parts = [line + "\n" for line in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
    print("    let mut s = String.new();")
    for p in parts:
        print("    s.push_str(%s);" % lit(p))
    print("    s")
    print("}")
    print()
print("fn data_files() -> Vec[(String, String)] {")
print("    let mut v: Vec[(String, String)] = Vec.new();")
for i, (name, _) in enumerate(files):
    print("    v.push((%s.to_string(), file_%d()));" % (lit(name), i))
print("    v")
print("}")
print()
print("fn data_dirs() -> Vec[String] {")
print("    let mut v: Vec[String] = Vec.new();")
for d in dirs:
    print("    v.push(%s.to_string());" % lit(d))
print("    v")
print("}")
