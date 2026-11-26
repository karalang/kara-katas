# LeetCode #1449 Form Largest Integer With Digits That Add up to Target: the
# bench, a mirror of largest_number.kara.


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


def main():
    # 5000 cases with the constraints' most target, 5000, each with nine
    # costs drawn from 1 to 50, each answer's digits folded to a checksum
    seed = 1449
    check = 0
    for _ in range(5000):
        cost = []
        for _ in range(9):
            seed = (seed * 1103515245 + 12345) % 2147483648
            cost.append(1 + seed // 65536 % 50)
        for b in largest_number(cost, 5000).encode():
            check = (check * 131 + b) % 1000000007
    print(f"5000 targets of 5000: checksum {check}")


main()
