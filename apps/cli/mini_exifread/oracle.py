#!/usr/bin/env python3
"""Replays data/jobs.tsv through the vendored ExifRead 3.5.1, printing what
mini_exifread.kara must print. A cli job is exifread.cli.run_cli on one
file, with the CLI's own logger set up (INFO, "%(message)s", stdout); the
file is held in memory instead of opened by name. An exception the library
lets escape prints as "error <Class>: <str(e)>" and a blank line.
Run: python3 -I -B oracle.py > expected.out"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
import exifread  # noqa: E402
from exifread import exif_log  # noqa: E402
from exifread.tags.fields import FIELD_DEFINITIONS  # noqa: E402
from exifread.utils import get_gps_coords  # noqa: E402

logger = exif_log.get_logger()


def options(flags):
    o = {"detailed": True, "strict": False, "builtin": False, "stop": None}
    if flags == "-":
        return o
    for f in flags.split(","):
        if f == "q":
            o["detailed"] = False
        elif f == "s":
            o["strict"] = True
        elif f == "b":
            o["builtin"] = True
        elif f.startswith("t="):
            o["stop"] = f[2:]
        else:
            raise SystemExit("bad flag " + f)
    return o


def process(o, data):
    return exifread.process_file(
        io.BytesIO(data),
        stop_tag=o["stop"],
        details=o["detailed"],
        strict=o["strict"],
        debug=False,
        extract_thumbnail=o["detailed"],
        builtin_types=o["builtin"],
    )


def cli(o, name, data):
    """The body of exifread.cli.run_cli for one file."""
    logger.info("Opening: %s", name)
    data = process(o, data)
    if not data:
        logger.warning("No EXIF information found")
        print()
        return
    if "JPEGThumbnail" in data:
        logger.info("File has JPEG thumbnail")
        del data["JPEGThumbnail"]
    if "TIFFThumbnail" in data:
        logger.info("File has TIFF thumbnail")
        del data["TIFFThumbnail"]
    for field in sorted(data):
        value = data[field]
        if o["builtin"]:
            logger.info("%s (%s): %r", field, type(value).__name__, value)
        else:
            logger.info("%s (%s): %s", field, FIELD_DEFINITIONS[value.field_type][1], value.printable)
    print()


def main():
    exif_log.setup_logger(False, False)
    with open(os.path.join(HERE, "data", "jobs.tsv"), encoding="utf-8") as fh:
        jobs = [ln.split("\t") for ln in fh.read().split("\n") if ln]
    for kind, flags, name, hexdata in jobs:
        print("== %s %s %s (%d bytes)" % (kind, flags, name, len(hexdata) // 2))
        sys.stdout.flush()
        data = bytes.fromhex(hexdata)
        o = options(flags)
        try:
            if kind == "cli":
                cli(o, name, data)
            elif kind == "gps":
                tags = process(o, data)
                print("coords %r" % (get_gps_coords(tags),))
            elif kind == "thumb":
                tags = process(o, data)
                for key in ("JPEGThumbnail", "TIFFThumbnail"):
                    if key in tags:
                        print("%s %d %s" % (key, len(tags[key]), tags[key].hex()))
                    else:
                        print("%s none" % key)
            else:
                raise SystemExit("bad job " + kind)
        except SystemExit:
            raise
        except Exception as e:
            sys.stdout.flush()
            print("error %s: %s" % (type(e).__name__, e))
            print()
        sys.stdout.flush()


main()
