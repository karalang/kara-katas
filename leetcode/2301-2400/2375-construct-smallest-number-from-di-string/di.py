# LeetCode #2375: Construct Smallest Number From DI String -- the Python
# mirror of the ★ arm: the digits 1 to n + 1 pushed on a stack, emptied at
# every I and at the end, so each run of D's comes out falling.


def smallest_number(pattern):
    out = []
    stack = []
    for i in range(len(pattern) + 1):
        stack.append(str(i + 1))
        if i == len(pattern) or pattern[i] == "I":
            while stack:
                out.append(stack.pop())
    return "".join(out)


def main():
    # LeetCode's two examples; one letter of each; then every pattern of
    # 1 to 8 letters, 510 in all, with a checksum of the numbers and how
    # many begin with 1
    print(smallest_number("IIIDIDDD"))
    print(smallest_number("DDD"))
    print(f"{smallest_number('I')} {smallest_number('D')}")
    check = 0
    ones = 0
    count = 0
    for n in range(1, 9):
        for mask in range(1 << n):
            letters = "".join("D" if (mask >> i) & 1 else "I" for i in range(n))
            number = smallest_number(letters)
            check = (check * 31 + int(number)) % 1000000007
            if number.startswith("1"):
                ones += 1
            count += 1
    print(f"{count} patterns: checksum {check}, {ones} begin with 1")


main()
