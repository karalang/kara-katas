# LeetCode #2214: Minimum Health to Beat Game -- the mirror of
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


def random_damage(n, top):
    return [next_random() % (top + 1) for _ in range(n)]


def show(damage, armor):
    print(f"{damage} with armor {armor} -> {minimum_health(damage, armor)}")


def main():
    # LeetCode's three examples, then four more: one level, no damage at
    # all, armor beyond every level, and the largest level twice
    show([2, 7, 4, 3], 4)
    show([2, 5, 3, 4], 7)
    show([3, 3, 3], 0)
    show([5], 2)
    show([0, 0, 0], 5)
    show([1, 2, 3], 100)
    show([9, 1, 9], 6)
    # 3000 random games of 1 to 30 levels, damage up to 10, 1000 and
    # 10^5 in turn, the armor up to the same
    check = 0
    for t in range(3000):
        top = [10, 1000, 100000][t % 3]
        n = next_random() % 30 + 1
        damage = random_damage(n, top)
        armor = next_random() % (top + 1)
        check = (check * 31 + minimum_health(damage, armor)) % 1000000007
    print(f"3000 games: checksum {check}")
    # the constraints' largest: 10^5 levels of 10^5 damage with all the
    # armor, then 10^5 random levels with none
    heavy = [100000] * 100000
    random = random_damage(100000, 100000)
    print(f"10^5 at 10^5 -> {minimum_health(heavy, 100000)}, 10^5 random -> {minimum_health(random, 0)}")


main()
