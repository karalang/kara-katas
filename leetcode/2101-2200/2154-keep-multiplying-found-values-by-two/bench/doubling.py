# LeetCode #2154: Keep Multiplying Found Values by Two -- the benchmark's
# Python mirror of doubling.kara.


def find_final_value(nums, original):
    found = set(nums)
    value = original
    while value in found:
        value *= 2
    return value


seed = 2154


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    row = []
    for _ in range(400000):
        row.append(next_random() % 1000 + 1)
    check = 0
    for _ in range(20000):
        a = next_random()
        b = next_random()
        start = (a * 32768 + b) % 399001
        original = next_random() % 1000 + 1
        value = find_final_value(row[start:start + 1000], original)
        check = (check * 31 + value) % 1000000007
    print(f"20000 solves: checksum {check}")


main()
