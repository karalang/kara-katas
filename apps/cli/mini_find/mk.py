# The inputs of mini_find: the tree it builds and the find commands it
# runs. Run as a script, it writes them into data/; mini_find.py, real.py
# and gen_kara.py import FILES.
import os

FILES = {}

# One entry per line: a directory, a file of a given size, or a link.
#   d MODE MTIME PATH
#   f MODE MTIME SIZE PATH
#   l TARGET PATH
# Paths are under data/proj; times are UTC.
FILES["manifest.txt"] = """d 0755 2026-10-14T08:00:00 .
f 0644 2026-10-14T07:59:00 1210 README.md
f 0644 2026-10-10T10:00:00 388 Makefile
f 0644 2026-10-15T11:58:30 96 space name.txt
d 0755 2026-10-13T18:00:00 src
f 0644 2026-10-13T17:45:10 734 src/main.c
f 0644 2026-10-12T09:00:00 2049 src/util.c
f 0644 2026-10-01T09:00:00 512 src/util.h
f 0444 2026-10-14T23:30:00 513 src/Version.h
d 0700 2026-09-01T00:00:00 src/old
f 0600 2026-08-15T06:15:00 4100 src/old/legacy.c
d 0755 2026-10-15T11:30:00 build
f 0755 2026-10-15T11:29:59 5321 build/app
f 0644 2026-10-15T11:29:40 1900 build/main.o
f 0644 2026-10-15T11:29:41 2600 build/util.o
d 0755 2026-10-15T11:20:00 build/cache
d 0755 2026-10-11T12:00:00 docs
f 0644 2026-10-11T11:59:00 3075 docs/guide.txt
f 0444 2026-10-02T16:20:00 640 docs/notes.TXT
f 0644 2026-10-11T12:00:00 0 docs/Empty.txt
d 0755 2026-10-03T08:00:00 docs/img
f 0644 2026-10-03T07:55:00 2100 docs/img/logo.png
f 0644 2026-10-03T07:56:00 1048577 docs/img/photo.png
d 0755 2026-10-09T14:00:00 scripts
f 4755 2026-10-09T13:00:00 220 scripts/deploy.sh
f 0750 2026-10-09T14:00:00 150 scripts/test.sh
d 0755 2026-10-14T08:00:00 .git
f 0644 2026-10-14T08:00:00 23 .git/HEAD
f 0644 2026-09-20T10:00:00 180 .git/config
d 0755 2026-10-14T08:00:00 .git/refs
d 1777 2026-10-15T09:00:00 tmp
f 0666 2026-10-15T08:59:00 10 tmp/a.tmp
f 0666 2026-10-15T09:00:00 0 tmp/b.tmp
l build/app latest
l docs docs-link
l missing.txt broken
l ../README.md src/readme-link
"""

FILES["jobs.txt"] = r"""# Listing the tree.
find data/proj
find data/proj -maxdepth 1
find data/proj/src/ -maxdepth 1
find data/proj//docs -maxdepth 1 -name img
find data/proj/src data/proj/docs -maxdepth 0
find data/proj/missing data/proj/Makefile
find data/proj -mindepth 2 -maxdepth 2 -type d
find data/proj -depth -type d
# Names and paths.
find data/proj -name '*.c'
find data/proj -iname '*.txt'
find data/proj -name '[A-Z]*'
find data/proj -name '[!a-z]*' -maxdepth 1
find data/proj -name '*[0-9]*' -o -name '\.*'
find data/proj -name 'space name.txt' -o -name '*\**'
find data/proj -path '*/src/*' -name '*.h'
find data/proj -ipath '*/DOCS/*.png'
find data/proj -wholename 'data/proj/b*'
find data/proj -lname '*.md'
find data/proj -ilname 'DOC*'
# Types and links.
find data/proj -type d
find data/proj -type l -printf '%p -> %l\n'
find data/proj -type f,l -name '*e*'
find data/proj -xtype l
find data/proj -xtype d
find -L data/proj -type l
find -L data/proj -name '*.png'
find -L data/proj -maxdepth 1 -printf '%y%Y %p\n'
find data/proj -maxdepth 1 -printf '%y%Y %p\n'
find -H data/proj/docs-link -name '*.png'
find data/proj/docs-link -name '*.png'
# Sizes.
find data/proj -type f -size +2k -printf '%s %p\n'
find data/proj -type f -size -1k
find data/proj -type f -size 1
find data/proj -type f -size 2 -o -type f -size 1M
find data/proj -type f -size +1M
find data/proj -type f -size -600c -size +100c -printf '%6s %f\n'
find data/proj -type f -size 3075c
find data/proj -empty
find data/proj -empty -type f
# Modes.
find data/proj -perm -4000
find data/proj -perm /o+w
find data/proj -type f -perm 644 -name '*.h'
find data/proj -type f -perm -u=x
find data/proj -perm /1000
find data/proj -type f ! -perm -u=w
find data/proj -perm -g=s,u=s -o -perm -1777
find data/proj -type f -perm /g=w,o=w -printf '%m %M %p\n'
# Times; now is 2026-10-15 12:00:00 UTC.
find data/proj -type f -mtime 0
find data/proj -type f -mtime -2 -mtime +0
find data/proj -type f -mtime +30
find data/proj -type f -mmin -60
find data/proj -type f -mmin +30 -mmin -46
find data/proj -type f -mmin 31
find data/proj -type f -newer data/proj/src/util.c
find data/proj ! -type l -newermt '2026-10-13 18:00'
find data/proj -type f -newermt 2026-10-14 ! -newermt '2026-10-15 09:00:00'
find data/proj -daystart -type f -mtime 0
find data/proj -daystart -type f -mtime 1
find data/proj/docs -type f -printf '%-12f|%6s|%TY-%Tm-%Td %TH:%TM|%t\n'
find data/proj/src -type f -printf '%T@ %Tj %Ta %Tb %TD %TF %Tk %Tr %TT %TS %f\n'
# Operators and actions.
find data/proj \( -name '*.c' -o -name '*.h' \) -printf '%f\n'
find data/proj -name .git -prune -o -type f -print
find data/proj -name .git -prune -o -name build -prune -o -name '*.o' -print
find data/proj -type d \( -name .git -o -name tmp \) -prune -o -type d -print
find data/proj -name '*.md' , -name '*.sh' -printf 'script %f\n'
find data/proj -type f -name '*.c' -print -quit
find data/proj -false -o -name Makefile
find data/proj -not -type d -not -type f
find data/proj ! \( -type d -o -name '*.*' \)
find data/proj -name '*.o' -a -true
find data/proj -maxdepth 1 -name 'M*' -printf 'one %f\n' -printf 'two %f\n'
find data/proj/src -printf '%d %y %m %M %f %h %P\n'
find data/proj/scripts -type f -printf '[%-10f][%5d][%.4f][%-6m][%3s]\n'
find data/proj/tmp -printf '%p\t%m\\%%\101\n'
find data/proj/tmp -printf '%f\c ignored\n'
find data/proj -maxdepth 0 -printf 'x\qy %j\n'
# Deleting.
find data/proj/build -name '*.o' -delete -print
find data/proj/build
find data/proj/tmp -type f -delete
find data/proj/src -name old -delete
find data/proj/docs/img -delete
find data/proj/docs -maxdepth 1
reset
find data/proj/build -maxdepth 1 -name '*.o'
# Mistakes.
find data/proj -foo
find data/proj -name
find data/proj -name a extra
find data/proj -type q
find data/proj -type f,
find data/proj -size 3q
find data/proj -size +1.5k
find data/proj -perm abc
find data/proj -maxdepth x
find data/proj -mindepth -1
find data/proj -mtime x
find data/proj -newermt garbage
find data/proj -newer data/proj/nope
find data/proj \(
find data/proj -name x \)
find data/proj \( \)
find data/proj !
find data/proj -o -name x
find data/proj -name a -o
find data/proj -delete -prune
find data/proj -printf 'oops %'
"""


def write_all():
    os.makedirs("data", exist_ok=True)
    for name, text in FILES.items():
        open(os.path.join("data", name), "w").write(text)


if __name__ == "__main__":
    write_all()
