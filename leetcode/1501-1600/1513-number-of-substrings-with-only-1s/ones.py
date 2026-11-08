# LeetCode #1513: Number of Substrings With Only 1s -- the Python mirror of
# the ★ arm: each '1' ends as many all-ones substrings as the run of ones
# it ends.

MOD = 1000000007


def num_sub(s):
    run = total = 0
    for c in s:
        if c == "1":
            run += 1
            total += run
        else:
            run = 0
    return total % MOD


seed = 1513


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most):
    check = 0
    for _ in range(count):
        n = next_random() % most + 1
        tenths = next_random() % 11
        s = "".join("1" if next_random() % 10 < tenths else "0" for _ in range(n))
        check = mix(check, num_sub(s))
    return check


for s in ["0110111", "101", "111111", "000", "1"]:
    print(f'"{s}" -> {num_sub(s)}')
print(f"100000 ones -> {num_sub('1' * 100000)}")
print(f"3000 strings of 1 to 12 bits: checksum {batch(3000, 12)}")
print(f"300 strings of 1 to 1000 bits: checksum {batch(300, 1000)}")
print(f"3 strings of 1 to 100000 bits: checksum {batch(3, 100000)}")
