# LeetCode #2491: Divide Players Into Teams of Equal Skill -- Python mirror
# of the ★ arm's benchmark (divide.kara): the same 20 lists and 25 passes,
# each skill set, asked and put back.


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


seed = 2491


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 100000
    passes = 25
    lists = []
    for l in range(20):
        total = 500 + l * 50
        skill = []
        for _ in range(n // 2):
            a = next_random() % (total - 1) + 1
            skill.append(a)
            skill.append(total - a)
        for i in range(n - 1, 0, -1):
            j = (next_random() * 32768 + next_random()) % (i + 1)
            skill[i], skill[j] = skill[j], skill[i]
        lists.append(skill)
    check = 0
    for p in range(passes):
        for l in range(20):
            at = check % n
            was = lists[l][at]
            lists[l][at] = (check // n + p) % 1000 + 1
            check = (check * 31 + divide_players(lists[l]) + 1 + p) % 1000000007
            lists[l][at] = was
    print(f"{passes} passes over 20 lists of 10^5: checksum {check}")


main()
