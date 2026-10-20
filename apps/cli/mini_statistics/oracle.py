# Runs data/jobs.tsv through Python's own statistics and math modules
# (3.13) and prints what each job gives; expected.out is this output.
import math
import os
import sys
from statistics import (NormalDist, StatisticsError, correlation, covariance, fmean,
                        geometric_mean, harmonic_mean, linear_regression, mean, median,
                        median_grouped, median_high, median_low, mode, multimode, pstdev,
                        pvariance, quantiles, stdev, variance)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
os.chdir(os.path.join(HERE, "data"))


def err(e):
    return "error: %s: %s" % (type(e).__name__, e)


def token(t):
    try:
        return int(t)
    except ValueError:
        pass
    try:
        return float(t)
    except ValueError:
        return t


def values(field):
    if field == "-":
        return []
    return [token(t) for t in field.split(",")]


def show(v):
    if type(v).__name__ == "LinearRegression":
        return "LinearRegression(slope=%r, intercept=%r)" % (v.slope, v.intercept)
    return repr(v)


# --- the functions, called one by one

def call(job):
    name = job[0]
    args = []
    kw = {}
    for field in job[1:]:
        key, eq, val = field.partition("=")
        if eq and key in ("weights", "interval", "n", "method", "xbar", "mu", "proportional"):
            if key == "weights":
                kw[key] = values(val)
            elif key == "method":
                kw[key] = val
            elif key == "proportional":
                kw[key] = val == "1"
            else:
                kw[key] = token(val)
        else:
            args.append(values(field))
    fn = {"mean": mean, "fmean": fmean, "geometric_mean": geometric_mean,
          "harmonic_mean": harmonic_mean, "median": median, "median_low": median_low,
          "median_high": median_high, "median_grouped": median_grouped, "mode": mode,
          "multimode": multimode, "quantiles": quantiles, "variance": variance,
          "pvariance": pvariance, "stdev": stdev, "pstdev": pstdev, "covariance": covariance,
          "correlation": correlation, "linear_regression": linear_regression,
          "fsum": math.fsum, "sumprod": math.sumprod}
    try:
        if name == "hypot":
            return show(math.hypot(*args[0]))
        if name in ("variance", "stdev") and "xbar" in kw:
            return show(fn[name](args[0], kw["xbar"]))
        if name in ("pvariance", "pstdev") and "mu" in kw:
            return show(fn[name](args[0], kw["mu"]))
        if name == "median_grouped" and "interval" in kw:
            return show(fn[name](args[0], kw["interval"]))
        return show(fn[name](*args, **kw))
    except Exception as e:
        return err(e)


def normal_op(d, op):
    name, _, arg = op.partition(":")
    if name == "repr":
        return repr(d)
    if name in ("mean", "median", "mode", "stdev", "variance"):
        return repr(getattr(d, name))
    if name == "pdf":
        return repr(d.pdf(token(arg)))
    if name == "inv_cdf":
        return repr(d.inv_cdf(token(arg)))
    if name == "quantiles":
        return repr(d.quantiles(token(arg)))
    if name == "zscore":
        return repr(d.zscore(token(arg)))
    if name.endswith("_nd") or name == "eq":
        mu, sigma = values(arg)
        other = NormalDist(mu, sigma)
        if name == "add_nd":
            return repr(d + other)
        if name == "sub_nd":
            return repr(d - other)
        return repr(d == other)
    c = token(arg)
    if name == "add":
        return repr(d + c)
    if name == "sub":
        return repr(d - c)
    if name == "rsub":
        return repr(c - d)
    if name == "mul":
        return repr(d * c)
    if name == "div":
        return repr(d / c)
    return repr(-d)


def normal(job):
    try:
        if job[0].startswith("from="):
            d = NormalDist.from_samples(values(job[0][5:]))
        else:
            mu, sigma = values(job[0])
            d = NormalDist(mu, sigma)
    except Exception as e:
        print("  " + err(e))
        return
    for op in job[1:]:
        try:
            print("  %s: %s" % (op, normal_op(d, op)))
        except Exception as e:
            print("  %s: %s" % (op, err(e)))


# --- programs

def read_csv(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    rows = []
    for i, line in enumerate(lines[1:], start=2):
        if line:
            rows.append((i, line.split(",")))
    return rows


def number(text):
    t = token(text)
    return None if isinstance(t, str) else t


def smallest(xs):
    best = xs[0]
    for x in xs[1:]:
        if x < best:
            best = x
    return best


def largest(xs):
    best = xs[0]
    for x in xs[1:]:
        if x > best:
            best = x
    return best


def latency(path):
    groups = {}
    for lineno, row in read_csv(path):
        v = number(row[1])
        if v is None:
            print("line %d: %s has no number (%r)" % (lineno, row[0], row[1]))
            continue
        groups.setdefault(row[0], []).append(v)
    every = []
    for ep, xs in groups.items():
        every.extend(xs)
        print("%s: %d requests" % (ep, len(xs)))
        print("  mean %r, median %r, fastest %r, slowest %r" % (mean(xs), median(xs), smallest(xs),
                                                               largest(xs)))
        if len(xs) < 2:
            print("  too few requests for a spread")
            continue
        q = quantiles(xs, n=20)
        print("  p50 %r, p90 %r, p95 %r" % (q[9], q[17], q[18]))
        nd = NormalDist.from_samples(xs)
        print("  stdev %r, normal fit %r" % (stdev(xs), nd))
        out = [x for x in xs if abs(nd.zscore(x)) > 2.5]
        print("  outliers: %s" % (", ".join(repr(x) for x in out) or "none"))
    print("overall: %d requests, fmean %r, median_high %r, p99 %r" % (
        len(every), fmean(every), median_high(every), quantiles(every, n=100, method="inclusive")[98]))


def abtest(path):
    groups = {}
    for _, row in read_csv(path):
        groups.setdefault(row[1], []).append(number(row[2]))
    for v in sorted(groups):
        xs = groups[v]
        paid = len([x for x in xs if x])
        print("%s: %d visitors, %d paid (%d per mille), mean %r, median %r, stdev %r" % (
            v, len(xs), paid, paid * 1000 // len(xs), mean(xs), median(xs), stdev(xs)))
        print("  quartiles %r" % quantiles(xs))
    a, b = groups["A"], groups["B"]
    ma, mb = mean(a), mean(b)
    va, vb = variance(a) / len(a), variance(b) / len(b)
    se = math.sqrt(va + vb)
    diff = mb - ma
    z = NormalDist().inv_cdf(0.975)
    lo, hi = diff - z * se, diff + z * se
    df = (va + vb) * (va + vb) / (va * va / (len(a) - 1) + vb * vb / (len(b) - 1))
    print("B - A: %r, standard error %r, Welch t %r with %r degrees of freedom" % (diff, se, diff / se,
                                                                                    df))
    print("95%% interval (z %r): %r to %r" % (z, lo, hi))
    if lo > 0:
        print("verdict: B earns more")
    elif hi < 0:
        print("verdict: A earns more")
    else:
        print("verdict: no clear winner yet")
    paying = [x for x in a + b if x]
    fit = NormalDist.from_samples(paying)
    print("paying visitors: %r, quartiles %r" % (fit, fit.quantiles()))


def capacity(path, slo):
    xs, ys = [], []
    for _, row in read_csv(path):
        xs.append(number(row[0]))
        ys.append(number(row[1]))
    print("%d load steps, %d to %d rps" % (len(xs), xs[0], xs[-1]))
    print("covariance %r" % covariance(xs, ys))
    print("correlation %r, ranked %r" % (correlation(xs, ys), correlation(xs, ys, method="ranked")))
    fit = linear_regression(xs, ys)
    print("fit: p99 = %r * rps + %r" % (fit.slope, fit.intercept))
    cap = (slo - fit.intercept) / fit.slope
    if cap > 0:
        print("capacity at %d ms: %r rps" % (slo, cap))
    else:
        print("an SLO of %d ms is below the fit's floor of %r ms" % (slo, fit.intercept))
    prop = linear_regression(xs, ys, proportional=True)
    print("through the origin: %r ms per rps, capacity %r rps" % (prop.slope, slo / prop.slope))
    res = [y - (fit.slope * x + fit.intercept) for x, y in zip(xs, ys)]
    s = stdev(res)
    worst = 0
    for i in range(len(res)):
        if res[i] > res[worst]:
            worst = i
    print("residuals: mean %r, stdev %r, worst %r at %d rps" % (fmean(res), s, res[worst], xs[worst]))
    knee = [x for x, r in zip(xs, res) if r > 2 * s]
    print("off the line from: %s" % (", ".join("%d" % x for x in knee) or "nowhere"))


def survey(path):
    rows = read_csv(path)
    ages = [number(r[2 - 1]) for _, r in rows]
    colors = [r[2] for _, r in rows]
    km = [number(r[3]) for _, r in rows]
    kmh = [number(r[4]) for _, r in rows]
    raises = [number(r[5]) for _, r in rows]
    mids = [a // 10 * 10 + 5 for a in ages]
    print("respondents: %d" % len(rows))
    print("age: mean %r, median %r, by decade %r, quartiles %r" % (
        mean(ages), median(ages), median_grouped(mids, 10), quantiles(ages, method="inclusive")))
    print("decade mode %r, low %r, high %r" % (mode(mids), median_low(mids), median_high(mids)))
    print("favourite colour: %r, all modes %r" % (mode(colors), multimode(colors)))
    print("colours in the middle: %r and %r" % (median_low(colors), median_high(colors)))
    print("commute: mean %r km, median %r km, quartiles %r" % (fmean(km), median(km), quantiles(km)))
    print("average speed %r km/h by distance, %r per commuter, %r arithmetic" % (
        harmonic_mean(kmh, weights=km), harmonic_mean(kmh), fmean(kmh, weights=km)))
    factors = [1 + r / 100 for r in raises]
    g = geometric_mean(factors)
    print("raises: mean %r%%, typical %r%% (geometric mean %r)" % (mean(raises), (g - 1) * 100, g))
    print("raises: stdev %r, pstdev %r, variance %r" % (stdev(raises), pstdev(raises),
                                                       variance(raises)))
    print("age against commute: correlation %r, ranked %r" % (correlation(ages, km),
                                                              correlation(ages, km, method="ranked")))


def sensors(path):
    groups = {}
    bad = 0
    for lineno, row in read_csv(path):
        try:
            v = float(row[1])
        except ValueError:
            print("line %d: %s sent %r" % (lineno, row[0], row[1]))
            bad += 1
            continue
        groups.setdefault(row[0], []).append(v)
    for s, xs in groups.items():
        print("%s: %d readings" % (s, len(xs)))
        for name, fn in (("mean", mean), ("fmean", fmean), ("variance", variance), ("stdev", stdev),
                         ("pvariance", pvariance), ("pstdev", pstdev),
                         ("geometric_mean", geometric_mean), ("harmonic_mean", harmonic_mean),
                         ("from_samples", NormalDist.from_samples)):
            try:
                print("  %s %r" % (name, fn(xs)))
            except Exception as e:
                print("  %s %s" % (name, err(e)))
    print("%d bad readings" % bad)


def growth(path):
    rows = read_csv(path)
    months = [r[0] for _, r in rows]
    revs = [number(r[1]) for _, r in rows]
    ratios = [revs[i] / revs[i - 1] for i in range(1, len(revs))]
    g = geometric_mean(ratios)
    print("%d months, %s to %s" % (len(revs), months[0], months[-1]))
    print("revenue: mean %r, median %r, quartiles %r" % (mean(revs), median(revs),
                                                        quantiles(revs, method="inclusive")))
    print("monthly growth: geometric %r, arithmetic %r" % (g, fmean(ratios)))
    best = worst = 0
    for i in range(len(ratios)):
        if ratios[i] > ratios[best]:
            best = i
        if ratios[i] < ratios[worst]:
            worst = i
    print("best month %s (%r), worst %s (%r)" % (months[best + 1], ratios[best], months[worst + 1],
                                                 ratios[worst]))
    print("year one fmean %r, year two fmean %r" % (fmean(revs[:12]), fmean(revs[12:])))
    nd = NormalDist.from_samples(ratios)
    print("growth fit %r, 90%% band %r to %r" % (nd, nd.inv_cdf(0.05), nd.inv_cdf(0.95)))
    print("next month forecast %r" % (revs[-1] * g))
    print("growth deciles %r" % quantiles(ratios, n=10))


def main():
    with open("jobs.tsv", encoding="utf-8") as f:
        jobs = f.read().split("\n")[:-1]
    for line in jobs:
        job = line.split("\t")
        print("== " + " ".join(job))
        kind, a = job[0], job[1:]
        try:
            if kind == "call":
                print("  " + call(a))
            elif kind == "normal":
                normal(a)
            elif kind == "latency":
                latency(a[0])
            elif kind == "abtest":
                abtest(a[0])
            elif kind == "capacity":
                capacity(a[0], int(a[1]))
            elif kind == "survey":
                survey(a[0])
            elif kind == "sensors":
                sensors(a[0])
            elif kind == "growth":
                growth(a[0])
        except Exception as e:
            print(err(e))


main()
