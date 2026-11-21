# LeetCode #1630: Arithmetic Subarrays -- the bench's Python mirror: the ★
# arm on 200 random problems of 500 numbers and 500 queries, all drawn
# first.


def check_arithmetic_subarrays(nums, l, r):
    answers = []
    for a, b in zip(l, r):
        run = sorted(nums[a : b + 1])
        step = run[1] - run[0]
        answers.append(all(y - x == step for x, y in zip(run, run[1:])))
    return answers


seed = 1630


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


problems = []
for p in range(200):
    nums = []
    for i in range(500):
        if p % 2 == 0:
            nums.append(3 * i - 700)
        else:
            nums.append((next_random() * 32768 + next_random()) % 200001 - 100000)
    for i in range(499, 0, -1):
        j = next_random() % (i + 1)
        nums[i], nums[j] = nums[j], nums[i]
    l, r = [], []
    for _ in range(500):
        a = next_random() % 499
        l.append(a)
        r.append(a + 1 + next_random() % (499 - a))
    problems.append((nums, l, r))
check = 0
yes = 0
for nums, l, r in problems:
    for answer in check_arithmetic_subarrays(nums, l, r):
        if answer:
            yes += 1
        check = (check * 31 + int(answer) + 1) % 1000000007
print(f"200 problems of 500 numbers and 500 queries: {yes} arithmetic, checksum {check}")
