#!/usr/bin/env python3
"""Writes data/: the inbox and to-do list of a small reminders tool
(data/inbox/, data/todo.txt), and data/jobs.tsv, the script oracle.py and
mini_parsedatetime.kara both replay.

Each line of jobs.tsv is one step, its fields separated by tabs:

    job      <title>
    now      <y> <m> <d> <H> <M> <S>   the clock time.localtime() reads
    cal      <locale> <version>        a new Calendar(Constants(locale),
                                       version); locale "-" is the default
    set      <name> <value>            an attribute of the Calendar's
                                       Constants (True/False or an int)
    parse    <text> [<version>]        Calendar.parse(text[, version=])
    src      <text> <9 ints>           parse(text, sourceTime=the tuple)
    dt       <text>                    Calendar.parseDT(text)
    nlp      <text>                    Calendar.nlp(text)
    range    <text>                    Calendar.evalRanges(text)
    inc      <6 ints> <month> <year>   Calendar.inc(datetime(...), month,
                                       year); "-" leaves one out
    words    <text>                    Calendar._convertUnitAsWords(text)
    qty      <text>                    Calendar._quantityToReal(text)
    dow      <wd> <wkdy> <offset> <style> <current>
                                       Calendar._CalculateDOWDelta(...)
    pdate    <text>                    Calendar.parseDate(text)
    pdtext   <text>                    Calendar.parseDateText(text)
    agenda   <inbox file> <out file>   every date nlp() finds in each line
                                       of data/inbox/<file>, written to
                                       data/out/<out file>
    todo     <out file>                data/todo.txt's tasks with their due
                                       times, soonest first, written to
                                       data/out/<out file>

In text fields a backslash escapes itself, a tab (\\t) and a newline
(\\n); anything else is literal.

Run: python3 -s -P -B mk.py"""
import os

os.makedirs("data/inbox", exist_ok=True)

INBOX = {
    "standup.txt": """Standup moved to tomorrow at 9:30am.
Retro is next friday at 3pm, bring notes.
Release freeze starts monday; code review by eod.
Out of office from 12/24 to 01/02, back on jan 5th.
Can we sync in 2 hours? Or tomorrow morning.
The quarterly review is on March 31st 2027 at noon.
Remind me 3 days before the launch on 11/20.
No dates in this line at all.
Lunch with the design team at 12:30 pm on Thursday.
Payroll runs at the end of month, invoices go out eom.
""",
    "family.txt": """Dentist appointment Tuesday at 4:15pm.
Pick up the kids at 3:20 today, swim class at 5pm.
Grandma's birthday is Dec 2nd, party the saturday after.
Flight leaves 2026-11-14 at 06:45 from gate 22.
Mom said "call me tonight" and "see you in 2 weeks".
Car service due in 6 months or 5,000 miles.
The lease ends on the 1st of august next year.
Tomorrow: soccer at 10am; Sunday: brunch at 11.
Water the plants every 3 days, next time is friday.
""",
    "ops.txt": """Cert for api.example.test expires 2027-01-15.
Rotate the keys every 90 days; last rotation was 30 days ago.
Maintenance window: 2am - 4am on Sunday.
Backups ran at 01:00:00 and 13:00:00.
Page the on-call if latency stays high for 15 minutes.
Postmortem due within 5 days of the incident (10/19).
Disk will fill in 3 weeks at the current rate.
Next patch tuesday is 11/10, the one after on 12/8.
The 5h job started 45 min ago.
""",
    "empty.txt": "",
}

TODO = """# task | when
Renew passport | in 3 weeks
File taxes | april 15th
Call the plumber | tomorrow at 8am
Team offsite | next friday
Pay rent | eom
Book flights | 2 days from now
Gym | tonight
Water plants | in 72 hours
Quarterly report | 12/31
Replace smoke detector batteries | next month
Dinner reservation | 7:30pm
Haircut | saturday at 11am
Read that book | someday
Dentist | 11/03/2026 2:15pm
Vet | thursday 9am
"""

for name, text in INBOX.items():
    with open(os.path.join("data/inbox", name), "w", encoding="utf-8") as f:
        f.write(text)
with open("data/todo.txt", "w", encoding="utf-8") as f:
    f.write(TODO)

WORDS = """now|right now|today|tomorrow|yesterday|noon|midnight|lunch|breakfast|dinner
morning|afternoon|evening|night|tonight|eod|eom|eoy|monday|tue|tues|wed|thu
friday|sat|sun|sunday|next monday|last friday|this friday|next sunday
last sunday|previous tuesday|prior wednesday|prev thu|next week|last week
this week|next month|last month|this month|end of month|end of week
end of day|end of year|next year|last year|this year|next hour|last hour
this hour|next day|last day|this day|next minute""".replace("\n", "|").split("|")

UNITS = """in 5 minutes|in 2 hours|5 hours ago|3 days ago|2 weeks ago|in 3 weeks
in 6 months|2 years ago|in 1.5 hours|2.5 days|0.5 months|1.25 years|-3 days
10 secs|45 min|1 hr|a day|an hour|two weeks|five days ago|twenty minutes
eleven hours|twelve days|ten years ago|zero days|in 0 hours|100 days
in 1000 days|90 days ago|5h|30m|2d|1w|3y|5 h 30 m|2 d ago|in 10 s
5 hours 30 minutes|1 day 2 hours|3 mins|2 mths|in 13 months|36 months ago
1,5 hours|in 99999 years|in 10000 days|in 5000000 days|7 wk|4 dy|2 yr
in 3.75 weeks|0.1 seconds|in 2,5 days""".replace("\n", "|").split("|")

TIMES = """5pm|5 pm|5:30pm|5:30 p.m.|5:30 P.M.|17:45|9:05:30|12am|12pm|12:15 am
12:00 pm|0930|1700|24:00|25:00|23:59:59|7a|7p|11 a.m.|noon tomorrow
tomorrow at noon|tomorrow 5pm|friday at 9am|next friday at 5pm|monday 10:30
at 6:15|6.30pm|12:60|9:5|10:00:60|13pm|0am|00:00|8:00:00.250|at 9""".replace("\n", "|").split("|")

DATES = """march 31|march 31st|mar 3rd 2027|may 2027|july 4th|dec 25|december 25, 2026
jan 1st|feb 29|feb 29 2028|31 august|1st march|2nd feb 2027|sept 9|october
nov 2026|the 31st|31st|1st|3rd of march|12/25|12/25/2026|12/25/26|2026-12-25
2026/1/5|1.5.2027|13/25|02/30|5/6/49|5/6/50|2026.12.31|10/23|10/22|1/1/1999
7-4|30/12/2026|aug 21 2007|august 32|june 0|feb 30 2027""".replace("\n", "|").split("|")

COMBOS = """3 days after tomorrow|2 hours before noon|one day before thursday
2 days after friday|a week from today|10 minutes after 4pm|3 weeks from now
next 4 hrs|in 2 days at 3pm|tomorrow at 6:45pm|the day after tomorrow
1 1/2 hours|5 days from monday|an hour before midnight|2 weeks after dec 25
3 months from now|1 year ago today|monday next week|next friday 9am
last monday at noon|dec 25 at 7pm|12/25 at 7pm|7pm on dec 25
tomorrow morning|friday evening|yesterday afternoon|tonight at 11
2 hours after 2026-10-30 10:00|next week monday|eod friday|eod tomorrow""".replace("\n", "|").split("|")

ODD = ["", "   ", "hello world", "xyz o'clock", "at", "next", "in", "from",
       "'tomorrow'", '"friday"', "tomorrow.", "mon. at 5pm", "Tomorrow", "NEXT WEEK",
       "TOMORROW AT 5PM", "  friday  ", "5 cats", "in a while", "-", "--", "in -3 days",
       "1-2", "week", "month", "monday monday", "noon noon", "a.m.", "p",
       "12/25/2026 5pm", "5pm 12/25/2026", "tomorrow tomorrow", "next next week",
       "jan", "j", "0", "00", "1", "31", "32", "2026", "99", "2026 10 23"]

RANGES = ["4-5pm", "4:30-5pm", "10am - 2pm", "4:00:55 pm - 5:90:44 am", "4p-5p",
          "06/07/06 - 08/09/06", "march 31 - june 1st, 2006", "Aug 21 - Sep 4, 2007",
          "march 1rd -13th", "march 1st - 13th", "9:30 - 11:00", "next week", "",
          "tomorrow 4-5pm", "4 - 5", "10:00-11:30", "9am-5pm tomorrow", "1/2 - 3/4",
          "july 4 - 7", "dec 24 - jan 2", "8:00 - 17:00 friday", "2-3am", "noon - 2pm",
          "march 3 - april 4", "4-5", "5pm-4pm", "nov 1 - 15th, 2026"]

NLP = ["Let's meet tomorrow at 5pm or next friday at noon, not 3 days ago.",
       "I'll be there in 2 hours.",
       "The meeting is on March 31st at 3pm in room 4.",
       "Call me at 9:30 tonight or tomorrow morning.",
       "From 12/24 to 01/02 the office is closed.",
       "Next is the word month.",
       "Ship it next month, review next week, and celebrate next year.",
       "On monday at 10am we plan; on friday we ship.",
       "Nothing to see here.",
       "",
       "Back in 5 minutes.",
       "the 5pm train, the 6:15 bus, and the 7 a.m. ferry",
       "Due 2026-11-30, reminder 3 days before.",
       "It happened 2 weeks ago yesterday.",
       "at noon on dec 25 and at midnight on dec 31",
       "Pay 5 dollars in 2 days, then 10 on the 1st.",
       "Lunch at 12:30 pm, dinner at 7:00 pm.",
       "Mom said \"call me tonight\" and \"see you in 2 weeks\".",
       "in 3 hours in 4 hours in 5 hours",
       "tomorrow tomorrow tomorrow",
       "Sync at eod, then again next monday at 9."]

L = []


def esc(t):
    return t.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n")


def step(*fields):
    L.append("\t".join(str(f) for f in fields))


def clock(y, m, d, H, M, S):
    step("now", y, m, d, H, M, S)


step("job", "every phrase on a friday afternoon")
clock(2026, 10, 23, 14, 30, 15)
step("cal", "-", 2)
for t in WORDS + UNITS + TIMES + DATES + COMBOS + ODD:
    step("parse", esc(t))

step("job", "the old flag style and parseDT")
step("cal", "-", 1)
for t in WORDS[:20] + UNITS[:20] + TIMES[:20] + DATES[:20] + COMBOS[:20] + ODD[:10]:
    step("parse", esc(t))
for t in ["tomorrow at 5pm", "noon", "3 days ago", "dec 25", "next week", "hello", "17:45:30"]:
    step("dt", esc(t))
    step("parse", esc(t), 2)

step("job", "other clocks")
for c in [(2026, 2, 2, 8, 0, 0), (2025, 12, 31, 23, 59, 59), (2028, 2, 29, 12, 0, 0),
          (2026, 1, 31, 0, 0, 0), (2027, 3, 14, 1, 59, 26), (2026, 10, 25, 9, 0, 0)]:
    clock(*c)
    step("cal", "-", 2)
    for t in WORDS[3:40:2] + UNITS[:30:3] + TIMES[:20:2] + DATES[:42:2] + COMBOS[:30:3]:
        step("parse", esc(t))

step("job", "the edges of the calendar")
for c in [(9999, 12, 15, 10, 0, 0), (9999, 12, 31, 23, 0, 0), (1, 1, 2, 0, 0, 0)]:
    clock(*c)
    step("cal", "-", 2)
    for t in ["next month", "next year", "in 2 weeks", "tomorrow", "yesterday", "in 30 days",
              "3 days ago", "next week", "last month", "2 years ago", "in 1 year", "eom",
              "eoy", "monday", "last monday", "this week", "1 month ago", "in 3 months",
              "jan 5", "12/25", "dec 25 2000", "in 100 years", "noon", "in 1 hour"]:
        step("parse", esc(t))

step("job", "an explicit source time")
clock(2026, 10, 23, 14, 30, 15)
step("cal", "-", 2)
for st in [(2026, 1, 15, 10, 0, 0, 3, 15, 0), (2026, 6, 30, 23, 0, 0, 0, 0, -1),
           (2024, 2, 29, 6, 30, 0, 3, 60, 1), (2026, 12, 31, 18, 45, 30, 3, 365, 0)]:
    for t in ["tomorrow", "next month", "in 3 days", "friday", "noon", "5pm", "eom",
              "next year", "march 1", "12/25", "2 weeks ago", "monday at 9", "now", "", "hello"]:
        step("src", esc(t), *st)

step("job", "the constants")
clock(2026, 10, 21, 16, 5, 0)
for name, value in [("StartHour", 8), ("StartTimeFromSourceTime", True), ("YearParseStyle", 0),
                    ("DOWParseStyle", -1), ("DOWParseStyle", 0), ("CurrentDOWParseStyle", True),
                    ("BirthdayEpoch", 30), ("StartHour", 0), ("StartHour", 24)]:
    step("cal", "-", 2)
    step("set", name, value)
    for t in ["tomorrow", "next week", "wednesday", "tuesday", "thursday", "next wednesday",
              "last wednesday", "next month", "3 days ago", "jan 5", "oct 21", "oct 20",
              "5/6/29", "5/6/31", "5/6/99", "eom", "yesterday", "monday"]:
        step("parse", esc(t))

step("job", "the australian locale")
clock(2026, 10, 23, 14, 30, 15)
step("cal", "en_AU", 2)
for t in ["12/05", "12/05/2027", "05-12-2027", "25/12", "13/1/27", "1/13/27", "2026-12-25",
          "12.05.2027", "31/4", "tomorrow", "next friday at 5pm", "dec 25", "25 dec",
          "4-5pm", "12/05 at 9am"]:
    step("parse", esc(t))
for t in ["06/07/06 - 08/09/06", "25-12-2026 - 1-1-2027"]:
    step("range", esc(t))
step("cal", "en_US", 2)
for t in ["12/05", "05-12-2027", "25/12"]:
    step("parse", esc(t))
step("cal", "fr_FR_missing", 2)
step("parse", esc("12/05"))

step("job", "ranges")
step("cal", "-", 2)
for t in RANGES:
    step("range", esc(t))
step("cal", "-", 1)
for t in RANGES[:8]:
    step("range", esc(t))

step("job", "finding dates in text")
step("cal", "-", 2)
for t in NLP:
    step("nlp", esc(t))
step("cal", "-", 1)
for t in NLP[:6]:
    step("nlp", esc(t))

step("job", "the helpers")
step("cal", "-", 2)
for args in [(2026, 1, 31, 9, 0, 0, 1, "-"), (2026, 1, 31, 9, 0, 0, "-", 1),
             (2024, 2, 29, 0, 0, 0, "-", 1), (2026, 3, 31, 12, 0, 0, -1, "-"),
             (2026, 10, 23, 0, 0, 0, 2.5, "-"), (2026, 10, 23, 0, 0, 0, -0.5, "-"),
             (2026, 10, 23, 0, 0, 0, 13, "-"), (2026, 10, 23, 0, 0, 0, -13, "-"),
             (2026, 10, 23, 0, 0, 0, 0, 0), (2026, 10, 23, 0, 0, 0, "-", 0.5),
             (2026, 10, 23, 0, 0, 0, "-", -1.25), (2026, 1, 1, 0, 0, 0, 12, "-"),
             (2026, 1, 1, 0, 0, 0, -12, "-"), (2026, 12, 15, 0, 0, 0, 1, "-"),
             (9999, 6, 1, 0, 0, 0, "-", 1), (1, 6, 1, 0, 0, 0, -7, "-"),
             (2026, 5, 31, 6, 7, 8, 1.5, 1.5), (2026, 10, 23, 0, 0, 0, "x", "-")]:
    step("inc", *args)
for t in ["one", "twenty one", "twenty-one", "one hundred", "one hundred and five",
          "two thousand twenty six", "three million, four hundred thousand and seven",
          "ninety nine", "a hundred", "", "eleven", "twelve hundred", "one billion",
          "seven thousand, two", "five dozen", "zero", "one quintillion"]:
    step("words", esc(t))
for t in ["", "5", "2.5", "1,5", "five", "a", "an", "twelve", "-3", " 7 ", "x", "1e3", "0.000"]:
    step("qty", esc(t))
for wd in range(7):
    for wkdy in [0, 3, 6]:
        for off in [-1, 0, 1, 2]:
            step("dow", wd, wkdy, off, 1, 0)
for args in [(4, 4, 2, 1, 1), (4, 4, 2, -1, 0), (4, 1, 2, -1, 0), (4, 1, 2, 0, 0),
             (4, 6, 2, 0, 1), (0, 6, 2, -1, 0), (6, 0, 1, -1, 0), (6, 0, -1, 1, 0),
             (3, 3, 2, 5, 0), (3, 3, 2, 5, 1)]:
    step("dow", *args)
for t in ["05/28/2006", "04.21", "12/25", "1/1/1", "13/1", "2/29", "2/29/2028", "2026/02/03",
          "10/23", "10/24", "6/6/49", "6/6/50", "0/0"]:
    step("pdate", esc(t))
for t in ["may 31st, 2006", "jan 1st", "july 2006", "oct 23", "oct 22", "feb 30",
          "december", "mar 5th 49", "mar 5th 50", "sep 31 2026"]:
    step("pdtext", esc(t))

step("job", "the reminders tool")
clock(2026, 10, 23, 14, 30, 15)
step("cal", "-", 2)
for name in sorted(INBOX):
    step("agenda", name, name.replace(".txt", ".agenda"))
step("todo", "todo.sorted")
clock(2026, 12, 30, 20, 0, 0)
step("todo", "todo.late")

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
