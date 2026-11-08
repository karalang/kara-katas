# LeetCode #1513: Number of Substrings With Only 1s -- the bench: 20
# strings of 500000 bits built once, then each counted five times by the
# ★ arm.

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


strings = ["".join("1" if next_random() % 20 < k else "0" for _ in range(500000)) for k in range(20)]
check = 0
for _ in range(5):
    for s in strings:
        check = (check * 31 + num_sub(s) + 1) % 1000000007
print(f"100 counts over 20 strings of 500000 bits: checksum {check}")
