# LeetCode #1553: Minimum Number of Days to Eat N Oranges -- the Python
# mirror of oranges.kara, the ★ arm: the best of a halving or a thirding
# after the single days they need, each answer kept. Prints byte-identical
# output.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most):
    check = 0
    total = 0
    for _ in range(count):
        wide = (next_random() * 32768 + next_random()) * 32768 + next_random()
        n = wide % most + 1
        d = min_days(n)
        total += d
        check = mix(check, d)
    print(f"{count} piles of up to {most}: {total} days, checksum {check}")


def main():
    global seed
    for n in [10, 6, 1, 2, 3, 4, 56, 820592, 1000000000, 2000000000]:
        print(f"n = {n} -> {min_days(n)}")
    seed = 1553
    batch(3000, 1000)
    batch(300, 1000000)
    batch(100, 2000000000)


main()
