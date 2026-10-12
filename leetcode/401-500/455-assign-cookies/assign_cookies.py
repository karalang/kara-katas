# LeetCode #455: Assign Cookies -- mirror of assign_cookies.kara (both
# sorted, least greedy child first), with the same harness.


def find_content_children(g, s):
    greed = sorted(g)
    sizes = sorted(s)
    child = 0
    for size in sizes:
        if child < len(greed) and size >= greed[child]:
            child += 1
    return child


# ---- test harness ---------------------------------------------------------


def listed(nums):
    return ",".join(str(x) for x in nums)


def show(g, s):
    fed = find_content_children(g, s)
    print(f"g [{listed(g)}] s [{listed(s)}]: {fed} content")


seed = 455


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_nums(n, top):
    nums = []
    for _ in range(n):
        r = next_random() * 65536
        r += next_random()
        nums.append(1 + r % top)
    return nums


def main():
    show([1, 2, 3], [1, 1])
    show([1, 2], [1, 2, 3])
    show([1, 2, 3], [])
    show([5], [4])
    show([2147483647], [2147483647, 1])
    show([10, 9, 8, 7], [5, 6, 7, 8])
    show([1, 1, 1, 1], [1, 1])
    show([3, 1, 2], [2, 3, 1])
    # 300 random cases of 1 to 200 children and 0 to 200 cookies, with
    # greed and sizes from 1 up to 5, 100, 10,000 or 2^31 - 1.
    count = 300
    total = 0
    checksum = 0
    for _ in range(count):
        children = 1 + next_random() % 200
        cookies = next_random() % 201
        top = [5, 100, 10000, 2147483647][next_random() % 4]
        g = random_nums(children, top)
        s = random_nums(cookies, top)
        fed = find_content_children(g, s)
        total += fed
        checksum = (checksum * 31 + fed) % 1000000007
    print(f"{count} random cases: {total} content, checksum {checksum}")


main()
