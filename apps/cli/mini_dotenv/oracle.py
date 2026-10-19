# Runs data/jobs.jsonl through the real python-dotenv 1.2.3
# (pip install "python-dotenv[cli]==1.2.3", click 8.5.0) and prints what
# mini_dotenv prints. Run it after mk.py; its output is expected.out.
import io, json, logging, os, shutil, sys

import dotenv
from dotenv.main import DotEnv, dotenv_values, load_dotenv, set_key, unset_key, get_key
from dotenv.parser import parse_stream
from dotenv.variables import parse_variables
from dotenv.cli import cli
from click.testing import CliRunner


PREFIX = ["  "]


class Show(logging.Handler):
    def emit(self, record):
        print(PREFIX[0] + "warning: " + record.getMessage())


def vis(s):
    # A line of command output with its control characters made visible.
    return "".join("\\x%02x" % ord(c) if ord(c) < 32 and c != "\t" or ord(c) == 127 else c for c in s)


log = logging.getLogger("dotenv.main")
log.addHandler(Show(level=logging.WARNING))
log.propagate = False


def set_environ(e):
    os.environ.clear()
    os.environ.update(e)


def show_environ(before):
    for k in sorted(os.environ):
        if before.get(k) != os.environ[k]:
            print("  %s=%r" % (k, os.environ[k]))


def main():
    os.makedirs("data/work", exist_ok=True)
    for n in os.listdir("data/work"):
        os.remove(os.path.join("data/work", n))
    saved = dict(os.environ)
    edits = 0
    for line in open("data/jobs.jsonl"):
        line = line.rstrip("\n")
        j = json.loads(line)
        print("== " + line)
        set_environ(j.get("environ", {}))
        k = j["kind"]
        if k == "parse":
            with open(j["file"], encoding="utf-8") as f:
                for b in parse_stream(f):
                    print("  %r" % (b,))
        elif k == "parse_text":
            for b in parse_stream(io.StringIO(j["text"])):
                print("  %r" % (b,))
        elif k == "vars":
            print("  %r" % (list(parse_variables(j["value"])),))
        elif k == "values":
            for key, v in dotenv_values(j["file"], interpolate=j["interpolate"]).items():
                print("  %r: %r" % (key, v))
        elif k == "values_override":
            d = DotEnv(j["file"], override=j["override"]).dict()
            for key, v in d.items():
                print("  %r: %r" % (key, v))
        elif k == "load":
            before = dict(os.environ)
            for f in j["files"]:
                r = load_dotenv(f, override=j["override"], interpolate=j.get("interpolate", True))
                print("  load %s -> %s" % (f, r))
            show_environ(before)
        elif k == "merge":
            config = {}
            for f in j["files"]:
                config.update(dotenv_values(f))
            config.update(os.environ)
            for key in sorted(config):
                print("  %s=%r" % (key, config[key]))
        elif k == "edit":
            edits += 1
            path = "data/work/edit%d.env" % edits
            if j["start"] is not None:
                shutil.copyfile(j["start"], path)
            for op in j["ops"]:
                try:
                    if op[0] == "set":
                        r = set_key(path, op[1], op[2], *op[3:])
                    elif op[0] == "unset":
                        r = unset_key(path, op[1])
                    else:
                        r = get_key(path, op[1])
                    print("  %s -> %r" % (" ".join(map(str, op)), r))
                except ValueError as e:
                    print("  %s -> ValueError: %s" % (" ".join(map(str, op)), e))
            if os.path.exists(path):
                print("  file %r" % open(path, "rb").read().decode("utf-8"))
            else:
                print("  no file")
        elif k == "cli":
            PREFIX[0] = ""
            r = CliRunner().invoke(cli, j["args"])
            PREFIX[0] = "  "
            out = r.output
            if out.endswith("\n"):
                out = out[:-1]
            if out:
                for out_line in out.split("\n"):
                    print("  | " + vis(out_line))
            print("  exit %d" % r.exit_code)
    set_environ(saved)


main()
