# LeetCode #1528: Shuffle String -- mirrors shuffle.kara (the ★ arm): each
# letter written where its index sends it. O(n).


def restore_string(s, indices):
    out = bytearray(len(s))
    for i, c in enumerate(s.encode()):
        out[indices[i]] = c
    return out.decode()


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def random_case(most, letters):
    n = next_random() % most + 1
    s = "".join(chr(97 + next_random() % letters) for _ in range(n))
    indices = list(range(n))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        indices[i], indices[j] = indices[j], indices[i]
    return s, indices


def batch(count, most, letters):
    check = 0
    for _ in range(count):
        s, indices = random_case(most, letters)
        for b in restore_string(s, indices).encode():
            check = mix(check, b - 96)
    print(f"{count} strings of 1 to {most} letters over {letters}: checksum {check}")


def main():
    global seed
    examples = [
        ("codeleet", [4, 5, 6, 7, 0, 2, 1, 3]),
        ("abc", [0, 1, 2]),
        ("aiohn", [3, 1, 4, 2, 0]),
        ("z", [0]),
        ("abcdefghij", [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]),
    ]
    for s, indices in examples:
        print(f"{s}, [{', '.join(map(str, indices))}] -> {restore_string(s, indices)}")
    seed = 1528
    batch(3000, 8, 3)
    batch(3000, 100, 26)


main()
