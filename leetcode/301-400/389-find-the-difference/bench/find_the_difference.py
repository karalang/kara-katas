# Benchmark for #389: mirror of find_the_difference.kara (XOR of every byte).


def find_the_difference(s, t):
    x = 0
    for b in s:
        x ^= b
    for b in t:
        x ^= b
    return x


def step(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [389]
    pool = bytes(step(seed) % 26 + 97 for _ in range(1000000))
    view = memoryview(pool)
    right = checksum = 0
    for _ in range(8000000):
        n = step(seed) % 1001
        a = step(seed) % (1000000 - n - 1)
        c = find_the_difference(view[a:a + n], view[a:a + n + 1])
        if c == pool[a + n]:
            right += 1
        checksum = (checksum * 31 + c) % 1000000007
    print(f"8000000 pairs, {right} right, checksum {checksum}")


main()
