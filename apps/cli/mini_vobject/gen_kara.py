"""Writes the generated part of mini_vobject.kara to stdout: data_files(),
every input file under data/ (jobs.txt included) as hex, which main() writes
back to disk before running the jobs."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def main():
    names = sorted(n for n in os.listdir(DATA) if os.path.isfile(os.path.join(DATA, n)))
    print("// ------------------------------------------------------------ data (gen_kara.py)")
    print()
    print("fn data_files() -> Vec[(String, String)] {")
    print("    let mut v: Vec[(String, String)] = Vec.new();")
    for n in names:
        with open(os.path.join(DATA, n), "rb") as f:
            hx = f.read().hex()
        print("    v.push((\"%s\".to_string(), \"%s\".to_string()));" % (n, hx))
    print("    v")
    print("}")


main()
