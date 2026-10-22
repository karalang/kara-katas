# LeetCode #854: K-Similar Strings -- Python mirror of the ★ arm and its
# harness.


def k_similarity(s1, s2):
    goal = s2.encode()
    n = len(goal)
    seen = {s1}
    level = [bytearray(s1.encode())]
    swaps = 0
    while True:
        nxt = []
        for cur in level:
            i = 0
            while i < n and cur[i] == goal[i]:
                i += 1
            if i == n:
                return swaps
            for j in range(i + 1, n):
                if cur[j] == goal[i] and cur[j] != goal[j]:
                    moved = bytearray(cur)
                    moved[i], moved[j] = moved[j], moved[i]
                    key = moved.decode()
                    if key not in seen:
                        seen.add(key)
                        nxt.append(moved)
        level = nxt
        swaps += 1


def show(s1, s2):
    print(f'"{s1}", "{s2}" -> {k_similarity(s1, s2)}')


seed = 854


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_pair(n, letters):
    a = [ord("a") + next_random() % letters for _ in range(n)]
    b = list(a)
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        b[i], b[j] = b[j], b[i]
    return bytes(a).decode(), bytes(b).decode()


def main():
    show("ab", "ba")
    show("abc", "bca")
    show("a", "a")
    show("abcdef", "abcdef")
    show("abcdef", "fabcde")
    show("aaabbb", "bbbaaa")
    show("abab", "baba")
    show("abcabc", "cbacba")
    show("abccaacceecdeea", "bcaacceeccdeaae")
    show("abcdefabcdefabcdefab", "badcfebadcfebadcfeba")
    show("abcdefabcdefabcdefab", "bcdefabcdefabcdefaba")
    long_total = 0
    for _ in range(12):
        a, b = random_pair(20, 6)
        long_total += k_similarity(a, b)
    print(f"12 random pairs of 20 letters: swaps sum to {long_total}")
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 12
        letters = 1 + next_random() % 6
        a, b = random_pair(n, letters)
        k = k_similarity(a, b)
        total += k
        check = (check * 31 + k) % 1000000007
    print(f"300 random pairs: swaps sum to {total}, checksum {check}")


main()
