# LeetCode #2399: Check Distances Between Same Letters -- the bench, the
# ★ arm in Python: the first index of each letter, checked at its second.

seed = 2399


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def check_distances(s, distance):
    first = [-1] * 26
    for i, ch in enumerate(s):
        c = ord(ch) - 97
        if first[c] < 0:
            first[c] = i
        elif i - first[c] - 1 != distance[c]:
            return False
    return True


def case(off):
    """All 26 letters, each twice, shuffled, and the distances true of it;
    when `off`, one letter's distance is one away from its true one."""
    b = [97 + i // 2 for i in range(52)]
    for i in range(1, 52):
        j = next_random() % (i + 1)
        b[i], b[j] = b[j], b[i]
    distance = [0] * 26
    first = [-1] * 26
    for i in range(52):
        c = b[i] - 97
        if first[c] < 0:
            first[c] = i
        else:
            distance[c] = i - first[c] - 1
    if off:
        letter = next_random() % 26
        distance[letter] += 1 if distance[letter] == 0 else -1
    return bytes(b).decode(), distance


def main():
    cases = [case(i % 2 == 1) for i in range(1000)]
    check = 0
    yes = 0
    for p in range(2000):
        for s, distance in cases:
            answer = check_distances(s, distance)
            if answer:
                yes += 1
            check = (check * 31 + (2 if answer else 1) + p) % 1000000007
    print(f"2000 passes over 1000 strings of 52 letters: checksum {check}, {yes} yes")


main()
