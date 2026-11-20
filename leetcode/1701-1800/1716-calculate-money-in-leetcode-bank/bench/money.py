# LeetCode #1716: Calculate Money in Leetcode Bank -- the Python mirror of
# the bench (money.kara): whole weeks and the days left in closed form, on
# 500000 random n, each answered 20 times.


def total_money(n):
    weeks, days = n // 7, n % 7
    return 28 * weeks + 7 * weeks * (weeks - 1) // 2 + days * (weeks + 1) + days * (days - 1) // 2


def next_random(state):
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def main():
    count = 500000
    rounds = 20
    seed = [1716]
    ns = [next_random(seed) % 1000 + 1 for _ in range(count)]
    total = 0
    check = 0
    for r in range(rounds):
        for n in ns:
            answer = total_money(n)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} values of n, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
