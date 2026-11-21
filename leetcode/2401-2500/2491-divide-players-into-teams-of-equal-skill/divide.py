# LeetCode #2491: Divide Players Into Teams of Equal Skill -- Python mirror
# of the ★ arm (divide.kara): sorted, paired from both ends, every pair
# asked for the same sum, and the products added up.


def divide_players(skill):
    s = sorted(skill)
    n = len(s)
    target = s[0] + s[n - 1]
    chemistry = 0
    for i in range(n // 2):
        a, b = s[i], s[n - 1 - i]
        if a + b != target:
            return -1
        chemistry += a * b
    return chemistry


# ---- test harness -----------------------------------------------------------

seed = 2491


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_skills(teams, top, spoil):
    total = next_random() % (2 * top - 1) + 2
    low = total - top if total - top > 1 else 1
    high = total - 1 if total - 1 < top else top
    skill = []
    for _ in range(teams):
        a = low + next_random() % (high - low + 1)
        skill.append(a)
        skill.append(total - a)
    for i in range(len(skill) - 1, 0, -1):
        j = next_random() % (i + 1)
        skill[i], skill[j] = skill[j], skill[i]
    if spoil:
        at = next_random() % len(skill)
        skill[at] = skill[at] - 1 if skill[at] > 1 else 2
    return skill


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    cases = [
        [3, 2, 5, 1, 3, 4],
        [3, 4],
        [1, 1, 2, 3],
        [1, 1],
        [5, 5, 5, 5],
        [1, 2, 3, 5],
        [2, 2, 1, 3],
        [1000, 1, 999, 2, 500, 501],
        [4, 4, 2, 6, 3, 5],
    ]
    for skill in cases:
        print(f"{show(skill)} -> {divide_players(skill)}")
    for top in [1000, 5]:
        divided = 0
        check = 0
        for t in range(2000):
            teams = next_random() % 100 + 1
            skill = random_skills(teams, top, t % 2 == 1)
            answer = divide_players(skill)
            if answer >= 0:
                divided += 1
            check = (check * 31 + answer + 1) % 1000000007
        print(f"2000 random to {top}: {divided} divide, checksum {check}")
    every = [1000] * 100000
    paired = [i // 2 % 1000 + 1 if i % 2 == 0 else 1000 - i // 2 % 1000 for i in range(100000)]
    random = random_skills(50000, 1000, False)
    spoiled = random_skills(50000, 1000, True)
    for name, skill in [("all 1000", every), ("paired", paired), ("random", random), ("spoiled", spoiled)]:
        print(f"10^5 {name} -> {divide_players(skill)}")


main()
