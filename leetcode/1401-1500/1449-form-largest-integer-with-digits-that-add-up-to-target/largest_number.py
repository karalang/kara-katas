# LeetCode #1449 Form Largest Integer With Digits That Add up to Target: a
# mirror of largest_number.kara.


def largest_number(cost, target):
    # the most digits each cost from 0 to target buys exactly, -1 when it
    # buys none; then the digits taken from 9 down, each while what is left
    # still buys one digit fewer
    most = [-1] * (target + 1)
    most[0] = 0
    for t in range(1, target + 1):
        for c in cost:
            if c <= t and most[t - c] >= 0:
                most[t] = max(most[t], most[t - c] + 1)
    if most[target] < 0:
        return "0"
    digits = []
    left = target
    for d in range(8, -1, -1):
        c = cost[d]
        while c <= left and most[left - c] == most[left] - 1:
            digits.append(chr(ord("1") + d))
            left -= c
    return "".join(digits)


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def costs(top):
    return [1 + next_random() % top for _ in range(9)]


def fold(s, check):
    for b in s.encode():
        check = (check * 131 + b) % 1000000007
    return (check * 131 + 32) % 1000000007


def main():
    global seed
    firsts = [
        largest_number([4, 3, 2, 5, 6, 7, 2, 5, 5], 9),
        largest_number([7, 6, 5, 5, 5, 6, 8, 7, 8], 12),
        largest_number([2, 4, 6, 2, 4, 6, 4, 4, 4], 5),
        largest_number([6, 10, 15, 40, 40, 40, 40, 40, 40], 47),
        largest_number([1] * 9, 5),
        largest_number([5000] * 9, 5000),
        largest_number([1] + [5000] * 8, 7),
    ]
    print(" ".join(firsts))
    seed = 1449
    all_one = largest_number([1] * 9, 5000)
    drawn = largest_number(costs(50), 5000)
    check = fold(drawn, fold(all_one, 0))
    print(f"target 5000: {len(all_one)} and {len(drawn)} digits, checksum {check}")
    total = 0
    check = 0
    for _ in range(2000):
        wide = next_random() % 3 == 0
        top = 1 + next_random() % 5000 if wide else 1 + next_random() % 30
        cost = costs(top)
        target = 1 + next_random() % 200
        got = largest_number(cost, target)
        total += len(got)
        check = fold(got, check)
    print(f"2000 random cases: {total} digits, checksum {check}")


main()
