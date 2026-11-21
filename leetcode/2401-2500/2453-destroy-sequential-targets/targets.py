# LeetCode #2453: Destroy Sequential Targets -- Python mirror of
# targets.kara: a dict counts each residue class, and a second pass keeps
# the least value of a largest class.


def destroy_targets(nums, space):
    count = {}
    for x in nums:
        count[x % space] = count.get(x % space, 0) + 1
    best = 0
    answer = 0
    for x in nums:
        c = count[x % space]
        if c > best or (c == best and x < answer):
            best = c
            answer = x
    return answer


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    a = next_random()
    return a * 32768 + next_random()


def main():
    global seed
    print(destroy_targets([3, 7, 8, 1, 1, 5], 2))
    print(destroy_targets([1, 3, 5, 2, 4, 6], 2))
    print(destroy_targets([6, 2, 5], 100))
    print(destroy_targets([1000000000], 1))
    print(destroy_targets([9, 4, 7, 4, 8], 1))
    print(destroy_targets([30, 10, 20, 1000000000], 1000000000))
    print(destroy_targets([12, 5, 9, 16, 2, 19], 7))
    seed = 2453
    for space in [1, 7, 1000, 1000000000]:
        nums = [1 + wide_random() % 1000000000 for _ in range(2000)]
        print(f"2000 values, space {space}: {destroy_targets(nums, space)}")
    small = [1 + next_random() % 50 for _ in range(2000)]
    print(f"2000 values up to 50, space 3: {destroy_targets(small, 3)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 8
        nums = [1 + next_random() % 20 for _ in range(n)]
        space = 1 + next_random() % 6
        check = (check * 31 + destroy_targets(nums, space)) % 1000000007
    print(f"3000 random: checksum {check}")


main()
