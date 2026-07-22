"""LeetCode 191 popcount benchmark kernel (Python mirror)."""


def hamming_weight(n):
    count = 0
    x = n
    while x != 0:
        x = x & (x - 1)
        count += 1
    return count


def main():
    n = 2000000
    k = 10
    nums = [0] * n
    state = 12345
    for i in range(n):
        state = (state * 1103515245 + 12345) % 2147483648
        nums[i] = state
    sink = 0
    for round in range(k):
        for j in range(n):
            sink += hamming_weight(nums[j] ^ round)
    print(sink)


main()
