# Writes data/ (the input files) and jobs.tsv: one shell pipeline per
# line, its arguments tab-separated (a tab inside one written as a
# vertical tab) and its stages separated by a group-separator (0x1d)
# argument, so that `|` can be an argument of `expr`.
import os
os.makedirs("data/conf.d", exist_ok=True)
def w(name, text):
    open("data/" + name, "w").write(text)

w("conf.d/app.conf", "port=8080\n")
w("empty.txt", "")
w("notes.txt", """\
TODO\tship the release notes\tdue: fri
name\tqty\tprice
widget\t12\t2.50
a\tbb\tccc\tdddd
The deploy script runs every night at two and rotates the logs before it uploads them to the archive bucket.
x\t\ty
""")
w("indent.txt", """\
        server {
            listen 80;
    \t    root /srv/www;
  mixed  spacing   here
        }
""")
w("header.bin", "KARA\x01\x00\x02\x7f\tv1.2\ncafé\n")
w("secret.txt", "user=deploy\npassword=hunter2 & more!\n")
w("token.b64", "dXNlcj1kZXBsb3kKcGFzc3dvcmQ9aHVudGVyMiAmIG1vcmUhCg==\n")
w("wrapped.b64", "VGhlIHF1aWNrIGJyb3du\nIGZveCBqdW1wcyBvdmVy\nIHRoZSBsYXp5IGRvZy4=\n")
w("bad.b64", "aGVsbG8*d29ybGQ=\n")
w("ports.txt", "22\n80\n443\n8080\n")
w("story.txt", """\
Once upon a time there was a build server that never slept. It compiled every commit that anyone pushed, day and night.

Then one day the disk filled up.
""")

jobs = []
def j(*stages):
    parts = []
    for i, st in enumerate(stages):
        if i:
            parts.append("\x1d")
        parts.extend(st)
    jobs.append("\t".join(a.replace("\t", "\v") for a in parts))

# printf
j(["printf", "%s has %d items\\n", "cart", "3"])
j(["printf", "%-10s|%5s|\\n", "left", "right", "a", "b"])
j(["printf", "%05d %+d % d %x %X %o %#x %#o\\n", "42", "7", "9", "255", "255", "8", "255", "8"])
j(["printf", "%.2f %8.3f %-8.1f| %f\\n", "3.14159", "2.5", "10", "1"])
j(["printf", "%c%c%c\\n", "abc", "xyz", "9"])
j(["printf", "%s=%s\\n", "a", "1", "b", "2", "c"])
j(["printf", "[%*d] [%-*d] [%.*s]\\n", "6", "42", "4", "7", "3", "abcdef"])
j(["printf", "%d %d %d %d\\n", "0x1F", "010", "'A", "-12"])
j(["printf", "%b|%s\\n", "tab\\there", "tab\\there"])
j(["printf", "octal \\101\\102 hex \\x43\\x44 quote \\\" back \\\\ pct %%\\n"])
j(["printf", "%b", "one\\ctwo"])
j(["printf", "%.3s|%10.4s|\\n", "abcdef", "abcdef"])
j(["printf", "%d\\n", "12abc"])
j(["printf", "%d %s\\n", "x1"])
j(["printf", "%u %i\\n", "-1", "077"])
j(["printf", "no newline"])
j(["printf", "%z\\n", "1"])
j(["printf"])
# expr
j(["expr", "3", "+", "4", "*", "2"])
j(["expr", "(", "3", "+", "4", ")", "*", "2"])
j(["expr", "17", "/", "5", "-", "17", "%", "5"])
j(["expr", "-7", "/", "2"])
j(["expr", "-7", "%", "2"])
j(["expr", "5", ">", "3"])
j(["expr", "abc", "<", "abd"])
j(["expr", "10", "<", "9"])
j(["expr", "10", "=", "010"])
j(["expr", "0", "|", "fallback"])
j(["expr", "", "|", "0"])
j(["expr", "3", "&", "0"])
j(["expr", "length", "deploy-2026"])
j(["expr", "substr", "release-v1.4.2", "10", "3"])
j(["expr", "index", "user@example.com", "@."])
j(["expr", "release-v1.4.2", ":", "release-v\\([0-9]*\\)"])
j(["expr", "release-v1.4.2", ":", ".*"])
j(["expr", "backup_2026.tar.gz", ":", "\\(.*\\)\\.tar\\.gz$"])
j(["expr", "match", "host42", "[a-z]*"])
j(["expr", "abc", ":", "x*"])
j(["expr", "file.txt", ":", "\\(.*\\)\\.png"])
j(["expr", "4", "/", "0"])
j(["expr", "4", "+", "x"])
j(["expr", "4", "+"])
j(["expr", "1", "2"])
# seq
j(["seq", "5"])
j(["seq", "3", "7"])
j(["seq", "10", "-3", "1"])
j(["seq", "-s", ",", "1", "6"])
j(["seq", "-w", "8", "11"])
j(["seq", "-w", "-2", "2"])
j(["seq", "0", "0.25", "1"])
j(["seq", "1.5", "4"])
j(["seq", "-f", "node%02g", "1", "3"])
j(["seq", "-f", "%.3f", "0", "0.5", "1"])
j(["seq", "-s", " ", "-w", "1", "3", "10"])
j(["seq", "5", "1"])
j(["seq", "1", "0", "3"])
j(["seq", "abc"])
j(["seq"])
# test
j(["test", "-f", "notes.txt"])
j(["test", "-f", "conf.d"])
j(["test", "-d", "conf.d"])
j(["test", "-e", "missing.txt"])
j(["test", "-s", "empty.txt"])
j(["test", "-s", "notes.txt"])
j(["test", "-z", ""])
j(["test", "-n", ""])
j(["test", "abc", "=", "abc"])
j(["test", "abc", "!=", "abc"])
j(["test", "10", "-lt", "9"])
j(["test", "10", "-ge", "10"])
j(["test", "-5", "-lt", "3"])
j(["test", "!", "-d", "notes.txt"])
j(["test", "-f", "notes.txt", "-a", "-d", "conf.d"])
j(["test", "-f", "missing", "-o", "-z", ""])
j(["test", "(", "1", "-eq", "2", ")", "-o", "x", "=", "x"])
j(["test", "abc"])
j(["test", ""])
j(["test"])
j(["test", "abc", "-eq", "1"])
j(["test", "1", "-eq"])
# basename and dirname
j(["basename", "/var/log/nginx/access.log"])
j(["basename", "/var/log/nginx/access.log", ".log"])
j(["basename", "-s", ".tar.gz", "/srv/backup/db.tar.gz"])
j(["basename", "-a", "/etc/hosts", "usr/lib/", "/", "plain"])
j(["basename", ".log", ".log"])
j(["basename", "a//b///"])
j(["dirname", "/var/log/nginx/access.log", "relative", "/", "usr/lib/", "//srv//x"])
j(["basename"])
# od
j(["od", "header.bin"])
j(["od", "-c", "header.bin"])
j(["od", "-A", "x", "-t", "x1z", "header.bin"])
j(["od", "-A", "d", "-t", "u1", "-N", "8", "header.bin"])
j(["od", "-A", "n", "-t", "x2", "header.bin"])
j(["od", "-t", "d4", "-j", "4", "header.bin"])
j(["od", "-b", "-w8", "ports.txt"])
j(["od", "-t", "a", "header.bin"])
j(["od", "-A", "x", "-t", "x1", "empty.txt"])
j(["printf", "%s", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab"], ["od", "-A", "d", "-c"])
j(["printf", "%s", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab"], ["od", "-A", "d", "-v", "-c"])
j(["od", "-t", "x8", "header.bin"])
j(["od", "-t", "q1", "header.bin"])
# base64
j(["base64", "secret.txt"])
j(["base64", "-w", "16", "secret.txt"])
j(["base64", "-w", "0", "secret.txt"])
j(["base64", "-d", "token.b64"])
j(["base64", "-d", "wrapped.b64"])
j(["printf", "%s", "a"], ["base64"])
j(["printf", "%s", "ab"], ["base64"], ["base64", "-d"])
j(["base64", "-d", "bad.b64"])
j(["base64", "missing.txt"])
# fold
j(["fold", "-w", "30", "story.txt"])
j(["fold", "-s", "-w", "30", "story.txt"])
j(["fold", "-w", "20", "notes.txt"])
j(["fold", "-b", "-w", "20", "notes.txt"])
j(["fold", "-w", "0", "story.txt"])
# expand and unexpand
j(["expand", "notes.txt"])
j(["expand", "-t", "4", "notes.txt"])
j(["expand", "-t", "8,14,20", "notes.txt"])
j(["expand", "-i", "-t", "2", "indent.txt"])
j(["unexpand", "indent.txt"])
j(["unexpand", "-a", "indent.txt"])
j(["unexpand", "-t", "4", "indent.txt"])
j(["expand", "notes.txt"], ["unexpand", "-a"])
# factor
j(["factor", "12", "97", "1", "0", "360", "1001", "65536"])
j(["factor", "600851475143", "9999999967", "4294967297"])
j(["printf", "%s\\n", "84 91", "  1024\t77"], ["factor"])
j(["factor", "12", "x9", "15"])
j(["seq", "2", "12"], ["factor"])
open("jobs.tsv", "w").write("\n".join(jobs) + "\n")
