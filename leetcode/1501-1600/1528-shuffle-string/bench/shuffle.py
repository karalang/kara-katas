# LeetCode #1528: Shuffle String -- bench: the ★ arm over 100000 random
# strings of 1 to 100 letters with shuffled indices, built once and
# answered 30 times.


def restore_string(s, indices):
    out = bytearray(len(s))
    for i, c in enumerate(s.encode()):
        out[indices[i]] = c
    return out.decode()


seed = 1528


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    cases = []
    for _ in range(100000):
        n = next_random() % 100 + 1
        s = "".join(chr(97 + next_random() % 26) for _ in range(n))
        indices = list(range(n))
        for i in range(n - 1, 0, -1):
            j = next_random() % (i + 1)
            indices[i], indices[j] = indices[j], indices[i]
        cases.append((s, indices))
    check = 0
    for p in range(30):
        for s, indices in cases:
            answer = restore_string(s, indices)
            check = mix(check, answer.encode()[p % len(answer)])
    print(f"30 passes over 100000 strings of up to 100 letters: checksum {check}")


main()
