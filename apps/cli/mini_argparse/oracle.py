# The oracle: every line of data/cases.txt parsed with Python's argparse,
# with the terminal 80 columns wide.
import contextlib, io, os, shlex, sys
os.environ["COLUMNS"] = "80"
import parsers

for line in open("data/cases.txt"):
    line = line.rstrip("\n")
    if not line or line.startswith("#"):
        if line:
            print(line)
        continue
    argv = shlex.split(line)
    parser = {"pkg": parsers.pkg, "backup": parsers.backup}[argv[0]]()
    out, err = io.StringIO(), io.StringIO()
    status = None
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            ns = parser.parse_args(argv[1:])
        except SystemExit as e:
            status = e.code
    print(f"$ {line}")
    for l in out.getvalue().splitlines():
        print(f"  |{l}")
    for l in err.getvalue().splitlines():
        print(f"  !{l}")
    if status is None:
        print(f"  {ns!r}")
    else:
        print(f"  exit {status}")
