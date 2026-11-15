# LeetCode #1169: Invalid Transactions -- the ★ arm's bench in Python: each
# transaction split into its fields, the places of each name's
# transactions gathered in a dict, and every transaction compared with the
# others of its name.


def invalid_transactions(transactions):
    txns = []
    by_name = {}
    for i, t in enumerate(transactions):
        name, time, amount, city = t.split(',')
        txns.append((name, int(time), int(amount), city))
        by_name.setdefault(name, []).append(i)
    out = []
    for i, (name, time, amount, city) in enumerate(txns):
        bad = amount > 1000 or any(
            abs(txns[j][1] - time) <= 60 and txns[j][3] != city for j in by_name[name]
        )
        if bad:
            out.append(transactions[i])
    return out


seed = 1169


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def line():
    name = next_random() % 200
    time = next_random() % 1001
    amount = next_random() % 1101
    city = next_random() % 2
    return f"n{name},{time},{amount},c{city}"


def main():
    lists = [[line() for _ in range(1000)] for _ in range(16)]
    total = 0
    check = 0
    for _ in range(300):
        for k in range(16):
            at = next_random() % 1000
            lists[k][at] = line()
            bad = invalid_transactions(lists[k])
            total += len(bad)
            for b in bad:
                check = (check * 31 + len(b)) % 1000000007
    print(f"300 rounds over 16 lists of 1000 transactions: {total} invalid, checksum {check}")


main()
