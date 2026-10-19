# LeetCode 796 -- Rotate String: the bench, in Python. Mirrors
# rotate_string.kara: goal is a rotation when it is as long as s and in s
# written twice.


def rotate_string(s, goal):
    return len(s) == len(goal) and goal in s + s


seed = 796


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    pairs = []
    for _ in range(4096):
        letters = 1 + next_random() % 4
        s = "".join(chr(97 + next_random() % letters) for _ in range(100))
        kind = next_random() % 3
        if kind == 2:
            goal = "".join(chr(97 + next_random() % letters) for _ in range(100))
        else:
            k = next_random() % 100
            change = next_random() % 100 if kind == 1 else -1
            out = []
            for j in range(100):
                c = s[(j + k) % 100]
                out.append(chr(97 + (ord(c) - 97 + 1) % letters) if j == change else c)
            goal = "".join(out)
        pairs.append((s, goal))
    rounds = 1500000
    rotations = 0
    check = 0
    for r in range(rounds):
        s, goal = pairs[r % 4096]
        if rotate_string(s, goal):
            rotations += 1
            check = (check * 131 + r % 4096) % 1000000007
    print(f"{rounds} pairs: {rotations} rotations, checksum {check}")


main()
