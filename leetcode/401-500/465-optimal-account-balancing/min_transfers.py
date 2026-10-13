# LeetCode #465: Optimal Account Balancing -- mirror of min_transfers.kara
# (the star arm: backtracking over the unsettled balances).


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


# ---- test harness ---------------------------------------------------------


def listed(transactions):
    return " ".join(f"{frm}->{to}:{amount}" for frm, to, amount in transactions)


def show(transactions):
    print(f"{listed(transactions)} -> {min_transfers(transactions)}")


seed = 465


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show([(0, 1, 10), (2, 0, 5)])
    show([(0, 1, 10), (1, 0, 1), (1, 2, 5), (2, 0, 5)])
    show([(0, 1, 5)])
    show([(0, 1, 5), (1, 0, 5)])
    show([(0, 1, 5), (1, 2, 5), (2, 3, 5)])
    show([(0, 1, 3), (2, 3, 3), (4, 5, 3)])
    show([(0, 1, 1), (0, 2, 2), (0, 3, 3), (4, 0, 6)])
    show([(0, 1, 2), (2, 3, 3), (4, 5, 5), (1, 3, 1), (5, 0, 4)])
    show([(0, 1, 100), (2, 3, 1), (4, 5, 1), (6, 7, 1), (8, 9, 1), (10, 11, 1), (11, 0, 100)])
    count = 300
    total = 0
    checksum = 0
    for _ in range(count):
        n = 1 + next_random() % 8
        size = [3, 10, 100][next_random() % 3]
        transactions = []
        for _ in range(n):
            frm = next_random() % 12
            to = (frm + 1 + next_random() % 11) % 12
            amount = 1 + next_random() % size
            transactions.append((frm, to, amount))
        fewest = min_transfers(transactions)
        total += fewest
        checksum = (checksum * 31 + fewest) % 1000000007
    print(f"{count} random ledgers: {total} transfers in all, checksum {checksum}")


main()
