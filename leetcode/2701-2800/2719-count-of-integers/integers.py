# LeetCode #2719: Count of Integers -- the ★ arm (integers.kara) in
# Python: a digit-by-digit recursion up to each bound, the free places'
# counts remembered by place and sum.
import sys

sys.setrecursionlimit(10000)
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


def random_number(longest):
    n = next_random() % longest + 1
    digits = [chr(ord("1") + next_random() % 9)]
    for _ in range(1, n):
        digits.append(chr(ord("0") + next_random() % 10))
    return "".join(digits)


def at_most(a, b):
    return len(a) < len(b) or (len(a) == len(b) and a <= b)


print(count("1", "12", 1, 8))
print(count("1", "5", 1, 5))
top = "1" + "0" * 22
print(count("1", top, 1, 400))
print(count("1", top, 400, 400))
print(count("4179", "4179", 21, 21))
nines = "9" * 22
print(count(nines, nines, 198, 400))
print(count("1", nines, 99, 99))
total = 0
check = 0
for c in range(2300):
    longest, most = (4, 40) if c < 2000 else (22, 200)
    a = random_number(longest)
    b = random_number(longest)
    low = next_random() % most + 1
    high = low + next_random() % (most - low + 1)
    found = count(a, b, low, high) if at_most(a, b) else count(b, a, low, high)
    total += found
    check = (check * 31 + found) % 1000000007
    if c == 1999:
        print(f"2000 ranges up to 10^4: counts sum to {total}, checksum {check}")
        total = 0
        check = 0
print(f"300 ranges up to 22 digits: counts mod p sum to {total}, checksum {check}")
