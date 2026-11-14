# LeetCode #1535: Find the Winner of an Array Game -- Python mirror of
# winner.kara (one pass with a running front and its streak); output
# byte-identical.


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


def batch(count, most, reach):
    check = 0
    for _ in range(count):
        n = draw(most - 1) + 2
        arr = [v * 3 for v in range(1, n + 1)]
        for i in range(n - 1, 0, -1):
            j = draw(i + 1)
            arr[i], arr[j] = arr[j], arr[i]
        k = draw(reach) + 1
        check = mix(check, get_winner(arr, k))
    print(f"{count} arrays of 2 to {most} values, k up to {reach}: checksum {check}")


for arr, k in [([2, 1, 3, 5, 4, 6, 7], 2), ([3, 2, 1], 10), ([1, 9, 8, 2, 3, 7, 6, 4, 5], 7),
               ([1, 11, 22, 33, 44, 55, 66, 77, 88, 99], 1000000000), ([5, 1], 1), ([1, 5], 1), ([4, 3, 2, 1, 5], 3)]:
    print(f"[{', '.join(map(str, arr))}], k = {k} -> {get_winner(arr, k)}")
rising = list(range(1, 100001))
print(f"1 to 100000, k = 1 -> {get_winner(rising, 1)}, k = 99999 -> {get_winner(rising, 99999)}")
batch(3000, 12, 15)
batch(300, 1000, 2000)
batch(3, 100000, 1000000000)
