"""Write data/jobs.tsv and the dictionary and keyboard files the port reads.

zxcvbn is the password strength estimator behind many sign-up forms: it
looks for dictionary words (with capitals, reversals and l33t
substitutions), keyboard walks, repeats, sequences, years and dates, and
scores the cheapest way to guess the whole password. The jobs are the
passwords a sign-up form sees, with the user's own name and birth year as
extra dictionary words where a form would pass them.

data/frequency_lists.tsv and data/adjacency_graphs.tsv are written from the
vendored library's own data, so the port and the library rank words and
walk keyboards from the same tables.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
sys.path.insert(0, os.path.join(HERE, "vendor"))

from zxcvbn.adjacency_graphs import ADJACENCY_GRAPHS  # noqa: E402
from zxcvbn.frequency_lists import FREQUENCY_LISTS  # noqa: E402

JOBS = []


def job(*fields):
    JOBS.append("\t".join(str(f) for f in fields))


def section(title):
    JOBS.append("# " + title)


section("common passwords")
for pw in ["password", "123456", "qwerty", "letmein", "dragon", "iloveyou",
           "trustno1", "monkey", "football", "hunter2", "baseball1",
           "superman", "master", "shadow", "michael"]:
    job("check", pw)

section("capitals, reversals and l33t")
for pw in ["Password", "PASSWORD", "passworD", "PassWord", "pAsSwOrD",
           "drowssap", "Drowssap", "ytrewq", "P@ssw0rd", "p4$$w0rd",
           "Tr0ub4dor&3", "l33tsp34k", "4ndr01d", "s3cr3t", "@dm1n",
           "|_|$3r", "5h4d0w", "$uperm4n", "m0nk3y!", "1l0v3y0u"]:
    job("check", pw)

section("keyboard walks")
for pw in ["qwertyuiop", "asdfghjkl;", "zxcvbnm", "1qaz2wsx", "qazwsxedc",
           "!@#$%^&*()", "~!@#$%", "QWERTY", "Qwerty123", "poiuytrewq",
           "kxpdx", "aoeuidhtns", "7894561230", "147258369", "159753",
           "963852741", "qwER43@!", "plmnko", "zaq12wsx", "1q2w3e4r5t"]:
    job("check", pw)

section("repeats and sequences")
for pw in ["aaaaaa", "zzzzzzzzzzzz", "abcabcabc", "aabaabaabaab", "abab",
           "123123123", "xyzxyz", "abcdef", "zyxwvu", "13579", "9753",
           "ABCDEFG", "abcdb975zy", "acegikmoqs", "0123456789",
           "racecar", "neveroddoreven", "hellohello", "byebyebye!",
           "AbCdEfGh"]:
    job("check", pw)

section("years and dates")
for pw in ["1991", "2015", "2049", "19910101", "01/01/1991", "1-1-91",
           "2015_06_04", "111504", "12.25.2016", "31 12 1999", "1/1/1",
           "summer2023", "Summer2023!", "winter1987", "born2012",
           "13131313", "4/31/2001", "20201220", "7.7.77", "2000-02-29"]:
    job("check", pw)

section("phrases and strong passwords")
for pw in ["correcthorsebatterystaple", "correct horse battery staple",
           "Tr0ub4dor&3", "WinterIsComing", "ihavealongpassword",
           "D0g.....................", "rWibMFACxAUGZmxhVncy",
           "Ba9ZyWABu99[BK#6MBgbH88Tofv)vs$w", "x7#Qm!2pL", "jK8$nB3@vR",
           "thisisaverylongpasswordthatnobodycouldguess",
           "The quick brown fox", "CorrectHorse", "purple-monkey-dishwasher",
           "a", "!", "", "  ", "Zürich2024!", "Ήλιος", "пароль123",
           "ÀÉÎÕÜ", "日本語のパスワード"]:
    job("check", pw)

section("user inputs")
job("check", "JohnSmith123", "John", "Smith")
job("check", "johnsmith", "John", "Smith")
job("check", "jane.doe1985", "Jane", "Doe", "int:1985")
job("check", "jane1985")
job("check", "acme-corp-2024", "ACME", "acme.example")
job("check", "Rex4ever", "rex", "rex", "4ever")
job("check", "8675309jenny", "int:8675309")
job("matches", "acme2024")
job("check", "acme2024")
job("matches", "acme2024")

section("matcher views")
for pw in ["P@ssw0rd", "abcabcabc", "aabaabaabaab", "qwerty123", "1991-12-31",
           "abcdb975zy", "!@#$%^", "Pa$$w0rd!!", "4ll0w3d", "1|1|1|1"]:
    job("matches", pw)
for pw in ["p4$$w0rd", "!@#$%^&*()", "1|1|1|1", "4ll0w3d", "nothing",
           "c0(]<[3", "%%22++77"]:
    job("subs", pw)

section("length limits")
job("check", "x" * 72)
job("check", "x" * 73)
job("check", "y" * 80, "max_length=100")
job("check", "abc", "max_length=2")
job("check", "Tr0ub4dor&3" * 6)

section("attack times")
for g in ["0", "1", "1004", "1005", "1006", "999999", "1000005", "1000006",
          "100000004", "100000005", "10000000004", "10000000005",
          "36", "3600", "86400", "2678400", "32140800", "3214080000",
          "321408000000", "1e20", "12345.678", "7.5", "0.5", "2.5"]:
    job("time", g)


def main():
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "frequency_lists.tsv"), "w",
              encoding="ascii") as fh:
        for name, words in FREQUENCY_LISTS.items():
            fh.write(name + "\t" + ",".join(words) + "\n")
    with open(os.path.join(DATA, "adjacency_graphs.tsv"), "w",
              encoding="ascii") as fh:
        for name, graph in ADJACENCY_GRAPHS.items():
            for key, adjacent in graph.items():
                cells = [a if a is not None else "" for a in adjacent]
                fh.write("\t".join([name, key] + cells) + "\n")
    with open(os.path.join(DATA, "jobs.tsv"), "w", encoding="utf-8") as fh:
        for line in JOBS:
            fh.write(line + "\n")
    with open(os.path.join(DATA, "files.txt"), "w", encoding="utf-8") as fh:
        fh.write("frequency_lists.tsv\nadjacency_graphs.tsv\n")


main()
