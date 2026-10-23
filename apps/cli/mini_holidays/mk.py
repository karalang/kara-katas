#!/usr/bin/env python3
"""Writes data/: the job script (jobs.tsv), the two CSV files the programs
read, the gettext catalogs the library translates with (copied from the
vendored package), and files.txt, the list gen_kara.py embeds.

Run from this directory: python3 -s -P -B mk.py"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
LOCALE = os.path.join(HERE, "vendor", "holidays", "locale")

T = "\t"


def J(*parts):
    return T.join(parts)


JOBS = [
    # The basics: one year of US federal holidays, and every way of naming a date.
    J("country", "us", "US", "years=2024"),
    J("items", "us"),
    J("len", "us"),
    J("bool", "us"),
    J("get", "us", "2024-07-04"),
    J("get", "us", "2024-07-05"),
    J("get", "us", "2024-07-06", "=Workday"),
    J("item", "us", "2024-11-28"),
    J("item", "us", "2024-07-05"),
    J("in", "us", "07/04/2024"),
    J("in", "us", "July 4, 2024"),
    J("in", "us", "4 Jul 2024"),
    J("in", "us", "20240704"),
    J("in", "us", "2024/07/04"),
    J("in", "us", "@1720051200"),
    J("in", "us", "@1720137599.9"),
    J("in", "us", "@1720137600"),
    J("in", "us", "date(2024,7,4)"),
    J("in", "us", "dt(2024,7,4,23,59)"),
    J("in", "us", "2024-02-30"),
    J("in", "us", "2024-13-01"),
    J("in", "us", "tomorrow"),
    J("in", "us", ""),
    J("years", "us"),
    J("attrs", "us"),
    # Years are computed on demand, one whole year at a time.
    J("country", "lazy", "US"),
    J("len", "lazy"),
    J("bool", "lazy"),
    J("repr", "lazy"),
    J("str", "lazy"),
    J("years", "lazy"),
    J("in", "lazy", "2023-12-25"),
    J("years", "lazy"),
    J("len", "lazy"),
    J("in", "lazy", "2026-01-02"),
    J("years", "lazy"),
    J("items", "lazy"),
    J("country", "fixed", "US", "expand=0"),
    J("in", "fixed", "2024-12-25"),
    J("get", "fixed", "2024-12-25"),
    J("len", "fixed"),
    J("str", "fixed"),
    J("country", "many", "USA", "years=2018..2027"),
    J("years", "many"),
    J("len", "many"),
    J("named", "many", "Juneteenth"),
    J("country", "few", "US", "years=2030,2022,2027,2024,2041,2019"),
    J("years", "few"),
    J("named", "few", "Christmas"),
    # Holidays on a weekend are observed on a weekday; observed=False drops that.
    J("country", "obs", "US", "years=2021,2022,2027"),
    J("sorted", "obs"),
    J("country", "noobs", "UnitedStates", "years=2021", "observed=0"),
    J("sorted", "noobs"),
    J("set", "obs", "observed", "0"),
    J("len", "obs"),
    J("get", "obs", "2021-12-24"),
    J("set", "obs", "observed", "1"),
    J("get", "obs", "2021-12-24"),
    J("years", "obs"),
    # States, and the unofficial category.
    J("country", "tx", "US", "subdiv=TX", "years=2021"),
    J("sorted", "tx"),
    J("country", "ca", "US", "subdiv=CA", "years=2024"),
    J("items", "ca"),
    J("country", "ga", "US", "subdiv=GA", "years=2024,2025"),
    J("sorted", "ga"),
    J("country", "ma", "US", "subdiv=MA", "years=2025"),
    J("items", "ma"),
    J("country", "dc", "US", "subdiv=DC", "years=2025,2021"),
    J("sorted", "dc"),
    J("country", "il", "US", "subdiv=IL", "years=2024"),
    J("items", "il"),
    J("country", "ny", "US", "subdiv=NY", "years=2023"),
    J("items", "ny"),
    J("country", "wa", "US", "subdiv=WA", "years=2024"),
    J("items", "wa"),
    J("country", "unoff", "US", "category=unofficial", "years=2024"),
    J("items", "unoff"),
    J("country", "both", "US", "categories=unofficial,public", "subdiv=NY", "years=2024"),
    J("items", "both"),
    J("attrs", "both"),
    J("country", "bad1", "US", "subdiv=ZZ"),
    J("country", "bad2", "US", "categories=bank"),
    J("country", "bad3", "US", "categories=public,bank", "subdiv=ZZ"),
    J("country", "old", "US", "state=TX", "years=2024"),
    J("attrs", "old"),
    J("len", "old"),
    J("country", "old2", "US", "prov=MA", "years=2024"),
    J("len", "old2"),
    J("country", "fm", "US", "subdiv=FM", "years=2024"),
    J("len", "fm"),
    J("country", "early", "US", "years=1776,1777,1870,1871,1938,1954,1971,1986"),
    J("sorted", "early"),
    J("country", "late", "US", "years=2100,2101"),
    J("len", "late"),
    J("years", "late"),
    # The United Kingdom: four nations, bank holidays moved to the next weekday.
    J("country", "gb", "GB", "years=2022"),
    J("items", "gb"),
    J("country", "sct", "UK", "subdiv=Scotland", "years=2022,2023"),
    J("sorted", "sct"),
    J("attrs", "sct"),
    J("country", "nir", "GB", "subdiv=NIR", "years=2023"),
    J("items", "nir"),
    J("country", "wls", "UnitedKingdom", "subdiv=WLS", "years=1970,1971"),
    J("sorted", "wls"),
    J("country", "eng", "GBR", "subdiv=England", "years=1874,1875,1977,2011,2020"),
    J("sorted", "eng"),
    J("country", "gbuk", "GB", "subdiv=UK", "years=2024"),
    J("items", "gbuk"),
    J("country", "gbe", "GB", "subdiv=SCT"),
    J("repr", "gbe"),
    J("str", "gbe"),
    J("country", "gbx", "GB", "subdiv=Cornwall"),
    # Germany, in German and in three translations read from gettext catalogs.
    J("country", "de", "DE", "years=2024"),
    J("items", "de"),
    J("country", "deen", "DE", "years=2024", "language=en_US"),
    J("items", "deen"),
    J("country", "deby", "Germany", "subdiv=BY", "categories=public,catholic", "years=2024", "language=en_US"),
    J("items", "deby"),
    J("country", "deby2", "DE", "subdiv=Bayern", "years=2024"),
    J("items", "deby2"),
    J("country", "decat", "DE", "categories=catholic", "years=2024"),
    J("len", "decat"),
    J("country", "decat2", "DE", "subdiv=BY", "categories=catholic", "years=2024"),
    J("items", "decat2"),
    J("country", "deth", "DE", "subdiv=Thüringen", "years=2024", "language=uk"),
    J("items", "deth"),
    J("country", "deth2", "DEU", "subdiv=TH", "years=2024", "language=th"),
    J("items", "deth2"),
    J("country", "deEN", "DE", "years=2024", "language=en_us"),
    J("get", "deEN", "2024-10-03"),
    J("attrs", "deEN"),
    J("country", "deja", "DE", "years=2024", "language=ja"),
    J("get", "deja", "2024-10-03"),
    J("country", "desn", "DE", "subdiv=SN", "years=2017,1994,1995", "language=en_US"),
    J("sorted", "desn"),
    J("country", "debe", "DE", "subdiv=BE", "years=2020,2025,2028", "language=en_US"),
    J("named", "debe", "anniversary"),
    J("getlist", "debe", "2025-05-08"),
    J("country", "de90", "DE", "years=1989,1990,1991"),
    J("sorted", "de90"),
    J("country", "debyp", "DE", "subdiv=BYP", "years=2024"),
    J("len", "debyp"),
    J("country", "demv", "DE", "subdiv=Mecklenburg-Vorpommern", "years=2022,2023"),
    J("named", "demv", "Frauentag"),
    J("country", "debw", "DE", "subdiv=Baden-Württemberg", "years=2024", "language=uk"),
    J("sorted", "debw"),
    # France and the Netherlands.
    J("country", "fr", "FR", "years=2025"),
    J("items", "fr"),
    J("country", "frgp", "FR", "subdiv=GP", "years=2025", "language=en_US"),
    J("items", "frgp"),
    J("country", "fram", "France", "subdiv=Alsace-Moselle", "years=2025"),
    J("items", "fram"),
    J("country", "frre", "FR", "subdiv=La Réunion", "years=1980,1981"),
    J("named", "frre", "esclavage"),
    J("country", "frpf", "FRA", "subdiv=PF", "years=2025", "language=uk"),
    J("items", "frpf"),
    J("country", "fr06", "FR", "years=2005,2008,1947,1948", "language=en_US"),
    J("named", "fr06", "Monday"),
    J("named", "fr06", "Labor"),
    J("country", "nl", "NL", "years=2025"),
    J("items", "nl"),
    J("country", "nlopt", "Netherlands", "categories=optional,public", "years=2025", "language=en_US"),
    J("items", "nlopt"),
    J("country", "nlk", "NLD", "years=1948,1949,1979,1980,2014,2017", "language=en_US"),
    J("named", "nlk", "'s Day"),
    J("country", "nlx", "NL", "subdiv=NH"),
    # Financial markets.
    J("market", "nyse", "NYSE", "years=2024"),
    J("items", "nyse"),
    J("count", "nyse", "2024-01-01", "2024-12-31"),
    J("market", "xnys", "XNYS", "years=2022,2021"),
    J("sorted", "xnys"),
    J("market", "ww1", "NYSE", "years=1914"),
    J("len", "ww1"),
    J("count", "ww1", "1914-07-01", "1914-12-31"),
    J("slice", "ww1", "1914-07-28", "1914-08-06"),
    J("market", "paper", "NewYorkStockExchange", "years=1968"),
    J("named", "paper", "Paper"),
    J("named", "paper", "o", "contains"),
    J("market", "old", "NYSE", "years=1888,1933,1945,2001,2012,2018,2025"),
    J("sorted", "old"),
    J("market", "ecb", "ECB", "years=2000,2024"),
    J("sorted", "ecb"),
    J("market", "tar", "TAR"),
    J("repr", "tar"),
    J("str", "tar"),
    J("market", "lse", "LSE"),
    J("market", "nysub", "NYSE", "subdiv=NY"),
    J("market", "usm", "US", "years=2024"),
    J("len", "usm"),
    J("country", "nyc", "NYSE", "years=2024"),
    J("len", "nyc"),
    J("country", "xx", "XX"),
    # Looking holidays up by name.
    J("named", "tx", "day"),
    J("named", "tx", "DAY", "icontains"),
    J("named", "tx", "Day", "contains"),
    J("named", "tx", "Christmas Day", "exact"),
    J("named", "tx", "christmas day", "iexact"),
    J("named", "tx", "Christ", "startswith"),
    J("named", "tx", "christ", "istartswith"),
    J("named", "tx", "christmas"),
    J("named", "tx", "christmas", "icontains", "split=0"),
    J("named", "tx", "Christmas Day (observed); Christmas Eve", "exact", "split=0"),
    J("named", "tx", "Christmas Day (observed); Christmas Eve", "exact"),
    J("named", "tx", "Eve", "bogus"),
    J("getlist", "tx", "2021-12-24"),
    J("getlist", "tx", "2021-12-23"),
    J("getlist", "tx", "2021-12-22"),
    # Removing and adding holidays.
    J("country", "rm", "US", "subdiv=TX", "years=2021"),
    J("popnamed", "rm", "Thanks"),
    J("get", "rm", "2021-11-26"),
    J("popnamed", "rm", "Christmas"),
    J("popnamed", "rm", "Christmas"),
    J("country", "rm2", "US", "subdiv=TX", "years=2021"),
    J("popnamed", "rm2", "Christmas Day (observed); Christmas Eve"),
    J("popnamed", "rm2", "Nothing"),
    J("pop", "rm2", "2021-07-05"),
    J("pop", "rm2", "2021-07-05"),
    J("pop", "rm2", "2021-07-05", "=gone"),
    J("update", "rm2", "2021-03-01=Founders Day", "2021-01-01=Extra Day"),
    J("updatelist", "rm2", "2021-03-02", "03/03/2021"),
    J("updateone", "rm2", "2021-03-04"),
    J("append", "rm2", "2021-07-05=Back Again"),
    J("update", "rm2", "2021-03-01=Founders Day; Second Name"),
    J("get", "rm2", "2021-03-01"),
    J("years", "rm2"),
    J("update", "rm2", "2030-06-01=Future Day"),
    J("years", "rm2"),
    J("len", "rm2"),
    J("items", "rm2"),
    J("country", "rm3", "US", "years=2021", "expand=0"),
    J("update", "rm3", "2030-06-01=Future Day"),
    J("years", "rm3"),
    J("items", "rm3"),
    J("named", "rm3", "Future"),
    # Ranges.
    J("country", "rg", "US", "years=2024"),
    J("slice", "rg", "2024-12-20", "2025-01-05"),
    J("years", "rg"),
    J("slice", "rg", "2024-12-31", "2024-12-01"),
    J("slice", "rg", "2024-11-01", "2024-12-31", "7"),
    J("slice", "rg", "2024-11-28", "2024-12-31", "td:7"),
    J("slice", "rg", "2024-12-31", "2024-11-01", "-7"),
    J("slice", "rg", "2024-12-31", "2024-11-01", "td:7"),
    J("slice", "rg", "2024-11-01", "2024-12-31", "0"),
    J("slice", "rg", "2024-01-01", ""),
    J("slice", "rg", "2024-07-04", "2024-07-04"),
    # Working days.
    J("working", "rg", "2024-07-04"),
    J("working", "rg", "2024-07-06"),
    J("working", "rg", "2024-07-05"),
    J("nth", "rg", "2024-07-03", "1"),
    J("nth", "rg", "2024-07-05", "-1"),
    J("nth", "rg", "2024-12-20", "5"),
    J("nth", "rg", "2024-12-31", "0"),
    J("nth", "rg", "2024-11-27", "-2"),
    J("count", "rg", "2024-01-01", "2024-12-31"),
    J("count", "rg", "2024-12-31", "2024-01-01"),
    J("count", "rg", "2024-07-04", "2024-07-04"),
    J("country", "lz", "US"),
    J("nth", "lz", "2029-12-21", "10"),
    J("years", "lz"),
    # Sums of calendars.
    J("country", "a", "US", "years=2024"),
    J("country", "b", "DE", "years=2024", "language=en_US"),
    J("add", "ab", "a", "b"),
    J("items", "ab"),
    J("attrs", "ab"),
    J("country", "c", "GB", "subdiv=SCT", "years=2023"),
    J("add", "abc", "ab", "c"),
    J("attrs", "abc"),
    J("years", "abc"),
    J("len", "abc"),
    J("in", "abc", "2025-01-01"),
    J("years", "abc"),
    J("len", "abc"),
    J("get", "abc", "2025-01-02"),
    J("working", "abc", "2024-12-26"),
    J("years", "a"),
    J("years", "c"),
    J("len", "c"),
    J("country", "d", "US", "subdiv=CA"),
    J("country", "e", "US", "subdiv=TX"),
    J("add", "de2", "d", "e"),
    J("str", "de2"),
    J("repr", "de2"),
    J("get", "de2", "2024-11-29"),
    J("years", "de2"),
    J("years", "d"),
    J("add", "mkt", "nyse", "ecb"),
    J("attrs", "mkt"),
    J("get", "mkt", "2024-12-26"),
    J("get", "mkt", "2024-07-04"),
    J("country", "s1", "US", "years=2023"),
    J("country", "s2", "NL", "years=2024", "language=en_US"),
    J("add", "s12", "s1", "s2"),
    J("years", "s12"),
    J("items", "s12"),
    J("in", "s2", "2026-04-27"),
    J("years", "s2"),
    J("in", "s12", "2025-04-27"),
    J("years", "s12"),
    J("get", "s12", "2026-04-27"),
    J("years", "s12"),
    J("country", "f1", "US", "years=2024", "expand=0"),
    J("country", "f2", "US", "subdiv=TX", "years=2024", "expand=0"),
    J("add", "f12", "f1", "f2"),
    J("in", "f12", "2025-01-01"),
    J("attrs", "f12"),
    # Copies share their years with the original.
    J("country", "orig", "US", "years=2024"),
    J("copy", "cp", "orig"),
    J("eq", "cp", "orig"),
    J("in", "cp", "2031-01-01"),
    J("years", "orig"),
    J("in", "orig", "2031-01-01"),
    J("eq", "cp", "orig"),
    J("len", "orig"),
    J("len", "cp"),
    J("eq", "a", "s1"),
    J("country", "a2", "US", "years=2024"),
    J("eq", "a", "a2"),
    J("country", "a3", "US", "years=2024", "observed=0"),
    J("eq", "a2", "a3"),
    J("pop", "a2", "2024-01-01"),
    J("update", "a2", "2024-01-01=New Year's Day"),
    J("eq", "a", "a2"),
    J("country", "cat", "US", "years=2024,2025"),
    J("set", "cat", "categories", "unofficial"),
    J("len", "cat"),
    J("sorted", "cat"),
    J("set", "cat", "categories", "bank"),
    J("len", "cat"),
    J("set", "cat", "categories", "public,unofficial"),
    J("len", "cat"),
    J("set", "cat", "expand", "0"),
    J("in", "cat", "2026-01-01"),
    J("len", "cat"),
    J("country", "emp", "US"),
    J("set", "emp", "categories", "unofficial"),
    J("in", "emp", "2024-10-31"),
    J("get", "emp", "2024-07-04"),
    J("repr", "nl"),
    J("str", "ecb"),
    # Programs.
    J("country", "nyc2", "US", "subdiv=NY"),
    J("payroll", "nyc2", "2025"),
    J("payroll", "nyse", "2024"),
    J("country", "team_us", "US", "subdiv=CA"),
    J("country", "team_de", "DE", "subdiv=BY", "language=en_US"),
    J("country", "team_gb", "GB", "subdiv=SCT"),
    J("country", "team_fr", "FR", "language=en_US"),
    J("country", "team_nl", "NL", "language=en_US"),
    J("sla", "tickets.csv"),
    J("pto", "team.csv", "2024-12-20", "2025-01-07"),
    J("pto", "team.csv", "2025-04-14", "2025-05-12"),
    J("pto", "missing.csv", "2025-04-14", "2025-05-12"),
    J("trading", "nyse", "2024"),
    J("trading", "xnys", "2001"),
    J("ics", "team_de", "2025", "de_by_2025.ics"),
    J("ics", "nlopt", "2025", "nl_2025.ics"),
    J("ics", "team_fr", "2026", "sub/fr.ics"),
    J("ics", "nobody", "2025", "x.ics"),
]

TICKETS = """id,team,opened,business_days
INC-1001,team_us,2024-11-27,3
INC-1002,team_de,2024-12-23,2
INC-1003,team_gb,2024-12-24,1
INC-1004,team_fr,2025-04-30,2
INC-1005,team_nl,2025-04-25,1
INC-1006,team_us,2025-03-28,2
INC-1007,team_de,2025-05-28,3
INC-1008,team_gb,2025-12-23,4
INC-1009,team_nl,2025-12-24,5
INC-1010,team_fr,2025-07-11,-2
INC-1011,team_xx,2025-07-11,2
INC-1012,team_us,2025-02-30,1
INC-1013,team_de,2025-10-02,0
"""

TEAM = """person,calendar
Ana,team_us
Bo,team_de
Chen,team_gb
Dara,team_fr
Eli,team_nl
Femi,team_us
"""

CATALOGS = [
    ("de", "DE"), ("en_US", "DE"), ("th", "DE"), ("uk", "DE"),
    ("en_US", "FR"), ("fr", "FR"), ("uk", "FR"),
    ("en_US", "NL"), ("nl", "NL"), ("uk", "NL"),
]


def main():
    if os.path.isdir(DATA):
        shutil.rmtree(DATA)
    os.makedirs(DATA)
    files = []
    with open(os.path.join(DATA, "jobs.tsv"), "w", encoding="utf-8") as f:
        for j in JOBS:
            f.write(j + "\n")
    for name, text in (("tickets.csv", TICKETS), ("team.csv", TEAM)):
        with open(os.path.join(DATA, name), "w") as f:
            f.write(text)
        files.append(name)
    for lang, entity in CATALOGS:
        rel = "locale/%s/LC_MESSAGES/%s.mo" % (lang, entity)
        os.makedirs(os.path.dirname(os.path.join(DATA, rel)), exist_ok=True)
        shutil.copy(os.path.join(LOCALE, lang, "LC_MESSAGES", entity + ".mo"), os.path.join(DATA, rel))
        files.append(rel)
    with open(os.path.join(DATA, "files.txt"), "w") as f:
        f.write("\n".join(files) + "\n")
    print(len(JOBS), "jobs")


main()
