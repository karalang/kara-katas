# Writes data/: the files the programs read, and jobs.tsv, the jobs.
import os

os.makedirs("data", exist_ok=True)


def write(name, text):
    with open(os.path.join("data", name), "w") as f:
        f.write(text)


write("invoices.csv", """invoice,item,qty,unit_price,vat_rate
INV-1001,Desk lamp,2,34.99,20
INV-1001,LED bulb,12,2.49,20
INV-1001,Shipping,1,5.95,0
INV-1002,Notebook,25,1.15,5
INV-1002,Fountain pen,3,18.333,20
INV-1002,Ink cartridge,10,0.875,20
INV-1003,Consulting hours,7.5,120.00,20
INV-1003,Travel,1,86.415,0
INV-1003,Discount,1,-50.00,20
INV-1004,Paper (ream),40,4.125,5
INV-1004,Toner,2,1E2,20
""")

write("rates.tsv", """USD\t1\t2
EUR\t0.9187\t2
GBP\t0.78645\t2
JPY\t149.8350\t0
BHD\t0.376\t3
CHF\t0.8812\t2
INR\t83.1275\t2
""")

write("conversions.tsv", """100.00\tUSD\tEUR
2500\tEUR\tJPY
19.99\tGBP\tUSD
1000000\tJPY\tINR
75.125\tBHD\tCHF
0.01\tUSD\tJPY
12.345\tCHF\tGBP
9.995\tUSD\tEUR
""")

write("loans.tsv", """car\t18500.00\t6.9\t60
mortgage\t320000\t5.875\t360
student\t27350.50\t4.53\t120
zero\t2400\t0\t12
tiny\t500\t19.99\t6
""")

write("bills.tsv", """team lunch\t187.40\t8.875\t18\t7
birthday\t432.15\t8.875\t20\t9
coffee\t14.85\t0\t15\t4
pizza\t60\t0\t0\t3
""")

write("brackets.tsv", """0\t10
11600\t12
47150\t22
100525\t24
191950\t32
243725\t35
609350\t37
""")

write("incomes.tsv", """9500
11600
58250.75
150000
243725
1000000
""")

write("growth.tsv", """1000\t5\t10
2500.50\t3.25\t30
100\t7\t72
1\t100\t1
""")

write("prices.tsv", """101.25
99.80
102.10
103.45
100.05
98.70
104.20
105.00
103.85
106.40
""")

J = []


def job(title, *lines):
    J.append("job\t" + title)
    for l in lines:
        J.append(l)


job("construct from strings",
    "new\t3.14", "new\t  -0.000  ", "new\t1_000.5", "new\t1e+3", "new\t-1E-3",
    "new\t.5", "new\t5.", "new\t+12.3400", "new\tInf", "new\t-infinity",
    "new\tnan", "new\tsNaN123", "new\t-NaN0045", "new\t0E-1000", "new\t1.5e999999",
    "new\tabc", "new\t1.2.3", "new\t", "new\t1 000", "new\t١٢٣")
job("conversion syntax with the trap off",
    "ctx\ttraps=",
    "new\tabc", "new\t12e", "add\t1\tfoo", "create\t 7 ", "create\t1_0", "create\tNaN12345678901234567890123456789")
job("ints, floats and tuples",
    "new\ti:12345678901234567890", "new\ti:-7", "new\tf:0.1", "new\tf:-0.0", "new\tf:1e300",
    "new\tf:inf", "new\tf:nan", "fromfloat\t2.5", "fromfloat\t1.1", "fromfloat\t1e-7",
    "tuple\t3.14", "tuple\t-0", "tuple\tInf", "tuple\tsNaN7", "tuple\t1.500E+8",
    "ratio\t3.14", "ratio\t-123e5", "ratio\t0.00", "ratio\t0.0625", "ratio\tInf", "ratio\tNaN")
job("str, repr and to_eng_string",
    "str\t123E+1", "str\t0.000001", "str\t0.0000001", "str\t-1.20E-7", "str\t1E+2",
    "str\t0E-8", "eng\t123E+1", "eng\t1E+7", "eng\t0.0000001", "eng\t0E-8", "eng\t0E+1",
    "eng\t-12.3E-10", "eng\t5E+2", "ctx\tcapitals=0", "str\t1E+5", "eng\t1E+5")
job("addition and subtraction",
    "add\t1.1\t2.2", "add\t1.30\t1.20", "add\t1E+2\t1E-2", "add\t-5\t5", "add\t0.00\t-0",
    "sub\t1.3\t1.07", "sub\t1.3\t2.07", "add\t9999999999999999999999999999\t1",
    "add\t1E+50\t1", "add\t1\t1E-40", "add\tInf\t-Inf", "add\tInf\t5", "add\tNaN3\t1",
    "sub\t-Inf\t-Inf", "add\t1\ti:41", "add\t1\tf:0.5", "ctx\trounding=ROUND_FLOOR",
    "add\t5\t-5", "sub\t0\t0", "neg\t0", "pos\t-0")
job("multiplication and division",
    "mul\t1.20\t3", "mul\t-7\t1E-3", "mul\t0\t-Inf", "mul\tInf\t-2", "mul\t1.5\t1.5",
    "div\t1\t3", "div\t2\t3", "div\t1\t4", "div\t12\t12", "div\t8.00\t2", "div\t2.400\t2.0",
    "div\t1000\t1E-3", "div\t1\t0", "div\t0\t0", "div\t-0\t5", "div\tInf\tInf", "div\t5\tInf",
    "div\t2.40E+6\t2", "div\t1\ti:7")
job("integer division and remainders",
    "floordiv\t7\t2", "floordiv\t-7\t2", "mod\t-7\t2", "mod\t7\t-2", "mod\t10\t3.3",
    "divmod\t7.5\t2", "divmod\t-7.5\t2", "divmod\t1\t0", "divmod\tInf\t3", "floordiv\t1E+40\t3",
    "remnear\t10\t6", "remnear\t2.1\t3", "remnear\t-10\t3", "remnear\t3.6\t1.3", "remnear\t10\t0.3",
    "remnear\t1E+40\t3", "mod\t5\t0", "floordiv\t0\t0")
job("powers",
    "pow\t2\t10", "pow\t2\t-2", "pow\t10\t-3", "pow\t1.1\t2", "pow\t-2\t3", "pow\t-2\t-3",
    "pow\t4\t0.5", "pow\t2\t0.5", "pow\t8\t1/3", "pow\t8\t0.333", "pow\t1.0\t5", "pow\t1.00\t-3",
    "pow\t0\t0", "pow\t0\t-1", "pow\t-0\t-1", "pow\tInf\t-1", "pow\t-1.5\t0.5", "pow\t1.0001\t10000",
    "pow\t0.9\t100", "pow\t10\t1000000", "pow\t3\t-0.75", "pow\t25\t-0.5", "pow\t1E-5\t2.5",
    "powmod\t3\t200\t7", "powmod\t-2\t3\t5", "powmod\t2.5\t2\t3", "powmod\t2\t-1\t3")
job("quantize and rounding modes",
    "quantize\t1.41421356\t0.001", "quantize\t2.5\t1", "quantize\t3.5\t1", "quantize\t-2.5\t1",
    "quantize\t1.005\t0.01\tROUND_HALF_UP", "quantize\t1.005\t0.01\tROUND_HALF_DOWN",
    "quantize\t1.015\t0.01\tROUND_HALF_EVEN", "quantize\t1.001\t0.01\tROUND_UP",
    "quantize\t-1.009\t0.01\tROUND_DOWN", "quantize\t-1.001\t0.01\tROUND_FLOOR",
    "quantize\t-1.009\t0.01\tROUND_CEILING", "quantize\t1.04\t0.1\tROUND_05UP",
    "quantize\t1.06\t0.1\tROUND_05UP", "quantize\t1.51\t0.1\tROUND_05UP",
    "quantize\t123.456\t1E+1", "quantize\t0\t1E-5", "quantize\t1E+30\t0.01", "quantize\tInf\t1",
    "quantize\tInf\t-Inf", "quantize\t1\tNaN", "quantize\t5\t1E+1000000",
    "round\t2.675\t2", "round\t2.5", "round\t-0.5", "round\t123.456\t-1", "round\tInf", "round\tNaN",
    "floor\t-1.5", "ceil\t-1.5", "int\t-9.99", "int\t1E+3", "int\tInf", "int\tNaN")
job("rounding to the context",
    "ctx\tprec=5",
    "pos\t1.23456789", "pos\t99999.5", "pos\t-99999.5", "add\t12345\t0.5", "mul\t123\t456",
    "ctx\tprec=5 rounding=ROUND_DOWN", "pos\t1.23459", "ctx\tprec=5 rounding=ROUND_UP", "pos\t1.23451",
    "ctx\tprec=5 rounding=ROUND_CEILING", "pos\t-1.23459", "ctx\tprec=5 rounding=ROUND_05UP",
    "pos\t1.23409", "pos\t1.23459", "ctx\tprec=3 rounding=ROUND_HALF_DOWN", "pos\t2.345", "pos\t2.3451")
job("overflow, underflow and clamping",
    "ctx\tprec=5 Emax=99 Emin=-99 traps=",
    "mul\t1E+99\t10", "pos\t9.99999E+99", "mul\t1E-99\t1E-3", "div\t1E-99\t1E+10", "pos\t1.2345E-102",
    "pos\t0E-200", "pos\t0E+200", "ctx\tprec=5 Emax=99 Emin=-99 traps= rounding=ROUND_DOWN",
    "mul\t1E+99\t10", "mul\t-1E+99\t10", "ctx\tprec=5 Emax=99 Emin=-99 traps= rounding=ROUND_FLOOR",
    "mul\t1E+99\t10", "mul\t-1E+99\t10", "ctx\tprec=5 Emax=99 Emin=-99 clamp=1 traps=",
    "pos\t1E+99", "pos\t1.2E+97", "normalize\t1.20000E+98", "ctx\tprec=5 Emax=99 Emin=-99",
    "mul\t1E+99\t10", "ctx\tprec=5 Emax=99 Emin=-99 traps=Underflow,Inexact", "div\t1\t3",
    "mul\t1E-99\t1E-3")
job("square roots, exp and logs",
    "sqrt\t2", "sqrt\t100", "sqrt\t0.0100", "sqrt\t1E-7", "sqrt\t-1", "sqrt\t-0", "sqrt\tInf",
    "sqrt\t1.21", "sqrt\t9E+5", "exp\t1", "exp\t0", "exp\t-1", "exp\t2.302585092994045684017991455",
    "exp\t100", "exp\t-Inf", "exp\t1E-30", "exp\t1E+10", "ln\t10", "ln\t2", "ln\t0.5", "ln\t1",
    "ln\t0", "ln\t-1", "ln\t1E+100", "log10\t1000", "log10\t2", "log10\t0.001", "log10\t0.002",
    "log10\t1.0000001", "logb\t250", "logb\t0", "logb\t-0.001", "ctx\tprec=50", "sqrt\t2", "ln\t3",
    "exp\t0.5", "ctx\tprec=6", "sqrt\t2", "exp\t10", "ln\t1.000001", "log10\t31622.8")
job("comparisons",
    "eq\t1.0\t1", "eq\t0\t-0", "eq\tNaN\tNaN", "eq\tsNaN\t1", "lt\t1.1\t1.10001", "lt\tNaN\t1",
    "ge\t-Inf\t-1E+999", "lt\t1.1\tf:1.1", "eq\t0.5\tf:0.5", "eq\t2\ti:2",
    "compare\t2.1\t3", "compare\t2.1\t2.10", "compare\tNaN\t1", "cmpsignal\tNaN\t1",
    "cmptotal\t12.30\t12.3", "cmptotal\t-0\t0", "cmptotal\tNaN\tInf", "cmptotal\tsNaN2\tNaN1",
    "cmptotal\t-NaN\t-sNaN", "cmptotalmag\t-3\t2", "max\t1\t2", "max\t1.0\t1", "max\t-0\t0",
    "max\tNaN\t3", "min\t1.00\t1.0", "min\tsNaN\t3", "maxmag\t-3\t2", "minmag\t-3\t2", "minmag\t-2\t2")
job("next values and classes",
    "nextplus\t1", "nextplus\t-1E-1000007", "nextminus\t1", "nextminus\tInf", "nextplus\t-Inf",
    "nexttoward\t1\t2", "nexttoward\t1\t0", "nexttoward\t1\t1.0", "nexttoward\t-1\t-1",
    "ctx\tprec=5 Emax=99 Emin=-99 traps=", "nexttoward\t9.9999E+99\tInf", "nexttoward\t1E-103\t0",
    "nextplus\t9.9999E+99", "class\t0", "class\t-0", "class\t1E-100", "class\t-1E-101",
    "class\t2.50", "class\t-Inf", "class\tNaN", "class\tsNaN", "isnormal\t1E-99",
    "issubnormal\t1E-100", "adjusted\t123.45", "adjusted\t0.001", "adjusted\tInf",
    "samequantum\t2.17\t0.001", "samequantum\t2.17\t0.01", "samequantum\tInf\t-Inf",
    "samequantum\tNaN\t1")
job("digit operations",
    "ctx\tprec=9", "scaleb\t7.50\t-2", "scaleb\t7.50\t3", "scaleb\t1\t1.5", "rotate\t34\t8",
    "rotate\t12\t9", "rotate\t123456789\t-2", "rotate\t123456789\t10", "shift\t34\t8", "shift\t12\t9",
    "shift\t123456789\t-2", "shift\t123456789\t+2", "and\t1101\t1011", "or\t1101\t1011",
    "xor\t1101\t1011", "invert\t101", "invert\t0", "and\t12\t1", "copysign\t1.50\t-7",
    "copyabs\t-Inf", "copynegate\t0", "normalize\t120.000", "normalize\t0.00", "normalize\t-1E+1",
    "integral\t2.5", "integral\t-1.7", "integralx\t2.5", "integralx\t7.0", "integralx\t1E+3",
    "fma\t2\t3\t4", "fma\t1E+27\t1E+27\t-1E+54", "fma\tInf\t0\t1")
job("formatting",
    "format\t1234567.891\t,.2f", "format\t1234567.891\t_.1f", "format\t-0.000\t.2f",
    "format\t-0.000\tz.2f", "format\t0.5\t.0%", "format\t0.12345\t.1%", "format\t123.456\te",
    "format\t123.456\t.2E", "format\t0.000012\tg", "format\t12345678\t.3g", "format\t1.5\t#.0f",
    "format\t42\t>10", "format\t42\t*^9.1f", "format\t-42\t=+10.2f", "format\t42\t010,.1f",
    "format\t42\t 08.3f", "format\tInf\t>8", "format\t-Inf\t.2%", "format\tNaN\t+f",
    "format\t1E+5\t", "format\t1E+5\tf", "format\t0E+3\tf", "format\t0E-3\te", "format\t123.456\t.0e",
    "format\t1234567\tn", "format\t1\t.2x", "format\t1\t0<5", "ctx\tcapitals=0", "format\t1E+20\t",
    "format\t7E+2\t.3", "ctx\trounding=ROUND_DOWN", "format\t2.999\t.2f", "format\t-2.999\t.0f")
job("contexts",
    "ctxrepr", "ctx\tbase=basic", "div\t1\t3", "ctx\tbase=extended", "div\t1\t0", "div\t0\t0",
    "sqrt\t-4", "ctx\tbase=extended prec=3 rounding=ROUND_UP capitals=0 clamp=1", "div\t2\t3",
    "ctx\tprec=0", "ctx\tEmin=5", "ctx\tcapitals=2", "ctx\trounding=ROUND_SIDEWAYS",
    "ctx\tprec=7 traps=Inexact", "div\t1\t8", "div\t1\t3", "add\t1.0000001\t0")
job("invoices", "invoices\tinvoices.csv")
job("currency conversion", "fx\trates.tsv\tconversions.tsv")
job("loan amortization", "loans\tloans.tsv")
job("bill splitting", "bills\tbills.tsv")
job("income tax", "tax\tbrackets.tsv\tincomes.tsv")
job("savings growth", "growth\tgrowth.tsv")
job("price statistics", "stats\tprices.tsv")

write("jobs.tsv", "\n".join(J) + "\n")
