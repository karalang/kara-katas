# Writes data/ (the input files) and jobs.tsv: one shell pipeline per
# line, its arguments tab-separated (a tab inside one written as a
# vertical tab) and its stages separated by a `|` argument.
import os
os.makedirs("data", exist_ok=True)
def w(name, text):
    open("data/" + name, "w").write(text)

w("passwd", """\
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
postgres:x:105:112:PostgreSQL administrator,,,:/var/lib/postgresql:/bin/bash
alice:x:1000:1000:Alice Liddell,,,:/home/alice:/bin/zsh
bob:x:1001:1001:Bob Builder:/home/bob:/bin/bash
deploy:x:1002:1002::/home/deploy:/bin/sh
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
""")

w("access.log", """\
10.0.12.7 - - [14/Oct/2026:09:12:01 +0000] "GET /api/orders HTTP/1.1" 200 1532
10.0.12.7 - - [14/Oct/2026:09:12:03 +0000] "POST /api/orders HTTP/1.1" 201 88
192.168.4.21 - alice [14/Oct/2026:09:13:44 +0000] "GET /static/app.js HTTP/2.0" 304 0
172.16.0.9 - - [14/Oct/2026:09:14:10 +0000] "GET /api/products/991 HTTP/1.1" 404 47
172.16.0.9 - - [14/Oct/2026:09:14:11 +0000] "GET /api/products/992 HTTP/1.1" 404 47
10.0.12.8 - - [14/Oct/2026:09:15:00 +0000] "POST /api/checkout HTTP/1.1" 502 166
192.168.4.21 - alice [14/Oct/2026:09:15:02 +0000] "DELETE /api/cart/7 HTTP/2.0" 204 0
10.0.12.8 - - [14/Oct/2026:09:15:31 +0000] "POST /api/checkout HTTP/1.1" 503 166
10.0.12.7 - - [14/Oct/2026:09:16:45 +0000] "GET /healthz HTTP/1.1" 200 2
10.0.12.10 - - [14/Oct/2026:09:17:02 +0000] "GET /api/orders HTTP/1.1" 200 1490
""")

w("inventory.csv", """\
sku,name,warehouse,qty,price
A-100,widget,berlin,120,2.50
A-101,widget large,berlin,8,4.75
B-200,gadget,lisbon,35,19.99
B-201,gadget pro,berlin,3,49.00
C-300,sprocket,lisbon,1000,0.33
C-301,sprocket,oslo,250,0.33
D-400,doohickey,oslo,0,12.00
""")

w("du.txt", """\
4.0K\t./etc
1.2G\t./var/lib/postgresql
512M\t./var/log
88K\t./home/deploy
2.5G\t./srv/media
900M\t./opt/app
16K\t./tmp
1.2G\t./home/alice
""")

w("sizes.txt", """\
1532 orders.json
88 receipt.txt
0 empty.log
1048576 dump-1.bin
1536 thumb.png
734003200 backup.tar
15728640 video.mp4
1025 notes.md
999999 almost.bin
""")

w("words.txt", """\
the quick brown fox jumps over the lazy dog
The Lazy Dog sleeps; the fox does not.
  indented line with   extra   spaces
Zebra apple Mango banana cherry

end of file
""")

w("hosts-a.txt", "app-1\napp-2\ncache-1\ndb-primary\nlb-1\nworker-3\n")
w("hosts-b.txt", "app-2\napp-3\ncache-1\ndb-replica\nlb-1\nworker-1\nworker-3\n")
w("names.tsv", "u1\tAlice\nu2\tBob\nu3\tCarol\nu5\tEve\n")
w("orders.tsv", "u1\to-100\t30.00\nu1\to-104\t12.50\nu2\to-101\t7.25\nu4\to-102\t100.00\nu5\to-103\t4.75\n")
w("unsorted.tsv", "u2\tBob\nu1\tAlice\n")
w("dups.txt", "error: disk full\nerror: disk full\nwarn: slow query\nerror: disk full\nERROR: Disk Full\ninfo: started\ninfo: started\ninfo: started\nwarn: slow query\n")
w("versions.txt", "1.10.0 2026-09-30\n1.2.0 2026-03-01\n1.9.3 2026-08-15\n10.0.0 2026-10-10\n1.9.10 2026-09-01\n")
w("mixed.txt", "10\n9\n-3\n  42\n3.5\nabc\n007\n-0.5\n1e3\n\n+5\n")
w("ids.txt", "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n")
w("noeol.txt", "first\nsecond\nthird")
w("cols.txt", "name\tage\tcity\nann\t31\tlisbon\nbo\t4\toslo\n")

jobs = []
def j(*stages):
    out = []
    for i, s in enumerate(stages):
        if i:
            out.append("|")
        out += s
    jobs.append("\t".join(out))

# sort
j(["sort", "hosts-b.txt"])
j(["sort", "-r", "words.txt"])
j(["sort", "-t:", "-k3,3n", "passwd"], ["cut", "-d:", "-f1,3"])
j(["sort", "-t:", "-k7,7", "-k1,1r", "passwd"], ["cut", "-d:", "-f1,7"])
j(["sort", "-n", "mixed.txt"])
j(["sort", "-rn", "sizes.txt"], ["head", "-n", "3"])
j(["sort", "-h", "-r", "du.txt"])
j(["sort", "-k2", "versions.txt"])
j(["sort", "-t,", "-k3,3", "-k4,4nr", "inventory.csv"])
j(["sort", "-f", "words.txt"])
j(["sort", "-u", "dups.txt"])
j(["sort", "-uf", "dups.txt"])
j(["sort", "-t,", "-k5,5n", "-s", "inventory.csv"])
j(["sort", "-b", "-k2,2", "words.txt"])
j(["sort", "-k1.2,1.4", "hosts-a.txt"])
j(["sort", "-c", "hosts-b.txt"])
j(["sort", "-c", "versions.txt"])
j(["sort", "-m", "hosts-a.txt", "hosts-b.txt"])
# cut
j(["cut", "-d:", "-f1,6", "passwd"])
j(["cut", "-d:", "-f5-", "passwd"])
j(["cut", "-d,", "-f2,4", "--output-delimiter= | ", "inventory.csv"])
j(["cut", "-c1-8,30-", "access.log"])
j(["cut", "-d", " ", "-f1", "access.log"], ["sort"], ["uniq", "-c"], ["sort", "-rn"])
j(["cut", "-d:", "-f1", "--complement", "passwd"])
j(["cut", "-d,", "-s", "-f1", "words.txt"])
j(["cut", "-f2", "cols.txt"])
j(["cut", "-d:", "passwd"])
j(["cut", "-f", "0", "cols.txt"])
# uniq
j(["uniq", "dups.txt"])
j(["sort", "dups.txt"], ["uniq", "-c"])
j(["sort", "dups.txt"], ["uniq", "-d"])
j(["sort", "dups.txt"], ["uniq", "-u"])
j(["sort", "-f", "dups.txt"], ["uniq", "-ci"])
j(["uniq", "-f", "1", "-c", "dups.txt"])
j(["uniq", "-s", "6", "dups.txt"])
# tr
j(["cat", "words.txt"], ["tr", "a-z", "A-Z"])
j(["cat", "words.txt"], ["tr", "-s", " "])
j(["cat", "words.txt"], ["tr", "-d", "aeiou"])
j(["cat", "words.txt"], ["tr", "-cs", "[:alpha:]", "\\n"], ["tr", "[:upper:]", "[:lower:]"], ["sort"], ["uniq", "-c"], ["sort", "-k1,1nr", "-k2,2"], ["head", "-n", "5"])
j(["cat", "passwd"], ["tr", ":", "\\t"], ["head", "-n", "2"])
j(["cat", "inventory.csv"], ["tr", "-d", "\\r"], ["tr", ",", ";"])
j(["cat", "words.txt"], ["tr", "abc", "x"])
j(["cat", "words.txt"], ["tr", "-ds", "a-z", " "])
j(["cat", "noeol.txt"], ["tr", "\\n", ","])
j(["tr", "a-z"])
j(["tr", "z-a", "x"])
# wc
j(["wc", "words.txt"])
j(["wc", "-l", "passwd", "access.log", "noeol.txt"])
j(["cat", "words.txt"], ["wc", "-w"])
j(["wc", "-c", "-l", "noeol.txt"])
j(["cat", "access.log"], ["wc"])
j(["wc", "missing.txt", "passwd"])
# head and tail
j(["head", "-n", "2", "passwd", "noeol.txt"])
j(["head", "-n", "-9", "ids.txt"])
j(["head", "-c", "20", "access.log"])
j(["tail", "-n", "3", "ids.txt"])
j(["tail", "-n", "+11", "ids.txt"])
j(["tail", "-n", "1", "noeol.txt"])
j(["tail", "-c", "7", "noeol.txt"])
j(["head", "-n", "x", "ids.txt"])
# join and comm
j(["join", "-t", "\v", "names.tsv", "orders.tsv"])
j(["join", "-t", "\v", "-a", "1", "-a", "2", "-e", "NONE", "-o", "0,1.2,2.2,2.3", "names.tsv", "orders.tsv"])
j(["join", "-t", "\v", "-v", "2", "names.tsv", "orders.tsv"])
j(["join", "-t", "\v", "-1", "1", "-2", "1", "-o", "2.2,1.2", "orders.tsv", "names.tsv"])
j(["join", "-t", "\v", "unsorted.tsv", "orders.tsv"])
j(["comm", "hosts-a.txt", "hosts-b.txt"])
j(["comm", "-12", "hosts-a.txt", "hosts-b.txt"])
j(["comm", "-3", "hosts-a.txt", "hosts-b.txt"])
j(["comm", "-23", "hosts-a.txt", "hosts-b.txt"])
# paste, nl, tac, numfmt
j(["paste", "hosts-a.txt", "hosts-b.txt"])
j(["paste", "-d,", "-s", "hosts-a.txt"])
j(["paste", "-d", ":-", "ids.txt", "hosts-a.txt", "hosts-b.txt"])
j(["cut", "-d:", "-f1", "passwd"], ["paste", "-s", "-d", " "])
j(["nl", "words.txt"])
j(["nl", "-b", "a", "-n", "rz", "-w", "3", "-s", ". ", "hosts-a.txt"])
j(["tac", "noeol.txt"])
j(["tac", "hosts-a.txt"])
j(["cat", "sizes.txt"], ["numfmt", "--to=iec", "--field=1"])
j(["cat", "sizes.txt"], ["numfmt", "--to=si", "--suffix=B", "--field=1", "--padding=6"])
j(["numfmt", "--from=iec", "1K", "2.5M", "1G", "512"])
j(["cut", "-f1", "du.txt"], ["numfmt", "--from=iec"], ["paste", "-sd+"])
j(["numfmt", "--to=iec", "--padding=8", "1023", "1024", "1536", "10240", "1048575"])
j(["numfmt", "abc"])
open("jobs.tsv", "w").write("\n".join(jobs) + "\n")
