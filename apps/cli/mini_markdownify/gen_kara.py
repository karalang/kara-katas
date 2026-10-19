# Prints the Kara functions that hold data/ (mk.PAGES, mk.JOBS and the
# option sets), for mini_markdownify.kara's data section.
import mk


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


files = [("pages/" + n, t) for n, t in mk.PAGES.items()]
files.append(("jobs.tsv", mk.JOBS.lstrip("\n")))
files.append(("options.tsv", mk.options_text()))
for i, (name, text) in enumerate(files):
    lines = text.split("\n")
    parts = [line + "\n" for line in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
    # at most 150 pushes per function
    chunks = [parts[k:k + 150] for k in range(0, len(parts), 150)] or [[]]
    for c, chunk in enumerate(chunks):
        print("fn file_%d_%d(s: mut ref String) {" % (i, c))
        for p in chunk:
            print("    s.push_str(%s);" % lit(p))
        print("}")
        print()
    print("fn file_%d() -> String {" % i)
    print("    let mut s = String.new();")
    for c in range(len(chunks)):
        print("    file_%d_%d(mut s);" % (i, c))
    print("    s")
    print("}")
    print()
print("fn data_files() -> Vec[(String, String)] {")
print("    let mut v: Vec[(String, String)] = Vec.new();")
for i, (name, _) in enumerate(files):
    print("    v.push((%s.to_string(), file_%d()));" % (lit(name), i))
print("    v")
print("}")
