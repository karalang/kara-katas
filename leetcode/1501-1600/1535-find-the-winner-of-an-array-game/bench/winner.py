# LeetCode #1535: Find the Winner of an Array Game -- bench: the ★ arm
# over 100 random arrays of 100000 distinct values, each with its own k
# from 1 to 200000, built once and answered 20 times. Python mirror of
# winner.kara.


def get_winner(arr, k):
    front, streak = arr[0], 0
    for v in arr[1:]:
        if v > front:
            front, streak = v, 1
        else:
            streak += 1
        if streak == k:
            return front
    return front


seed = 1535


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def draw(below):
    hi = next_random()
    return (hi * 32768 + next_random()) % below


cases = []
for _ in range(100):
    n = 100000
    arr = [v * 3 for v in range(1, n + 1)]
    for i in range(n - 1, 0, -1):
        j = draw(i + 1)
        arr[i], arr[j] = arr[j], arr[i]
    cases.append((arr, draw(200000) + 1))
check = 0
for _ in range(20):
    for arr, k in cases:
        check = mix(check, get_winner(arr, k))
print(f"20 passes over 100 arrays of 100000 values: checksum {check}")
