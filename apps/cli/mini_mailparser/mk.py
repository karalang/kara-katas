# Writes data/: a mailbox of 16 messages under data/mail/ (one per file, as
# a mail client or an MTA would hand them over), an attachment the composer
# sends, and data/jobs.jsonl, the edits mini_mailparser makes to parsed
# messages.
import base64
import json
import os
import quopri

os.makedirs("data/mail", exist_ok=True)
os.makedirs("data/outbox", exist_ok=True)


def b64(b, width=76):
    s = base64.b64encode(b).decode()
    return "\n".join(s[i:i + width] for i in range(0, len(s), width)) + "\n"


def qp(s, charset="utf-8"):
    return quopri.encodestring(s.encode(charset)).decode()


PDF = bytes(range(256))[:80] + b"%PDF-1.4\n% fake report\n" + bytes([0, 255, 128, 10, 13]) * 6
PNG = b"\x89PNG\r\n\x1a\n" + bytes((i * 37) % 256 for i in range(60))

MAIL = {}

MAIL["01.eml"] = """From ana.lima@example.org Mon Oct 19 14:30:02 2026
Return-Path: <ana.lima@example.org>
Received: from mail.example.org (mail.example.org [192.0.2.10])
\tby mx.example.net (Postfix) with ESMTPS id 4F2A31C0042
\tfor <ben@example.net>; Mon, 19 Oct 2026 14:30:02 +0000 (UTC)
Received: from [10.0.0.7] (unknown [198.51.100.23]) by mail.example.org with ESMTPSA id abc123; Mon, 19 Oct 2026 14:30:01 +0000
From: "Ana Lima" <ana.lima@example.org>
To: Ben Okafor <ben@example.net>
Subject: Quarterly report draft, with a subject line long enough that a mail client would fold it
Date: Mon, 19 Oct 2026 09:30:00 -0500
Message-ID: <r1@example.org>
References: <a1@example.org> <a2@example.org> <a3@example.org> <a4@example.org> <a5@example.org>

Hi Ben,

The draft is attached to the next mail.
From now on I will send them weekly.
>From the last meeting: nothing new.

Ana
"""

MAIL["02.eml"] = """From: Support Desk <support@example.com>
To: dana@example.gov
Subject: =?utf-8?q?Your_ticket_=E2=80=94_resolved?=
Date: Tue, 20 Oct 2026 10:00:00 +0000
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="alt-7f3a"

This is a multi-part message in MIME format.

--alt-7f3a
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: quoted-printable

""" + qp("Hello Dana,\n\nYour ticket #4411 — “printer offline” — is resolved.\nA very long line that quoted-printable has to break with a soft line break because it runs past seventy-six characters.\n\nRegards, Support\n") + """
--alt-7f3a
Content-Type: text/html; charset="utf-8"
Content-Transfer-Encoding: base64

""" + b64("<p>Hello Dana,</p><p>Your ticket <b>#4411</b> — resolved.</p>\n".encode()) + """
--alt-7f3a--

Epilogue text after the close boundary.
"""

MAIL["03.eml"] = """From: =?utf-8?q?Jos=C3=A9_Mart=C3=ADnez?= <jose@example.es>
To: Fox Mulder <fox@example.gov>
Subject: Informe trimestral
Date: Wed, 21 Oct 2026 08:15:00 +0200
MIME-Version: 1.0
Content-Type: multipart/mixed;
 boundary="==outer==";
 report-type=quarterly

--==outer==
Content-Type: multipart/alternative; boundary=inner

--inner
Content-Type: text/plain; charset=iso-8859-1
Content-Transfer-Encoding: quoted-printable

""" + qp("Adjunto el informe. Saludos, José\n", "latin-1") + """--inner
Content-Type: text/html; charset=iso-8859-1
Content-Transfer-Encoding: 8bit

<p>Adjunto el informe.</p>
--inner--

--==outer==
Content-Type: application/pdf; name="informe.pdf"
Content-Disposition: attachment;
 filename*0*=utf-8''Informe%20trimestral%20;
 filename*1*=%E2%80%94%20Q3.pdf
Content-Transfer-Encoding: base64

""" + b64(PDF) + """--==outer==
Content-Type: image/png
Content-Disposition: inline; filename="chart.png"
Content-ID: <chart@example.es>
Content-Transfer-Encoding: base64

""" + b64(PNG) + """--==outer==--
"""

crlf = """From: ops@example.com
To: oncall@example.com
Subject: Disk alert
Date: Thu, 22 Oct 2026 03:00:00 +0000
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="crlf-b"

--crlf-b
Content-Type: text/plain

/var is at 91%.
--crlf-b
Content-Type: text/csv; name=usage.csv
Content-Disposition: attachment; filename=usage.csv

mount,used
/var,91
--crlf-b--
"""
MAIL["04.eml"] = crlf.replace("\n", "\r\n")

MAIL["05.eml"] = """From: Eve <eve@example.com>
To: carol@example.com
Subject: Fwd: Lunch?
Date: Fri, 23 Oct 2026 12:00:00 +0100
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="fwd"

--fwd
Content-Type: text/plain; charset=us-ascii

See below.

--fwd
Content-Type: message/rfc822
Content-Disposition: inline

From: Bob <bob@example.com>
To: Eve <eve@example.com>
Subject: Lunch?
Date: Fri, 23 Oct 2026 11:00:00 +0100

Noon at the usual place?
--fwd--
"""

MAIL["06.eml"] = """From: list@example.org
To: readers@example.org
Subject: Weekly digest, issue 12
MIME-Version: 1.0
Content-Type: multipart/digest; boundary="dg"

--dg

From: alice@example.com
Subject: First post

Hello list.

--dg
Content-Type: text/plain

Not a message, a note.
--dg

From: bob@example.com
Subject: Second post

Hi again.
--dg--
"""

MAIL["07.eml"] = """From: hr@example.com
To: all@example.com
Subject: No boundary
MIME-Version: 1.0
Content-Type: multipart/mixed

--anything
Content-Type: text/plain

body
--anything--
"""

MAIL["08.eml"] = """From: hr@example.com
To: all@example.com
Subject: Truncated upload
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="cut"

preamble line
--cut
Content-Type: text/plain

first part
--cut
Content-Type: application/octet-stream
Content-Transfer-Encoding: base64

AAECAwQFBgcICQ==
"""

MAIL["09.eml"] = """From: x@example.com
Subject: Never starts
Content-Type: multipart/mixed; boundary="nope"

There is no boundary here,
only text.
"""

MAIL["10.eml"] = """ leading continuation line
From: x@example.com
:no-name header
Subject: Odd headers
From misplaced@example.com Fri Oct 23 00:00:00 2026
X-Empty:
X-Folded: one
  two
\tthree
This line has no colon, so the body starts here
and continues.
"""

MAIL["11.eml"] = """From: bad@example.com
Subject: Bad base64 and a uuencoded file
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=b

--b
Content-Type: text/plain
Content-Transfer-Encoding: base64

SGVsbG8gd29ybGQ
--b
Content-Type: text/plain
Content-Transfer-Encoding: base64

SGVs*bG8g!d29y
bGQh
--b
Content-Type: application/octet-stream
Content-Transfer-Encoding: x-uuencode

begin 644 notes.txt
M5&AI<R!I<R!A('5U96YC;V1E9"!F:6QE+B!)="!H87,@;6]R92!T:&%N(&]N
'92!L:6YE+@H`
`
end
--b
Content-Type: application/octet-stream
Content-Transfer-Encoding: uuencode

no begin line here
--b
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: quoted-printable

Soft=20break=
 here, a =3D sign, a bad =ZZ escape, trailing space=20
=E2=82=AC done
--b--
"""

MAIL["12.eml"] = """From: Dörte <doerte@example.de>
To: Grüße Team <gruesse@example.de>
Subject: Grüße aus Köln
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit

Liebe Grüße, Dörte — bis bald! 🙂
"""

MAIL["13.eml"] = """From: MAILER-DAEMON@mx.example.net
To: ana.lima@example.org
Subject: Undelivered Mail Returned to Sender
MIME-Version: 1.0
Content-Type: multipart/report; report-type=delivery-status; boundary="dsn"

--dsn
Content-Description: Notification
Content-Type: text/plain; charset=us-ascii

I'm sorry to have to inform you that your message could not
be delivered to one or more recipients.

--dsn
Content-Description: Delivery report
Content-Type: message/delivery-status

Reporting-MTA: dns; mx.example.net
Arrival-Date: Mon, 19 Oct 2026 14:30:02 +0000

Final-Recipient: rfc822; nobody@example.net
Action: failed
Status: 5.1.1

Final-Recipient: rfc822; other@example.net
Action: delayed
Status: 4.4.1

--dsn
Content-Description: Undelivered Message Headers
Content-Type: text/rfc822-headers

Subject: Quarterly report draft
Message-ID: <r1@example.org>

--dsn--
"""

MAIL["14.eml"] = """From: signer@example.com
To: you@example.com
Subject: Signed note
MIME-Version: 1.0
Content-Type: multipart/signed; protocol="application/pgp-signature"; micalg=pgp-sha256; boundary="sig"

--sig
Content-Type: text/plain; charset=us-ascii
X-Long: aaaaaaaaaa bbbbbbbbbb cccccccccc dddddddddd eeeeeeeeee ffffffffff gggggggggg hhhhhhhhhh

Signed text.
--sig
Content-Type: application/pgp-signature; name="signature.asc"

-----BEGIN PGP SIGNATURE-----
iQEzBAEBCAAdFiEEexampleexampleexampleexample
-----END PGP SIGNATURE-----
--sig--
"""

MAIL["15.eml"] = """From: weird@example.com
Subject: Strange content types
Content-Type: multipart/mixed; boundary="w"; charset=utf-8
Content-Transfer-Encoding: base64

--w
Content-Type: text

no slash
--w
Content-Type: TEXT/HTML; CHARSET="ISO-8859-1"; Name="a;b.html"

<b>caps</b>
--w
Content-Type: text/plain; title="semi;colon"; note="say \\"hi\\""; flag; empty=; x=1

params
--w
Content-Type: text/plain; charset*=us-ascii'en'%41%42C; title*0="part one "; title*1="and two"

rfc 2231
--w
Content-Type: application/x-thing; name*=utf-8''%E2%82%AC%20euro.txt
Content-Disposition: ATTACHMENT

euro
--w--
"""

MAIL["16.eml"] = """From nobody Sat Oct 24 09:00:00 2026
From: poet@example.com
Subject: From lines

From here the poem starts.
 From with a space is fine.
From the end.
"""

for name, text in MAIL.items():
    with open("data/mail/" + name, "w", encoding="utf-8", newline="") as f:
        f.write(text)

with open("data/outbox/agenda.txt", "w", encoding="utf-8") as f:
    f.write("Agenda\n1. Budget\n2. Hiring\n3. Résumé review\n")
with open("data/outbox/logo.bin", "wb") as f:
    f.write(bytes((i * 7 + 3) % 256 for i in range(100)))

JOBS = [
    {"file": "02.eml", "part": 0, "ops": [["get_param", "boundary", {}], ["get_params", {}], ["set_param", "charset", "utf-8", {}], ["get_params", {}], ["set_boundary", "new-b"], ["get_boundary"]]},
    {"file": "02.eml", "part": 1, "ops": [["set_type", "text/markdown"], ["del_param", "charset", {}], ["set_param", "format", "flowed", {"requote": False}], ["set_param", "charset", "latin-1", {"replace": True}]]},
    {"file": "03.eml", "part": 4, "ops": [["get_filename"], ["get_param", "filename", {"header": "content-disposition"}], ["get_param", "filename", {"header": "content-disposition", "unquote": False}], ["get_params", {"header": "content-disposition"}], ["set_param", "filename", "Résumé.pdf", {"header": "Content-Disposition"}], ["get_filename"], ["set_param", "filename", "plain.pdf", {"header": "Content-Disposition", "charset": "utf-8", "language": "en"}], ["get_filename"]]},
    {"file": "03.eml", "part": 0, "ops": [["get_param", "report-type", {}], ["set_boundary", "renamed"], ["get_boundary"], ["del_param", "report-type", {}], ["get_params", {}]]},
    {"file": "15.eml", "part": 2, "ops": [["get_params", {}], ["get_params", {"unquote": False}], ["get_content_charset"], ["get_param", "name", {}], ["get_filename"]]},
    {"file": "15.eml", "part": 3, "ops": [["get_params", {}], ["get_param", "flag", {}], ["get_param", "empty", {}], ["get_param", "note", {}], ["set_param", "x", "2", {}], ["del_param", "flag", {}], ["del_param", "missing", {}]]},
    {"file": "15.eml", "part": 4, "ops": [["get_params", {}], ["get_content_charset"], ["get_param", "title", {}], ["set_param", "title", "new", {}]]},
    {"file": "15.eml", "part": 5, "ops": [["get_filename"], ["get_content_disposition"], ["get_param", "name", {}]]},
    {"file": "01.eml", "part": 0, "ops": [["get_all", "received"], ["replace_header", "subject", "Short"], ["replace_header", "x-missing", "v"], ["add_header", "Content-Disposition", "attachment", {"filename": "a b.txt"}], ["add_header", "X-Flags", None, {"seen": None, "size": "10"}], ["add_header", "Content-Disposition", "inline", {"filename": ["iso-8859-1", "fr", "été.txt"]}], ["add_header", "Content-Disposition", "inline", {"filename": "Grüße.txt"}], ["set", "X-New", "Grüße"], ["del", "received"], ["get_all", "received"], ["get_all", "content-disposition"], ["set_param", "charset", "utf-8", {}], ["get_content_type"], ["set_type", "nonsense"], ["set_type", "text/x-note"]]},
    {"file": "10.eml", "part": 0, "ops": [["set_boundary", "x"], ["del_param", "charset", {}], ["set_param", "a", "b", {"header": "X-Custom"}], ["set_param", "a", "c", {"header": "X-Custom"}], ["get", "x-custom"], ["get", "x-empty"], ["get", "x-folded"], ["get_content_type"]]},
    {"file": "12.eml", "part": 0, "ops": [["get_content_charset"], ["set_param", "charset", "iso-8859-1", {}], ["get_charsets"], ["set", "Subject", "second"], ["get_all", "subject"]]},
]
with open("data/jobs.jsonl", "w", encoding="utf-8") as f:
    for j in JOBS:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
