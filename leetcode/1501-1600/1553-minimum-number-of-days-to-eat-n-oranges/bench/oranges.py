# LeetCode #1553: Minimum Number of Days to Eat N Oranges -- bench: the ★
# arm (halve or third after the single days, every answer kept in a fresh
# map per call) over 20000 piles of 1 to 2*10^9, drawn once, each asked 3
# times. Python mirror of
# oranges.kara.


def days(n, memo):
    if n <= 1:
        return n
    if n in memo:
        return memo[n]
    halve = n % 2 + days(n // 2, memo)
    third = n % 3 + days(n // 3, memo)
    best = 1 + min(halve, third)
    memo[n] = best
    return best


def min_days(n):
    return days(n, {})


seed = 1553


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    piles = []
    for _ in range(20000):
        wide = (next_random() * 32768 + next_random()) * 32768 + next_random()
        piles.append(wide % 2000000000 + 1)
    check = 0
    total = 0
    for _ in range(3):
        for n in piles:
            d = min_days(n)
            total += d
            check = mix(check, d)
    print(f"3 passes over 20000 piles of up to 2000000000: {total} days, checksum {check}")


main()
