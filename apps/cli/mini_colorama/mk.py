#!/usr/bin/env python3
r"""Writes data/jobs.tsv: one colorama operation per line, tab-separated.

Columns: op and arg. Ops map onto colorama's public API:
  fore/back/style <NAME>   Fore/Back/Style.<NAME>   -> the SGR escape
  title <text>             ansi.set_title(text)
  clearscreen <mode>       ansi.clear_screen(mode)
  clearline <mode>         ansi.clear_line(mode)
  cursorup/down/fwd/back <n>   Cursor.UP/DOWN/FORWARD/BACK(n)
  pos <x>;<y>              Cursor.POS(x, y)
  combo                    a Fore+Style composed string
  strip <text-with-ansi>   remove CSI sequences (AnsiToWin32 strip path)

The code-producing ops and `combo` emit real ANSI (ESC / BEL bytes); the
`strip` args carry real ESC bytes too. Both survive a tab/newline-delimited
file because ESC (0x1b) and BEL (0x07) are neither tab, newline, nor any
boundary `str.splitlines` recognises. OSC stripping is out of scope: colorama's
convert path for a title OSC calls into the Windows terminal and raises on a
non-Windows host, so only CSI sequences are stripped here (its portable half).
"""
import os

ESC = "\x1b"

JOBS = [
    ("fore", "RED"), ("fore", "GREEN"), ("fore", "BLUE"),
    ("fore", "LIGHTBLUE_EX"), ("fore", "RESET"),
    ("back", "GREEN"), ("back", "WHITE"), ("back", "RESET"),
    ("style", "BRIGHT"), ("style", "DIM"), ("style", "NORMAL"),
    ("style", "RESET_ALL"),
    ("title", "build ok"),
    ("clearscreen", "2"), ("clearscreen", "0"),
    ("clearline", "2"),
    ("cursorup", "2"), ("cursordown", "1"), ("cursorfwd", "5"),
    ("cursorback", "3"), ("pos", "3;4"),
    ("combo", ""),
    ("strip", ESC + "[31m" + ESC + "[1mERROR" + ESC + "[0m ok"),
    ("strip", "x" + ESC + "[2Ky"),
    ("strip", "a" + ESC + "[mb"),
    ("strip", ESC + "[38;5;9mX" + ESC + "[0m"),
    ("strip", "ab" + ESC + "["),
    ("strip", "plain text, no ansi"),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w") as fh:
    for op, arg in JOBS:
        fh.write(op + "\t" + arg + "\n")
