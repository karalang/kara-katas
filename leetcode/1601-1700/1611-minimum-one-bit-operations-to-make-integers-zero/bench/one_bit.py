# LeetCode #1611: Minimum One Bit Operations to Make Integers Zero -- the
# bench in Python, mirroring one_bit.kara: n turned back from Gray code,
# the XOR of n and all its right shifts.


def minimum_one_bit_operations(n):
    k = 0
    while n > 0:
        k ^= n
        n >>= 1
    return k


def main():
    seed = 1611

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    numbers = []
    for _ in range(10000000):
        a = next_random()
        numbers.append((a * 32768 + next_random()) % 1000000001)
    check = total = 0
    for n in numbers:
        ops = minimum_one_bit_operations(n)
        check = (check * 31 + ops + 1) % 1000000007
        total += ops
    print(f"10000000 numbers up to 10^9: total {total}, checksum {check}")


main()
