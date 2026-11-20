# LeetCode #2399: Check Distances Between Same Letters -- a Python mirror
# of the ★ arm: the first index of each letter, checked at its second.
# Prints the same output as distances.kara.

seed = 0


def check_distances(s, distance):
    first = [-1] * 26
    for i, ch in enumerate(s):
        c = ord(ch) - ord("a")
        if first[c] < 0:
            first[c] = i
        elif i - first[c] - 1 != distance[c]:
            return False
    return True


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def case(m):
    letters = list(range(26))
    for i in range(1, 26):
        j = next_random() % (i + 1)
        letters[i], letters[j] = letters[j], letters[i]
    b = []
    for i in range(m):
        b.append(letters[i])
        b.append(letters[i])
    for i in range(1, len(b)):
        j = next_random() % (i + 1)
        b[i], b[j] = b[j], b[i]
    distance = [next_random() % 50 for _ in range(26)]
    first = [-1] * 26
    for i, c in enumerate(b):
        if first[c] < 0:
            first[c] = i
        else:
            distance[c] = i - first[c] - 1
    return "".join(chr(ord("a") + c) for c in b), distance


def show(x):
    return "true" if x else "false"


def main():
    global seed
    example = [0] * 26
    example[0] = 1
    example[1] = 3
    example[2] = 0
    example[4] = 5
    print(show(check_distances("abaccb", example)))
    second = [0] * 26
    second[0] = 1
    print(show(check_distances("aa", second)))
    print(f"{show(check_distances('zz', [0] * 26))} {show(check_distances('zz', [1] * 26))}")
    seed = 2399
    alphabet = "".join(chr(ord("a") + i % 26) for i in range(52))
    far = [25] * 26
    print(show(check_distances(alphabet, far)))
    far[25] = 24
    print(show(check_distances(alphabet, far)))
    check = 0
    yes = 0
    for t in range(3000):
        m = 1 + next_random() % 26
        s, distance = case(m)
        letter = ord(s[next_random() % len(s)]) - ord("a")
        if t % 3 == 1:
            distance[letter] += 1 if distance[letter] == 0 else -1
        elif t % 3 == 2:
            distance[letter] = next_random() % 50
        ok = check_distances(s, distance)
        check = (check * 31 + (2 if ok else 1)) % 1000000007
        if ok:
            yes += 1
    print(f"3000 strings: checksum {check}, {yes} yes")


if __name__ == "__main__":
    main()
