# LeetCode #859: Buddy Strings -- Python mirror of the bench program (the ★
# arm, one pass over the positions where the strings differ).


def buddy_strings(a, b):
    if len(a) != len(b):
        return False
    first = -1
    second = -1
    for i in range(len(a)):
        if a[i] != b[i]:
            if first < 0:
                first = i
            elif second < 0:
                second = i
            else:
                return False
    if first < 0:
        seen = [False] * 26
        for c in a:
            k = c - 97
            if seen[k]:
                return True
            seen[k] = True
        return False
    return second >= 0 and a[first] == b[second] and a[second] == b[first]


seed = 859


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 20000
    s = bytearray(97 + next_random() % 26 for _ in range(n))
    goal = bytearray(s)
    buddies = 0
    check = 0
    for r in range(40000):
        i = next_random() % n
        j = next_random() % n
        kind = r % 3
        old = goal[i]
        if kind == 1:
            goal[i] = 97 + (old - 97 + 1 + next_random() % 25) % 26
        else:
            goal[i], goal[j] = goal[j], goal[i]
        k = next_random() % n
        l = next_random() % n
        if kind == 2:
            goal[k], goal[l] = goal[l], goal[k]
        yes = buddy_strings(s, goal)
        if kind == 2:
            goal[k], goal[l] = goal[l], goal[k]
        if kind == 1:
            goal[i] = old
        else:
            goal[i], goal[j] = goal[j], goal[i]
        if yes:
            buddies += 1
        check = (check * 31 + (r + 2 if yes else 1)) % 1000000007
    print(f"40000 rounds on 20000 letters: {buddies} buddies, checksum {check}")


main()
