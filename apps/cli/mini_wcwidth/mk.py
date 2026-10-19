# Writes data/: the jobs in data/jobs.jsonl and the files the reports read.
# The characters for the per-version jobs are picked here with wcwidth
# itself: the ones whose width changes between Unicode versions, and a
# fixed set of the usual hard cases.
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wcwidth  # noqa: E402

os.makedirs("data", exist_ok=True)
jobs = []


def job(kind, **kw):
    kw["kind"] = kind
    jobs.append(kw)


versions = list(wcwidth.list_versions())

# Characters whose width is not the same in every version: a code point
# from each range of each table, spread over the code space.
changing = []
for c in range(0x80, 0x40000):
    ws = set(wcwidth.wcwidth(chr(c), v) for v in versions)
    if len(ws) > 1:
        changing.append(c)
picked = []
step = max(1, len(changing) // 40)
for k in range(0, len(changing), step):
    picked.append(changing[k])
picked = picked[:40]

usual = [
    0x00, 0x01, 0x1F, 0x20, 0x41, 0x7E, 0x7F, 0x80, 0x9F, 0xA0, 0xAD, 0xE9,
    0x300, 0x483, 0x488, 0x5BF, 0x600, 0x903, 0x1100, 0x115F, 0x1160, 0x11FF,
    0x200B, 0x200C, 0x200D, 0x200E, 0x2028, 0x2060, 0x231A, 0x2329, 0x2764,
    0x3000, 0x3041, 0x303F, 0x4E2D, 0xA4D0, 0xAC00, 0xD7A3, 0xD7B0, 0xFE0F,
    0xFE10, 0xFEFF, 0xFF01, 0xFF61, 0xFFE0, 0x1F1EF, 0x1F300, 0x1F468,
    0x1F4BB, 0x1F600, 0x1F6D7, 0x1F90C, 0x1FA70, 0x1FAE8, 0x20000, 0x2FFFD,
    0x30000, 0xE0001, 0xE0100, 0xF0000, 0x10FFFD,
]

for k, v in enumerate(versions):
    job("wcwidth", version=v, texts=[chr(c) for c in picked])
    if k % 3 == 0:
        job("wcwidth", version=v, texts=[chr(c) for c in usual])
job("wcwidth", texts=[chr(c) for c in usual])
job("wcwidth", env="9.0.0", texts=[chr(c) for c in picked[:12]])
job("wcwidth", version="auto", env="5.0", texts=[chr(c) for c in picked[:12]])
job("wcwidth", version="latest", env="4.1.0", texts=[chr(c) for c in picked[:12]])
job("wcwidth", version="6.2.9", texts=[chr(c) for c in picked[:12]])
job("wcwidth", version="2", texts=["a", "中", "̀", "中", "́"])
job("wcwidth", version="nine", texts=["b", "中", "́", "中"])
job("wcwidth", version="nine", texts=["c", "d", "\x07", "\x9b"])
job("wcwidth", texts=["", "ab", "中文", "é"])

# How a version string is matched.
given = [
    "4.1.0", "5.0.0", "15.1.0", "8.0", "8", "4.9.9", "1", "4.1", "4.0.9",
    "5", "12", "12.1", "15", "16", "16.0.0", "99.0", "6.2.5", "9.0.0.1",
    "9.0.0.0", "10.0", "10.0.0.0.0", "latest", "auto", "LATEST", "",
    " 8.0", "8.0 ", "　 9 .0", "８.0.0", "٨.٠",
    "8_0.0", "1_0.0.0", "8__0", "+8.0", "-1", "0.0.0", "-0", "8.-1",
    "x.y", "8.0a", ".8", "8.", "1e3", "௪.1", "5.१", "0x9",
    "15.1.0 ", "15.0.0.0", "15.0.1", "14.9", "11.0.0", "11.00.000",
    "011", "4.1.0", "\x00", "8.0\n",
]
for k in range(0, len(given), 7):
    job("match", given=given[k:k + 7])
job("match", env="12.1", given=["auto", "latest", "auto"])
job("match", env="", given=["auto", "8.0"])
job("match", env="auto", given=["auto"])
job("match", env="latest", given=["auto"])
job("match", env=" 7", given=["auto", "7.0.0"])
job("match", env="0.5", given=["auto", "auto"])

# Strings.
texts = [
    "", "hello", "hello, world", "中文字", "こんにちは",
    "ﾊﾝｶｸ", "ＡＢＣ", "é́", "क्ष",
    "각", "각", "กำ", "العربية",
    "שָׁלוֹם", "tab\there", "bell\x07", "csi\x9b",
    "nul\x00x", "\x7f", "soft­hyphen", "zero​width", "‍", "a‍",
    "‍a", "‍‍", "a‍‍b", "\U0001F469‍\U0001F4BB",
    "\U0001F468‍\U0001F469‍\U0001F467‍\U0001F466", "\U0001F44D\U0001F3FD",
    "❤️", "❤", "️", "a️", "#️⃣", "1️",
    "©️", "❤️️", "中️", "́️",
    "❤‍️", "❤́️", "\U0001F1EF\U0001F1F5",
    "\U0001F3F3️‍\U0001F308", "⌚", "☕", "\U0001F6D7",
    "\U0001FAE8", "\U00020000\U0002A6D6", "", "\U000E0001\U000E0041",
    " ", "﻿bom", "　　", "⺀", "〿",
]
for v in ["latest", "8.0.0", "9.0.0", "13.0.0", "5.0.0"]:
    job("wcswidth", version=v, texts=texts)
job("wcswidth", version="4.1", texts=texts[:20])
job("wcswidth", texts=["hello", "中文", "a‍"], n=2)
job("wcswidth", texts=["中文字", "❤️x", "ab\x07c"], n=3)
job("wcswidth", texts=["abc", "中文"], n=0)
job("wcswidth", texts=["abc", "中"], n=-2)
job("wcswidth", texts=["abc", "a‍", "a‍b"], n=5)
job("wcswidth", texts=["a‍"], n=1)
job("wcswidth", version="nine", texts=["abc", "❤️", "中", "❤️"])
job("wcswidth", version="7", texts=["❤️", "中"])
job("wcswidth", version="x", texts=["abc", "ab\x01", "é"])

# The app's own reports.
files = [
    "README.md", "説明書.txt", "写真", "notes", "café.txt",
    "café.txt", "\U0001F4C1 projects", "\U0001F469‍\U0001F4BB code",
    "❤️.png", "ﾊﾝｶｸ.csv", "사진", "Makefile",
    "bad\x01name", "الملف.pdf", "a", "zero​space",
    "日本語の長いファイル名.docx",
    "x.tar.gz", "\U0001F1EF\U0001F1F5 trip", "ภาษาไทย",
    "tmp", "ＡＢＣ", "build.sh",
]
with open("data/files.txt", "w") as f:
    for n in files:
        f.write(n + "\n")
with open("data/files_small.txt", "w") as f:
    for n in files[:6]:
        f.write(n + "\n")
with open("data/files_one.txt", "w") as f:
    f.write("日本語の長いファイル名.docx\n")
for w in [80, 60, 40, 30, 20, 12]:
    job("columns", file="files.txt", width=w)
job("columns", file="files_small.txt", width=40)
job("columns", file="files_small.txt", width=8)
job("columns", file="files_one.txt", width=10)

users = [
    "name,city,role,note",
    "Ada Lovelace,London,admin,first programmer",
    "山田太郎,東京,dev,リードエンジニア",
    "Renée,Paris,ops,on call \U0001F4DF",
    "José,Bogotá,dev,❤️ rust",
    "김민준,서울,qa,테스트 자동화",
    "محمد,القاهرة,dev,مرحبا",
    "Ngozi,Lagos,lead,\U0001F469‍\U0001F52C research",
    "สมชาย,กรุงเทพ,ops,กะดึก",
    "tab\tuser,Oslo,dev,ctrl\x07char",
    "ﾊﾝｶｸ,大阪,dev,ﾊﾝｶｸ only",
]
with open("data/users.csv", "w") as f:
    f.write("\n".join(users) + "\n")
job("table", file="users.csv", widths=[0, 0, 0, 0], align="<<^<")
job("table", file="users.csv", widths=[8, 6, 5, 10], align="<>^<")
job("table", file="users.csv", widths=[4, 3, 1, 6], align=">^<>")
job("table", file="users.csv", widths=[12, 0, 0, 16], align="^^^^")
job("table", file="users.csv", widths=[2, 2, 2, 2], align="<<<<")

chat = [
    "ada: Has anyone tried the new build? It prints 中文 fine now.",
    "太郎: はい、昨日から使っています。問題なしです！",
    "renée: ❤️❤️❤️ great work \U0001F44F\U0001F3FD\U0001F44F\U0001F3FD",
    "ngozi: see https://example.com/a/very/long/path/that/does/not/fit/on/one/line",
    "민준: 한국어로 된 긴 문장을 여기에 씁니다 줄바꿈 테스트",
    "bot: build #42 \U0001F469‍\U0001F4BB\U0001F468‍\U0001F4BB\U0001F9D1‍\U0001F4BB done in  3   spaces",
    "\U0001F916: \U0001F1EF\U0001F1F5\U0001F1F0\U0001F1F7\U0001F1F3\U0001F1EC\U0001F1EB\U0001F1F7",
    "x: éééééééééééé",
    "long_user_name_here: hi",
    "山: 山山山山山山山山山山山山山山山山山山",
]
with open("data/chat.log", "w") as f:
    f.write("\n".join(chat) + "\n")
for w in [40, 24, 16, 10, 6]:
    job("wrap", file="chat.log", width=w)

log = [
    "2026-10-19 12:00:01 INFO\tserver started on :8080",
    "2026-10-19 12:00:02 WARN\tslow query → 注文テーブル (812 ms)",
    "2026-10-19 12:00:03 INFO\tuser 山田太郎 logged in from \U0001F1EF\U0001F1F5",
    "2026-10-19 12:00:04 ERROR\tbad byte \x1b[31m in header\x7f",
    "\t\tindented\ttwice",
    "中\t文\t字\tx",
    "c1 control \x85 and \x9b here",
    "❤️\t\U0001F469‍\U0001F4BB\tend",
    "",
    "short",
]
with open("data/app.log", "w") as f:
    f.write("\n".join(log) + "\n")
for w in [72, 50, 30, 12, 3]:
    job("tail", file="app.log", width=w)

with open("data/jobs.jsonl", "w") as f:
    for j in jobs:
        f.write(json.dumps(j) + "\n")
print(len(jobs), "jobs")
