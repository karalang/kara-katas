#!/usr/bin/env python3
"""Runs the inventory console over data/sessions/*.txt with the vendored
`cmd` module (CPython 3.13's Lib/cmd.py) and prints the transcript
mini_cmd.kara must reproduce byte for byte (README.md has the rules).

The console reads each session file as its stdin with use_rawinput off,
so the prompt is written before every read, as a terminal would show it
with the input not echoed. The parsing of a line, the empty-line repeat,
`?` and `!`, the help listing and its columns are the module's; the
inventory and its messages are the port's own.

Run from this directory: python3 -I -B oracle.py > expected.out"""
import os
import sys

sys.path.insert(0, "vendor")
import cmd  # noqa: E402


def cents(text):
    """A price as cents: digits, optionally a point and one or two more."""
    whole, dot, frac = text.partition(".")
    if not whole.isascii() or not whole.isdigit() or len(whole) > 7:
        return None
    if dot and (not frac.isascii() or not frac.isdigit() or len(frac) > 2):
        return None
    return int(whole) * 100 + int((frac + "00")[:2])


def money(c):
    return f"{c // 100}.{c % 100:02d}"


class Inventory(cmd.Cmd):
    intro = "Inventory console. Type help or ? to list commands."
    prompt = "(inv) "
    doc_leader = "Stock and prices for the shop floor."
    ruler = "-"
    use_rawinput = False

    def __init__(self, stock, stdin, history):
        super().__init__(stdin=stdin)
        self.stock = stock
        self.history = history
        self.count = 0

    # ---- hooks

    def precmd(self, line):
        self.history.append(line)
        return line

    def postcmd(self, stop, line):
        self.count += 1
        return stop

    def postloop(self):
        print(f"[{self.count} lines handled]")

    # ---- commands

    def do_add(self, arg):
        """Add stock: add NAME QTY [PRICE].

        QTY is added to what is there; PRICE, when given, replaces the
        price (a new item without one costs 0.00).
            add bolts 100 0.15
        """
        words = arg.split()
        if len(words) not in (2, 3):
            print("usage: add NAME QTY [PRICE]")
            return
        name, qty = words[0], words[1]
        if not qty.isascii() or not qty.isdigit() or len(qty) > 7:
            print(f"bad quantity: {qty}")
            return
        price = None
        if len(words) == 3:
            price = cents(words[2])
            if price is None:
                print(f"bad price: {words[2]}")
                return
        have, old = self.stock.get(name, (0, 0))
        self.stock[name] = (have + int(qty), old if price is None else price)
        q, p = self.stock[name]
        print(f"{name}: {q} at {money(p)}")

    def help_add(self):
        print("add NAME QTY [PRICE] -- see also: help pricing")

    def do_remove(self, arg):
        """Remove an item entirely: remove NAME"""
        if arg not in self.stock:
            print(f"no item {arg!r}")
            return
        del self.stock[arg]
        print(f"removed {arg}")

    def do_list(self, arg):
        """List the items, or those whose names start with ARG."""
        names = sorted(n for n in self.stock if n.startswith(arg))
        if not names:
            print("(nothing)")
        for n in names:
            q, p = self.stock[n]
            print(f"{n:<12}{q:>7}{money(p):>10}")

    def help_list(self):
        print("list [PREFIX]: items in name order, with quantity and price")

    def do_set(self, arg):
        """\tset NAME qty|price VALUE\t(changes one field)"""
        words = arg.split()
        if len(words) != 3 or words[1] not in ("qty", "price"):
            print(f"cannot set: {arg!r}")
            return
        name, field, value = words
        if name not in self.stock:
            print(f"no item {name!r}")
            return
        q, p = self.stock[name]
        if field == "qty":
            if not value.isascii() or not value.isdigit() or len(value) > 7:
                print(f"bad quantity: {value}")
                return
            q = int(value)
        else:
            c = cents(value)
            if c is None:
                print(f"bad price: {value}")
                return
            p = c
        self.stock[name] = (q, p)
        print(f"{name}: {q} at {money(p)}")

    def do_total(self, arg):
        """
            Total value of the stock.

            Each item counts quantity times price.


        """
        t = sum(q * p for q, p in self.stock.values())
        print(f"total {money(t)} over {len(self.stock)} items")

    def do_show(self, arg):
        q, p = self.stock.get(arg, (0, 0))
        print(f"{arg!r}: qty={q} price={money(p)}")

    def do_ping(self, arg):
        """
        """
        print("pong" + (" " + arg if arg else ""))

    def do_shell(self, arg):
        print(f"(not running) {arg}")

    def do_history(self, arg):
        """Show the lines read so far, across sessions."""
        for i, h in enumerate(self.history, 1):
            print(f"{i:>3} {h!r}")

    def do_columns(self, arg):
        """columns WIDTH WORD...: lay the words out as help does."""
        words = arg.split()
        if not words or not words[0].isascii() or not words[0].isdigit():
            print("usage: columns WIDTH WORD...")
            return
        self.columnize(words[1:], int(words[0]))

    def do_complete(self, arg):
        # What Tab would offer at the end of ARG: the word being typed is
        # the text after the last space.
        line = arg
        text = line[line.rfind(" ") + 1:]
        begidx = len(line) - len(text)
        endidx = len(line)
        if begidx > 0:
            c, _, _ = self.parseline(line)
            if c == "":
                f = self.completedefault
            else:
                f = getattr(self, "complete_" + c, self.completedefault)
        else:
            f = self.completenames
        got = sorted(f(text, line, begidx, endidx))
        print(f"{text!r}: " + (" ".join(got) if got else "(none)"))

    def help_pricing(self):
        print("Prices are in dollars with at most two decimals: 3, 3.5, 3.50.")

    def help_EOF(self):
        print("End of input ends the session.")

    def do_quit(self, arg):
        """Leave the console."""
        print("bye")
        return True

    def do_EOF(self, arg):
        print()
        return True


def main():
    stock = {}
    history = []
    folder = os.path.join("data", "sessions")
    for name in sorted(os.listdir(folder)):
        print(f"==== {name}")
        with open(os.path.join(folder, name), encoding="utf-8", newline="") as fh:
            Inventory(stock, fh, history).cmdloop()


main()
