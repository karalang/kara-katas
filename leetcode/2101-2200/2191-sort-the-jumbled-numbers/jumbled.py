# Python mirror of jumbled.kara (LeetCode #2191, the ★ arm): each
# number's mapped value worked out once, digit by digit from the last,
# kept with its place; the pairs sorted and the numbers read back.


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


def random_mapping():
    mapping = list(range(10))
    for i in range(9, 0, -1):
        j = next_random() % (i + 1)
        mapping[i], mapping[j] = mapping[j], mapping[i]
    return mapping


def random_nums(n, top):
    nums = []
    for _ in range(n):
        high = next_random() % 32768
        nums.append((high * 32768 + next_random()) % top)
    return nums


def checksum(xs, check):
    for x in xs:
        check = (check * 31 + x % 1000003) % 1000000007
    return check


def fmt(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def show(mapping, nums):
    print(f"{fmt(mapping)}, {fmt(nums)} -> {fmt(sort_jumbled(mapping, nums))}")


show([8, 9, 4, 0, 2, 1, 3, 5, 7, 6], [991, 338, 38])
show([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [789, 456, 123])
show([9, 8, 7, 6, 5, 4, 3, 2, 1, 0], [42])
show([9, 8, 7, 6, 5, 4, 3, 2, 1, 0], [0, 9, 90, 999999999])
show([1, 0, 2, 3, 4, 5, 6, 7, 8, 9], [12, 2, 112, 1, 0])
show([9, 1, 2, 3, 4, 5, 6, 7, 8, 0], [9, 1000, 19, 0, 909])
firsts = check = 0
for rnd in range(2000):
    mapping = random_mapping()
    n = next_random() % 30 + 1
    top = [10, 1000, 1000000000][rnd % 3]
    nums = random_nums(n, top)
    s = sort_jumbled(mapping, nums)
    firsts += s[0]
    check = checksum(s, check)
print(f"2000 cases: first numbers add up to {firsts}, checksum {check}")
mapping = random_mapping()
nums = random_nums(30000, 1000000000)
s = sort_jumbled(mapping, nums)
print(f"30000 numbers: first {s[0]}, last {s[29999]}, checksum {checksum(s, 0)}")
