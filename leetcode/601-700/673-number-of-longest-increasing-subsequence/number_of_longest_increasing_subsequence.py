# LeetCode #673: Number of Longest Increasing Subsequence -- the length
# and count ending at each place.
# Mirrors the ★ arm (number_of_longest_increasing_subsequence.kara) and
# its test harness.


def find_number_of_lis(nums):
    n = len(nums)
    length = [1] * n
    count = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]:
                    length[i] = length[j] + 1
                    count[i] = count[j]
                elif length[j] + 1 == length[i]:
                    count[i] += count[j]
    best = 0
    for v in length:
        best = max(best, v)
    total = 0
    for i in range(n):
        if length[i] == best:
            total += count[i]
    return total


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(nums):
    if len(nums) <= 10:
        body = ", ".join(str(v) for v in nums)
        return f"[{body}]"
    return f"{len(nums)} numbers"


def main():
    cases = [[1, 3, 5, 4, 7], [2, 2, 2, 2, 2], [7], [1, 2, 3, 4, 5, 6],
             [6, 5, 4, 3, 2, 1], [1, 1, 2, 2, 3, 3], [-3, -1, -2, 0],
             [3, 1, 2], [1, 2, 4, 3, 5, 4, 7, 2], [1, 2, 3, 1, 2, 3, 1, 2, 3],
             [2, 1, 4, 3, 6, 5, 8, 7, 10, 9]]
    pairs = []
    for i in range(30):
        pairs.append(2 * i + 2)
        pairs.append(2 * i + 1)
    cases.append(pairs)
    rising = []
    falling = []
    for i in range(2000):
        rising.append(i - 1000000)
        falling.append(1000000 - i)
    cases.append(rising)
    cases.append(falling)
    for nums in cases:
        print(f"{show(nums)}: {find_number_of_lis(nums)}")
    rng = Rng(673)
    s = 0
    most = 0
    for c in range(300):
        size = 1 + rng.next() % 200
        spread = [5, 50, 2000001][c % 3]
        nums = []
        for _ in range(size):
            nums.append(rng.next() % spread - spread // 2)
        got = find_number_of_lis(nums)
        most = max(most, got)
        s = (s * 31 + got) % 1000000007
    print(f"300 random: largest {most}, checksum {s}")
    for _ in range(3):
        nums = []
        for _ in range(1000):
            nums.append((rng.next() * 32768 + rng.next()) % 2000001 - 1000000)
        print(f"1000 random: {find_number_of_lis(nums)}")


main()
