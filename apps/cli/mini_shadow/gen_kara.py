# Prints the Kara functions that hold mk.FILES, for mini_shadow.kara's
# data section.
import mk

def lit(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'

names = list(mk.FILES)
for i, n in enumerate(names):
    print("fn file_%d() -> String {" % i)
    lines = mk.FILES[n].split("\n")
    parts = [l + "\n" for l in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
    print("    let mut s = String.new();")
    for p in parts:
        print("    s.push_str(%s);" % lit(p))
    print("    s")
    print("}")
    print()
print("fn data_files() -> Vec[(String, String)] {")
print("    let mut v: Vec[(String, String)] = Vec.new();")
for i, n in enumerate(names):
    print('    v.push((%s.to_string(), file_%d()));' % (lit(n), i))
print("    v")
print("}")
print()
import usage
for name, text in (("chage_usage", usage.CHAGE), ("passwd_usage", usage.PASSWD)):
    print("// The usage message shadow 4.13 prints after an error.")
    print("fn %s() -> String {" % name)
    print("    let mut s = String.new();")
    for l in text.split("\n")[:-1]:
        print("    s.push_str(%s);" % lit(l + "\n"))
    print("    s")
    print("}")
    print()
