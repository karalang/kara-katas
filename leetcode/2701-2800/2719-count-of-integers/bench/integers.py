# LeetCode #2719: Count of Integers -- the bench (integers.kara in
# Python): the good numbers up to each bound by a digit-by-digit
# recursion, a free place's count remembered by place and digit sum.
MOD = 1000000007


def good_up_to(bound, min_sum, max_sum):
    digits = [ord(b) - 48 for b in bound]
    memo = [[-1] * (max_sum + 1) for _ in digits]

    def walk(place, total, tight):
        if total > max_sum:
            return 0
        if place == len(digits):
            return 1 if total >= min_sum else 0
        if not tight and memo[place][total] >= 0:
            return memo[place][total]
        top = digits[place] if tight else 9
        ways = 0
        for d in range(top + 1):
            ways = (ways + walk(place + 1, total + d, tight and d == top)) % MOD
        if not tight:
            memo[place][total] = ways
        return ways

    return walk(0, 0, True)


def count(num1, num2, min_sum, max_sum):
    own = sum(ord(b) - 48 for b in num1)
    itself = 1 if min_sum <= own <= max_sum else 0
    return (good_up_to(num2, min_sum, max_sum) - good_up_to(num1, min_sum, max_sum) + itself + MOD) % MOD


seed = 2719


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


ranges, rounds = 300, 10
problems = []
for _ in range(ranges):
    a = [chr(ord("1") + next_random() % 4)]
    b = [chr(ord("5") + next_random() % 5)]
    for _ in range(1, 22):
        a.append(chr(ord("0") + next_random() % 10))
        b.append(chr(ord("0") + next_random() % 10))
    low = next_random() % 400 + 1
    high = low + next_random() % (401 - low)
    problems.append(("".join(a), "".join(b), low, high))
total = 0
check = 0
for r in range(rounds):
    for num1, num2, low, high in problems:
        found = count(num1, num2, low, high)
        total += found
        check = (check * 31 + found + r) % 1000000007
print(f"{ranges} ranges of 22 digits, {rounds} rounds: counts mod p sum to {total}, checksum {check}")
