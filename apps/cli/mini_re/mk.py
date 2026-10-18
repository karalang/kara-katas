#!/usr/bin/env python3
"""Writes data/: an access log, an app log, a source file and a config,
and data/cases.tsv, the jobs mini_re runs. Each case is
op <TAB> pattern <TAB> flags <TAB> subject [<TAB> extra]. The pattern
and replacement fields are raw; in the subject, \\n, \\t and \\\\ stand
for a newline, a tab and a backslash, and @name means the file
data/name."""
import os

os.makedirs("data", exist_ok=True)


def put(name, text):
    with open("data/" + name, "w", encoding="utf-8", newline="") as f:
        f.write(text)


put("access.log", """\
203.0.113.7 - - [09/Mar/2024:17:42:05 +0000] "GET /menu HTTP/1.1" 200 5120 "-" "curl/8.5.0"
198.51.100.23 - ana [09/Mar/2024:17:42:06 +0000] "POST /orders HTTP/1.1" 201 312 "https://cafe.example/menu" "Mozilla/5.0 (X11; Linux x86_64)"
192.0.2.44 - - [09/Mar/2024:17:42:07 +0000] "GET /orders/9 HTTP/1.1" 404 0 "-" "Mozilla/5.0"
203.0.113.7 - - [09/Mar/2024:17:42:08 +0000] "DELETE /orders/7 HTTP/2.0" 204 - "-" "curl/8.5.0"
10.0.0.5 - boø [09/Mar/2024:17:42:09 +0000] "GET /search?q=cr%C3%A8me&page=2 HTTP/1.1" 200 2048 "-" "Mozilla/5.0"
garbage line without the usual fields
2001:db8::1 - - [09/Mar/2024:17:42:10 +0000] "GET /healthz HTTP/1.1" 500 91 "-" "kube-probe/1.29"
""")

put("app.log", """\
2024-03-09 17:42:05,123 INFO  [main] server started on port 8443
2024-03-09 17:42:06,004 WARN  [pool-2] slow query took 1532ms: SELECT * FROM orders WHERE id = 42
2024-03-09 17:42:07,500 ERROR [pool-1] payment failed for user=ana@example.com card=4111-1111-1111-1111
2024-03-09 17:42:07,501 ERROR [pool-1] Traceback (most recent call last):
2024-03-09 17:42:08,000 DEBUG [main] cache hit ratio 0.93
2024-03-09 17:42:09,010 INFO  [http] GET /menu from 203.0.113.7 in 12ms
2024-03-09 17:42:10,000 ERROR [pool-3] lost connection to db-2.internal:5432 (retry 3/5)
contact: Zoë <zoe.k@cafe.example>, ops@cafe.example; bad: foo@, @bar.com
""")

put("calc.txt", """\
total := price * (1 + rate_2) - 3.50
IF total >= 100 THEN discount := 0.1; ENDIF
name := 'O''Brien'  # a comment
x := y <> z
""")

put("hosts.conf", """\
# hosts and ports
[db]
primary = db-1.internal:5432
replica=db-2.internal:5432
  timeout   =  2.5s
[cache]
url = redis://cache.internal:6379/0
; old = memcached://cache.internal:11211
[empty]
""")

cases = []


def c(op, pattern, flags, subject, *extra):
    cases.append("\t".join([op, pattern, flags or "-", subject] + list(extra)))


# --- literals, classes, anchors
c("search", r"cat", "", "concatenate")
c("search", r"Cat", "", "concatenate")
c("search", r"Cat", "i", "conCATenate")
c("match", r"con", "", "concatenate")
c("match", r"cat", "", "concatenate")
c("fullmatch", r"con\w+", "", "concatenate")
c("fullmatch", r"con\w+", "", "concatenate!")
c("search", r"a.c", "", "a\\nc abc")
c("search", r"a.c", "s", "a\\nc abc")
c("findall", r"[aeiou]", "", "regular expression")
c("findall", r"[^aeiou\s]+", "", "regular expression")
c("findall", r"[a-cx-z]", "", "abcdwxyz")
c("findall", r"[-a]", "", "a-b-c")
c("findall", r"[a-]", "", "a-b-c")
c("findall", r"[]a]", "", "a]b]")
c("findall", r"[\]\-\\]", "", "a]b-c\\\\d")
c("findall", r"\d+", "", "order 42 of 1000, item ٣٤")
c("findall", r"\d+", "a", "order 42 of 1000, item ٣٤")
c("findall", r"\w+", "", "naïve café 東京 x_1")
c("findall", r"\w+", "a", "naïve café 東京 x_1")
c("findall", r"\s+", "", "a b\\tc\\n d")
c("findall", r"\S+", "", " a b\\tc\\n d ")
c("findall", r"\D+", "", "a1b22c")
c("findall", r"\W+", "", "a, b; c!")
c("findall", r"[\d.]+", "", "v1.2.3 and 4.5")
c("findall", r"[\w.-]+@[\w-]+\.[\w.]+", "", "@app.log")
c("findall", r"\x41é\101\t", "", "AéA\\t")
c("findall", r"[\x41-\x43]", "", "ABCD")
c("search", r"^b", "", "a\\nb")
c("search", r"^b", "m", "a\\nb")
c("findall", r"^\w+", "m", "one two\\nthree four\\nfive")
c("findall", r"\w+$", "m", "one two\\nthree four\\nfive")
c("findall", r"\w+$", "", "one two\\nthree four\\n")
c("search", r"four$", "", "three four\\n")
c("search", r"four\Z", "", "three four\\n")
c("search", r"\Athree", "m", "x\\nthree")
c("findall", r"\bcat\b", "", "cat concat cat's bobcat")
c("findall", r"\Bcat\B", "", "cat concat concatenate")
c("findall", r"\b\w", "", "hello big world")
c("findall", r"$", "", "a\\nb\\n")
c("findall", r"$", "m", "a\\nb\\n")
c("findall", r"^", "m", "a\\nb\\n")
# --- quantifiers
c("search", r"ab*", "", "abbbc")
c("search", r"ab*?", "", "abbbc")
c("search", r"ab+?", "", "abbbc")
c("search", r"ab??", "", "abbbc")
c("search", r"a{2}", "", "aaaa")
c("search", r"a{2,}", "", "aaaa")
c("search", r"a{,2}", "", "aaaa")
c("search", r"a{1,3}?", "", "aaaa")
c("search", r"a{3,5}", "", "aa aaaaaaa")
c("findall", r"\d{2,3}", "", "1 12 123 1234 12345")
c("findall", r"x{0}y", "", "xy y")
c("search", r"a{,}", "", "aaa")
c("search", r"a{x}", "", "a{x}")
c("search", r"a{1,x}", "", "a{1,x}")
c("search", r"a*+a", "", "aaaa")
c("search", r"a++b", "", "aaab")
c("search", r"(?>a+)b", "", "aaab")
c("search", r"(?>a+)a", "", "aaaa")
c("search", r"(?>x|xy)z", "", "xyz")
c("search", r"(?:x|xy)z", "", "xyz")
c("search", r"\d?+\d", "", "12")
c("search", r"<.*>", "", "<a><b>")
c("search", r"<.*?>", "", "<a><b>")
c("findall", r"<[^>]*>", "", "<a href='x'>link</a>")
# --- groups
c("search", r"(\w+)@(\w+)\.com", "", "mail ana@example.com now")
c("search", r"(?P<user>\w+)@(?P<host>[\w.]+)", "", "mail ana@example.com now")
c("search", r"(a)|(b)", "", "b")
c("search", r"(a)(b)?", "", "ac")
c("search", r"(a|b)*c", "", "abac")
c("search", r"(a*)*b", "", "aab")
c("search", r"(a*)+b", "", "aab")
c("search", r"(a|)*b", "", "aab")
c("search", r"(a?)*?b", "", "aab")
c("search", r"((a)|b)+", "", "ab")
c("search", r"(?:(\d)\.)+", "", "1.2.3.x")
c("search", r"(\w)(\w)?(\w)?", "", "ab")
c("search", r"(?P<a>x)(?P<b>y)?(?P<c>z)", "", "xz")
c("search", r"(\w+) \1", "", "hello hello world")
c("search", r"(?P<w>\w+) (?P=w)", "", "the the cat")
c("search", r"(a)\1", "i", "aA")
c("search", r"(\w+)\s+\1\b", "", "this is is it")
c("search", r"(a)?\1", "", "b")
c("search", r"(a)?(?(1)b|c)", "", "ab")
c("search", r"(a)?(?(1)b|c)", "", "c")
c("search", r"(?P<q>')?\w+(?(q)')", "", "'word' and word")
c("findall", r"(<)?\w+@\w+\.\w+(?(1)>|$)", "", "<a@b.cd> e@f.gh")
c("search", r"(?#a comment)abc", "", "xabc")
# --- lookaround
c("findall", r"\w+(?=,)", "", "a, b, c")
c("findall", r"\w+(?!,)\b", "", "a, b, c")
c("findall", r"(?<=\$)\d+", "", "$10 and 20 and $30")
c("findall", r"(?<!\$)\b\d+", "", "$10 and 20 and $30")
c("search", r"(?<=ab)c", "", "abc")
c("search", r"(?<=a|b)c", "", "bc")
c("search", r"(?<=(a))c", "", "ac")
c("search", r"(?=(\w+))\w", "", "word")
c("findall", r"(?=(\d\d))", "", "12345")
c("search", r"^(?!.*password).*$", "", "user=ana token=x")
c("search", r"^(?!.*password).*$", "", "user=ana password=x")
c("search", r"(?<=\bfoo)bar", "", "foobar")
# --- flags
c("findall", r"(?i)cafe", "", "CAFE Cafe cafe")
c("findall", r"(?i:ca)fe", "", "CAFE Cafe cafe CAfe")
c("findall", r"(?-i:ca)fe", "i", "CAFE Cafe cafe caFE")
c("findall", r"[a-z]+", "i", "Hello WORLD")
c("findall", r"[^a-z]+", "i", "Hello WORLD")
c("findall", r"é", "i", "É é e")
c("findall", r"(?x) \d+ # digits\n  \. \d*", "", "1.5 2. 3")
c("findall", r"(?x)a\ b [ ]c", "", "a b c ab c")
c("findall", r"(?m)^\w", "", "a\\nb")
c("findall", r"(?s).", "", "a\\nb")
c("findall", r"(?a)\w+", "", "café")
c("findall", r"(?im)^x", "", "X\\nx")
c("search", r"a(?i)b", "", "aB")
c("search", r"(?u)\w", "a", "x")
# --- alternation and priority
c("search", r"cat|category", "", "category")
c("search", r"category|cat", "", "category")
c("search", r"(cat|category)s?\b", "", "categorys")
c("findall", r"a|b|", "", "abc")
c("search", r"|a", "", "a")
c("findall", r"(\d+)-(\d+)|(\w+)", "", "10-20 ab 3-4")
# --- empty matches
c("findall", r"x*", "", "abxd")
c("sub", r"x*", "", "abxd", "-")
c("split", r"x*", "", "abxd")
c("split", r"", "", "abc")
c("findall", r"\b", "", "ab cd")
c("sub", r"\b", "", "ab cd", "|")
c("findall", r"a??", "", "aa")
c("finditer", r"\w*", "", "ab, c")
# --- sub and templates
c("sub", r"(\w+)@(\w+)", "", "ana@ex bo@ex", r"\2:\1")
c("sub", r"(?P<y>\d{4})-(?P<m>\d\d)", "", "2024-03 and 1999-12", r"\g<m>/\g<y>")
c("sub", r"\d", "", "a1b2c3", r"<\g<0>>")
c("sub", r"\s+", "", "a  b \\t c", " ")
c("sub", r"o", "", "foo boo", "0", "2")
c("sub", r"(a)|b", "", "ab", r"[\1]")
c("sub", r",", "", "a,b", r"\n")
c("sub", r",", "", "a,b", r"\\")
c("sub", r",", "", "a,b", r"\&")
c("sub", r",", "", "a,b", r"\g<1>")
c("sub", r"(a)", "", "a", r"\2")
c("sub", r"(a)", "", "a", r"\q")
c("sub", r"(?P<x>a)", "", "a", r"\g<y>")
c("sub", r"(?P<x>a)", "", "a", r"\g<x")
c("sub", r"(a)", "", "a", r"\10")
c("sub", r"(a)", "", "a", r"\g<-1>")
c("sub", r"(?P<x>a)", "", "a", r"\g<1x>")
c("sub", r"a", "", "aaa", "", "0")
c("sub", r"(\w+) (\w+)", "", "hello world", r"\2 \1")
c("sub", r"[\w.]+@[\w.]+", "", "@app.log", "<email>")
c("sub", r"\b(\d{4})-\d{4}-\d{4}-(\d{4})\b", "", "@app.log", r"\1-****-****-\2")
c("sub", r"(?m)^(\S+ \S+) (\w+)\s+", "", "@app.log", r"\2 \1 ")
# --- split
c("split", r",\s*", "", "a, b,c ,d")
c("split", r"(,)\s*", "", "a, b,c")
c("split", r"(,)|(;)", "", "a,b;c")
c("split", r"\s+", "", " a b  c ")
c("split", r"\W+", "", "Words, words, words.", "1")
c("split", r"[:=]", "", "a=b:c", "5")
c("split", r"x", "", "")
c("split", r"x*", "", "")
c("split", r"(?m)^", "", "a\\nb\\nc")
c("split", r"\n", "", "@hosts.conf")
# --- finditer and real formats
c("finditer", r'(?P<ip>[\d.:a-f]+) - (?P<user>\S+) \[(?P<ts>[^\]]+)\] "(?P<method>[A-Z]+) (?P<path>\S+) (?P<proto>[^"]+)" (?P<status>\d{3}) (?P<bytes>\d+|-)', "m", "@access.log")
c("finditer", r"(?m)^(?P<date>\d{4}-\d\d-\d\d) (?P<time>[\d:,]+) (?P<level>[A-Z]+)\s+\[(?P<thread>[^\]]+)\] (?P<msg>.*)$", "", "@app.log")
c("finditer", r"(?m)^\s*(?P<key>[\w.]+)\s*=\s*(?P<value>.*?)\s*$", "", "@hosts.conf")
c("finditer", r"(?m)^\[(?P<section>[^\]]*)\]$", "", "@hosts.conf")
c("findall", r"(\w[\w.-]*):(\d+)", "", "@hosts.conf")
c("findall", r"(?P<scheme>\w+)://(?P<host>[^:/]+)(?::(?P<port>\d+))?", "", "@hosts.conf")
c("findall", r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "", "@access.log")
c("findall", r'"[^"\\]*(?:\\.[^"\\]*)*"', "", r'say "hi \"there\"" and "x"')
c("findall", r"'(?:[^']|'')*'", "", "@calc.txt")
c("tokens", r"(?P<NUMBER>\d+(?:\.\d*)?)|(?P<ASSIGN>:=)|(?P<END>;)|(?P<ID>[A-Za-z_]\w*)|(?P<OP>[+\-*/()]|<>|>=|<=|[<>=])|(?P<STRING>'(?:[^']|'')*')|(?P<COMMENT>\#.*)|(?P<NEWLINE>\n)|(?P<SKIP>[ \t]+)|(?P<MISMATCH>.)", "", "@calc.txt")
c("tokens", r"(?P<num>\d+)|(?P<word>[a-z]+)|(?P<other>.)", "", "ab12+c")
# --- backtracking that terminates
c("search", r"(a+)+b", "", "aaaaaaaaaaaaaaaaaaaaab")
c("search", r"(x+x+)+y", "", "xxxxxxxxxxy")
c("search", r"^(\w+\s?)*$", "", "a few words here")
c("fullmatch", r"(?:\d+\.){3}\d+", "", "192.168.0.1")
c("fullmatch", r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "", "first.last+tag@sub.example.co")
c("fullmatch", r"(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?", "", "23:59:60")
c("fullmatch", r"(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?", "", "07:05")
c("fullmatch", r"v?(\d+)\.(\d+)\.(\d+)(?:-([\w.]+))?(?:\+([\w.]+))?", "", "v1.2.3-rc.1+build.5")
# --- compile and errors
c("compile", r"(a)(?P<n>b)(?:c)(d)", "", "")
c("compile", r"*a", "", "")
c("compile", r"a**", "", "")
c("compile", r"a{2}{3}", "", "")
c("compile", r"a(?", "", "")
c("compile", r"(a", "", "")
c("compile", r"a)", "", "")
c("compile", r"[a", "", "")
c("compile", r"[z-a]", "", "")
c("compile", r"a\q", "", "")
c("compile", r"\2(a)", "", "")
c("compile", r"(a\1)", "", "")
c("compile", r"(?P<1a>x)", "", "")
c("compile", r"(?P<a>x)(?P<a>y)", "", "")
c("compile", r"(?P=b)", "", "")
c("compile", r"(?P<a>x", "", "")
c("compile", r"(?<x>a)", "", "")
c("compile", r"(?Px)", "", "")
c("compile", r"(?<=a+)b", "", "")
c("compile", r"(?<=a|bc)d", "", "")
c("compile", r"a{3,2}", "", "")
c("compile", r"x(?i)y", "", "")
c("compile", r"(?z)", "", "")
c("compile", r"\x4", "", "")
c("compile", r"\u12", "", "")
c("compile", r"[\d-z]", "", "")
c("compile", r"(?(2)a|b)(x)", "", "")
c("compile", r"(?(1)a|b|c)(x)", "", "")
c("compile", r"\\", "", "")
c("compile", r"a\\", "", "")
c("compile", "a\\", "", "")
c("compile", r"(?P<ünï>x)", "", "")
c("compile", r"()+", "", "")

put("cases.tsv", "\n".join(cases) + "\n")
