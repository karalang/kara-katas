# LeetCode #859: Buddy Strings -- Python mirror of the ★ arm (one pass over
# the positions where the strings differ).


def buddy_strings(s, goal):
    a = s.encode()
    b = goal.encode()
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


def show(s, goal):
    print(f's = "{s}", goal = "{goal}" -> {str(buddy_strings(s, goal)).lower()}')


seed = 859


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letter(i):
    return chr(97 + i)


def random_text(n, k):
    return "".join(letter(next_random() % k) for _ in range(n))


def edited(s, k):
    cs = list(s)
    n = len(cs)
    edit = next_random() % 5
    if edit == 1:
        i = next_random() % n
        j = next_random() % n
        cs[i], cs[j] = cs[j], cs[i]
    elif edit == 2 and n >= 3:
        i = next_random() % (n - 2)
        cs[i], cs[i + 1], cs[i + 2] = cs[i + 1], cs[i + 2], cs[i]
    elif edit == 3:
        i = next_random() % n
        cs[i] = letter(next_random() % k)
    elif edit == 4:
        cs.pop()
    return "".join(cs)


def main():
    for s, goal in [("ab", "ba"), ("ab", "ab"), ("aa", "aa"), ("aaaaaaabc", "aaaaaaacb"), ("a", "a"),
                    ("a", "b"), ("abc", "ab"), ("abcd", "badc"), ("abcd", "abdc"), ("abab", "abab"),
                    ("abc", "abc"), ("abc", "acd"), ("abac", "abad"), ("ab", "ca")]:
        show(s, goal)
    words = [letter(x // 9) + letter(x // 3 % 3) + letter(x % 3) for x in range(27)]
    buddies = sum(1 for s in words for g in words if buddy_strings(s, g))
    print(f"all 729 pairs of length 3 over three letters: {buddies} are buddies")
    total = 0
    check = 0
    for r in range(2000):
        n = 1 + next_random() % 30
        k = 1 + next_random() % 26
        s = random_text(n, k)
        goal = edited(s, k)
        yes = buddy_strings(s, goal)
        if yes:
            total += 1
        check = (check * 31 + (r + 2 if yes else 1)) % 1000000007
    print(f"2000 random pairs: {total} are buddies, checksum {check}")


main()
