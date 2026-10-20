# LeetCode 811 — Subdomain Visit Count, a map from domain to visits (mirror of the ★ arm).


def subdomain_visits(cpdomains):
    counts = {}
    for entry in cpdomains:
        space = entry.find(" ")
        n = int(entry[:space])
        domain = entry[space + 1:]
        while True:
            counts[domain] = counts.get(domain, 0) + n
            dot = domain.find(".")
            if dot < 0:
                break
            domain = domain[dot + 1:]
    return [f"{total} {domain}" for domain, total in counts.items()]


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def sorted_visits(cpdomains):
    return sorted(subdomain_visits(cpdomains))


def show(cpdomains):
    print(f"cpdomains = [{', '.join(cpdomains)}] -> [{', '.join(sorted_visits(cpdomains))}]")


def summary(lines):
    check = 0
    for line in lines:
        n = int(line[:line.find(" ")])
        check = (check * 131 + n + len(line)) % 1000000007
    return len(lines), check


def random_domain(width):
    tops = ["com", "org", "net", "io"]
    middles = ["leetcode", "google", "yahoo", "wiki", "kara"]
    lefts = ["mail", "discuss", "www", "api", "m", "docs"]
    top = tops[next_random() % min(width, 4)]
    middle = middles[next_random() % min(width, 5)]
    if next_random() % 3 == 0:
        return f"{middle}.{top}"
    return f"{lefts[next_random() % min(width, 6)]}.{middle}.{top}"


def main():
    global seed
    show(["9001 discuss.leetcode.com"])
    show(["900 google.mail.com", "50 yahoo.com", "1 intel.mail.com", "5 wiki.org"])
    show(["1 a.b.c", "2 b.c", "3 d.c"])
    show(["10000 x.y", "10000 x.y"])
    show(["7 a.com", "3 b.com"])
    show(["1 a.com", "1 com.a"])
    seed = 811
    big = []
    for i in range(100):
        n = 1 + (i * 7919 + 13) % 10000
        big.append(f"{n} {random_domain(6)}")
    lines, check = summary(sorted_visits(big))
    print(f"100 entries -> {lines} domains, checksum {check}")
    total = 0
    allc = 0
    for r in range(300):
        entries = []
        for _ in range(1 + next_random() % 10):
            n = 1 + next_random() % 50
            entries.append(f"{n} {random_domain(3)}")
        lines, check = summary(sorted_visits(entries))
        total += lines
        allc = (allc * 131 + check + r) % 1000000007
    print(f"300 random rounds of 1 to 10 entries: {total} domains, checksum {allc}")


main()
