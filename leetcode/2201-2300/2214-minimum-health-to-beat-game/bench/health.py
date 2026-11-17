# LeetCode #2214: Minimum Health to Beat Game -- bench mirror of
# health.kara: the damage summed in one pass with its largest, then the
# sum less what the armor saves on the largest, plus 1.


def minimum_health(damage, armor):
    total = 0
    worst = 0
    for d in damage:
        total += d
        worst = max(worst, d)
    return total - min(worst, armor) + 1


seed = 2214


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    games = []
    for g in range(100):
        # 10^5 levels, the damage up to 10, 1000 and 10^5 in turn
        top = [10, 1000, 100000][g % 3]
        games.append([next_random() % (top + 1) for _ in range(100000)])
    check = 0
    for damage in games:
        for a in range(20):
            # punch: one level hurts a little more before each answer
            damage[a * 4999] += 1
            check = (check * 31 + minimum_health(damage, a * 5000)) % 1000000007
    print(f"100 games of 10^5, 20 armors: checksum {check}")


main()
