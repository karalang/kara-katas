# LeetCode #1630: Arithmetic Subarrays -- the Python mirror of the ★ arm:
# each query's run copied out, sorted, and checked pair by pair.


def check_arithmetic_subarrays(nums, l, r):
    answers = []
    for a, b in zip(l, r):
        run = sorted(nums[a : b + 1])
        step = run[1] - run[0]
        answers.append(all(y - x == step for x, y in zip(run, run[1:])))
    return answers


def show(answers):
    return "[" + ", ".join("true" if a else "false" for a in answers) + "]"


# ---- the harness: the same as every arm's ---------------------------------

seed = 1630


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, most, spread, asks):
    check = 0
    yes = 0
    for _ in range(count):
        n = next_random() % (most - 1) + 2
        nums = [next_random() % (2 * spread + 1) - spread for _ in range(n)]
        m = next_random() % asks + 1
        l, r = [], []
        for _ in range(m):
            a = next_random() % (n - 1)
            l.append(a)
            r.append(a + 1 + next_random() % (n - 1 - a))
        for answer in check_arithmetic_subarrays(nums, l, r):
            if answer:
                yes += 1
            check = (check * 31 + int(answer) + 1) % 1000000007
    print(f"{count} problems of up to {most} numbers: {yes} queries arithmetic, checksum {check}")


print(show(check_arithmetic_subarrays([4, 6, 5, 9, 3, 7], [0, 0, 2], [2, 3, 5])))
print(show(check_arithmetic_subarrays([-12, -9, -3, -12, -6, 15, 20, -25, -20, -15, -10], [0, 1, 6, 4, 8, 7], [4, 4, 9, 7, 9, 10])))
print(show(check_arithmetic_subarrays([7, 7, 7, 7], [0, 1], [3, 2])))
print(show(check_arithmetic_subarrays([1, 3, 3, 5, 7], [0, 1], [4, 3])))
batch(3000, 8, 2, 6)
batch(300, 500, 100000, 50)
batch(20, 500, 3, 500)
