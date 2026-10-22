# LeetCode #860: Lemonade Change -- Python mirror of the ★ arm (count the
# fives and tens, pay a twenty with a ten when there is one).


def lemonade_change(bills):
    fives = 0
    tens = 0
    for b in bills:
        if b == 5:
            fives += 1
        elif b == 10:
            if fives == 0:
                return False
            fives -= 1
            tens += 1
        elif tens > 0 and fives > 0:
            tens -= 1
            fives -= 1
        elif fives >= 3:
            fives -= 3
        else:
            return False
    return True


def show(bills):
    print(f"{bills} -> {str(lemonade_change(bills)).lower()}")


seed = 860


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_bill():
    r = next_random() % 10
    if r < 5:
        return 5
    if r < 8:
        return 10
    return 20


def main():
    for bills in [[5, 5, 5, 10, 20], [5, 5, 10, 10, 20], [5], [10], [20], [5, 10], [5, 20],
                  [5, 5, 5, 20], [5, 5, 10, 20], [5, 5, 10, 20, 5, 5, 5, 20], [5, 5, 5, 10, 20, 20],
                  [5, 5, 5, 5, 10, 20, 10, 20], [5, 10, 5, 20], [5, 5, 5, 5, 20, 20, 5, 10]]:
        show(bills)
    queues = 0
    served = 0
    total = 3
    for n in range(1, 8):
        for code in range(total):
            bills = []
            c = code
            for _ in range(n):
                bills.append([5, 10, 20][c % 3])
                c //= 3
            queues += 1
            if lemonade_change(bills):
                served += 1
        total *= 3
    print(f"all {queues} queues of one to seven bills: {served} get their change")
    yes = 0
    check = 0
    for r in range(2000):
        n = 1 + next_random() % 40
        bills = [random_bill() for _ in range(n)]
        ok = lemonade_change(bills)
        if ok:
            yes += 1
        check = (check * 31 + (r + 2 if ok else 1)) % 1000000007
    print(f"2000 random queues: {yes} get their change, checksum {check}")


main()
