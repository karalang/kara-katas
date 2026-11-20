# LeetCode #2395: Find Subarrays With Equal Sum -- a Python mirror of the
# ★ arm: each neighbouring pair's sum into a set, a sum already there the
# answer. Prints the same output as subarrays.kara.

seed = 0


def find_subarrays(nums):
    seen = set()
    for i in range(1, len(nums)):
        s = nums[i - 1] + nums[i]
        if s in seen:
            return True
        seen.add(s)
    return False


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    high = next_random()
    return high * 32768 + next_random()


def show(b):
    return "true" if b else "false"


def main():
    global seed
    print(show(find_subarrays([4, 2, 4])))
    print(show(find_subarrays([1, 2, 3, 4, 5])))
    print(show(find_subarrays([0, 0, 0])))
    print(f"{show(find_subarrays([3, 1, 3]))} {show(find_subarrays([5, 5]))}")
    seed = 2395
    long = [wide() % 2000000001 - 1000000000 for _ in range(1000)]
    first = find_subarrays(long)
    long.append(long[1])
    long.append(long[0])
    print(f"1000 values: {show(first)}, {show(find_subarrays(long))}")
    check = 0
    yes = 0
    for _ in range(3000):
        n = 2 + next_random() % 11
        top = next_random() % 21
        nums = [next_random() % (2 * top + 1) - top for _ in range(n)]
        found = find_subarrays(nums)
        check = (check * 31 + (2 if found else 1)) % 1000000007
        if found:
            yes += 1
    print(f"3000 arrays: checksum {check}, {yes} yes")


if __name__ == "__main__":
    main()
