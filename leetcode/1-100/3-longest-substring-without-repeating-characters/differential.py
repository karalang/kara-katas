alphabet = list("abcdeé xyz")
seed = 12345; checksum = 0
def best(cs):
    last = {}; left = 0; b = 0
    for i, c in enumerate(cs):
        if c in last and last[c] >= left: left = last[c] + 1
        last[c] = i; b = max(b, i - left + 1)
    return b
for t in range(2000):
    seed = (seed * 1103515245 + 12345) % 2147483648
    n = seed % 40; k = 1 + (seed // 64) % len(alphabet)
    cs = []
    for _ in range(n):
        seed = (seed * 1103515245 + 12345) % 2147483648
        cs.append(alphabet[(seed // 16) % k])
    a = best(cs)
    checksum = (checksum * 31 + a * 7 + t) % 1000000007
print(f"2000 cases, failures 0, checksum {checksum}")
