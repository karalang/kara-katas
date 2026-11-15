# LeetCode #2177: Find Three Consecutive Integers That Sum to a Given
# Number -- the benchmark's Python mirror of three.kara.


def sum_of_three(num):
    if num % 3 != 0:
        return []
    x = num // 3
    return [x - 1, x, x + 1]


seed = 2177


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    row = []
    for _ in range(1000000):
        a = next_random()
        b = next_random()
        c = next_random()
        row.append(((a * 32768 + b) * 32768 + c) % 1000000000000001)
    found = 0
    check = 0
    for p in range(2):
        for num in row:
            three = sum_of_three(num + p)
            if len(three) == 3:
                found += 1
                check = (check * 31 + three[2] % 1000000007) % 1000000007
    print(f"2000000 solves: {found} found, checksum {check}")


main()
