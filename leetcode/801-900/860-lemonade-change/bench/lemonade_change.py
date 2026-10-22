# LeetCode #860: Lemonade Change -- Python mirror of the bench program (the
# ★ arm, count the fives and tens, pay a twenty with a ten when there is one).


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


seed = 860


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 100000
    bills = []
    fives = 0
    tens = 0
    for _ in range(n):
        r = next_random() % 10
        if r >= 8 and tens > 0 and fives > 0:
            bills.append(20)
            tens -= 1
            fives -= 1
        elif r >= 8 and fives >= 3:
            bills.append(20)
            fives -= 3
        elif r >= 5 and fives > 0:
            bills.append(10)
            fives -= 1
            tens += 1
        else:
            bills.append(5)
            fives += 1
    served = 0
    check = 0
    for r in range(1000):
        i = next_random() % n
        old = bills[i]
        bills[i] = 10 if old == 5 else 20 if old == 10 else 5
        yes = lemonade_change(bills)
        bills[i] = old
        if yes:
            served += 1
        check = (check * 31 + (r + 2 if yes else 1)) % 1000000007
    print(f"1000 rounds on 100000 bills: {served} served, checksum {check}")


main()
