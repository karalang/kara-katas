# LeetCode #2712: Minimum Cost to Make All Characters Equal -- the Python
# mirror of the star arm (equal.kara): each boundary between two unequal
# neighbours must be crossed by exactly one flip, an odd number in fact,
# and the cheapest flip that crosses the boundary before index i costs
# min(i, n - i), the prefix flip ending there or the suffix flip
# starting there.


def minimum_cost(s):
    n = len(s)
    cost = 0
    for i in range(1, n):
        if s[i] != s[i - 1]:
            cost += min(i, n - i)
    return cost


seed = 2712


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_bits(n, change_in_8):
    last = "0" if next_random() % 2 == 0 else "1"
    bits = [last]
    for _ in range(n - 1):
        if next_random() % 8 < change_in_8:
            last = "1" if last == "0" else "0"
        bits.append(last)
    return "".join(bits)


print(minimum_cost("0011"))
print(minimum_cost("010101"))
print(minimum_cost("1"))
print(minimum_cost("10"))
print(minimum_cost("0" * 100000))
print(minimum_cost("01" * 50000))
print(minimum_cost("0" * 50000 + "1" * 50000))
total = 0
check = 0
for _ in range(2000):
    n = next_random() % 20 + 1
    change = next_random() % 9
    cost = minimum_cost(random_bits(n, change))
    total += cost
    check = (check * 31 + cost) % 1000000007
print(f"2000 strings up to 20: costs sum to {total}, checksum {check}")
total = 0
check = 0
for _ in range(50):
    n = (next_random() * 32768 + next_random()) % 100000 + 1
    change = next_random() % 9
    cost = minimum_cost(random_bits(n, change))
    total += cost
    check = (check * 31 + cost) % 1000000007
print(f"50 strings up to 100000: costs sum to {total}, checksum {check}")
