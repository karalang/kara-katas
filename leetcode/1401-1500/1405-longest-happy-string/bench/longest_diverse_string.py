# LeetCode #1405 bench, Python: the same greedy, a sort of the three
# letters before each one placed, workload and checksum as
# longest_diverse_string.kara.


def longest_diverse_string(a, b, c):
    left = [(a, "a"), (b, "b"), (c, "c")]
    out = []
    while True:
        left.sort(key=lambda x: -x[0])
        placed = False
        for i in range(3):
            n, ch = left[i]
            if n == 0:
                break
            if len(out) >= 2 and out[-1] == ch and out[-2] == ch:
                continue
            out.append(ch)
            left[i] = (n - 1, ch)
            placed = True
            break
        if not placed:
            return "".join(out)


def main():
    seed = 1405
    check = 0
    for _ in range(20000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        a = seed // 65536 % 101
        seed = (seed * 1103515245 + 12345) % 2147483648
        b = seed // 65536 % 101
        seed = (seed * 1103515245 + 12345) % 2147483648
        c = 1 + seed // 65536 % 100
        for ch in longest_diverse_string(a, b, c):
            check = (check * 131 + ord(ch)) % 1000000007
    print(f"20000 strings of up to 300 letters: checksum {check}")


main()
