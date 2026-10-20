# Writes data/: the CSV files the five programs read and jobs.tsv, the
# jobs oracle.py and mini_statistics.kara both run. The data comes from a
# fixed linear congruential generator, so every run writes the same bytes.
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


class Lcg:
    def __init__(self, seed):
        self.s = seed

    def next(self):
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) % (1 << 64)
        return self.s >> 33

    def below(self, n):
        return self.next() % n


def write(name, text):
    with open(os.path.join(DATA, name), "w", encoding="utf-8", newline="") as f:
        f.write(text)


def latency_csv():
    r = Lcg(7)
    lines = ["endpoint,ms"]
    endpoints = [("/api/login", 40, 25), ("/api/search", 120, 90), ("/api/cart", 30, 8),
                 ("/healthz", 2, 2)]
    for i in range(150):
        ep, base, spread = endpoints[r.below(4)]
        v = base + r.below(spread * 10) / 10
        if r.below(30) == 0:
            v = v * 12
        if ep == "/healthz":
            lines.append("%s,%d" % (ep, int(v)))
        elif r.below(5) == 0:
            lines.append("%s,%d" % (ep, int(v)))
        else:
            lines.append("%s,%.1f" % (ep, v))
        if i in (40, 97):
            lines.append("%s,timeout" % ep)
    lines.append("/api/export,1830.5")
    lines.append("/api/report,")
    return "\n".join(lines) + "\n"


def ab_csv():
    r = Lcg(11)
    lines = ["visitor,variant,revenue"]
    for i in range(140):
        variant = "AB"[r.below(2)]
        if r.below(3) == 0:
            rev = "0"
        else:
            rev = "%.2f" % ((20 if variant == "A" else 23) + r.below(2000) / 100)
        lines.append("v%04d,%s,%s" % (i, variant, rev))
    return "\n".join(lines) + "\n"


def load_csv():
    r = Lcg(5)
    lines = ["rps,p99_ms"]
    for i in range(36):
        rps = 50 + 25 * i + r.below(20)
        p99 = 35 + rps * 0.21 + r.below(400) / 10
        if i > 30:
            p99 += (i - 30) * 40
        lines.append("%d,%.1f" % (rps, p99))
    return "\n".join(lines) + "\n"


def survey_csv():
    r = Lcg(3)
    colors = ["blue", "green", "red", "purple", "black", "orange"]
    lines = ["respondent,age,color,commute_km,commute_kmh,raise_pct"]
    for i in range(90):
        age = 18 + r.below(50) + r.below(10)
        color = colors[r.below(6)]
        km = 1 + r.below(300) / 10
        kmh = 8 + r.below(70)
        raise_pct = "%.1f" % (r.below(120) / 10 - 1.5)
        lines.append("r%03d,%d,%s,%.1f,%d,%s" % (i, age, color, km, kmh, raise_pct))
    return "\n".join(lines) + "\n"


def sensors_csv():
    r = Lcg(13)
    lines = ["sensor,reading"]
    for i in range(80):
        s = "s%d" % (r.below(4) + 1)
        v = "%.3f" % (20 + r.below(5000) / 1000)
        if s == "s2" and r.below(8) == 0:
            v = "nan"
        if s == "s3" and i == 33:
            v = "inf"
        if s == "s4" and r.below(10) == 0:
            v = "-inf" if r.below(2) else "inf"
        if r.below(25) == 0:
            v = "ERR"
        lines.append("%s,%s" % (s, v))
    lines.append("s5,21.5")
    lines.append("s6,1e308")
    lines.append("s6,1e308")
    lines.append("s6,-1e308")
    return "\n".join(lines) + "\n"


def growth_csv():
    r = Lcg(17)
    lines = ["month,revenue"]
    rev = 12000.0
    for m in range(1, 25):
        rev = rev * (1 + (r.below(200) - 60) / 1000)
        lines.append("2025-%02d,%.2f" % (m, rev) if m <= 12 else "2026-%02d,%.2f" % (m - 12, rev))
    return "\n".join(lines) + "\n"


SCORES = ("105,129,87,86,111,111,89,81,108,92,110,100,75,105,103,109,76,119,99,91,103,129,106,"
          "101,84,111,74,87,86,103,103,106,86,111,75,87,102,121,111,88,89,101,106,95,103,107,101,"
          "81,109,104")

CALLS = [
    "mean\t1,2,3,4,4",
    "mean\t1,2,3,4",
    "mean\t2,4,6",
    "mean\t0.1,0.2,0.3",
    "mean\t3,2.25,4.5,-0.5,0.25",
    "mean\t1e50,1,-1e50,1e50,1,-1e50",
    "mean\t-0.0",
    "mean\t-",
    "mean\t1,nan,3",
    "mean\tinf,1,-inf",
    "mean\tinf,2",
    "mean\t1000000000.1,1000000000.2,1000000000.3",
    "fmean\t3.5,4.0,5.25",
    "fmean\t85,92,83,91\tweights=0.20,0.20,0.30,0.30",
    "fmean\t1,2,3\tweights=1,1,2",
    "fmean\t-",
    "fmean\t1,2\tweights=1",
    "fmean\t1,2\tweights=1,-1",
    "fmean\t1e308,1e308,-1e308",
    "fmean\tinf,-inf",
    "fmean\tnan,inf",
    "fmean\t0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1",
    "geometric_mean\t54,24,36",
    "geometric_mean\t1.5,2.5,4",
    "geometric_mean\t1,0,4",
    "geometric_mean\t2,-1",
    "geometric_mean\t2,-1.5,3",
    "geometric_mean\t-",
    "geometric_mean\tnan,1",
    "geometric_mean\t0,inf",
    "geometric_mean\t2,inf",
    "harmonic_mean\t40,60",
    "harmonic_mean\t40,60\tweights=5,30",
    "harmonic_mean\t2.5,3,10",
    "harmonic_mean\t1,0,2",
    "harmonic_mean\t1,-2,0",
    "harmonic_mean\t5",
    "harmonic_mean\t-1",
    "harmonic_mean\t-",
    "harmonic_mean\t1,2\tweights=1",
    "harmonic_mean\t1,2\tweights=0,0",
    "harmonic_mean\t1,2\tweights=1,-1",
    "harmonic_mean\t0,2\tweights=0,1",
    "harmonic_mean\t0.5\tweights=2",
    "harmonic_mean\t3,nan",
    "harmonic_mean\tinf,inf",
    "median\t1,3,5",
    "median\t1,3,5,7",
    "median\t1,2.5",
    "median\t-",
    "median_low\t1,3,5,7",
    "median_high\t1,3,5,7",
    "median_low\tred,blue,green,blue",
    "median_high\t-",
    "median_grouped\t52,52,53,54",
    "median_grouped\t1,3,3,5,7",
    "median_grouped\t1,2,2,3,4,4,4,4,4,5\tinterval=2",
    "median_grouped\t25,35,35,45,45,45,55\tinterval=10",
    "median_grouped\t-",
    "mode\t1,1,2,3,3,3,3,4",
    "mode\tred,blue,blue,red,green,red,red",
    "mode\t1,1.0,2",
    "mode\t1.0,1,2",
    "mode\tnan,nan,1",
    "mode\t-",
    "multimode\ta,a,b,b,b,b,c,c,d,d,d,d,e,e,f,f,f,f,g,g",
    "multimode\t-",
    "multimode\t-0.0,0.0,1",
    "multimode\t3,1,2",
    "quantiles\t%s\tn=10" % SCORES,
    "quantiles\t%s\tn=10\tmethod=inclusive" % SCORES,
    "quantiles\t%s" % SCORES,
    "quantiles\t1,2\tn=4",
    "quantiles\t1,2\tn=4\tmethod=inclusive",
    "quantiles\t5\tn=4",
    "quantiles\t5\tn=1",
    "quantiles\t-",
    "quantiles\t1,2,3\tn=0",
    "quantiles\t1,2,3\tmethod=median",
    "quantiles\t1.5,2.5,10\tn=4",
    "quantiles\t1,2,3,4,5\tn=3\tmethod=inclusive",
    "variance\t2.75,1.75,1.25,0.25,0.5,1.25,3.5",
    "variance\t2.75,1.75,1.25,0.25,0.5,1.25,3.5\txbar=1.6071428571428572",
    "variance\t1,2,3,4",
    "variance\t1,3,5,7",
    "variance\t1",
    "variance\tnan,1,2",
    "variance\tinf,1",
    "variance\t1000000000.1,1000000000.2,1000000000.3",
    "variance\t1e-5,2e-5,4e-5",
    "pvariance\t0.0,0.25,0.25,1.25,1.5,1.75,2.75,3.25",
    "pvariance\t1,3",
    "pvariance\t1,2,3\tmu=2",
    "pvariance\t2,4\tmu=3",
    "pvariance\t1,2,4\tmu=2.5",
    "pvariance\t-",
    "stdev\t1.5,2.5,2.5,2.75,3.25,4.75",
    "stdev\t1,2,3,4",
    "stdev\t1,2,3,4\txbar=2",
    "stdev\tnan,1,2",
    "stdev\tinf,1",
    "stdev\t5",
    "stdev\t0.1,0.1,0.1",
    "pstdev\t1.5,2.5,2.5,2.75,3.25,4.75",
    "pstdev\t-",
    "pstdev\t7",
    "pstdev\t1,2,4\tmu=2.5",
    "covariance\t1,2,3,4,5,6,7,8,9\t1,2,3,1,2,3,1,2,3",
    "covariance\t1,2,3,4,5,6,7,8,9\t9,8,7,6,5,4,3,2,1",
    "covariance\t1,2,3\t1,2",
    "covariance\t1\t1",
    "covariance\t0.5,1.5,nan\t1,2,3",
    "correlation\t1,2,3,4,5,6,7,8,9\t1,2,3,4,5,6,7,8,9",
    "correlation\t1,2,3,4,5,6,7,8,9\t9,8,7,6,5,4,3,2,1",
    "correlation\t1,2,3,4,5,6,7,8,9\t1,2,3,1,2,3,1,2,3",
    "correlation\t1,2,3,4,5\t1,4,9,16,25",
    "correlation\t1,2,3,4,5\t1,4,9,16,25\tmethod=ranked",
    "correlation\t3,1,2,2,5,4\t10,20,20,30,40,30\tmethod=ranked",
    "correlation\t1,2,3\t5,5,5",
    "correlation\t1,2,3\t1,2,3\tmethod=kendall",
    "correlation\t1,2\t1",
    "correlation\t1e200,2e200,3e200\t1,2,4",
    "linear_regression\t1,2,3,4,5,6,7,8,9,10\t1,4,7,8,13,16,19,22,25,27",
    "linear_regression\t1,2,3,4,5,6,7,8,9,10\t3,5,10,12,14,18,20,25,26,29\tproportional=1",
    "linear_regression\t1,2,3\t2,4,6\tproportional=1",
    "linear_regression\t1.5,2.5,3.5\t2,4,6\tproportional=1",
    "linear_regression\t2,2,2\t1,2,3",
    "linear_regression\t0,0\t1,2\tproportional=1",
    "linear_regression\t1\t2",
    "fsum\t0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1",
    "fsum\t1e-16,1,1e16",
    "fsum\t1e100,1,-1e100,1e-100,1e50,-1,-1e50",
    "fsum\t1e308,1e308,-1e308",
    "fsum\tinf,-inf",
    "fsum\tnan,1",
    "fsum\t1,2,3",
    "fsum\t-",
    "sumprod\t1,2,3\t4,5,6",
    "sumprod\t0.1,0.2\t3,4",
    "sumprod\t1,2.5,3\t2,2,2",
    "sumprod\t1,2\t1",
    "sumprod\t1e200,1\t1e200,1",
    "sumprod\tnan,1\t1,1",
    "sumprod\t0.1,0.2,0.3\t0.1,0.2,-0.3",
    "sumprod\t-\t-",
    "hypot\t3,4",
    "hypot\t1,1,1,1",
    "hypot\t0,0",
    "hypot\t-",
    "hypot\t-3",
    "hypot\tinf,nan",
    "hypot\tnan,1",
    "hypot\t1e200,1e200",
    "hypot\t0.1,0.2,0.3",
]

NORMAL = [
    "0,1\trepr\tmean\tmedian\tmode\tstdev\tvariance",
    "0,1\tpdf:0\tpdf:1.5\tpdf:-3",
    "0,1\tinv_cdf:0.975\tinv_cdf:0.5\tinv_cdf:0.0001\tinv_cdf:0.9\tinv_cdf:1e-300\tinv_cdf:0\tinv_cdf:1",
    "0,1\tquantiles:4\tquantiles:10\tquantiles:1",
    "100,15\tzscore:130\tzscore:85.5\tinv_cdf:0.25",
    "100,15\tadd:5\tadd_nd:50,20\tsub_nd:50,20\tsub:7.5\trsub:10\tmul:-2\tdiv:4\tdiv:0\tneg",
    "100,15\teq:100,15\teq:100.0,15.0\teq:100,16",
    "1,0\tpdf:1\tzscore:2\tinv_cdf:0.5\tvariance",
    "1,-1\trepr",
    "from=2.5,3.25,5.5,11.25,11.75\trepr\tinv_cdf:0.8",
    "from=1\trepr",
    "from=1,2,nan\trepr",
    "from=1,2,inf\trepr",
    "from=4,4,4,4\trepr\tpdf:4\tzscore:4",
]

PROGRAMS = [
    "latency\tlatency.csv",
    "abtest\tab.csv",
    "capacity\tload.csv\t250",
    "capacity\tload.csv\t30",
    "survey\tsurvey.csv",
    "sensors\tsensors.csv",
    "growth\tgrowth.csv",
    "latency\tmissing.csv",
]


def main():
    if os.path.isdir(DATA):
        shutil.rmtree(DATA)
    os.makedirs(DATA)
    write("latency.csv", latency_csv())
    write("ab.csv", ab_csv())
    write("load.csv", load_csv())
    write("survey.csv", survey_csv())
    write("sensors.csv", sensors_csv())
    write("growth.csv", growth_csv())
    jobs = ["call\t" + c for c in CALLS] + ["normal\t" + n for n in NORMAL] + PROGRAMS
    write("jobs.tsv", "\n".join(jobs) + "\n")


main()
