# Writes data/: the payloads the jobs encode (payloads/) and the job list
# (jobs.txt). A job line is `name | payload | options`, the options
# `key=value` words: ec (L, M, Q, H), version, fit (0 or 1), mask, border,
# box, optimize, and out (the outputs, joined with '+').
import os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

LOREM = (
    "Kara is a systems language with effects, ownership and parallelism "
    "built in. This paragraph stands in for the kind of text people put in "
    "QR codes on posters: event details, a short note, a menu, a link with "
    "a long tracking query string. "
)


def payloads():
    p = {}
    p["url.txt"] = "https://www.example.org/products/ultra-widget?ref=qr&utm_source=print&utm_campaign=2024"
    p["wifi.txt"] = "WIFI:T:WPA;S:Cafe Gamma 5G;P:correct horse battery staple;H:false;;"
    p["vcard.vcf"] = "\r\n".join([
        "BEGIN:VCARD", "VERSION:3.0", "N:Lovelace;Ada;;;", "FN:Ada Lovelace",
        "ORG:Analytical Engines Ltd", "TEL;TYPE=WORK,VOICE:+44 20 7946 0958",
        "EMAIL:ada@engines.example", "URL:https://engines.example/ada", "END:VCARD", ""])
    p["phone.txt"] = "4915112345678"
    p["digits.txt"] = "".join(str((i * 7 + 3) % 10) for i in range(160))
    p["alnum.txt"] = "HTTPS://EXAMPLE.ORG/TRACK/1Z999AA10123456784"
    p["mixed.txt"] = "Order #A-1007: 000123456789012345678901 SHIPPED VIA DHL EXPRESS TO BERLIN 10115, ETA 3 days"
    p["utf8.txt"] = "Grüße aus Köln — 東京 🚀 naïve café"
    p["boarding.txt"] = "M1LOVELACE/ADA        EABC123 LHRJFKBA 0175 123Y012A0001 147>1181W 4123BBA 0000000000000"
    p["short-digits.txt"] = "123\n"
    p["empty.txt"] = ""
    p["paragraph.txt"] = LOREM * 3
    p["long.txt"] = (LOREM * 12)[:1800]
    p["bytes.bin"] = bytes(range(256)).decode("latin-1")
    return p


JOBS = """\
url default        | url.txt          | out=info+ascii
url high           | url.txt          | ec=H out=info+svg-path
wifi               | wifi.txt         | ec=Q out=info+ascii-invert
vcard              | vcard.vcf        | out=info+matrix
phone              | phone.txt        | ec=L border=1 out=info+ascii+svg
phone no border    | phone.txt        | ec=L border=0 out=info+ascii+ascii-invert
digits             | digits.txt       | out=info
digits optimize 0  | digits.txt       | optimize=0 out=info
alnum              | alnum.txt        | ec=Q out=info+svg-fragment
mixed              | mixed.txt        | out=info+svg-path-circle
mixed optimize 4   | mixed.txt        | optimize=4 out=info
mixed optimize 0   | mixed.txt        | optimize=0 out=info
utf8               | utf8.txt         | ec=H out=info+ascii
boarding pass      | boarding.txt     | ec=L out=info+svg-circle
short digits       | short-digits.txt | out=info+ascii
empty              | empty.txt        | out=info+ascii
mask 3             | url.txt          | mask=3 out=info+ascii
version 6          | wifi.txt         | version=6 out=info
version 2 no fit   | wifi.txt         | version=2 fit=0 out=info
version 41         | wifi.txt         | version=41 out=info
mask 9             | wifi.txt         | mask=9 out=info
box 4              | alnum.txt        | box=4 border=2 out=svg-path-fill
box 25             | phone.txt        | box=25 out=svg-fill
paragraph          | paragraph.txt    | out=info+matrix
long               | long.txt         | ec=L out=info
long high          | long.txt         | ec=H out=info
bytes              | bytes.bin        | ec=Q out=info+svg-path
"""


def main():
    if os.path.isdir(DATA):
        shutil.rmtree(DATA)
    os.makedirs(os.path.join(DATA, "payloads"))
    for name, text in payloads().items():
        with open(os.path.join(DATA, "payloads", name), "w", encoding="utf-8", newline="") as f:
            f.write(text)
    with open(os.path.join(DATA, "jobs.txt"), "w", encoding="utf-8") as f:
        f.write(JOBS)


if __name__ == "__main__":
    main()
