# Prints the Kara functions that hold data/corpus.txt and data/jobs.txt
# (as mk.py writes them), for the end of mini_spellchecker.kara. Lines are
# grouped into literals of about 2 KB.
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


def emit(fn, path):
    print()
    print(f"// {path}, which main() writes out and the jobs read back.")
    print(f"fn {fn}() -> String {{")
    print("    let mut s = String.new();")
    chunk = ""
    for line in open(path, encoding="utf-8", newline="\n").read().split("\n")[:-1]:
        chunk += line + "\n"
        if len(chunk) > 2000:
            print("    s.push_str(%s);" % lit(chunk))
            chunk = ""
    if chunk:
        print("    s.push_str(%s);" % lit(chunk))
    print("    s")
    print("}")


print()
print("// ------------------------------------------------------------ data")
emit("corpus_text", "data/corpus.txt")
emit("jobs_text", "data/jobs.txt")
