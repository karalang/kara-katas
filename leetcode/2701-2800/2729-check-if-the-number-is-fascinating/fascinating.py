# LeetCode #2729: Check if The Number is Fascinating -- the ★ arm
# (fascinating.kara) in Python: n, 2 n and 3 n joined, the digits sorted,
# compared with "123456789".


def is_fascinating(n):
    return "".join(sorted(f"{n}{2 * n}{3 * n}")) == "123456789"


print("true" if is_fascinating(192) else "false")
print("true" if is_fascinating(100) else "false")
print("true" if is_fascinating(999) else "false")
found = []
check = 0
for n in range(100, 1000):
    yes = is_fascinating(n)
    if yes:
        found.append(n)
    check = (check * 31 + (2 if yes else 1)) % 1000000007
print(f"[{', '.join(map(str, found))}]")
print(f"{len(found)} of 900 fascinating, checksum {check}")
