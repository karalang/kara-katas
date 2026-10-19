# Writes data/: the jobs in data/jobs.jsonl, two feature files and the
# step table for the BDD runner, an access log, an application log and a
# few documents to scan.
import json
import os
import random

R = random.Random(114)
jobs = []


def job(op, fmt, s=None, **kw):
    j = {"op": op, "fmt": fmt}
    if s is not None:
        j["s"] = s
    j.update(kw)
    jobs.append(j)


def P(fmt, s, **kw):
    job("parse", fmt, s, **kw)


def S(fmt, s, **kw):
    job("search", fmt, s, **kw)


def F(fmt, s, **kw):
    job("findall", fmt, s, **kw)


def E(fmt, **kw):
    job("expr", fmt, **kw)


# ------------------------------------------------------------ the basics
P("hello {}", "hello world")
P("hello {}", "hello  world ")
P("hello {}", "Hello World")
P("hello {}", "Hello World", cs=True)
P("hello {}", "hello world", cs=True)
P("{} {}", "a b c")
P("{}{}", "abc")
P("{} and {}", "salt and pepper and ginger")
P("{name} is {age:d}", "Alice is 30")
P("{name} is {age:d}", "Alice is thirty")
P("{name} is {age:d} years", "Bob Smith is 42 years")
P("{0} {1}", "x y")
P("{1} {0}", "x y")
P("{_x} {y}", "1 2")
P("{-} {y}", "1 2")
P("{}", "")
P("", "")
P("", "x")
P("x", "X")
P("{}", "line one\nline two")
P("{}\n{}", "line one\nline two")
P("a.b {}", "a.b c")
P("a.b {}", "axb c")
P("1+1={:d}", "1+1=2")
P("(x) {}", "(x) y")
P("[{}]", "[inside]")
P("cost: ${:f}", "cost: $3.50")
P("^{}$", "^anchored$")
P("a|b {}", "a|b c")
P("a!b {}", "a!b c")
P("path\\to\\{}", "path\\to\\file")
P("tab\t{}", "tab\tthere")
P("x{2,3} {}", "xx y")
P("x{2,3} {}", "x{2,3} y")
P("x{,3}y", "xxxy")
P("x{,3}y", "x{,3}y")
P("a { b", "a { b")
P("a } b", "a } b")
P("{{}}", "{}")
P("{{{}}}", "{abc}")
P("{{x}} {}", "{x} 5")
P("{{x}} {}", "{{x}} 5")
P("}}{{", "}{")
P("café {}", "CAFÉ noir")
P("straße {}", "STRASSE x")
P("Σ {}", "σ x")
P("{} ünïcödé", "ÜNÏCÖDÉ? no: üNÏcödé")
P("naïve {x}", "NAÏVE 1")
P("{x:d}", "٣")
P("{x:d}", "1٣")
P("{x:n}", "١٢")
P("{x:w}", "日本語")
P("{x}-{y}", "a-b-c")
P("{x:d}-{y}", "1-2-3")
P("{greeting}, {name}!", "Hello, World!")
P("{greeting}, {name}!", "Hello, , !")

# fixed and named fields together, and the counts behind them
P("{} {name} {}", "a b c")
P("{name} {} {other} {}", "1 2 3 4")
P("{:d} {name:d} {:d}", "1 2 3")
P("{} {:g} {}", "a 1.5e3 b")
P("{} {:g} {}", "a 7 b")
P("{} {:ti} {}", "a 2011-11-21 b")
P("{:%} {}", "50% off")
P("{:n} {}", "1,000 rest")

# ------------------------------------------------------------ repeated names
P("{a} {a}", "x x")
P("{a} {a}", "x y")
P("{a} {a}", "abc ABC")
P("{a} {a}", "abc ABC", cs=True)
P("{a:d} {a:d}", "5 5")
P("{a:d} {a:d}", "5 05")
P("{a:d} {a}", "5 5")
P("{a} {b} {a} {b}", "1 2 1 2")
P("{a} {b} {a} {b}", "1 2 2 1")
P("{a}{a}", "xyxy")
P("{a}{a}", "aaaa")
P("{a}{a}{a}", "abcabcabc")
P("{a.b} {a.b}", "q q")
P("{a[b]} {a[b]}", "q q")
P("{a:>3} {a:>3}", "  x   x")

# ------------------------------------------------------------ dotted and indexed names
P("{a.b}", "1")
P("{a.b} {a_b}", "1 2")
P("{a_b} {a.b}", "1 2")
P("{a.b} {a_b} {a-b}", "1 2 3")
P("{a-b} {a_b}", "1 2")
P("{a-b} {a_b} {a.b}", "1 2 3")
P("{a.b.c} {a_b_c}", "1 2")
P("{a_b_c} {a.b.c}", "1 2")
P("{hyphen-name}", "ok")
P("{a[b]}", "1")
P("{a[b]} {a[c]}", "1 2")
P("{a[b][c]} {a[b][d]} {a[e]}", "1 2 3")
P("{x[0]} {x[1]}", "first second")
P("{a[b]} {a}", "1 2")
P("{a} {a[b]}", "1 2")
P("{a} {a[b][c]}", "1 2")
P("{a:d} {a[b]}", "1 2")
P("{a[b]} {a[b][c]}", "1 2")
P("{a[b][c]} {a[b]}", "1 2")
P("{a.b[c]} {a.b[d]}", "1 2")
P("{a[b.c]} {a[b-c]}", "1 2")
P("{a[b c]}", "1")
S("{a[b c]}", "1")
P("{a[b!]}", "1")
P("{a[*]}", "1")
P("{a[b:c]}", "1")
P("{a[b]} {a_b_}", "1 2")
P("{a_b_} {a[b]}", "1 2")
P("{ab} {ab}", "1 1")
P("{a[1]} {a[2]}", "1 2")
P("{user[name]} <{user[email]}>", "Jo <jo@example.org>")

# ------------------------------------------------------------ repeated names with other types
P("{a} {a:d}", "1 1")
P("{a:d} {a:f}", "1 1.0")
P("{a:>4} {a:<4}", "   x x   ")
P("{n.x:d} {n.x:w}", "1 1")

# ------------------------------------------------------------ format specs
for spec, vals in [
    ("d", ["0", "42", "-42", "+42", " 42", "0042", "1_000", "1,000", "0x1F", "-0x1f", "+0X1f", " 0x1f", "0b101",
           "0o17", "0O17", "-0b11", "012", "0b", "0x", "4.2", "", "x"]),
    ("3d", ["1", "123", "1234", "  7", "-12"]),
    ("03d", ["007", "7", "0007"]),
    (",d", ["1,234,567", "1234567", "1,2,3"]),
    ("_d", ["1_234", "1,234"]),
    ("n", ["1,234", "1.234.567", "123", "1234", "12,34", "-1,000"]),
    ("b", ["101", "0b101", "0B11", "-101", "102", "2"]),
    ("o", ["17", "0o17", "0O7", "-17", "8"]),
    ("x", ["ff", "FF", "0xff", "0XFF", "-1a", "g"]),
    ("X", ["DEADbeef", "0x10"]),
    ("f", ["3.14", ".5", "-0.5", "+2.0", " 1.25", "3", "1e5", "nan", "NAN", "NaN", "inf", "-inf", "INF", "-INF",
           "1.", "0.1", "123456789.123456789", "0.000001", "1.0e5"]),
    (".0f", ["3", "3.0", "-7", "nan"]),
    (".2f", ["3.14", "3.14159", "3"]),
    ("F", ["3.14", ".5", "-0.5", "1.50", "+2.000", "0.0000001", "00.10", "-0.00", "nan", "-nan", "inf", "-INF", "3"]),
    (".0F", ["42", "007", "-0"]),
    ("e", ["1.5e3", "1.5E+03", "-2.5e-10", ".5e1", "1e5", "nan", "-inf", "+INF", "3.0"]),
    ("E", ["1.5E3"]),
    ("g", ["1", "1.5", "1e5", "1.5e-3", "-7", "nan", "-inf", "1E+20", ".5"]),
    ("G", ["2.5E2"]),
    ("%", ["50%", "12.5%", "-5%", "100%", "0.1%", "50", "50 %"]),
    ("w", ["word", "two words", "under_score", "dash-ed", "123"]),
    ("W", ["!?", "a!"]),
    ("s", ["   ", "x", "\t\n"]),
    ("S", ["nospace", "has space"]),
    ("D", ["abc", "a1"]),
    ("l", ["letters", "Letters", "l3tters", "ünï"]),
]:
    for v in vals:
        P("{:%s}" % spec, v)

P("{x:5}", "  abc")
P("{x:5}", "abc")
P("{x:5}", "abcdef")
P("{x:<5}|", "abc  |")
P("{x:>5}|", "  abc|")
P("{x:^7}|", "  abc  |")
P("{x:^}|", "  abc   |")
P("{x:<}|", "abc   |")
P("{x:>}|", "   abc|")
P("{x:*^9}|", "***abc***|")
P("{x:*<9}|", "abc******|")
P("{x:.>6}|", "...abc|")
P("{x:->6}|", "---abc|")
P("{x:0>6}|", "000abc|")
P("{x:.2}", "ab")
P("{x:.2}", "abc")
P("{x:.2}|", "abc|")
P("{x:3.5}", "ab")
P("{x:3.5}", "abcd")
P("{x:3.5}", "abcdefg")
P("{x:>3.5}", "  abcd")
P("{x:0}", "abc")
P("{x:}", "abc")
P("{x:+}", "abc")
P("{x:<10d}|", "42        |")
P("{x:>10d}|", "        42|")
P("{x:^10d}|", "    42    |")
P("{x:=10d}|", "0000000042|")
P("{x:=10d}|", "-000000042|")
P("{x:x=10d}|", "xxxxxxxx42|")
P("{x:.=8d}|", "......42|")
P("{x:.=8d}|", "anything42|")
P("{x:0=8.2f}", "00003.14")
P("{x:*^10.2f}", "***3.14***")
P("{x:*^10.2f}", "**-3.14***")
P("{x:+d}", "+5")
P("{x: d}", " 5")
P("{x:-d}", "-5")
P("{x:#x}", "0xff")
P("{x:#b}", "0b1")
P("{x:q}", "1")
P("{x:dd}", "1")
P("{x:5q}", "1")
P("{x:ti }", "1")
P("{x:c]}", "1")
P("{x:|>5}", "||abc")
S("{x:|>5}", "||abc")
P("{x:|^9}", "abc")
P("{x:(>5}", "((abc")
P("{x:)>5}", "))abc")
P("{x:[>5}", "[[abc")
P("{x:]>5}", "]]abc")
P("{x:{>5}", "{{abc")
P("{x:\\>5}", "\\\\abc")
P("{x:$>5}", "$$abc")
P("{x:?>5}", "??abc")
P("{x:+>5}", "++abc")
P("{x:^>5}", "^^abc")
P("{x:a<5}", "bcaaa")
P("{x:<<5}", "ab<<<")
P("{x:<5d}", "12   ")
P("{x:,.2f}", "1,234.50")
P("{x:,.2f}", "1234.50")

# ------------------------------------------------------------ dates and times
for v in ["2011-11-21", "2011-11-21 10:21", "2011-11-21T10:21:36", "2011-11-21T10:21:36.1", "2011-11-21T10:21:36.123456789",
          "2011-11-21T10:21:36Z", "2011-11-21T10:21:36z", "2011-11-21 10:21:36+10:00", "2011-11-21 10:21:36 +1000",
          "2011-11-21 10:21:36-0530", "2011-11-21T10:21:36 -01:00", "2011-11-21Z", "2011-13-21", "2011-02-29", "2012-02-29",
          "0000-01-01", "2011-11-21 25:00", "2011-11-21 10:61", "2011-11-21 10:21:60", "2011-11-21  10:21", "2011-1-21",
          "2011-11-21T1:2:3"]:
    P("{:ti}", v)
for v in ["21/11/2011", "21-11-2011", "21/11/2011 10:21", "21/11/2011 10:21:36 AM", "21/11/2011 10:21:36 PM",
          "21/11/2011 12:00 AM", "21/11/2011 12:00 PM", "21/11/2011 12:30 am", "21/11/2011 10:21 +1000",
          "21/11/2011 10:21 PM -05:30", "21/Nov/2011", "21/November/2011", "21/nov/2011", "21/Sept/2011", "32/11/2011",
          "21/13/2011", "1/2/2011", "21/11/2011 13:00 PM", "21/11/2011 10:21 +530"]:
    P("{:tg}", v)
for v in ["11/21/2011", "11-21-2011 10:21:36 AM", "Nov/21/2011", "nov/21/2011", "November/21/2011 1:02 PM", "2/30/2012",
          "12/31/1999 11:59:59.999 PM", "11/21/2011 10:21 +10:00"]:
    P("{:ta}", v)
for v in ["Mon, 21 Nov 2011 10:21:36 +1000", "21 Nov 2011 10:21:36 +1000", "Mon, 21 Nov 2011 10:21:36.5 -0800",
          "Tue, 01 Mar 2016 00:00 +00:00", "Mon,  21 Nov 2011 10:21:36 +1000", "Mon, 21  Nov 2011 10:21:36 +1000",
          "mon, 21 nov 2011 10:21:36 +1000", "Mon, 21 Nov 2011 10:21:36", "Wed, 31 Feb 2011 10:21:36 +0000"]:
    P("{:te}", v)
for v in ["21/Nov/2011:10:21:36 +1000", "21/Nov/2011:10:21:36 -0700", "21-Nov-2011:10:21:36 +0000",
          "21/nov/2011:10:21:36 +1000", "21/Nov/2011:10:21 +1000", "1/Jan/2000:00:00:00 +9999", "21/Nov/2011:10:21:36"]:
    P("{:th}", v)
for v in ["Mon Nov 21 10:21:36 2011", "Mon Nov  1 10:21:36 2011", "Sun Feb 29 23:59:59 2012", "Sun Feb 29 23:59:59 2011",
          "mon nov 21 10:21:36 2011", "Mon Nov 21 10:21 2011"]:
    P("{:tc}", v)
for v in ["10:21", "10:21:36", "10:21:36.5", "10:21 PM", "12:00 AM", "12:00 PM", "10:21:36 PM -05:00", "10:21 +1000",
          "", "PM", " PM", "13:21 PM", "10:21 pm", "1:2:3.0000009", "99:99"]:
    P("{:tt}", v)
P("at {:tt} on {:ti}", "at 10:21 PM on 2011-11-21")
P("{when:ti} {level:w}", "2011-11-21 10:21:36 INFO")
P("{when:ti}|{}", "2011-11-21 10:21:36Z|rest")
P("{a:ti} {b:ti}", "2011-11-21 2012-01-02")
P("{:th} {} {:d}", "21/Nov/2011:10:21:36 +1000 GET 200")
P("{:tg} {}", "21/11/2011 10:21 PM x")
P("{:ts}", "x")

# strftime types
for fmt, v in [
    ("%Y-%m-%d", "2020-05-17"), ("%Y-%m-%d", "2020-5-7"), ("%Y-%m-%d", "2020-02-30"), ("%Y-%m-%d", "2020-13-01"),
    ("%Y-%m-%d", "0000-01-01"), ("%Y-%m-%d", "2020-00-10"), ("%Y-%m-%d", "2021-02-29"), ("%Y-%m-%d", "2024-02-29"),
    ("%d/%m/%Y", "17/05/2020"), ("%d/%m/%Y", "45/05/2020"), ("%d/%m/%Y", "32/05/2020"), ("%d/%m/%Y", "3/5/2020"),
    ("%d/%m/%Y", "0/5/2020"), ("%Y%m%d", "20200517"), ("%Y%m%d", "202051"), ("%y-%m-%d", "68-01-01"),
    ("%y-%m-%d", "69-01-01"), ("%y-%m-%d", "00-12-31"), ("%Y.%m.%d", "2020.05.17"), ("%Y.%m.%d", "2020x05x17"),
    ("%H:%M", "09:30"), ("%H:%M", "9:5"), ("%H:%M", "24:00"), ("%H:%M", "23:60"), ("%H:%M:%S", "23:59:59"),
    ("%H:%M:%S", "23:59:60"), ("%H:%M:%S", "23:59:61"), ("%H:%M:%S", "23:59:62"), ("%H:%M:%S.%f", "10:00:00.5"),
    ("%H:%M:%S.%f", "10:00:00.123456"), ("%I:%M %p", "09:30 PM"), ("%I:%M %p", "12:00 AM"), ("%I:%M %p", "12:00 PM"),
    ("%I:%M %p", "12:00 pm"), ("%I:%M %p", "13:00 PM"), ("%I:%M", "12:30"), ("%I:%M", "11:30"), ("%p", "PM"),
    ("%Y-%m-%d %H:%M:%S", "2020-05-17 10:20:30"), ("%Y-%m-%dT%H:%M:%S%z", "2020-05-17T10:20:30+0200"),
    ("%Y-%m-%dT%H:%M:%S%z", "2020-05-17T10:20:30-05:30"), ("%Y-%m-%dT%H:%M:%S%z", "2020-05-17T10:20:30+00:00"),
    ("%Y-%m-%dT%H:%M:%S%z", "2020-05-17T10:20:30+0000"), ("%Y-%m-%dT%H:%M:%S%z", "2020-05-17T10:20:30+01:30:15"),
    ("%Y-%m-%dT%H:%M:%S%z", "2020-05-17T10:20:30+0130:15"), ("%Y-%m-%dT%H:%M:%S%z", "2020-05-17T10:20:30|0200"),
    ("%Y-%m-%dT%H:%M:%S%z", "2020-05-17T10:20:30+0560"), ("%Y-%m-%dT%H:%M:%S%z", "2020-05-17T10:20:30+2500"),
    ("%Y-%m-%dT%H:%M:%S%z", "2020-05-17T10:20:30-2400"), ("%H:%M%z", "10:20+0100"), ("%H:%M%z", "10:20-0100"),
    ("%a %d %b %Y", "Sun 17 May 2020"), ("%a %d %b %Y", "sun 17 may 2020"), ("%a %d %b %Y", "Mon 17 May 2020"),
    ("%A %d %B %Y", "Sunday 17 May 2020"), ("%A %d %B %Y", "WEDNESDAY 1 JANUARY 2020"),
    ("%B %d, %Y", "September 9, 2020"), ("%b %d, %Y", "Sep 9, 2020"), ("%b %d, %Y", "Sept 9, 2020"),
    ("%d %B %Y", "9 Sep 2020"), ("%w %Y-%m-%d", "3 2020-05-17"), ("%Y-%j", "2020-001"), ("%Y-%j", "2020-366"),
    ("%Y-%j", "2021-366"), ("%Y-%j", "2020-60"), ("%Y-%j", "2020-000"), ("%Y-%j", "2021-367"),
    ("%Y %U %w", "2020 20 0"), ("%Y %U %w", "2020 0 3"), ("%Y %W %w", "2020 20 1"), ("%Y %W %w", "2020 0 0"),
    ("%Y %U", "2020 20"), ("%f", "123"), ("%f", "-123"), ("%f", "1234567"), ("%Y-%q", "2020-%q"),
    ("%Y-%m-%d %H", "2020-05-17 7"), ("%Y-%m-%d %H", "2020-05-17  7"), ("%Y-%m-%d %H", "2020-05-17 07"),
    ("%Y-%m-%d%%", "2020-05-17%%"), ("%Y/%m/%d %I%p", "2020/05/17 7pm"), ("%d.%m.%Y %H:%M", "17.05.2020 08:00"),
    ("%Y-%m-%d %H:%M %H", "2020-05-17 08:00 08"),
]:
    P("{:%s}" % fmt, v)
P("{:%H:%M%z} {}", "10:20+0100 tail")
P("{:%H:%M%z} {}", "10:20+01:00 tail")
P("{:%Y-%m-%d} {:d}", "2020-05-17 5")
P("{d:%Y-%m-%d} {n:d}", "2020-05-17 5")
P("{:%d/%m/%Y} {:%d/%m/%Y}", "01/02/2020 03/04/2021")
P("from {start:%Y-%m-%d} to {end:%Y-%m-%d}", "from 2020-01-01 to 2020-12-31")
P("{:%H}", "7")
P("{:%Y}", "2020")
P("{:%m %Y}", "5 2020")

# ------------------------------------------------------------ extra types
X = "Number,Bool,Word,Color,Size,Range,Csv"
P("{:Number}", "42", extra=X)
P("{:Number}", "4x", extra=X)
P("{n:Number} items", "12 items", extra=X)
P("{:Bool} {:Bool}", "yes NO", extra=X)
P("{:Bool} {}", "On rest", extra=X)
P("{:Bool} {}", "maybe rest", extra=X)
P("{a:Bool} {b:Bool} {c:Bool}", "true off FALSE", extra=X)
P("{:Word}", "hello", extra=X)
P("{:Word} {:Word}", "hello big world", extra=X)
P("{c:Color}", "Red", extra=X)
P("{c:Color}", "red", extra=X, cs=True)
P("{c:Color}", "Red", extra=X, cs=True)
P("{c:Color} {}", "blue sky", extra=X)
P("{:Size} {}", "3x4 tiles", extra=X)
P("{:Size} {}", "3X4 tiles", extra=X)
P("{:Size} {} {}", "3x4 tiles here", extra=X)
P("{s:Size} {n:d}", "10x20 5", extra=X)
P("{:Range}", "3-6", extra=X)
P("{:Range} {}", "3-6 rest", extra=X)
P("{:Range} {:d}", "3-6 10", extra=X)
P("{:Range} {} {}", "1-2 x y", extra=X)
P("{r:Range} {n:d}", "1-3 9", extra=X)
P("{:Csv}", "a, b,c", extra=X)
P("{tags:Csv}; {}", "x,y;z; rest", extra=X)
P("{:d}", "7", extra="d=Number")
P("{:d}", "-7", extra="d=Number")
P("{:q}", "7", extra="q=Number")
P("{:Num}", "7", extra="Num=Number,Number=Bool")
P("{:Number}", "7", extra="Num=Number")
P("{:>5Number}", "   42", extra=X)
P("{:Number:}", "1", extra=X)

# ------------------------------------------------------------ errors
P("{a} {a:d}", "1 1")
P("{a:d} {a}", "1 1")
P("{:dx}", "1")
P("{x:tz}", "1")
P("{x:t}", "1")
P("{:%}x", "5%x")
P("{x!r}", "1")
P("{x", "{x")
P("x}", "x}")
P("{x}}", "1}")
P("{{x}", "{1")

# ------------------------------------------------------------ search and findall
S("age: {:d}", "name: Al, age: 31, height: 180")
S("{:d}", "abc 12 def 34")
S("{:d}", "no digits")
S("{} wrote", "Then Alice wrote a letter")
S("{who} wrote", "Then Alice wrote a letter")
S("x={:d}", "x=1 x=2 x=3", pos=4)
S("x={:d}", "x=1 x=2 x=3", pos=4, endpos=7)
S("x={:d}", "x=1 x=2 x=3", pos=4, endpos=6)
S("x={:d}", "x=12", endpos=3)
S("{:d}", "12345", pos=2)
S("{:ti}", "logged at 2011-11-21 10:21:36Z by root")
S("{:th}", '1.2.3.4 - - [21/Nov/2011:10:21:36 +1000] "GET / HTTP/1.1"')
S("{:w}", "  -- word --")
S("{:Size}", "a 3x4 b", extra=X)
S("ERROR {}", "error disk full")
S("ERROR {}", "error disk full", cs=True)
S("{a}{a}", "xxabab")
S("{a:d}-{a:d}", "1-2 3-3 4-4")
S("<{tag}>", "<b>bold</b>")
S("{x:^}", "   centered   ")
F("{:d}", "1 22 333 4444")
F("{:d}", "abc")
F("<{}>", "<a> <b> <c>")
F("{key}={value}", "a=1 b=2 c=3")
F("{key:w}={value:w}", "a=1 b=2 c=3")
F("{key:w}={value:d}", "a=1, b=two, c=3")
F("#{:w}", "#one #two #three")
F("{:d}{:l}", "3kg 10m 5")
F("${:f}", "$3.50 and $4.25, $5")
F("{:d}", "1 2 3 4 5 6", pos=3, endpos=8)
F("{:ti}", "2011-11-21 then 2012-01-02T03:04 and 1999-12-31Z")
F("{a}-{a}", "x-x y-z w-w")
F("{:Bool}", "yes no maybe on", extra=X)
F("[{}]", "[a][b]")
F("{:.1}", "abc")
F("{:2}", "abcde")
F("({:d},{:d})", "(1,2) (3,4)(5, 6)")

# ------------------------------------------------------------ expressions
for f in ["hello {}", "{name} is {age:d}", "{a} {a}", "{a.b} {a_b} {a-b}", "{a[b][c]}", "{:5.2f}", "{:>10}", "{:^10d}",
          "{:=10d}", "{:x}", "{:g}", "{:%}", "{:n}", "{:w}", "{:s}", "{:l}", "{:ti}", "{:tt}", "{:th}", "{:%Y-%m-%d}",
          "{:%Y.%m}", "a.b(c)*", "{{}} {}", "x{2,3}", "{:|>5}", "{a:,d}", "{a:_x}", "{:.3}", "{:3.5}", "{:3}",
          "this is a very long format string {} with fields", "exactly twenty chars", "twenty-one characters",
          "{0} {1} {x}", "{:Size} {}", "{:Range} {}", "{:Word}", "{:e}", "{:.0f}", "{:F}", "{:*^9}", "{:.>9}",
          "{:\\<5}", "{:0=6d}", "{:%H:%M%z} {}"]:
    E(f, extra=X if ":" in f and any(t in f for t in ("Size", "Range", "Word")) else None)
E("{a} {a:d}")
E("{:q}")
E("{a[b]} {a_b_}")


# ------------------------------------------------------------ round trips
# Python's format() writes a value with a spec, and parse reads it back
def spec_rand(kind):
    fill = R.choice(["", "", "", "*", "0", "-", " ", "."])
    align = R.choice(["", "", "<", ">", "^", "="]) if kind != "s" else R.choice(["", "<", ">", "^"])
    if fill and not align:
        fill = ""
    sign = R.choice(["", "", "+", " ", "-"]) if kind != "s" else ""
    zero = R.choice(["", "", "0"]) if kind != "s" else ""
    width = R.choice(["", "", "4", "8", "12"])
    group = R.choice(["", "", ","]) if kind in ("d", "f") else ""
    prec = ""
    if kind in ("f", "e", "%"):
        prec = R.choice(["", ".1", ".2", ".3", ".0"])
    if kind == "s":
        prec = R.choice(["", "", ".3", ".8"])
    return fill + align + sign + zero + width + group + prec


for k in range(220):
    kind = R.choice(["d", "d", "f", "f", "e", "%", "x", "o", "b", "s", "s", "g"])
    spec = spec_rand(kind)
    if kind == "d":
        v = R.choice([R.randint(-99, 99), R.randint(-10 ** 7, 10 ** 7), 0])
    elif kind in ("x", "o", "b"):
        v = R.randint(0, 5000)
    elif kind == "s":
        v = R.choice(["abc", "hello world", "x", "Kāra", "a b", "tab\tsep", "ünï"])
    elif kind == "g":
        v = R.choice([1.5, 100.0, 1e-5, 123456789.0, 0.25, -3.75, 7.0])
    else:
        v = round(R.uniform(-1000, 1000), R.randint(0, 4))
    full = spec + ("" if kind == "s" else kind)
    try:
        text = format(v, full)
    except ValueError:
        continue
    pre = R.choice(["", "v=", "[", "value: "])
    post = R.choice(["", ";", "]", " units"])
    P("%s{v:%s}%s" % (pre, full, post), pre + text + post)

# random named templates over random records
words = ["alpha", "beta", "gamma", "delta", "Epsilon", "ZETA", "eta", "theta"]
for k in range(80):
    n = R.randint(1, 4)
    names = R.sample(["user", "host", "port", "path", "code", "msg", "id"], n)
    seps = [R.choice([" ", ": ", " | ", "/", "=", ", "]) for _ in range(n - 1)]
    types = {nm: R.choice(["", "", ":d", ":w", ":l"]) for nm in names}
    fmt = ""
    s = ""
    for i, nm in enumerate(names):
        t = types[nm]
        if t == ":d":
            val = str(R.randint(0, 9999))
        elif t == ":w":
            val = R.choice(words) + R.choice(["", "_1", "2"])
        elif t == ":l":
            val = R.choice(words)
        else:
            val = R.choice(words + ["a b", "x/y", "1=2", "q, r"])
        if R.random() < 0.08:
            val = val + "!"
        fmt += "{%s%s}" % (nm, t)
        s += val
        if i < n - 1:
            fmt += seps[i]
            s += seps[i]
    op = R.choice(["parse", "parse", "parse", "search"])
    job(op, fmt, s, cs=R.random() < 0.2)

# ------------------------------------------------------------ the BDD runner, the log report, the scanners
job("bdd", "", files=["features/cart.feature", "features/inventory.feature"])
job("bdd", "", files=["features/inventory.feature"], dry=True)
job("logs", '{ip} - {user} [{when:th}] "{method} {path} {proto}" {status:d} {size} "{referer}" "{agent}"',
    file="access.log")
job("logs", '{ip} - {user} [{when:th}] "{request}" {status:d} {size}', file="access.log", search=True)
job("applog", "{when:ti} {level:w} [{logger}] {message}", file="app.log")
job("scan", '<a href="{url}">{text}</a>', file="page.html")
job("scan", "#{tag:w}", file="post.txt")
job("scan", "{qty:d} {unit:l} of {thing:w}", file="recipe.txt")
job("scan", "{key:w} = {value}\n", file="settings.ini")
job("scan", "TODO({who:w}): {what}.", file="code.py")

os.makedirs("data/features", exist_ok=True)

FEATURE_CART = """Feature: Shopping cart
  Prices are in dollars and cents.

  Background:
    Given the store sells apple at $0.50 each
    And the store sells "pear" at $0.75 each
    And the store sells loaf of bread at $2.25 each

  Scenario: Adding fruit
    Given an empty cart
    When I add 3 apple
    And I add a pear
    Then the cart has 4 items
    And the total is $2.25

  Scenario: Removing things
    Given an empty cart
    When I add 2 loaf of bread
    And I add 1 apple
    And I remove apple
    Then the cart has 2 items
    And the cart contains loaf of bread
    But the cart does not contain apple
    And the total is $4.50

  Scenario: A discount code
    Given an empty cart
    When I add 10 apple
    And I apply the code SAVE10
    Then the total is $4.50
    And the total is $5.00
    And the cart has 10 items

  Scenario: Things the store does not sell
    Given an empty cart
    When I add 2 mango
    Then the cart has 0 items
    And I am told "we do not sell mango"

  Scenario: Steps nobody wrote
    Given an empty cart
    When I juggle 3 apple
    Then the cart has 0 items

  Scenario Outline: Many apples
    Given an empty cart
    When I add <n> apple
    Then the total is <total>
    And the cart has <n> items

    Examples:
      | n  | total  |
      | 1  | $0.50  |
      | 4  | $2.00  |
      | 12 | $6.00  |
      | 7  | $9.99  |
"""

FEATURE_INV = """Feature: Inventory
  Scenario: Receiving stock
    Given the warehouse holds 10 apple
    When 5 apple arrive on 2024-03-01
    And 3 apple leave on 2024-03-02
    Then the warehouse holds 12 apple
    And the last movement was on 2024-03-02

  Scenario: Selling out
    Given the warehouse holds 2 PEAR
    When 2 pear leave on 2024-02-29
    Then the warehouse holds 0 pear
    And pear is out of stock

  Scenario: Dates the calendar does not have
    Given the warehouse holds 1 plum
    When 1 plum arrive on 2023-02-29
    Then the warehouse holds 2 plum

  Scenario: Shouting
    GIVEN THE WAREHOUSE HOLDS 4 FIG
    Then the warehouse holds 4 fig
"""

STEPS = """given\tstore_sells\tthe store sells {item} at {price:Money} each
given\tstore_sells_quoted\tthe store sells "{item}" at {price:Money} each
given\tempty_cart\tan empty cart
when\tadd_one\tI add a {item}
when\tadd_many\tI add {qty:d} {item}
when\tremove\tI remove {item}
when\tapply_code\tI apply the code {code:w}
then\tcart_count\tthe cart has {n:d} items
then\ttotal\tthe total is {amount:Money}
then\tcontains\tthe cart contains {item}
then\tnot_contains\tthe cart does not contain {item}
then\ttold\tI am told "{message}"
given\tholds\tthe warehouse holds {qty:d} {item:w}
when\tarrive\t{qty:d} {item:w} arrive on {day:%Y-%m-%d}
when\tleave\t{qty:d} {item:w} leave on {day:%Y-%m-%d}
then\tholds_check\tthe warehouse holds {qty:d} {item:w}
then\tlast_move\tthe last movement was on {day:%Y-%m-%d}
then\tout_of_stock\t{item:w} is out of stock
"""

with open("data/features/cart.feature", "w") as f:
    f.write(FEATURE_CART)
with open("data/features/inventory.feature", "w") as f:
    f.write(FEATURE_INV)
with open("data/steps.txt", "w") as f:
    f.write(STEPS)

# an access log in the combined format, with a few lines that do not fit
methods = ["GET", "GET", "GET", "POST", "PUT", "DELETE", "HEAD"]
paths = ["/", "/index.html", "/api/users", "/api/users/42", "/static/app.js", "/login", "/search?q=kara",
         "/favicon.ico"]
agents = ["Mozilla/5.0 (X11; Linux x86_64)", "curl/8.5.0", "Googlebot/2.1", "python-requests/2.31"]
ips = ["10.0.0.%d" % i for i in range(1, 8)] + ["192.168.1.20", "2001:db8::1"]
lines = []
for i in range(160):
    day = 21 + i // 60
    hh = (i * 7) % 24
    mm = (i * 13) % 60
    ss = (i * 29) % 60
    tz = R.choice(["+0000", "+1000", "-0700", "+0530"])
    status = R.choice([200, 200, 200, 200, 304, 404, 500, 301, 201])
    size = "-" if status in (304, 301) else str(R.randint(0, 50000))
    ref = R.choice(["-", "https://example.org/", "https://search.example/?q=x"])
    who = R.choice(["-", "-", "-", "alice", "bob"])
    line = '%s - %s [%02d/Nov/2011:%02d:%02d:%02d %s] "%s %s HTTP/1.1" %d %s "%s" "%s"' % (
        R.choice(ips), who, day, hh, mm, ss, tz, R.choice(methods), R.choice(paths), status, size, ref,
        R.choice(agents))
    lines.append(line)
lines[17] = 'garbage line without structure'
lines[44] = '10.0.0.3 - - [21/Nov/2011:10:00:00 +0000] "GET /a HTTP/1.1" 200 12'
lines[71] = '10.0.0.3 - - [22/Nov/2011:25:00:00 +0000] "GET /b HTTP/1.1" 200 1 "-" "x"'
lines[99] = '10.0.0.3 - - [22/Foo/2011:10:00:00 +0000] "GET /c HTTP/1.1" 200 1 "-" "x"'
lines[120] = '10.0.0.4 - - [23/Nov/2011:01:02:03 +0000] "BREW /pot HTCPCP/1.0" 418 0 "-" "teapot"'
lines[121] = '10.0.0.4 - - [23/Nov/2011:01:02:03 +0000] "GET /x HTTP/1.1" 2OO 5 "-" "x"'
lines[130] = ''
with open("data/access.log", "w") as f:
    f.write("\n".join(lines) + "\n")

applog = []
levels = ["INFO", "INFO", "DEBUG", "WARNING", "ERROR"]
loggers = ["app.web", "app.db", "worker", "app.web.auth"]
for i in range(70):
    t = "2024-03-%02d %02d:%02d:%02d" % (1 + i // 30, (i * 5) % 24, (i * 11) % 60, (i * 17) % 60)
    if i % 9 == 0:
        t += ".%03d" % (i * 37 % 1000)
    if i % 13 == 0:
        t += "Z"
    msg = R.choice(["request served in %d ms" % R.randint(1, 900), "user %s logged in" % R.choice(["al", "bo"]),
                    "cache miss for key k%d" % R.randint(1, 50), "retrying [attempt %d]" % R.randint(1, 3),
                    "disk at %d%%" % R.randint(50, 99)])
    applog.append("%s %s [%s] %s" % (t, R.choice(levels), R.choice(loggers), msg))
applog[5] = "  continuation of a stack trace"
applog[33] = "2024-03-02 99:00:00 INFO [app.web] bad hour"
with open("data/app.log", "w") as f:
    f.write("\n".join(applog) + "\n")

with open("data/page.html", "w") as f:
    f.write('<p>See <a href="https://example.org/">the site</a> and <a href="/docs">the docs</a>.</p>\n'
            '<ul><li><A HREF="/upper">shouting</A></li><li><a href="/two">one</a><a href="/three">two</a></li></ul>\n'
            '<a href="/broken">no end\n<p>then <a href="/later">later</a></p>\n')
with open("data/post.txt", "w") as f:
    f.write("Shipping #kara today! #compilers #rust_lang and #2024 #über, not a#tag. ##double #\n")
with open("data/recipe.txt", "w") as f:
    f.write("Mix 2 cups of flour with 1 cup of milk.\nAdd 3 tbsp of sugar, 10 g of salt and 1 pinch of love.\n"
            "Bake 25 minutes of time.\n")
with open("data/settings.ini", "w") as f:
    f.write("[server]\nhost = example.org\nport = 8080\n\n[client]\nretries = 3\nname = kara client\nempty = \n")
with open("data/code.py", "w") as f:
    f.write("# TODO(ana): handle the empty case.\nx = 1  # TODO(bo): rename this.\n# todo(cy): lower case.\n"
            "# TODO(dee): no full stop\n# TODO(eve): two. sentences.\n")

with open("data/jobs.jsonl", "w") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
print(len(jobs), "jobs")
