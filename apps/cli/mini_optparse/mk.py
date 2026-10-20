# Writes data/: jobs.tsv (the parser jobs), backup.conf and
# backup_runs.tsv (the backup tool's config file and command lines), and
# vcs_runs.tsv (command lines for the git-like dispatcher). Run it from
# the app directory.
#
# jobs.tsv, one op per line, fields split by tabs:
#   job NAME                        start a job
#   env COLUMNS=V | env COLUMNS     set or unset $COLUMNS
#   parser key=value...             a new OptionParser (see below)
#   option OPTS key=value...        add_option; OPTS split by commas
#   group TITLE [DESC]              add_option_group; options go there
#   endgroup                        options go to the parser again
#   set_defaults key=LIT...
#   remove OPT | has OPT | group_of OPT
#   interspersed 0|1
#   parse ARG...                    parse_args with every ARG as given
#   help | usage | version | defaults
# A LIT is s:text, i:5, f:1.5, b:1, n: (None) or l:a,b (a list of strings).
# action, type, dest, help, metavar and callback are plain strings,
# nargs a number, default/const/choices are LITs; any other key is passed
# through so that optparse can refuse it. help=@SUPPRESS is SUPPRESS_HELP.
import os

jobs = []


def job(name, *ops):
    jobs.append(["job", name])
    for op in ops:
        jobs.append(list(op))


job("basics",
    ("env", "COLUMNS"),
    ("parser", "prog=backup-tool"),
    ("option", "-v,--verbose", "action=store_true", "help=print each file"),
    ("option", "-q,--quiet", "action=store_false", "dest=verbose"),
    ("option", "-f,--file", "dest=filename", "metavar=FILE"),
    ("option", "-n,--count", "type=int", "default=i:1"),
    ("parse",),
    ("parse", "-v", "-f", "out.txt", "a", "b"),
    ("parse", "-vf", "x.tar", "-q"),
    ("parse", "-fv"),
    ("parse", "--file=y.tar", "--verb", "--qu"),
    ("parse", "--file=", "--count=3"),
    ("parse", "-n", "0x1f"),
    ("parse", "-n", "017"),
    ("parse", "-n0o17"),
    ("parse", "-n", "0b"),
    ("parse", "-n", "0b101"),
    ("parse", "-n", "09"),
    ("parse", "-n", " 1_000 "),
    ("parse", "-n", "-12"),
    ("parse", "-n", "+0x10"),
    ("parse", "-n", "1__0"),
    ("parse", "-x"),
    ("parse", "-vx"),
    ("parse", "--fi"),
    ("parse", "--c", "2"),
    ("parse", "--zip"),
    ("parse", "--verbose=yes"),
    ("parse", "-f"),
    ("parse", "--file"),
    ("parse", "a", "--", "-v"),
    ("parse", "-", "-v", ""),
    ("parse", "--=a.tar"),
    ("parse", "--", "--"),
    )

job("actions",
    ("parser", "prog=build"),
    ("option", "-I,--include", "action=append", "dest=paths"),
    ("option", "--debug", "action=append_const", "const=s:debug", "dest=tags"),
    ("option", "--trace", "action=append_const", "const=s:trace", "dest=tags"),
    ("option", "-v", "action=count", "dest=verbosity"),
    ("option", "--fast", "action=store_const", "const=i:3", "dest=level"),
    ("option", "--slow", "action=store_const", "const=i:1", "dest=level"),
    ("option", "--plain", "action=store_const", "dest=level"),
    ("option", "--point", "type=float", "nargs=2"),
    ("option", "-D,--define", "action=append", "nargs=2", "metavar=KEY VALUE"),
    ("option", "--mode", "choices=l:fast,safe"),
    ("option", "--size", "type=long"),
    ("option", "-j", "type=int", "dest=jobs"),
    ("parse", "-I", "a", "-Ib", "--include=c", "-vvv", "--debug", "--trace", "--debug"),
    ("parse", "-v", "--fast", "-v", "--slow"),
    ("parse", "--fast", "--plain"),
    ("parse", "--point", "1.5", "2e3"),
    ("parse", "--point", "inf", "-1_0.5"),
    ("parse", "--point", " .5", "7."),
    ("parse", "--point", "nan", "-Infinity"),
    ("parse", "--point", "1e400", "1e-400"),
    ("parse", "--point", "0.1", "1_000.000_1"),
    ("parse", "--point", "1"),
    ("parse", "--point", "1", "x"),
    ("parse", "--point", "1_", "2"),
    ("parse", "--point", "1e", "2"),
    ("parse", "--point", "infinit", "2"),
    ("parse", "--point=3", "4"),
    ("parse", "-D", "cc", "clang", "-Dld", "lld", "-D", "x"),
    ("parse", "--mode", "slow"),
    ("parse", "--mo", "safe"),
    ("parse", "--mode=Safe"),
    ("parse", "--size", "-7", "-j", "08"),
    ("parse", "-j", "0x"),
    ("parse", "-j", "0_7"),
    ("help",),
    )

job("option errors",
    ("parser", "prog=lint"),
    ("option", "-"),
    ("option", "--"),
    ("option", "-ab"),
    ("option", "-a,---b"),
    ("option", "-a,--b,c"),
    ("option", "-a,--b", "action=storee"),
    ("option", "-c", "type=bogus"),
    ("option", "-c", "type=str"),
    ("option", "-d", "action=store_true", "type=int"),
    ("option", "-e", "type=choice"),
    ("option", "-e", "type=choice", "choices=s:abc"),
    ("option", "-e", "type=int", "choices=l:a"),
    ("option", "-e", "choices=l:a,b", "action=count"),
    ("option", "-g", "action=store_true", "const=i:1"),
    ("option", "-g", "action=count", "nargs=2"),
    ("option", "-g", "action=help", "type=int"),
    ("option", "-k", "action=callback", "callback=nosuch"),
    ("option", "-k", "callback=nosuch"),
    ("option", "-m", "colour=red", "size=2", "action=store_true"),
    ("option", "-m", "action=store_const"),
    ("option", "-p,--pid-file"),
    ("option", "-P,--pid-file"),
    ("option", "-h,--host"),
    ("option", "--x-y-z", "action=callback", "callback=csv", "type=string"),
    ("option", "--w", "action=callback", "callback=csv"),
    ("option", "-r", "action=version"),
    ("parse", "-r"),
    ("defaults",),
    )

job("conflict resolve",
    ("parser", "prog=deploy", "conflict=resolve", "version=%prog 1.0"),
    ("option", "-f,--file", "help=file to deploy"),
    ("option", "-f,--force", "action=store_true", "help=skip the checks"),
    ("option", "--file", "action=store_true", "dest=file2", "help=never shown"),
    ("option", "-h,--host", "default=s:localhost", "help=target host [default: %default]"),
    ("option", "--version", "action=store_true", "help=print the release"),
    ("help",),
    ("defaults",),
    ("parse", "-f", "--file", "-h", "web1"),
    ("parse", "--help"),
    ("has", "--force"),
    ("remove", "--force"),
    ("has", "--force"),
    ("has", "-f"),
    ("remove", "--nope"),
    ("parse", "-f"),
    ("usage",),
    ("version",),
    )

job("callbacks",
    ("parser", "prog=etl"),
    ("option", "--tags", "action=callback", "type=string", "callback=csv", "help=comma separated"),
    ("option", "-V,--values", "action=callback", "callback=vararg", "dest=vals"),
    ("option", "-a", "action=callback", "callback=check_order"),
    ("option", "-b", "action=store_true"),
    ("option", "--note", "action=callback", "callback=record", "type=string"),
    ("option", "--pair", "action=callback", "callback=record", "type=int", "nargs=2"),
    ("option", "--flag", "action=callback", "callback=record"),
    ("parse", "--tags", "a,b,,c", "-V", "1", "-2", "3.5", "x", "-b", "y"),
    ("parse", "-V", "--tags", "q"),
    ("parse", "-V", "1e3", "-inf", "-nan", "--", "-x"),
    ("parse", "-V", "-1_0", "-x"),
    ("parse", "-a", "-b"),
    ("parse", "-b", "-a"),
    ("parse", "--note", "hi", "pos", "--note=there", "--flag", "--", "z"),
    ("parse", "--pair", "1", "2", "--pair", "3", "x"),
    ("parse", "--flag=1"),
    )

job("help screens",
    ("env", "COLUMNS"),
    ("parser", "prog=backup-tool", "usage=usage: %prog [options] SRC DEST", "version=%prog 2.4.1",
     "description=%prog copies a source tree to a destination, keeping a rotating set of dated snapshots and pruning the oldest ones once the set is full.",
     "epilog=Exit status is 0 on success and 2 on a usage error. Report bugs to the operations team."),
    ("option", "-v,--verbose", "action=count", "help=print more detail; repeat for even more"),
    ("option", "-n,--dry-run", "action=store_true", "help=show what would be copied, but copy nothing"),
    ("option", "--keep", "type=int", "default=i:7", "metavar=N", "help=keep N snapshots [default: %default]"),
    ("option", "--compress", "choices=l:none,gzip,zstd", "default=s:zstd", "help=compression (%default by default; none, gzip or zstd)"),
    ("option", "--secret-debug", "action=store_true", "help=@SUPPRESS"),
    ("group", "Filtering", "These options decide which files are copied. They are applied in the order given."),
    ("option", "-x,--exclude", "action=append", "metavar=GLOB", "help=skip files that match GLOB"),
    ("option", "--max-size-in-bytes-per-file", "type=int", "metavar=BYTES", "help=skip larger files"),
    ("option", "--since", "help=only files changed since %default", "default=n:"),
    ("endgroup",),
    ("group", "Expert"),
    ("option", "--io-threads", "type=int", "default=s:4"),
    ("endgroup",),
    ("help",),
    ("parse", "--version"),
    ("parse", "--ver"),
    ("parse", "--compress", "lz4"),
    ("group_of", "--since"),
    ("group_of", "-v"),
    ("env", "COLUMNS=60"),
    ("parser", "prog=backup-tool", "usage=Usage: %prog SRC DEST", "formatter=titled", "description=Copies SRC to DEST."),
    ("option", "-v,--verbose", "action=count", "help=print more detail; repeat for even more"),
    ("option", "-o,--output", "metavar=PATH", "help=write the log to PATH instead of standard output"),
    ("group", "Filtering"),
    ("option", "-x,--exclude", "action=append", "metavar=GLOB", "help=skip files that match GLOB"),
    ("endgroup",),
    ("help",),
    ("parse", "-o"),
    ("env", "COLUMNS=abc"),
    ("parser", "usage=@SUPPRESS", "prog=quiet", "width=40", "max_help_position=10", "indent=4", "short_first=0"),
    ("option", "-o,--output", "metavar=PATH", "help=write the log to PATH instead of standard output"),
    ("option", "-l", "help=list"),
    ("help",),
    ("parse", "--bad"),
    ("usage",),
    ("parser", "prog=bare", "add_help=0", "description=   Leading  spaces   and trailing.   "),
    ("help",),
    ("parse", "-h"),
    )

job("defaults",
    ("parser", "prog=sync", "usage=%prog [options] [REMOTE]"),
    ("option", "-l,--level", "type=int"),
    ("option", "-r,--rate", "type=float", "default=s:1.5"),
    ("option", "-v", "action=store_true", "dest=verbose"),
    ("set_defaults", "verbose=b:1", "level=s:3", "extra=s:42"),
    ("option", "-q", "action=store_false", "dest=verbose"),
    ("option", "--label", "default=i:5"),
    ("defaults",),
    ("parse",),
    ("parse", "-l", "9", "-q"),
    ("set_defaults", "level=s:ten"),
    ("parse", "-l", "2"),
    ("set_defaults", "level=n:", "rate=f:2.0"),
    ("parse",),
    ("interspersed", "0"),
    ("parse", "-v", "commit", "-m", "msg"),
    ("parse", "--", "-v"),
    ("interspersed", "1"),
    ("parse", "-v", "commit", "-q", "msg"),
    )

backup_conf = """\
# backup.conf: defaults for backup-tool, one key = value per line
keep = 14
compress = gzip
exclude_from = /etc/backup/excludes
dry_run = no
bandwidth = 2.5
"""

backup_runs = [
    [],
    ["-vv", "/srv/www", "/mnt/backup/www"],
    ["--keep", "3", "--compress=none", "-x", "*.log", "-x*.tmp", "/home", "/mnt/backup/home"],
    ["-nq", "--bandwidth", "0x10", "/srv/db", "/mnt/backup/db"],
    ["--keep", "two", "/srv", "/mnt"],
    ["/srv/www"],
    ["--compress", "xz", "/srv", "/mnt"],
    ["--ke", "5", "--bw", "10", "/a", "/b"],
    ["--help"],
]

vcs_runs = [
    ["status"],
    ["-C", "/repo", "status", "-s"],
    ["--verbose", "commit", "-m", "fix the build", "-a"],
    ["commit", "-am", "two words", "--", "-notes.txt"],
    ["commit"],
    ["log", "-n", "3", "--oneline", "main..topic"],
    ["log", "-n", "three"],
    ["-v", "push", "--force", "origin", "main", "-v"],
    ["push", "--set-upstream", "origin"],
    ["checkout", "-b", "feature/x", "--track"],
    ["frobnicate"],
    ["--bogus", "status"],
    [],
    ["commit", "--help"],
    ["-C"],
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", newline="") as f:
    for line in jobs:
        f.write("\t".join(line) + "\n")
with open("data/backup.conf", "w", newline="") as f:
    f.write(backup_conf)
with open("data/backup_runs.tsv", "w", newline="") as f:
    for run in backup_runs:
        f.write("\t".join(["run"] + run) + "\n")
with open("data/vcs_runs.tsv", "w", newline="") as f:
    for run in vcs_runs:
        f.write("\t".join(["run"] + run) + "\n")
