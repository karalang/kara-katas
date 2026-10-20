# Runs data/jobs.tsv through Python's own decimal module, the pure-Python
# _pydecimal that mini_decimal ports, and prints what expected.out holds.
import _pydecimal as decimal
from _pydecimal import Decimal, Context, getcontext, setcontext, localcontext

ROUNDINGS = ["ROUND_DOWN", "ROUND_HALF_UP", "ROUND_HALF_EVEN", "ROUND_CEILING",
             "ROUND_FLOOR", "ROUND_UP", "ROUND_HALF_DOWN", "ROUND_05UP"]
SIGNALS = {s.__name__: s for s in decimal._signals}
CENT = Decimal("0.01")


def err(e):
    return f"{type(e).__name__}: {e}"


def show(v):
    if isinstance(v, tuple) and not hasattr(v, "_fields"):
        return "(" + ", ".join(show(x) for x in v) + ")"
    return repr(v)


def arg(a):
    if a.startswith("i:"):
        return int(a[2:])
    if a.startswith("f:"):
        return float(a[2:])
    return Decimal(a)


def make_context(spec):
    base = decimal.DefaultContext
    words = spec.split(" ") if spec else []
    for w in words:
        if w.startswith("base="):
            base = {"default": decimal.DefaultContext, "basic": decimal.BasicContext,
                    "extended": decimal.ExtendedContext}[w[5:]]
    c = base.copy()
    c.clear_flags()
    for w in words:
        k, _, v = w.partition("=")
        if k == "base":
            continue
        if k == "traps":
            c.clear_traps()
            for t in v.split(",") if v else []:
                c.traps[SIGNALS[t]] = 1
        elif k == "rounding":
            c.rounding = v
        else:
            setattr(c, k, int(v))
    return c


def op(name, a):
    c = getcontext()
    if name == "new":
        return Decimal(arg(a[0]))
    if name == "create":
        return c.create_decimal(a[0])
    if name == "fromfloat":
        return Decimal.from_float(float(a[0]))
    x = arg(a[0])
    if name == "tuple":
        return x.as_tuple()
    if name == "ratio":
        return x.as_integer_ratio()
    if name == "str":
        return str(x)
    if name == "eng":
        return x.to_eng_string()
    if name == "neg":
        return -x
    if name == "pos":
        return +x
    if name == "round":
        return round(x, int(a[1])) if len(a) > 1 else round(x)
    if name == "floor":
        import math
        return math.floor(x)
    if name == "ceil":
        import math
        return math.ceil(x)
    if name == "int":
        return int(x)
    if name == "sqrt":
        return x.sqrt()
    if name == "exp":
        return x.exp()
    if name == "ln":
        return x.ln()
    if name == "log10":
        return x.log10()
    if name == "logb":
        return x.logb()
    if name == "nextplus":
        return x.next_plus()
    if name == "nextminus":
        return x.next_minus()
    if name == "class":
        return x.number_class()
    if name == "isnormal":
        return x.is_normal()
    if name == "issubnormal":
        return x.is_subnormal()
    if name == "adjusted":
        return x.adjusted()
    if name == "invert":
        return x.logical_invert()
    if name == "copyabs":
        return x.copy_abs()
    if name == "copynegate":
        return x.copy_negate()
    if name == "normalize":
        return x.normalize()
    if name == "integral":
        return x.to_integral_value()
    if name == "integralx":
        return x.to_integral_exact()
    if name == "format":
        return format(x, a[1])
    if name == "quantize":
        return x.quantize(arg(a[1]), a[2] if len(a) > 2 else None)
    y = arg(a[1])
    two = {
        "add": lambda: x + y, "sub": lambda: x - y, "mul": lambda: x * y,
        "div": lambda: x / y, "floordiv": lambda: x // y, "mod": lambda: x % y,
        "divmod": lambda: divmod(x, y), "pow": lambda: x ** y,
        "remnear": lambda: x.remainder_near(y),
        "eq": lambda: x == y, "lt": lambda: x < y, "ge": lambda: x >= y,
        "compare": lambda: x.compare(y), "cmpsignal": lambda: x.compare_signal(y),
        "cmptotal": lambda: x.compare_total(y), "cmptotalmag": lambda: x.compare_total_mag(y),
        "max": lambda: x.max(y), "min": lambda: x.min(y),
        "maxmag": lambda: x.max_mag(y), "minmag": lambda: x.min_mag(y),
        "nexttoward": lambda: x.next_toward(y), "samequantum": lambda: x.same_quantum(y),
        "scaleb": lambda: x.scaleb(y), "rotate": lambda: x.rotate(y), "shift": lambda: x.shift(y),
        "and": lambda: x.logical_and(y), "or": lambda: x.logical_or(y),
        "xor": lambda: x.logical_xor(y), "copysign": lambda: x.copy_sign(y),
    }
    if name in two:
        return two[name]()
    z = arg(a[2])
    if name == "powmod":
        return pow(x, y, z)
    if name == "fma":
        return x.fma(y, z)
    raise AssertionError(name)


def flags():
    names = [s.__name__ for s, v in getcontext().flags.items() if v]
    return f" {{{', '.join(names)}}}" if names else ""


# ------------------------------------------------------------ programs

def read_rows(name, sep="\t"):
    with open("data/" + name) as f:
        return [line.rstrip("\n").split(sep) for line in f if line.strip()]


def invoices(path):
    rows = read_rows(path, ",")[1:]
    order = []
    lines = {}
    for inv, item, qty, price, rate in rows:
        if inv not in lines:
            order.append(inv)
            lines[inv] = []
        lines[inv].append((item, Decimal(qty), Decimal(price), Decimal(rate)))
    grand = Decimal(0)
    for inv in order:
        print(f"  {inv}")
        net_total = Decimal(0)
        vat_total = Decimal(0)
        by_rate = {}
        for item, qty, price, rate in lines[inv]:
            net = (qty * price).quantize(CENT, decimal.ROUND_HALF_UP)
            vat = (net * rate / 100).quantize(CENT, decimal.ROUND_HALF_UP)
            net_total += net
            vat_total += vat
            by_rate[rate] = by_rate.get(rate, Decimal(0)) + net
            print(f"    {item:<18}{qty:>6} x {price:>9} = {net:>10,.2f}  VAT {rate:>3}% {vat:>8,.2f}")
        on_totals = sum((n * r / 100).quantize(CENT, decimal.ROUND_HALF_UP)
                        for r, n in sorted(by_rate.items()))
        gross = net_total + vat_total
        grand += gross
        print(f"    net {net_total:,.2f}  vat {vat_total:,.2f}  gross {gross:,.2f}")
        print(f"    vat by rate {on_totals:,.2f}  difference {on_totals - vat_total:+.2f}")
    print(f"  all invoices {grand:,.2f}")


def fx(rates_path, conv_path):
    rates = {}
    places = {}
    for cur, rate, p in read_rows(rates_path):
        rates[cur] = Decimal(rate)
        places[cur] = Decimal(10) ** -int(p)
    for amount, src, dst in read_rows(conv_path):
        a = Decimal(amount)
        usd = a / rates[src]
        out = (usd * rates[dst]).quantize(places[dst])
        with localcontext() as c:
            c.prec = 10
            cross = rates[dst] / rates[src]
        print(f"  {amount:>10} {src} = {out} {dst}  (rate {cross}, exact {usd * rates[dst]})")
    with localcontext() as c:
        c.prec = 6
        c.traps[decimal.Inexact] = True
        try:
            print(f"  strict {Decimal(1) / rates['GBP']}")
        except decimal.Inexact as e:
            print(f"  strict GBP rate: {err(e)}")


def loans(path):
    for name, principal, rate, months in read_rows(path):
        p = Decimal(principal)
        n = int(months)
        r = Decimal(rate) / 100 / 12
        if r:
            payment = (p * r / (1 - (1 + r) ** -n)).quantize(CENT, decimal.ROUND_HALF_UP)
        else:
            payment = (p / n).quantize(CENT, decimal.ROUND_HALF_UP)
        print(f"  {name}: {p:,.2f} at {rate}% over {n} months, payment {payment:,.2f}")
        balance = p
        paid_interest = Decimal(0)
        for m in range(1, n + 1):
            interest = (balance * r).quantize(CENT, decimal.ROUND_HALF_UP)
            pay = payment if m < n else balance + interest
            balance = balance + interest - pay
            paid_interest += interest
            if m <= 3 or m == n:
                print(f"    {m:>3} interest {interest:>9,.2f} principal {pay - interest:>10,.2f} balance {balance:>12,.2f}")
        print(f"    total interest {paid_interest:,.2f}, last payment {pay:,.2f}")


def bills(path):
    for label, subtotal, tax, tip, people in read_rows(path):
        s = Decimal(subtotal)
        t = (s * Decimal(tax) / 100).quantize(CENT, decimal.ROUND_HALF_UP)
        g = (s * Decimal(tip) / 100).quantize(CENT, decimal.ROUND_HALF_UP)
        total = s + t + g
        k = int(people)
        share = (total / k).quantize(CENT, decimal.ROUND_DOWN)
        extra = int((total - share * k) / CENT)
        shares = [share + CENT if i < extra else share for i in range(k)]
        print(f"  {label}: {s} + tax {t} + tip {g} = {total} for {k}")
        print(f"    {' '.join(str(x) for x in shares)} (sum {sum(shares)})")


def tax(brackets_path, incomes_path):
    brackets = [(Decimal(lo), Decimal(rate) / 100) for lo, rate in read_rows(brackets_path)]
    for (inc,) in read_rows(incomes_path):
        income = Decimal(inc)
        owed = Decimal(0)
        marginal = brackets[0][1]
        for i, (lo, rate) in enumerate(brackets):
            hi = brackets[i + 1][0] if i + 1 < len(brackets) else None
            if income <= lo:
                break
            top = income if hi is None or income < hi else hi
            owed += (top - lo) * rate
            marginal = rate
        owed = owed.quantize(CENT, decimal.ROUND_HALF_EVEN)
        effective = owed / income
        print(f"  {income:>14,.2f} tax {owed:>12,.2f} effective {effective:.2%} marginal {marginal:.0%}")


def growth(path):
    with localcontext() as c:
        c.prec = 12
        for p, rate, years in read_rows(path):
            principal = Decimal(p)
            r = Decimal(rate) / 100
            y = int(years)
            yearly = principal * (1 + r) ** y
            continuous = principal * (r * y).exp()
            doubling = Decimal(2).ln() / (1 + r).ln()
            print(f"  {principal} at {rate}% for {y} years: yearly {yearly:.2f} continuous {continuous:.2f}")
            print(f"    doubles in {doubling:.3f} years, log10 of final {yearly.log10():.6f}, {yearly.to_eng_string()}")


def stats(path):
    prices = [Decimal(x) for (x,) in read_rows(path)]
    with localcontext() as c:
        c.prec = 30
        n = len(prices)
        mean = sum(prices) / n
        srt = sorted(prices)
        median = (srt[n // 2 - 1] + srt[n // 2]) / 2 if n % 2 == 0 else srt[n // 2]
        var = sum((x - mean) ** 2 for x in prices) / n
        sd = var.sqrt()
        returns = [(prices[i] / prices[i - 1]).ln() for i in range(1, n)]
        total = sum(returns)
    print(f"  n {n} mean {mean} median {median}")
    print(f"  variance {var}")
    print(f"  stdev {sd} ~ {sd.quantize(Decimal('0.0001'))}")
    print(f"  log return {total:.10f} = ln({prices[-1]}/{prices[0]}) {(prices[-1] / prices[0]).ln():.10f}")
    print(f"  best day {max(returns):.6f} worst day {min(returns):.6f}")


PROGRAMS = {"invoices": invoices, "fx": fx, "loans": loans, "bills": bills,
            "tax": tax, "growth": growth, "stats": stats}


def main():
    with open("data/jobs.tsv") as f:
        lines = [l.rstrip("\n") for l in f if l.strip()]
    for line in lines:
        a = line.split("\t")
        if a[0] == "job":
            print(f"== {a[1]}")
            setcontext(make_context(""))
            continue
        if a[0] == "ctx":
            try:
                c = make_context(a[1])
            except Exception as e:
                print(f"  ctx {a[1]} -> {err(e)}")
                continue
            setcontext(c)
            print(f"  ctx {a[1]} -> {c!r}")
            continue
        if a[0] == "ctxrepr":
            print(f"  {getcontext()!r}")
            continue
        if a[0] in PROGRAMS:
            PROGRAMS[a[0]](*a[1:])
            continue
        getcontext().clear_flags()
        try:
            v = show(op(a[0], a[1:]))
        except Exception as e:
            v = err(e)
        print(f"  {' '.join(a)} -> {v}{flags()}")


main()
