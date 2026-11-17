# LeetCode #2241: Design an ATM Machine -- the benchmark's Python mirror
# of atm.kara: the counts of the five banknotes, smallest first; a
# withdrawal plans as many of each as fit, largest first, and takes the
# plan only when it pays the whole amount.


class Atm:
    def __init__(self):
        self.counts = [0] * 5

    def deposit(self, banknotes_count):
        for i in range(5):
            self.counts[i] += banknotes_count[i]

    def withdraw(self, amount):
        values = [20, 50, 100, 200, 500]
        plan = [0] * 5
        left = amount
        for i in reversed(range(5)):
            plan[i] = min(left // values[i], self.counts[i])
            left -= plan[i] * values[i]
        if left != 0:
            return [-1]
        for i in range(5):
            self.counts[i] -= plan[i]
        return plan


seed = 2241


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def main():
    paid = 0
    check = 0
    counts = [0] * 5
    for _ in range(200):
        atm = Atm()
        for _ in range(5000):
            if next_random() % 2 == 0:
                for i in range(5):
                    counts[i] = wide_random() % 1000000001
                atm.deposit(counts)
            else:
                amount = (wide_random() % 100000000 + 1) * 10
                answer = atm.withdraw(amount)
                if answer[0] >= 0:
                    paid += 1
                for n in answer:
                    check = (check * 31 + n % 1000000007 + 1) % 1000000007
    print(f"200 machines of 5000 calls: {paid} withdrawals paid, checksum {check}")


main()
