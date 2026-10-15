# Writes data/ (the input files) and jobs.tsv (one awk run per line:
# tab-separated arguments, a newline inside one written as a vertical
# tab; a line starting with @cat shows a file).
import os
os.makedirs("data", exist_ok=True)
def w(name, text):
    open("data/" + name, "w").write(text)

w("access.log", """\
10.0.12.7 - - [14/Oct/2026:09:12:01 +0000] "GET /api/orders?page=2 HTTP/1.1" 200 1532 "-" "curl/8.5.0" 0.042
10.0.12.7 - - [14/Oct/2026:09:12:03 +0000] "POST /api/orders HTTP/1.1" 201 88 "-" "curl/8.5.0" 0.130
192.168.4.21 - alice [14/Oct/2026:09:13:44 +0000] "GET /static/app.js HTTP/2.0" 304 0 "https://shop.example.com/" "Mozilla/5.0" 0.003
172.16.0.9 - - [14/Oct/2026:09:14:10 +0000] "GET /api/products/991 HTTP/1.1" 404 47 "-" "python-requests/2.32" 0.011
172.16.0.9 - - [14/Oct/2026:09:14:11 +0000] "GET /api/products/992 HTTP/1.1" 404 47 "-" "python-requests/2.32" 0.009
10.0.12.8 - - [14/Oct/2026:09:15:00 +0000] "POST /api/checkout HTTP/1.1" 502 166 "-" "okhttp/4.12" 2.501
192.168.4.21 - alice [14/Oct/2026:09:15:02 +0000] "DELETE /api/cart/7 HTTP/2.0" 204 0 "https://shop.example.com/cart" "Mozilla/5.0" 0.027
10.0.12.8 - - [14/Oct/2026:09:15:31 +0000] "POST /api/checkout HTTP/1.1" 503 166 "-" "okhttp/4.12" 5.000
10.0.12.7 - - [14/Oct/2026:09:16:45 +0000] "GET /healthz HTTP/1.1" 200 2 "-" "kube-probe/1.31" 0.001
10.0.12.7 - - [14/Oct/2026:09:17:02 +0000] "GET /api/orders?page=3 HTTP/1.1" 200 1490 "-" "curl/8.5.0" 0.038
""")

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

w("sales.csv", """\
date,region,product,units,price
2026-10-01,north,widget,12,2.50
2026-10-01,south,gadget,3,19.99
2026-10-02,north,gadget,5,19.99
2026-10-02,east,widget,40,2.45
2026-10-03,south,widget,7,2.50
2026-10-03,east,,1,99.00
2026-10-04,north,sprocket,100,0.333
2026-10-04,west,gadget,2,21.00
""")

w("users.tsv", "u1\talice\tadmin\nu2\tbob\tdev\nu3\tcarol\tdev\nu4\tdave\tops\n")
w("orders.tsv", "o-100\tu2\t30.00\no-101\tu1\t12.50\no-102\tu9\t7.25\no-103\tu2\t4.75\no-104\tu3\t100.00\n")

w("ps.txt", """\
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.1 167744 11200 ?        Ss   Oct13   0:04 /sbin/init
postgres     812  1.2  3.4 221340 68412 ?        Ss   Oct13   2:31 postgres: checkpointer
postgres     813  0.4  1.1 221204 22016 ?        Ss   Oct13   0:52 postgres: walwriter
www-data    1401 12.5  6.0 912004 121880 ?       Sl   08:00  14:02 node /srv/shop/server.js --port 8000
www-data    1402 11.9  5.8 911876 118204 ?       Sl   08:00  13:40 node /srv/shop/server.js --port 8001
alice       2210  0.0  0.0   8920  3412 pts/0    Ss   09:01   0:00 -zsh
alice       2290 99.1  0.2  15400  4880 pts/0    R+   09:10   1:12 python3 crunch.py --threads 1
""")

w("df.txt", """\
Filesystem     1K-blocks     Used Available Use% Mounted on
/dev/nvme0n1p2  98304000 81920000  11468800  88% /
tmpfs            4096000     1024   4094976   1% /dev/shm
/dev/nvme0n1p1    524288    61440    462848  12% /boot/efi
/dev/sdb1      976762584 937692080  39070504  97% /var/lib/postgresql
""")

w("contacts.txt", """\
Alice Liddell
alice@example.com
+44 20 7946 0018

Bob Builder
bob@example.org

Carol Danvers
carol@example.net
+1 555 0100
Room 4B
""")

w("app.log", """\
2026-10-14T09:12:01Z INFO  api started on :8000
2026-10-14T09:12:05Z INFO  GET /api/orders took 42ms
2026-10-14T09:13:10Z WARN  slow query took 812ms table=orders
2026-10-14T09:14:00Z ERROR payment gateway timeout
  at Gateway.charge (gateway.js:88)
  at Checkout.run (checkout.js:31)

2026-10-14T09:14:02Z INFO  GET /api/orders took 38ms
2026-10-14T09:15:00Z ERROR db connection reset
  at Pool.query (pool.js:120)

2026-10-14T09:15:30Z INFO  POST /api/checkout took 2501ms
""")

w("env.conf", "host=db.internal;port=5432;user=shop;sslmode=require;pool=20")
w("nums.txt", "10 9\n010 10\nabc 1\n2 10\n1e3 999\n -5 -10\n0.5 .5\n")
w("report.awk", """\
# Per-status report over an access log.
function bucket(code) {
    return int(code / 100) "xx"
}
{
    b = bucket($9)
    if (!(b in count)) order[++n] = b
    count[b]++
    bytes[b] += $10
}
END {
    for (i = 1; i <= n; i++) {
        b = order[i]
        printf "%s %3d requests %8d bytes\\n", b, count[b], bytes[b]
    }
}
""")
w("a.txt", "one\ntwo\n")
w("b.txt", "three\n")

jobs = []
# A newline inside an argument is written as a vertical tab.
def j(*args):
    jobs.append("\t".join(a.replace("\n", "\v") for a in args))

# fields, patterns, the special variables
j("{ print $1 }", "access.log")
j("-F:", "$3 >= 1000 && $7 !~ /nologin/ { print $1, $6 }", "passwd")
j("END { print NR, \"requests\" }", "access.log")
j("{ s += $10 } END { print s, \"bytes,\", s / NR, \"average\" }", "access.log")
j("$9 >= 500", "access.log")
j("-F:", "-v", "OFS=:", "$7 == \"/bin/bash\" { $7 = \"/bin/zsh\"; print }", "passwd")
j("{ print NR \": \" $NF \"s \" $(NF-2) }", "access.log")
j("NR % 3 == 1", "passwd")
j("NR == 2, NR == 4 { print FNR, FILENAME, $1 }", "passwd")
j("/ERROR/, /^$/", "app.log")
j("length($0) > 100 { print NR, length($0) }", "access.log")
j("{ print length }", "a.txt", "b.txt")
j("FNR == 1 { print \"--\", FILENAME } { print FNR, NR, $0 }", "a.txt", "b.txt")
# arrays
j("{ c[$1]++ } END { for (ip in c) n++; print n, \"distinct clients\" }", "access.log")
j("!seen[$9]++ { print $9 }", "access.log")
j("-f", "report.awk", "access.log")
j("{ t[$1] += $NF } END { for (k in t) if (t[k] > 1) print k, t[k] }", "access.log")
j("-F\\t", "NR == FNR { name[$1] = $2; next } { print $1, ($2 in name ? name[$2] : \"unknown(\" $2 \")\"), $3 }", "users.tsv", "orders.tsv")
j("-F\\t", "-v", "OFS=\\t", "NR == FNR { role[$1] = $3; next } $2 in role { sum[role[$2]] += $3 } END { print \"dev\", sum[\"dev\"]; print \"admin\", sum[\"admin\"]; print \"ops\", sum[\"ops\"] + 0 }", "users.tsv", "orders.tsv")
j("BEGIN { a[1,2] = \"x\"; a[\"k\"] = 1; if ((1,2) in a) print \"pair\"; for (k in a) if (index(k, SUBSEP)) { split(k, p, SUBSEP); print p[1], p[2] }; delete a[1,2]; print length(a); delete a; print length(a) }")
# a top-N with a user sort, since awk has no sort
j("""function isort(keys, vals, n,   i, j, k) {
    for (i = 2; i <= n; i++) {
        k = keys[i]
        for (j = i - 1; j >= 1 && vals[keys[j]] < vals[k]; j--) keys[j + 1] = keys[j]
        keys[j + 1] = k
    }
}
{ if (!($1 in hits)) ips[++n] = $1; hits[$1]++ }
END { isort(ips, hits, n); for (i = 1; i <= n && i <= 3; i++) printf "%-14s %d\\n", ips[i], hits[ips[i]] }""", "access.log")
# CSV
j("-F,", "NR > 1 { rev[$2] += $4 * $5; if (!($2 in seen)) { seen[$2]; r[++n] = $2 } } END { for (i = 1; i <= n; i++) printf \"%-6s %9.2f\\n\", r[i], rev[r[i]]; }", "sales.csv")
j("-F,", "NR > 1 && $3 == \"\" { print \"line \" NR \": no product\" }", "sales.csv")
j("-F,", "NR > 1 { printf \"%s %-9s %5.1f%%\\n\", $1, $3, 100 * $4 / 169 }", "sales.csv")
# ps and df, the classic one-liners
j("NR > 1 && $3 > 10 { printf \"%-8s %5d %5.1f%% \", $1, $2, $3; for (i = 11; i <= NF; i++) printf \"%s%s\", $i, (i < NF ? \" \" : \"\\n\") }", "ps.txt")
j("NR > 1 { mem[$1] += $6 } END { print \"postgres\", mem[\"postgres\"] \" KiB\"; print \"www-data\", mem[\"www-data\"] / 1024 \" MiB\" }", "ps.txt")
j("NR > 1 { sub(/%/, \"\", $5); if ($5 + 0 >= 90) print \"ALERT\", $6, $5 \"%\", int($4 / 1024) \" MiB free\" }", "df.txt")
j("NR > 1 { u += $3; t += $2 } END { printf \"%.1f%% of %.2f GiB used\\n\", 100 * u / t, t / 1048576 }", "df.txt")
# records and field splitting
j("BEGIN { RS = \"\"; FS = \"\\n\" } { printf \"%s <%s> %d lines\\n\", $1, $2, NF }", "contacts.txt")
j("BEGIN { RS = \";\" } { split($0, kv, \"=\"); printf \"%-8s %s\\n\", kv[1], kv[2] }", "env.conf")
j("-F[:,]", "NR <= 4 { print NF, $5, $6 }", "passwd")
j("{ n = split($4, t, /[\\/:\\[]/); print n, t[2], t[3], t[4] \":\" t[5] }", "access.log")
j("{ $3 = \"\"; print; print NF }", "a.txt")
j("{ NF = 2; print } END { $0 = \"p   q  r\"; print NF, $3; $5 = \"e\"; print; print NF }", "nums.txt")
j("-v", "OFS=-", "{ $1 = $1; print }", "nums.txt")
j("BEGIN { FS = \",\" } { print NF \": \" $2 \"|\" $3 }", "sales.csv")
# strings
j("{ gsub(/[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+/, \"x.x.x.x\"); print $1, $NF }", "access.log")
j("match($0, /took [0-9]+ms/) { print substr($0, RSTART + 5, RLENGTH - 7), \"ms at\", substr($1, 12, 8) }", "app.log")
j("BEGIN { s = \"aaa\"; n = gsub(/a*/, \"-\", s); print n, s; t = \"hello\"; gsub(//, \"-\", t); print t; u = \"banana\"; gsub(/ana/, \"[&]\", u); print u; v = \"a.b.c\"; sub(/\\./, \"\\\\&\", v); print v; w = \"x\"; print gsub(/y/, \"z\", w), w }")
j("BEGIN { print index(\"hello\", \"ll\"), index(\"hello\", \"z\"), toupper(\"mixed Case 1\"), tolower(\"ABC\"); print substr(\"hello\", 0), substr(\"hello\", 5, 1), substr(\"hello\", 2, 100), substr(\"hello\", 3), \"[\" substr(\"hello\", 9) substr(\"hello\", 2, 0) \"]\" }")
j("BEGIN { n = split(\"a b  c\", p); print n, p[3]; n = split(\"a,,b\", q, \",\"); print n, \"[\" q[2] \"]\"; n = split(\"\", r); print n; n = split(\"2026-10-14\", d, \"-\"); print d[1] + 0, d[2] * 2 }")
j("{ if (match($0, / (INFO|WARN|ERROR) /)) { lvl = substr($0, RSTART + 1, RLENGTH - 2); c[lvl]++ } } END { print \"INFO\", c[\"INFO\"], \"WARN\", c[\"WARN\"], \"ERROR\", c[\"ERROR\"] }", "app.log")
j("$2 ~ \"^\" lvl { print }", "lvl=ERR", "app.log")
j("{ print x, $0 }", "x=1", "a.txt", "x=2", "b.txt")
j("BEGIN { printf \"%s|%c|%c|%5s|%-5s|%.2s\\n\", \"str\", 65, \"hello\", \"ab\", \"ab\", \"abc\" }")
# numbers
j("BEGIN { print 0.1 + 0.2, 1e6, 1e16, 1e20, 100000 * 100000, 1 / 3, -0, 2 ^ 53 + 1, 3.0, \"3.0\" + 0, \"1e3\" + 0, \" 12abc\" + 0, \".5\" + 0, 2 ^ 3 ^ 2, -2 ^ 2, 7 % 3, -7 % 3, 2.5 % 1 }")
j("BEGIN { printf \"%5d|%-5d|%05d|%+d|%x|%o|%e|%.3e|%g|%G|%10.4f|%%|%i|%X|% d|%.0f|%.0f|%#o|%#x\\n\", 42, 42, 42, 42, 255, 8, 1234.5678, 0.000123456, 0.0001234, 1e-10, 3.14159265, -7.9, 255, 5, 0.5, 1.5, 8, 255 }")
j("BEGIN { printf \"%d %d %d %s %s %g %g %g %.10g\\n\", \"3abc\", 2147483648 * 4, -2.7, 1e6, 1234567.5, 100000, 1000000, 123456789, 2/3; printf \"%*d|%-*d|%.*f\\n\", 5, 1, 4, 2, 2, 3.14159 }")
j("BEGIN { x = 0.1; y = x \"\"; CONVFMT = \"%.2f\"; z = 3.14159 \"\"; a[3.14159] = 1; for (k in a) print y, z, k; OFMT = \"%.3f\"; print 3.14159, 17, 1e3, 2 / 3 \"\" }")
j("{ print ($1 < $2), ($1 == $2), ($1 \"\" < $2 \"\") }", "nums.txt")
j("BEGIN { print 1 == 1.0, \"10\" < \"9\", 10 < 9, \"abc\" < 1, x == 0, x == \"\", length(x) }")
j("BEGIN { print int(-3.7), int(\"4.9x\"), sqrt(2), exp(1), log(10), atan2(0, -1), sin(0), cos(0) }")
# control flow and functions
j("""function fib(n) { return n < 2 ? n : fib(n - 1) + fib(n - 2) }
function fact(n) { if (n <= 1) return 1; return n * fact(n - 1) }
BEGIN {
    for (i = 0; i <= 10; i++) printf "%d%s", fib(i), (i < 10 ? " " : "\\n")
    print fact(20), fact(25)
    i = 0
    while (1) { if (++i > 5) break; if (i % 2) continue; printf "even %d\\n", i }
    do { i-- } while (i > 3)
    print "i", i, i++ + ++i, i--, -i, !i, !!i
}""")
j("function add(arr, k, v) { arr[k] = v; n2++ } function count(arr,   c, k) { for (k in arr) c++; return c } BEGIN { add(m, \"a\", 1); add(m, \"b\", 2); print count(m), n2, m[\"b\"] }")
j("NR == 3 { exit 3 } { print } END { print \"end at\", NR }", "passwd")
j("BEGIN { while ((getline line < \"passwd\") > 0) n++; print n, \"users\"; close(\"passwd\"); getline line < \"passwd\"; split(line, f, \":\"); print f[1]; print (getline x < \"missing\") }")
j("NR == 1 { getline; print \"after getline:\", NR, $1; getline tmp; print \"into var:\", NR, tmp, $1 }", "a.txt", "b.txt")
j("{ print $1 > ($9 \".txt\") } END { close(\"200.txt\"); print \"more\" >> \"200.txt\"; print \"wrote\", NR }", "access.log")
jobs.append("@cat\t200.txt")
jobs.append("@cat\t404.txt")
j("BEGIN { printf \"to stderr\\n\" > \"/dev/stderr\"; print \"to stdout\"; ORS = \"|\"; print \"a\"; print \"b\"; ORS = \"\\n\"; print \"\"; print \"tab\\there\", \"q\\\"uote\", \"back\\\\slash\" }")
j("BEGIN { OFS = \"\\t\"; print \"a\", \"b\"; $0 = \"x y z\"; $1 = $1; print }")
j("BEGIN { for (i = 1; i < ARGC; i++) print i, ARGV[i]; print ARGC }", "access.log", "x=1", "passwd")
j("BEGIN { if (\"aa\" ~ /a{2}/) print \"interval\"; if (\"ab\" ~ /^[[:alpha:]]+$/) print \"class\"; if (\"a+b\" ~ /a\\+b/) print \"escape\"; if (\"/x/\" ~ /\\/x\\//) print \"slash\"; r = \"^[0-9]+$\"; if (\"123\" ~ r) print \"dynamic\" }")
# errors
j("BEGIN { x = 1 +* 2 }")
j("{ print $1")
j("BEGIN { foo(1) }")
j("{ print }", "nofile", "a.txt")
j("BEGIN { print (\"a\" ~ /(/) }")
open("jobs.tsv", "w").write("\n".join(jobs) + "\n")
