# Writes the inputs under data/.
import base64, os, quopri
os.makedirs("data/outbox", exist_ok=True)
os.makedirs("data/inbox", exist_ok=True)

cases = r"""
b64encode | 
b64encode | f
b64encode | fo
b64encode | foo
b64encode | foobar
b64encode | \x00\xff\xfe\xfd\xfc?>
b64encode alt=-_ | \xfb\xff\xbf
urlsafe_b64encode | \xfb\xff\xbf\x00
b64decode | Zm9vYmFy
b64decode | Zm9vYg==
b64decode | Zm9vYg
b64decode | Zm9vY
b64decode | Zm9v YmFy\n
b64decode | Zm9v!!YmFy
b64decode | YQ==YQ
b64decode | YQ=x=
b64decode | ==YQ==
b64decode validate | Zm9vYmFy
b64decode validate | Zm9v YmFy
b64decode validate | =Zm9v
b64decode validate | YQ===
b64decode validate | YQ==x
b64decode validate | YQ=x
b64decode validate | YWJj=
b64decode validate | Y=
b64decode validate | YR==
b64decode alt=-_ | -_-_
b64decode alt=-_ | +/+/
urlsafe_b64decode | -_-_
urlsafe_b64decode | -_8A
encodebytes | The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog.
encodebytes | 
decodebytes | VGhlIHF1aWNr\nIGJyb3du\n
b32encode | 
b32encode | a
b32encode | ab
b32encode | abc
b32encode | abcd
b32encode | abcde
b32encode | \xff\x00\xff
b32hexencode | abcde
b32decode | MFRGG===
b32decode | MFRGGZDF
b32decode | mfrgg===
b32decode casefold | mfrgg===
b32decode | MFRGG==
b32decode | MFRGGZ==
b32decode | MF=GG===
b32decode | ========
b32decode | ME======
b32decode | MFRA====
b32decode | 0FRGG===
b32decode map01=L | 01RGG===
b32decode map01=I | 1EZQ====
b32hexdecode | C5H66===
b32hexdecode casefold | c5h66===
b16encode | \x00\x01\xab\xff
b16decode | 0001ABFF
b16decode | 0001abff
b16decode casefold | 0001abff
b16decode | 0001A
b16decode | 00G1
a85encode | 
a85encode | hello
a85encode | \x00\x00\x00\x00\x00
a85encode | \x00\x00
a85encode | \x00\x00\x00\x00
a85encode foldspaces | four    spaces    
a85encode pad | hello
a85encode adobe | hello world
a85encode wrapcol=10 | the quick brown fox jumps
a85encode adobe wrapcol=10 | the quick brown fox
a85encode adobe wrapcol=1 | ab
a85decode | BOu!rDZ
a85decode | BOu!r D Z\n
a85decode | z
a85decode | !!z
a85decode | !!
a85decode | s8W-"
a85decode | s8W-#
a85decode | BOu!rv
a85decode foldspaces | y
a85decode | y
a85decode foldspaces | !y
a85decode adobe | <~BOu!rDZ~>
a85decode adobe | BOu!rDZ~>
a85decode adobe | <~BOu!rDZ
b85encode | 
b85encode | hello
b85encode pad | hello
b85encode | \x00\x00\x00\x00\xff\xff\xff\xff
b85decode | Xk~0{Zv
b85decode | Xk~0{Zy<
b85decode | Xk~0"Zv
b85decode | |NsC0
b85decode | |NsC1
z85encode | \x86\x4f\xd2\x6f\xb5\x59\xf7\x5b
z85decode | HelloWorld
z85decode | Hello~orld
z85decode | %nSc0
hexlify | \x01\x02\xab
hexlify sep=- n=2 | \x01\x02\x03\x04\x05
hexlify sep=- n=-2 | \x01\x02\x03\x04\x05
hexlify sep=: | \xde\xad\xbe\xef
unhexlify | 01ab
unhexlify | 01AB
unhexlify | 01a
unhexlify | 0x
crc32 | 
crc32 | The quick brown fox jumps over the lazy dog
crc32 value=1 | hello
crc_hqx | 123456789
crc_hqx value=65535 | 123456789
qp_encode | plain text
qp_encode | a=b and caf\xc3\xa9
qp_encode | trailing space \n
qp_encode | tab\tinside
qp_encode quotetabs | tab\tinside and spaces
qp_encode | line one\nline two\t\n.\nend.
qp_encode | 0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
qp_encode | 012345678901234567890123456789012345678901234567890123456789012345678901234\xc3\xa9xyz
qp_encode | 01234567890123456789012345678901234567890123456789012345678901234567890123 x
qp_encode header | Hello World_x=y caf\xc3\xa9
qp_encode | \r\n
qp_decode | a=3Db caf=C3=A9
qp_decode | soft=\nbreak
qp_decode | trailing   \nspace
qp_decode | bad=ZZescape =4
qp_decode | ==3D
qp_decode | end=
qp_decode | crlf=\r\nline
qp_decode header | Hello_World=5F
qp_decode | Hello_World
"""
open("data/cases.txt", "w").write(cases.lstrip("\n"))

note = (
    "Nightly build report — café branch\n"
    "\n"
    "All 1,284 tests passed. Coverage is 87.5% (up from 86.9%), and the binary size is 4.2 MiB.\n"
    "Line with trailing spaces   \n"
    "Line with a tab\there and an equals sign: a=b\n"
    ".\n"
    "From the release checklist: ✓ tagged, ✓ signed, ✗ announced.\n"
    "A very long line that keeps going past the seventy-six character limit of quoted-printable so it has to be broken with soft line breaks somewhere in the middle.\n"
    "日本語の行\n"
    "-- \n"
    "build-bot\n"
)
open("data/outbox/note.txt", "w", encoding="utf-8").write(note)
open("data/outbox/report.csv", "w").write(
    "suite,tests,failed,seconds\nlexer,212,0,1.9\nparser,388,0,4.1\ntypecheck,431,0,9.7\ncodegen,253,0,31.2\n")

# Messages received: written as mail clients write them.
logo = bytes((i * 37 + 11) % 256 for i in range(120))
b64 = base64.b64encode(logo).decode()
lines60 = "\n".join(b64[i:i + 60] for i in range(0, len(b64), 60))
m1 = f"""From: =?iso-8859-1?q?Andr=E9_M=FCller?= <andre@example.de>
To: team@example.com
Subject: =?utf-8?b?UGhvdG9zIGZyb20gdGhlIG9mZnNpdGUg8J+TuA==?=
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="b1_phone"

This is a multi-part message in MIME format.

--b1_phone
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: base64

{base64.encodebytes("Here are the photos. Schöne Grüße!\n".encode()).decode()}
--b1_phone
Content-Type: image/png; name="logo.png"
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename="logo.png"

{lines60}
--b1_phone
Content-Type: image/jpeg; name="broken.jpg"
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename="broken.jpg"

/9j/4AAQSkZJRgABAQ
--b1_phone--
"""
open("data/inbox/01-phone.eml", "w").write(m1)

html = ("<html><body><p style=\"color: #333\">Your invoice for October is ready. "
        "The total is €1.234,50 and is due on 15 November.</p></body></html>\n")
qp = quopri.encodestring(html.encode(), quotetabs=False).decode()
m2 = f"""From: Billing <billing@example.com>
To: team@example.com
Subject: =?utf-8?q?Invoice_=E2=84=96_2026-10_=E2=80=94_due_15_Nov?=
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="alt-42"

--alt-42
Content-Type: text/plain; charset="iso-8859-1"
Content-Transfer-Encoding: quoted-printable

Your invoice for October is ready. The total is EUR 1.234,50 (that is =A31.05=
6,12 in sterling).   
A bad escape =ZZ stays, and so does a lone = at the end =
--alt-42
Content-Type: text/html; charset="utf-8"
Content-Transfer-Encoding: quoted-printable

{qp}
--alt-42--
"""
open("data/inbox/02-invoice.eml", "w").write(m2)

csv = b"id,amount\r\n1,10.00\r\n2,-3.50\r\n"
noisy = base64.b64encode(csv).decode()
noisy = noisy[:10] + " *" + noisy[10:20] + "\r\n" + noisy[20:]
m3 = ("From: exporter@example.org\r\n"
      "To: team@example.com\r\n"
      "Subject: Export ready\r\n"
      "Content-Type: multipart/mixed; boundary=XYZ\r\n"
      "\r\n"
      "--XYZ\r\n"
      "Content-Type: text/plain\r\n"
      "\r\n"
      "The export is attached.\r\n"
      "--XYZ\r\n"
      "Content-Type: text/csv; name=export.csv\r\n"
      "Content-Transfer-Encoding: base64\r\n"
      "Content-Disposition: attachment; filename=export.csv\r\n"
      "\r\n"
      f"{noisy}\r\n"
      "--XYZ--\r\n")
open("data/inbox/03-export.eml", "w", newline="").write(m3)
