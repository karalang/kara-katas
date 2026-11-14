# LeetCode #1538: Guess the Majority in a Hidden Array -- bench: the ★ arm
# (every bit compared with bit 0, n queries) over 100 readers of 5 to 50000
# bits, built once, each asked 20 times. Python mirror of majority.kara.


class ArrayReader:
    def __init__(self, nums):
        self.nums = nums
        self.calls = 0

    def query(self, a, b, c, d):
        self.calls += 1
        nums = self.nums
        ones = nums[a] + nums[b] + nums[c] + nums[d]
        if ones == 0 or ones == 4:
            return 4
        if ones == 2:
            return 0
        return 2

    def length(self):
        return len(self.nums)


def guess_majority(reader):
    n = reader.length()
    q0123 = reader.query(0, 1, 2, 3)
    q1234 = reader.query(1, 2, 3, 4)
    same = [True] * n
    same[1] = reader.query(0, 2, 3, 4) == q1234
    same[2] = reader.query(0, 1, 3, 4) == q1234
    same[3] = reader.query(0, 1, 2, 4) == q1234
    same[4] = q1234 == q0123
    for i in range(5, n):
        same[i] = reader.query(1, 2, 3, i) == q0123
    with_zero = 0
    other = -1
    for i in range(n):
        if same[i]:
            with_zero += 1
        else:
            other = i
    if with_zero * 2 > n:
        return 0
    if with_zero * 2 < n:
        return other
    return -1


seed = 1538


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    readers = []
    for _ in range(100):
        a = next_random()
        n = (a * 32768 + next_random()) % 49996 + 5
        chance = next_random() % 101
        nums = [1 if next_random() % 100 < chance else 0 for _ in range(n)]
        readers.append(ArrayReader(nums))
    check = 0
    for _ in range(20):
        for reader in readers:
            check = mix(check, guess_majority(reader))
    calls = sum(r.calls for r in readers)
    print(f"20 passes over 100 readers of up to 50000 bits: checksum {check}, {calls} calls")


main()
