# Writes data/ for mini_icalendar: calendar files as Google Calendar,
# Outlook, Thunderbird and other tools export them, broken files, and
# the list of time zone names the system's tz database has.
import os
import sys
import zoneinfo

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def fold(line, width=75, sep="\r\n "):
    # RFC 5545 folding by octets, the way most producers do it
    out = []
    cur = ""
    n = 0
    for c in line:
        k = len(c.encode("utf-8"))
        if n + k > width:
            out.append(cur)
            cur = ""
            n = 1
        cur += c
        n += k
    out.append(cur)
    return sep.join(out)


def ics(lines, eol="\r\n", width=75, sep=None):
    if sep is None:
        sep = eol + " "
    return "".join(fold(l, width, sep) + eol for l in lines)


NEW_YORK = """BEGIN:VTIMEZONE
TZID:America/New_York
X-LIC-LOCATION:America/New_York
BEGIN:DAYLIGHT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
TZNAME:EDT
DTSTART:19700308T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
TZNAME:EST
DTSTART:19701101T020000
RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU
END:STANDARD
END:VTIMEZONE""".split("\n")

GOOGLE = [
    "BEGIN:VCALENDAR",
    "PRODID:-//Google Inc//Google Calendar 70.9054//EN",
    "VERSION:2.0",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
    "X-WR-CALNAME:Platform team",
    "X-WR-TIMEZONE:America/New_York",
    "X-WR-CALDESC:Standups\\, reviews and on-call handovers",
    *NEW_YORK,
    "BEGIN:VEVENT",
    "DTSTART;TZID=America/New_York:20260302T093000",
    "DTEND;TZID=America/New_York:20260302T094500",
    "RRULE:FREQ=WEEKLY;WKST=MO;UNTIL=20261231T045959Z;BYDAY=MO,TU,WE,TH,FR",
    "EXDATE;TZID=America/New_York:20260525T093000,20260703T093000",
    "DTSTAMP:20261015T120000Z",
    "ORGANIZER;CN=Priya Raman:mailto:priya@example.com",
    "UID:4f1c0a7e2b@google.com",
    "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=ACCEPTED;CN=Priya Raman;X-NUM-GUESTS=0:mailto:priya@example.com",
    "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE;CN=dev-oncall@example.com;X-NUM-GUESTS=0:mailto:dev-oncall@example.com",
    "ATTENDEE;CUTYPE=RESOURCE;ROLE=NON-PARTICIPANT;PARTSTAT=ACCEPTED;CN=Room 4.12 (Kepler);X-NUM-GUESTS=0:mailto:c_1889k2@resource.calendar.example.com",
    "CREATED:20260220T183000Z",
    "DESCRIPTION:Daily standup. Join: https://meet.example.com/abc-defg-hij\\n\\nAgenda:\\n- yesterday\\n- today\\n- blockers\\n\\nDial-in: +1 555-0100\\, PIN 4417#",
    "LAST-MODIFIED:20261015T115900Z",
    "LOCATION:Room 4.12 (Kepler)\\; or online",
    "SEQUENCE:3",
    "STATUS:CONFIRMED",
    "SUMMARY:Platform standup",
    "TRANSP:OPAQUE",
    "BEGIN:VALARM",
    "ACTION:DISPLAY",
    "DESCRIPTION:This is an event reminder",
    "TRIGGER:-P0DT0H10M0S",
    "END:VALARM",
    "END:VEVENT",
    "BEGIN:VEVENT",
    "DTSTART;TZID=America/New_York:20260709T100000",
    "DTEND;TZID=America/New_York:20260709T104500",
    "DTSTAMP:20261015T120000Z",
    "UID:4f1c0a7e2b@google.com",
    "RECURRENCE-ID;TZID=America/New_York:20260709T093000",
    "CREATED:20260220T183000Z",
    "DESCRIPTION:Moved for the all-hands.",
    "LAST-MODIFIED:20260701T090000Z",
    "SEQUENCE:4",
    "STATUS:CONFIRMED",
    "SUMMARY:Platform standup (moved)",
    "TRANSP:OPAQUE",
    "END:VEVENT",
    "BEGIN:VEVENT",
    "DTSTART;VALUE=DATE:20261126",
    "DTEND;VALUE=DATE:20261128",
    "DTSTAMP:20261015T120000Z",
    "UID:thanksgiving-2026@google.com",
    "CATEGORIES:Holiday,Office closed",
    "CLASS:PUBLIC",
    "SUMMARY:Thanksgiving (office closed)",
    "TRANSP:TRANSPARENT",
    "END:VEVENT",
    "BEGIN:VEVENT",
    "DTSTART:20261103T140000Z",
    "DURATION:PT1H30M",
    "DTSTAMP:20261015T120000Z",
    "UID:oncall-handover-44@google.com",
    "RRULE:FREQ=MONTHLY;BYDAY=1TU;COUNT=6",
    "SUMMARY:On-call handover",
    "DESCRIPTION:Rotation: alice → bob → chen → dana. Runbook: https://wiki.example.com/oncall?tab=handover&view=full",
    "URL:https://wiki.example.com/oncall",
    "END:VEVENT",
    "END:VCALENDAR",
]

W_EUROPE = """BEGIN:VTIMEZONE
TZID:W. Europe Standard Time
BEGIN:STANDARD
DTSTART:16010101T030000
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
RRULE:FREQ=YEARLY;INTERVAL=1;BYDAY=-1SU;BYMONTH=10
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:16010101T020000
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
RRULE:FREQ=YEARLY;INTERVAL=1;BYDAY=-1SU;BYMONTH=3
END:DAYLIGHT
END:VTIMEZONE""".split("\n")

OUTLOOK = [
    "BEGIN:VCALENDAR",
    "METHOD:REQUEST",
    "PRODID:Microsoft Exchange Server 2010",
    "VERSION:2.0",
    *W_EUROPE,
    "BEGIN:VEVENT",
    "ORGANIZER;CN=\"Weber, Thomas\":mailto:thomas.weber@example.de",
    "ATTENDEE;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE;CN=\"Müller, Jana\":mailto:jana.mueller@example.de",
    "ATTENDEE;ROLE=OPT-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE;CN=Sean O'Brien:mailto:sean.obrien@example.ie",
    "ATTENDEE;ROLE=REQ-PARTICIPANT;PARTSTAT=TENTATIVE;DELEGATED-FROM=\"mailto:cfo@example.de\";CN=Finance Team:mailto:finance@example.de",
    "DESCRIPTION;LANGUAGE=de-DE:Hallo zusammen\\,\\n\\nbitte die Zahlen für Q3 mitbringen.\\nAgenda: Budget\\; Forecast\\; Sonstiges\\n\\n",
    "UID:040000008200E00074C5B7101A82E00800000000A0B1C2D3E4F5A6B7C8D9E0F1A2B3C4D5E6F7A8B9",
    "SUMMARY;LANGUAGE=de-DE:Q3 Budgetrunde",
    "DTSTART;TZID=W. Europe Standard Time:20260915T140000",
    "DTEND;TZID=W. Europe Standard Time:20260915T153000",
    "CLASS:PUBLIC",
    "PRIORITY:5",
    "DTSTAMP:20260901T081500Z",
    "TRANSP:OPAQUE",
    "STATUS:CONFIRMED",
    "SEQUENCE:0",
    "LOCATION;LANGUAGE=de-DE:Besprechungsraum Rhein (3. OG)",
    "ATTACH;FMTTYPE=text/plain;ENCODING=BASE64;VALUE=BINARY;X-FILENAME=agenda.txt:QWdlbmRhOgoxLiBCdWRnZXQgUTMKMi4gRm9yZWNhc3QgUTQKMy4gU29uc3RpZ2VzCg==",
    "X-MICROSOFT-CDO-APPT-SEQUENCE:0",
    "X-MICROSOFT-CDO-OWNERAPPTID:2117283546",
    "X-MICROSOFT-CDO-BUSYSTATUS:TENTATIVE",
    "X-MICROSOFT-CDO-INTENDEDSTATUS:BUSY",
    "X-MICROSOFT-CDO-ALLDAYEVENT:FALSE",
    "X-MICROSOFT-CDO-IMPORTANCE:1",
    "X-MICROSOFT-CDO-INSTTYPE:0",
    "X-MICROSOFT-DONOTFORWARDMEETING:FALSE",
    "X-MICROSOFT-DISALLOW-COUNTER:FALSE",
    "X-ALT-DESC;FMTTYPE=text/html:<html><body><p>Hallo zusammen\\,</p><p>bitte die Zahlen für Q3 mitbringen.</p></body></html>",
    "BEGIN:VALARM",
    "DESCRIPTION:REMINDER",
    "TRIGGER;RELATED=START:-PT15M",
    "ACTION:DISPLAY",
    "END:VALARM",
    "END:VEVENT",
    "END:VCALENDAR",
]

TEAMS = [
    "BEGIN:VCALENDAR",
    "PRODID:-//Microsoft Corporation//Outlook 16.0 MIMEDIR//EN",
    "VERSION:2.0",
    "METHOD:PUBLISH",
    "X-MS-OLK-FORCEINSPECTOROPEN:TRUE",
    "BEGIN:VEVENT",
    "CLASS:PUBLIC",
    "CREATED:20260810T171200Z",
    "DESCRIPTION:Microsoft Teams meeting\\nJoin on your computer or mobile app\\nhttps://teams.example.com/l/meetup-join/19%3ameeting_ZmE4%40thread.v2/0?context=%7b%22Tid%22%3a%2201%22%7d\\n",
    "DTEND;TZID=\"Pacific Standard Time\":20260818T100000",
    "DTSTAMP:20260810T171200Z",
    "DTSTART;TZID=\"Pacific Standard Time\":20260818T093000",
    "LAST-MODIFIED:20260810T171200Z",
    "LOCATION:Microsoft Teams Meeting",
    "PRIORITY:5",
    "SEQUENCE:0",
    "SUMMARY;LANGUAGE=en-us:Vendor sync – contract renewal",
    "TRANSP:OPAQUE",
    "UID:040000008200E00074C5B7101A82E0080000000050F4A1C9D2C7DA01",
    "X-MICROSOFT-CDO-BUSYSTATUS:BUSY",
    "X-MICROSOFT-CDO-IMPORTANCE:1",
    "X-MICROSOFT-DISALLOW-COUNTER:FALSE",
    "X-MS-OLK-AUTOFILLLOCATION:FALSE",
    "X-MS-OLK-CONFTYPE:0",
    "END:VEVENT",
    "BEGIN:VEVENT",
    "DTSTART;TZID=Tokyo Standard Time:20260820T090000",
    "DTEND;TZID=Tokyo Standard Time:20260820T093000",
    "DTSTAMP:20260810T171200Z",
    "UID:tokyo-ops-review",
    "SUMMARY:Ops review (Tokyo)",
    "END:VEVENT",
    "END:VCALENDAR",
]

BERLIN = """BEGIN:VTIMEZONE
TZID:Europe/Berlin
X-LIC-LOCATION:Europe/Berlin
BEGIN:DAYLIGHT
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
TZNAME:CEST
DTSTART:19700329T020000
RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=3
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
TZNAME:CET
DTSTART:19701025T030000
RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=10
END:STANDARD
END:VTIMEZONE""".split("\n")

THUNDERBIRD = [
    "BEGIN:VCALENDAR",
    "PRODID:-//Mozilla.org/NONSGML Mozilla Calendar V1.1//EN",
    "VERSION:2.0",
    *BERLIN,
    "BEGIN:VTODO",
    "CREATED:20261001T072011Z",
    "LAST-MODIFIED:20261012T183402Z",
    "DTSTAMP:20261012T183402Z",
    "UID:1c9e7f2a-0b4d-4e8a-9f61-3d2c5b7a8e90",
    "SUMMARY:Renew passport",
    "STATUS:IN-PROCESS",
    "PRIORITY:1",
    "PERCENT-COMPLETE:40",
    "CATEGORIES:Errands,Personal",
    "DTSTART;TZID=Europe/Berlin:20261014T090000",
    "DUE;TZID=Europe/Berlin:20261030T170000",
    "X-MOZ-GENERATION:3",
    "BEGIN:VALARM",
    "ACTION:DISPLAY",
    "TRIGGER;VALUE=DATE-TIME:20261028T080000Z",
    "DESCRIPTION:Default Mozilla Description",
    "END:VALARM",
    "END:VTODO",
    "BEGIN:VTODO",
    "CREATED:20260901T100000Z",
    "DTSTAMP:20260905T163000Z",
    "UID:7d3b2e1f-4a5c-4b6d-8e9f-0a1b2c3d4e5f",
    "SUMMARY:File expense report",
    "STATUS:COMPLETED",
    "COMPLETED:20260905T163000Z",
    "PERCENT-COMPLETE:100",
    "DUE;VALUE=DATE:20260906",
    "END:VTODO",
    "BEGIN:VEVENT",
    "CREATED:20261002T101500Z",
    "DTSTAMP:20261002T101500Z",
    "UID:b8a4c2d0-6e1f-4a3b-9c5d-7e8f9a0b1c2d",
    "SUMMARY:Call with the London office",
    "DTSTART;TZID=/mozilla.org/20050126_1/Europe/London:20261105T160000",
    "DTEND;TZID=/mozilla.org/20050126_1/Europe/London:20261105T163000",
    "RDATE;VALUE=PERIOD:20261112T160000Z/PT30M,20261119T160000Z/20261119T170000Z",
    "X-MOZ-LASTACK:20261101T090000Z",
    "X-MOZ-SNOOZE-TIME:20261105T155000Z",
    "BEGIN:VALARM",
    "ACTION:EMAIL",
    "ATTENDEE:mailto:me@example.net",
    "SUMMARY:Reminder",
    "DESCRIPTION:The London call starts in 10 minutes",
    "TRIGGER;RELATED=START:-PT10M",
    "REPEAT:2",
    "DURATION:PT5M",
    "END:VALARM",
    "END:VEVENT",
    "END:VCALENDAR",
]

FREEBUSY = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//Example Corp//CalDAV Server 4.2//EN",
    "METHOD:REPLY",
    "BEGIN:VFREEBUSY",
    "UID:fb-2026-11-02-dana",
    "ORGANIZER;CN=Scheduling Assistant:mailto:scheduler@example.com",
    "ATTENDEE;CN=Dana Kim:mailto:dana@example.com",
    "DTSTAMP:20261030T120000Z",
    "DTSTART:20261102T080000Z",
    "DTEND:20261102T180000Z",
    "FREEBUSY;FBTYPE=BUSY:20261102T090000Z/PT1H,20261102T130000Z/20261102T143000Z",
    "FREEBUSY;FBTYPE=BUSY-TENTATIVE:20261102T160000Z/PT45M",
    "FREEBUSY;FBTYPE=BUSY-UNAVAILABLE:20261102T120000Z/PT1H",
    "URL:https://cal.example.com/freebusy/dana.ifb",
    "END:VFREEBUSY",
    "BEGIN:VAVAILABILITY",
    "UID:avail-dana-2026",
    "DTSTAMP:20261030T120000Z",
    "SUMMARY:Office hours",
    "ORGANIZER:mailto:dana@example.com",
    "DTSTART:20261101T000000Z",
    "BEGIN:AVAILABLE",
    "UID:avail-dana-weekdays",
    "SUMMARY:Weekdays",
    "DTSTART;TZID=America/New_York:20261102T090000",
    "DTEND;TZID=America/New_York:20261102T170000",
    "RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR",
    "DTSTAMP:20261030T120000Z",
    "END:AVAILABLE",
    "END:VAVAILABILITY",
    "END:VCALENDAR",
]

JOURNAL = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//Example//Field Notes 1.4//EN",
    "BEGIN:VJOURNAL",
    "UID:journal-2026-10-03@example.org",
    "DTSTAMP:20261003T201500Z",
    "DTSTART;VALUE=DATE:20261003",
    "SUMMARY:Site visit: Montmartre",
    "DESCRIPTION:Walked the route twice.\\nNotes:\\n1) Stairs at Rue Foyatier are steep\\; avoid with equipment.\\n2) Café on the corner opens at 07:30.\\n3) Backup route via the funicular.",
    "DESCRIPTION;LANGUAGE=fr:Itinéraire parcouru deux fois.",
    "GEO:48.886705;2.343104",
    "RESOURCES:Camera,Tripod",
    "COMMENT:日本語のメモ: 坂道が多いので、機材は少なめにすること。雨の日は滑りやすい。🙂 Bring a spare battery and the long lens.",
    "COMMENT:Second comment, a long one that keeps going so that it must be folded at least once when it is written back out to a file.",
    "ATTACH:https://files.example.org/visits/montmartre/route.gpx",
    "ATTACH;FMTTYPE=image/jpeg:https://files.example.org/visits/montmartre/IMG_0412.jpg",
    "RELATED-TO;RELTYPE=PARENT:project-paris-2026@example.org",
    "REQUEST-STATUS:2.0;Success",
    "URL;VALUE=URI:https://notes.example.org/j/2026-10-03",
    "X-SCORE;VALUE=FLOAT:4.25",
    "X-RATING;VALUE=INTEGER:+7",
    "X-WEATHER;X-SOURCE=\"https://weather.example.org/api?q=paris\";UNITS=metric:12C\\, light rain",
    "X-ESCAPED-PARAM;X-NOTE=a\\,b\\;c:value",
    "X-CARET;X-TITLE=Line one^nLine ^'two^' ^^ok:caret escapes",
    "CLASS:PRIVATE",
    "END:VJOURNAL",
    "END:VCALENDAR",
]

# LF line ends, lowercase names, whitespace around parameters, a tab
# fold, a byte order mark, an unknown component and a stray comment
LENIENT = (
    "﻿begin:vcalendar\n"
    "version:2.0\n"
    "prodid:-//Hand written//EN\n"
    "\n"
    "begin:vevent\n"
    "uid:lenient-1\n"
    "dtstamp:20261001T000000Z\n"
    "dtstart ; tzid = Europe/Paris : 20261201T100000\n"
    "summary:Folded with a tab and\n"
    "\t a space\n"
    "description:first\\nsecond\\Nthird\\\\fourth\\:fifth\n"
    "Summary:a second summary\n"
    "end:vevent\n"
    "BEGIN:X-ACME-WIDGET\n"
    "X-ACME-COLOR:teal\n"
    "X-ACME-SIZE;VALUE=INTEGER:3\n"
    "END:X-ACME-WIDGET\n"
    "BEGIN:VEVENT\n"
    "UID:mismatched-end\n"
    "SUMMARY:Closed by END:VTODO\n"
    "END:VTODO\n"
    "end:vcalendar\n"
)

ERRORS = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//Example//Importer test//EN",
    "X-PUBLISHED-TTL:P1W",
    "X-COUNT;VALUE=INTEGER:many",
    "BEGIN:VEVENT",
    "UID:broken-values",
    "DTSTAMP:20261001T000000Z",
    "DTSTART:2026-12-01T10:00:00",
    "DTEND:20261301T100000",
    "DURATION:PT1.5H",
    "GEO:51.5;north",
    "PRIORITY:high",
    "SEQUENCE:9999999999",
    "RRULE:FREQ=FORTNIGHTLY;COUNT=3",
    "EXDATE:20261224T250000",
    "TRIGGER:soon",
    "a line that is not a property",
    "DESCRIPTION;:empty parameter section",
    ";X=1:no name",
    "X-SIZE;VALUE=FLOAT:inf",
    "X-WHEN;VALUE=DATE:20260230",
    "SUMMARY:Still imported",
    "END:VEVENT",
    "END:VCALENDAR",
]

TYPES = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//Example//Value types//EN",
    "BEGIN:VEVENT",
    "UID:types-1",
    "DTSTAMP:20261001T000000Z",
    "DTSTART;TZID=Etc/UTC:20261201T100000",
    "DTEND;TZID=UTC:20261201T110000",
    "RECURRENCE-ID;TZID=Europe/Berlin;VALUE=DATE:20261201",
    "RDATE;TZID=Nowhere/Special:20261208T100000,20261215T100000",
    "RDATE:",
    "EXDATE;VALUE=DATE:20261222,20261229",
    "RRULE:FREQ=YEARLY;BYMONTH=2,5L;BYMONTHDAY=-1;BYSETPOS=1,-1;BYHOUR=9,17;INTERVAL=1_0;UNTIL=20301231",
    "EXRULE:FREQ=daily;byday=sa,su;wkst=su;bogus",
    "X-START;VALUE=TIME:083000",
    "X-END;VALUE=TIME:170000Z",
    "X-OFFSET;VALUE=UTC-OFFSET:-0330",
    "X-FLAG;VALUE=BOOLEAN:true",
    "X-LINK;VALUE=URI:https://example.com/a?b=c,d;e",
    "X-BLOCK;VALUE=PERIOD:20261201T090000/20261201T090000",
    "X-LONG;VALUE=DURATION:-P2W3DT4H5M6S",
    "X-WEEKS;VALUE=DURATION:P1W",
    "X-DAY;VALUE=DURATION:PT86400S",
    "X-SPAN;VALUE=DATE:20261201",
    "X-NUM;VALUE=INTEGER:-42",
    "X-RATIO;VALUE=FLOAT:-0.5e-3",
    "X-ADDRESS;VALUE=CAL-ADDRESS:mailto:ops@example.com",
    "CATEGORIES;LANGUAGE=en:one\\,two,three",
    "CATEGORIES:four",
    "GEO:-33.8688;151.2093",
    "PERCENT-COMPLETE:+05",
    "END:VEVENT",
    "END:VCALENDAR",
]

# the VTIMEZONE comes after the event that uses it, so the parser parses
# the calendar again once it knows the zone; two calendars in one file
MULTI = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//Example//Exporter A//EN",
    "BEGIN:VEVENT",
    "UID:late-zone",
    "DTSTAMP:20261001T000000Z",
    "DTSTART;TZID=Harbour Office:20261110T083000",
    "SUMMARY:Uses a zone defined below",
    "END:VEVENT",
    "BEGIN:VTIMEZONE",
    "TZID:Harbour Office",
    "BEGIN:STANDARD",
    "DTSTART:19700101T000000",
    "TZOFFSETFROM:+1000",
    "TZOFFSETTO:+1000",
    "TZNAME:HBR",
    "END:STANDARD",
    "END:VTIMEZONE",
    "END:VCALENDAR",
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//Example//Exporter B//EN",
    "BEGIN:VEVENT",
    "UID:second-calendar",
    "DTSTAMP:20261001T000000Z",
    "DTSTART;TZID=Harbour Office:20261111T083000",
    "DTSTART;TZID=W. Europe Standard Time:20261111T083000",
    "SUMMARY:Two DTSTARTs",
    "END:VEVENT",
    "END:VCALENDAR",
]

BROKEN = {
    "broken/orphan_property.ics": ["SUMMARY:No calendar around me", "BEGIN:VCALENDAR", "END:VCALENDAR"],
    "broken/stray_end.ics": ["BEGIN:VCALENDAR", "END:VEVENT", "END:VCALENDAR", "END:VCALENDAR"],
    "broken/bad_todo_due.ics": ["BEGIN:VCALENDAR", "VERSION:2.0", "BEGIN:VTODO", "UID:t1", "DUE:2026-11-01", "END:VTODO", "END:VCALENDAR"],
    "broken/bad_param.ics": ["BEGIN:VCALENDAR", "X-FOO;BAD PARAM=1:x", "END:VCALENDAR"],
    "broken/param_without_value.ics": ["BEGIN:VCALENDAR", "BEGIN:VTODO", "SUMMARY;LANGUAGE:x", "END:VTODO", "END:VCALENDAR"],
    "broken/unterminated.ics": ["BEGIN:VCALENDAR", "VERSION:2.0", "BEGIN:VEVENT", "UID:x", "END:VEVENT"],
    "broken/bad_offset.ics": ["BEGIN:VCALENDAR", "BEGIN:VTIMEZONE", "TZID:Bad", "BEGIN:STANDARD", "TZOFFSETTO:+2500", "END:STANDARD", "END:VTIMEZONE", "END:VCALENDAR"],
    "broken/control_char.ics": ["BEGIN:VCALENDAR", "BEGIN:VTODO", "X-A;X-B=a\x07b:c", "END:VTODO", "END:VCALENDAR"],
    "broken/x_comment_only.ics": ["X-COMMENT:exported by a script", "BEGIN:VCALENDAR", "VERSION:2.0", "END:VCALENDAR"],
    "broken/empty.ics": [],
}

FILES = {
    "calendars/google_team.ics": ics(GOOGLE),
    "calendars/outlook_invite.ics": ics(OUTLOOK),
    "calendars/teams_publish.ics": ics(TEAMS, width=74),
    "calendars/thunderbird_tasks.ics": ics(THUNDERBIRD),
    "calendars/freebusy_reply.ics": ics(FREEBUSY),
    "calendars/field_journal.ics": ics(JOURNAL),
    "calendars/lenient.ics": LENIENT,
    "calendars/importer_errors.ics": ics(ERRORS),
    "calendars/value_types.ics": ics(TYPES),
    "calendars/two_calendars.ics": ics(MULTI),
}
for name, lines in BROKEN.items():
    FILES["calendars/" + name] = ics(lines)


def zones():
    # the zone names the tz database has, and which of them icalendar
    # counts as UTC
    sys.path.insert(0, HERE)
    from icalendar.timezone.tzid import get_equivalent_tzids

    out = []
    for name in sorted(zoneinfo.available_timezones()):
        utc = "UTC" in get_equivalent_tzids(name)
        out.append(name + (" utc" if utc else ""))
    return "\n".join(out) + "\n"


def main():
    files = dict(FILES)
    files["tz/zones.txt"] = zones()
    files["calendars.txt"] = "\n".join(sorted(k[len("calendars/"):] for k in FILES)) + "\n"
    for name, text in files.items():
        path = os.path.join(DATA, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)


if __name__ == "__main__":
    main()
