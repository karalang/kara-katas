# The two command-line interfaces, built with Python's argparse.
import argparse
from argparse import ArgumentParser, ArgumentTypeError


def positive_int(s):
    n = int(s)
    if n <= 0:
        raise ArgumentTypeError(f"must be a positive integer, got {n}")
    return n


def date(s):
    parts = s.split("-")
    ok = len(parts) == 3 and all(p.isdigit() for p in parts) and len(parts[0]) == 4
    if ok:
        m, d = int(parts[1]), int(parts[2])
        ok = 1 <= m <= 12 and 1 <= d <= 31
    if not ok:
        raise ArgumentTypeError(f"not a date: {s!r} (expected YYYY-MM-DD)")
    return s


def pkg():
    p = ArgumentParser(
        prog="pkg",
        description="A small package manager. It installs, removes and lists "
        "packages from a configured index, and keeps a lock file next to "
        "the project.",
        epilog='Run "%(prog)s COMMAND --help" for the options of one command.',
    )
    p.add_argument("-V", "--version", action="version", version="%(prog)s 2.4.1")
    p.add_argument("-v", "--verbose", action="count", default=0,
                   help="print more output; repeat for even more (-vv)")
    p.add_argument("-q", "--quiet", action="store_true", help="print only errors")
    p.add_argument("-C", "--directory", metavar="DIR", default=".",
                   help="run as if started in %(metavar)s")
    p.add_argument("--color", choices=["auto", "always", "never"], default="auto",
                   help="when to color the output (default: %(default)s)")
    p.add_argument("--index-url", metavar="URL", default="https://pkg.example.org/simple",
                   help="base URL of the package index")
    p.add_argument("--timeout", type=float, default=15.0,
                   help="network timeout in seconds")
    sub = p.add_subparsers(dest="command", title="commands", metavar="COMMAND",
                           required=True)

    ins = sub.add_parser("install", aliases=["i", "add"], help="install packages",
                         description="Install packages and their dependencies.")
    ins.add_argument("packages", nargs="+", metavar="PACKAGE",
                     help="a package name, optionally with a version such as "
                     "requests==2.31 or a range such as 'flask>=3,<4'")
    ins.add_argument("-U", "--upgrade", action="store_true",
                     help="upgrade packages that are already installed")
    ins.add_argument("-r", "--requirement", action="append", default=[],
                     metavar="FILE", dest="requirements",
                     help="install from the given requirements file; may be "
                     "given more than once")
    ins.add_argument("--no-deps", action="store_true",
                     help="don't install dependencies")
    ins.add_argument("-j", "--jobs", type=int, default="4",
                     help="number of parallel downloads (default: %(default)s)")
    ins.add_argument("--target", help="install into this directory instead of "
                     "the environment")
    where = ins.add_mutually_exclusive_group()
    where.add_argument("--user", action="store_true", help="install for the current user")
    where.add_argument("--system", action="store_true", help="install for all users")
    ins.set_defaults(handler="install")

    rm = sub.add_parser("remove", aliases=["rm"], help="remove packages")
    rm.add_argument("packages", nargs="+", metavar="PACKAGE")
    rm.add_argument("-y", "--yes", action="store_true", help="don't ask for confirmation")
    rm.add_argument("--keep-config", action=argparse.BooleanOptionalAction,
                    default=True, help="keep the package's configuration files")
    rm.set_defaults(handler="remove")

    ls = sub.add_parser("list", help="list installed packages")
    ls.add_argument("pattern", nargs="?", default="*",
                    help="only packages whose names match this glob")
    ls.add_argument("--format", choices=["columns", "json", "freeze"],
                    default="columns", help="output format")
    ls.add_argument("--outdated", action="store_true",
                    help="only packages with a newer version on the index")
    ls.add_argument("--exclude", action="extend", nargs="+", metavar="PKG",
                    help="leave these packages out")
    ls.set_defaults(handler="list")

    se = sub.add_parser("search", help="search the index")
    se.add_argument("query", nargs="+")
    se.add_argument("--limit", type=positive_int, default=20, metavar="N",
                    help="show at most N results")
    se.add_argument("--sort", choices=["name", "downloads", "updated"],
                    default="downloads")
    se.add_argument("-i", dest="case_insensitive", action="store_true",
                    help="ignore case")
    se.set_defaults(handler="search")

    cfg = sub.add_parser("config", help="read and write settings")
    csub = cfg.add_subparsers(dest="config_command")
    g = csub.add_parser("get", help="print a setting")
    g.add_argument("key")
    s = csub.add_parser("set", help="change a setting")
    s.add_argument("key")
    s.add_argument("value")
    s.add_argument("--global", dest="scope", action="store_const", const="global",
                   default="project", help="change the user-wide setting")
    u = csub.add_parser("unset", help="remove a setting")
    u.add_argument("key", nargs="+")
    csub.add_parser("list", help="print all settings")
    cfg.set_defaults(handler="config")

    run = sub.add_parser("run", help="run a script from the project file")
    run.add_argument("script")
    run.add_argument("args", nargs=argparse.REMAINDER,
                     help="arguments passed on to the script")
    run.set_defaults(handler="run")
    return p


def backup():
    b = ArgumentParser(
        prog="backup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Copy a directory tree into a dated, compressed archive.",
        epilog="examples:\n"
        "  backup --full /home /mnt/disk\n"
        "  backup --since 2024-01-01 --exclude '*.tmp' /etc /mnt/disk\n",
    )
    b.add_argument("source", help="directory to back up")
    b.add_argument("dest", help="where to write the archive")
    mode = b.add_mutually_exclusive_group(required=True)
    mode.add_argument("--full", action="store_true", help="copy everything")
    mode.add_argument("--incremental", action="store_true",
                      help="copy what changed since the last backup")
    mode.add_argument("--since", metavar="DATE", type=date,
                      help="copy what changed since DATE")
    comp = b.add_argument_group("compression",
                                "Archives are compressed with zstd. Level 0 "
                                "stores the files uncompressed.")
    comp.add_argument("-l", "--level", type=int, choices=[0, 1, 3, 9, 19],
                      default=3, help="zstd level (default: %(default)s)")
    comp.add_argument("--dedupe", action="store_true",
                      help="store identical files once")
    b.add_argument("-x", "--exclude", action="append", metavar="GLOB",
                   help="skip files matching GLOB")
    b.add_argument("--keep", type=int, default=7, metavar="N",
                   help="keep the newest N archives and delete the older ones")
    b.add_argument("-n", "--dry-run", action="store_true",
                   help="show what would be copied")
    b.add_argument("--rate", nargs=2, type=int, metavar=("MIN", "MAX"),
                   help="limit the bandwidth to between MIN and MAX KiB/s")
    b.add_argument("--notify", nargs="?", const="root@localhost", metavar="EMAIL",
                   help="mail a report when done (to %(const)s if no address "
                   "is given)")
    b.add_argument("--tz-offset", type=int, default=0, metavar="HOURS",
                   help="hours to add to file times")
    return b
