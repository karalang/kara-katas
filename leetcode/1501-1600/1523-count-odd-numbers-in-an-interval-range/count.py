# LeetCode #1523: Count Odd Numbers in an Interval Range -- mirrors
# count.kara, the ★ arm: odd numbers up to high less those below low.


def count_odds(low, high):
    return (high + 1) // 2 - low // 2


seed = 1523


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most):
    check = 0
    for _ in range(count):
        a = (next_random() * 32768 + next_random()) % (most + 1)
        b = (next_random() * 32768 + next_random()) % (most + 1)
        check = mix(check, count_odds(min(a, b), max(a, b)))
    print(f"{count} intervals within 0 to {most}: checksum {check}")


for low, high in [(3, 7), (8, 10), (0, 0), (5, 5), (0, 1000000000), (999999999, 1000000000)]:
    print(f"{low} to {high} -> {count_odds(low, high)}")
batch(3000, 20)
batch(3000, 1000000000)
