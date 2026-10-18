#!/usr/bin/env python3
"""Writes data/rules/*.rrule: each file is an iCalendar recurrence (the
lines rrulestr parses), a `--` line, and the queries to run on it. A first
line starting with `@` names rrulestr options (unfold, forceset,
compatible). See README.md for the queries."""
import os
import shutil

shutil.rmtree("data", ignore_errors=True)
os.makedirs("data/rules")

n = 0


def rule(name, text, queries, opts=""):
    global n
    n += 1
    body = ""
    if opts:
        body += "@ " + opts + "\n"
    body += text.strip("\n") + "\n--\n" + queries.strip("\n") + "\n"
    with open("data/rules/%03d-%s.rrule" % (n, name), "w") as f:
        f.write(body)


RFC = "DTSTART:19970902T090000\n"

# ------------------------------------------------ RFC 5545 section 3.8.5.3

rule("daily-10", RFC + "RRULE:FREQ=DAILY;COUNT=10", "all\nstr\ncount")
rule("daily-until", RFC + "RRULE:FREQ=DAILY;UNTIL=19971224T000000",
     "count\nlist 3\nbefore 19971224T000000\nat -1\nstr")
rule("every-other-day", RFC + "RRULE:FREQ=DAILY;INTERVAL=2",
     "list 6\nafter 19971231T000000\nbetween 19971001 19971010\nstr")
rule("every-10-days-5", RFC + "RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5", "all")
rule("january-3-years-yearly",
     "DTSTART:19980101T090000\n"
     "RRULE:FREQ=YEARLY;UNTIL=20000131T140000;BYMONTH=1;BYDAY=SU,MO,TU,WE,TH,FR,SA",
     "count\nlist 3\nat 31\nat -1\nstr")
rule("january-3-years-daily",
     "DTSTART:19980101T090000\nRRULE:FREQ=DAILY;UNTIL=20000131T140000;BYMONTH=1",
     "count\nat 31\nat -1\nstr")
rule("weekly-10", RFC + "RRULE:FREQ=WEEKLY;COUNT=10", "all\nstr")
rule("weekly-until", RFC + "RRULE:FREQ=WEEKLY;UNTIL=19971224T000000",
     "count\nat -1")
rule("every-other-week", RFC + "RRULE:FREQ=WEEKLY;INTERVAL=2;WKST=SU",
     "list 8\nstr")
rule("weekly-tu-th-until",
     "DTSTART:19970902T090000\nRRULE:FREQ=WEEKLY;UNTIL=19971007T000000;WKST=SU;BYDAY=TU,TH",
     "all\nstr")
rule("weekly-tu-th-count", RFC + "RRULE:FREQ=WEEKLY;COUNT=10;WKST=SU;BYDAY=TU,TH",
     "all")
rule("mo-we-fri-other-week",
     "DTSTART:19970901T090000\n"
     "RRULE:FREQ=WEEKLY;INTERVAL=2;UNTIL=19971224T000000;WKST=SU;BYDAY=MO,WE,FR",
     "count\nlist 6\nat -1\nstr")
rule("tu-th-other-week-8", RFC + "RRULE:FREQ=WEEKLY;INTERVAL=2;COUNT=8;WKST=SU;BYDAY=TU,TH",
     "all")
rule("first-friday-10", "DTSTART:19970905T090000\nRRULE:FREQ=MONTHLY;COUNT=10;BYDAY=1FR",
     "all\nstr")
rule("first-friday-until",
     "DTSTART:19970905T090000\nRRULE:FREQ=MONTHLY;UNTIL=19971224T000000;BYDAY=1FR",
     "all")
rule("first-last-sunday-other-month",
     "DTSTART:19970907T090000\nRRULE:FREQ=MONTHLY;INTERVAL=2;COUNT=10;BYDAY=1SU,-1SU",
     "all\nstr")
rule("second-to-last-monday",
     "DTSTART:19970922T090000\nRRULE:FREQ=MONTHLY;COUNT=6;BYDAY=-2MO", "all")
rule("third-to-last-day", "DTSTART:19970928T090000\nRRULE:FREQ=MONTHLY;BYMONTHDAY=-3",
     "list 6\nstr")
rule("2nd-and-15th", RFC + "RRULE:FREQ=MONTHLY;COUNT=10;BYMONTHDAY=2,15", "all")
rule("first-and-last-day",
     "DTSTART:19970930T090000\nRRULE:FREQ=MONTHLY;COUNT=10;BYMONTHDAY=1,-1",
     "all\nstr")
rule("every-18-months-10th-to-15th",
     "DTSTART:19970910T090000\n"
     "RRULE:FREQ=MONTHLY;INTERVAL=18;COUNT=10;BYMONTHDAY=10,11,12,13,14,15",
     "all")
rule("tuesday-other-month", RFC + "RRULE:FREQ=MONTHLY;INTERVAL=2;BYDAY=TU",
     "list 18\nstr")
rule("june-july-yearly", "DTSTART:19970610T090000\nRRULE:FREQ=YEARLY;COUNT=10;BYMONTH=6,7",
     "all\nstr")
rule("every-other-year-jan-feb-mar",
     "DTSTART:19970310T090000\nRRULE:FREQ=YEARLY;INTERVAL=2;COUNT=10;BYMONTH=1,2,3",
     "all")
rule("every-third-year-yeardays",
     "DTSTART:19970101T090000\nRRULE:FREQ=YEARLY;INTERVAL=3;COUNT=10;BYYEARDAY=1,100,200",
     "all\nstr")
rule("20th-monday", "DTSTART:19970519T090000\nRRULE:FREQ=YEARLY;BYDAY=20MO",
     "list 3\nstr")
rule("monday-of-week-20", "DTSTART:19970512T090000\nRRULE:FREQ=YEARLY;BYWEEKNO=20;BYDAY=MO",
     "list 3\nstr")
rule("thursdays-in-march", "DTSTART:19970313T090000\nRRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=TH",
     "list 11")
rule("thursdays-in-summer",
     "DTSTART:19970605T090000\nRRULE:FREQ=YEARLY;BYDAY=TH;BYMONTH=6,7,8", "list 39")
rule("friday-13th",
     "DTSTART:19970902T090000\nEXDATE:19970902T090000\nRRULE:FREQ=MONTHLY;BYDAY=FR;BYMONTHDAY=13",
     "list 5")
rule("saturday-after-first-sunday",
     "DTSTART:19970913T090000\nRRULE:FREQ=MONTHLY;BYDAY=SA;BYMONTHDAY=7,8,9,10,11,12,13",
     "list 10\nstr")
rule("us-election-day",
     "DTSTART:19961105T090000\n"
     "RRULE:FREQ=YEARLY;INTERVAL=4;BYMONTH=11;BYDAY=TU;BYMONTHDAY=2,3,4,5,6,7,8",
     "list 3\nstr")
rule("third-tue-wed-thu",
     "DTSTART:19970904T090000\nRRULE:FREQ=MONTHLY;COUNT=3;BYDAY=TU,WE,TH;BYSETPOS=3",
     "all\nstr")
rule("second-to-last-weekday",
     "DTSTART:19970929T090000\nRRULE:FREQ=MONTHLY;BYDAY=MO,TU,WE,TH,FR;BYSETPOS=-2",
     "list 7\nstr")
rule("every-3-hours-until",
     RFC + "RRULE:FREQ=HOURLY;INTERVAL=3;UNTIL=19970902T170000", "all\nstr")
rule("every-15-minutes-6", RFC + "RRULE:FREQ=MINUTELY;INTERVAL=15;COUNT=6", "all")
rule("every-90-minutes-4", RFC + "RRULE:FREQ=MINUTELY;INTERVAL=90;COUNT=4", "all")
rule("every-20-minutes-byhour",
     RFC + "RRULE:FREQ=DAILY;BYHOUR=9,10,11,12,13,14,15,16;BYMINUTE=0,20,40",
     "list 26\nstr")
rule("every-20-minutes-minutely",
     RFC + "RRULE:FREQ=MINUTELY;INTERVAL=20;BYHOUR=9,10,11,12,13,14,15,16",
     "list 26\nstr")
rule("wkst-monday",
     "DTSTART:19970805T090000\nRRULE:FREQ=WEEKLY;INTERVAL=2;COUNT=4;BYDAY=TU,SU;WKST=MO",
     "all\nstr")
rule("wkst-sunday",
     "DTSTART:19970805T090000\nRRULE:FREQ=WEEKLY;INTERVAL=2;COUNT=4;BYDAY=TU,SU;WKST=SU",
     "all\nstr")
rule("feb-30-ignored", "DTSTART:20070115T090000\nRRULE:FREQ=MONTHLY;BYMONTHDAY=15,30;COUNT=5",
     "all")

# ------------------------------------------------ dateutil's own cases

rule("monthly-31st-skips",
     "DTSTART:20141231T000000\nRRULE:FREQ=MONTHLY;COUNT=7", "all\nstr")
rule("leap-day-yearly", "DTSTART:20000229T120000\nRRULE:FREQ=YEARLY;COUNT=4",
     "all\nstr")
rule("leap-day-by-yearday",
     "DTSTART:19960101T000000\nRRULE:FREQ=YEARLY;COUNT=6;BYYEARDAY=60,-306",
     "all")
rule("last-day-of-year", "DTSTART:19970101T000000\nRRULE:FREQ=YEARLY;COUNT=4;BYYEARDAY=-1",
     "all")
rule("week-53", "DTSTART:19970101T090000\nRRULE:FREQ=YEARLY;COUNT=3;BYWEEKNO=53;BYDAY=MO",
     "all\nstr")
rule("last-week", "DTSTART:19970101T090000\nRRULE:FREQ=YEARLY;COUNT=6;BYWEEKNO=-1;BYDAY=MO,SU",
     "all")
rule("week-1-crosses-year",
     "DTSTART:19970101T090000\nRRULE:FREQ=YEARLY;COUNT=8;BYWEEKNO=1",
     "all")
rule("week-1-wkst-sunday",
     "DTSTART:19970101T090000\nRRULE:FREQ=YEARLY;COUNT=6;BYWEEKNO=1;BYDAY=SU,SA;WKST=SU",
     "all\nstr")
rule("week-52-53-daily",
     "DTSTART:19981225T090000\nRRULE:FREQ=DAILY;COUNT=12;BYWEEKNO=52,53", "all")
rule("easter-sunday", "DTSTART:19970101T090000\nRRULE:FREQ=YEARLY;COUNT=6;BYEASTER=0",
     "all\nstr")
rule("easter-holidays",
     "DTSTART:20200101T100000\nRRULE:FREQ=YEARLY;COUNT=12;BYEASTER=-2,1,39,50",
     "all\nstr")
rule("easter-saturdays-near",
     "DTSTART:20240101T080000\nRRULE:FREQ=WEEKLY;COUNT=4;BYEASTER=-1,6;BYDAY=SA",
     "all")
rule("yearly-nth-weekday-by-month",
     "DTSTART:20240101T180000\nRRULE:FREQ=YEARLY;COUNT=8;BYMONTH=5,11;BYDAY=-1MO,4TH",
     "all\nstr")
rule("yearly-setpos-last-workday",
     "DTSTART:20231201T170000\nRRULE:FREQ=YEARLY;COUNT=4;BYDAY=MO,TU,WE,TH,FR;BYSETPOS=-1",
     "all")
rule("monthly-setpos-times",
     "DTSTART:20240101T080000\n"
     "RRULE:FREQ=MONTHLY;COUNT=6;BYDAY=MO;BYHOUR=8,16;BYSETPOS=1,-1,2",
     "all\nstr")
rule("weekly-setpos-negative-times",
     "DTSTART:20240304T000000\n"
     "RRULE:FREQ=WEEKLY;COUNT=5;BYDAY=MO,FR;BYHOUR=9,12,15;BYMINUTE=30;BYSETPOS=-2,4",
     "all")
rule("hourly-byhour-construct",
     "DTSTART:20240101T170000\nRRULE:FREQ=HOURLY;INTERVAL=4;BYHOUR=1,2,5,7,13,21;COUNT=9",
     "all\nstr")
rule("hourly-filtered-by-weekday",
     "DTSTART:20240105T200000\nRRULE:FREQ=HOURLY;INTERVAL=5;BYDAY=MO;COUNT=8",
     "all")
rule("minutely-byminute-construct",
     "DTSTART:20240101T000700\nRRULE:FREQ=MINUTELY;INTERVAL=10;BYMINUTE=7,17,27,50;COUNT=6",
     "all\nstr")
rule("minutely-byhour-night",
     "DTSTART:20240101T224500\nRRULE:FREQ=MINUTELY;INTERVAL=25;BYHOUR=23,0;COUNT=8",
     "all")
rule("secondly-small",
     "DTSTART:20240101T235958\nRRULE:FREQ=SECONDLY;INTERVAL=7;COUNT=5", "all\nstr")
rule("secondly-bysecond",
     "DTSTART:20240101T120000\nRRULE:FREQ=SECONDLY;INTERVAL=15;BYSECOND=0,30;BYMINUTE=0,1;COUNT=6",
     "all")
rule("daily-bysecond-timeset",
     "DTSTART:20240101T060000\nRRULE:FREQ=DAILY;COUNT=6;BYHOUR=6,18;BYMINUTE=0,30;BYSECOND=15",
     "all\nstr")
rule("yearly-bymonthday-negative-february",
     "DTSTART:20230101T000000\nRRULE:FREQ=YEARLY;COUNT=4;BYMONTH=2;BYMONTHDAY=-1,-29",
     "all\nstr")
rule("weekly-cross-year",
     "DTSTART:20241230T090000\nRRULE:FREQ=WEEKLY;COUNT=6;BYDAY=MO,WE,FR;BYYEARDAY=1,2,3,-1,-2,363,364,365",
     "all")
rule("monthly-interval-wrap",
     "DTSTART:20231115T100000\nRRULE:FREQ=MONTHLY;INTERVAL=5;COUNT=6", "all")
rule("yearly-many-months-daily-time",
     "DTSTART:20240131T233000\nRRULE:FREQ=DAILY;INTERVAL=29;COUNT=8", "all")

# ------------------------------------------------ queries on long rules

rule("standup-weekdays",
     "DTSTART:20240102T093000\nRRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR",
     "after 20240105T093000\nafter 20240105T093000 inc\nbefore 20240108T093000\n"
     "before 20240108T093000 inc\nbetween 20240110 20240117\n"
     "between 20240110T093000 20240117T093000 inc\nin 20240110T093000\nin 20240113T093000\n"
     "at 0\nat 9\nxafter 20240301 4\nxafter 20240301T093000 3 inc")
rule("payday-15th-and-last",
     "DTSTART:20240115T000000\nRRULE:FREQ=MONTHLY;BYMONTHDAY=15,-1;BYDAY=MO,TU,WE,TH,FR",
     "list 8\nbetween 20240601 20241231\nafter 20240831")
rule("billing-until-count",
     "DTSTART:20240131T080000\nRRULE:FREQ=MONTHLY;BYMONTHDAY=-1;UNTIL=20241231T235959",
     "count\nall\nat 3\nat 12\nat -12\nat -13\nin 20240229T080000\nstr")

# ------------------------------------------------ sets

rule("set-exdate",
     "DTSTART:19970902T090000\nRRULE:FREQ=DAILY;COUNT=10\n"
     "EXDATE:19970904T090000,19970906T090000\nEXDATE:19970910T090000",
     "all\ncount\nin 19970904T090000")
rule("set-rdate",
     "DTSTART:20240101T100000\nRRULE:FREQ=WEEKLY;COUNT=4\n"
     "RDATE:20240103T150000,20240101T100000\nRDATE:20231225T100000",
     "all\nafter 20240101T100000\nbefore 20240101T100000")
rule("set-exrule",
     "DTSTART:20240101T090000\nRRULE:FREQ=DAILY;COUNT=21\nEXRULE:FREQ=WEEKLY;BYDAY=SA,SU",
     "all\ncount")
rule("set-two-rrules",
     "DTSTART:20240101T090000\nRRULE:FREQ=WEEKLY;COUNT=4;BYDAY=MO\n"
     "RRULE:FREQ=WEEKLY;COUNT=4;BYDAY=MO,TH;BYHOUR=9,14",
     "all\ncount\nat -2")
rule("set-exdate-date-value",
     "DTSTART:20240101T000000\nRRULE:FREQ=DAILY;COUNT=6\nEXDATE;VALUE=DATE:20240102,20240105",
     "all")
rule("set-forceset", RFC + "RRULE:FREQ=YEARLY;COUNT=3", "all\ncount", "forceset")
rule("set-compatible-adds-dtstart",
     "DTSTART:20240103T120000\nRRULE:FREQ=WEEKLY;COUNT=3;BYDAY=FR", "all", "compatible")
rule("set-exrule-infinite",
     "DTSTART:20240101T080000\nRRULE:FREQ=DAILY\nEXRULE:FREQ=DAILY;INTERVAL=3\n"
     "EXDATE:20240105T080000",
     "list 6\nafter 20240201\nbetween 20240301 20240310\nat 4")
rule("unfold-continued",
     "DTSTART:20240101T090000\nRRULE:FREQ=MONTHLY;COUNT=4;\n BYDAY=MO;BYSETPOS=2\n\n"
     "EXDATE:20240212T090000",
     "all", "unfold")
rule("lowercase-rule",
     "dtstart:20240301T070000\nrrule:freq=weekly;count=3;byday=sa;wkst=su",
     "all\nstr")
rule("bare-rule-line",
     "DTSTART:20240301T070000 FREQ=DAILY;INTERVAL=3;COUNT=3", "all\nstr")

# ------------------------------------------------ errors

rule("err-freq", RFC + "RRULE:FREQ=FORTNIGHTLY;COUNT=3", "all")
rule("err-count", RFC + "RRULE:FREQ=DAILY;COUNT=TEN", "all")
rule("err-unknown-part", RFC + "RRULE:FREQ=DAILY;COUNT=3;BYFORTNIGHT=2", "all")
rule("err-byday", RFC + "RRULE:FREQ=WEEKLY;BYDAY=MO,XX", "all")
rule("err-byday-zero", RFC + "RRULE:FREQ=MONTHLY;BYDAY=0MO", "all")
rule("err-byday-empty", RFC + "RRULE:FREQ=MONTHLY;BYDAY=MO,,TU", "all")
rule("err-bysetpos", RFC + "RRULE:FREQ=MONTHLY;BYDAY=MO;BYSETPOS=0", "all")
rule("err-bysetpos-range", RFC + "RRULE:FREQ=MONTHLY;BYDAY=MO;BYSETPOS=400", "all")
rule("err-until", RFC + "RRULE:FREQ=DAILY;UNTIL=NEVER", "all")
rule("err-no-equals", RFC + "RRULE:FREQ=DAILY;COUNT", "all")
rule("err-empty-byset", "DTSTART:20240101T170000\nRRULE:FREQ=HOURLY;INTERVAL=4;BYHOUR=2,6",
     "all")
rule("err-property", RFC + "RRULE:FREQ=DAILY\nATTENDEE:MAILTO:A@EXAMPLE.COM", "all")
rule("err-rrule-parm", RFC + "RRULE;X-NAME=1:FREQ=DAILY", "all")
rule("err-rdate-parm", RFC + "RRULE:FREQ=DAILY\nRDATE;VALUE=PERIOD:19970903T090000", "all")
rule("err-exdate-parm", RFC + "RRULE:FREQ=DAILY\nEXDATE;FOO=BAR:19970903T090000", "all")
rule("err-two-dtstarts", "DTSTART:20240101,20240102\nRRULE:FREQ=DAILY", "all")
rule("err-unknown-name-in-rrule", RFC + "RRULE:FREQ=DAILY;COUNT=2\nRRULE:FOO:BAR", "all")
rule("err-index", RFC + "RRULE:FREQ=DAILY;COUNT=3", "at 3\nat -4\nat 2\nat -3")
rule("err-minutely-empty",
     "DTSTART:20240101T000000\nRRULE:FREQ=MINUTELY;INTERVAL=120;BYHOUR=3",
     "list 2\nstr")
rule("minutely-hour-skip",
     "DTSTART:20240101T000000\nRRULE:FREQ=MINUTELY;INTERVAL=60;BYHOUR=3;BYMINUTE=0",
     "list 3\nstr")
