# LeetCode #2335: Minimum Amount of Time to Fill Cups -- the bench, the ★
# arm in Python: the larger of the most cups of one kind and half of all
# the cups, rounded up.


def fill_cups(amount):
    most = max(amount[0], amount[1], amount[2])
    total = amount[0] + amount[1] + amount[2]
    return max(most, (total + 1) // 2)


def main():
    amount = [0, 0, 0]
    check = 0
    for p in range(3):
        for a in range(101):
            for b in range(101):
                for c in range(101):
                    amount[0] = a
                    amount[1] = b
                    amount[2] = c
                    check = (check * 31 + fill_cups(amount) + p) % 1000000007
    print(f"3 passes over 101^3 amounts: checksum {check}")


main()
