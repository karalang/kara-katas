# Writes data/ for mini_docopt: the usage messages of the programs in
# docopt 0.6.2's examples/ directory (MIT, see README) and of some made-up
# tools, under data/docs/, and the jobs in data/jobs.jsonl: command lines
# to parse against a usage message, docopt's git example dispatching to
# its subcommands, a Naval Fate session, and small cases that test one
# rule each.
import json
import os
import shutil

D = "data"
if os.path.isdir(D):
    shutil.rmtree(D)
os.makedirs(os.path.join(D, "docs"))

# The docstrings of docopt 0.6.2's examples, unchanged.
EXAMPLES = {
    'quick':
        'Usage:\n  quick_example.py tcp <host> <port> [--timeout=<seconds>]\n  quick_example.py serial <port> [--baud=9600] [--timeout=<seconds>]\n  quick_example.py -h | --help | --version\n\n',
    'naval_fate':
        'Naval Fate.\n\nUsage:\n  naval_fate.py ship new <name>...\n  naval_fate.py ship <name> move <x> <y> [--speed=<kn>]\n  naval_fate.py ship shoot <x> <y>\n  naval_fate.py mine (set|remove) <x> <y> [--moored|--drifting]\n  naval_fate.py -h | --help\n  naval_fate.py --version\n\nOptions:\n  -h --help     Show this screen.\n  --version     Show version.\n  --speed=<kn>  Speed in knots [default: 10].\n  --moored      Moored (anchored) mine.\n  --drifting    Drifting mine.\n\n',
    'arguments':
        'Usage: arguments_example.py [-vqrh] [FILE] ...\n          arguments_example.py (--left | --right) CORRECTION FILE\n\nProcess FILE and optionally apply correction to either left-hand side or\nright-hand side.\n\nArguments:\n  FILE        optional input file\n  CORRECTION  correction angle, needs FILE, --left or --right to be present\n\nOptions:\n  -h --help\n  -v       verbose mode\n  -q       quiet mode\n  -r       make report\n  --left   use left-hand side\n  --right  use right-hand side\n\n',
    'calculator':
        "Not a serious example.\n\nUsage:\n  calculator_example.py <value> ( ( + | - | * | / ) <value> )...\n  calculator_example.py <function> <value> [( , <value> )]...\n  calculator_example.py (-h | --help)\n\nExamples:\n  calculator_example.py 1 + 2 + 3 + 4 + 5\n  calculator_example.py 1 + 2 '*' 3 / 4 - 5    # note quotes around '*'\n  calculator_example.py sum 10 , 20 , 30 , 40\n\nOptions:\n  -h, --help\n\n",
    'counted':
        'Usage: counted_example.py --help\n       counted_example.py -v...\n       counted_example.py go [go]\n       counted_example.py (--path=<path>)...\n       counted_example.py <file> <file>\n\nTry: counted_example.py -vvvvvvvvvv\n     counted_example.py go go\n     counted_example.py --path ./here --path ./there\n     counted_example.py this.txt that.txt\n\n',
    'odd_even':
        'Usage: odd_even_example.py [-h | --help] (ODD EVEN)...\n\nExample, try:\n  odd_even_example.py 1 2 3 4\n\nOptions:\n  -h, --help\n\n',
    'options':
        'Example of program with many options using docopt.\n\nUsage:\n  options_example.py [-hvqrf NAME] [--exclude=PATTERNS]\n                     [--select=ERRORS | --ignore=ERRORS] [--show-source]\n                     [--statistics] [--count] [--benchmark] PATH...\n  options_example.py (--doctest | --testsuite=DIR)\n  options_example.py --version\n\nArguments:\n  PATH  destination path\n\nOptions:\n  -h --help            show this help message and exit\n  --version            show version and exit\n  -v --verbose         print status messages\n  -q --quiet           report only file names\n  -r --repeat          show all occurrences of the same error\n  --exclude=PATTERNS   exclude files or directories which match these comma\n                       separated patterns [default: .svn,CVS,.bzr,.hg,.git]\n  -f NAME --file=NAME  when parsing directories, only check filenames matching\n                       these comma separated patterns [default: *.py]\n  --select=ERRORS      select errors and warnings (e.g. E,W6)\n  --ignore=ERRORS      skip errors and warnings (e.g. E4,W)\n  --show-source        show source code for each error\n  --statistics         count errors and warnings\n  --count              print total number of errors and warnings to standard\n                       error and set exit code to 1 if total is not null\n  --benchmark          measure processing speed\n  --testsuite=DIR      run regression tests from dir\n  --doctest            run doctest on myself\n\n',
    'options_shortcut':
        'Example of program which uses [options] shortcut in pattern.\n\nUsage:\n  options_shortcut_example.py [options] <port>\n\nOptions:\n  -h --help                show this help message and exit\n  --version                show version and exit\n  -n, --number N           use N as a number\n  -t, --timeout TIMEOUT    set timeout TIMEOUT seconds\n  --apply                  apply changes to database\n  -q                       operate in quiet mode\n\n',
    'validation':
        'Usage: prog.py [--count=N] PATH FILE...\n\nArguments:\n  FILE     input file\n  PATH     out directory\n\nOptions:\n  --count=N   number of operations\n\n',
    'git':
        "\nusage: git [--version] [--exec-path=<path>] [--html-path]\n           [-p|--paginate|--no-pager] [--no-replace-objects]\n           [--bare] [--git-dir=<path>] [--work-tree=<path>]\n           [-c name=value]\n           <command> [<args>...]\n       git [--help]\n\nThe most commonly used git commands are:\n   add        Add file contents to the index\n   branch     List, create, or delete branches\n   checkout   Checkout a branch or paths to the working tree\n   clone      Clone a repository into a new directory\n   commit     Record changes to the repository\n   push       Update remote refs along with associated objects\n   remote     Manage set of tracked repositories\n\nSee 'git help <command>' for more information on a specific command.\n\n",
    'git_add':
        "usage: git add [options] [--] [<filepattern>...]\n\n    -h, --help\n    -n, --dry-run        dry run\n    -v, --verbose        be verbose\n\n    -i, --interactive    interactive picking\n    -p, --patch          select hunks interactively\n    -e, --edit           edit current diff and apply\n    -f, --force          allow adding otherwise ignored files\n    -u, --update         update tracked files\n    -N, --intent-to-add  record only the fact that the path will be added later\n    -A, --all            add all, noticing removal of tracked files\n    --refresh            don't add, only refresh the index\n    --ignore-errors      just skip files which cannot be added because of errors\n    --ignore-missing     check if - even missing - files are ignored in dry run\n\n",
    'git_branch':
        "\nusage: git branch [options] [-r | -a] [--merged=<commit> | --no-merged=<commit>]\n       git branch [options] [-l] [-f] <branchname> [<start-point>]\n       git branch [options] [-r] (-d | -D) <branchname>\n       git branch [options] (-m | -M) [<oldbranch>] <newbranch>\n\nGeneric options\n    -h, --help\n    -v, --verbose         show hash and subject, give twice for upstream branch\n    -t, --track           set up tracking mode (see git-pull(1))\n    --set-upstream        change upstream info\n    --color=<when>        use colored output\n    -r                    act on remote-tracking branches\n    --contains=<commit>   print only branches that contain the commit\n    --abbrev=<n>          use <n> digits to display SHA-1s\n\nSpecific git-branch actions:\n    -a                    list both remote-tracking and local branches\n    -d                    delete fully merged branch\n    -D                    delete branch (even if not merged)\n    -m                    move/rename a branch and its reflog\n    -M                    move/rename a branch, even if target exists\n    -l                    create the branch's reflog\n    -f, --force           force creation (when already exists)\n    --no-merged=<commit>  print only not merged branches\n    --merged=<commit>     print only merged branches\n\n",
    'git_checkout':
        'usage: git checkout [options] <branch>\n       git checkout [options] <branch> -- <file>...\n\n    -q, --quiet           suppress progress reporting\n    -b <branch>           create and checkout a new branch\n    -B <branch>           create/reset and checkout a branch\n    -l                    create reflog for new branch\n    -t, --track           set upstream info for new branch\n    --orphan <new branch>\n                          new unparented branch\n    -2, --ours            checkout our version for unmerged files\n    -3, --theirs          checkout their version for unmerged files\n    -f, --force           force checkout (throw away local modifications)\n    -m, --merge           perform a 3-way merge with the new branch\n    --conflict <style>    conflict style (merge or diff3)\n    -p, --patch           select hunks interactively\n\n',
    'git_clone':
        "usage: git clone [options] [--] <repo> [<dir>]\n\n    -v, --verbose         be more verbose\n    -q, --quiet           be more quiet\n    --progress            force progress reporting\n    -n, --no-checkout     don't create a checkout\n    --bare                create a bare repository\n    --mirror              create a mirror repository (implies bare)\n    -l, --local           to clone from a local repository\n    --no-hardlinks        don't use local hardlinks, always copy\n    -s, --shared          setup as shared repository\n    --recursive           initialize submodules in the clone\n    --recurse-submodules  initialize submodules in the clone\n    --template <template-directory>\n                          directory from which templates will be used\n    --reference <repo>    reference repository\n    -o, --origin <branch>\n                          use <branch> instead of 'origin' to track upstream\n    -b, --branch <branch>\n                          checkout <branch> instead of the remote's HEAD\n    -u, --upload-pack <path>\n                          path to git-upload-pack on the remote\n    --depth <depth>       create a shallow clone of that depth\n\n",
    'git_commit':
        'usage: git commit [options] [--] [<filepattern>...]\n\n    -h, --help\n    -q, --quiet           suppress summary after successful commit\n    -v, --verbose         show diff in commit message template\n\nCommit message options\n    -F, --file <file>     read message from file\n    --author <author>     override author for commit\n    --date <date>         override date for commit\n    -m, --message <message>\n                          commit message\n    -c, --reedit-message <commit>\n                          reuse and edit message from specified commit\n    -C, --reuse-message <commit>\n                          reuse message from specified commit\n    --fixup <commit>      use autosquash formatted message to fixup specified commit\n    --squash <commit>     use autosquash formatted message to squash specified commit\n    --reset-author        the commit is authored by me now\n                          (used with -C-c/--amend)\n    -s, --signoff         add Signed-off-by:\n    -t, --template <file>\n                          use specified template file\n    -e, --edit            force edit of commit\n    --cleanup <default>   how to strip spaces and #comments from message\n    --status              include status in commit message template\n\nCommit contents options\n    -a, --all             commit all changed files\n    -i, --include         add specified files to index for commit\n    --interactive         interactively add files\n    -o, --only            commit only specified files\n    -n, --no-verify       bypass pre-commit hook\n    --dry-run             show what would be committed\n    --short               show status concisely\n    --branch              show branch information\n    --porcelain           machine-readable output\n    -z, --null            terminate entries with NUL\n    --amend               amend previous commit\n    --no-post-rewrite     bypass post-rewrite hook\n    -u, --untracked-files=<mode>\n                          show untracked files, optional modes: all, normal, no.\n                          [default: all]\n\n',
    'git_push':
        "usage: git push [options] [<repository> [<refspec>...]]\n\n    -h, --help\n    -v, --verbose         be more verbose\n    -q, --quiet           be more quiet\n    --repo <repository>   repository\n    --all                 push all refs\n    --mirror              mirror all refs\n    --delete              delete refs\n    --tags                push tags (can't be used with --all or --mirror)\n    -n, --dry-run         dry run\n    --porcelain           machine-readable output\n    -f, --force           force updates\n    --thin                use thin pack\n    --receive-pack <receive-pack>\n                          receive pack program\n    --exec <receive-pack>\n                          receive pack program\n    -u, --set-upstream    set upstream for git pull/status\n    --progress            force progress reporting\n\n",
    'git_remote':
        '\nusage: git remote [-v | --verbose]\n       git remote add [-t <branch>] [-m <master>] [-f] [--mirror] <name> <url>\n       git remote rename <old> <new>\n       git remote rm <name>\n       git remote set-head <name> (-a | -d | <branch>)\n       git remote [-v | --verbose] show [-n] <name>\n       git remote prune [-n | --dry-run] <name>\n       git remote [-v | --verbose] update [-p | --prune] [(<group> | <remote>)...]\n       git remote set-branches <name> [--add] <branch>...\n       git remote set-url <name> <newurl> [<oldurl>]\n       git remote set-url --add <name> <newurl>\n       git remote set-url --delete <name> <url>\n\n    -v, --verbose         be verbose; must be placed before a subcommand\n\n',
}

# Usage messages of some made-up tools, written for this app.
MINE = {
    "docker_run": """Run a command in a new container.

Usage:
  docker run [options] [-e <kv>]... [-p <port>]... IMAGE [COMMAND] [ARG...]
  docker run (-h | --help)

Options:
  -h, --help                Show this screen.
  -d, --detach              Run container in background and print its ID.
  -e, --env=<kv>            Set an environment variable.
  -p, --publish=<port>      Publish a container's port [default: ].
  --name=<name>             Assign a name to the container.
  -i, --interactive         Keep STDIN open even if not attached.
  -t, --tty                 Allocate a pseudo-TTY.
  --rm                      Remove the container when it exits.
  -m, --memory=<bytes>      Memory limit [default: 0].
  -v, --volume=<vol>        Bind mount a volume.
  -w, --workdir=<dir>       Working directory inside the container.
  --restart=<policy>        Restart policy [DEFAULT: no].
""",
    "curl": """curl, a small subset.

Usage:
  curl [options] <url>...
  curl --version

Options:
  -X, --request=<method>     Request method to use [default: GET]
  -H, --header=<header>      Pass a custom header to the server
  -d, --data=<data>          HTTP POST data
  -o, --output=<file>        Write to file instead of stdout
  -s, --silent               Silent mode
  -v, --verbose              Make the operation more talkative
  -L, --location             Follow redirects
  --max-time=<seconds>       Maximum time allowed for the transfer [default: 30]
  -u, --user=<user:password> Server user and password
  --compressed               Request a compressed response
""",
    "ssh": """OpenSSH client, in docopt's words.

Usage:
  ssh [-46AaCNqT] [-v]... [-p <port>] [-i <identity>]... [-L <spec>]... [-o <option>]... <destination> [<command>...]
  ssh -V

Options:
  -4             Use IPv4 addresses only.
  -6             Use IPv6 addresses only.
  -A             Enable forwarding of the authentication agent.
  -a             Disable forwarding of the authentication agent.
  -C             Request compression of all data.
  -N             Do not execute a remote command.
  -q             Quiet mode.
  -T             Disable pseudo-terminal allocation.
  -v             Verbose mode; give it several times for more.
  -p <port>      Port to connect to on the remote host [default: 22].
  -i <identity>  Identity (private key) file.
  -L <spec>      Local port forwarding, [bind_address:]port:host:hostport.
  -o <option>    Options in the format used in the configuration file.
  -V             Display the version number and exit.
""",
    "tar": """Usage: tar (-c | -x | -t) [-vzjp] [-f ARCHIVE] [-C DIR] [--exclude=PATTERN]... [FILE...]
       tar --help

  -c             create a new archive
  -x             extract files from an archive
  -t             list the contents of an archive
  -v             verbosely list files processed
  -z             filter the archive through gzip
  -j             filter the archive through bzip2
  -p             preserve permissions
  -f ARCHIVE     use archive file ARCHIVE [default: -]
  -C DIR         change to directory DIR
  --exclude=PATTERN  exclude files matching PATTERN
  --help         give this help list
""",
    "kubectl_get": """Display one or many resources.

Usage:
  kubectl get <resource> [<name>...] [-n <namespace> | -A] [-o <format>] [-l <selector>] [-w] [--show-labels]
  kubectl get -h

Options:
  -n, --namespace=<namespace>  The namespace scope for this request [default: default].
  -A, --all-namespaces         List the requested object(s) across all namespaces.
  -o, --output=<format>        Output format, one of json|yaml|wide|name.
  -l, --selector=<selector>    Selector (label query) to filter on.
  -w, --watch                  After listing, watch for changes.
  --show-labels                Show all labels as the last column.
  -h, --help                   Help for get.
""",
    "pip": """pip, the top level.

Usage:
  pip [options] <command> [<args>...]

General Options:
  -h, --help          Show help.
  --isolated          Run pip in an isolated mode.
  -v, --verbose       Give more output.
  -q, --quiet         Give less output.
  --log=<path>        Path to a verbose appending log.
  --proxy=<proxy>     Specify a proxy in the form scheme://[user:passwd@]proxy.server:port.
  --timeout=<sec>     Set the socket timeout [default: 15].
""",
    "pip_install": """Usage:
  pip install [options] <requirement>...
  pip install [options] -r <file>...
  pip install [options] [-e] <path>...

Options:
  -r, --requirement <file>  Install from the given requirements file.
  -e, --editable            Install a project in editable mode.
  -U, --upgrade             Upgrade all specified packages.
  --user                    Install to the user install directory.
  --no-deps                 Don't install package dependencies.
  -t, --target <dir>        Install packages into <dir>.
  --index-url=<url>         Base URL of the package index [default: https://pypi.org/simple].
""",
    "backup": """backup -- snapshot directories to a repository.

USAGE:
    backup init <repo>
    backup snapshot <repo> <path>... [--tag=<tag>]... [--exclude=<glob>]... [--dry-run]
    backup restore <repo> <snapshot> [--target=<dir>] [--include=<glob>]...
    backup forget <repo> (--keep-last=<n> | --keep-daily=<n> | --keep-weekly=<n>)... [--prune]
    backup (ls | stats) <repo> [<snapshot>]
    backup --version

Options:
    --tag=<tag>          Tag the snapshot.
    --exclude=<glob>     Leave out matching files.
    --dry-run            Only say what would be done.
    --target=<dir>       Where to restore to [default: .].
    --include=<glob>     Restore only matching files.
    --keep-last=<n>      Keep the last n snapshots.
    --keep-daily=<n>     Keep one snapshot a day for n days.
    --keep-weekly=<n>    Keep one snapshot a week for n weeks.
    --prune              Delete data nothing refers to any more.
""",
}

docs = dict(EXAMPLES)
docs.update(MINE)
for name, doc in docs.items():
    with open(os.path.join(D, "docs", name + ".txt"), "w", encoding="utf-8") as f:
        f.write(doc)

jobs = []


def run(doc, argv, version=None, options_first=False, help=True):
    jobs.append(["docopt", doc, argv.split() if isinstance(argv, str) else argv,
                 {"version": version, "options_first": options_first, "help": help}])


# The examples, as their own scripts call docopt.
for a in ["tcp 127.0.0.1 80 --timeout=30", "serial COM3 --baud=115200", "serial /dev/ttyUSB0", "--version",
          "-h", "tcp localhost", "tcp h p --timeout", "serial p --baud 9600 --timeout 5", "--help --version"]:
    run("quick", a, version="0.1.1rc")
for a in ["ship new Guardian Defiant Enterprise", "ship Guardian move 10 50", "ship Guardian move 10 50 --speed=20",
          "ship Guardian move 1 2 --speed 5 --sp=6", "ship shoot 3 4", "mine set 10 20 --moored",
          "mine remove 1 1 --drifting", "mine set 1 1 --moored --drifting", "ship new", "--version", "--help", "-h",
          "ship Guardian move 1", "mine set 1 2 --moor", "mine set 1 2 --mo", "ship x move 1 2 --speed",
          "ship x move 1 2 --moored=yes", "ship x move 1 2 --unknown", "ship Guardian move -- -1 -2", "ship move 1 2"]:
    run("naval_fate", a, version="Naval Fate 2.0")
for a in ["-vqr file.txt", "-v a b c", "--left 5 FILE", "--right 7 x.txt", "--left 5", "--left --right 1 f",
          "", "-h", "-vvq x"]:
    run("arguments", a)
for a in ["1 + 2 + 3 + 4 + 5", "1 + 2 * 3 / 4 - 5", "sum 10 , 20 , 30 , 40", "sum 10 20", "1 +", "max 1",
          "1 + 2 x 3", "-h"]:
    run("calculator", a)
for a in ["--help", "-v", "-vvvvvvvvvv", "-v -v -vv", "go", "go go", "go go go", "--path ./here --path ./there",
          "--path=a", "this.txt that.txt", "only.txt", "--pa x", ""]:
    run("counted", a)
for a in ["1 2 3 4", "1 2 3", "-h", "a b", "--help 1 2"]:
    run("odd_even", a)
for a in ["-vq --exclude=x,y --select=E1 --show-source src", "--doctest", "--testsuite=tests", "--version",
          "-f '*.py' -r --count src lib", "-fNAME src", "--select=E --ignore=W src", "--file=x.py --stat --bench p",
          "--testsuite", "src --count --count", "-hv"]:
    run("options", a, version="1.0.0rc2")
for a in ["8080", "-n 5 -t 30 8080", "--number=5 --timeout=30 --apply -q 8080", "-qn5 80", "--apply", "--appl 80",
          "--number 1 --number 2 80", "-x 80", "--version"]:
    run("options_shortcut", a, version="1.0.0rc2")
for a in ["--count=5 out a b c", "out", "out a", "--count=x out a"]:
    run("validation", a)
for a in ["add -n -v file1 file2", "add --patch", "add -- -weird", "add -A", "add --all --dry", "add --ignore x",
          "add -i -p"]:
    run("git_add", a)
for a in ["branch", "branch -a", "branch -r --merged=main", "branch new-feature main", "branch -d old",
          "branch -D old -f", "branch -m old new", "branch -M new", "branch -vv --color=always",
          "branch --merged=a --no-merged=b", "branch -r -a", "branch --contains=HEAD~3 --abbrev=7"]:
    run("git_branch", a)
for a in ["checkout main", "checkout -b feature main", "checkout main -- a.txt b.txt", "checkout -q --orphan gh-pages main",
          "checkout --conflict diff3 -m main", "checkout -23 main", "checkout"]:
    run("git_checkout", a)
for a in ["clone https://example.com/r.git", "clone --depth 1 -b main https://example.com/r.git dir",
          "clone --bare --mirror -- src", "clone -vq --origin=up -u /bin/up src dst", "clone --recurs src",
          "clone --re src"]:
    run("git_clone", a)
for a in ["commit -m 'msg'", "commit -am fix", "commit --amend --no-edit", "commit -m a -m b", "commit -F msg.txt -- a b",
          "commit -u", "commit -uno", "commit --untracked-files=normal", "commit -C HEAD --reset-author", "commit -s -S"]:
    run("git_commit", a)
for a in ["push", "push origin main", "push -u origin feature", "push --tags --force origin", "push --delete origin old",
          "push --repo=up", "push -nv --porcelain origin a b c", "push --exec=/x origin"]:
    run("git_push", a)
for a in ["remote", "remote -v", "remote add -f origin https://example.com/r.git", "remote add -t main -m main up url",
          "remote rename a b", "remote rm a", "remote set-head origin -a", "remote set-head origin main",
          "remote -v show origin", "remote prune --dry-run origin", "remote update -p a b", "remote set-branches o a b",
          "remote set-url o new", "remote set-url --add o new", "remote set-url --delete o old", "remote set-url o"]:
    run("git_remote", a)

for a in ["-d --name web -p 80:80 -p 443:443 -e A=1 -e B=2 nginx", "-it --rm alpine sh -c 'echo hi'",
          "--memory=512m -v /data:/data -w /data postgres:16", "nginx", "-e A=1 -e B=2 -e C=3 img cmd a1 a2",
          "--restart=always redis", "-h", "--rm", "-dit busybox", "-p", "--name=x --name=y img",
          "--det img", "img --rm"]:
    run("docker_run", a)
for a in ["https://example.com", "-sSL https://a https://b", "-X POST -d '{}' -H 'Content-Type: x' https://api",
          "--request=PUT --data=a --max-time=5 u", "-u admin:secret https://x", "--user=a:b u", "-o out.html -L u",
          "--version", "--compress u", "--max u", "-v"]:
    run("curl", a, version="curl 8.5.0")
for a in ["host", "-v host", "-vvv -p 2222 user@host", "-i ~/.ssh/id_ed25519 -i k2 -L 8080:localhost:80 host uptime",
          "-46 host", "-NT -L 1:a:2 -L 3:b:4 host", "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null h",
          "-V", "-q host ls -la /tmp", "host -v", "-p", "-Cqp22 host"]:
    run("ssh", a)
for a in ["-cvzf backup.tar.gz src docs", "-xf a.tar -C /tmp", "-t", "-tvf a.tar", "-c -x f", "--exclude=*.o --exclude=*.a -cf x .",
          "-xjpf a.tar.bz2", "--help", "-cf", "-cfx", "-czf - ."]:
    run("tar", a)
for a in ["pods", "pods -A", "pods web-1 web-2 -n prod -o wide", "deploy -l app=web,tier!=db -w", "pods -n a -A",
          "svc --show-labels -o=yaml", "-h", "nodes --namespace=kube-system", "pods --all", "pods --s"]:
    run("kubectl_get", a)
for a in ["install requests", "-v install --upgrade requests", "--isolated --timeout=5 list --outdated",
          "install -r req.txt --user", "--log=/tmp/pip.log --proxy=http://proxy:3128 download x", "-h", "help install",
          "--verbose", "-vv install x"]:
    run("pip", a, options_first=True)
for a in ["install requests flask", "install -r requirements.txt -r dev.txt", "install -e .", "install -U --user x",
          "install --index-url=https://test.pypi.org/simple x", "install -t vendor --no-deps a b", "install -r", "install"]:
    run("pip_install", a)
for a in ["init /srv/repo", "snapshot /srv/repo /home /etc --tag=daily --tag=host1 --exclude=*.tmp",
          "snapshot /srv/repo /home --dry-run", "restore /srv/repo latest --target=/tmp/r --include=*.conf",
          "restore r s", "forget /srv/repo --keep-last=3 --keep-daily=7 --prune", "forget r --keep-weekly=4 --keep-weekly=8",
          "forget r", "ls r", "stats r snap1", "ls", "--version", "snapshot r", "restore r s --target"]:
    run("backup", a, version="backup 1.4.0")

# docopt's git example, which parses the top level with options_first and
# hands the rest to a subcommand.
for a in ["add -n file", "--bare -p branch -a", "--version", "-c user.name=x commit -m hi", "--git-dir=/r push origin",
          "checkout -b f", "clone src", "remote -v", "help", "--help", "frobnicate", "--no-pager status",
          "--exec-path=/x --html-path --work-tree=/w add -A", "-p", "", "branch -x"]:
    jobs.append(["git", a.split()])

# A Naval Fate session: each line is parsed and then carried out.
jobs.append(["naval", [
    "ship new Guardian Defiant Enterprise",
    "ship Guardian move 10 50",
    "ship Defiant move 10 50 --speed=20",
    "ship Enterprise move 3 4 --speed 12",
    "mine set 3 4 --moored",
    "mine set 7 7 --drifting",
    "mine set 8 8",
    "ship shoot 10 50",
    "ship Voyager move 1 1",
    "ship Enterprise move 7 7",
    "mine remove 3 4",
    "mine remove 0 0",
    "ship new Defiant Voyager",
    "ship shoot 7 7",
    "ship Voyager move 3 4 --speed=fast",
    "ship Guardian move 1",
    "--version",
    "ship shoot 3 4",
]])

# Small cases, each testing one rule.
CASES = [
    ("no usage", "Program that does things.\n", ""),
    ("two usages", "Usage: prog\n\nusage: prog other\n", ""),
    ("usage in prose", "Read the usage: notes.\n\nUsage: prog\n", ""),
    ("unmatched paren", "Usage: prog (a | b\n", "a"),
    ("unmatched bracket", "Usage: prog [a\n", "a"),
    ("unexpected ending", "Usage: prog a )\n", "a"),
    ("short twice", "Usage: prog -x\n\nOptions:\n  -x  one\n  -x  two\n", "-x"),
    ("flag given an argument", "Usage: prog --foo=<x>\n\nOptions:\n  --foo  a flag\n", "--foo=1"),
    ("option eats paren", "Usage: prog -o\n\nOptions:\n  -o FILE  output\n", "-o x"),
    ("long eats paren", "Usage: prog --out\n\nOptions:\n  --out=<f>  output\n", "--out x"),
    ("long in usage only", "Usage: prog --out=<f>\n", "--out=x"),
    ("long in usage, space", "Usage: prog --out <f>\n", "--out x"),
    ("options shortcut", "Usage: prog [options]\n\nOptions: -a  All.\n", ""),
    ("options shortcut set", "Usage: prog [options]\n\nOptions: -a  All.\n", "-a"),
    ("options shortcut unknown", "Usage: prog [options]\n\nOptions: -a  All.\n", "-x"),
    ("one-line options", "Usage: prog [options]\n\nOptions:\n  -a  All.\n  -b, --bee  Bees. [default: none]\n", "-ab"),
    ("default on flag", "Usage: prog [-q]\n\nOptions:\n  -q  quiet [default: yes]\n", ""),
    ("default case", "Usage: prog [--x=<v>]\n\nOptions:\n  --x=<v>  [DeFaUlT: 7]\n", ""),
    ("two defaults", "Usage: prog [--x=<v>]\n\nOptions:\n  --x=<v>  a [default: 1] or [default: 2]\n", ""),
    ("default runs on", "Usage: prog [--x=<v>]\n\nOptions:\n  --x=<v>  first line\n           [default: from line two]\n", ""),
    ("commands", "Usage: prog add | rm\n", "add"),
    ("commands other", "Usage: prog add | rm\n", "mv"),
    ("command case", "Usage: prog ADD | rm\n", "ADD"),
    ("argument forms", "Usage: prog <a> [B] [<c>...]\n", "1 2 3 4"),
    ("required repeat", "Usage: prog <f>...\n", ""),
    ("either options", "Usage: prog (--xx=X|--yy=Y)\n", "--xx=1"),
    ("either both", "Usage: prog (--xx=X|--yy=Y)\n", "--xx=1 --yy=2"),
    ("stacked arg", "Usage: prog [-v] [-o FILE]\n\nOptions:\n  -v\n  -o FILE\n", "-vofile"),
    ("stacked arg apart", "Usage: prog [-v] [-o FILE]\n\nOptions:\n  -v\n  -o FILE\n", "-vo file"),
    ("short needs arg", "Usage: prog [-o FILE]\n\nOptions:\n  -o FILE\n", "-o"),
    ("double dash", "Usage: prog [-o] [--] <arg>\n\nOptions: -o\n", "-- -o"),
    ("double dash only", "Usage: prog [-o] [--] <arg>\n\nOptions: -o\n", "-o --"),
    ("dash command", "Usage: prog [-]\n", "-"),
    ("upper arguments", "Usage: prog [NAME]...\n", "a b c"),
    ("upper with digits", "Usage: prog X1 Y_2\n", "a b"),
    ("not upper", "Usage: prog x1 y_2\n", "x1 y_2"),
    ("options first", "Usage: prog [--opt] [<args>...]\n", "this --opt"),
    ("options before", "Usage: prog [--opt] [<args>...]\n", "--opt this that"),
    ("prefix unique", "Usage: prog [--version] [--verbose]\n", "--verb"),
    ("prefix ambiguous", "Usage: prog [--version] [--verbose]\n", "--ver"),
    ("exact beats prefix", "Usage: prog [--ver] [--verbose]\n", "--ver"),
    ("count -v", "Usage: prog -v...\n", "-vvvv -v"),
    ("count both forms", "Usage: prog [-v | -vv | -vvv]\n", "-vv"),
    ("count none", "Usage: prog [-v]...\n", ""),
    ("repeated command", "Usage: prog (go | stop)...\n", "go go stop go"),
    ("either repeat", "Usage: prog (a <x> | b <x>)...\n", "a 1 b 2 a 3"),
    ("either repeat 2", "Usage: prog (a <x> | b <y>)...\n", "a 1 b 2 a 3"),
    ("argument list default", "Usage: prog [-o <o>]...\n\nOptions: -o <o>  [default: x y]\n", ""),
    ("argument list given", "Usage: prog [-o <o>]...\n\nOptions: -o <o>  [default: x y]\n", "-o a -o b"),
    ("long equals empty", "Usage: prog [--opt=<v>]\n", "--opt="),
    ("unknown long equals", "Usage: prog [options]\n", "--zip=3"),
    ("help disabled", "Usage: prog [-h]\n\nOptions: -h  help\n", "-h", {"help": False}),
    ("help unknown", "Usage: prog <x>\n", "--help"),
    ("help after error", "Usage: prog <x>\n", "--he"),
    ("version disabled", "Usage: prog [--version]\n", "--version"),
    ("tabs in options", "Usage: prog [options]\n\nOptions:\n\t-a\tAll\n  -b  Bees\n", "-a"),
    ("unicode", "Usage: prog <ünï> [--café=<x>]\n", "ö --café=b"),
    ("blank line with spaces", "Usage: prog a\n   \n  prog b\n", "b"),
    ("usage continues", "Usage: prog a\n  prog b\nOther text\n\n", "b"),
    ("ellipsis glued", "Usage: prog <a>...<b>\n", "1 2 3"),
    ("pipes glued", "Usage: prog (a|b|c)[d]\n", "c d"),
    ("option shadowing arg", "Usage: prog [-a] <x>\n\nOptions: -a  all\n", "-- -a"),
    ("command after args", "Usage: prog <x> add\n", "add add"),
    ("negative number", "Usage: prog <n>\n", "-5"),
    ("lone dash dash in usage", "Usage: prog --\n", "--"),
    ("bracket default arg", "Usage: prog [<a>]\n\nArguments:\n  <a>  thing [default: 3]\n", ""),
    ("Usage word inside", "Program usage:\n  prog go\n", "go"),
    ("repeated option arg", "Usage: prog --path=<p> --path=<p>\n", "--path=a --path=b"),
    ("repeated flag", "Usage: prog -v -v\n", "-v -v"),
    ("repeated flag once", "Usage: prog -v -v\n", "-v"),
]
for c in CASES:
    label, doc, argv = c[0], c[1], c[2]
    extra = c[3] if len(c) > 3 else {}
    jobs.append(["case", label, doc, argv.split(),
                 {"version": extra.get("version"), "options_first": label.startswith("options first"),
                  "help": extra.get("help", True)}])

with open(os.path.join(D, "jobs.jsonl"), "w", encoding="utf-8") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
print("%d jobs" % len(jobs))
