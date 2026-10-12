# LeetCode #444: Sequence Reconstruction -- mirror of
# sequence_reconstruction.kara (positions and neighbouring pairs).


def sequence_reconstruction(nums, sequences):
    n = len(nums)
    position = [0] * (n + 1)
    for i in range(n):
        position[nums[i]] = i
    covered = [False] * n
    for s in sequences:
        for j in range(1, len(s)):
            a = position[s[j - 1]]
            b = position[s[j]]
            if a >= b:
                return False
            if b == a + 1:
                covered[a] = True
    for i in range(n - 1):
        if not covered[i]:
            return False
    return True


def lst(v):
    return "[" + ",".join(str(x) for x in v) + "]"


def show(nums, sequences):
    ans = "true" if sequence_reconstruction(nums, sequences) else "false"
    print(f"{lst(nums)} [{','.join(lst(s) for s in sequences)}]: {ans}")

seed = 444
def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


show([1, 2, 3], [[1, 2], [1, 3]])
show([1, 2, 3], [[1, 2]])
show([1, 2, 3], [[1, 2], [1, 3], [2, 3]])
show([1], [[1]])
show([4, 1, 5, 2, 6, 3], [[5, 2, 6, 3], [4, 1, 5, 2]])
show([2, 1], [[2], [1]])
show([1, 2, 3], [[2, 1], [1, 3]])
show([1, 2, 3], [[1, 2], [2, 3], [3, 1]])
count = 300
true_count = 0
checksum = 0
for case in range(count):
    n = 1 + next_random() % 60
    nums = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        nums[i], nums[j] = nums[j], nums[i]
    sequences = []
    windows = 1 + next_random() % (n * 2 + 2)
    for _ in range(windows):
        start = next_random() % n
        length = 1 + next_random() % 12
        s = []
        for i in range(start, min(start + length, n)):
            if len(s) == 0 or next_random() % 10 != 0:
                s.append(nums[i])
        sequences.append(s)
    answer = sequence_reconstruction(nums, sequences)
    if answer:
        true_count += 1
    checksum = (checksum * 31 + n * 2 + (1 if answer else 0)) % 1000000007
print(f"{count} random cases: {true_count} true, checksum {checksum}")
