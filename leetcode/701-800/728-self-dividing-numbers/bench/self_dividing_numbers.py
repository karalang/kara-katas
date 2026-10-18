# LeetCode #728: Self Dividing Numbers -- each digit, by remainders.
# Benchmark mirror of the Kara star arm: peel each number's digits off
# with % 10 and // 10, stopping at a 0 or a digit that does not divide
# it, and collect the numbers that pass.


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def self_dividing(n):
    rest = n
    while rest > 0:
        d = rest % 10
        if d == 0 or n % d != 0:
            return False
        rest //= 10
    return True


def self_dividing_numbers(left, right):
    out = []
    for n in range(left, right + 1):
        if self_dividing(n):
            out.append(n)
    return out


def main():
    seed = [728]
    count = 0
    total = 0
    for _ in range(40000):
        a = 1 + next_random(seed) % 10000
        b = 1 + next_random(seed) % 10000
        left, right = min(a, b), max(a, b)
        found = self_dividing_numbers(left, right)
        count += len(found)
        total += sum(found)
    print(f"40000 random ranges: {count} numbers, sum {total}")


main()
