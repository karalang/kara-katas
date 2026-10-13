# LeetCode #464: Can I Win -- mirror of can_i_win.kara (the star arm:
# search with a memo keyed by the bitmask of numbers used).


def wins_from(used, left, m, memo):
    if used in memo:
        return memo[used]
    result = False
    for n in range(1, m + 1):
        bit = 1 << (n - 1)
        if used & bit == 0 and (n >= left or not wins_from(used | bit, left - n, m, memo)):
            result = True
            break
    memo[used] = result
    return result


def can_i_win(max_choosable, desired_total):
    if desired_total <= 0:
        return True
    if max_choosable * (max_choosable + 1) // 2 < desired_total:
        return False
    return wins_from(0, desired_total, max_choosable, {})


# ---- test harness ---------------------------------------------------------


def show(max_choosable, desired_total):
    wins = "true" if can_i_win(max_choosable, desired_total) else "false"
    print(f"max_choosable {max_choosable}, desired_total {desired_total} -> {wins}")


seed = 464


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show(10, 11)
    show(10, 0)
    show(10, 1)
    show(1, 1)
    show(1, 2)
    show(2, 3)
    show(3, 4)
    show(4, 6)
    show(5, 15)
    show(6, 21)
    show(10, 40)
    show(12, 50)
    show(12, 79)
    count = 300
    won = 0
    checksum = 0
    for case in range(count):
        m = 1 + next_random() % 12
        total = next_random() % (m * (m + 1) // 2 + 6)
        if can_i_win(m, total):
            won += 1
            checksum = (checksum * 31 + case + 1) % 1000000007
    print(f"{count} random games: the first player wins {won}, checksum {checksum}")


main()
