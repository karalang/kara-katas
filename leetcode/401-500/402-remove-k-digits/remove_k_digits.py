# LeetCode #402: Remove K Digits -- mirror of remove_k_digits.kara (a stack
# that keeps digits rising).


def remove_kdigits(num, k):
    left = k
    stack = []
    for c in num:
        while left > 0 and stack and stack[-1] > c:
            stack.pop()
            left -= 1
        stack.append(c)
    while left > 0:
        stack.pop()
        left -= 1
    out = "".join(stack).lstrip("0")
    return out if out else "0"


seed = 402


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(num, k):
    print(f'"{num}", k = {k}: "{remove_kdigits(num, k)}"')


def main():
    for num, k in [("1432219", 3), ("10200", 1), ("10", 2), ("9", 1), ("112", 1), ("123456", 3),
                   ("654321", 3), ("100200", 1), ("10001", 4), ("1234567890", 9), ("5337", 2),
                   ("43214321", 4)]:
        show(num, k)
    length = 0
    checksum = 0
    for _ in range(3000):
        n = 1 + step() % 40
        digits = []
        for i in range(n):
            d = 1 + step() % 9 if i == 0 else step() % 10
            digits.append(chr(48 + d))
        num = "".join(digits)
        k = step() % (n + 1)
        r = remove_kdigits(num, k)
        length += len(r)
        for b in r.encode():
            checksum = (checksum * 31 + b) % 1000000007
        checksum = (checksum * 31 + 7) % 1000000007
    print(f"3000 random numbers: {length} digits kept, checksum {checksum}")


main()
