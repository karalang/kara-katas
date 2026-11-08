"""Writes data/sessions/ for mini_cmd: three sessions typed at the
inventory console, read in name order, each one the console's stdin.

Run from this directory: python3 -s -P -B mk.py"""
import os

SESSIONS = {
    # Setting up: an empty first line repeats nothing; help in all its
    # forms; `?` and `!`; a command glued to punctuation; a line with no
    # command word; a literal EOF line ends the session, and what follows
    # it is never read.
    "01_setup.txt": (
        "\n"
        "add bolts 100 0.15\n"
        "add nuts 250 .05\n"
        "add nuts 250 0.05\n"
        "add washers 40\n"
        "add café 3 2.5\n"
        "add bolts 20\n"
        "\n"
        "list\n"
        "?\n"
        "help\n"
        "help add\n"
        "help set\n"
        "help total\n"
        "help ping\n"
        "help show\n"
        "help nosuch\n"
        "help pricing\n"
        "help EOF\n"
        "help help\n"
        "help columns\n"
        "help history\n"
        "help remove\n"
        "help quit\n"
        "help complete\n"
        "help add extra\n"
        "?list\n"
        "!ls -l\n"
        "set-price bolts 0.20\n"
        "set bolts price 0.20\n"
        "set bolts qty many\n"
        "set nails qty 3\n"
        "   total   \n"
        "-oops\n"
        "frobnicate 1\n"
        "add\n"
        "add x y\n"
        "add x 1 2.345\n"
        "EOF\n"
        "list\n"
    ),
    # Reports: the history so far, the columns help uses at other widths,
    # what Tab would complete, whitespace around commands, and an empty
    # line repeating a command that had a tab in it.
    "02_reports.txt": (
        "history\n"
        "columns 20 alpha beta gamma delta epsilon zeta eta theta\n"
        "columns 79\n"
        "columns 5 a\n"
        "columns 3 aaaa bbbb cccc\n"
        "columns 0 x y\n"
        "columns 30 a bb ccc dddd eeeee ffffff ggggggg hhhhhhhh i j k\n"
        "columns many words\n"
        "complete\n"
        "complete a\n"
        "complete he\n"
        "complete help p\n"
        "complete help \n"
        "complete list b\n"
        "complete -x y\n"
        "complete EO\n"
        "ping\n"
        "ping   hello   world \n"
        "\t list\tb\n"
        "\n"
        "remove washers\n"
        "remove washers\n"
        "remove\n"
        "show café\n"
        "show\n"
        "total\n"
        "quit\n"
        "total\n"
    ),
    # A file with Windows line ends and no final one: the empty line
    # repeats the add, and the end of the file is the EOF command.
    "03_crlf.txt": (
        "list\r\n"
        "add rope 2 9.99\r\n"
        "\r\n"
        "list r\r\n"
        "history\r\n"
        "total"
    ),
}

os.makedirs("data/sessions", exist_ok=True)
for name, text in SESSIONS.items():
    with open(f"data/sessions/{name}", "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
