# LeetCode #2439: Minimize Maximum of Array -- Python mirror of the ★ arm
# (minmax.kara): the largest ceiling average of any prefix, in one pass.


def minimize_array_value(nums):
    total = 0
    answer = 0
    for i, x in enumerate(nums):
        total += x
        answer = max(answer, (total + i) // (i + 1))
    return answer


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    a = next_random()
    return a * 32768 + next_random()


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    global seed
    for nums in ([3, 7, 1, 6], [10, 1], [0, 0], [0, 1000000000]):
        print(f"{show(nums)}: {minimize_array_value(nums)}")
    n = 10000
    first = [0] * n
    first[0] = 1000000000
    last = [0] * n
    last[n - 1] = 1000000000
    full = [1000000000] * n
    rise = [i * 100000 for i in range(n)]
    seed = 2439
    random = [wide_random() % 1000000001 for _ in range(n)]
    print(f"10^9 first: {minimize_array_value(first)}")
    print(f"10^9 last: {minimize_array_value(last)}")
    print(f"all 10^9: {minimize_array_value(full)}")
    print(f"rising: {minimize_array_value(rise)}")
    print(f"random: {minimize_array_value(random)}")
    check = 0
    total = 0
    for _ in range(3000):
        length = 2 + next_random() % 11
        nums = [next_random() % 21 for _ in range(length)]
        answer = minimize_array_value(nums)
        check = (check * 31 + answer) % 1000000007
        total += answer
    print(f"3000 random: checksum {check}, total {total}")


main()
