# Benchmark for #464: mirror of can_i_win.kara (the star arm: search with
# a memo keyed by the bitmask of numbers used) on the same workload.
import sys

sys.setrecursionlimit(10000)


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


def main():
    games = 10
    seed = 464
    won = 0
    checksum = 0
    for game in range(games):
        seed = (seed * 1103515245 + 12345) % 2147483648
        total = 100 + (seed // 65536) % 111
        if can_i_win(20, total):
            won += 1
            checksum = (checksum * 31 + game + 1) % 1000000007
    print(f"{games} games of 1 to 20: the first player wins {won}, checksum {checksum}")


main()
