# LeetCode #2395: Find Subarrays With Equal Sum -- the bench, the ★ arm in
# Python: each neighbouring pair's sum into a set, a sum already there the
# answer.

seed = 2395


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


def main():
    arrays = []
    for _ in range(100):
        top = 1000 + wide() % 1000000
        arrays.append([wide() % (2 * top + 1) - top for _ in range(1000)])
    check = 0
    yes = 0
    for p in range(2000):
        for a in arrays:
            found = find_subarrays(a)
            check = (check * 31 + (2 if found else 1) + p) % 1000000007
            if found:
                yes += 1
    print(f"2000 passes over 100 arrays of 1000 values: checksum {check}, {yes} yes")


if __name__ == "__main__":
    main()
