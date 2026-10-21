"""Writes the generated parts of mini_dpkt.kara to stdout: with the
argument `tables`, dpkt's cipher suite table; with none, the files under
data/ (the captures as hex)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
os.chdir(HERE)

from dpkt import ssl_ciphersuites  # noqa: E402


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
        elif ord(ch) < 32 or ord(ch) > 126:
            out.append("\\u{%x}" % ord(ch))
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


def tables():
    suites = sorted(ssl_ciphersuites.BY_CODE.values(), key=lambda c: c.code)
    print("// ------------------------------------------------------------ tables")
    print()
    print("// dpkt's cipher suites (ssl_ciphersuites.BY_CODE), as gen_kara.py read")
    print("// them: the code, then the name, kx, encoding, mode and mac properties.")
    print("fn suite(code: i64, name: Str, kx: Str, encoding: Str, mode: Str, mac: Str) -> Option[Suite] {")
    print("    Some(Suite { code: code, name: name.to_string(), kx: kx.to_string(), encoding: encoding.to_string(), "
          "mode: mode.to_string(), mac: mac.to_string() })")
    print("}")
    per = 120
    chunks = [suites[k:k + per] for k in range(0, len(suites), per)]
    for n, chunk in enumerate(chunks):
        print()
        print("fn suites_%d(code: i64) -> Option[Suite] {" % n)
        print("    match code {")
        for c in chunk:
            print("        0x%04x => suite(code, %s, %s, %s, %s, %s),"
                  % (c.code, lit(c.name), lit(c.kx), lit(c.encoding), lit(c.mode), lit(c.mac)))
        print("        _ => None,")
        print("    }")
        print("}")
    print()
    print("// BY_CODE.get(code)")
    print("fn suite_by_code(code: i64) -> Option[Suite] {")
    for n, chunk in enumerate(chunks):
        kw = "if" if n == 0 else "} else if"
        if n < len(chunks) - 1:
            print("    %s code <= 0x%04x {" % (kw, chunk[-1].code))
        else:
            print("    } else {")
        print("        suites_%d(code)" % n)
    print("    }")
    print("}")


def is_text(b):
    try:
        s = b.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return all(c >= " " or c in "\n\t" for c in s)


def datafiles():
    names = []
    for root, dirs, files in os.walk("data"):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), "data")
            if not rel.startswith("out" + os.sep):
                names.append(rel)
    names.sort()
    print("// ------------------------------------------------------------ data")
    print()
    print("// The files under data/, in path order; the captures are spelled in hex.")
    print("fn data_files() -> Vec[DataFile] {")
    print("    let mut v: Vec[DataFile] = Vec.new();")
    for k in range(len(names)):
        print("    v.push(data_%d());" % k)
    print("    v")
    print("}")
    for k, n in enumerate(names):
        b = open(os.path.join("data", n), "rb").read()
        print()
        print("fn data_%d() -> DataFile {" % k)
        print("    let mut t = String.new();")
        if is_text(b):
            for line in b.decode("utf-8").splitlines(keepends=True):
                print("    t.push_str(%s);" % lit(line))
            print("    DataFile { path: %s.to_string(), body: t, hex: false }" % lit(n))
        else:
            h = b.hex()
            for i in range(0, len(h), 96):
                print('    t.push_str("%s");' % h[i:i + 96])
            print("    DataFile { path: %s.to_string(), body: t, hex: true }" % lit(n))
        print("}")


if sys.argv[1:] == ["tables"]:
    tables()
else:
    datafiles()
