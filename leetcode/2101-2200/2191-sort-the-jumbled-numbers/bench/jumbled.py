# benchmark's Python mirror of jumbled.kara (LeetCode #2191, the ★ arm):
# (value, place) pairs sorted.


def mapped(mapping, n):
    if n == 0:
        return mapping[0]
    rest, value, place = n, 0, 1
    while rest > 0:
        value += mapping[rest % 10] * place
        place *= 10
        rest //= 10
    return value


def sort_jumbled(mapping, nums):
    keyed = sorted((mapped(mapping, x), i) for i, x in enumerate(nums))
    return [nums[i] for _, i in keyed]


seed = 2191


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big_random():
    a = next_random()
    b = next_random()
    return a * 32768 + b


def main():
    row = [big_random() % 1000000000 for _ in range(1000000)]
    check = 0
    for _ in range(200):
        mapping = list(range(10))
        for i in range(9, 0, -1):
            j = next_random() % (i + 1)
            mapping[i], mapping[j] = mapping[j], mapping[i]
        start = big_random() % 970001
        for x in sort_jumbled(mapping, row[start:start + 30000]):
            check = (check * 31 + x % 1000003) % 1000000007
    print(f"200 solves: checksum {check}")


main()
