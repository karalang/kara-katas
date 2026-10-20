# Runs data/ through Python 3.13's own optparse module and prints what
# expected.out holds. Run it from the app directory, after mk.py.
import io
import os
import contextlib
from optparse import (OptionParser, OptionValueError, IndentedHelpFormatter,
                      TitledHelpFormatter, SUPPRESS_HELP, SUPPRESS_USAGE)


def read_tsv(path):
    with open(path, newline="") as f:
        text = f.read()
    return [line.split("\t") for line in text.split("\n")[:-1]]


# ------------------------------------------------------------ callbacks

def cb_csv(option, opt_str, value, parser):
    setattr(parser.values, option.dest, value.split(","))


# The vararg callback from the optparse documentation.
def cb_vararg(option, opt_str, value, parser):
    assert value is None
    value = []

    def floatable(str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    for arg in parser.rargs:
        # stop on --foo like options
        if arg[:2] == "--" and len(arg) > 2:
            break
        # stop on -a, but not on -3 or -3.0
        if arg[:1] == "-" and len(arg) > 1 and not floatable(arg):
            break
        value.append(arg)

    del parser.rargs[:len(value)]
    setattr(parser.values, option.dest, value)


# check_order, also from the documentation: -a may not follow -b.
def cb_check_order(option, opt_str, value, parser):
    if parser.values.b:
        raise OptionValueError("can't use -a after -b")
    parser.values.a = 1


def cb_record(option, opt_str, value, parser):
    print("callback %s value=%r rargs=%r largs=%r"
          % (opt_str, value, parser.rargs, parser.largs))
    parser.values.ensure_value("seen", []).append(opt_str)


CALLBACKS = {"csv": cb_csv, "vararg": cb_vararg,
             "check_order": cb_check_order, "record": cb_record}


# ------------------------------------------------------------ the spec

def lit(s):
    kind, _, rest = s.partition(":")
    if kind == "s":
        return rest
    if kind == "i":
        return int(rest)
    if kind == "f":
        return float(rest)
    if kind == "b":
        return rest == "1"
    if kind == "n":
        return None
    if kind == "l":
        return rest.split(",") if rest else []
    raise ValueError(s)


PLAIN = ("action", "type", "dest", "help", "metavar")


def option_kwargs(fields):
    kw = {}
    for f in fields:
        k, _, v = f.partition("=")
        if k in PLAIN:
            kw[k] = SUPPRESS_HELP if (k == "help" and v == "@SUPPRESS") else v
        elif k == "callback":
            kw[k] = CALLBACKS.get(v, v)
        elif k == "nargs":
            kw[k] = int(v)
        elif k in ("default", "const", "choices"):
            kw[k] = lit(v)
        else:
            kw[k] = v
    return kw


def new_parser(fields):
    kw = {}
    fkw = {}
    titled = False
    for f in fields:
        k, _, v = f.partition("=")
        if k == "usage":
            kw["usage"] = SUPPRESS_USAGE if v == "@SUPPRESS" else v
        elif k in ("prog", "version", "description", "epilog"):
            kw[k] = v
        elif k == "conflict":
            kw["conflict_handler"] = v
        elif k == "add_help":
            kw["add_help_option"] = v == "1"
        elif k == "formatter":
            titled = v == "titled"
        elif k == "indent":
            fkw["indent_increment"] = int(v)
        elif k in ("width", "max_help_position", "short_first"):
            fkw[k] = int(v)
    fmt = TitledHelpFormatter(**fkw) if titled else IndentedHelpFormatter(**fkw)
    return OptionParser(formatter=fmt, **kw)


def show(text, prefix):
    if not text:
        return
    lines = text.split("\n")
    if lines[-1] == "":
        lines.pop()
    for line in lines:
        print(prefix + (" " + line if line else ""))


def captured(fn):
    out = io.StringIO()
    err = io.StringIO()
    code = None
    exc = None
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            fn()
        except SystemExit as e:
            code = e.code
        except (OptionValueError, ValueError) as e:
            exc = "%s: %s" % (type(e).__name__, e)
    show(out.getvalue(), "  |")
    show(err.getvalue(), "  err|")
    if code is not None:
        print("  [exit %d]" % code)
    if exc is not None:
        print("  ! " + exc)


# ------------------------------------------------------------ the jobs

def run_jobs():
    p = None
    target = None
    for f in read_tsv("data/jobs.tsv"):
        op = f[0]
        if op == "job":
            print("== " + f[1])
            continue
        if op == "parse":
            print("> parse %r" % (f[1:],))
        else:
            print("> " + " ".join(f))
        try:
            if op == "env":
                k, eq, v = f[1].partition("=")
                if eq:
                    os.environ[k] = v
                else:
                    os.environ.pop(k, None)
            elif op == "parser":
                p = new_parser(f[1:])
                target = p
            elif op == "option":
                opts = f[1].split(",")
                o = target.add_option(*opts, **option_kwargs(f[2:]))
                print("  %s: action=%s type=%s dest=%s nargs=%s"
                      % (o, o.action, o.type, o.dest, o.nargs))
            elif op == "group":
                target = p.add_option_group(f[1], f[2] if len(f) > 2 else None)
            elif op == "endgroup":
                target = p
            elif op == "set_defaults":
                p.set_defaults(**{k: lit(v) for k, _, v in
                                  (x.partition("=") for x in f[1:])})
            elif op == "remove":
                p.remove_option(f[1])
                print("  removed " + f[1])
            elif op == "has":
                print("  %s" % p.has_option(f[1]))
            elif op == "group_of":
                g = p.get_option_group(f[1])
                print("  %s" % (g.title if g else None))
            elif op == "interspersed":
                if f[1] == "1":
                    p.enable_interspersed_args()
                else:
                    p.disable_interspersed_args()
            elif op == "defaults":
                print("  %s" % p.defaults)
            elif op == "parse":
                def go():
                    opts, args = p.parse_args(f[1:])
                    print("values: %s" % opts)
                    print("args: %r" % args)
                captured(go)
            elif op == "help":
                captured(p.print_help)
            elif op == "usage":
                captured(p.print_usage)
            elif op == "version":
                captured(p.print_version)
        except Exception as e:
            print("  ! %s: %s" % (type(e).__name__, e))


# ------------------------------------------------------------ the programs

def read_conf(path):
    conf = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            k, _, v = line.partition("=")
            conf[k.strip()] = v.strip()
    return conf


def backup_parser():
    p = OptionParser(prog="backup-tool", usage="%prog [options] SRC DEST",
                     version="%prog 2.4.1")
    p.add_option("-v", "--verbose", action="count", default=0,
                 help="print more detail; repeat for even more")
    p.add_option("-q", "--quiet", action="store_const", const=0,
                 dest="verbose", help="print only errors")
    p.add_option("-n", "--dry-run", action="store_true",
                 help="show what would be copied, but copy nothing")
    p.add_option("--keep", type="int", metavar="N",
                 help="keep N snapshots [default: %default]")
    p.add_option("--compress", choices=["none", "gzip", "zstd"],
                 help="none, gzip or zstd [default: %default]")
    p.add_option("-x", "--exclude", action="append", metavar="GLOB",
                 help="skip files that match GLOB")
    p.add_option("--exclude-from", metavar="FILE",
                 help="read more globs from FILE")
    p.add_option("--bandwidth", "--bw", type="float", metavar="MBPS",
                 help="limit the copy to MBPS megabytes a second")
    return p


def backup_run(p, argv):
    opts, args = p.parse_args(argv)
    if len(args) != 2:
        p.error("expected SRC and DEST, got %d argument(s)" % len(args))
    src, dest = args
    mode = "dry run" if opts.dry_run else "copy"
    print("%s %s -> %s" % (mode, src, dest))
    print("  keep %d, compress %s, verbosity %d" % (opts.keep, opts.compress, opts.verbose))
    if opts.bandwidth is not None:
        print("  bandwidth %r MB/s, %d KB a tick" % (opts.bandwidth, int(opts.bandwidth * 1024 / 10)))
    excludes = list(opts.exclude or [])
    if opts.exclude_from:
        excludes.append("@" + opts.exclude_from)
    print("  excludes %r" % (excludes,))
    if opts.verbose > 1:
        print("  options %s" % opts)


def backup_program():
    print("== program: backup-tool with backup.conf")
    conf = read_conf("data/backup.conf")
    print("> config %s" % conf)
    p = backup_parser()
    p.set_defaults(**conf)
    for f in read_tsv("data/backup_runs.tsv"):
        argv = f[1:]
        print("$ backup-tool " + " ".join(argv))
        captured(lambda: backup_run(p, argv))


SUBCOMMANDS = ["status", "commit", "log", "push", "checkout"]


def vcs_sub(cmd):
    p = OptionParser(prog="vcs " + cmd)
    if cmd == "status":
        p.set_usage("%prog [-s] [-b]")
        p.add_option("-s", "--short", action="store_true", help="one line a file")
        p.add_option("-b", "--branch", action="store_true", help="show the branch")
    elif cmd == "commit":
        p.set_usage("%prog -m MSG [-a] [FILE...]")
        p.add_option("-m", "--message", metavar="MSG", help="the commit message")
        p.add_option("-a", "--all", action="store_true", help="commit every changed file")
        p.add_option("--amend", action="store_true", help="replace the last commit")
    elif cmd == "log":
        p.set_usage("%prog [-n N] [--oneline] [RANGE]")
        p.add_option("-n", "--max-count", type="int", metavar="N", help="show at most N commits")
        p.add_option("--oneline", action="store_true", help="one line a commit")
    elif cmd == "push":
        p.set_usage("%prog [-f] [-u] REMOTE [BRANCH]")
        p.add_option("-f", "--force", action="store_true", help="overwrite the remote branch")
        p.add_option("-u", "--set-upstream", action="store_true", help="track the remote branch")
    else:
        p.set_usage("%prog [-b NEW] [--track] [BRANCH]")
        p.add_option("-b", dest="new_branch", metavar="NEW", help="create branch NEW")
        p.add_option("--track", action="store_true", help="track the upstream")
    return p


def vcs_run(top, argv):
    opts, args = top.parse_args(argv)
    if not args:
        top.error("no command given")
    cmd = args[0]
    if cmd not in SUBCOMMANDS:
        top.error("unknown command %r (choose from %s)" % (cmd, ", ".join(SUBCOMMANDS)))
    sub = vcs_sub(cmd)
    sopts, sargs = sub.parse_args(args[1:])
    where = opts.chdir or "."
    if opts.verbose:
        print("[%s] %s %s %r" % (where, cmd, sopts, sargs))
    if cmd == "status":
        print("status of %s%s%s" % (where, " (short)" if sopts.short else "",
                                    " with branch" if sopts.branch else ""))
    elif cmd == "commit":
        if sopts.message is None:
            sub.error("a commit message is required (use -m)")
        files = "all changed files" if sopts.all else ", ".join(sargs) or "the index"
        print("commit %r from %s" % (sopts.message, files))
    elif cmd == "log":
        n = "all" if sopts.max_count is None else str(sopts.max_count)
        rng = sargs[0] if sargs else "HEAD"
        print("log %s, %s commits%s" % (rng, n, ", one line each" if sopts.oneline else ""))
    elif cmd == "push":
        if len(sargs) not in (1, 2):
            sub.error("expected REMOTE [BRANCH]")
        branch = sargs[1] if len(sargs) == 2 else "the current branch"
        print("push %s to %s%s%s" % (branch, sargs[0], " (forced)" if sopts.force else "",
                                     ", tracking it" if sopts.set_upstream else ""))
    else:
        print("checkout %s%s" % ("new branch " + sopts.new_branch if sopts.new_branch
                                 else (sargs[0] if sargs else "nothing"),
                                 " tracking upstream" if sopts.track else ""))


def vcs_program():
    print("== program: vcs, a git-like dispatcher")
    top = OptionParser(prog="vcs", usage="%prog [-C DIR] [-v] COMMAND [ARGS...]")
    top.disable_interspersed_args()
    top.add_option("-C", dest="chdir", metavar="DIR", help="run as if started in DIR")
    top.add_option("-v", "--verbose", action="store_true", help="show the parsed options")
    for f in read_tsv("data/vcs_runs.tsv"):
        argv = f[1:]
        print("$ vcs " + " ".join(argv))
        captured(lambda: vcs_run(top, argv))


os.environ.pop("COLUMNS", None)
run_jobs()
os.environ.pop("COLUMNS", None)
backup_program()
vcs_program()
