"""Runs data/jobs.txt through the copy of tinytag 2.3.2 in tinytag/.

A `tinytag` job is the command line (tinytag/__main__.py) with those
arguments; what it writes to stderr is printed in line with its stdout,
then its exit status. The other jobs call the Python API: `get` is
TinyTag.get with keyword arguments, `images` prints a file's images,
`supported` asks TinyTag.is_supported, and `files` lists what the
command line saved."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
os.chdir(HERE)

from tinytag import TinyTag  # noqa: E402
from tinytag import __main__ as cli  # noqa: E402


def run_cli(args):
    sys.argv = ["tinytag"] + args
    saved = sys.stderr
    sys.stderr = sys.stdout
    try:
        rc = cli._run()
    finally:
        sys.stderr = saved
    print("exit %d" % rc)


def get(args):
    name = args[0]
    kw = {}
    for a in args[1:]:
        k, v = a.split("=")
        kw["check_magic_bytes" if k == "magic" else k] = v == "1"
    try:
        tag = TinyTag.get(name, **kw)
    except Exception as e:
        print("error: %s: %s" % (type(e).__name__, e))
        return
    print(json.dumps(tag.as_dict(), ensure_ascii=False, indent=2))
    if kw.get("image"):
        show_images(tag)


def show_images(tag):
    images = tag.images.as_dict()
    if not images:
        print("no images")
    for k, v in images.items():
        print("%s: %r" % (k, v))
    print("any: %r" % (tag.images.any,))


def images(args):
    show_images(TinyTag.get(args[0], image=True))


def files(args):
    d = args[0]
    for name in sorted(os.listdir(d)):
        with open(os.path.join(d, name), "rb") as f:
            data = f.read()
        print("%s %d bytes %s" % (name, len(data), data[:16].hex()))


def main():
    with open("data/jobs.txt") as f:
        lines = [x.strip() for x in f if x.strip() and not x.startswith("#")]
    for line in lines:
        print("$ " + line)
        parts = line.split()
        cmd, args = parts[0], parts[1:]
        if cmd == "tinytag":
            run_cli(args)
        elif cmd == "get":
            get(args)
        elif cmd == "images":
            images(args)
        elif cmd == "supported":
            for a in args:
                print("%s: %s" % (a, TinyTag.is_supported(a)))
        elif cmd == "files":
            files(args)
        else:
            print("unknown job")


main()
