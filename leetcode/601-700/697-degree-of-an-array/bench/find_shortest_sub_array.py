# LeetCode #697: Degree of an Array -- bench program, Python mirror of the table arm.

seed = 697


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def find_shortest_sub_array(nums):
    size = 50000
    count = [0] * size
    first = [-1] * size
    last = [0] * size
    for i, x in enumerate(nums):
        if first[x] < 0:
            first[x] = i
        last[x] = i
        count[x] += 1
    degree = 0
    best = len(nums)
    for x in range(size):
        if count[x] == 0:
            continue
        span = last[x] - first[x] + 1
        if count[x] > degree or (count[x] == degree and span < best):
            degree = count[x]
            best = span
    return best


def main():
    arrays = []
    for k in range(40):
        rng = 1 + 1250 * k
        nums = []
        for _ in range(50000):
            a = next_random()
            b = next_random()
            nums.append((a * 65536 + b) % rng)
        arrays.append(nums)
    rounds = 20
    total = 0
    checksum = 0
    for _ in range(rounds):
        for nums in arrays:
            r = find_shortest_sub_array(nums)
            total += r
            checksum = (checksum * 31 + r) % 1000000007
    print(f"{rounds} rounds of 40 arrays of 50000: shortest spans sum to {total}, checksum {checksum}")


main()
