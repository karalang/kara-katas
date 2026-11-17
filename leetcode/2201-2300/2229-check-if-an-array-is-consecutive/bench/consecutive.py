# LeetCode #2229: Check if an Array Is Consecutive -- the benchmark's
# Python mirror of consecutive.kara: the span against the count, and a
# set to find a repeat.


def is_consecutive(nums):
    seen = set()
    smallest = nums[0]
    largest = nums[0]
    for x in nums:
        if x in seen:
            return False
        seen.add(x)
        smallest = min(smallest, x)
        largest = max(largest, x)
    return largest - smallest + 1 == len(nums)


seed = 2229


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def main():
    lists = []
    for l in range(4):
        nums = list(range(100000))
        for i in range(99999, 0, -1):
            j = wide_random() % (i + 1)
            nums[i], nums[j] = nums[j], nums[i]
        if l >= 2:
            frm = wide_random() % 100000
            to = wide_random() % 100000
            nums[to] = nums[frm]
        lists.append(nums)
    yes = 0
    check = 0
    for _ in range(25):
        for l in range(4):
            # punch: two numbers trade places before each answer
            i = wide_random() % 100000
            j = wide_random() % 100000
            lists[l][i], lists[l][j] = lists[l][j], lists[l][i]
            answer = is_consecutive(lists[l])
            if answer:
                yes += 1
            check = (check * 31 + lists[l][i] + (1 if answer else 2)) % 1000000007
    print(f"100 answers: {yes} consecutive, checksum {check}")


main()
