# LeetCode #2241: Design an ATM Machine -- the Python mirror of atm.kara:
# the counts of the five banknotes in a list, smallest first; a
# withdrawal takes as many of each banknote as fit, largest first, into
# a separate plan, and only when the plan pays the whole amount is it
# taken from the counts.


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


# ---- test harness ---------------------------------------------------------


def run(calls):
    atm = Atm()
    answers = []
    for kind, args in calls:
        if kind == 0:
            atm.deposit(args)
        else:
            answers.append(atm.withdraw(args[0]))
    return answers


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def calls_of(count, notes, top):
    calls = []
    for _ in range(count):
        if next_random() % 2 == 0:
            counts = [wide_random() % (notes + 1) for _ in range(5)]
            calls.append((0, counts))
        else:
            amount = wide_random() % top + 1
            if next_random() % 4 != 0:
                amount = (amount + 9) // 10 * 10
            calls.append((1, [amount]))
    return calls


def tally(answers, check):
    c = check
    for answer in answers:
        for n in answer:
            c = (c * 31 + n % 1000000007 + 1) % 1000000007
    return c


def show_list(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def show_calls(calls):
    return "[" + ", ".join(f"({k}, {show_list(a)})" for k, a in calls) + "]"


def main():
    global seed
    examples = [
        [(0, [0, 0, 1, 2, 1]), (1, [600]), (0, [0, 1, 0, 1, 1]), (1, [600]), (1, [550])],
        [(0, [1, 1, 1, 1, 1]), (1, [890]), (1, [20])],
        [(1, [20]), (0, [0, 0, 0, 0, 0]), (1, [10])],
        [(0, [0, 0, 0, 3, 1]), (1, [600]), (1, [700]), (1, [600])],
        [(0, [2, 1, 0, 0, 0]), (1, [60]), (1, [90]), (1, [40]), (1, [50])],
        [(0, [1000000000] * 5), (1, [1000000000]), (1, [999999990]), (1, [30])],
    ]
    for calls in examples:
        answers = run(calls)
        print(f"{show_calls(calls)} -> [" + ", ".join(show_list(a) for a in answers) + "]")
    seed = 2241
    paid = 0
    check = 0
    for _ in range(3000):
        count = next_random() % 30 + 1
        notes = next_random() % 6 + 1
        top = (next_random() % 300 + 1) * 10
        answers = run(calls_of(count, notes, top))
        paid += sum(1 for a in answers if a[0] >= 0)
        check = tally(answers, check)
    print(f"3000 small machines: {paid} withdrawals paid, checksum {check}")
    paid = 0
    check = 0
    for r in range(4):
        top = [1000000000, 1000000, 10000, 1000][r]
        answers = run(calls_of(5000, 1000000000, top))
        paid += sum(1 for a in answers if a[0] >= 0)
        check = tally(answers, check)
    print(f"4 large machines: {paid} withdrawals paid, checksum {check}")


main()
