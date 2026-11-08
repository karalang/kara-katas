# LeetCode #2031: Count Subarrays With More Ones Than Zeros -- Python mirror
# of the ★ arm (subarrays.kara). Count a 1 as +1 and a 0 as -1; `seen`
# counts the prefix sums so far and `below` how many lie under the current
# one, moved one step at a time. O(n).

MOD = 1000000007


def subarrays_more_ones(nums):
    n = len(nums)
    seen = [0] * (2 * n + 1)
    prefix = n
    seen[prefix] = 1
    below = 0
    total = 0
    for x in nums:
        if x == 1:
            below += seen[prefix]
            prefix += 1
        else:
            prefix -= 1
            below -= seen[prefix]
        total = (total + below) % MOD
        seen[prefix] += 1
    return total


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, answer):
    return (check * 31 + answer) % 1000000007


def draw(n, ones):
    return [1 if next_random() % 10 < ones else 0 for _ in range(n)]


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    global seed
    examples = [
        [0, 1, 1, 0, 1],
        [0],
        [1],
        [1, 1, 1],
        [0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 1, 1, 0],
        [1, 1, 0, 0, 0, 1, 1, 1, 1, 0],
    ]
    for nums in examples:
        print(f"{show(nums)} -> {subarrays_more_ones(nums)}")
    seed = 2031
    total = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 20 + 1
        ones = next_random() % 11
        answer = subarrays_more_ones(draw(n, ones))
        total += answer
        check = mix(check, answer)
    print(f"3000 arrays of up to 20 bits: {total} subarrays, checksum {check}")
    check = 0
    for a in range(6):
        answer = subarrays_more_ones(draw(100000, [5, 6, 10, 4, 8, 9][a]))
        check = mix(check, answer)
    print(f"6 arrays of 100000 bits: checksum {check}")


main()
