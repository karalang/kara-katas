# Runs data/jobs.tsv through filetype itself (vendor/filetype/, unchanged)
# and prints what each job gives; expected.out is this output.
import contextlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
sys.dont_write_bytecode = True

import filetype  # noqa: E402
import filetype.__main__ as cli  # noqa: E402
from filetype.types import Type  # noqa: E402

DATA = os.path.join(HERE, "data")


class Csv(Type):
    """A matcher an application adds: a first line of printable ASCII
    with a comma in it."""
    MIME = "text/csv"
    EXTENSION = "csv"

    def __init__(self):
        super(Csv, self).__init__(mime=Csv.MIME, extension=Csv.EXTENSION)

    def match(self, buf):
        line = bytes(buf).split(b"\n")[0]
        return b"," in line and all(0x20 <= b < 0x7f for b in line)


def kind_str(k):
    return "None" if k is None else "%s (%s)" % (k.extension, k.mime)


def ext_of(k):
    return "-" if k is None else k.extension


def report(path_or_bytes):
    k = filetype.guess(path_or_bytes)
    print("guess: " + kind_str(k))
    print("mime: %s, extension: %s" % (filetype.guess_mime(path_or_bytes), filetype.guess_extension(path_or_bytes)))
    cats = [
        ("image", filetype.image_match), ("audio", filetype.audio_match), ("video", filetype.video_match),
        ("font", filetype.font_match), ("document", filetype.document_match), ("archive", filetype.archive_match),
        ("application", filetype.application_match),
    ]
    print(" ".join("%s=%s" % (n, ext_of(f(path_or_bytes))) for n, f in cats))
    flags = [
        ("is_image", filetype.is_image), ("is_audio", filetype.is_audio), ("is_video", filetype.is_video),
        ("is_font", filetype.is_font), ("is_document", filetype.is_document), ("is_archive", filetype.is_archive),
    ]
    yes = [n for n, f in flags if f(path_or_bytes)]
    print("flags: " + (" ".join(yes) if yes else "-"))


def guess_job(args):
    report(os.path.join(DATA, args[0]))


def head_job(args):
    with open(os.path.join(DATA, args[0]), "rb") as f:
        data = f.read()[:int(args[1])]
    report(bytearray(data))


def get_type_job(args):
    kw = {}
    for a in args:
        k, v = a.split("=", 1)
        kw[k] = v
    print(kind_str(filetype.get_type(**kw)))


def supported_job(args):
    if args[0] == "ext":
        print(filetype.is_extension_supported(args[1]))
    else:
        print(filetype.is_mime_supported(args[1]))


def types_job(args):
    print("%d types" % len(filetype.types))
    for k in filetype.types:
        print("%s %s %s" % (type(k).__name__, k.extension, k.mime))


def cli_job(args):
    out = io.StringIO()
    err = io.StringIO()
    old = sys.argv
    sys.argv = ["filetype"] + args
    cwd = os.getcwd()
    os.chdir(DATA)
    code = 0
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            cli.main()
    except SystemExit as e:
        code = e.code
    finally:
        sys.argv = old
        os.chdir(cwd)
    for line in out.getvalue().splitlines():
        print("| " + line)
    for line in err.getvalue().splitlines():
        print("! " + line)
    print("exit %s" % code)


def custom_job(args):
    filetype.add_type(Csv())
    print("%d types, first %s" % (len(filetype.types), filetype.types[0].extension))
    report(os.path.join(DATA, args[0]))


def custom_bad_job(args):
    try:
        filetype.add_type(object())
    except TypeError as e:
        print("error: TypeError: %s" % e)
    print("%d types" % len(filetype.types))


JOBS = {
    "guess": guess_job, "head": head_job, "get_type": get_type_job, "supported": supported_job,
    "types": types_job, "cli": cli_job, "custom": custom_job, "custom-bad": custom_bad_job,
}


def main():
    with open(os.path.join(DATA, "jobs.tsv"), encoding="utf-8") as f:
        jobs = [line.rstrip("\n").split("\t") for line in f]
    for job in jobs:
        print("== " + " ".join(job))
        JOBS[job[0]](job[1:])


main()
