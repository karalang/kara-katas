"""Writes data/: the vCard files a membership secretary imports into the
club's address book, exported from Apple Contacts, Outlook and a Google
takeout, plus the cards that other tools mangle, and jobs.txt.

Every file is written here as bytes, so nothing comes from a real person."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def card(lines, crlf=True):
    sep = "\r\n" if crlf else "\n"
    return (sep.join(lines) + sep).encode("utf-8")


FILES = {}


# A plain Apple Contacts export: grouped lines, item1./item2. prefixes,
# a structured N and ADR, a base64 photo, categories.
FILES["apple_card.vcf"] = card([
    "BEGIN:VCARD",
    "VERSION:3.0",
    "PRODID:-//Apple Inc.//macOS 14.4//EN",
    "N:Okafor;Adaeze;Chidinma;Dr.;PhD",
    "FN:Dr. Adaeze Okafor\\, PhD",
    "ORG:Harbourview Choral Society;Alto Section",
    "TITLE:Section Leader",
    "EMAIL;type=INTERNET;type=HOME;type=pref:adaeze@example.org",
    "item1.EMAIL;type=INTERNET:a.okafor@example.net",
    "item1.X-ABLabel:_$!<Other>!$_",
    "TEL;type=CELL;type=VOICE;type=pref:+44 7700 900123",
    "TEL;type=HOME;type=VOICE:+44 20 7946 0958",
    "item2.ADR;type=HOME;type=pref:;;14 Willow Lane;Bristol;;BS1 4ST;United Kingdom",
    "item2.X-ABADR:gb",
    "CATEGORIES:Choir,Committee,Alto",
    "NOTE:Joined 2019. Prefers email.\\nCommittee since 2021.",
    "PHOTO;ENCODING=b;TYPE=JPEG:AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8gISIjJCUmJygpKissLS4vMDEyMzQ1Njc4OTo7",
    "X-ABUID:A1B2C3D4-0000-0000-0000-000000000001",
    "REV:2024-02-11T09:15:22Z",
    "END:VCARD",
])


# Several cards in one file (an Outlook export), with quoted-printable.
FILES["outlook_batch.vcf"] = card([
    "BEGIN:VCARD",
    "VERSION:2.1",
    "N;CHARSET=utf-8;ENCODING=QUOTED-PRINTABLE:Gr=C3=B6nholm;=C3=89lise;;;",
    "FN;CHARSET=utf-8;ENCODING=QUOTED-PRINTABLE:=C3=89lise Gr=C3=B6nholm",
    "ORG;CHARSET=utf-8;ENCODING=QUOTED-PRINTABLE:Caf=C3=A9 Nordic",
    "TEL;CELL:+358 40 1234567",
    "EMAIL;INTERNET:elise@example.fi",
    "NOTE;ENCODING=QUOTED-PRINTABLE:Long=20line=20that=20keeps=20going=20and=\r\n going=20past=20seventy=20five=20characters=20for=20folding=20tests.",
    "END:VCARD",
    "BEGIN:VCARD",
    "VERSION:2.1",
    "N:Smith;John;Q;Mr;Jr",
    "FN:John Q. Smith Jr",
    "TEL;WORK;VOICE:+1 555 0100",
    "URL:http\\://example.com/~jsmith",
    "END:VCARD",
    "BEGIN:VCARD",
    "VERSION:2.1",
    "N:;Reception;;;",
    "FN:Front Desk",
    "TEL;WORK:+1 555 0199",
    "END:VCARD",
])


# A Google Takeout card: vCard 3.0, multiple ADR, labels, x-fields.
FILES["google_card.vcf"] = card([
    "BEGIN:VCARD",
    "VERSION:3.0",
    "FN:Kwame Mensah",
    "N:Mensah;Kwame;;;",
    "EMAIL;TYPE=INTERNET:kwame.mensah@example.com",
    "EMAIL;TYPE=INTERNET;TYPE=WORK:k.mensah@example.co.uk",
    "TEL;TYPE=CELL:+233 24 123 4567",
    "ADR;TYPE=HOME:;;P.O. Box 1234;Accra;Greater Accra;00233;Ghana",
    "ADR;TYPE=WORK:;Suite 5;8 Independence Ave;Accra;;;Ghana",
    "ORG:Mensah & Partners",
    "BDAY:1986-07-19",
    "X-GENDER:M",
    "CATEGORIES:myContacts",
    "END:VCARD",
])


# Line folding on long values, and escaped characters in text.
FILES["folded.vcf"] = card([
    "BEGIN:VCARD",
    "VERSION:3.0",
    "FN:Margarethe von Hohenzollern-Sigmaringen",
    "N:von Hohenzollern-Sigmaringen;Margarethe;;;",
    "NOTE:This note is deliberately long enough that vobject must fold it ac",
    " ross several lines\\, and it contains a comma\\, a semicolon\\; and a backsl",
    " ash \\\\ to exercise the escaping rules on the way back out.",
    "ORG:Deutsche Gesellschaft für Chormusik;Verwaltung;Büro München",
    "END:VCARD",
])


# A minimal valid card.
FILES["minimal.vcf"] = card([
    "BEGIN:VCARD",
    "VERSION:3.0",
    "FN:Sam Rivera",
    "END:VCARD",
])


# An iCalendar file, parsed with transform off (structure only, no dates
# turned native) so the generic component model is exercised.
FILES["meeting.ics"] = card([
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//Harbourview//Scheduler 1.0//EN",
    "CALSCALE:GREGORIAN",
    "METHOD:REQUEST",
    "BEGIN:VEVENT",
    "UID:evt-0001@example.org",
    "DTSTAMP:20240210T120000Z",
    "DTSTART:20240315T190000Z",
    "DTEND:20240315T210000Z",
    "SUMMARY:Spring concert rehearsal",
    "LOCATION:St Mary\\'s Hall\\, Redcliffe",
    "DESCRIPTION:Bring scores for Fauré and the new commission.\\nTea at 20:00.",
    "ORGANIZER;CN=Adaeze Okafor:mailto:adaeze@example.org",
    "ATTENDEE;ROLE=REQ-PARTICIPANT;CN=Alto Section:mailto:altos@example.org",
    "CATEGORIES:Rehearsal,Choir",
    "STATUS:CONFIRMED",
    "SEQUENCE:2",
    "END:VEVENT",
    "BEGIN:VTODO",
    "UID:todo-0007@example.org",
    "DTSTAMP:20240210T120500Z",
    "SUMMARY:Book the hall for the summer term",
    "STATUS:NEEDS-ACTION",
    "PRIORITY:1",
    "END:VTODO",
    "END:VCALENDAR",
])


# vCard 2.1 with a singleton parameter whose name is unclear (HOME, WORK).
FILES["v21_singletons.vcf"] = card([
    "BEGIN:VCARD",
    "VERSION:2.1",
    "N:Tanaka;Yuki",
    "FN:Yuki Tanaka",
    "TEL;HOME;VOICE:+81 3 1234 5678",
    "TEL;WORK;FAX:+81 3 1234 5679",
    "EMAIL;INTERNET;PREF:yuki@example.jp",
    "ADR;HOME:;;1-2-3 Shibuya;Tokyo;;150-0002;Japan",
    "END:VCARD",
])


# Broken cards, each a different way a tool can mangle the file.
FILES["no_version.vcf"] = card([
    "BEGIN:VCARD",
    "FN:No Version Here",
    "N:Nemo;;;;",
    "END:VCARD",
])

FILES["unclosed.vcf"] = card([
    "BEGIN:VCARD",
    "VERSION:3.0",
    "FN:Dangling Card",
])

FILES["stray_end.vcf"] = card([
    "END:VCARD",
    "BEGIN:VCARD",
    "VERSION:3.0",
    "FN:After Stray End",
    "END:VCARD",
])

FILES["mismatched_end.vcf"] = card([
    "BEGIN:VCARD",
    "VERSION:3.0",
    "FN:Mismatched",
    "END:VCALENDAR",
])

FILES["bad_line.vcf"] = card([
    "BEGIN:VCARD",
    "VERSION:3.0",
    "this line has no colon",
    "FN:Has A Bad Line",
    "END:VCARD",
])

FILES["empty.vcf"] = b""

FILES["just_text.vcf"] = b"this is not a vcard at all\r\nno begin line\r\n"

# Blank lines between cards (logical line boundaries).
FILES["blank_separated.vcf"] = card([
    "BEGIN:VCARD",
    "VERSION:3.0",
    "FN:First Card",
    "END:VCARD",
    "",
    "",
    "BEGIN:VCARD",
    "VERSION:3.0",
    "FN:Second Card",
    "END:VCARD",
])


def jobs():
    vcards = ["apple_card.vcf", "outlook_batch.vcf", "google_card.vcf",
              "folded.vcf", "minimal.vcf", "v21_singletons.vcf",
              "blank_separated.vcf"]
    broken = ["no_version.vcf", "unclosed.vcf", "stray_end.vcf",
              "mismatched_end.vcf", "bad_line.vcf", "empty.vcf", "just_text.vcf"]
    out = []
    for n in vcards + ["meeting.ics"] + broken:
        out.append("count " + n)
    for n in vcards:
        out.append("dump " + n)
    out.append("dump meeting.ics")
    for n in vcards:
        out.append("fields " + n)
    for n in ["apple_card.vcf", "google_card.vcf", "v21_singletons.vcf"]:
        out.append("struct " + n)
    for n in vcards + ["meeting.ics"]:
        out.append("roundtrip " + n)
    for n in broken:
        out.append("parse " + n)
    out.append("qp outlook_batch.vcf")
    out.append("photo apple_card.vcf")
    out.append("build simple")
    out.append("build structured")
    out.append("fold 20")
    out.append("fold 75")
    out.append("escape")
    return out


def main():
    os.makedirs(DATA, exist_ok=True)
    for n, b in FILES.items():
        with open(os.path.join(DATA, n), "wb") as f:
            f.write(b)
    with open(os.path.join(DATA, "jobs.txt"), "w") as f:
        f.write("\n".join(jobs()) + "\n")
    print(len(FILES), "files,", sum(len(b) for b in FILES.values()), "bytes")


main()
