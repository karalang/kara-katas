# LeetCode #2043: Simple Bank System -- the ★ arm in Python, the same
# algorithm and workload as bank.kara: the balances in a list indexed by
# account - 1, every call checked whole before anything changes.


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


seed = 2043


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big_random():
    hi = next_random()
    mid = next_random()
    return (hi * 32768 + mid) * 32768 + next_random()


def main():
    n, calls_per, top = 100000, 1000000, 1000000
    balance = [big_random() % (top + 1) for _ in range(n)]
    ops = []
    for _ in range(calls_per):
        kind = next_random() % 3
        a = big_random() % (n + 2)
        b = big_random() % (n + 2)
        ops.append((kind, a, b, big_random() % (top + 1)))
    calls = succeeded = check = 0
    for rnd in range(40):
        bank = Bank(list(balance))
        for kind, a, b, money in ops:
            if kind == 0:
                ok = bank.transfer(a, b, money)
            elif kind == 1:
                ok = bank.deposit(a, money)
            else:
                ok = bank.withdraw(a, money)
            calls += 1
            if ok:
                succeeded += 1
                check = (check * 31 + calls + rnd) % 1000000007
    print(f"{calls} calls: {succeeded} succeed, checksum {check}")


main()
