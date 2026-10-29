# LeetCode #1018: Binary Prefix Divisible By 5 -- bench
# Mirrors prefix.kara; see ../README.md § Benchmarks.


def prefixes_div_by5(nums):
    answer = []
    r = 0
    for bit in nums:
        r = (r * 2 + bit) % 5
        answer.append(r == 0)
    return answer


seed = 1018


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    length = 2000000
    rounds = 50
    nums = [next_random() % 2 for _ in range(length)]
    trues = 0
    total = 0
    for rnd in range(rounds):
        at = rnd * 39989 % length
        nums[at] = 1 - nums[at]
        answer = prefixes_div_by5(nums)
        for i in range(len(answer)):
            if answer[i]:
                trues += 1
                total = (total + i) % 1000000007
    print(f"{rounds} rounds over {length} bits: {trues} true, index sum {total}")


main()
