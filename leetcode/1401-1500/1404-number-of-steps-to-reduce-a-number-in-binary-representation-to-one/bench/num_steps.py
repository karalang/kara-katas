# LeetCode #1404 bench, Python: the same walk with a carry, workload and
# checksum as num_steps.kara.


def num_steps(s):
    bits = list(s)
    steps = 0
    carry = 0
    for i in range(len(bits) - 1, 0, -1):
        bit = (1 if bits[i] == "1" else 0) + carry
        if bit == 1:
            steps += 2
            carry = 1
        else:
            steps += 1
    return steps + carry


def main():
    seed = 1404
    pool = []
    for _ in range(100000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        pool.append("0" if seed // 65536 % 2 == 0 else "1")
    pool = "".join(pool)
    check = 0
    for r in range(200000):
        at = (check + r * 7919) % 99501
        s = "1" + pool[at:at + 499]
        check = (check * 131 + num_steps(s)) % 1000000007
    print(f"200000 numbers of 500 digits: checksum {check}")


main()
