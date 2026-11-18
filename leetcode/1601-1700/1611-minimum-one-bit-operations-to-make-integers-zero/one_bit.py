# LeetCode #1611: Minimum One Bit Operations to Make Integers Zero -- the
# Python mirror of one_bit.kara: n turned back from Gray code, the XOR of n
# and all its right shifts.


def minimum_one_bit_operations(n):
    k = 0
    while n > 0:
        k ^= n
        n >>= 1
    return k


seed = 1611


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


for n in [3, 6, 0, 1, 2, 1024, 1023, 1000000000]:
    print(minimum_one_bit_operations(n))
check = most = 0
for n in range(4096):
    ops = minimum_one_bit_operations(n)
    check = mix(check, ops)
    most = max(most, ops)
print(f"every n below 4096: most {most}, checksum {check}")
check = total = 0
for _ in range(100000):
    a = next_random()
    n = (a * 32768 + next_random()) % 1000000001
    ops = minimum_one_bit_operations(n)
    check = mix(check, ops)
    total += ops
print(f"100000 random n to 10^9: total {total}, checksum {check}")
