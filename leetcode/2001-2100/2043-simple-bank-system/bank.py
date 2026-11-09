# LeetCode #2043: Simple Bank System -- Python mirror of the ★ arm
# (bank.kara): the balances in a list indexed by account - 1, every
# operation checked whole before anything changes.


class Bank:
    def __init__(self, balance):
        self.balance = balance

    def exists(self, account):
        return 1 <= account <= len(self.balance)

    def transfer(self, account1, account2, money):
        if not self.exists(account1) or not self.exists(account2) or self.balance[account1 - 1] < money:
            return False
        self.balance[account1 - 1] -= money
        self.balance[account2 - 1] += money
        return True

    def deposit(self, account, money):
        if not self.exists(account):
            return False
        self.balance[account - 1] += money
        return True

    def withdraw(self, account, money):
        if not self.exists(account) or self.balance[account - 1] < money:
            return False
        self.balance[account - 1] -= money
        return True


# ---- test harness ---------------------------------------------------------


def run(balance, ops):
    bank = Bank(balance)
    results = []
    for kind, a, b, money in ops:
        if kind == 0:
            results.append(bank.transfer(a, b, money))
        elif kind == 1:
            results.append(bank.deposit(a, money))
        else:
            results.append(bank.withdraw(a, money))
    return results


seed = 2043


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big_random():
    hi = next_random()
    mid = next_random()
    return (hi * 32768 + mid) * 32768 + next_random()


def problem(n, calls, top):
    balance = [big_random() % (top + 1) for _ in range(n)]
    ops = []
    for _ in range(calls):
        kind = next_random() % 3
        a = big_random() % (n + 2)
        b = big_random() % (n + 2)
        money = big_random() % (top + 1)
        ops.append((kind, a, b, money))
    return balance, ops


def tally(results, check):
    for ok in results:
        check = (check * 31 + (2 if ok else 1)) % 1000000007
    return check


def show(v):
    return "[" + ", ".join(v) + "]"


def main():
    examples = [
        ([10, 100, 20, 50, 30], [(2, 3, 0, 10), (0, 5, 1, 20), (1, 5, 0, 20), (0, 3, 4, 15), (2, 10, 0, 50)]),
        ([0], [(2, 1, 0, 0), (2, 1, 0, 1), (1, 1, 0, 1000000000000), (0, 1, 1, 1000000000000), (0, 1, 2, 1), (2, 1, 0, 1000000000000)]),
        ([5, 5], [(0, 1, 2, 5), (0, 1, 2, 1), (0, 2, 1, 10), (2, 0, 0, 0), (1, 3, 0, 1), (0, 0, 1, 0)]),
    ]
    for balance, ops in examples:
        shown = show(str(x) for x in balance) + " " + show("(" + ", ".join(str(x) for x in op) + ")" for op in ops)
        results = run(list(balance), ops)
        print(f"{shown} -> {show('true' if ok else 'false' for ok in results)}")
    succeeded = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 8 + 1
        calls = next_random() % 30 + 1
        top = next_random() % 100 + 1
        balance, ops = problem(n, calls, top)
        results = run(balance, ops)
        succeeded += sum(results)
        check = tally(results, check)
    print(f"2000 small banks: {succeeded} calls succeed, checksum {check}")
    succeeded = 0
    check = 0
    for top in [1000000000000, 1000000, 100, 1]:
        balance, ops = problem(100000, 10000, top)
        results = run(balance, ops)
        succeeded += sum(results)
        check = tally(results, check)
    print(f"4 large banks: {succeeded} calls succeed, checksum {check}")


main()
