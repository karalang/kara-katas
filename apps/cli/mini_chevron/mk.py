# Writes data/: the Mustache cases (inputs/cases.txt, with CRLF line
# ends put into the one case that is about them) and the site files the
# command-line jobs render (inputs/site/, copied as they are; the CI
# workflow template was saved on Windows and has CRLF line ends).
import os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
CRLF_CASE = "=== sections: CRLF line ends"


def cases():
    with open(os.path.join(HERE, "inputs", "cases.txt"), encoding="utf-8", newline="") as f:
        lines = f.read().split("\n")
    out = []
    in_case = False
    in_template = False
    for line in lines:
        if line.startswith("=== "):
            in_case = line == CRLF_CASE
            in_template = False
        elif line.startswith("~~~ "):
            in_template = in_case and line == "~~~ template"
        elif in_template:
            line += "\r"
        out.append(line)
    return "\n".join(out)


def main():
    if os.path.isdir(DATA):
        shutil.rmtree(DATA)
    os.makedirs(DATA)
    with open(os.path.join(DATA, "cases.txt"), "w", encoding="utf-8", newline="") as f:
        f.write(cases())
    shutil.copytree(os.path.join(HERE, "inputs", "site"), os.path.join(DATA, "site"))


if __name__ == "__main__":
    main()
