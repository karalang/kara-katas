"""Writes data/ for mini_ledger: a chart of accounts, the 2025 and 2026
journals of one household, market prices, a card statement as the bank
exports it with the rules that import it, a file of mistakes, and the
reports to run. The month-end balance assertions are computed here, from
the same amounts the journals carry.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)

seed = 11


def rnd(n):
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return (seed // 65536) % n


def usd(c):
    """cents as the journal writes them, with grouping."""
    neg = c < 0
    c = abs(c)
    s = f"{c // 100:,}.{c % 100:02d}"
    return ("-" if neg else "") + s


checking = 0  # cents, tracked for the assertions
savings = 0


def txn(out, date, payee, narr, postings, flag="*"):
    head = f"{date} {flag} {payee}" + (f" | {narr}" if narr else "")
    out.append(head)
    for acc, amt in postings:
        out.append(f"  {acc}  {amt}" if amt else f"  {acc}")
    out.append("")


def chk(c):
    global checking
    checking += c
    return f"{usd(c)} USD"


def month_days(y, m):
    if m == 2:
        return 29 if y % 4 == 0 else 28
    return 30 if m in (4, 6, 9, 11) else 31


GROCERS = ["Whole Foods", "Trader Joe's", "Safeway", "Berkeley Bowl"]
DINERS = ["Chez Panisse", "Zachary's Pizza", "Burma Superstar", "Tacos Sinaloa"]


def year_2025():
    global savings, checking
    out = ["; 2025: salary, rent, the broker and a trip to Lisbon", ""]
    txn(out, "2025-01-01", "Opening balances", "", [
        ("Assets:Bank:Checking", chk(420000)),
        ("Assets:Bank:Savings", "12,000.00 USD"),
        ("Assets:Bank:Old-Checking", "250.00 USD"),
        ("Assets:Broker:Cash", "3,000.00 USD"),
        ("Equity:Opening-Balances", None),
    ])
    savings += 1200000
    for m in range(1, 13):
        ym = f"2025-{m:02d}"
        if m > 1:
            out.append(f"{ym}-01 balance Assets:Bank:Checking {usd(checking)} USD")
            out.append("")
        rent = 185000
        txn(out, f"{ym}-01", "Parkview Apartments", "Rent", [
            ("Expenses:Rent", f"{usd(rent)} USD"), ("Assets:Bank:Checking", chk(-rent))])
        u = 9000 + rnd(7000)
        txn(out, f"{ym}-05", "PG&E", "", [
            ("Expenses:Utilities", f"{usd(u)} USD"), ("Assets:Bank:Checking", chk(-u))])
        for k in range(3):
            g = 4000 + rnd(9000)
            day = 4 + k * 8 + rnd(4)
            txn(out, f"{ym}-{day:02d}", GROCERS[rnd(4)], "", [
                ("Expenses:Food:Groceries", f"{usd(g)} USD"), ("Assets:Bank:Checking", chk(-g))])
        if m != 6:
            r = 3500 + rnd(6000)
            txn(out, f"{ym}-{18 + rnd(5):02d}", DINERS[rnd(4)], "Dinner", [
                ("Expenses:Food:Restaurants", f"{usd(r)} USD"), ("Assets:Bank:Checking", chk(-r))])
        for day in (15, month_days(2025, m)):
            txn(out, f"{ym}-{day:02d}", "Acme Robotics", "Salary", [
                ("Assets:Bank:Checking", chk(320000)), ("Income:Salary", "-3,200.00 USD")])
        interest = savings * 35 // 12000
        savings += interest
        txn(out, f"{ym}-{month_days(2025, m):02d}", "Ally Bank", "Interest", [
            ("Assets:Bank:Savings", f"{usd(interest)} USD"), ("Income:Interest", None)])
        if m == 2:
            txn(out, "2025-02-03", "Transfer", "To the broker", [
                ("Assets:Broker:Cash", "6,000.00 USD"), ("Assets:Bank:Checking", chk(-600000))])
            txn(out, "2025-02-10", "Fidelity", "Buy AAPL", [
                ("Assets:Broker:Stocks", "10 AAPL {187.50 USD}"), ("Assets:Broker:Cash", None)])
        if m == 3:
            txn(out, "2025-03-03", "Fidelity", "Buy VTI", [
                ("Assets:Broker:Stocks", "20 VTI {270.10 USD}"), ("Assets:Broker:Cash", None)])
            txn(out, "2025-03-15", "Transfer", "Empty the old account", [
                ("Assets:Bank:Checking", chk(25000)), ("Assets:Bank:Old-Checking", "-250.00 USD")])
            out.append("2025-03-31 close Assets:Bank:Old-Checking")
            out.append("")
        if m in (3, 6, 9, 12):
            div = 2400 + rnd(900)
            txn(out, f"{ym}-26", "Vanguard", "VTI dividend", [
                ("Assets:Broker:Cash", f"{usd(div)} USD"), ("Income:Dividends", None)])
        if m == 5:
            txn(out, "2025-05-12", "Fidelity", "Buy AAPL", [
                ("Assets:Broker:Stocks", "8 AAPL {201.25 USD}"), ("Assets:Broker:Cash", None)])
        if m == 6:
            # 1,500.00 EUR at 1.1342 USD is 1,701.30 USD.

            checking -= 170130
            txn(out, "2025-06-02", "Wise", "Euros for Lisbon", [
                ("Assets:Wise:EUR", "1,500.00 EUR @ 1.1342 USD"), ("Assets:Bank:Checking", None)])
            for day, payee, acc, amt in [
                (11, "Hotel Avenida", "Expenses:Travel", "640.00 EUR"),
                (12, "Time Out Market", "Expenses:Food:Restaurants", "38.60 EUR"),
                (13, "Carris", "Expenses:Transport:Transit", "12.40 EUR"),
                (14, "Cervejaria Ramiro", "Expenses:Food:Restaurants", "71.25 EUR"),
                (15, "Uber", "Expenses:Transport:Transit", "18.90 EUR"),
            ]:
                txn(out, f"2025-06-{day}", payee, "", [(acc, amt), ("Assets:Wise:EUR", None)])
        if m == 7:
            txn(out, "2025-07-01", "Transfer", "To the broker", [
                ("Assets:Broker:Cash", "4,500.00 USD"), ("Assets:Bank:Checking", chk(-450000))])
        if m == 8:
            txn(out, "2025-08-04", "Fidelity", "Buy MSFT", [
                ("Assets:Broker:Stocks", "5 MSFT {410.00 USD}"), ("Assets:Broker:Cash", None)])
        if m == 10:
            txn(out, "2025-10-06", "Transfer", "To savings", [
                ("Assets:Bank:Savings", "5,000.00 USD"), ("Assets:Bank:Checking", chk(-500000))])
            savings += 500000
        if m == 11:
            txn(out, "2025-11-14", "Fidelity", "Sell AAPL", [
                ("Assets:Broker:Stocks", "-12 AAPL {} @ 228.40 USD"),
                ("Assets:Broker:Cash", "2,735.85 USD"),
                ("Expenses:Fees", "4.95 USD"),
                ("Income:Capital-Gains", None),
            ])
    out.append(f"2026-01-01 balance Assets:Bank:Savings {usd(savings)} USD")
    return "\n".join(out) + "\n"


CARD = []  # (date, description, cents), oldest first


def card_rows():
    rows = []
    for m in (1, 2, 3):
        for k in range(4):
            day = 2 + k * 7 + rnd(5)
            shop = ["WHOLE FOODS MKT #10234", "TRADER JOE'S #127", "SAFEWAY 0981", "BERKELEY BOWL WEST"][rnd(4)]
            rows.append((f"2026-{m:02d}-{day:02d}", shop, -(3500 + rnd(9000))))
        rows.append((f"2026-{m:02d}-03", "NETFLIX.COM", -1549))
        rows.append((f"2026-{m:02d}-09", "SPOTIFY USA", -1199))
        rows.append((f"2026-{m:02d}-{11 + rnd(4):02d}", "SHELL OIL 57444", -(4200 + rnd(2500))))
        rows.append((f"2026-{m:02d}-{19 + rnd(5):02d}", "UBER   *TRIP  HELP.UBER.COM", -(1300 + rnd(2000))))
        rows.append((f"2026-{m:02d}-{6 + rnd(3):02d}", "BLUE BOTTLE COFFEE, OAKLAND", -(600 + rnd(500))))
        rows.append((f"2026-{m:02d}-{21 + rnd(5):02d}", "CHIPOTLE 1883", -(1400 + rnd(900))))
        rows.append((f"2026-{m:02d}-{14 + rnd(3):02d}", "AMZN Mktp US*2K4L19", -(1800 + rnd(6000))))
    rows.append(("2026-02-21", "APPLE STORE R014", -124900))
    rows.append(("2026-01-27", "PAYMENT - THANK YOU", 50000))
    rows.append(("2026-02-26", "PAYMENT - THANK YOU", 150000))
    rows.append(("2026-03-26", "PAYMENT - THANK YOU", 40000))
    rows.sort(key=lambda r: r[0])
    return rows


def bank_csv():
    rows = card_rows()
    bal = 0
    lines = []
    for date, desc, c in rows:
        bal += c
        CARD.append((date, desc, c))
        y, m, d = date.split("-")
        dd = f"{m}/{d}/{y}"
        amt = usd(c)
        if "," in amt:
            amt = f'"{amt}"'
        elif rnd(3) == 0 and c < 0:
            amt = "-$" + amt[1:]
        q = f'"{desc}"' if "," in desc or rnd(4) == 0 else desc
        bs = usd(bal)
        bs = f'"{bs}"' if "," in bs else bs
        lines.append(f"{dd},{q},{amt},{bs}")
    lines.reverse()
    # A row the bank garbled, in the middle of the statement.
    lines.insert(9, '13/45/2026,"REFUND, BAD DATE",5.00,0.00')
    return "Date,Description,Amount,Balance\n" + "\n".join(lines) + "\n"


def year_2026():
    global checking, savings
    pay = {d: c for d, desc, c in CARD if desc.startswith("PAYMENT")}
    out = ["; 2026, first quarter; the card's purchases come from the bank import", ""]
    for m in (1, 2, 3):
        ym = f"2026-{m:02d}"
        out.append(f"{ym}-01 balance Assets:Bank:Checking {usd(checking)} USD")
        out.append("")
        txn(out, f"{ym}-01", "Parkview Apartments", "Rent", [
            ("Expenses:Rent", "1,925.00 USD"), ("Assets:Bank:Checking", chk(-192500))])
        u = 11000 + rnd(6000)
        txn(out, f"{ym}-05", "PG&E", "", [
            ("Expenses:Utilities", f"{usd(u)} USD"), ("Assets:Bank:Checking", chk(-u))],
            flag="!" if m == 2 else "*")
        for day in (15, month_days(2026, m)):
            txn(out, f"{ym}-{day:02d}", "Acme Robotics", "Salary", [
                ("Assets:Bank:Checking", chk(345000)), ("Income:Salary", "-3,450.00 USD")])
        for d, c in pay.items():
            if d.startswith(ym):
                checking -= c
        interest = savings * 35 // 12000
        savings += interest
        txn(out, f"{ym}-{month_days(2026, m):02d}", "Ally Bank", "Interest", [
            ("Assets:Bank:Savings", f"{usd(interest)} USD"), ("Income:Interest", None)])
        if m == 1:
            txn(out, "2026-01-20", "Wise", "Euros for Porto", [
                ("Assets:Wise:EUR", "500.00 EUR @@ 541.65 USD"), ("Assets:Bank:Checking", chk(-54165))])
            txn(out, "2026-01-30", "Vanguard", "VTI dividend", [
                ("Assets:Broker:Cash", "31.07 USD"), ("Income:Dividends", None)])
        if m == 2:
            txn(out, "2026-02-09", "Fidelity", "Buy MSFT", [
                ("Assets:Broker:Stocks", "6 MSFT {398.60 USD}"), ("Assets:Broker:Cash", None)])
            txn(out, "2026-02-14", "Livraria Lello", "", [
                ("Expenses:Travel", "15.00 EUR"), ("Assets:Wise:EUR", None)])
        if m == 3:
            txn(out, "2026-03-10", "Fidelity", "Sell the AAPL bought in May", [
                ("Assets:Broker:Stocks", "-5 AAPL {201.25 USD} @ 241.10 USD"),
                ("Assets:Broker:Cash", "1,205.50 USD"),
                ("Income:Capital-Gains", None),
            ])
            out.append("2026-03-31 balance Assets:Broker:Stocks 11 MSFT")
            out.append("2026-03-31 balance Assets:Broker 1 AAPL")
            out.append("")
    out.append(f"2026-04-01 balance Assets:Bank:Checking {usd(checking)} USD")
    out.append(f"2026-04-01 balance Assets:Bank:Savings {usd(savings)} USD")
    return "\n".join(out) + "\n"


ACCOUNTS = """; the chart of accounts
2025-01-01 open Assets:Bank:Checking USD
2025-01-01 open Assets:Bank:Savings USD
2025-01-01 open Assets:Bank:Old-Checking USD
2025-01-01 open Assets:Broker:Cash USD
2025-01-01 open Assets:Broker:Stocks AAPL,VTI,MSFT
2025-01-01 open Assets:Wise:EUR EUR
2025-01-01 open Liabilities:Card:Visa USD
2025-01-01 open Equity:Opening-Balances
2025-01-01 open Income:Salary USD
2025-01-01 open Income:Interest USD
2025-01-01 open Income:Dividends USD
2025-01-01 open Income:Capital-Gains USD
2025-01-01 open Expenses:Rent USD
2025-01-01 open Expenses:Utilities USD
2025-01-01 open Expenses:Food:Groceries USD
2025-01-01 open Expenses:Food:Restaurants
2025-01-01 open Expenses:Food:Coffee USD
2025-01-01 open Expenses:Transport:Fuel USD
2025-01-01 open Expenses:Transport:Transit
2025-01-01 open Expenses:Travel
2025-01-01 open Expenses:Subscriptions USD
2025-01-01 open Expenses:Shopping USD
2025-01-01 open Expenses:Fees USD
2025-01-01 open Expenses:Uncategorized USD
"""


def prices():
    out = ["; month-end closing prices", ""]
    walk = {"AAPL": 18500, "VTI": 27000, "MSFT": 41500}
    eur = 10850
    for y, m in [(2025, k) for k in range(1, 13)] + [(2026, k) for k in (1, 2, 3)]:
        date = f"{y}-{m:02d}-{month_days(y, m):02d}"
        for c in walk:
            walk[c] += rnd(1800) - 700
            out.append(f"{date} price {c} {usd(walk[c])} USD")
        eur += rnd(260) - 120
        out.append(f"{date} price EUR {eur // 10000}.{eur % 10000:04d} USD")
    out.append("2026-03-31 price USD 0.9215 EUR")
    return "\n".join(out) + "\n"


RULES = """# Importing the Visa statement: first match wins, ignoring case.
account Liabilities:Card:Visa
currency USD
default Expenses:Uncategorized

match whole foods => Expenses:Food:Groceries => Whole Foods
match trader joe => Expenses:Food:Groceries => Trader Joe's
match safeway => Expenses:Food:Groceries => Safeway
match berkeley bowl => Expenses:Food:Groceries => Berkeley Bowl
match netflix => Expenses:Subscriptions => Netflix
match spotify => Expenses:Subscriptions => Spotify
match shell oil => Expenses:Transport:Fuel => Shell
match uber => Expenses:Transport:Transit => Uber
match blue bottle => Expenses:Food:Coffee
match chipotle => Expenses:Food:Restaurants => Chipotle
match payment - thank you => Assets:Bank:Checking => Card payment
"""

BROKEN = """; mistakes: each is refused or reported, and nothing else changes
2026-02-30 * Corner Store | a day that does not exist
  Expenses:Food:Groceries  10.00 USD
  Assets:Bank:Checking
2026-03-02 * Corner Store | does not balance
  Expenses:Food:Groceries  12.40 USD
  Assets:Bank:Checking  -12.39 USD

2026-03-03 * Corner Store | two postings without amounts
  Expenses:Food:Groceries
  Assets:Bank:Checking

2026-03-04 * Corner Store | a typo in the account
  Expenses:Food:Grocery  5.00 USD
  Assets:Bank:Checking

2026-03-05 * Old bank | the account was closed
  Assets:Bank:Old-Checking  5.00 USD
  Assets:Bank:Checking

2026-03-06 * Fidelity | sells more than it holds
  Assets:Broker:Stocks  -40 VTI {}
  Assets:Broker:Cash

2026-03-07 * Fidelity | a lot with no cost
  Assets:Broker:Stocks  3 VTI {}
  Assets:Broker:Cash

2026-03-08 * Cafe | a bad amount
  Expenses:Food:Restaurants  12.3.4 USD
  Assets:Bank:Checking

2026-03-09 * Wise | dollars into the euro account
  Assets:Wise:EUR  20.00 USD
  Assets:Bank:Checking

2026-03-10 * Fidelity | no lot at that cost
  Assets:Broker:Stocks  -2 AAPL {150.00 USD}
  Assets:Broker:Cash

2026-03-11 * Bank | nothing to fill in
  Expenses:Fees  0.00 USD
  Assets:Bank:Checking

2026-03-12 * Fidelity | dividends into a stock account
  Assets:Broker:Stocks  12.00 USD
  Income:Dividends

2026-02-01 * Credit union | not open yet
  Assets:Bank:Credit-Union  5.00 USD
  Assets:Bank:Checking

2026-06-01 open Assets:Bank:Credit-Union USD
2025-12-31 balance Assets:Bank:Savings 99.00 USD
  Expenses:Fees  1.00 USD
2026-01-15 pad Assets:Bank:Checking Equity:Opening-Balances
This line is not a directive
2026-01-01 open Assets:Bank:Checking USD
2026-03-13 * | no payee
  Expenses:Fees  1.00 USD
  Assets:Bank:Checking
2026-03-14 * Corner Store
  expenses:food  1.00 USD
  Assets:Bank:Checking
"""

REPORTS = """# one command a line
balance --depth 2
balance Expenses
balance --at 2025-06-30 Assets Liabilities
register Assets:Bank:Checking --from 2026-03-01
register Liabilities:Card --to 2026-01-20
register Assets:Broker:Stocks
value USD
value USD --at 2025-06-30
value EUR --at 2025-06-30
income 2025-01-01 2025-12-31
income 2026-01-01 2026-03-31
lots Assets:Broker
print 2025-11-14 2025-11-14
print 2026-01-20 2026-01-21
balance Equity:Nothing
register Assets:Nope
value
income 2026-03-31 2026-01-01
balance --depth x
income 2026-01-01 2026-02-30
frobnicate now
"""

files = {
    "accounts.journal": ACCOUNTS,
    "2025.journal": year_2025(),
    "bank.csv": bank_csv(),
    "bank.rules": RULES,
    "prices.journal": prices(),
    "zz_broken.journal": BROKEN,
    "reports.txt": REPORTS,
}
files["2026.journal"] = year_2026()
for name, text in files.items():
    with open(os.path.join("data", name), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
