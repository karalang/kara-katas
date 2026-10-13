# Benchmark for #465: mirror of min_transfers.kara (the star arm:
# backtracking over the unsettled balances) on the same workload.


def fewest_from(debts, start):
    first = start
    while first < len(debts) and debts[first] == 0:
        first += 1
    if first == len(debts):
        return 0
    best = -1
    for j in range(first + 1, len(debts)):
        if debts[j] * debts[first] < 0:
            debts[j] += debts[first]
            count = 1 + fewest_from(debts, first + 1)
            debts[j] -= debts[first]
            if best < 0 or count < best:
                best = count
    return best


def min_transfers(transactions):
    people = 0
    for frm, to, _ in transactions:
        people = max(people, frm + 1, to + 1)
    balance = [0] * people
    for frm, to, amount in transactions:
        balance[frm] -= amount
        balance[to] += amount
    debts = [b for b in balance if b != 0]
    return fewest_from(debts, 0)


def main():
    ledgers = 20000
    seed = 465

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    total = 0
    checksum = 0
    for _ in range(ledgers):
        transactions = []
        for _ in range(8):
            frm = next_random() % 12
            to = (frm + 1 + next_random() % 11) % 12
            amount = 1 + next_random() % 3
            transactions.append((frm, to, amount))
        fewest = min_transfers(transactions)
        total += fewest
        checksum = (checksum * 31 + fewest) % 1000000007
    print(f"{ledgers} ledgers of 8 transactions: {total} transfers in all, checksum {checksum}")


main()
