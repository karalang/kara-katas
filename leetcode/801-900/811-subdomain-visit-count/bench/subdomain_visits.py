# LeetCode 811 -- Subdomain Visit Count: the bench, with the ★ arm's map
# from domain to visits.

seed = 811


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


TOPS = ["com", "org", "net", "io"]
MIDDLES = ["leetcode", "google", "yahoo", "wiki", "kara"]
LEFTS = ["mail", "discuss", "www", "api", "m", "docs"]


def random_domain():
    top = TOPS[next_random() % 4]
    middle = MIDDLES[next_random() % 5]
    if next_random() % 3 == 0:
        return f"{middle}.{top}"
    return f"{LEFTS[next_random() % 6]}.{middle}.{top}"


# 64 lists of 100 entries are made once. Each round writes a new count into
# one entry of the next list and counts that list's visits; the answer's
# lines, in whatever order they come, are folded into a sum.
def main():
    lists = []
    domains = []
    for _ in range(64):
        lst = []
        doms = []
        for _ in range(100):
            d = random_domain()
            lst.append(f"{1 + next_random() % 10000} {d}")
            doms.append(d)
        lists.append(lst)
        domains.append(doms)
    rounds = 100000
    lines = 0
    check = 0
    for r in range(rounds):
        k = r % 64
        i = r // 64 % 100
        lists[k][i] = f"{1 + next_random() % 10000} {domains[k][i]}"
        out = subdomain_visits(lists[k])
        s = 0
        for line in out:
            space = line.find(" ")
            s += int(line[:space]) * 7 + len(line)
        lines += len(out)
        check = (check * 131 + s) % 1000000007
    print(f"{rounds} rounds of 100 entries: {lines} lines, checksum {check}")


main()
