# LeetCode #2375: Construct Smallest Number From DI String -- the bench,
# the ★ arm in Python: the digits 1 to n + 1 pushed on a stack, emptied at
# every I and at the end, so each run of D's comes out falling.


def smallest_number(pattern):
    p = pattern.encode()
    out = bytearray()
    stack = bytearray()
    for i in range(len(p) + 1):
        stack.append(49 + i)
        if i == len(p) or p[i] == 73:
            while stack:
                out.append(stack.pop())
    return out.decode()


def main():
    # every pattern of 1 to 8 letters, 510 in all
    patterns = []
    for n in range(1, 9):
        for mask in range(1 << n):
            patterns.append("".join("D" if (mask >> i) & 1 else "I" for i in range(n)))
    check = 0
    for p in range(2000):
        for pattern in patterns:
            for b in smallest_number(pattern).encode():
                check = (check * 31 + (b - 48) + p) % 1000000007
    print(f"2000 passes over 510 patterns: checksum {check}")


main()
