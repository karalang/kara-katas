# LeetCode #2343: Query Kth Smallest Trimmed Number -- the bench, the ★ arm
# in Python: for each query the indices sorted by their trimmed text and
# then by index, and the k-th taken.


def smallest_trimmed_numbers(nums, queries):
    width = len(nums[0])
    answer = []
    for k, trim in queries:
        order = sorted(range(len(nums)), key=lambda i: (nums[i][width - trim:], i))
        answer.append(order[k - 1])
    return answer


def scrambled(index):
    return index * 2654435761 % 2147483647


def main():
    cases = []
    for c in range(10):
        nums = ["".join(str(scrambled(c * 10000 + i * 100 + d) % 10) for d in range(100)) for i in range(100)]
        queries = [[1 + scrambled(c * 1000 + q + 500000) % 100, 1 + scrambled(c * 1000 + q + 700000) % 100] for q in range(100)]
        cases.append((nums, queries))
    check = 0
    for p in range(50):
        for nums, queries in cases:
            for i in smallest_trimmed_numbers(nums, queries):
                check = (check * 31 + i + p) % 1000000007
    print(f"50 passes over 10 cases of 100 numbers of 100 digits under 100 queries: checksum {check}")


main()
