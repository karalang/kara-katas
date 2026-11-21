# LeetCode #2442: Count Number of Distinct Integers After Reverse
# Operations -- Python mirror of the ★ arm (distinct.kara): the digits
# reversed by % 10 and // 10, and a table of flags up to the largest.


def reversed_digits(x):
    r = 0
    y = x
    while y > 0:
        r = r * 10 + y % 10
        y //= 10
    return r


def count_distinct_integers(nums):
    values = nums[:]
    for x in nums:
        values.append(reversed_digits(x))
    largest = 0
    for v in values:
        largest = max(largest, v)
    seen = [False] * (largest + 1)
    count = 0
    for v in values:
        if not seen[v]:
            seen[v] = True
            count += 1
    return count


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    global seed
    for nums in ([1, 13, 10, 12, 31], [2, 2, 2], [1000000], [100, 1, 10], [121, 7, 1221, 98789]):
        print(f"{show(nums)}: {count_distinct_integers(nums)}")
    seed = 2442
    print(f"1 to 10^5: {count_distinct_integers(list(range(1, 100001)))}")
    print(f"multiples of 10: {count_distinct_integers([i * 10 for i in range(1, 100001)])}")
    random = []
    for _ in range(100000):
        a = next_random()
        random.append(1 + (a * 32768 + next_random()) % 1000000)
    print(f"random: {count_distinct_integers(random)}")
    check = 0
    total = 0
    for _ in range(3000):
        length = 1 + next_random() % 10
        nums = [1 + next_random() % 200 for _ in range(length)]
        answer = count_distinct_integers(nums)
        check = (check * 31 + answer) % 1000000007
        total += answer
    print(f"3000 random: checksum {check}, total {total}")


main()
