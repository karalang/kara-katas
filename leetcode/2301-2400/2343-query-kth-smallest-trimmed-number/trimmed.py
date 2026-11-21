# LeetCode #2343: Query Kth Smallest Trimmed Number -- the Python mirror of
# the ★ arm: for each query the indices sorted by their trimmed number,
# compared as text of equal length, and then by index.


def smallest_trimmed_numbers(nums, queries):
    width = len(nums[0])
    answer = []
    for k, trim in queries:
        order = sorted(range(len(nums)), key=lambda i: (nums[i][width - trim:], i))
        answer.append(order[k - 1])
    return answer


SEED = [2343]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def random_digits(width, alphabet):
    return "".join(str(next_random() % alphabet) for _ in range(width))


def main():
    print(show(smallest_trimmed_numbers(["102", "473", "251", "814"], [[1, 1], [2, 3], [4, 2], [1, 2]])))
    print(show(smallest_trimmed_numbers(["24", "37", "96", "04"], [[2, 1], [2, 2]])))
    print(show(smallest_trimmed_numbers(["7"], [[1, 1]])))
    print(show(smallest_trimmed_numbers(["00", "00", "00"], [[1, 2], [2, 1], [3, 2]])))
    nums = [random_digits(100, 10) for _ in range(100)]
    queries = [[1 + next_random() % 100, 1 + next_random() % 100] for _ in range(100)]
    big = smallest_trimmed_numbers(nums, queries)
    print(f"100 by 100: {sum(big)}, first {big[0]}, last {big[-1]}")
    check = 0
    total = 0
    for _ in range(2000):
        n = 1 + next_random() % 10
        width = 1 + next_random() % 6
        alphabet = 2 + next_random() % 9
        nums = [random_digits(width, alphabet) for _ in range(n)]
        m = 1 + next_random() % 5
        queries = [[1 + next_random() % n, 1 + next_random() % width] for _ in range(m)]
        for i in smallest_trimmed_numbers(nums, queries):
            check = (check * 31 + i + 1) % 1000000007
            total += i
    print(f"2000 cases: checksum {check}, indices {total}")


main()
