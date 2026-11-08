# LeetCode #2031: Count Subarrays With More Ones Than Zeros -- the ★ arm in
# Python, the same algorithm and workload as subarrays.kara.

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


seed = 2031


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for a in range(20):
        arrays.append([1 if next_random() % 10 < a % 9 + 1 else 0 for _ in range(100000)])
    calls = 0
    total = 0
    check = 0
    for rnd in range(100):
        for a in range(20):
            at = (rnd * 997 + a * 31) % 100000
            arrays[a][at] = 1 - arrays[a][at]
            answer = subarrays_more_ones(arrays[a])
            calls += 1
            total = (total + answer) % MOD
            check = (check * 31 + answer) % MOD
    print(f"{calls} calls: sum {total}, checksum {check}")


main()
