# LeetCode 829 — Consecutive Numbers Sum, by each run length.
#
# Mirrors consecutive_numbers_sum.kara: n has a run of k consecutive
# numbers exactly when n - k * (k - 1) / 2 is a positive multiple of k,
# and k runs while 1 + 2 + ... + k fits in n.

def consecutive_numbers_sum(n):
    count = 0
    k = 1
    while k * (k + 1) // 2 <= n:
        if (n - k * (k - 1) // 2) % k == 0:
            count += 1
        k += 1
    return count

seed = 0

def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def show(n):
    print(f"{n} -> {consecutive_numbers_sum(n)}")

for n in [5, 9, 15, 1, 2, 3, 4, 1024, 945, 1000000000, 999999937, 536870912, 918918000]:
    show(n)
total = 0
check = 0
for n in range(1, 3001):
    r = consecutive_numbers_sum(n)
    total += r
    check = (check * 131 + r) % 1000000007
print(f"1 to 3000: total {total}, checksum {check}")
seed = 829
total = 0
check = 0
for _ in range(100):
    a = next_random()
    b = next_random()
    n = 1 + (a * 32768 + b) % 1000000000
    r = consecutive_numbers_sum(n)
    total += r
    check = (check * 131 + r) % 1000000007
print(f"100 random up to 10^9: total {total}, checksum {check}")
