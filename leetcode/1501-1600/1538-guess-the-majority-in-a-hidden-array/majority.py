# LeetCode #1538: Guess the Majority in a Hidden Array -- Python mirror of
# majority.kara (every bit compared with bit 0); output byte-identical.


class ArrayReader:
    def __init__(self, nums):
        self.nums = nums
        self.calls = 0

    def query(self, a, b, c, d):
        self.calls += 1
        ones = self.nums[a] + self.nums[b] + self.nums[c] + self.nums[d]
        return 4 if ones in (0, 4) else 0 if ones == 2 else 2

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


def judged(nums):
    answer = guess_majority(ArrayReader(nums))
    ones = sum(nums)
    zeros = len(nums) - ones
    majority = 1 if ones > zeros else 0 if zeros > ones else -1
    if answer == -1:
        return -1 if majority == -1 else -2
    if answer < 0 or answer >= len(nums) or nums[answer] != majority:
        return -2
    return majority


def batch(count, most):
    check = 0
    ties = 0
    for _ in range(count):
        hi = next_random()
        n = (hi * 32768 + next_random()) % (most - 4) + 5
        chance = next_random() % 101
        nums = [1 if next_random() % 100 < chance else 0 for _ in range(n)]
        verdict = judged(nums)
        if verdict == -1:
            ties += 1
        check = mix(check, verdict + 2)
    print(f"{count} arrays of 5 to {most} bits: {ties} ties, checksum {check}")


for nums in [[0, 0, 1, 0, 1, 1, 1, 1], [0, 0, 1, 1, 0], [1, 0, 1, 0, 1, 0, 1, 0], [1, 1, 1, 1, 1], [0, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 1]]:
    print(f"[{', '.join(map(str, nums))}] -> {judged(nums)}")
alternating = [i % 2 for i in range(100000)]
print(f"100000 alternating -> {judged(alternating)}")
alternating.append(1)
print(f"100001 alternating -> {judged(alternating)}")
batch(3000, 12)
batch(300, 1000)
batch(30, 100000)
